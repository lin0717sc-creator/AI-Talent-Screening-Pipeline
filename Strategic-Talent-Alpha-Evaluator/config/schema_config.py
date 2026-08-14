class AISchemaRegistry:
    """
    大模型输出宪法：严格定义 AI 返回的评估数据结构
    """
    TALENT_EVALUATION_SCHEMA = {
        "type": "object",
        "properties": {
            "candidate_id": {
                "type": "string",
                "description": "候选人唯一标识符 (Email或ID)"
            },
            "capability_score": {
                "type": "number",
                "description": "技术与项目综合能力得分"
            },
            "stability_score": {
                "type": "number",
                "description": "稳定性底线得分"
            },
            "talent_alpha": {
                "type": "number",
                "description": "加权后的最终商业 Alpha 值"
            },
            "is_high_risk": {
                "type": "boolean",
                "description": "是否触发了稳定性或技术底线熔断"
            },
            "risk_tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "触发的风控标签，如没有则为空数组"
            },
            "strategic_advice": {
                "type": "string",
                "description": "用一句话给 HR 的战略聘用建议"
            }
        },
        # 【强控主权】：这些字段一个都不准少！必须强制返回！
        "required": [
            "candidate_id", 
            "capability_score", 
            "stability_score", 
            "talent_alpha", 
            "is_high_risk", 
            "strategic_advice"
        ],
        "additionalProperties": False  # 绝对禁止大模型自己捏造额外字段
    }