# ==========================================
# 文件路径: src/core/pipeline.py
# ==========================================
import os
import pandas as pd
from config import settings
from src.core.etl_cleaner import ETLCleaner
from src.core.stability import StabilityScoringEngine
from src.core.capability import CapabilityScoringEngine

class MasterDataPipeline:
    """
    V4.0 全局打分与风控漏斗 (总控大脑)
    """
    def __init__(self):
        # 完美继承你的绝对路径字典寻址
        self.output_green = settings.STORAGE_REGISTRY['master_output_csv']
        self.output_yellow = self.output_green.replace('.csv', '_human_audit.csv')
        self.output_red = self.output_green.replace('.csv', '_rejected_audit.csv')
        
        self.df = None
        self.df_green = None
        self.df_yellow = None
        self.df_red = None

    # 🚀 继承你的老版绝招：数据契约防崩装饰器
    def validate_data_contract(func):
        def wrapper(self, *args, **kwargs):
            if self.df is None or self.df.empty:
                print("🚨 [熔断警告]：输入数据为空，流程终止！")
                return
            return func(self, *args, **kwargs)
        return wrapper

    def execute_pipeline(self):
        """主线流水线启动函数"""
        # --------------------------------------------------
        # Phase 0: ETL 数据并网与探针提取 (包含你的密度去重法)
        # --------------------------------------------------
        etl = ETLCleaner()
        self.df = etl.run_pipeline()
        
        # 启动后续引擎
        self._run_engines()

    @validate_data_contract
    def _run_engines(self):
        # --------------------------------------------------
        # Phase 1: 稳定性风控与红黄牌大闸 (扫雷下限)
        # --------------------------------------------------
        self.df = StabilityScoringEngine.process_dataframe(self.df)

        # --------------------------------------------------
        # Phase 2 & 3: 核心能力加分与双底线熔断 (提纯上限)
        # --------------------------------------------------
        self.df = CapabilityScoringEngine.process_dataframe(self.df)

        # --------------------------------------------------
        # Phase 3.5: 动态权重合成 (Talent Alpha 变形金刚)
        # --------------------------------------------------
        self._apply_dynamic_talent_alpha()

        # --------------------------------------------------
        # Phase 4: 终端商业分发与排序
        # --------------------------------------------------
        self._route_and_sort_assets()

        # --------------------------------------------------
        # Phase 5: 物理落盘封存
        # --------------------------------------------------
        self.export_deliverables()

    def _apply_dynamic_talent_alpha(self):
        print("\n[STAGE 3] 启动 V4.0 动态业务场景变形引擎...")
        profile_name = settings.ACTIVE_PROFILE
        profile_data = settings.TALENT_WEIGHT_PROFILES.get(profile_name)
        
        if not profile_data:
            weights = {"capability": 0.33, "potential": 0.33, "stability": 0.33}
        else:
            weights = profile_data['weights']
            print(f"🎯 注入业务指令: {profile_name} ({profile_data['desc']})")

        def _calculate_alpha(row):
            if row.get('triage_flag') == 'RED':
                return 0.0
                
            capability = float(row.get('Tech_Score', 0)) + float(row.get('Project_Score', 0))
            potential = float(row.get('Potential_Score', 0))
            stability = float(row.get('Stability_Score', 0))
            
            alpha = (capability * weights['capability']) + \
                    (potential * weights['potential']) + \
                    (stability * weights['stability'])
                    
            if row.get('Has_PoW', False):
                alpha *= 1.2
            return round(alpha, 2)

        self.df['Talent_Alpha'] = self.df.apply(_calculate_alpha, axis=1)

    def _route_and_sort_assets(self):
        self.df_green = self.df[self.df['triage_flag'] == 'GREEN'].copy()
        self.df_yellow = self.df[self.df['triage_flag'] == 'YELLOW'].copy()
        self.df_red = self.df[self.df['triage_flag'] == 'RED'].copy()
        
        if not self.df_green.empty:
            self.df_green = self.df_green.sort_values(by='Talent_Alpha', ascending=False)
        if not self.df_yellow.empty:
            self.df_yellow = self.df_yellow.sort_values(by='Talent_Alpha', ascending=False)
            
        print(f"\n[STAGE 4] 终端商业三库分发完毕！")
        print(f"  => 🟢 黄金大盘: {len(self.df_green)} 人 | 🟡 捡漏池: {len(self.df_yellow)} 人 | 🔴 坟墓池: {len(self.df_red)} 人")

    def export_deliverables(self):
        print("\n[STAGE 5] --- 后端物理落锁 ---")
        os.makedirs(os.path.dirname(self.output_green), exist_ok=True)
        
        if not self.df_green.empty:
            self.df_green.to_csv(self.output_green, index=False, encoding='utf-8-sig')
            print(f"✅ 黄金大盘已落锁: {self.output_green}")
            
        if not self.df_yellow.empty:
            self.df_yellow.to_csv(self.output_yellow, index=False, encoding='utf-8-sig')
            print(f"⚠️ 捡漏审计池已落锁: {self.output_yellow}")
            
        if not self.df_red.empty:
            cols_to_keep = [c for c in self.df_red.columns if c not in ['Tech_Score', 'Project_Score', 'Potential_Score', 'Talent_Alpha']]
            self.df_red[cols_to_keep].to_csv(self.output_red, index=False, encoding='utf-8-sig')
            print(f"☠️ 阵亡名册及死因已封存: {self.output_red}")