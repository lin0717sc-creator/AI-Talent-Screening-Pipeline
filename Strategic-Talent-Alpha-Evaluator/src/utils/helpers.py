import pandas as pd

def extract_skills_tags(text_cell, pattern):
    """
    👑 纯净化算子：正则标签标准提白
    输入一行脏文本，吐出干净的标签，绝对不带有任何副作用。
    """
    if pd.isna(text_cell) or not isinstance(text_cell, str):
        return 'NO_SKILLS_TAG'
    
    matches = pattern.findall(text_cell)
    if matches:
        # 去重、修剪空格、首字母大写、重新排序，呈现大厂绝对正规的清洗美感
        tags = set([m.strip().title() for m in matches])
        return ", ".join(sorted(list(tags)))
    
    return 'NON_STANDARD_SKILLS'
