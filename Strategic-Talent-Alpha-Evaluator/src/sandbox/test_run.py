import sys
import os
# 往上跳两级，精准锚定项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)

import json

# 🚀 强行拉齐交通网络，保证能找到 config 和 src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from src.core.json_validator import JSONEnforcer

def simulate_battlefield():
    enforcer = JSONEnforcer()

    print("\n--- 🟢 测试 1：纯净的黄金数据 ---")
    good_data = '{"candidate_id": "lin@test.com", "capability_score": 85, "stability_score": 90, "talent_alpha": 87.5, "is_high_risk": false, "risk_tags": [], "strategic_advice": "强烈建议录用"}'
    result1 = enforcer.validate_and_repair(good_data)
    print("✅ 成功解析:", result1['candidate_id'])

    print("\n--- 🟡 测试 2：带有 Markdown 和废话的脏数据 ---")
    dirty_data = '''好的指挥官，这是你要的JSON：
    ```json
    {
        "candidate_id": "dirty@test.com", 
        "capability_score": 60, 
        "stability_score": 40, 
        "talent_alpha": 50, 
        "is_high_risk": true, 
        "risk_tags": ["FREQUENT_JUMPER"], 
        "strategic_advice": "外包可接，全职慎用"
    }
    ```
    希望对您有帮助！'''
    result2 = enforcer.validate_and_repair(dirty_data)
    print("✅ 成功剥离废话并解析:", result2['candidate_id'])

    print("\n--- 🔴 测试 3：恶意篡改类型与少字段（暴力熔断测试） ---")
    fatal_data = '{"candidate_id": "hacker@test.com", "capability_score": 80, "stability_score": 80, "talent_alpha": "八十", "is_high_risk": false, "risk_tags": []}'
    
    result3 = enforcer.validate_and_repair(fatal_data)
    
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(result3, f, indent=4, ensure_ascii=False)
    print("\n🏆 测试完毕。被重构的兜底数据已安全落锁至 output.json！")

if __name__ == "__main__":
    simulate_battlefield()