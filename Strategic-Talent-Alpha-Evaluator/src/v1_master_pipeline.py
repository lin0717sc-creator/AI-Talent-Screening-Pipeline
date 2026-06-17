import os
import re
import pandas as pd

class MasterDataPipeline:
    """
    👑 【智能人才招聘筛选代码库 V1.0】
    📅 第 15 天：工业级面向对象 (OOP) 数据清洗总控台
    
    设计信条：
    1. 私有资产护城河：数据只在 self.df 中流转，外界绝对不可见。
    2. 节点级雷达监控：拒绝静默蒸发，每过一道安检门必须汇报战果。
    3. 动态跨平台通航：彻底抛弃硬编码路径，适应任何电脑与服务器。
    """
    def __init__(self, input_path, output_path):
        print("\n" + "🔥" * 20)
        print("[SYSTEM] V1.0 Industrial Data Pipeline Initializing...")
        print("🔥" * 20)
        self.input_path = input_path
        self.output_path = output_path
        self.df = None # 核心私有资产容器
        
        # 预加载正则引信
        self.tech_pattern = re.compile(r'python|tableau|data analytics|sql|machine learning|excel', re.IGNORECASE)

    def load_asset(self):
        """【三部曲之一：前端并网风控】"""
        print("\n--- 🛡️ 第一部：前端并网风控 ---")
        
        # 拦截暗坑三：温室路径死锁（文件不存在直接静默拦截，不爆红字）
        if not os.path.exists(self.input_path):
            print(f"[CRITICAL ERROR] Pipeline halted. Missing source asset: {self.input_path}")
            return False
            
        # 强控主权：全部以硬态 str 读入，防数据变形
        self.df = pd.read_csv(self.input_path, dtype=str)
        print(f"[TELEMETRY] Source asset loaded. Initial Raw Rows: {len(self.df)}")
        return True

    def _extract_skills(self, text_cell):
        """内部私有算子：正则标签提白"""
        if pd.isna(text_cell) or not isinstance(text_cell, str):
            return 'NO_SKILLS_TAG'
        matches = self.tech_pattern.findall(text_cell)
        if matches:
            tags = set([m.strip().title() for m in matches])
            return ", ".join(sorted(list(tags)))
        return 'NON_STANDARD_SKILLS'

    def execute_pipeline(self):
        """【三部曲之二：核心技术绞杀（四大神级商业规则全量整编）】"""
        print("\n--- ⚔️ 第二部：核心技术绞杀 ---")

        # 1. 僵尸熔断：无情枪毙没有 Email 的行 (主键依存)
        self.df = self.df.dropna(subset=['email'])
        print(f"[TELEMETRY] 僵尸熔断完毕 (Dropped missing emails). Current Rows: {len(self.df)}")

        # 2. 降维去重：林指挥官的“信息密度降维排序”神级补丁！
        self.df['valid_info_count'] = self.df.notna().sum(axis=1) # 算力核查
        self.df = self.df.sort_values(by=['email', 'valid_info_count'], ascending=[True, False]) # 优胜劣汰
        self.df = self.df.drop_duplicates(subset=['email'], keep='first') # 扣下扳机
        self.df = self.df.drop(columns=['valid_info_count']) # 掩痕交割
        print(f"[TELEMETRY] 降维去重完毕 (Info Density Sort). Current Rows: {len(self.df)}")

        # 3. 正则提白：抽取 standard_skills，抛弃脏数据
        if 'skills' in self.df.columns:
            self.df['standard_skills'] = self.df['skills'].apply(self._extract_skills)
            self.df = self.df.drop(columns=['skills'])
            print(f"[TELEMETRY] 正则提白完毕 (Regex Standardization applied).")

        # 4. 补丁抢救：拯救偏才资产
        fill_rules = {
            'phone': 'UNKNOWN_PHONE',
            'standard_skills': 'NO_SKILLS_TAG'
        }
        # 动态防崩：只填充存在的列
        safe_fill_rules = {k: v for k, v in fill_rules.items() if k in self.df.columns}
        self.df = self.df.fillna(safe_fill_rules)
        print(f"[TELEMETRY] 静态补丁抢救完毕 (Missing values imputed).")

    def export_deliverable(self):
        """【三部曲之三：后端落锁维护】"""
        print("\n--- 🔒 第三部：后端落锁维护 ---")
        
        # 终极主权拦截一：切除全空幽灵行
        self.df = self.df.dropna(how='all')
        
        # 终极主权拦截二：碾碎断层，重铺索引！防下游匹配错位！
        self.df = self.df.reset_index(drop=True)
        
        # 物理落盘
        self.df.to_csv(self.output_path, index=False, encoding='utf-8')
        
        print(f"[TELEMETRY] 物理落锁成功！最终高价值黄金资产: {len(self.df)} 行.")
        print(f"➡️ 终极交付路径: {self.output_path}")
        print("====================================================\n")

# =========================================================================
# 🚦 外部调用入口：只有这里可以控制战车启动
# =========================================================================
if __name__ == "__main__":
    # 动态相对路径机制：随处可跑，告别本地温室环境
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # 接入你在第 14 天做的高压测试源数据！
    INPUT_FILE = os.path.join(BASE_DIR, "../data/raw_resumes.csv")
    OUTPUT_FILE = os.path.join(BASE_DIR, "../data/cleaned_v1_master.csv")
    
    # 实例化流水线对象（提车）
    pipeline = MasterDataPipeline(INPUT_FILE, OUTPUT_FILE)
    
    # 流水线全自动点火防线
    if pipeline.load_asset():
        pipeline.execute_pipeline()
        pipeline.export_deliverable()
