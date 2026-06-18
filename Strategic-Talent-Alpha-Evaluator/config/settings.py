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
