import os
import pandas as pd
from src.utils.helpers import extract_regex_feature, extract_all_skills
from config import settings

class MasterDataPipeline:
    def __init__(self):
        self.input_path = settings.INPUT_PATH
        self.output_path = settings.OUTPUT_PATH
        self.df = None

    def load_asset(self):
        print("\n[STAGE 1] --- 🛡️ 前端并网风控 ---")
        if not os.path.exists(self.input_path):
            print(f"🛑 错误：找不到资产文件: {self.input_path}")
            return False
        self.df = pd.read_csv(self.input_path, dtype=str)
        print(f"✅ 资产并网成功. 初始行数: {len(self.df)}")
        return True

    def execute_pipeline(self):
        print("\n[STAGE 2] --- ⚔️ 核心技术绞杀与特征提取 ---")
        
        # 1. 基础熔断
        if 'email' in self.df.columns:
            self.df = self.df.dropna(subset=['email'])
        
        # 2. 自动化特征剥离
        print(f"[TELEMETRY] 正在处理列: {settings.RESUME_COLUMN}")
        
        # 提取 email (假设 CSV 里有 email 列)
        self.df['extracted_email'] = self.df['email'].apply(
            lambda x: extract_regex_feature(x, settings.EMAIL_PATTERN)
        )
        # 提取 skills
        self.df['extracted_skills'] = self.df[settings.RESUME_COLUMN].apply(
            lambda x: extract_all_skills(x, settings.SKILL_PATTERN)
        )
        print("✅ 特征剥离已完成.")

    def export_deliverable(self):
        print("\n[STAGE 3] --- 🔒 后端落锁维护 ---")
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.df.to_csv(self.output_path, index=False, encoding='utf-8')
        print(f"✅ 黄金资产已落锁至: {self.output_path}")