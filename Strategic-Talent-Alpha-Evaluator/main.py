import sys
import os

# 强行拉齐交通网络，解决全局模块导入路径报错
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.pipeline import MasterDataPipeline

def ignition():
    print("\n🚀 [SYSTEM CENTRAL] V4.0 智能人才招聘筛选引擎点火启动...")
    try:
        pipeline = MasterDataPipeline()
        
        # V4.0 全流程一键贯穿：
        # Phase 0 (ETL去重/PoW) -> Phase 1 (稳定性扣分) -> Phase 2&3 (能力/双底线) -> Phase 3.5 (Talent Alpha) -> Phase 4&5 (三库分发落盘)
        pipeline.execute_pipeline()
        
        print("\n🎉 报告指挥官，V4.0 引擎运行成功！黄金大盘、灰度捡漏池与阵亡名册已全部落锁！")
    except Exception as e:
        print(f"\n🚨 [SYSTEM ERROR] 引擎运行遭遇异常，报错日志: {e}")

if __name__ == "__main__":
    ignition()
