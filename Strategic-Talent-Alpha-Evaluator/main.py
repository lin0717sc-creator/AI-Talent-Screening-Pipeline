import os
import sys

# 👑 拦截架构暗坑：在程序启动的最先一毫秒，强行将项目根目录并入系统搜寻网络
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

# 跨舱调用，血缘极度纯净
from config import settings
from src.core.pipeline import MasterDataPipeline

def ignition_sequence():
    print("\n" + "🔥" * 25)
    print("👑 [SYSTEM CENTRAL] V1.0 Modular Pipeline Firing Up...")
    print("🔥" * 25)
    
    # 动态开辟日志账本区
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    
    # 提车：实例化战车，全量喂入中央内阁的子弹
    pipeline = MasterDataPipeline(
        input_path=settings.INPUT_PATH,
        output_path=settings.OUTPUT_PATH,
        tech_pattern=settings.TECH_PATTERN,
        fill_rules=settings.FILL_RULES
    )
    
    # 全自动防线链条触发
    if pipeline.load_asset():
        pipeline.execute_pipeline()
        pipeline.export_deliverable()
        print(f"\n🏆 [SUCCESS] Execution complete. Deliverable secured into golden zone.")
    else:
        print(f"\n🛑 [FAILED] Ignition aborted by Wind Control windlock.")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    ignition_sequence()
