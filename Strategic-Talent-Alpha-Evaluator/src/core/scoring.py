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
    """
    
    @classmethod
    def _calculate_raw_tech_score(cls, extracted_skills) -> float:
        """
        原子算子一：技术硬实力原始分核算（注入小写容错去重池）
        """
        if not isinstance(extracted_skills, (list, set, zip)):
            if isinstance(extracted_skills, str):
                extracted_skills = extracted_skills.split(',')
            else:
                return 0.0
                
        # 将简历提取词进行格式平铺压扁
        skills_set = set([str(s).lower().strip() for s in extracted_skills])
        
        # 1. 弹性准入网双轨拦截（技术工具和合规心智缺一不可）
        if not skills_set.intersection(TECH_FOUNDATION_POOL):
            return 0.0
        if not skills_set.intersection(COMPLIANCE_CONCEPT_POOL):
            return 0.0
            
        # 2. 特征身价静态撞击累加
        raw_score = sum(TECH_SKILL_WEIGHTS.get(skill, 0) for skill in skills_set)
        
        # 3. 🦾 动态对账：配置驱动的【1+1 > 2】技术多维组合拳红利
        # 组合拳红利 A：工业级全栈交付红利 (GitHub铁证 + 算力压榨)
        if BONUS_TECH_DELIVERY['trigger_skill'] in skills_set and skills_set.intersection(BONUS_TECH_DELIVERY['performance_tags']):
            raw_score += BONUS_TECH_DELIVERY['points']
            
        # 组合拳红利 B：AI新基建生产力红利 (AI核心技能 + 云端部署交付)
        if skills_set.intersection(BONUS_AI_INFRA['ai_skills']) and skills_set.intersection(BONUS_AI_INFRA['cloud_tags']):
            raw_score += BONUS_AI_INFRA['points']
            
        return float(min(raw_score, TECH_SCORE_CAP))

    @classmethod
    def _calculate_raw_project_score(cls, extracted_project_tags) -> float:
        """
        原子算子二：项目产出硬实力原始分核算（注入跨界复合重构红利）
        """
        if not isinstance(extracted_project_tags, (list, set, zip)):
            if isinstance(extracted_project_tags, str):
                extracted_project_tags = extracted_project_tags.split(',')
            else:
                return 0.0
                
        project_set = set([str(p).lower().strip() for p in extracted_project_tags])
        
        # 1. 弹性双轨准入网拦截（效益与交付双轨并存）
        if not project_set.intersection(PROJECT_BENEFIT_POOL):
            return 0.0
        if not project_set.intersection(PROJECT_DELIVERY_POOL):
            return 0.0
            
        # 2. 特征身价静态累加
        raw_score = sum(PROJECT_OUTPUT_WEIGHTS.get(tag, 0) for tag in project_set)
        
        # 3. 🦾 动态对账：配置驱动的【1+1 > 2】跨界项目红利
        # 组合拳红利 C：FinOps算力财务重构红利（海量吞吐 + 降本增效指标）
        if project_set.intersection(BONUS_FINOPS['scale_tags']) and project_set.intersection(BONUS_FINOPS['finance_tags']):
            raw_score += BONUS_FINOPS['points']
            
        # 组合拳红利 D：MGT567亚太战略交付红利（端到端智能管道 + 新加坡跨部门总部对齐）
        if project_set.intersection(BONUS_APAC_STRATEGY['pipeline_tags']) and project_set.intersection(BONUS_APAC_STRATEGY['strategy_tags']):
            raw_score += BONUS_APAC_STRATEGY['points']
            
        return float(min(raw_score, PROJECT_SCORE_CAP))

    @classmethod
    def evaluate_pipeline_scores(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        总控打分矩阵：双舱向量化齐发 ➔ 级联交叉熔断 ➔ 4:6身价出货
        """
        df['raw_tech_score'] = df['standard_skills'].apply(cls._calculate_raw_tech_score)
        df['raw_project_score'] = df['project_tags'].apply(cls._calculate_raw_project_score)
        
        # 4:6 黄金比例身价计算
        df['final_market_score'] = (df['raw_tech_score'] * GLOBAL_WEIGHT_TECH) + (df['raw_project_score'] * GLOBAL_WEIGHT_PROJECT)
        
        # 🔐 终极拦截线：单偏科混子全盘抹杀，总分归零
        df.loc[(df['raw_tech_score'] == 0.0) | (df['raw_project_score'] == 0.0), 'final_market_score'] = 0.0
        
        return df