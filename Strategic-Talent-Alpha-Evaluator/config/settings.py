import os
import re

# 绝对路径
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CONFIG_DIR)

INPUT_PATH = os.path.join(BASE_DIR, "data", "raw", "raw_resumes.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_v1_master.csv")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# 🛡️ 修复契约：将提取源从硬编码的 'resume_text' 改为配置文件
# 你目前的 CSV 包含: name, email, phone, skills, ...
RESUME_COLUMN = "skills" 

# 战略宪法：正则引擎
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
SKILL_PATTERN = re.compile(r'\b(Python|SQL|Tableau|Machine Learning|Cloud Computing)\b', re.IGNORECASE)

FILL_RULES = {
    'phone': 'UNKNOWN_PHONE',
    'standard_skills': 'NO_SKILLS_TAG'
}

# 🛡️ 语义映射宪法：将多种变体归一化为标准标签
SKILL_MAPPING = {
    'python': 'Python',
    'py': 'Python',
    'sql': 'SQL',
    'tableau': 'Tableau',
    'machine learning': 'ML',
    'ml': 'ML'
}
# 提取技能的正则需保持，但结果要进入归一化流水线

# 商业加权矩阵
SKILL_WEIGHTS = {
    'Python': 0.4,
    'SQL': 0.3,
    'Tableau': 0.1,
    'ML': 0.2
}

# 必须具备的技能（一票否决权）
MUST_HAVE_SKILLS = ['Python']

# 增补：组合加成权重 (如果同时具备 Python 和 ML，触发 synergy_bonus)
SYNERGY_BONUS = {
    'Python_ML': 0.20,  # 额外奖励 20%
}