import os
import pandas as pd
from src.utils.helpers import (
    extract_regex_feature, 
    extract_all_skills, 
    normalize_skills
)
from config import settings
from src.core.scoring import BusinessScoringEngine

class MasterDataPipeline:
    def __init__(self):
        # 修正：调用新的存储注册表字典，执行绝对路径挂载
        self.input_path = settings.STORAGE_REGISTRY['input_csv']
        self.output_path = settings.STORAGE_REGISTRY['master_output_csv']
        self.df = None

    def load_asset(self):
        print("\n[STAGE 1] --- 前端并网风控 ---")
        if not os.path.exists(self.input_path):
            print(f"🛑 错误：找不到资产文件: {self.input_path}")
            return False
        self.df = pd.read_csv(self.input_path, dtype=str)
        
        # 注入防崩补丁：初始化 project_tags 列，确保打分引擎有合法输入源进行撞击
        if 'project_tags' not in self.df.columns:
            self.df['project_tags'] = ""
            
        print(f"✅ 资产并网成功. 初始行数: {len(self.df)}")
        return True

    def validate_data_contract(func):
        def wrapper(self, *args, **kwargs):
            if self.df is None or self.df.empty:
                print("🚨 [熔断警告]：输入数据为空，流程终止！")
                return
            result = func(self, *args, **kwargs)
            if 'standard_skills' in self.df.columns and self.df['standard_skills'].isnull().any():
                print("⚠️ [审计警告]：检测到缺失标准技能标签，请审查熔断策略！")
            return result
        return wrapper

    @validate_data_contract  
    def execute_pipeline(self):
        print("\n[STAGE 2] --- 核心技术绞杀与特征提取 ---")
        
        # 基础熔断
        if 'email' in self.df.columns:
            self.df = self.df.dropna(subset=['email'])
        
        # 自动化特征剥离
        print(f"[TELEMETRY] 正在处理特征源列: {settings.RESUME_COLUMN}")
        
        self.df['extracted_email'] = self.df['email'].apply(
            lambda x: extract_regex_feature(x, settings.EMAIL_PATTERN)
        )
        
        self.df['raw_skills'] = self.df[settings.RESUME_COLUMN].apply(
            lambda x: extract_all_skills(x, settings.SKILL_PATTERN)
        )
        
        # 降维归一化
        self.df['standard_skills'] = self.df['raw_skills'].apply(
            lambda x: normalize_skills(x, settings.SKILL_MAPPING)
        )
        
        # 🚀 核心替换：物理级联双轨打分引擎，执行原始分计算、交叉熔断与大盘分配
        print("[TELEMETRY] 启动大盘双轨打分引擎...")
        self.df = BusinessScoringEngine.evaluate_pipeline_scores(self.df)
        print("[TELEMETRY] 商业打分引擎点火完毕，多维加权分析已落盘。")

    def export_deliverable(self):
        print("\n[STAGE 3] --- 后端落锁维护 ---")
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.df.to_csv(self.output_path, index=False, encoding='utf-8')
        print(f"✅ 黄金资产已落锁至: {self.output_path}")