import pandas as pd
from config.settings import (
    TECH_FOUNDATION_POOL, COMPLIANCE_CONCEPT_POOL, TECH_SKILL_WEIGHTS,
    PROJECT_BENEFIT_POOL, PROJECT_DELIVERY_POOL, PROJECT_OUTPUT_WEIGHTS,
    BONUS_TECH_DELIVERY, BONUS_AI_INFRA, BONUS_FINOPS, BONUS_APAC_STRATEGY,
    GLOBAL_WEIGHT_TECH, GLOBAL_WEIGHT_PROJECT, TECH_SCORE_CAP, PROJECT_SCORE_CAP
)

class BusinessScoringEngine:
    """
    大厂级规则打分引擎：彻底合并硬核技术与自研项目双通路，全面填充1+1>2跨界红利。
    实装 V1.5 潜力对冲与风控熔断机制。
    """
    
    @classmethod
    def _calculate_raw_tech_score(cls, extracted_skills) -> float:
        """原子算子一：技术硬实力原始分核算（注入小写容错去重池）"""
        if not isinstance(extracted_skills, (list, set, zip)):
            if isinstance(extracted_skills, str):
                extracted_skills = extracted_skills.split(',')
            else:
                return 0.0
                
        skills_set = set([str(s).lower().strip() for s in extracted_skills])
        
        # 1. 弹性准入网双轨拦截
        if not skills_set.intersection(TECH_FOUNDATION_POOL):
            return 0.0
        if not skills_set.intersection(COMPLIANCE_CONCEPT_POOL):
            return 0.0
            
        # 2. 特征身价静态撞击累加
        raw_score = sum(TECH_SKILL_WEIGHTS.get(skill, 0) for skill in skills_set)
        
        # 3. 动态红利对账
        if BONUS_TECH_DELIVERY['trigger_skill'] in skills_set and skills_set.intersection(BONUS_TECH_DELIVERY['performance_tags']):
            raw_score += BONUS_TECH_DELIVERY['points']
            
        if skills_set.intersection(BONUS_AI_INFRA['ai_skills']) and skills_set.intersection(BONUS_AI_INFRA['cloud_tags']):
            raw_score += BONUS_AI_INFRA['points']
            
        return float(min(raw_score, TECH_SCORE_CAP))

    @classmethod
    def _calculate_raw_project_score(cls, extracted_project_tags) -> float:
        """原子算子二：项目产出硬实力原始分核算（注入跨界复合重构红利）"""
        if not isinstance(extracted_project_tags, (list, set, zip)):
            if isinstance(extracted_project_tags, str):
                extracted_project_tags = extracted_project_tags.split(',')
            else:
                return 0.0
                
        project_set = set([str(p).lower().strip() for p in extracted_project_tags])
        
        # 1. 弹性双轨准入网拦截
        if not project_set.intersection(PROJECT_BENEFIT_POOL):
            return 0.0
        if not project_set.intersection(PROJECT_DELIVERY_POOL):
            return 0.0
            
        # 2. 特征身价静态累加
        raw_score = sum(PROJECT_OUTPUT_WEIGHTS.get(tag, 0) for tag in project_set)
        
        # 3. 动态红利对账
        if project_set.intersection(BONUS_FINOPS['scale_tags']) and project_set.intersection(BONUS_FINOPS['finance_tags']):
            raw_score += BONUS_FINOPS['points']
            
        if project_set.intersection(BONUS_APAC_STRATEGY['pipeline_tags']) and project_set.intersection(BONUS_APAC_STRATEGY['strategy_tags']):
            raw_score += BONUS_APAC_STRATEGY['points']
            
        return float(min(raw_score, PROJECT_SCORE_CAP))

    # 🚀 第 19 天新增：潜力原子算子
    @classmethod
    def _calculate_potential_score(cls, row) -> float:
        """
        原子算子三：潜力对冲分核算（横向扫描：学历基线 + 商业词频 + 极客风控）
        """
        # 提取学历、技能与项目标签
        edu_str = str(row.get('education', '')).lower().strip()
        skills_str = str(row.get('standard_skills', ''))
        project_str = str(row.get('project_tags', ''))
        
        skills_set = set([s.strip() for s in skills_str.split(',') if s.strip()])
        project_set = set([p.strip() for p in project_str.split(',') if p.strip()])
        
        # 1. 学历对冲基线
        if 'master' in edu_str or 'phd' in edu_str:
            pot_score = 60.0
        elif 'bachelor' in edu_str:
            pot_score = 40.0
        else:
            pot_score = 20.0
            
        # 2. 商业决策词频叠加 (每个高潜词 +10)
        pot_score += len(project_set) * 10.0
        
        # 3. 架构师风控防线：惩罚“A型危险极客”
        # 如果项目重构词 >= 2，但技能池里没有任何合规心智，直接腰斩！
        has_compliance = bool(skills_set.intersection(COMPLIANCE_CONCEPT_POOL))
        if len(project_set) >= 2 and not has_compliance:
            pot_score = pot_score * 0.5
            
        return float(min(pot_score, 100.0))

    @classmethod
    def evaluate_pipeline_scores(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        总控打分矩阵：三舱协同齐发 ➔ 级联交叉熔断 ➔ 多维身价出货 ➔ 白盒化审计
        """
        df['raw_tech_score'] = df['standard_skills'].apply(cls._calculate_raw_tech_score)
        df['raw_project_score'] = df['project_tags'].apply(cls._calculate_raw_project_score)
        df['potential_score'] = df.apply(cls._calculate_potential_score, axis=1) 
        
        final_scores = []
        audit_logs = []  # 🚀 新增：验尸报告池
        
        for idx in range(len(df)):
            t_score = df['raw_tech_score'].iloc[idx]
            p_score = df['raw_project_score'].iloc[idx]
            pot_score = df['potential_score'].iloc[idx]
            
            # 读取特征用于写诊断报告
            skills = str(df['standard_skills'].iloc[idx])
            has_compliance = bool(set(skills.split(', ')).intersection({'pdpa', 'security', 'audit', 'compliance', 'privacy', 'mom'}))
            has_tech = bool(set(skills.split(', ')).intersection({'python', 'sql', 'tableau', 'machine_learning', 'cloud_computing'}))
            
            log = "✅ [Qualified] 资产合格"
            final_score = (t_score * 0.4) + (p_score * 0.4) + (pot_score * 0.2)
            
            # 🚀 白盒化审计：精确指出死因
            if t_score == 0.0:
                if not has_compliance and not has_tech:
                    log = "❌ [Fatal] 乱码或纯白板：无技术无合规"
                elif not has_compliance:
                    log = "❌ [Fatal] 偏科码农：缺乏 PDPA/Security 等合规心智"
                elif not has_tech:
                    log = "❌ [Fatal] 偏科法务：缺乏硬核技术底座"
                final_score = 0.0
                
            elif p_score == 0.0:
                log = "❌ [Fatal] 理论派：缺乏 ROI/降本增效 等商业落地产出"
                final_score = 0.0
                
            elif pot_score < 30.0:
                if not has_compliance:
                    log = "❌ [Fatal] A型危险极客：创新极强但无视合规，存在安全隐患"
                else:
                    log = "❌ [Fatal] 潜力过低：缺乏基础商业视野"
                final_score = 0.0
                
            final_scores.append(round(final_score, 2))
            audit_logs.append(log)
            
        df['final_market_score'] = final_scores
        df['audit_log'] = audit_logs  # 挂载验尸报告
        
        return df