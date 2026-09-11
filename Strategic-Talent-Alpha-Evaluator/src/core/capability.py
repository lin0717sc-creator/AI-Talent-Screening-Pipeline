import pandas as pd
import re
import json  # 💡 新增：用于将字典转化为结构化 JSON 证据
from config import settings

class CapabilityScoringEngine:
    """
    Phase 2 & 3: 核心能力加分与双底线熔断算子 (V6.0 证据层架构版)
    目标：计算技术与项目得分，抽取密度先验信号，输出置信度与证据图谱。
    """

    @staticmethod
    def evaluate_capability(row):
        """
        单行核心加分算子，返回 10 维战力向量：
        [Tech, Project, Potential, Total, flag, risk, audit_log, Density, Confidence, Evidence]
        """
        # 1. 🛡️ 算力保护闸：如果上一层的稳定性大闸已经判了死刑 (RED)，直接跳过，零算力消耗！
        current_flag = row.get('triage_flag', 'RED')
        is_risk = row.get('is_high_risk', True)
        audit_log = str(row.get('stability_audit_log', ''))

        if current_flag == 'RED':
            # 补齐 10 个字段，防止 Pandas 拼接报错
            return pd.Series([0.0, 0.0, 0.0, 0.0, current_flag, is_risk, audit_log, 'Low', 0.0, "{}"])
        
        # 提取数据与探针状态
        text = str(row.get('normalized_text', ''))
        
        # 🚨 [架构师特权]：临时强制全员拥有开源资产，为了测试大模型！
        # has_pow = row.get('Has_PoW', False)  <-- 把原来这行注释掉
        has_pow = True

        # ==========================================
        # 📈 步骤一：特征降维与加分提取
        # ==========================================
        found_tech_skills = set()
        for raw_word, std_word in settings.SKILL_MAPPING.items():
            if re.search(r'\b' + re.escape(raw_word) + r'\b', text):
                found_tech_skills.add(std_word)

        found_project_tags = set()
        for raw_word, std_word in settings.PROJECT_MAPPING.items():
            if re.search(r'\b' + re.escape(raw_word) + r'\b', text):
                found_project_tags.add(std_word)

        # 🚀 降维打击外挂 1：抽取信息密度作为先验路由信号 (Prior Signal)
        total_keywords = len(found_tech_skills) + len(found_project_tags)
        resume_density = 'High' if total_keywords >= 15 else ('Low' if total_keywords <= 5 else 'Medium')

        # ==========================================
        # 💼 架构师级更新：Evidence Engine & Confidence (证据引擎与置信度)
        # ==========================================
       
        # 1. 初始化结构化证据字典 (强制按字母排序，防止缓存击穿！)
        evidence_graph = {
            "tech_hits": sorted(list(found_tech_skills)),
            "project_hits": sorted(list(found_project_tags)),
            "risk_flags": [],
            "compliance_note": ""
        }
        
        # 2. 置信度校准 (Confidence Calibration)
        confidence_score = 0.90  # 默认高置信度
        if resume_density == 'Low':
            confidence_score = 0.30  # 字太少，模型把握极低，需要人工介入
        elif resume_density == 'Medium':
            confidence_score = 0.60


        # ==========================================
        # 🛡️ AI Governance Interceptor (企业合规拦截器)
        # ==========================================
        active_profile_config = settings.TALENT_WEIGHT_PROFILES.get(settings.ACTIVE_PROFILE, {})
        strict_density_filter = active_profile_config.get("strict_density_filter", True)
        
        # 定义什么是高阶稀有技能（用于触发“扫地僧”保护）
        rare_skills_pool = {'llm', 'vectorization', 'agentic_workflow', 'chunking', 'parquet'}
        has_rare_skill = any(skill in found_tech_skills for skill in rare_skills_pool)
        
        reject_reasons = []
        
        # 1. 收集缺陷证据 (不再直接处决)
        if strict_density_filter and resume_density == 'Low':
            reject_reasons.append("LOW_DENSITY")
            evidence_graph["risk_flags"].append("LOW_DENSITY") # 写入图谱
        if not has_pow:
            reject_reasons.append("NO_POW")
            evidence_graph["risk_flags"].append("NO_POW")      # 写入图谱
            
        # 2. 合规审判庭
        if len(reject_reasons) > 0:
            if reject_reasons == ["NO_POW"]:
                current_flag = "YELLOW" # ⚠️ 强行扭转为人工池
                audit_log += " | ⚠️ [合规保护] 仅缺开源资产，防 Proxy Bias，移交 HR"
                evidence_graph["compliance_note"] = "触发防 Proxy Bias 保护"
                
            elif "LOW_DENSITY" in reject_reasons and has_rare_skill:
                current_flag = "YELLOW" # ⚠️ 强行扭转为人工池
                audit_log += " | ⚠️ [合规保护] 简历极短但含高阶特征(疑似扫地僧)，移交 HR"
                evidence_graph["compliance_note"] = "触发扫地僧熔断保护"
                
            else:
                # 3. 只有证据确凿（没字数且没资产），才批准处决
                death_reason = "多维特征全面溃败(无密度+无资产)"
                new_audit = f"{audit_log} | [❌ 合规审计通过] {death_reason}"
                evidence_graph["compliance_note"] = "合法自动化淘汰"
                # 处决时也要带上字典！
                return pd.Series([0.0, 0.0, 0.0, 0.0, 'RED', True, new_audit, resume_density, confidence_score, json.dumps(evidence_graph, ensure_ascii=False)])

        # ==========================================
        # ⚖️ 步骤二：单底线熔断与灰度放行 (老代码无损保留)
        # ==========================================   
        tech_weights = sorted([settings.TECH_SKILL_WEIGHTS.get(skill, 0) for skill in found_tech_skills], reverse=True)
        project_weights = sorted([settings.PROJECT_OUTPUT_WEIGHTS.get(tag, 0) for tag in found_project_tags], reverse=True)
        
        tech_score = sum(tech_weights[:5])
        project_score = sum(project_weights[:5])

        # 1. 对“PPT战神”保持零容忍 (完全没有技术词汇的，直接击毙)
        if tech_score == 0:
            death_reason = "纯商业忽悠(技术分为0)"
            new_audit = f"{audit_log} | [❌ 致命底线熔断] {death_reason}"
            evidence_graph["risk_flags"].append("ZERO_TECH_SCORE")
            return pd.Series([tech_score, project_score, 0.0, 0.0, 'RED', True, new_audit, resume_density, confidence_score, json.dumps(evidence_graph, ensure_ascii=False)])

        # 2. 对“偏科老实人”网开一面，交还生杀大权给 LLM 或人类 HR
        if project_score == 0:
            # 仅仅是追加一句警告，但不改判 RED，允许存活到下一关！
            audit_log += " | [⚠️ 偏科警告] 未检测到商业产出词汇，交由大模型或HR定夺"
            evidence_graph["risk_flags"].append("ZERO_PROJECT_SCORE")

        # ==========================================
        # 🌟 步骤三：跨界红利与潜力加分计算
        # ==========================================
        potential_score = 0.0
        
        # 激活 MGT567 混合红利 (基于你 settings 里的组合拳配置)
        if hasattr(settings, 'BONUS_AI_INFRA'):
            ai_infra = settings.BONUS_AI_INFRA
            if any(s in found_tech_skills for s in ai_infra.get('ai_skills', [])) and \
               any(t in found_tech_skills for t in ai_infra.get('cloud_tags', [])):
                potential_score += ai_infra.get('points', 15.0)
                
        if hasattr(settings, 'BONUS_FINOPS'):
            finops = settings.BONUS_FINOPS
            if any(s in found_project_tags for s in finops.get('scale_tags', [])) and \
               any(t in found_project_tags for t in finops.get('finance_tags', [])):
                potential_score += finops.get('points', 15.0)

        # 基础长板合成
        final_total = tech_score + project_score + potential_score

        # 🚀 降维打击外挂 3：彻底废除此处的 1.2 倍静态开关。
        # 真正的动态 PoW 开源信号测算，已移交至 pipeline.py 的 _calculate_and_validate 统一处理！
        if has_pow:
            audit_log += " | [💎 PoW 认证] 发现开源资产信号 (移交管线动态测算)"
            evidence_graph["compliance_note"] = "持有顶级开源资产"
        # 🚨 注意：返回值多了一个 resume_density
        
        # 🚀 将最终的 evidence_graph 转化为 JSON 字符串传给下游
        final_evidence = json.dumps(evidence_graph, ensure_ascii=False)

        # 🚨 返回 10 个维度的完整数据流！
        return pd.Series([tech_score, project_score, potential_score, final_total, current_flag, is_risk, audit_log, resume_density, confidence_score, final_evidence])


    @staticmethod
    def process_dataframe(df):
        """
        接管数据流，执行价值评估，过滤淘汰者
        """
        print("\n[STAGE 2] 启动 V6.0 能力防刷分大闸 (Top 5 战力核算)...")
        
        # 极速向量化运算：全盘扫描
        results = df.apply(CapabilityScoringEngine.evaluate_capability, axis=1)

        # 🚨 极度重要：映射全新的 10 个数据列！
        results.columns = [
            'Tech_Score', 'Project_Score', 'Potential_Score', 'Raw_Total_Score', 
            'triage_flag', 'is_high_risk', 'final_audit_log', 'ResumeDensity',
            'Confidence_Score', 'Evidence_Graph'
        ]

        
        # 覆写主干数据状态
        for col in results.columns:
            df[col] = results[col]

        # 打印审计遥测报告 (仅统计在这一层被杀的人)
        survivors = df[df['triage_flag'] != 'RED']
        # 找出那些本来稳定性过关（>0），却因为偏科死在这一层的人
        bluffers = df[(df['triage_flag'] == 'RED') & (df['Tech_Score'] == 0) & (df['Stability_Score'] > 0)]
        nerds = df[(df['triage_flag'] == 'RED') & (df['Project_Score'] == 0) & (df['Stability_Score'] > 0)]

        print(f"📊 核心能力估值扫描完毕：")
        print(f"  => ⚔️ 击杀 PPT 战神 (技术底线熔断): {len(bluffers)} 份")
        print(f"  => ⚔️ 击杀 呆板码农 (商业底线熔断): {len(nerds)} 份")
        print(f"  => 🏆 成功穿越双底线幸存者: {len(survivors)} 份 (已赋予身价总分，准备进行业务权重变形)")
        
        return df