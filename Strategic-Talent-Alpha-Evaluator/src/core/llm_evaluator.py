import os
import json
import hashlib
import time
from src.utils.logger import SYSTEM_LOGGER

# ==========================================
# 🧠 V6.0 LLM 战略裁决大脑 (带精确指纹缓存层)
# ==========================================

# 👑 【高管面试展示区】这是系统真实运作时挂载的 System Prompt (提示词工程)
SYSTEM_PROMPT = """
你现在是顶尖科技公司的CTO。任务是对候选人项目进行评估，输出严格的JSON格式。
【最高纲领：反虚假繁荣与诚实溢价】

1. 寻找肌肉记忆（击杀PPT战神）：
   无视“0到1、赋能、商业闭环”等宏大叙事。强制向下寻找脏活累活。若无“修复、重构、配置、优化、排障”等具体动词，直接判定为虚假繁荣。

2. 严密计算“吹牛杠杆率” (Bullshit Leverage Ratio)：
   在后台执行计算：商业黑话频次 ÷ 真实技术动词频次。
   - 若比值 > 2（黑话极多，动词极少），设为 "High"。
   - 若比值 < 1（全是干活细节，没有废话），设为 "Low"。

3. 赋予诚实溢价（保护真正的螺丝钉）：
   若候选人只负责局部底层模块，没有吹嘘主导全局，且逻辑自洽，判定为 true。

4.【最高评估法则：证据权重 (Evidence-Based Evaluation)】
绝对不要仅仅因为候选人使用了“千万级、主导、赋能、AI 架构”等宏大词汇（Claim）就给予高分。你必须执行严格的**【主张-证据一致性校验】**：
    1. 提取核心主张 (Claim)：找出他最引以为傲的业绩。
    2. 搜寻底层证据 (Evidence)： 不要看他的态度是否谦虚，必须去寻找“灵魂 7 问”的答案：
         2.1写了什么具体模块？
         2.2改了哪段核心逻辑？
         2.3代码部署在哪里？
         2.4业务上下游谁在使用？
         2.5出现过什么线上事故（如 OOM、死锁）？
         2.6如何定位排障的？
         2.7哪个具体的量化指标得到了改善?
    3. 计算自洽度 (Consistency)：只有当候选人的核心主张（Claim）能与上述细节（Evidence）完美吻合，且作用边界（Scope）清晰时，才可将 consistency_score 评定为 High。仅表现出“谦虚”但缺乏上述技术细节，最多评为 Medium。
    4. 对这种“脱实向虚”的简历，实施残酷的降维打击。

必须输出JSON结构：
{
    "bullshit_ratio": "Low/Medium/High",
    "integrity_tag": true/false,
    "strategic_advice": "20字以内的极度冷酷/赞赏短评",
    "evidence_matrix": {
        "core_claim": "最核心的主张",
        "supporting_evidence": ["证据1", "证据2"],
        "missing_evidence": ["缺失证据1"],
        "consistency_score": "High/Medium/Low"
    }
}
"""

