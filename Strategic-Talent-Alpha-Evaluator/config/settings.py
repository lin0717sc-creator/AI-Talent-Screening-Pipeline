import os
import re

# ==============================================================================
# 📂 1. 📂 物理目录与资产寻址注册表（绝对路径硬锁死，绝杀 FileNotFoundError）
# ==============================================================================
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CONFIG_DIR)

STORAGE_REGISTRY = {
    'input_source': os.path.join(BASE_DIR, "data", "01_input_source"),
    'raw_pool': os.path.join(BASE_DIR, "data", "02_raw"),
    'processed_pool': os.path.join(BASE_DIR, "data", "03_processed"),
    'input_csv': os.path.join(BASE_DIR, "data", "02_raw", "raw_resumes.csv"),
    'master_output_csv': os.path.join(BASE_DIR, "data", "03_processed", "cleaned_v1_master.csv"),
    'log_dir': os.path.join(BASE_DIR, "logs")
}
RESUME_COLUMN = "skills" 

# ==============================================================================
# 🛡️ 2. 传统Regex清洗引擎与历史数据字典 (特征探针全面扩容)
# ==============================================================================
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

# 🚀 扩容探针：不仅抓技术底座，还必须抓取合规词汇和红利词汇（如 Github, Vectorization, LLM）
SKILL_PATTERN = re.compile(
    r'\b(Python|SQL|Tableau|Machine Learning|Cloud Computing|PDPA|MOM|Compliance|Privacy|Security|Audit|'
    r'GitHub|Vectorization|Chunking|Parquet|AWS|GCP|Docker|LLM|Prompt Engineering|Agentic Workflow)\b', 
    re.IGNORECASE
)

FILL_RULES = {
    'phone': 'UNKNOWN_PHONE',
    'standard_skills': 'NO_SKILLS_TAG'
}

# 🚀 扩容映射：确保新抓上来的词能被精准小写归一化，喂给打分引擎
SKILL_MAPPING = {
    'python': 'python',
    'py': 'python',
    'sql': 'sql',
    'tableau': 'tableau',
    'machine learning': 'machine_learning',
    'ml': 'machine_learning',
    'cloud computing': 'cloud',
    # 合规心智映射
    'pdpa': 'pdpa',
    'mom': 'mom',
    'compliance': 'compliance',
    'privacy': 'privacy',
    'security': 'security',
    'audit': 'audit',
    # 红利特征映射
    'github': 'github_portfolio',
    'vectorization': 'vectorization',
    'chunking': 'chunking',
    'parquet': 'parquet',
    'aws': 'aws',
    'gcp': 'gcp',
    'docker': 'docker',
    'llm': 'llm',
    'prompt engineering': 'prompt_engineering',
    'agentic workflow': 'agentic_workflow'
}

# ==============================================================================
# 🧱 3. 🧱 维度一：技术能力打分矩阵配置（高召回语义池驱动）
# ==============================================================================
# 技术弹性准入网
TECH_FOUNDATION_POOL = {'python', 'sql', 'pandas', 'cloud', 'github', 'github_portfolio'}
COMPLIANCE_CONCEPT_POOL = {'pdpa', 'mom', 'compliance', 'privacy', 'governance', 'regulation', 'security', 'audit'}

# 技术特征身价计分板
TECH_SKILL_WEIGHTS = {
    'python': 10,
    'sql': 10,
    'machine_learning': 20,       # 刚性主管红线（Python基础之 2 倍）
    'llm': 15,                     # 时代大模型生产力
    'prompt_engineering': 15,
    'agentic_workflow': 15,
    'vectorization': 15,           # 算力压榨
    'chunking': 15,
    'parquet': 15,
    'aws': 10,                     # 云端交付
    'gcp': 10,
    'docker': 10,
    'api_integration': 10,
    'github_portfolio': 20,        # 开源主权铁证
    'tableau': 10,                 # 商业智能可视化
    'powerbi': 10
}

# ==============================================================================
# 🏁 4. 🧭 维度二：项目产出打分矩阵配置（应届生自愈双轨路由）
# ==============================================================================
# 项目弹性准入网（效益池与交付池）
PROJECT_BENEFIT_POOL = {
    'roi', 'cost_savings', 'revenue_per_employee', 'l_dec', '人效', '成本压缩',  # 工业轨
    'simulation_metrics', 'accuracy_delta', 'performance_delta', 'benchmark_optimization' # 自研/学术轨
}
PROJECT_DELIVERY_POOL = {
    'production_launch', 'cloud_deployment', 'saas_commercialization',  # 工业轨
    'local_end_to_end_integration', 'github_open_source_release', 'thesis_prototype_verification' # 自研/学术轨
}
# 项目特征身价计分板
PROJECT_OUTPUT_WEIGHTS = {
    'million_row': 20,
    'high_throughput': 20,
    'roi_optimization': 20,
    'cost_savings_tag': 20,
    'revenue_per_employee_tag': 20,
    'end_to_end_pipeline': 15,
    'automated_workflow': 15,
    'agentic_workflow': 15,
    'predictive_modeling': 15,
    'regional_hq_alignment': 10,
    'global_synergy': 10,
    'saas_interface': 10
}
# ==============================================================================
# ⚔️ 5. 🔥 🔥 核心核心：补齐“跨界硬能力混合红利”配置矩阵 🔥 🔥
# ==============================================================================
# 组合拳A：工业级全栈交付红利配置
BONUS_TECH_DELIVERY = {
    'trigger_skill': 'github_portfolio',
    'performance_tags': {'vectorization', 'chunking', 'parquet'},
    'points': 10.0
}
# 组合拳B：AI新基建生产力红利配置
BONUS_AI_INFRA = {
    'ai_skills': {'llm', 'prompt_engineering', 'agentic_workflow'},
    'cloud_tags': {'aws', 'gcp', 'docker'},
    'points': 15.0
}

# 组合拳C：FinOps算力财务重构红利配置
BONUS_FINOPS = {
    'scale_tags': {'million_row', 'high_throughput'},
    'finance_tags': {'cost_savings_tag', 'roi_optimization'},
    'points': 15.0
}

# 组合拳D：MGT567亚太战略交付红利配置 (1+1>2 终极破格分)
BONUS_APAC_STRATEGY = {
    'pipeline_tags': {'end_to_end_pipeline', 'agentic_workflow'},
    'strategy_tags': {'regional_hq_alignment', 'global_synergy'},
    'points': 15.0
}

# ==============================================================================
# 🎯 6. 顶层宏观配比系数与大盘截断上限（4:6 黄金比例契约）
# ==============================================================================
GLOBAL_WEIGHT_TECH = 0.4
GLOBAL_WEIGHT_PROJECT = 0.6

TECH_SCORE_CAP = 100
PROJECT_SCORE_CAP = 100