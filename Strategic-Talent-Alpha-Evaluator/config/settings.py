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
# 🛡️ 2.1 传统Regex清洗引擎与历史数据字典 (特征探针全面扩容)
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
# 🛡️ 2.2 高潜特征与商业落地探针 (Potential & Project Matrix) - 第19天新增
# ==============================================================================
# 锁定高信息密度的重构词与商业决策词，拒绝形容词
PROJECT_PATTERN = re.compile(
    r'\b(A/B Testing|Optimization|Framework Rebuild|Zero-to-One|Cost Reduction|ROI|'
    r'FinOps|End-to-End|Cross-functional|Automation|Scalability|Throughput)\b', 
    re.IGNORECASE
)

# 降维收敛：将五花八门的业务黑话，强制归一化为咱们打分引擎里需要的标准词
PROJECT_MAPPING = {
    'a/b testing': 'ab_testing',
    'optimization': 'optimization',
    'framework rebuild': 'rebuild',
    'zero-to-one': '0_to_1',
    'cost reduction': 'cost_reduction',
    'roi': 'roi',
    'finops': 'finops',
    'end-to-end': 'end_to_end',
    'cross-functional': 'cross_functional',
    'automation': 'automation',
    'scalability': 'scalability',
    'throughput': 'throughput'
}

# ==============================================================================
# 🧱 3. 🧱 维度一：技术能力打分矩阵配置（高召回语义池驱动）
# ==============================================================================
# 技术弹性准入网 (融合了最新的精英技术要求)
TECH_FOUNDATION_POOL = {'python', 'sql', 'pandas', 'cloud', 'github', 'github_portfolio', 'tableau', 'machine_learning', 'cloud_computing', 'docker', 'llm', 'aws'}
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
    'powerbi': 10,
    'cloud_computing': 10          # 补充精英资产用词
}

# ==============================================================================
# 🏁 4. 🧭 维度二：项目产出打分矩阵配置（应届生自愈双轨路由）
# ==============================================================================
# 项目弹性准入网（完美保留你的工业轨与自研轨，并注入高潜极客词汇）
PROJECT_BENEFIT_POOL = {
    'roi', 'cost_savings', 'revenue_per_employee', 'l_dec', '人效', '成本压缩',  # 你的原版硬核词
    'simulation_metrics', 'accuracy_delta', 'performance_delta', 'benchmark_optimization',
    'finops', 'cost_reduction', 'optimization', 'scalability', 'throughput'       # 第19天新增高潜词
}

PROJECT_DELIVERY_POOL = {
    'production_launch', 'cloud_deployment', 'saas_commercialization',  
    'local_end_to_end_integration', 'github_open_source_release', 'thesis_prototype_verification',
    'end_to_end', 'ab_testing', 'cross_functional', 'automation', 'framework_rebuild' # 第19天新增高潜词
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
    'saas_interface': 10,
    # 下方为新增高潜词记分
    'finops': 20,
    'ab_testing': 15,
    'framework_rebuild': 20,
    'end_to_end': 15
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

# ==============================================================================
# ⚠️ 7. 维度三：V3.0 稳定性与离职风险特征雷达（Stability Radar）
# ==============================================================================

# 1. 内部调动与集团并购特征（用于 Phase 0 并网防御）
MERGE_WORDS = r'(?i)\b(acquired|merged|internal transfer|promoted|内部调动|晋升|收购|合并)\b'

# 2. 特殊用工性质特征（用于 Phase 2 黄牌截留）
GIG_WORDS = r'(?i)\b(contract|freelance|consultant|vendor|outsourcing|外包|顾问|独立开发者)\b'
FOUNDER_WORDS = r'(?i)\b(founder|co-founder|entrepreneur|ceo|创始人|联合创始人)\b'

# 3. 宏观经济/裁员受害者特征（用于 Phase 3-A 捡漏池截留）
LAYOFF_WORDS = r'(?i)\b(layoff|retrenchment|redundancy|restructure|company closed|downsizing|裁员|业务裁撤|公司倒闭)\b'

# 稳定性阈值定义 (Hyperparameters)
STABILITY_THRESHOLDS = {
    'fresh_grad_max_exp': 2.0,      # 应届生绝对豁免线 (年)
    'mercenary_max_tenure': 12,     # 纯血雇佣兵绞杀线 (个月)
    'anchor_tenure': 60,            # 定海神针安全线 (个月)
    'dangerous_gap': 6              # 危险断层线 (个月)
}

# ==============================================================================
# 🕵️ 8. 维度四：代码主权锚点探针 (Proof of Work) - V4新增防忽悠大闸
# ==============================================================================
POW_PATTERNS = [
    r'(?i)github\.com/[a-zA-Z0-9_-]+',
    r'(?i)gitee\.com/[a-zA-Z0-9_-]+',
    r'(?i)kaggle\.com/[a-zA-Z0-9_-]+',
    r'(?i)huggingface\.co/[a-zA-Z0-9_-]+',
    r'(?i)[a-zA-Z0-9_-]+\.(dev|io)' # 个人极客博客
]

# ==============================================================================
# ⚙️ 9. 业务场景动态权重矩阵 (Talent Alpha) - V4变形金刚引擎
# ==============================================================================
TALENT_WEIGHT_PROFILES = {
    "PIONEER_TEAM": {
        "desc": "急缺技术突破的先遣团队 (看重能力与潜力，极度包容跳槽)",
        "weights": {"capability": 0.50, "potential": 0.40, "stability": 0.10}
    },
    "LOCAL_STEADY": {
        "desc": "新加坡本地高度重视培训成本的运维团队 (极度看重稳定性)",
        "weights": {"capability": 0.30, "potential": 0.20, "stability": 0.50}
    },
    "BALANCED_CORE": {
        "desc": "中坚骨干团队 (大厂标准配置)",
        "weights": {"capability": 0.40, "potential": 0.30, "stability": 0.30}
    }
}

# 当前激活的业务线配置（HR/指挥官 可随时在这里切换场景）
ACTIVE_PROFILE = "BALANCED_CORE"