class LLMEvaluator:
    """
    V6.0 终极大脑：带精确指纹缓存的 LLM 质证引擎
    """
    def __init__(self, cache_dir="data/04_cache"):
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(cache_dir, "llm_evidence_cache.json")
        self.cache_db = self._load_cache()
        
        # ⚠️ 这里是你未来填入 DeepSeek API Key 的地方
        self.api_key = "sk-your-deepseek-api-key-here"

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
            json.dump(self.cache_db, f, ensure_ascii=False, indent=4)

    # 🚀 新老融合点 1：将证据图谱(evidence_graph)一起卷入 MD5 哈希计算！
    def _generate_fingerprint(self, text, evidence_graph="{}"):
        if not text:
            text = "empty_text_fingerprint"
        
        # 将项目描述和前置规则引擎收集的证据合体，确保哈希的绝对唯一性
        combined_context = f"TEXT:{text} | EVIDENCE:{evidence_graph}"
        normalized_text = combined_context.strip().lower()
        
        return hashlib.md5(normalized_text.encode('utf-8')).hexdigest()

    # 🚀 新老融合点 2：接收 pipeline 传来的第二个参数 (evidence_graph)
    def evaluate_project(self, project_desc: str, evidence_graph: str = "{}") -> dict:
        """主入口：先查缓存，没有再调取核心引擎"""
        fingerprint = self._generate_fingerprint(project_desc, evidence_graph)
        
        if fingerprint in self.cache_db:
            SYSTEM_LOGGER.info(f"⚡ [LLM Cache 命中] 提取历史指纹 {fingerprint[:8]}... 耗时: 0ms (免流)")
            return self.cache_db[fingerprint]

        SYSTEM_LOGGER.info(f"🌐 [LLM Cache 未命中] 呼叫大脑进行逻辑质证...")
        start_time = time.time()

        # 呼叫底层逻辑 (传入文本与前置证据)
        result = self._call_deepseek_api(project_desc, evidence_graph)
        
        end_time = time.time()
        SYSTEM_LOGGER.info(f"✅ [大脑响应成功] 耗时: {end_time - start_time:.2f}s")

        self.cache_db[fingerprint] = result
        self._save_cache()
        return result

    # 🚀 新老融合点 3：底层 API 接口签名同步，内部完全保留你牛逼的 Mock 逻辑
    def _call_deepseek_api(self, project_desc: str, evidence_graph: str = "{}") -> dict:
        """
        [V6.0 离线压测挡板 / Mock Mode] 
        原封不动保留的历史逻辑。在接入真实 API 前保障系统不雪崩的物理防线。
        """
        # 模拟网络调用延迟
        time.sleep(0.5)
        
        if not project_desc or len(project_desc) < 10:
            return {
                "bullshit_ratio": "N/A", 
                "integrity_tag": False, 
                "strategic_advice": "信息缺失，无法评估",
                "evidence_matrix": {
                    "core_claim": "无有效文本",
                    "supporting_evidence": [],
                    "missing_evidence": ["简历内容过短"],
                    "consistency_score": "Low"
                }
            }
            
        try:
            # 🚨 触发 PPT战神 拦截逻辑
            if "赋能" in project_desc or "闭环" in project_desc or "0到1" in project_desc:
                return {
                    "bullshit_ratio": "High", 
                    "integrity_tag": False, 
                    "strategic_advice": "满纸黑话无排障细节，建议直接淘汰",
                    "evidence_matrix": {
                        "core_claim": "从0到1实现全链路商业闭环与生态赋能",
                        "supporting_evidence": ["无底层代码痕迹"],
                        "missing_evidence": ["具体的架构图", "QPS压测数据", "任何一行真实的排障代码"],
                        "consistency_score": "Low"
                    }
                }
                
            # 🛡️ 触发 诚实螺丝钉 护航逻辑
            elif "内存泄漏" in project_desc or "300行" in project_desc or "OOM" in project_desc:
                return {
                    "bullshit_ratio": "Low", 
                    "integrity_tag": True, 
                    "strategic_advice": "诚实的局部破局者，逻辑自洽，立刻面试",
                    "evidence_matrix": {
                        "core_claim": "排查并修复内存泄漏问题，重构底层逻辑",
                        "supporting_evidence": ["明确指出了 OOM/内存泄漏", "界定了具体的工作量边界"],
                        "missing_evidence": ["无"],
                        "consistency_score": "High"
                    }
                }

            # 🚀 极简扫地僧护航 (字数少，但全是核心痛点)
            elif len(project_desc) < 50 and any(k in project_desc for k in ["重构", "OOM", "P99", "底层", "死锁"]):
                return {
                    "bullshit_ratio": "Low", 
                    "integrity_tag": True, 
                    "strategic_advice": "字少事大！极简扫地僧，命中核心痛点，务必面谈！",
                    "evidence_matrix": {
                        "core_claim": "高度浓缩的底层排障或架构重构",
                        "supporting_evidence": ["文本极短但直接命中核心复杂场景 (如 P99/OOM)"],
                        "missing_evidence": ["无废话"],
                        "consistency_score": "High"  
                    }
                }
     
            # 🟡 常规平庸简历
            else:
                return {
                    "bullshit_ratio": "Medium", 
                    "integrity_tag": False, 
                    "strategic_advice": "平庸的业务执行者，缺乏亮点",
                    "evidence_matrix": {
                        "core_claim": "按时完成业务需求开发",
                        "supporting_evidence": ["参与了常规模块编写"],
                        "missing_evidence": ["缺乏深度调优细节", "没有高可用架构经验"],
                        "consistency_score": "Medium"
                    }
                }
               
        except Exception as e:
            SYSTEM_LOGGER.error(f"❌ 神经中枢连接断裂: {str(e)}")
            return {
                "bullshit_ratio": "ERROR", 
                "integrity_tag": False, 
                "strategic_advice": "LLM 引擎熔断",
                "evidence_matrix": {
                    "core_claim": "系统解析崩溃",
                    "supporting_evidence": ["无有效数据"],
                    "missing_evidence": ["数据流中断"],
                    "consistency_score": "Low"
                }
            }

# ==========================================
# 🔌 向后兼容接口 (Backward Compatibility)
# ==========================================
# 实例化全局评估引擎，确保 pipeline.py 调用此文件时不会报错
_evaluator_instance = LLMEvaluator()

def deepseek_strategic_scan(project_desc: str, evidence_graph: str = "{}") -> dict:
    """供外部 pipeline 调用的统一接口，自动经过缓存层路由"""
    return _evaluator_instance.evaluate_project(project_desc, evidence_graph)