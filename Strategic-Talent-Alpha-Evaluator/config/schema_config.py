# ==========================================
# 战略意义: 大模型输入/输出的双重宪法中心 (V3.0 解耦瘦身版)
# ==========================================

# 🚀 架构师主权动作：从外部冷库导入庞大的 Few-Shot 种子资产
from config.few_shot_seeds import FEW_SHOT_EXAMPLES

class AIPromptRegistry:
    """
    大模型输入宪法：强制思维链 (CoT) 与输出规范模板
    """
    # 巧妙利用字符串拼接 (+ FEW_SHOT_EXAMPLES +) 完成物理合拢，让模板保持极致精简！
    EVALUATION_PROMPT_TEMPLATE = """
你现在是一位冷酷、极度严苛的跨国大厂 HR 战略总监。
请对以下候选人简历进行冰冷的量化打分。

【MGT567 战略人力资本核心定义（强制对齐）】
1. 胜任力密度与业务敏锐度：指候选人硬核技术栈与真实商业收益的结合程度。仅罗列工具而无量化商业产出的描述，视为低效密度。
2. 推演逻辑一致性：指候选人履历中因果关系的严密性。若宣称了宏大结果但缺乏具体架构、排障细节，即视为逻辑跳跃与简历注水。
3. 包容性盲选机制：作为大厂红线，彻底忽略性别、年龄、国籍噪音，100% 聚焦于代码主权与业务产出。

【最高评估法则：证据权重 (Evidence-Based Evaluation)】
绝对不要仅仅因为候选人使用了“千万级、主导、赋能、AI 架构”等宏大词汇（Claim）就给予高分。你必须执行严格的【主张-证据一致性校验】：
1. 提取核心主张 (Claim)：找出他最引以为傲的业绩或头衔。
2. 搜寻底层证据 (Evidence)：像顶尖技术面试官一样，去寻找“架构设计、QPS、并发死锁处理、缓存穿透排障、具体部署环境、真实代码行数”等肌肉记忆。
3. 计算自洽度 (Consistency)：如果主张了宏大叙事但缺乏底层细节支撑（或未能清晰界定局部产出），将 consistency_score 判为 Low。
4. 对“脱实向虚”的简历，必须在 evidence_matrix 中明确指出缺失的证据，并实施残酷降权。

【强控输出规范】
你必须严格按照以下两步输出：

第一步：强制批判性思考
在 <thought_process> 标签内写下减分推演。
🚨 【基准分死锁指令】：基础能力分固定为 100 分，推演只能做减法扣分。严禁自行发明分数上限格式（如 15/40）！

第二步：输出最终评估结果
输出纯净 JSON。
🚨 【枚举字典死锁指令】：risk_tags 必须且只能从以下字典挑选（严禁造词）：
["Logical_Inconsistency", "Low_Business_Acumen", "PPT_Warrior_Risk", "Credential_Inflation_Risk", "Unverifiable_Business_Claims", "Knowledge_Decay_Risk", "Zero_Code_Sovereignty"]

【输出格式示例】
""" + FEW_SHOT_EXAMPLES + """

【候选人简历输入】：
{resume_text}
"""

class AISchemaRegistry:
    """
    大模型输出宪法：严格定义 AI 返回的评估数据结构 (Schema 不变 + 证据矩阵)
    """
    TALENT_EVALUATION_SCHEMA = {
        "type": "object",
        "properties": {
            "candidate_id": {"type": "string"},
            "capability_score": {"type": "number"},
            "stability_score": {"type": "number"},
            "talent_alpha": {"type": "number"},
            "is_high_risk": {"type": "boolean"},
            "risk_tags": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "Logical_Inconsistency", 
                        "Low_Business_Acumen", 
                        "PPT_Warrior_Risk", 
                        "Credential_Inflation_Risk", 
                        "Unverifiable_Business_Claims", 
                        "Knowledge_Decay_Risk", 
                        "Zero_Code_Sovereignty"
                    ]
                }
            },
            "strategic_advice": {"type": "string"},
            
            # 🚀 架构师重点：新增 Evidence Matrix (证据矩阵)
            "evidence_matrix": {
                "type": "object",
                "properties": {
                    "core_claim": {
                        "type": "string",
                        "description": "候选人简历中吹得最大的牛/最核心的主张（例如：负责千万级高并发系统）"
                    },
                    "supporting_evidence": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "支撑该主张的底层技术细节（如：QPS、降级策略、内存泄漏排障等）"
                    },
                    "missing_evidence": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "该级别主张本应该有，但候选人根本没写的关键证据"
                    },
                    "consistency_score": {
                        "type": "string",
                        "enum": ["High", "Medium", "Low"],
                        "description": "主张与证据的匹配度。缺乏细节则判为 Low。"
                    }
                },
                "required": ["core_claim", "supporting_evidence", "missing_evidence", "consistency_score"]
            }
        },
        # 🚨 终极死锁：在此处强制要求 LLM 必须吐出 evidence_matrix 字段！
        "required": ["candidate_id", "capability_score", "stability_score", "talent_alpha", "is_high_risk", "strategic_advice", "evidence_matrix"],
        "additionalProperties": False
    }