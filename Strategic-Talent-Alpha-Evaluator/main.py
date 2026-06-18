import sys
import os

# 强行拉齐交通网络，解决路径报错
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.pipeline import MasterDataPipeline

def ignition():
    print("\n🚀 [SYSTEM CENTRAL] 引擎启动...")
    pipeline = MasterDataPipeline()
    if pipeline.load_asset():
        pipeline.execute_pipeline()
        pipeline.export_deliverable()
        print("🎉 报告指挥官，引擎运行成功，当前商业决策打分权重已加载！")

if __name__ == "__main__":
    ignition()
