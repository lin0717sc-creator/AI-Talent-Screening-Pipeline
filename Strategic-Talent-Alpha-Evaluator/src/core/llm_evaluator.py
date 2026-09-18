import os
import json
import hashlib
import time
import re
from openai import OpenAI, RateLimitError, APIConnectionError, APITimeoutError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from src.utils.logger import SYSTEM_LOGGER

# ==========================================
# 🧠 V7.1 2-Pass Hybrid 战略大脑 (物理分层 + Python拦截网)
# ==========================================

# ----------------- PASS 1：绝对中立的事实提取器 -----------------
PASS1_PROMPT = """
你现在是绝对中立的【事实提取器 (Data Extractor)】。
你的唯一任务是：从输入文本中提取候选人的核心技术主张，并找出支撑该主张的原文。
【纪律要求】：
1. 严禁进行任何评价、打分或真伪判断。
2. `evidence_span` 必须 100% 逐字复制原文。如果找不到直接对应的原话，必须填 "None"。

严格输出以下 JSON：
{
    "extracted_claims": [
        {
            "claim_id": "C01",
            "skill_claim": "候选人的技术或业务主张",
            "evidence_span": "必须是原文中的原话子串，找不到填 None"
        }
    ]
}
"""

# ----------------- PASS 2：毫不留情的对抗审判官 -----------------
PASS2_PROMPT = """
你现在是顶尖科技公司的【CTO与对抗性审查官 (Adversarial Verifier)】。
你将收到一份候选人的简历原文，以及一份【经过系统严格校验的客观主张清单】。
请基于这些铁证，进行冷酷的抗欺诈审查，并输出 JSON。

【最高纲领】
1. 严密计算“Claim-to-Evidence Ratio (主张实证倒挂率)”：商业黑话频次 ÷ 真实技术动词频次。(>2为High, <1为Low)。
2. 【四态无罪推论】：对每个主张进行状态判定。
   - SUPPORTED: 主张与证据完美闭环。
   - PARTIALLY_SUPPORTED: 缺乏深度细节。
   - CONTRADICTED: 时间线、逻辑错乱或被系统标记为造假。
   - INSUFFICIENT_EVIDENCE: 只有主张，证据为 None。
3. 🚨【探针多样性与反作弊 (Anti-Gaming)】：
   针对 INSUFFICIENT_EVIDENCE 的主张，必须生成刀刀见血的追问。严禁生成“你是怎么做的”这种废话。
   你必须从以下【问题族】中，随机抽取 1-2 个维度生成具体拷问：
   - [Baseline / 基线]: 追问优化前的数据、基准线。（例如：降低40%成本，原先的基数是多少？）
   - [Ownership / 归属]: 剥离团队包装，追问具体手写量。（例如：哪一行核心代码是你亲自提交的？）
   - [Failure / 失败边界]: 拷问方案的阴暗面。（例如：上线后引发过什么副作用或 OOM 故障？）
   - [Trade-off / 权衡]: 极限施压。（例如：如果流量瞬间暴增 3 倍，最先崩溃的是哪个组件？）
   - [Counterfactual / 反事实]: 考验技术视野。（例如：如果不修改当前的中间件，还有什么替代方案？）

严格按照以下 JSON 输出格式返回：
{
    "bullshit_ratio": "Low/Medium/High",
    "integrity_tag": true/false,
    "strategic_advice": "20字以内的极度冷酷/赞赏短评",
    "claim_verdicts": [
        {
            "claim_id": "对应输入的C01等编号",
            "evidence_strength": "Strong/Weak/None",
            "verification_status": "SUPPORTED / PARTIALLY_SUPPORTED / CONTRADICTED / INSUFFICIENT_EVIDENCE"
        }
    ],
    "interview_probes": [
        "[Ownership] 你提到重构了核心交易链路，具体是哪个核心类的锁机制是你亲自手写的？",
        "[Failure] 缓存优化上线后的第一个月，出现过最严重的缓存击穿故障是什么？"
    ]
}
"""

