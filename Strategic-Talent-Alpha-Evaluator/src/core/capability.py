import pandas as pd
import re
from config import settings

class CapabilityScoringEngine:
    """
    Phase 2 & 3: 核心能力加分与双底线熔断算子 (V4.0 长板互补引擎)
    目标：计算技术与项目得分，执行双底线熔断，并叠加 PoW 主权溢价与潜力红利。
    """

    @staticmethod
    def evaluate_capability(row):
        """
        单行核心加分算子，返回 [Tech, Project, Potential, Total_Score, flag, risk, audit_log]
        """
        # 1. 🛡️ 算力保护闸：如果上一层的稳定性大闸已经判了死刑 (RED)，直接跳过，零算力消耗！
        current_flag = row.get('triage_flag', 'RED')
        is_risk = row.get('is_high_risk', True)
        audit_log = str(row.get('stability_audit_log', ''))

        if current_flag == 'RED':
            return pd.Series([0.0, 0.0, 0.0, 0.0, current_flag, is_risk, audit_log])

        # 提取数据与探针状态
        text = str(row.get('normalized_text', ''))
        has_pow = row.get('Has_PoW', False)

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

        # 依据计分板计算基础分 (无上限，凭实力垒高)
        tech_score = sum(settings.TECH_SKILL_WEIGHTS.get(skill, 0) for skill in found_tech_skills)
        project_score = sum(settings.PROJECT_OUTPUT_WEIGHTS.get(tag, 0) for tag in found_project_tags)

        # ==========================================
        # ❌ 步骤二：双底线物理熔断 (Anti-PPT 战神)
        # ==========================================
        if tech_score == 0 or project_score == 0:
            death_reason = "纯商业忽悠(技术分为0)" if tech_score == 0 else "纯底层码农(无商业产出思维)"
            new_audit = f"{audit_log} | [❌ 致命底线熔断] {death_reason}"
            # 强制改判红牌，打入坟墓池
            return pd.Series([tech_score, project_score, 0.0, 0.0, 'RED', True, new_audit])

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
        base_total = tech_score + project_score + potential_score

        # ==========================================
        # 🚀 步骤四：代码主权锚点加权 (Proof of Work)
        # ==========================================
        if has_pow:
            final_total = base_total * 1.2  # 携带 GitHub/Kaggle，总资产溢价 20%
            audit_log += " | [💎 PoW 认证] 携带开源数字资产(身价*1.2)"
        else:
            final_total = base_total

        return pd.Series([tech_score, project_score, potential_score, final_total, current_flag, is_risk, audit_log])

    @staticmethod
    def process_dataframe(df):
        """
        接管数据流，执行价值评估，过滤淘汰者
        """
        print("\n[STAGE 2] 启动 V4.0 能力与项目大闸 (加分与双底线熔断引擎)...")
        
        # 极速向量化运算：全盘扫描
        results = df.apply(CapabilityScoringEngine.evaluate_capability, axis=1)
        results.columns = ['Tech_Score', 'Project_Score', 'Potential_Score', 'Raw_Total_Score', 'triage_flag', 'is_high_risk', 'final_audit_log']
        
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