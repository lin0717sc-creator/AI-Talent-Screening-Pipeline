import pandas as pd
import numpy as np
import os
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

# 1. 配置路径 (请确保与你的实际路径对齐)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PREDICTED_SCORE_FILE = os.path.join(BASE_DIR, "data", "03_processed", "cleaned_v1_master.csv")
GROUND_TRUTH_FILE = os.path.join(BASE_DIR, "data", "historical_labels.csv")

def run_evaluation():
    print("\n[EVAL STAGE] 启动 V6.0 模型效度回测引擎 (Backtesting)...")
    
    # 2. 读取数据
    try:
        df_pred = pd.read_csv(PREDICTED_SCORE_FILE)
        df_truth = pd.read_csv(GROUND_TRUTH_FILE)
    except FileNotFoundError as e:
        print(f"❌ 找不到文件，请检查路径: {e}")
        return

    # 3. 数据并网 (以 email 为主键，将预测分和真实结局拼在一起)
    # 假设你的最终总分列名叫 'Talent_Alpha'，如果不是，请修改下方列名！
    SCORE_COLUMN = 'Talent_Alpha' 
    if SCORE_COLUMN not in df_pred.columns:
        print(f"⚠️ 警告: 预测结果中没有找到 '{SCORE_COLUMN}' 列，请修改代码中的列名。")
        return
        
    # 架构师级更新：使用 left join，保留所有历史候选人
    # 如果系统把他们枪毙了（不在 master 表里），就把他们的分数强行记为 0！
    df_merged = pd.merge(df_truth, df_pred[['email', SCORE_COLUMN]], on='email', how='left')
    df_merged[SCORE_COLUMN] = df_merged[SCORE_COLUMN].fillna(0)
    
    if len(df_merged) < 2:
        print("❌ 样本量过少，无法计算统计学指标，请确保有足够的对齐数据。")
        return
        
    print(f"✅ 成功匹配到 {len(df_merged)} 条历史回测数据。")

    # 4. 提取对撞变量
    y_true = df_merged['Offer_Status'].astype(int)
    y_scores = df_merged[SCORE_COLUMN].astype(float)
    
    # 设定一个阈值（比如总分大于 30 分，系统就建议发 Offer）
    threshold = 30.0 
    y_pred = (y_scores >= threshold).astype(int)

    # 5. 核心计算：硬核统计学指标
    print("\n" + "="*50)
    print("📊 [模型效度检验报告 - Calibration Metrics]")
    print("="*50)
    
    try:
        # 计算 AUC (Area Under Curve) - 衡量模型将正样本排在负样本前面的综合能力
        auc = roc_auc_score(y_true, y_scores)
        print(f"🏆 模型综合排序能力 (AUC): {auc:.4f}  <-- (越接近 1 越牛，0.5等于瞎猜)")
        
        # 计算 Precision, Recall, F1
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        
        print(f"🎯 查准率 ($Precision$):   {precision:.4f}  (系统推荐的人，有多少真的拿了Offer)")
        print(f"🔍 查全率 ($Recall$):      {recall:.4f}  (真实拿Offer的人，有多少被系统找出来了)")
        print(f"⚖️  F1-Score ($F1$):       {f1:.4f}  (两者的调和平均数)")
        print("-" * 50)
        print("详细分类报告:")
        print(classification_report(y_true, y_pred, target_names=['淘汰 (0)', '录取 (1)'], zero_division=0))
        print("混淆矩阵:")
        print(confusion_matrix(y_true, y_pred, labels=[0, 1]))

        # ==========================================
        # 💼 架构师级更新：商业错误成本矩阵 (Cost Matrix)
        # ==========================================
        # 1. 提取混淆矩阵的核心变量
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
        
        # 2. 情景 A：常规骨干岗 (防骗子模式) -> 极度厌恶 FP (错放水货)
        cost_fp_core = 10000  # 招错一个水货，公司损失 10000 美金
        cost_fn_core = 2000   # 错过一个普通人，重新发个JD只要 2000 美金
        cost_core = (fp * cost_fp_core) + (fn * cost_fn_core)
        
        # 3. 情景 B：AI 架构师 / 先锋岗 (淘金模式) -> 极度厌恶 FN (错杀大牛)
        cost_fp_pioneer = 1000   # 面试官浪费一小时，损失 1000 美金
        cost_fn_pioneer = 50000  # 错过一个天才架构师，战略受损 50000 美金
        cost_pioneer = (fp * cost_fp_pioneer) + (fn * cost_fn_pioneer)

        # 4. 打印财务账单
        print("\n" + "-" * 50)
        print("💰 [商业财务对赌 - Expected Cost Analysis]")
        print("-" * 50)
        print(f"当前大闸防线状态 -> 漏放水货 (FP): {fp} 人 | 错杀大牛 (FN): {fn} 人")
        print(f"📉 若应用于【常规骨干岗】预估业务损失: ${cost_core:,}")
        print(f"📉 若应用于【核心先锋岗】预估业务损失: ${cost_pioneer:,}")

    except Exception as e:
        print(f"❌ 计算指标时出错: {e}")

if __name__ == "__main__":
    run_evaluation()