class LLMEvaluator:
    """
    V7.1 终极大脑：2-Pass Hybrid 架构 + Python 中间件校验
    """
    def __init__(self, cache_dir="data/04_cache"):
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(cache_dir, "llm_evidence_cache.json")
        self.cache_db = self._load_cache()
        # ⚠️ 这里填入你的真实 API Key
        self.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    def _load_cache(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_cache(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache_db, f, ensure_ascii=False, indent=2)

    # ==========================================
    # 🧬 算法层：SimHash (64-bit) 与 Jaccard 计算
    # ==========================================
    @staticmethod
    def _compute_simhash(text: str) -> int:
        """为文本生成 64 位 SimHash 局部敏感哈希指纹"""
        if not text: return 0
        tokens = re.findall(r'[\w]+', text.lower())
        if not tokens: return 0 
        v = [0] * 64
        for token in tokens:
            token_hash = int(hashlib.md5(token.encode('utf-8')).hexdigest()[:16], 16)
            for i in range(64):
                bit = (token_hash >> i) & 1
                v[i] += 1 if bit else -1
        fingerprint = 0
        for i in range(64):
            if v[i] > 0:
                fingerprint |= (1 << i)
        return fingerprint

    @staticmethod
    def _hamming_distance(h1: int, h2: int) -> int:
        """计算两个 64 位哈希值的汉明距离"""
        return bin(h1 ^ h2).count('1')

    @staticmethod
    def _jaccard_similarity(text_a: str, text_b: str) -> float:
        """二次确认：计算 Token 级 Jaccard 相似度"""
        set_a = set(re.findall(r'[\w]+', text_a.lower()))
        set_b = set(re.findall(r'[\w]+', text_b.lower()))
        if not set_a or not set_b: return 0.0
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        return intersection / union if union > 0 else 0.0

    # ==========================================
    # 🚀 断路器与指数退避装甲 
    # ==========================================
    @retry(
        retry=retry_if_exception_type((RateLimitError, APIConnectionError, APITimeoutError)),
        wait=wait_exponential(multiplier=2, min=2, max=32),
        stop=stop_after_attempt(3), 
        reraise=True 
    )
    def _invoke_llm_with_retry(self, client, messages):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.0
        )
        # 🛡️ 强化版 JSON 剥离装甲
        res = response.choices[0].message.content.strip() # 第一步：先干掉前后的空白和换行！
        if res.startswith("```json"): 
            res = res[7:]
        elif res.startswith("```"): # 兼容模型偶尔只写 ``` 而不写 json 的情况
            res = res[3:]
            
        res = res.strip() # 剥离头部后，再清一次内部可能的换行
        
        if res.endswith("```"): 
            res = res[:-3]
            
        return json.loads(res.strip())

    # ==========================================
    # 🛡️ 继承旧版的物理降级与兜底保护机制
    # ==========================================
    def _fallback_evaluation(self, project_desc: str, error_msg: str) -> dict:
        SYSTEM_LOGGER.error(f"❌ 真实神经中枢连接断裂或跳闸: {error_msg}")
        try:
            if "赋能" in project_desc or "闭环" in project_desc or "0到1" in project_desc:
                return {
                    "bullshit_ratio": "High", 
                    "integrity_tag": False, 
                    "strategic_advice": "满纸黑话无排障细节，建议直接淘汰",
                    "claim_modeling": [],
                    "interview_probes": ["系统熔断降级，建议重点追问底层实现细节"]
                }
            elif len(project_desc) < 50 and any(k in project_desc for k in ["重构", "OOM", "P99", "底层", "死锁"]):
                return {
                    "bullshit_ratio": "Low", 
                    "integrity_tag": True, 
                    "strategic_advice": "字少事大！极简扫地僧，务必面谈！",
                    "claim_modeling": [],
                    "interview_probes": ["系统熔断降级，命中硬核底盘词汇，直接技术面实测"]
                }
            else:
                return {
                    "bullshit_ratio": "Medium", 
                    "integrity_tag": False, 
                    "strategic_advice": "平庸业务执行者或系统降级无法深入扫描",
                    "claim_modeling": [],
                    "interview_probes": ["需人工复核"]
                }
        except:
            return {
                "bullshit_ratio": "ERROR", 
                "integrity_tag": False, 
                "strategic_advice": "系统彻底熔断",
                "claim_modeling": [],
                "interview_probes": ["数据流中断"]
            }

    # ==========================================
    # 👑 核心：2-Pass 业务编排与 Python 拦截网
    # ==========================================
    def _run_2pass_pipeline(self, project_desc: str, evidence_graph: str) -> dict:
        client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com/v1")
        
        # ----------- PASS 1: 提取事实 -----------
        msg_pass1 = [
            {"role": "system", "content": PASS1_PROMPT},
            {"role": "user", "content": f"<EVIDENCE_SOURCE>\n{project_desc}\n</EVIDENCE_SOURCE>"}
        ]
        SYSTEM_LOGGER.info("    ├─ [Pass 1] 启动中立事实提取...")
        pass1_res = self._invoke_llm_with_retry(client, msg_pass1)
        
        # ----------- MIDDLEWARE: Python 物理校验拦截幻觉 -----------
        validated_claims = []
        for claim in pass1_res.get("extracted_claims", []):
            span = claim.get("evidence_span", "None")
            # 🚨 核心风控：如果模型说有证据，但在原文找不到，直接处决该证据！
            if span != "None" and span not in project_desc:
                SYSTEM_LOGGER.warning(f"    │  ⚠️ 捕获模型幻觉！捏造证据: '{span}' (已物理清空)")
                claim["evidence_span"] = "None" 
                claim["system_flag"] = "HALLUCINATION_DETECTED"
            validated_claims.append(claim)
            
        # ----------- PASS 2: 对抗性质证 -----------
        msg_pass2 = [
            {"role": "system", "content": PASS2_PROMPT},
            {"role": "user", "content": f"<VALIDATED_CLAIMS>\n{json.dumps(validated_claims, ensure_ascii=False)}\n</VALIDATED_CLAIMS>\n<ORIGINAL_TEXT>\n{project_desc}\n</ORIGINAL_TEXT>"}
        ]
        SYSTEM_LOGGER.info("    ├─ [Pass 2] 启动对抗性审判...")
        pass2_res = self._invoke_llm_with_retry(client, msg_pass2)
        
        # ----------- ADAPTER: 组装输出，对齐 V7.0 Pipeline 契约 -----------
        # 巧妙地将 Pass 1 的 claim 事实和 Pass 2 的 verdict 判决合并，生成 pipeline.py 需要的 claim_modeling 结构
        final_claim_modeling = []
        verdicts_map = {v.get("claim_id"): v for v in pass2_res.get("claim_verdicts", [])}
        
        for claim in validated_claims:
            c_id = claim.get("claim_id")
            verdict = verdicts_map.get(c_id, {})
            final_claim_modeling.append({
                "skill_claim": claim.get("skill_claim"),
                "evidence_span": claim.get("evidence_span"),
                "evidence_strength": verdict.get("evidence_strength", "None"),
                "verification_status": verdict.get("verification_status", "INSUFFICIENT_EVIDENCE")
            })
            
        return {
            "bullshit_ratio": pass2_res.get("bullshit_ratio", "Medium"),
            "integrity_tag": pass2_res.get("integrity_tag", False),
            "strategic_advice": pass2_res.get("strategic_advice", "无建议"),
            "claim_modeling": final_claim_modeling,
            "interview_probes": pass2_res.get("interview_probes", [])
        }


    # ==========================================
    # 🛡️ 主入口与三级缓存漏斗
    # ==========================================
    def evaluate_project(self, project_desc: str, evidence_graph: str = "{}") -> dict:
        """
        三级缓存穿透漏斗：MD5 -> SimHash -> 真实 API 调用
        """
        combined_context = f"TEXT:{project_desc.strip()} | EVIDENCE:{evidence_graph.strip()}"
        exact_hash = hashlib.md5(combined_context.encode('utf-8')).hexdigest()
        
        # 🚀 [Tier 1]: 精确匹配 (Canonical Exact Cache，MD5)
        if exact_hash in self.cache_db:
            SYSTEM_LOGGER.info(f"⚡ [L1 Exact Cache 命中] MD5: {exact_hash[:8]}... 0ms 免流返回")
            return self.cache_db[exact_hash]["result"]

        # 🚀 [Tier 2]: 模糊匹配 (Near-Duplicate SimHash Cache)
        current_simhash = self._compute_simhash(project_desc)
        for cached_hash, cache_entry in self.cache_db.items():
            if cache_entry.get("simhash", 0) == 0: continue
            if self._hamming_distance(current_simhash, cache_entry["simhash"]) <= 3:
                if self._jaccard_similarity(project_desc, cache_entry.get("source_text", "")) >= 0.85:
                    SYSTEM_LOGGER.info(f"🎯 [L2 SimHash 近似命中] 成功免流！")
                    self.cache_db[exact_hash] = {"simhash": current_simhash, "source_text": project_desc, "result": cache_entry["result"]}
                    self._save_cache()
                    return cache_entry["result"]

        # 🚀 [Tier 3]: 真实调用并注册索引
        SYSTEM_LOGGER.info(f"🌐 [Cache 全未命中] 启动 V7.1 2-Pass 双轨验证机制...")
        start_time = time.time()
        
        try:
            result = self._run_2pass_pipeline(project_desc, evidence_graph)
        except Exception as e:
            # 🚀 发生崩溃时，完美衔接旧代码的物理降级逻辑
            result = self._fallback_evaluation(project_desc, str(e))

        SYSTEM_LOGGER.info(f"✅ [2-Pass 验证完成] 耗时: {time.time() - start_time:.2f}s")

        self.cache_db[exact_hash] = {"simhash": current_simhash, "source_text": project_desc, "result": result}
        self._save_cache()
        return result