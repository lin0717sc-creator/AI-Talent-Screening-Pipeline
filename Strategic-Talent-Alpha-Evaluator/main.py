# ==========================================
# 文件路径: main.py
# 👑 V5.0 Strategic-Talent-Alpha-Evaluator (至高点火引信)
# ==========================================
import os
import sys

# 🚀 强行拉齐交通网络，解决全局模块导入路径报错
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from config.settings import ACTIVE_PROFILE
from src.core.pipeline import MasterDataPipeline
from src.utils.logger import SYSTEM_LOGGER  # 🚀 V5.0 引入全局工业雷达

def pre_flight_check():
    """起飞前自检：确保物理目录防线存在，并填装备用弹药"""
    os.makedirs("data/02_raw", exist_ok=True)
    os.makedirs("data/03_processed", exist_ok=True)
    
    raw_path = "data/02_raw/raw_resumes.csv"
    if not os.path.exists(raw_path):
        SYSTEM_LOGGER.warning("未检测到真实源数据，系统启动备用预案：生成压测模拟弹药...")
        import pandas as pd
        import random
        emails = [f"user_{i}@test.com" for i in range(100)]
        skills = [random.choice(["Python, SQL", "Excel, PPT", "Java, Docker, Kubernetes"]) for _ in range(100)]
        pow_links = [random.choice(["github.com/hacker", "", "kaggle.com/data_god"]) for _ in range(100)]
        
        df = pd.DataFrame({"email": emails, "skills": skills, "portfolio": pow_links})
        df.to_csv(raw_path, index=False)
        SYSTEM_LOGGER.info("备用弹药已物理落盘至 data/02_raw/raw_resumes.csv")

def ignition():
    SYSTEM_LOGGER.info("="*50)
    SYSTEM_LOGGER.info("🚀 [SYSTEM CENTRAL] V5.0 智能人才招聘筛选引擎点火启动...")
    SYSTEM_LOGGER.info(f"🎯 当前注入战略指令: {ACTIVE_PROFILE}")
    SYSTEM_LOGGER.info("="*50)
    
    # 第一步：物理环境查验
    pre_flight_check()

    try:
        # 第二步：唤醒大厂级面向对象总控管线
        pipeline = MasterDataPipeline()
        
        # 第三步：V5.0 全流程一键贯穿
        # Phase 0 (ETL/PoW) -> Phase 1 (稳定性) -> Phase 2&3 (能力双底线) -> Phase 3.5 (JSON大闸) -> Phase 4&5 (落盘)
        pipeline.execute_pipeline()
        
        SYSTEM_LOGGER.info("\n🎉 报告指挥官，V5.0 引擎运行成功！黄金大盘、灰度捡漏池与阵亡名册已全部完成云端落锁！")
    except Exception as e:
        SYSTEM_LOGGER.error(f"\n🚨 [FATAL ERROR] 引擎主轴遭遇致命异常，系统已触发物理熔断！报错日志: {e}")

if __name__ == "__main__":
    ignition()