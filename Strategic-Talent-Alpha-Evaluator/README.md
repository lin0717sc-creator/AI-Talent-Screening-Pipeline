# 👑 Strategic-Talent-Alpha-Evaluator (V4.0.0)
### 🇸🇬 Industrial-Grade Enterprise AI Talent Screening & Pipeline Engineering System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Data Governance](https://img.shields.io/badge/Compliance-SG%20PDPA-red.svg)]()
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20Pipeline-green.svg)]()

## 📊 1. Commercial Value Proposition (商业价值阐述)
In high-volume recruitment scenarios (e.g., Southeast Asian tech giants receiving over 100K+ resumes per quarter), legacy Applicant Tracking Systems (ATS) suffer from excessive noise, computational redundancy, and fragmented data lineages.

**Strategic-Talent-Alpha-Evaluator (V4.0)** is a high-performance, multi-layered data pipeline designed to ingest highly chaotic applicant datasets, evaluate both **downside risk (Stability)** and **upside potential (Capability & PoW)**, and deploy them into dynamic business profiles.

* **Tri-Pool Asset Routing**: Instead of silent vaporizations, candidates are surgically triaged into three distinct commercial pools: 🟢 Golden Market (Ready-to-Hire), 🟡 Grey-Market Arbitrage (Human Audit), and 🔴 Graveyard (Fatal Denials).
* **Dynamic Talent Alpha**: Instantly shifts screening logic (Weights: Capability/Potential/Stability) based on changing departmental needs (e.g., Pioneer Team vs. Steady Local Ops).
* **Compliance Shield**: Architected strictly above the red line of the **Singapore Personal Data Protection Act (PDPA)**, featuring native sandbox isolation to prevent data leaks.

---

## 🏗️ 2. System Architecture & Directory Topology (项目目录架构图)
The framework adopts the **"1+1+1+1 Modular Stacking" (积木式叠加架构)** principle. It strictly decouples global orchestration, domain configurations, stateless extractors, and risk/capability engines.

```text
Strategic-Talent-Alpha-Evaluator/
├── .env                    # 🔑 Environment Variables & Security Credentials
├── .gitignore              # 🛡️ Data Leakage Firewall (PDPA Red Line Shield)
├── main.py                 # 🚀 Supreme Command Entrypoint (One-Click Ignition)
├── README.md               # 📄 Project Documentation & Blueprint Specifications
├── requirements.txt        # 📦 Environment Dependencies Specifications
├── config/
│   ├── __init__.py
│   └── settings.py         # 🛡️ Central Cabinet: Weights, PoW Patterns, Risk Thresholds & Path Registry
├── data/
│   ├── 01_input_source/    # 📥 Isolated Raw Ingestion Zone (Git-Ignored)
│   ├── 02_raw/             # 📊 Working Raw Data Pool (raw_resumes.csv)
│   └── 03_processed/       # 📤 Output Delivery Zone (Golden Asset & Audit Logs)
│       ├── cleaned_v1_master.csv                 # 🟢 Golden Market
│       ├── cleaned_v1_master_human_audit.csv     # 🟡 Grey-Market Arbitrage Pool
│       └── cleaned_v1_master_rejected_audit.csv  # 🔴 Graveyard Audit Log
├── logs/                   # 🔒 Telemetry Log Vault for Compliance Auditing
└── src/                    # ⚔️ 4-Layer Processing Core Package
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   ├── etl_cleaner.py  # Phase 0: Information Density Deduplication & PoW Extractor
    │   ├── stability.py    # Phase 1: Downside Risk & Stability Deductive Operator
    │   ├── capability.py   # Phase 2&3: Upside Value Matrix & Double-Bottom-Line Kill-Switch
    │   ├── scoring.py      # Core Scoring Calculators & Synergy Weight Engine
    │   └── pipeline.py     # Master CNS Orchestrator & Dynamic Talent-Alpha Engine
    ├── sandbox/
    │   ├── __init__.py
    │   └── test_run.py     # Isolated Pressure-Testing Sandbox Environment
    └── utils/
        ├── __init__.py
        └── helpers.py      # Stateless Pure Functional Regex & Normalization Utilities

---

## 🛠️ 3. Technical Stack (技术栈选型)
- **Runtime**: Python 3.11+
- **Data Governance**: Pandas (ETL Pipeline, Vectorized In-Memory Stream)
- **Intelligent Engine**: Regex Pattern Matching, Deductive Risk Radar & Multi-Factor Matrix
- **Architecture**: Modular Pipeline Design (Decoupled Operator-Controller Pattern)

---

## ⚔️ 4. Core Engineering Breakthroughs (四大硬核工程平移)

### 🛡️ Core 1: Decoupled Compute & Config Architecture (计算与配置彻底解耦)

All strategic parameters (Regex dictionaries, risk thresholds, dynamic weight profiles) are extracted into config/settings.py. The execution engines (src/core/) remain stateless and deterministic, achieving 100% decoupling from dynamic business requirement shifts.

### ⚔️ Core 2: Information-Density Deduplication Algorithm (特征信息密度去重)

Eliminates loss of talent value when applicants submit revised versions (V2/V3). The pipeline computes an Information Density Metric (skill_length), prioritizing richer skill matrices while purging redundant email submissions before regex evaluation.

### 🎯 Core 3: Continuous Deductive Stability Engine & Risk Trigger (稳定性连续扣分与风险熔断)

Rethinks risk assessment by transitioning from arbitrary tagging to a continuous 100-to-0 deduction model.
· Evaluates tenure, gap periods, and macro-layoff/founder keywords.
· Automatically injects is_high_risk: true and logs granular deduction 
· reasons into stability_audit_log.
Executes immediate Red-Line Kill-Switch if the stability score drops below 30.

### 🔒 Core 4: Anti-PPT Double-Bottom-Line Kill-Switch & PoW Premium (双底线熔断与代码主权溢价)

Prevents biased candidate selection via a dual-bottom-line check:
· Zero-Score Hard Kill: Candidates scoring 0 in either Technical Hard Skills OR Project/Business Mindset are instantly classified as 🔴 Red and discarded.
· Proof-of-Work (PoW) Premium: Ingests GitHub/Kaggle/HuggingFace anchors, multiplying the total capability asset by 1.2x for verifiable geek talent.

### 🤖 Core 5: Dynamic Talent-Alpha Transformer Matrix (变形金刚式动态权重矩阵)
Implements calculate_talent_alpha(), supporting instant scene shifting without code modification:
· Pioneer Team Profile: High weight on Capability (50%) and Potential (40%), tolerant of instability.
· Local Steady Profile: Heavy emphasis on Stability (50%) to minimize local training costs in Singapore.
· Balanced Core Profile: Balanced distribution (40% Capability, 30% Potential, 30% Stability).

---

## 🚀 5. Automated Ignition Sequence (系统一键总启航)

```bash
# Step 1: Data Ingestion (原始数据并网入库)
cp your_dirty_resumes.csv data/02_raw/raw_resumes.csv

