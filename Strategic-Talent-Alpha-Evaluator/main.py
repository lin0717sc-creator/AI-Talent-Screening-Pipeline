# ==========================================
# 文件路径: main.py
# 👑 V5.0 Strategic-Talent-Alpha-Evaluator (总控台)
# ==========================================
import os
import sys
import pandas as pd
from tqdm import tqdm

# 🚀 拉齐交通网络
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from config.settings import ACTIVE_PROFILE, SAFE_SETTINGS
from src.utils.logger import SYSTEM_LOGGER  # 🚀 V5.0 引入全局工业雷达

def ensure_directories():
    """确保三库文件结构存在"""
    os.makedirs("data/02_raw", exist_ok=True)
    os.makedirs("data/03_processed", exist_ok=True)

def generate_mock_data():
    """如果没有真实数据，生成模拟数据用于压测体验"""
    raw_path = "data/02_raw/raw_resumes.csv"
    if not os.path.exists(raw_path):
        SYSTEM_LOGGER.warning("未检测到原始数据，系统正在自动生成压测模拟数据...")
        import random
        emails = [f"user_{i}@test.com" for i in range(100)]
        skills = [random.choice(["Python, SQL", "Excel, PPT", "Java, Docker, Kubernetes"]) for _ in range(100)]
        pow_links = [random.choice(["github.com/hacker", "", "kaggle.com/data_god"]) for _ in range(100)]
        
        df = pd.DataFrame({"email": emails, "skills": skills, "portfolio": pow_links})
        df.to_csv(raw_path, index=False)

def engine_ignition():
    SYSTEM_LOGGER.info("="*50)
    SYSTEM_LOGGER.info("👑 [SYSTEM CENTRAL] V5.0 动态人才评估流水线总引擎启动")
    SYSTEM_LOGGER.info(f"🎯 当前注入业务指令: {ACTIVE_PROFILE}")
    SYSTEM_LOGGER.info("="*50)

    ensure_directories()
    generate_mock_data()

    # --- [前端并网风控] ---
    SYSTEM_LOGGER.info("[STAGE 1] 🛡️ 启动前端并网风控与序列重置...")
    raw_df = pd.read_csv("data/02_raw/raw_resumes.csv")
    
    initial_len = len(raw_df)
    raw_df = raw_df.drop_duplicates(subset=['email']).reset_index(drop=True)
    SYSTEM_LOGGER.info(f"✅ 并网成功！原始并发: {initial_len} 行，有效独立资产: {len(raw_df)} 行")

    # --- [核心技术绞杀] ---
    SYSTEM_LOGGER.info("[STAGE 2] ⚔️ 启动 Pandas 并发绞杀引擎 (挂载容错装甲)...")
    tqdm.pandas(desc="⚙️ 引擎吞吐进度")

    def core_evaluation_logic(row):
        """核心评估引擎 (已挂载防崩溃看门狗)"""
        try:
            skills = str(row.get('skills', ''))
            portfolio = str(row.get('portfolio', ''))
            
            # 使用经过 Pydantic V2 校验的配置
            cap_weight = SAFE_SETTINGS.capability
            
            base_score = 50
            if 'Python' in skills or 'Java' in skills:
                base_score += 30 * cap_weight
                
            is_risk = base_score < 40
            
            if 'github.com' in portfolio or 'kaggle.com' in portfolio:
                base_score *= 1.2
                
            return pd.Series([round(base_score, 2), is_risk, "核心战神，立刻安排面试！" if base_score > 55 else "常规储备池"])
            
        except Exception as e:
            # 记录详细的行级异常审计日志，而不是直接抛出崩溃
            SYSTEM_LOGGER.error(f"❌ 资产解析异常 | 邮箱: {row.get('email', 'UNKNOWN')} | 报错: {str(e)}")
            return pd.Series([0.0, True, f"SYSTEM_ERROR: {str(e)}"])

    # 并发吞吐
    raw_df[['Talent_Alpha', 'is_high_risk', 'strategic_advice']] = raw_df.progress_apply(core_evaluation_logic, axis=1)

    # --- [后端落锁维护] ---
    SYSTEM_LOGGER.info("[STAGE 3] 🔒 启动商业降维排序与后端落锁机制...")
    
    golden_pool = raw_df[raw_df['is_high_risk'] == False].copy()
    top_50_gods = golden_pool.sort_values(by='Talent_Alpha', ascending=False).head(50)
    
    output_path = "data/03_processed/cleaned_v1_master.csv"
    top_50_gods.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    SYSTEM_LOGGER.info(f"🏆 [战役告捷] 大盘清洗完毕！黄金池剩余: {len(golden_pool)} 人。")
    SYSTEM_LOGGER.info(f"👉 顶尖 50 名超级战神资产已物理落锁至: {output_path}")

if __name__ == "__main__":
    engine_ignition()