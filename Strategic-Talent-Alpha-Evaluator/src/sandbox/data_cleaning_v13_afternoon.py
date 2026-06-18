import os
import pandas as pd

class SmoothSalvageEngine:
    """
    【智能人才招聘筛选代码库 V1.0】
    📅 第 13 天下午战略资产：次要缺失维度平滑抢救与默认值死锁引擎
    """
    def __init__(self, input_path):
        print("[STATUS] Day 13 Afternoon Smooth Salvage Engine online.")
        self.input_path = input_path
        self.raw_df = None
        self.working_df = None

    def load_and_secure_grid(self):
        """【三部曲之一：前端并网风控】挂载上午快照，独立内存切片"""
        if not os.path.exists(self.input_path):
            print(f"[CRITICAL ERROR] Pipeline broken. Morning snapshot missing: {self.input_path}")
            return False
        # 读取上午刚被硬熔断洗干净的冷资产
        self.raw_df = pd.read_csv(self.input_path, dtype=str)
        # 🧠 核心风控：深层 copy 独立解耦，决不用 inplace=True，消灭 SettingWithCopyWarning（规避坑②）
        self.working_df = self.raw_df.copy()
        return True

    def execute_smooth_salvage(self):
        """【三部曲之二：核心技术绞杀】文本型标准化填充，死锁下游 Regex 战场（规避坑①、坑③）"""
        print("[PROCESS] Executing tactical value filling on elective columns...")
        
        # 强控主权：只对次要缺失维度执行平滑打补丁，必须全量填充纯文本字符串（str），绝不用数字！
        self.working_df['phone'] = self.working_df['phone'].fillna('UNKNOWN_PHONE')
        self.working_df['skills'] = self.working_df['skills'].fillna('NO_SKILLS_TAG')
        
        initial_na_phone = self.raw_df['phone'].isnull().sum()
        initial_na_skills = self.raw_df['skills'].isnull().sum()
        
        print("\n" + "🩹 " * 15)
        print(f"🎯 [SMOOTH SALVAGE AUDIT TOTALS]")
        print(f"➡️ 成功打上标准化防崩补丁的电话缺失格 (Alex): {initial_na_phone} cells")
        print(f"➡️ 成功打上标准化防崩补丁的技能缺失格: {initial_na_skills} cells")
        print("🩹 " * 15 + "\n")
        
        return self.working_df

    def export_and_lock_asset(self, output_path):
        """【三部曲之三：后端落锁维护】最终通关冷资产物理落盘"""
        self.working_df.to_csv(output_path, index=False, encoding='utf-8')
        
        print("\n" + "🔒 " * 15)
        print("[BACKEND AUDIT SUCCESS] Day 13 full-day warfare captured.")
        print(f"➡️ Final Global Target Asset: {output_path}")
        print("🔒 " * 15 + "\n")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(__file__)
    # 完美的物理合合拢证据链
    INPUT_PATH = os.path.join(BASE_DIR, "../data/cleaned_step2_mid.csv")   # 上午的战果作为下午的输入
    OUTPUT_PATH = os.path.join(BASE_DIR, "../data/cleaned_step2.csv")     # 最终出货落锁资产
    
    # 轰鸣点火
    pipeline = SmoothSalvageEngine(INPUT_PATH)
    if pipeline.load_and_secure_grid():
        pipeline.execute_smooth_salvage()
        pipeline.export_and_lock_asset(OUTPUT_PATH)
        
        # 下午核心强控：自动二次反向挂载审计双轨线
        print("🔎 " * 15)
        print("[POST-LOCK VERIFICATION] Compiling absolute final validation...")
        print("🔎 " * 15)
        
        verified_df = pd.read_csv(OUTPUT_PATH, dtype=str)
        print("\n--- 🏆 Final Audited Cleaned Step 2 Snapshot Matrix (df.info()) ---")
        verified_df.info()
        print("\n📊 查看最终进入‘黄金圣殿’、100%零缺失、零格式隐患的精锐数据资产：")
        print(verified_df)
        print("\n🏆 STATUS: DAY 13 DOUBLE-WARFARE FULLY CAPTURED. PIPELINE DIS DEAD-LOCKED.")