# Step 2: Supreme Command Launch (中央控制台一键启动)
python main.py

# Step 3: Deliverable Verification (终端三库物理落锁出货)
# 🟢 Golden Market: data/03_processed/cleaned_v1_master.csv
# 🟡 Grey Arbitrage: data/03_processed/cleaned_v1_master_human_audit.csv
# 🔴 Graveyard Log: data/03_processed/cleaned_v1_master_rejected_audit.csv

```

---

## 🏆 6. Production Telemetry Log Exhibit (生产环境雷达日志)

```text
🚀 [SYSTEM CENTRAL] V4.0 智能人才招聘筛选引擎点火启动...

[STAGE 0] 启动 ETL 数据清洗与探针扫描管线...
✅ 数据加载与高密度去重完毕。原始: 100, 有效存活: 82
🔍 探针扫描完毕：共发现 14 名携带数字资产 (GitHub/Kaggle 等) 的极客。
[STAGE 0] 🟢 数据并网与探针提取完毕！数据流移交下一级...

[STAGE 1] 启动 V4.0 稳定性风控大闸 (扣分制红线引擎)...
📊 稳定性风控探针扫描完毕：
  => 🟢 黄金无风险 (80-100分): 48 份
  => 🟡 高危但带病晋级 (30-79分): 22 份
  => 🔴 纯血雇佣兵熔断绞杀 (0-29分): 12 份 (一票否决，不分配后续算力)

[STAGE 2] 启动 V4.0 能力与项目大闸 (加分与双底线熔断引擎)...
📊 核心能力估值扫描完毕：
  => ⚔️ 击杀 PPT 战神 (技术底线熔断): 4 份
  => ⚔️ 击杀 呆板码农 (商业底线熔断): 3 份
  => 🏆 成功穿越双底线幸存者: 63 份 (已赋予身价总分，准备进行业务权重变形)

[STAGE 3] 启动 V4.0 动态业务场景变形引擎...
🎯 注入业务指令: BALANCED_CORE (中坚骨干团队大厂标准配置)
⚖️ 资源倾斜配比 -> 能力:0.4 | 潜力:0.3 | 稳定性:0.3

[STAGE 4] 终端商业三库分发完毕！
  => 🟢 黄金无暇资产: 45 人 (已按 BALANCED_CORE 业务排序)
  => 🟡 高性价比捡漏: 18 人 (已排序，自带 is_high_risk 爆红预警)
  => 🔴 阵亡封存资产: 19 人 (估值归零，死因已入库)

[STAGE 5] --- 后端物理落锁 ---
✅ 黄金大盘已落锁: Strategic-Talent-Alpha-Evaluator/data/03_processed/cleaned_v1_master.csv
⚠️ 捡漏审计池已落锁: Strategic-Talent-Alpha-Evaluator/data/03_processed/cleaned_v1_master_human_audit.csv
☠️ 阵亡名册及死因已封存: Strategic-Talent-Alpha-Evaluator/data/03_processed/cleaned_v1_master_rejected_audit.csv

🎉 报告指挥官，V4.0 引擎运行成功！黄金大盘、灰度捡漏池与阵亡名册已全部落锁！

---

### 💡 补全说明
1. **完整对应你本地电脑的 VS Code 结构**：把 `.env`、`requirements.txt`、`scoring.py`、`test_run.py` 全部包含在内。
2. **完整呈现 `data/` 三库落盘路径**：清晰标记出了 `01_input_source`、`02_raw`、`03_processed` 及其输出的 3 个 CSV 文件。
3. **闭环了战役目标**：在 Section 4 里精准阐述了第 20 天你拍板的 `is_high_risk: true` 熔断、PoW 1.2倍溢价加成与动态变形金刚矩阵。