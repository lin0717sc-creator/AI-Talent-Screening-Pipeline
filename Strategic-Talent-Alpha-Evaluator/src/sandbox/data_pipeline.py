import os
import pandas as pd

def init_data_pipeline(file_path):
    """
    【第11天下午任务：数据维度与噪声漏洞审查】
    作用：强行读取数据，并全量扫描噪声漏洞（剔除所有控制台不兼容特殊符号）。
    """
    print("[STATUS] Starting Second Campaign: Day 11 Afternoon Pipeline...")
    
    if not os.path.exists(file_path):
        print(f"[CRITICAL ERROR] Cannot find data source file at: {file_path}")
        return None
        
    encodings = ['utf-8', 'gbk', 'utf-8-sig', 'latin1']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding, dtype=str)
            print(f"[SUCCESS] Connection complete! Employed encoding: [{encoding}]")
            break
        except UnicodeDecodeError:
            continue

    if df is None:
        print("[CRITICAL] All external encoding layers breached.")
        return None

    # =========================================================================
    # ⚡ 下午核心战术动作：噪声漏洞全面审查
    # =========================================================================
    print("\n" + "===" * 15)
    print(" AUDIT: Running comprehensive noise and vulnerability scanning...")
    print("===" * 15 + "\n")

    # 动作一：提取基本骨架信息
    print("--- Dimension 1: Data Dictionary & Data Type Audit (df.info) ---")
    # info() 会打印出每一列的真实数据类型，以及有多少是非空的
    df.info()
    print("-" * 50 + "\n")

    # 动作二：精确计算每一列的“漏填空值（NaN）”数量
    print("--- Dimension 2: Missing Value Absolute Count Statistics (df.isnull().sum()) ---")
    # isnull().sum() 是我们用来抓捕缺失噪声的工业长枪
    missing_data = df.isnull().sum()
    print(missing_data)
    print("-" * 50 + "\n")

    # 动作三：商科视角的噪声研判报告
    print("💡 STRATEGIC ANALYSIS REPORT:")
    for column in df.columns:
        missing_count = df[column].isnull().sum()
        if missing_count > 0:
            print(f"  [ALERT] Column [{column}] has {missing_count} missing values! Action required in next stage.")
        else:
            print(f"  [LOCKED] Column [{column}] is 100% solid. No missing noise.")
    print("=" * 50 + "\n")
    
    return df

if __name__ == "__main__":
    RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/raw_resumes.csv")
    raw_dataframe = init_data_pipeline(RAW_DATA_PATH)
    