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
from src.utils.logger import SYSTEM_LOGGER  # 🚀 V5.0 全局工业雷达
# 👑 引入 V7.0 生化洗消舱
from src.core.canonicalizer import ResumeCanonicalizer

class MasterDataPipeline:
    """
    V7.1 全局打分与风控漏斗 (总控大脑 - 挂载 LLM 反虚假繁荣引擎)
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

        # 🚀 降维打击外挂注入：仅仅针对筛选出的“High-Priority Talent Pool (绿池)”进行 LLM 深度审判
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
                        # 🚨 修复：注释掉这行高频刷屏日志，或将其删除！
                        # SYSTEM_LOGGER.info(f"  🔗 提取动态开源信号 (PoW): {dynamic_premium:.2%} 溢价")
                
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
                    
                    # 🚀 替换为 V7.0 的主张建模兜底数据，骗过 JSON 大闸
                    "claim_modeling": [
                        {
                            "skill_claim": "基于规则引擎的基础能力初筛",
                            "evidence_span": f"计算出基础能力分: {capability}",
                            "evidence_strength": "Weak", 
                            "verification_status": "Insufficient"
                        }
                    ],
                    "interview_probes": ["需等待 LLM 深度精读后生成最终追问清单"]
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
    # 🚀 V7.1 新增外挂模块：LLM 大模型终极裁决
    # ==========================================
    def _run_llm_deep_scan(self):
        if self.df_green is None or self.df_green.empty:
            return
            
        SYSTEM_LOGGER.info("[STAGE 4.5] 🧠 启动 DeepSeek 神经中枢，对High-Priority Talent Pool (绿池)(Top 50)进行降维精读...")
        
        # 截取前 50 名，好钢用在刀刃上，防止 API 账单爆炸
        top_50 = self.df_green.head(50).copy()
        
        # 容错机制：如果没有 project_desc，防止报错
        if 'project_desc' not in top_50.columns:
            top_50['project_desc'] = "无详细项目描述"


        # ==========================================
        # 🚀 衔接新代码：唤醒带有指纹缓存的 LLMEvaluator 与 洗消舱
        # ==========================================
        llm_engine = LLMEvaluator()
        canonicalizer = ResumeCanonicalizer() # 👈 启动洗消舱
        
        def apply_llm_with_cache(row):
            project_text = str(row.get('project_desc', ''))
            evidence = str(row.get('Evidence_Graph', '{}'))
            
            # 1. 物理洗消：拦截并清理文本，提取出干净文本 (canonical_text) 和风险警告 (risk_flags)
            clean_doc = canonicalizer.normalize(project_text)
            
            # 2. 呼叫缓存引擎！（必须传入洗干净的 canonical_text）
            result = llm_engine.evaluate_project(clean_doc.canonical_text, evidence)
            
            # 3. 将洗消舱抓到的风险一起塞入结果中返回，方便后续落盘
            result['risk_flags_text'] = ", ".join(clean_doc.risk_flags) if clean_doc.risk_flags else "安全"
            return result
            
        # 挂载 LLM(使用新的缓存引擎，不再用 apply 纯文本，而是 apply 整个 row)
        llm_results = top_50.apply(apply_llm_with_cache, axis=1)


        # ==========================================
        # 👇 绝对不能丢的灵魂👇
        # ==========================================
        top_50['Claim-to-Evidence Ratio (主张实证倒挂率)'] = llm_results.apply(lambda x: x.get('bullshit_ratio'))
        top_50['Logical Consistency Guardrail (逻辑自洽)'] = llm_results.apply(lambda x: x.get('integrity_tag'))
        top_50['LLM_高管点评'] = llm_results.apply(lambda x: x.get('strategic_advice'))
        
        # 🚀 修改这里：提取新的 CEL 主张建模数组
        top_50['claim_modeling'] = llm_results.apply(lambda x: json.dumps(x.get('claim_modeling', []), ensure_ascii=False))

        # 👑 新增商业化大杀器：HR/CTO 面试追问清单 & 投毒风险 (这部分保持不变)
        top_50['【HR/CTO 面试追问清单】'] = llm_results.apply(
            lambda x: "\n".join(x.get('interview_probes', [])) if x.get('interview_probes', []) else "无追问建议"
        )

        top_50['Prompt Injection Risk (提示词注入预警)'] = llm_results.apply(lambda x: x.get('risk_flags_text'))


        SYSTEM_LOGGER.info("[STAGE 4.6 & 4.7] ⚖️ 启动最高法庭：执行三大指标物理分离与 2x2 风控路由...")
        
        def apply_decision_metrics(row):
            # 基础分兜底
            base_score = row.get('Talent_Alpha', 0.0)

            #🚀 升级版四态 CEL (Claim-Evidence-Logic) 结算
            try:
                # 解析大模型吐出的主张数组
                claim_models = json.loads(row.get('claim_modeling', '[]'))
            except:
                claim_models = []
                
            # 统计全新的四种校验状态
            total_claims = len(claim_models)
            supported_count = sum(1 for c in claim_models if c.get('verification_status') == 'SUPPORTED')
            contradicted_count = sum(1 for c in claim_models if c.get('verification_status') == 'CONTRADICTED')
            insufficient_count = sum(1 for c in claim_models if c.get('verification_status') == 'INSUFFICIENT_EVIDENCE')

            # --------------------------------------------------
            # 📊 指标 1：证据覆盖率 (Evidence Coverage)
            # --------------------------------------------------
            evidence_coverage = (supported_count / total_claims) if total_claims > 0 else 0.0
            
            # --------------------------------------------------
            # 📊 指标 2：置信度 (Confidence)
            # --------------------------------------------------
            confidence = evidence_coverage
            if contradicted_count > 0:
                confidence = confidence * 0.5  # 发现矛盾造假，系统极度不信任该简历
                
            # --------------------------------------------------
            # 📊 指标 3：能力分 (Capability Score) -> Talent_Alpha
            # --------------------------------------------------
            capability_score = base_score


            # 斩杀 Over-Packaged Claimant (过度包装型主张者) (保留绝对底线)
            if row.get('Claim-to-Evidence Ratio (主张实证倒挂率)') == 'High':
                capability_score *= 0.5
                SYSTEM_LOGGER.warning(f"  🔪 击杀PPT战神: {row.get('email', '')}，杠杆率过高，分数腰斩！")
                
            # 实力溢价：有真凭实据的主张给予加分
            capability_score += (supported_count * 5) 
            # 信用破产惩罚：造假主张直接重扣
            capability_score -= (contradicted_count * 20) 
            
            # 【不变量建立】：insufficient_count 绝对不参与扣分！疑罪从无！
            if insufficient_count > 0 and contradicted_count == 0:
                SYSTEM_LOGGER.info(f"  ⚖️ 疑罪从无: {row.get('email', '')} 存在 {insufficient_count} 处无证据主张，能力分不扣，仅降置信度。")
            
            # 确保分数在 0-100 之间
            capability_score = max(0.0, min(100.0, capability_score))


            # --------------------------------------------------
            # 🔀 2x2 商业风控路由 (Decision Matrix)
            # --------------------------------------------------
            CAP_THRESHOLD = 70.0    # 能力及格线 
            CONF_THRESHOLD = 0.5    # 置信度及格线 (50% 证据覆盖)
            
            if capability_score >= CAP_THRESHOLD and confidence >= CONF_THRESHOLD:
                decision_route = "GREEN"
                route_reason = "铁证如山：高能力 + 高置信，直通终面"
            elif capability_score >= CAP_THRESHOLD and confidence < CONF_THRESHOLD:
                decision_route = "YELLOW"
                route_reason = "潜力包装客：分数高但缺乏细节证据，需重点追问"
            elif capability_score < CAP_THRESHOLD and confidence >= CONF_THRESHOLD:
                decision_route = "RED"
                route_reason = "确诊水货：铁证表明其能力未达标，安全淘汰"
            else:
                # 🚨 核心价值观修复：低分 + 低置信度 -> 转黄池交由人工盲测，绝不误杀！
                decision_route = "YELLOW"
                route_reason = "Unsubstantiated Claimants (无实证包装者)：信息极度匮乏导致低分，拒绝淘汰，转人工"


            # ==================================================
            # 🚨 终极补丁：物理隔离安全告警与人才决策 (双通道仲裁)
            # ==================================================
            # 通道 A: 提取底层洗消舱传来的安全事件信号
            security_risk = str(row.get('Prompt Injection Risk (提示词注入预警)', '安全'))
            is_security_alert = (security_risk != '安全')
            
            # 通道 B: 结合仲裁
            if is_security_alert:
                # 无论他原本是神仙(GREEN)还是水货(RED)，只要触发了安全探针
                # 强制挂起至 YELLOW 池！绝不自动淘汰，防止误杀写了“注入攻击研究”的安全工程师
                decision_route = "YELLOW"
                route_reason = f"【🛑安全仲裁挂起】人才判决已被挂起。系统侦测到安全风险: [{security_risk}]。需安全员人工核实是真实攻击还是专业履历。"

            elif contradicted_count > 0 and decision_route == "GREEN":
                # 普通的业务造假降级
                decision_route = "YELLOW"
                route_reason = "触发业务造假警报：强行降级至人工池复核"

            return pd.Series([
                round(capability_score, 1),
                round(evidence_coverage, 2),
                round(confidence, 2),
                decision_route,
                route_reason
            ])

        # 接收并应用新的三大指标与路由判定
        top_50[['Talent_Alpha', 'Evidence_Coverage', 'LLM_Confidence', 'Final_Route', 'Route_Reason']] = top_50.apply(apply_decision_metrics, axis=1)


        # ==========================================
        # 将人员根据新路由分流回各大盘 (修复幽灵标签)
        # ==========================================
        green_survivors = top_50[top_50['Final_Route'] == 'GREEN'].copy()
        demoted_to_yellow = top_50[top_50['Final_Route'] == 'YELLOW'].copy()
        demoted_to_red = top_50[top_50['Final_Route'] == 'RED'].copy()
        
        # 1. 极其关键：从原始绿池中彻底剔除这批已经被大模型评估过的 50 个人
        self.df_green = self.df_green.drop(top_50.index, errors='ignore')
        
        # 🚨 修复：强制覆写 triage_flag，彻底抹除幽灵标签！
        if not green_survivors.empty:
            green_survivors['triage_flag'] = 'GREEN'
            self.df_green = pd.concat([green_survivors, self.df_green], ignore_index=True)
            self.df_green = self.df_green.sort_values(by='Talent_Alpha', ascending=False)
            
        if not demoted_to_yellow.empty:
            demoted_to_yellow['triage_flag'] = 'YELLOW'  # 👈 同步状态
            self.df_yellow = pd.concat([self.df_yellow, demoted_to_yellow], ignore_index=True)
            SYSTEM_LOGGER.warning(f"  ⚠️ 警报: {len(demoted_to_yellow)} 名候选人已落入黄池。")
            
        if not demoted_to_red.empty:
            demoted_to_red['triage_flag'] = 'RED'       # 👈 同步状态
            self.df_red = pd.concat([self.df_red, demoted_to_red], ignore_index=True)
            SYSTEM_LOGGER.warning(f"  ☠️ 警报: {len(demoted_to_red)} 名候选人直接打入红池淘汰。")


    def export_deliverables(self):
        SYSTEM_LOGGER.info("\n[STAGE 5] --- Backend Data Commit (后端数据提交) ---")
        os.makedirs(os.path.dirname(self.output_green), exist_ok=True)
        
        # ==========================================
        # 🚨 [V7.1 终极装甲] 物理清洗：碾平大模型生成的换行符，防止击穿 CSV
        # ==========================================
        for df in [self.df_green, self.df_yellow, self.df_red]:
            # 替换为真实的列名！
            actual_col_name = '【HR/CTO 面试追问清单】' 
            if not df.empty and actual_col_name in df.columns:
                df[actual_col_name] = df[actual_col_name].astype(str).str.replace('\n', ' ', regex=False)
        # ==========================================

        if not self.df_green.empty:
            self.df_green.to_csv(self.output_green, index=False, encoding='utf-8-sig')
            SYSTEM_LOGGER.info(f"✅ High-Priority Talent Pool (绿池)已落锁: {self.output_green}")
            # 自动展示 Top 3 战神！
            SYSTEM_LOGGER.info("\n👑 [大盘简报] 斩获黄金池 Top 3 超级战神：")

            # 确保 DataFrame 不为空且包含 Talent_Alpha 列
            if not self.df_green.empty and 'Talent_Alpha' in self.df_green.columns:
                # 按Final Talent Valuation (最终人才估值)从高到低排序，取前 3 名
                top3 = self.df_green.sort_values(by='Talent_Alpha', ascending=False).head(3)

                for index, row in top3.iterrows():
                    email = row.get('email', 'Unknown_Geek')
                    score = row.get('Talent_Alpha', 0.0)
                    # 兼容 V7.1 的新字段
                    claim = row.get('Claim-to-Evidence Ratio (主张实证倒挂率)', 'Unknown')
                
                    print(f"  => 🏅 {email} | 综合分: {score:.1f} | 杠杆率: {claim}")
            else:
                print("  => 🈳 当前阈值下，黄金池无人幸存。")
            

        if not self.df_yellow.empty:
            self.df_yellow.to_csv(self.output_yellow, index=False, encoding='utf-8-sig')
            SYSTEM_LOGGER.info(f"✅ Secondary Verification Pool (黄池)已落锁: {self.output_yellow}")
            
        if not self.df_red.empty:
            cols_to_keep = [c for c in self.df_red.columns if c not in ['Tech_Score', 'Project_Score', 'Potential_Score', 'Talent_Alpha']]
            self.df_red[cols_to_keep].to_csv(self.output_red, index=False, encoding='utf-8-sig')
            SYSTEM_LOGGER.info(f"☠️ Intercepted & Archived Roster (拦截封存库): {self.output_red}")
