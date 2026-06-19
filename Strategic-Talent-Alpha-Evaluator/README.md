# 👑 Strategic-Talent-Alpha-Evaluator (V1.0)
### 🇸🇬 Industrial-Grade Enterprise AI Talent Screening & Pipeline Engineering System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Data Governance](https://img.shields.io/badge/Compliance-SG%20PDPA-red.svg)]()
[![Architecture](https://img.shields.io/badge/Architecture-OOP%20%2F%20Decoupled-green.svg)]()

## 📊 1. Commercial Value Proposition (商业价值阐述)
In high-volume recruitment scenarios (e.g., Southeast Asian tech giants receiving over 100K+ resumes per quarter), legacy Applicant Tracking Systems (ATS) suffer from excessive noise, computational redundancy, and fragmented data lineages.

**Strategic-Talent-Alpha-Evaluator** is a high-performance, object-oriented data pipeline designed to ingest highly chaotic applicant datasets and compress them into standardized, high-density professional capital. 

* **Asset Preservation Rate**: Reclaims high-potential "outlier candidates" via programmatic patching rather than silent error vaporization.
* **Compliance Shield**: Architected strictly above the red line of the **Singapore Personal Data Protection Act (PDPA)**, featuring native sandbox isolation to prevent data leaks.

---

## 🏗️ 2. System Architecture & Directory Topology (项目目录架构图)
The framework adopts the **"High Cohesion, Low Coupling" (高内聚，低耦合)** principle, enforcing a strict division between global orchestration, domain configuration, stateless operators, and isolated compute sandboxes.

```text
Strategic-Talent-Alpha-Evaluator/
├── config/
│   ├── __init__.py
│   └── settings.py         # 🛡️ STAGE 1: Central Configuration Cabinet (Policy Rules)
├── data/
│   ├── raw/                # 📥 Isolated Ingestion Zone (Strictly Git-Ignored for PDPA)
│   └── processed/          # 📤 Locked Output Zone (Golden Delivery Assets)
├── logs/                   # 🔒 STAGE 3: Telemetry Log Vault for Compliance Auditing
├── src/                    # ⚔️ STAGE 2: Regular Army Processing Core Package
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── pipeline.py     # OOP Processing Engine (Zero Hardcoding)
│   ├── sandbox/
│   │   ├── __init__.py
│   │   └── test_run.py     # Pressure Testing Sandbox Environment
│   └── utils/
│       ├── __init__.py
│       └── helpers.py      # Stateless Pure Functional Operators
├── .gitignore              # Data Leakage Firewall
└── main.py                 # 🚀 Supreme Command Entrypoint (Ignition 引信)

```

---

## 🛠️ 3. Technical Stack (技术栈选型)
- **Runtime**: Python 3.11+
- **Data Governance**: Pandas (ETL Pipeline)
- **Intelligent Engine**: Regex-based Pattern Matching & Custom Scoring Logic
- **Architecture**: Object-Oriented Design (Decoupled Operator-Controller Pattern)

---

## ⚔️ 4. Core Engineering Breakthroughs (四大硬核工程平移)

### 🛡️ Core 1: Decoupled Compute & Storage Architecture (计算与配置彻底分离)

To prevent legacy "Hardcoding" brittleness, all strategic business metrics (Regular Expression dictionaries, fill rules, skill lists) have been upwardly extracted into `config/settings.py`. The underlying execution engine (`src/core/pipeline.py`) acts as a cold, deterministic machine, achieving **100% decoupling from dynamic business requirement shifting**.

### ⚔️ Core 2: In-Memory Pipeline Processing (内存全量流转，拒绝磁盘污染)

Unlike novice workflows that dump intermediate `.csv` chunks after every operation—causing severe I/O bottlenecks and expanding the system's attack surface under SG PDPA auditing—this system operates **fully in-memory**. Data streams are ingested, vectorized, filtered, and standardized in RAM, hitting the physical disk only at the terminal output anchor.

### 🎯 Core 3: Information-Density Deduplication Algorithm (特征信息密度去重)

Traditional deduplication filters via simple `keep='first'` scripts, leading to massive losses of talent value when applicants submit revised versions (V2/V3) with richer skill matrices. This pipeline introduces an **Information Density Metric**, scoring rows by missing-value inversion, sorting by density hierarchy, and isolating the absolute optimum candidate profile.

### 🔒 Core 4: Absolute Baseline Path Anchoring & Path Drift Defense (中央绝对路径锚定)

Enforces a dynamic double-upward anchor (`BASE_DIR`) in the configuration module. This system-level defense ensures that no matter where the code is executed (local terminal, distributed remote server, or cron-job orchestration), the workspace alignment coordinates remain invariant, completely eliminating `FileNotFoundError` caused by relative directory shifting.

### 🤖 Core 5: Intelligent Feature Extraction Engine (V1.0 Update)
Integrated a decoupled **Regex-based automated feature extraction engine** into the pipeline. 
- **Dynamic Feature Stripping**: Automatically parses unstructured resume data into structured fields (e.g., Email, Standardized Skills Tags).
- **Non-Greedy Extraction**: Employs non-greedy regex logic (`.*?`) to prevent data noise contamination, ensuring high-fidelity output.
- **Config-Driven**: Extraction patterns are fully managed in `config/settings.py`, allowing HR teams to pivot screening criteria instantly without triggering a production downtime.

### 🤖 Core 6: Engineering Breakthroughs
1. **Intelligent Feature Extraction**: Decoupled Regex engine for automated parsing of unstructured resume data.
2. **Data Normalization Engine**: Built-in semantic mapping dictionary to standardize fragmented skill tags (e.g., "py" -> "Python").
3. **Robust Circuit Breaker (熔断机制)**: Implemented decorator-based validation to intercept malformed data at the pipeline entrance.
4. **Weighted Scoring Engine (V1.0 Update)**: 
   - **Capability Scoring**: Multi-dimensional weighted analysis engine (Python: 0.4, SQL: 0.3, etc.).
   - **Hard-Constraint Enforcement**: Strictly enforces "Must-Have" skill prerequisites; non-compliant candidates are automatically filtered.
   - **Synergy Bonus (协同加成)**: Non-linear scoring logic that rewards high-value skill clusters (e.g., Python + ML Bonus).
   - **Business Protection (异常处理)**: Implemented 30-point baseline protection for zero-skill entries, ensuring production stability.

---

## 🚀 5. Automated Ignition Sequence (系统一键总启航)

```bash
# Step 1: Ingestion Zone Placement (原始脏数据物理并网入库)
cp your_dirty_data.csv data/raw/raw_resumes.csv

# Step 2: Unified Execution Launch (中央总控制台一键点火引信启动)
python main.py

# Step 3: Output Deliverable Review (黄金资产全自动物理落锁出货)
# Target Deliverable Secured at: data/processed/cleaned_v1_master.csv

```

---

## 🏆 6. Production Telemetry Log Exhibit (生产环境雷达盘面实录)

```text
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
👑 [SYSTEM CENTRAL] V1.0 Modular Pipeline Firing Up...
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥

--- 🛡️ [STAGE 1] 前端并网风控检查 ---
[TELEMETRY] 资产并网安全。初始 Raw 数据: 36 行.

--- ⚔️ [STAGE 2] 核心技术模块化绞杀 ---
[TELEMETRY] 1. 僵尸熔断完毕. 剩余高价值资产: 33 行.
[TELEMETRY] 2. 信息密度排序去重完毕. 独一主权资产: 31 行.
[TELEMETRY] 3. 跨舱并网成功。标准技能标签提取已合拢.
[TELEMETRY] 4. 静态补丁依据中央宪法填充完毕.

--- 🔒 [STAGE 3] 后端落锁维护出货 ---
[TELEMETRY] 物理落锁成功！生成纯净化黄金数据: 30 行.
➡️ 终极交付地址: Strategic-Talent-Alpha-Evaluator/data/processed/cleaned_v1_master.csv

🏆 [SUCCESS] Execution complete. Deliverable secured into golden zone.
==================================================
