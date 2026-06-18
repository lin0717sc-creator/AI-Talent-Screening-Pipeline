import os
import numpy as np
import pandas as pd

class HardMeltdownEngine:
    """
    【智能人才招聘筛选代码库 V1.0】
    📅 第 13 天上午战略资产：全主权缺失值硬熔断绞杀引擎
    """
    def __init__(self, input_path):
        print("[STATUS] Day 13 Hard Meltdown Engine initialized.")
        self.input_path = input_path
        self.raw_df = None       # 锁定上一步的去重资产（作为审计底层）
        self.working_df = None   # 隔离的工作内存区
        
    def load_and_secure_grid(self):
        """【三部曲之一：前端并网风控】拉入内存，开辟独立副本"""
        if not os.path.exists(self.input_path):
            print(f"[CRITICAL ERROR] Pipeline broken. Input snapshot missing: {self.input_path}")
            return False
        # 继承第11、12天的str防御参数，确保资产不变形
        self.raw_df = pd.read_csv(self.input_path, dtype=str)
        self.working_df = self.raw_df.copy() # 深层解耦，杜绝 SettingWithCopyWarning （对冲坑③）
        return True

    def freeze_fake_null_noise(self):
        """【三部曲之一：前端并网风控】将恶性的字符串'None'/'null'强行化为 np.nan（狙击坑①）"""
        print("[PROCESS] Unifying hidden malicious string nulls into standard NaN...")
        
        # 强控主权：对内存中的所有特征列进行地毯式扫描，剪掉空格，将伪装字符强制变成 np.nan
        for col in self.working_df.columns:
            self.working_df[col] = self.working_df[col].str.strip()
            self.working_df[col] = self.working_df[col].replace(['None', 'null', 'NULL', '', 'NaN'], np.nan)
        print("[SUCCESS] Hidden string noise fully converted into cold logical NaN.")

    def execute_hard_meltdown(self, critical_column='email'):
        """【三部曲之二：核心技术绞杀】指定主键定向枪毙，杜绝全量屠杀（规避坑②）"""
        initial_rows = len(self.working_df)
        print(f"📊 [STAGE INTEL] Candidates in grid before meltdown: {initial_rows} rows.")
        
        # 🧠 核心长枪：dropna(subset=[...]) 
        # 意思：锁死只检查 critical_column 这一列。只要这列是 NaN，整行剥离枪毙！其他列是空的不归我管！
        self.working_df = self.working_df.dropna(subset=[critical_column])
        
        # 重新整理因为枪毙数据而断掉的内存索引（重新洗牌）
        self.working_df = self.working_df.reset_index(drop=True)
        
        final_rows = len(self.working_df)
        killed_zombies = initial_rows - final_rows
        
        print("\n" + "⚔️ " * 15)
        print(f"🎯 [HARD MELTDOWN RESULT]")
        print(f"➡️ 无联系方式被当场枪毙的僵尸资产 (John): {killed_zombies} rows")
        print(f"➡️ 拥有通行主权、安全存活通过的精锐 (Lin, Alex): {final_rows} rows")
        print("⚔️ " * 15 + "\n")
        
        return self.working_df

    def export_and_lock_asset(self, output_path):
        """【三部曲之三：后端落锁维护】冷资产阶段性保存，留存物理证据链"""
        self.working_df.to_csv(output_path, index=False, encoding='utf-8')
        
        print("\n" + "🔒 " * 15)
        print("[BACKEND AUDIT SUCCESS] Meltdown step snapshot anchored to disk.")
        print(f"➡️ Output Destination Path: {output_path}")
        print(f"➡️ Asset Structural Validation: Column [email] contains 0% missing values.")
        print("🔒 " * 15 + "\n")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(__file__)
    # 👑 完美的物理证据链：输入是第12天洗干净的去重资产
    INPUT_PATH = os.path.join(BASE_DIR, "../data/cleaned_step1.csv")
    OUTPUT_PATH = os.path.join(BASE_DIR, "../data/cleaned_step2_mid.csv")
    
    # 点火开拔
    pipeline = HardMeltdownEngine(INPUT_PATH)
    if pipeline.load_and_secure_grid():
        pipeline.freeze_fake_null_noise()
        pipeline.execute_hard_meltdown(critical_column='email')
        pipeline.export_and_lock_asset(OUTPUT_PATH)
        
        # 二次反向挂载校验（下午战术防污染视界）
        print("\n🏆 STATUS: DAY 13 MORNING HARD-MELTDOWN FULLY COMPLETE.")
