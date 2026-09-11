# ==========================================
# 👑 V6.0 Strategic-Talent-Alpha-Evaluator (总控点火引信)
# ==========================================
import os
import sys

# 🚀 强行拉齐交通网络，解决全局模块导入路径报错
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from config.settings import ACTIVE_PROFILE
from src.core.pipeline import MasterDataPipeline
from src.utils.logger import SYSTEM_LOGGER

def pre_flight_check():
    """起飞前自检：确保物理目录防线存在，并检查弹药库状态"""
    os.makedirs("data/02_raw", exist_ok=True)
    os.makedirs("data/03_processed", exist_ok=True)
    
    raw_path = "data/02_raw/raw_resumes.csv"
    if not os.path.exists(raw_path):
        # 🚨 拔除所有假数据硬编码，恢复大厂真实逻辑：没有数据就报错拦截！
        SYSTEM_LOGGER.error(f"🚨 [致命错误] 未在 {raw_path} 检测到输入数据！")
        SYSTEM_LOGGER.warning("💡 请先将真实的候选人数据 (或测试用例) 放入该目录后再启动引擎。")
        sys.exit(1) # 直接物理熔断，停止运行

def ignition():
    SYSTEM_LOGGER.info("="*50)
    SYSTEM_LOGGER.info("🚀 [SYSTEM CENTRAL] V6.0 智能人才招聘筛选引擎点火启动...")
    SYSTEM_LOGGER.info(f"🎯 当前注入战略指令: {ACTIVE_PROFILE}")
    SYSTEM_LOGGER.info("="*50)
    
    # 第一步：物理环境查验
    pre_flight_check()

    try:
        # 第二步：唤醒大厂级面向对象总控管线
        pipeline = MasterDataPipeline()
        
        # 第三步：V6.0 全流程一键贯穿 (已挂载 LLM 大脑)
        pipeline.execute_pipeline()
        
        SYSTEM_LOGGER.info("\n🎉 报告指挥官，V6.0 引擎运行成功！黄金大盘、灰度捡漏池与阵亡名册已全部完成云端落锁！")
    except Exception as e:
        SYSTEM_LOGGER.error(f"\n🚨 [FATAL ERROR] 引擎主轴遭遇致命异常，系统已触发物理熔断！报错日志: {e}")

if __name__ == "__main__":
    ignition()