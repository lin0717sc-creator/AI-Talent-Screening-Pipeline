import os
import re

# 👑 绝对根路径动态锚定：向上两级，精准锁定整个项目的中央大盘坐标
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CONFIG_DIR)

# 📊 物理资产绝对流动通道
INPUT_PATH = os.path.join(BASE_DIR, "data", "raw", "raw_resumes.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_v1_master.csv")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# ⚔️ 战略业务规则：核心正则引信（后续可无限扩充加权词典）
TECH_PATTERN = re.compile(r'python|tableau|data analytics|sql|machine learning|excel', re.IGNORECASE)

# 🩹 静态补丁抢救规则矩阵
FILL_RULES = {
    'phone': 'UNKNOWN_PHONE',
    'standard_skills': 'NO_SKILLS_TAG'
}
