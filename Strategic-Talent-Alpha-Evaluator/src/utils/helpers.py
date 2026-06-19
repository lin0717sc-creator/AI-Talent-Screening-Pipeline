import pandas as pd

def extract_regex_feature(text, pattern, default="N/A"):
    """使用正则从字符串提取单项特征"""
    if not isinstance(text, str):
        return default
    match = pattern.search(text)
    return match.group(0) if match else default

def extract_all_skills(text, pattern):
    """提取所有匹配到的技能点并返回列表"""
    if not isinstance(text, str):
        return []
    # 使用 set 去重，并转为排序列表
    return sorted(list(set(pattern.findall(text))))

def normalize_skills(skill_list, mapping):
    """
    ⚔️ 核心技术绞杀：将抓取到的技能标签降维并映射到标准标签
    """
    normalized = set()
    for skill in skill_list:
        clean_skill = str(skill).lower().strip()
        # 如果在映射表中，则归一化；否则保留原值（或者你可以选择丢弃未识别标签）
        standard_label = mapping.get(clean_skill, clean_skill)
        normalized.add(standard_label)
    return list(normalized)

def calculate_advanced_score(skills, weights, must_haves, synergy):
    """
    ⚔️ 工业级打分算子：支持硬性指标过滤 + 组合加成计算
    """
    # 1. 一票否决
    if not all(skill in skills for skill in must_haves):
        return 0.0
    
    # 2. 基础加权求和
    base_score = sum(weights.get(s, 0) * 100 for s in skills)
    
    # 3. 组合加成 (Synergy Bonus)
    if 'Python' in skills and 'ML' in skills:
        base_score *= (1 + synergy.get('Python_ML', 0))
        
    return round(base_score, 2)