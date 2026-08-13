import pandas as pd
import re
from config import settings

class ETLCleaner:
    """
    Phase 0: 数据并网与特征探针提取算子
    目标：降噪、清洗文本，提取关键主权资产 (PoW) 与时间轴，为后续引擎提供标准化数据。
    """
    def __init__(self):
        # 挂载 settings 中的绝对路径
        self.input_path = settings.STORAGE_REGISTRY['input_csv']
        self.df = None

    def load_and_deduplicate(self):
        """加载数据并执行【高密度信息去重法】"""
        print("\n[STAGE 0] 启动 ETL 数据清洗与探针扫描管线...")
        try:
            self.df = pd.read_csv(self.input_path, dtype=str)
            initial_count = len(self.df)
            
            # 1. 基础熔断：没有邮箱的直接剔除
            if 'email' in self.df.columns:
                self.df = self.df.dropna(subset=['email'])
            
            # 2. 🚀 核心继承：信息密度去重 (保留写得最丰满的简历)
            if settings.RESUME_COLUMN in self.df.columns and 'email' in self.df.columns:
                self.df['skill_length'] = self.df[settings.RESUME_COLUMN].astype(str).apply(len)
                self.df = self.df.sort_values('skill_length', ascending=False).drop_duplicates(subset=['email'], keep='first')
                self.df = self.df.drop(columns=['skill_length'])
                
            self.df = self.df.fillna('')
            print(f"✅ 数据加载与高密度去重完毕。原始: {initial_count}, 有效存活: {len(self.df)}")
        except Exception as e:
            print(f"❌ 数据加载失败，请检查文件路径: {e}")

    def extract_proof_of_work(self, text):
        """
        核心探针：扫描代码主权锚点 (Proof of Work)
        防 PPT 战神的第一道防线
        """
        text = str(text)
        for pattern in settings.POW_PATTERNS:
            if re.search(pattern, text):
                return True
        return False

    def clean_text_data(self):
        """文本极简降噪，提取 PoW 主权标记"""
        
        # ⚠️ 注意这里：_normalize 必须缩进在 clean_text_data 的内部
        def _normalize(row):
            raw_text = str(row.get(settings.RESUME_COLUMN, ''))
            clean_text = re.sub(r'\s+', ' ', raw_text.lower()).strip()
            return clean_text

        self.df['normalized_text'] = self.df.apply(_normalize, axis=1)
        
        # 执行 PoW 探针扫描，生成布尔值列
        self.df['Has_PoW'] = self.df['normalized_text'].apply(self.extract_proof_of_work)
        
        pow_count = self.df['Has_PoW'].sum()
        print(f"🔍 探针扫描完毕：共发现 {pow_count} 名携带数字资产 (GitHub/Kaggle 等) 的极客。")

    def format_timeline_fields(self):
        """
        【时间轴基建底座】
        为了让 Phase 1 的稳定性引擎正常工作，这里强制格式化时间字段。
        """
        if 'total_experience_years' not in self.df.columns:
            self.df['total_experience_years'] = 3.0
            
        if 'max_tenure_months' not in self.df.columns:
            self.df['max_tenure_months'] = 12
            
        if 'max_gap_months' not in self.df.columns:
            self.df['max_gap_months'] = 0
            
        # 强制转换为浮点型，防止后续数学计算报错
        self.df['total_experience_years'] = self.df['total_experience_years'].astype(float)
        self.df['max_tenure_months'] = self.df['max_tenure_months'].astype(float)
        self.df['max_gap_months'] = self.df['max_gap_months'].astype(float)

    def run_pipeline(self):
        """执行完整清洗管线，返回干净的 DataFrame 给下游"""
        self.load_and_deduplicate()
        if self.df is not None:
            self.clean_text_data()
            self.format_timeline_fields()
            print("[STAGE 0] 🟢 数据并网与探针提取完毕！数据流移交下一级...\n")
            return self.df
        return None
    