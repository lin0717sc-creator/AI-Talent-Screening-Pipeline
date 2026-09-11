import os
import json
import pandas as pd
from src.core.llm_evaluator import LLMEvaluator
from tqdm import tqdm  # 🆕 降维打击外挂 1：引入雷达探针
from config import settings
from src.core.etl_cleaner import ETLCleaner
from src.core.stability import StabilityScoringEngine
from src.core.capability import CapabilityScoringEngine
from src.core.json_validator import JSONEnforcer  # 🆕 降维打击外挂 2：引入 JSON 锁死大闸
from src.core.llm_evaluator import deepseek_strategic_scan  # 🚀 V6.0 引入 LLM 大脑
from src.utils.logger import SYSTEM_LOGGER  # 🚀 V5.0 全局工业雷达


class MasterDataPipeline:
    """
    V6.0 全局打分与风控漏斗 (总控大脑 - 挂载 LLM 反虚假繁荣引擎)
    """
    def __init__(self):
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
                SYSTEM_LOGGER.error("🚨 [熔断警告]：输入数据为空，流程终止！")
                return
            return func(self, *args, **kwargs)
        return wrapper

    def execute_pipeline(self):
        """主线流水线启动函数"""
        # --------------------------------------------------
        # Phase 0: ETL 数据并网与探针提取 (包含密度去重法)
        # --------------------------------------------------
        SYSTEM_LOGGER.info("[STAGE 0] 启动 ETL 数据并网与探针提取...")
        etl = ETLCleaner()
        self.df = etl.run_pipeline()
        
        # 启动后续引擎
        self._run_engines()

    @validate_data_contract
    def _run_engines(self):

        # Phase 1: 稳定性风控与红黄牌大闸
        SYSTEM_LOGGER.info("[STAGE 1] 启动稳定性风控与红黄牌大闸...")
        self.df = StabilityScoringEngine.process_dataframe(self.df)

        # Phase 2 & 3: 核心能力加分与双底线熔断
        SYSTEM_LOGGER.info("[STAGE 2] 启动 核心能力加分与双底线熔断...")
        self.df = CapabilityScoringEngine.process_dataframe(self.df)

        # Phase 3.5: 动态权重合成与 AI 战略建议生成
        self._apply_dynamic_talent_alpha()

        # Phase 4: 终端商业分发与排序
        self._route_and_sort_assets()

        # 🚀 降维打击外挂注入：仅仅针对筛选出的“黄金大盘”进行 LLM 深度审判
        self._run_llm_deep_scan()

        # 物理落盘封存
        self.export_deliverables()

    def _apply_dynamic_talent_alpha(self):
        SYSTEM_LOGGER.info("[STAGE 3] 启动动态业务场景变形引擎与 JSON 锁死探针...")
        profile_name = settings.ACTIVE_PROFILE
        profile_data = settings.TALENT_WEIGHT_PROFILES.get(profile_name)

        if not profile_data:
            weights = {"capability": 0.33, "potential": 0.33, "stability": 0.33}
        else:
            weights = profile_data['weights']

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
                    # 🚀 架构升级：废弃静态 1.2x 拍脑袋溢价，引入动态开源信号算子
                    if str(row.get('Has_PoW', 'False')).lower() in ['true', '1']:
                        # 真实场景中，这里会异步调用 GitHub GraphQL API 获取参数。
                        # 当前处于挡板模式，我们做安全 Mock，并设定极度收敛的惩罚机制：
                        
                        # 假设我们通过探针提取到了这两个核心指标 (0~1 之间)
                        originality = float(row.get('PoW_Originality', 0.3))    # 原创度 (Fork / AI 占比)
                        commit_depth = float(row.get('PoW_CommitDepth', 0.5))   # 提交深度 (真实代码行数)
                        
                        # 公式: OpenSourceSignal = f(Originality, CommitDepth)
                        pow_signal = (originality * 0.7) + (commit_depth * 0.3)
                        
                        # 动态溢价范围压缩在 1.00x 到 1.15x 之间。
                        # 绝不盲目给 1.2，如果是纯 Fork 刷星 (pow_signal极低)，溢价近乎为 0！
                        dynamic_premium = pow_signal * 0.15 
                        alpha *= (1.0 + dynamic_premium)
                        SYSTEM_LOGGER.info(f"  🔗 提取动态开源信号 (PoW): {dynamic_premium:.2%} 溢价")
                
                alpha = round(alpha, 2)
                
                # 3. 完美合龙大模型 JSON 锁死宪法
                # (业务场景：将算出的分数送给LLM生成战略建议，然后必须经过大闸校验才能回到系统)
                mock_llm_json = json.dumps({
                    "candidate_id": str(row.get('email', 'unknown')),
                    "capability_score": capability,
                    "stability_score": stability,
                    "talent_alpha": alpha,
                    "is_high_risk": True if row.get('triage_flag') == 'RED' else False,
                    "risk_tags": ["Logical_Inconsistency"] if row.get('triage_flag') == 'RED' else [],
                    "strategic_advice": "核心战神，立刻安排面试！" if alpha > 75 else ("一票否决" if row.get('triage_flag') == 'RED' else "常规储备池"),
                    # 🚀 降维打击外挂 4：植入全局兜底证据矩阵，满足宪法 Schema 的绝对审查！
                    "evidence_matrix": {
                        "core_claim": "基于规则引擎计算出的综合能力指标",
                        "supporting_evidence": [f"计算出基础能力分: {capability}", f"计算出稳定性指标: {stability}"],
                        "missing_evidence": ["需等待 LLM 深度精读"],
                        "consistency_score": "Medium"
                    }
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
        SYSTEM_LOGGER.info("[STAGE 4] 启动终端商业分发与排序...")
        self.df_green = self.df[self.df['triage_flag'] == 'GREEN'].copy()
        self.df_yellow = self.df[self.df['triage_flag'] == 'YELLOW'].copy()
        self.df_red = self.df[self.df['triage_flag'] == 'RED'].copy()


        # 降维打击要求：暴力按照 Talent_Alpha 从高到低排序，只把最牛的人推给企业！
        if not self.df_green.empty:
            self.df_green = self.df_green.sort_values(by='Talent_Alpha', ascending=False)
        if not self.df_yellow.empty:
            self.df_yellow = self.df_yellow.sort_values(by='Talent_Alpha', ascending=False)


    # ==========================================
    # 🚀 V6.0 新增外挂模块：LLM 大模型终极裁决
    # ==========================================
    def _run_llm_deep_scan(self):
        if self.df_green is None or self.df_green.empty:
            return
            
        SYSTEM_LOGGER.info("[STAGE 4.5] 🧠 启动 DeepSeek 神经中枢，对黄金大盘(Top 50)进行降维精读...")
        
        # 截取前 50 名，好钢用在刀刃上，防止 API 账单爆炸
        top_50 = self.df_green.head(50).copy()
        
        # 容错机制：如果没有 project_desc，防止报错
        if 'project_desc' not in top_50.columns:
            top_50['project_desc'] = "无详细项目描述"

        # ==========================================
        # 🚀 衔接新代码：唤醒带有指纹缓存的 LLMEvaluator
        # ==========================================
        llm_engine = LLMEvaluator()
        
        def apply_llm_with_cache(row):
            project_text = row.get('project_desc', '')
            evidence = row.get('Evidence_Graph', '{}')
            # 呼叫缓存引擎！（不仅传简历，还把第一层收集的结构化证据传进去）
            return llm_engine.evaluate_project(project_text, evidence)
            
        # 挂载 LLM (使用新的缓存引擎，不再用 apply 纯文本，而是 apply 整个 row)
        llm_results = top_50.apply(apply_llm_with_cache, axis=1)

        # ==========================================
        # 👇 绝对不能丢的灵魂👇
        # ==========================================
        top_50['吹牛杠杆率'] = llm_results.apply(lambda x: x.get('bullshit_ratio'))
        top_50['诚实自洽护航'] = llm_results.apply(lambda x: x.get('integrity_tag'))
        top_50['LLM_高管点评'] = llm_results.apply(lambda x: x.get('strategic_advice'))

        # 🚀 降维打击外挂 5：物理封存案件调查板证据
        top_50['evidence_matrix'] = llm_results.apply(lambda x: json.dumps(x.get('evidence_matrix', {}), ensure_ascii=False))

        SYSTEM_LOGGER.info("[STAGE 4.6] ⚖️ 启动大模型裁决执行官：执行打五折与护航溢价...")
        def apply_llm_裁决(row):
            final_score = row['Talent_Alpha']

            # 1. 斩杀 PPT 战神 (逻辑不变)
            if row['吹牛杠杆率'] == 'High':
                final_score *= 0.5  # 斩杀虚假繁荣
                SYSTEM_LOGGER.warning(f"  🔪 击杀PPT战神: {row.get('email', '')}，分数腰斩！")
                
            # 2. 🚀 升级：基于证据矩阵的一致性溢价 (Consistency Premium)
            try:
                evidence = json.loads(row.get('evidence_matrix', '{}'))
                consistency = evidence.get('consistency_score', 'Medium')
            except:
                consistency = 'Medium'
                
            # 如果主张与证据极度自洽 (High)，才给予 1.2 倍溢价
            if consistency == 'High': 
                final_score *= 1.2  
                SYSTEM_LOGGER.info(f"  🛡️ 触发一致性溢价: {row.get('email', '')} 证据链完美闭环，获得1.2倍加成！")
                
            return round(final_score, 2)
            
        top_50['Talent_Alpha'] = top_50.apply(apply_llm_裁决, axis=1)
        
        # 重新排序，并将这经过大模型洗礼的 Top 50 塞回黄金大盘
        top_50 = top_50.sort_values(by='Talent_Alpha', ascending=False)
        self.df_green.update(top_50)
        
        # 同步新增的列
        for col in ['吹牛杠杆率', '诚实自洽护航', 'LLM_高管点评', 'evidence_matrix']:
            if col not in self.df_green.columns:
                self.df_green[col] = None
            self.df_green.loc[top_50.index, col] = top_50[col]
            
        self.df_green = self.df_green.sort_values(by='Talent_Alpha', ascending=False)

    def export_deliverables(self):
        SYSTEM_LOGGER.info("\n[STAGE 5] --- 后端物理落锁 ---")
        os.makedirs(os.path.dirname(self.output_green), exist_ok=True)
        
        if not self.df_green.empty:
            self.df_green.to_csv(self.output_green, index=False, encoding='utf-8-sig')
            SYSTEM_LOGGER.info(f"✅ 黄金大盘已落锁: {self.output_green}")
            # 自动展示 Top 3 战神！
            SYSTEM_LOGGER.info("\n👑 [大盘简报] 斩获黄金池 Top 3 超级战神：")

            # 确保 DataFrame 不为空且包含 Talent_Alpha 列
            if not self.df_green.empty and 'Talent_Alpha' in self.df_green.columns:
                # 按最终身价从高到低排序，取前 3 名
                top3 = self.df_green.sort_values(by='Talent_Alpha', ascending=False).head(3)

                for index, row in top3.iterrows():
                    email = row.get('email', 'Unknown_Geek')
                    score = row.get('Talent_Alpha', 0.0)
                    # 兼容 V6.0 的新字段
                    claim = row.get('吹牛杠杆率', 'Unknown')
                
                    print(f"  => 🏅 {email} | 综合分: {score:.1f} | 杠杆率: {claim}")
            else:
                print("  => 🈳 当前阈值下，黄金池无人幸存。")
            

        if not self.df_yellow.empty:
            self.df_yellow.to_csv(self.output_yellow, index=False, encoding='utf-8-sig')
            SYSTEM_LOGGER.info(f"✅ 捡漏池已落锁: {self.output_yellow}")
            
        if not self.df_red.empty:
            cols_to_keep = [c for c in self.df_red.columns if c not in ['Tech_Score', 'Project_Score', 'Potential_Score', 'Talent_Alpha']]
            self.df_red[cols_to_keep].to_csv(self.output_red, index=False, encoding='utf-8-sig')
            SYSTEM_LOGGER.info(f"☠️ 阵亡名册及死因已封存: {self.output_red}")
