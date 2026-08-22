# ==========================================
# 用于剥离大模型 <thought_process> 标签、提取纯净 JSON 并拦截报错的动作
# ==========================================
import json
import re
from jsonschema import validate, ValidationError
from config.schema_config import AISchemaRegistry

class JSONEnforcer:
    """
    大模型输出执法者：负责提取思维链(CoT)、清洗废话、校验格式、触发熔断
    """
    def __init__(self):
        # 挂载前端定好的宪法 (Schema)
        self.schema = AISchemaRegistry.TALENT_EVALUATION_SCHEMA

    def clean_llm_noise(self, raw_output):
        """
        物理剥离大模型的废话、提取 <thought_process>，并强行榨取纯净 JSON 资产
        """
        text = str(raw_output).strip()
        
        # 🚀 绞杀暗坑三（V2.0 新增）：提取并打印 AI 的“内心戏”用于后台审计
        thought_match = re.search(r'<thought_process>(.*?)</thought_process>', text, re.DOTALL)
        if thought_match:
            print(f"🧠 [AI 批判性推演日志]:\n{thought_match.group(1).strip()}\n" + "-"*40)
        
        # 🚨 终极防 IDE 截断写法：用 `{3}` 代替连续三个反引号
        # 绞杀暗坑二：剔除 Markdown 代码块包裹
        if text.startswith('`'):
            # 匹配顶格的三个反引号 (不管后面带不带 json)
            text = re.sub(r'^`{3}(?:json)?\s*', '', text)
            # 匹配结尾的三个反引号
            text = re.sub(r'\s*`{3}$', '', text)
            
        # 绞杀暗坑一：用正则强行提取第一个 { 和最后一个 } 之间的内容
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return text

    def validate_and_repair(self, llm_output, max_retries=3):
        """
        核心验证引擎：带暴力熔断与自动重试机制
        """
        attempt = 0
        current_input = llm_output
        
        while attempt < max_retries:
            try:
                # 1. 物理清洗噪声 (现已包含 CoT 思维链剥离功能)
                cleaned_text = self.clean_llm_noise(current_input)
                
                # 2. 尝试解析 JSON (拦截非标准引号、缺少逗号等错误)
                parsed_json = json.loads(cleaned_text)
                
                # 3. 宪法校验 (拦截类型错误、缺少必填字段等)
                validate(instance=parsed_json, schema=self.schema)
                
                # 如果顺利走到这里，说明是纯净的黄金数据！
                print("✅ [落锁成功] 真实评估分数已剥离并经过 Schema 验证。")
                return parsed_json
                
            except (json.JSONDecodeError, ValidationError) as e:
                attempt += 1
                # 终端强制爆红预警
                print(f"⚠️ [熔断警报] 第 {attempt} 次解析失败。原因: {str(e)[:50]}...")
                print("🚨 报告指挥官，检测到噪声干扰，格式锁死引擎已启动自动修复！")
                
                # 达到最大重试次数后直接返回兜底数据
                if attempt == max_retries:
                    print("❌ 修复上限耗尽。强制启动防崩溃兜底预案！")
                    return self._generate_fallback_json()

    def _generate_fallback_json(self):
        """防止后端彻底宕机的兜底数据 (Fallback)"""
        return {
            "candidate_id": "SYS_ERROR_FALLBACK",
            "capability_score": 0,
            "stability_score": 0,
            "talent_alpha": 0,
            "is_high_risk": True,
            "risk_tags": ["FORMAT_CORRUPTION", "LLM_HALLUCINATION"],
            "strategic_advice": "数据解析严重崩溃，此候选人档案已隔离，需人工介入。"
        }