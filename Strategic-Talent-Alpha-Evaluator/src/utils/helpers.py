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
    