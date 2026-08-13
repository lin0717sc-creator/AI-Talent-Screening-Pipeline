import pandas as pd
import re
from config import settings

class StabilityScoringEngine:
    """
    Phase 1: 稳定性风控与红黄牌大闸 (V4.0 扣分制)
    目标：防守下限。基于时间轴与风险探针，执行连续扣分，并导出三库分流标签。
    """
    
    @staticmethod
    def evaluate_stability(row):
        """
        单行核心扣分算子，返回 [Stability_Score, triage_flag, is_high_risk, audit_log]
        """
        # 1. 提取 Phase 0 (etl_cleaner) 传递过来的干净数据
        text = str(row.get('normalized_text', '')).lower()
        exp_years = float(row.get('total_experience_years', 3.0))
        max_tenure = float(row.get('max_tenure_months', 12.0))
        gap_months = float(row.get('max_gap_months', 0.0))

        # 开局默认满分 (保健因素，证明你不违规即可)
        score = 100.0
        logs = []
        
        # 2. 触发风控特征探针
        has_gig = bool(re.search(settings.GIG_WORDS, text))
        has_founder = bool(re.search(settings.FOUNDER_WORDS, text))
        has_layoff = bool(re.search(settings.LAYOFF_WORDS, text))
        
        thresh = settings.STABILITY_THRESHOLDS
        
        # ==========================================
        # 🛡️ 绝对豁免层：应届生/首职试错期
        # ==========================================
        if exp_years <= thresh.get('fresh_grad_max_exp', 2.0):
            return pd.Series([100.0, 'GREEN', False, '[✅ 放行] 经验≤2年，触发探索期绝对豁免'])
            
        # ==========================================
        # 📉 连续扣分与动态加分层
        # ==========================================
        
        # A. 极度不稳定扣分 (核心绞杀逻辑)
        if max_tenure < thresh.get('mercenary_max_tenure', 12):
            if has_layoff:
                score -= 40  # 宏观受灾，扣分较轻 (剩余60分)
                logs.append("最长单段<12个月，但具备宏观裁员特征 (-40分)")
            else:
                score -= 80  # 纯血跳槽，无情绞杀 (剩余20分)
                logs.append("无一年以上存活证明，且无裁员/创业特征 (-80分)")
        elif max_tenure >= thresh.get('anchor_tenure', 60):
            score += 10      # 定海神针补偿
            logs.append("拥有5年以上定海神针经历 (+10分)")
            
        # B. 危险空窗期 (Gap) 扣分
        if gap_months > thresh.get('dangerous_gap', 6):
            # 超出危险期的部分，每 3 个月扣 10 分
            extra_gap = gap_months - thresh['dangerous_gap']
            penalty = max(10, (extra_gap // 3) * 10) 
            score -= penalty
            logs.append(f"检测到 {gap_months} 个月危险空窗期 (-{penalty}分)")
            
        # C. 特殊用工属性 (外包/创业) 强制封顶
        if has_gig or has_founder:
            reason = "创业者" if has_founder else "独立顾问/外包"
            if score > 65:
                score = 65
                logs.append(f"特殊属性({reason})触发分数封顶 65 分")
                
        # 确保分数被锁定在 0 ~ 100 的合法区间
        score = max(0.0, min(100.0, score))
        
        # ==========================================
        # ⚖️ 定级、落标签与熔断诊断 (依据分数区间)
        # ==========================================
        if score >= 80:
            flag = 'GREEN'
            is_risk = False
            audit = "[✅ 黄金大盘] 稳定性健康" if not logs else f"[✅ 黄金大盘] {'; '.join(logs)}"
        elif score >= 30:
            flag = 'YELLOW'
            is_risk = True  # 触发高风险警报，供前端或 HR 系统标红
            audit = f"[⚠️ 风险截留] {'; '.join(logs)}"
        else:
            flag = 'RED'
            is_risk = True
            audit = f"[❌ 致命一票否决] 跌破30分红线: {'; '.join(logs)}"
            
        return pd.Series([score, flag, is_risk, audit])

    @staticmethod
    def process_dataframe(df):
        """
        批量接管数据流，执行打分并生成分流统计
        """
        print("\n[STAGE 1] 启动 V4.0 稳定性风控大闸 (扣分制红线引擎)...")
        
        # 极速向量化运算：对全盘数据应用扣分算子
        results = df.apply(StabilityScoringEngine.evaluate_stability, axis=1)
        results.columns = ['Stability_Score', 'triage_flag', 'is_high_risk', 'stability_audit_log']
        
        # 拼装回主干数据流
        df = pd.concat([df, results], axis=1)
        
        # 打印审计遥测报告
        green_count = (df['triage_flag'] == 'GREEN').sum()
        yellow_count = (df['triage_flag'] == 'YELLOW').sum()
        red_count = (df['triage_flag'] == 'RED').sum()
        
        print(f"📊 稳定性风控探针扫描完毕：")
        print(f"  => 🟢 黄金无风险 (80-100分): {green_count} 份")
        print(f"  => 🟡 高危但带病晋级 (30-79分): {yellow_count} 份")
        print(f"  => 🔴 纯血雇佣兵熔断绞杀 (0-29分): {red_count} 份 (一票否决，不分配后续算力)")
        
        return df