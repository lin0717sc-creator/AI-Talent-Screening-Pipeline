import os
import re
import pandas as pd

class PandasRegexInjectionEngine:
    """
    👑 【智能人才招聘筛选代码库 V1.0】
    📅 第 14 天：Regex正则引擎与Pandas并网流水线（纯净解耦版）
    
    职责：只负责提取 standard_skills，绝对不碰 age 和 gender！留给下游沙盒处理。
    """
    def __init__(self, input_path):
        print("[STATUS] Day 14 Regex Injection Engine online.")
        self.input_path = input_path
        self.raw_df = None
        self.working_df = None
        self.tech_pattern = re.compile(r'python|tableau|data analytics', re.IGNORECASE)

    def load_and_secure_grid(self):
        if not os.path.exists(self.input_path):
            print(f"[CRITICAL ERROR] Pipeline broken. Input missing: {self.input_path}")
            return False
        self.raw_df = pd.read_csv(self.input_path, dtype=str)
        self.working_df = self.raw_df.copy() 
        return True

    def _execute_standard_extraction(self, text_cell):
        if not isinstance(text_cell, str) or text_cell == 'NO_SKILLS_TAG':
            return 'NO_SKILLS_TAG'
            
        matches = self.tech_pattern.findall(text_cell)
        if matches:
            raw_tags = [m.strip().title() for m in matches]
            combined_str = ", ".join(raw_tags)
            pure_set = set([item.strip() for item in combined_str.split(',') if item.strip()])
            return ", ".join(sorted(list(pure_set)))
        else:
            return 'NON_STANDARD_SKILLS'

    def execute_sovereign_cleansing_pipeline(self):
        """核心动作：只做标签标准化，剔除旧 skills 列"""
        print("[PROCESS] Firing morning Regex kernel for [standard_skills] extraction...")
        self.working_df['standard_skills'] = self.working_df['skills'].apply(lambda x: self._execute_standard_extraction(x))
        
        print("[SOVEREIGN CONTROL] Vaporizing legacy uncleaned [skills] to enforce version differentiation...")
        self.working_df = self.working_df.drop(['skills'], axis=1)
        
        # ⚠️ 注意：这里我们彻底去掉了 drop age/gender 的逻辑，把它们完好无损地输送给下一步的沙盒！
        return self.working_df

    def export_and_lock_asset(self, output_path):
        self.working_df.to_csv(output_path, index=False, encoding='utf-8')
        final_rows = len(self.working_df)
        print("\n" + "🔒 " * 15)
        print("[BACKEND AUDIT SUCCESS] Structural tags snapshot anchored to disk.")
        print(f"➡️ Local Destination Path: {output_path}")
        print(f"➡️ Total Asset Verified: {final_rows} rows locked into step 3.")
        print("🔒 " * 15 + "\n")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(__file__)
    INPUT_PATH = os.path.join(BASE_DIR, "../data/cleaned_step2.csv")
    OUTPUT_PATH = os.path.join(BASE_DIR, "../data/cleaned_step3.csv") 
    
    engine = PandasRegexInjectionEngine(INPUT_PATH)
    if engine.load_and_secure_grid():
        engine.execute_sovereign_cleansing_pipeline()
        engine.export_and_lock_asset(OUTPUT_PATH)
        
        verified_df = pd.read_csv(OUTPUT_PATH, dtype=str)
        print("\n--- Final Cleaned Snapshot Matrix Structure (df.info()) ---")
        print(verified_df.columns.tolist()) # 只打印列名，确认 age 和 gender 还在！
        print("\n🏆 STATUS: DAY 14 MORNING REGEX EXTRACTION COMPLETE. READY FOR SANDBOX.")
