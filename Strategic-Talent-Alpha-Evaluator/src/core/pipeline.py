import os
import json
import pandas as pd
from tqdm import tqdm  # 🆕 降维打击外挂 1：引入雷达探针
from config import settings
from src.core.etl_cleaner import ETLCleaner
from src.core.stability import StabilityScoringEngine
from src.core.capability import CapabilityScoringEngine
from src.core.json_validator import JSONEnforcer  # 🆕 降维打击外挂 2：引入 JSON 锁死大闸

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
        # Phase 0: ETL 数据并网与探针提取 (包含密度去重法)
        # --------------------------------------------------
        etl = ETLCleaner()
        self.df = etl.run_pipeline()
        
        # 启动后续引擎
        self._run_engines()

    @validate_data_contract
    def _run_engines(self):
        # Phase 1: 稳定性风控与红黄牌大闸
        self.df = StabilityScoringEngine.process_dataframe(self.df)

        # Phase 2 & 3: 核心能力加分与双底线熔断
        self.df = CapabilityScoringEngine.process_dataframe(self.df)

        # Phase 3.5: 动态权重合成与 AI 战略建议生成
        self._apply_dynamic_talent_alpha()

        # Phase 4: 终端商业分发与排序
        self._route_and_sort_assets()

        # Phase 5: 物理落盘封存
        self.export_deliverables()

    def _apply_dynamic_talent_alpha(self):
        print("\n[STAGE 3] 启动 V4.0 动态业务场景变形引擎与 JSON 锁死探针...")
        profile_name = settings.ACTIVE_PROFILE
        profile_data = settings.TALENT_WEIGHT_PROFILES.get(profile_name)
        
        if not profile_data:
            weights = {"capability": 0.33, "potential": 0.33, "stability": 0.33}
        else:
            weights = profile_data['weights']
            print(f"🎯 注入业务指令: {profile_name} ({profile_data['desc']})")

        # 🚀 激活 Pandas 的多线程/迭代进度条雷达！
        tqdm.pandas(desc="⚙️ 万级数据吞吐中...")
        
        # 实例化第22天的执法大闸
        enforcer = JSONEnforcer()

        def _calculate_and_validate(row):
            # 🛡️ 降维打击外挂 3：防雪崩物理隔离舱（哪怕出错也绝不死机）
            try:
                # 1. 抽取基础分
                capability = float(row.get('Tech_Score', 0)) + float(row.get('Project_Score', 0))
                potential = float(row.get('Potential_Score', 0))
                stability = float(row.get('Stability_Score', 0))
                
                # 2. 算分与代码主权溢价
                if row.get('triage_flag') == 'RED':
                    alpha = 0.0
                else:
                    alpha = (capability * weights['capability']) + \
                            (potential * weights['potential']) + \
                            (stability * weights['stability'])
                    if row.get('Has_PoW', False):
                        alpha *= 1.2
                
                alpha = round(alpha, 2)
                
                # 3. 完美合龙大模型 JSON 锁死宪法
                # (业务场景：将算出的分数送给LLM生成战略建议，然后必须经过大闸校验才能回到系统)
                mock_llm_json = json.dumps({
                    "candidate_id": str(row.get('email', 'unknown')),
                    "capability_score": capability,
                    "stability_score": stability,
                    "talent_alpha": alpha,
                    "is_high_risk": True if row.get('triage_flag') == 'RED' else False,
                    "risk_tags": ["High_Risk"] if row.get('triage_flag') == 'RED' else [],
                    "strategic_advice": "核心战神，立刻安排面试！" if alpha > 75 else ("一票否决" if row.get('triage_flag') == 'RED' else "常规储备池")
                })
                
                # 强制通过 JSONEnforcer 执法清洗
                validated_data = enforcer.validate_and_repair(mock_llm_json)
                
                # 双列返回：Alpha 分数 和 给 HR 的战略建议
                return pd.Series([validated_data['talent_alpha'], validated_data['strategic_advice']])
                
            except Exception as e:
                # ☠️ 万一某份简历格式极度变态导致报错，启动阵亡兜底，掩护其他数据安全通过！
                fallback = enforcer._generate_fallback_json()
                return pd.Series([0.0, fallback['strategic_advice']])

        # 🚀 降维打击：将普通的 apply 替换为 progress_apply！
        self.df[['Talent_Alpha', 'Strategic_Advice']] = self.df.progress_apply(_calculate_and_validate, axis=1)

    def _route_and_sort_assets(self):
        self.df_green = self.df[self.df['triage_flag'] == 'GREEN'].copy()
        self.df_yellow = self.df[self.df['triage_flag'] == 'YELLOW'].copy()
        self.df_red = self.df[self.df['triage_flag'] == 'RED'].copy()
        
        # 降维打击要求：暴力按照 Talent_Alpha 从高到低排序，只把最牛的人推给企业！
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
            # 自动展示 Top 3 战神！
            print("\n👑 [大盘简报] 斩获黄金池 Top 3 超级战神：")
            print(self.df_green[['email', 'Talent_Alpha', 'Strategic_Advice']].head(3).to_string(index=False))
            
        if not self.df_yellow.empty:
            self.df_yellow.to_csv(self.output_yellow, index=False, encoding='utf-8-sig')
            print(f"\n⚠️ 捡漏审计池已落锁: {self.output_yellow}")
            
        if not self.df_red.empty:
            cols_to_keep = [c for c in self.df_red.columns if c not in ['Tech_Score', 'Project_Score', 'Potential_Score', 'Talent_Alpha']]
            self.df_red[cols_to_keep].to_csv(self.output_red, index=False, encoding='utf-8-sig')
            print(f"☠️ 阵亡名册及死因已封存: {self.output_red}")