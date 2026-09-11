import sys
import os
# 往上跳两级，精准锚定项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)

import json

# 🚀 强行拉齐交通网络，保证能找到 config 和 src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.json_validator import JSONEnforcer

def simulate_battlefield():
    enforcer = JSONEnforcer()

    print("\n--- 🟢 测试 1：纯净的黄金数据 ---")
    # 🚨 修复：在 strategic_advice 后加上了 evidence_matrix
    good_data = '{"candidate_id": "lin@test.com", "capability_score": 85, "stability_score": 90, "talent_alpha": 87.5, "is_high_risk": false, "risk_tags": [], "strategic_advice": "强烈建议录用", "evidence_matrix": {"core_claim": "精通数据流水线设计", "supporting_evidence": ["独立完成了数据清洗和落锁"], "missing_evidence": ["无大厂高并发经验"], "consistency_score": "High"}}'
    result1 = enforcer.validate_and_repair(good_data)
    print("✅ 成功解析:", result1['candidate_id'])

    print("\n--- 🟡 测试 2：带有 Markdown 和废话的脏数据 ---")
    # 🚨 修复：1. 改了合规的 risk_tags (PPT_Warrior_Risk)；2. 加了 evidence_matrix
    dirty_data = '''好的指挥官，这是你要的JSON：
    ```json
    {
        "candidate_id": "dirty@test.com", 
        "capability_score": 60, 
        "stability_score": 40, 
        "talent_alpha": 50, 
        "is_high_risk": true, 
        "risk_tags": ["PPT_Warrior_Risk"], 
        "strategic_advice": "外包可接，全职慎用",
        "evidence_matrix": {
            "core_claim": "全栈架构大牛",
            "supporting_evidence": [],
            "missing_evidence": ["没有任何底层代码和排障细节"],
            "consistency_score": "Low"
        }
    }
    ```
    希望对您有帮助！'''
    result2 = enforcer.validate_and_repair(dirty_data)
    print("✅ 成功剥离废话并解析:", result2['candidate_id'])

    print("\n--- 🔴 测试 3：恶意篡改类型与少字段（暴力熔断测试） ---")
    # 这个数据本来就是用来测试系统防崩溃的，所以不用加 evidence_matrix，让它继续报错并触发兜底就行！
    fatal_data = '{"candidate_id": "hacker@test.com", "capability_score": 80, "stability_score": 80, "talent_alpha": "八十", "is_high_risk": false, "risk_tags": []}'
    
    result3 = enforcer.validate_and_repair(fatal_data)
    
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(result3, f, indent=4, ensure_ascii=False)
    print("\n🏆 测试完毕。被重构的兜底数据已安全落锁至 output.json！")

if __name__ == "__main__":
    simulate_battlefield()