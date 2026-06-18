import os
import pandas as pd
from src.utils.helpers import extract_skills_tags

class MasterDataPipeline:
    """
    ⚔️ 工业级 OOP 数据清洗核心引擎
    拒绝静默蒸发，数据只在 self.df 内存中流转，过关必须强行打出雷达 Telemetry。
    """
    def __init__(self, input_path, output_path, tech_pattern, fill_rules):
        self.input_path = input_path
        self.output_path = output_path
        self.tech_pattern = tech_pattern
        self.fill_rules = fill_rules
        self.df = None

    def load_asset(self):
        print("\n--- 🛡️ [STAGE 1] 前端并网风控检查 ---")
        if not os.path.exists(self.input_path):
            print(f"[CRITICAL ERROR] 战车致盲。找不到源头资产: {self.input_path}")
            return False
        
        self.df = pd.read_csv(self.input_path, dtype=str)
        print(f"[TELEMETRY] 资产并网安全。初始 Raw 数据: {len(self.df)} 行.")
        return True

    def execute_pipeline(self):
        print("\n--- ⚔️ [STAGE 2] 核心技术模块化绞杀 ---")
        
        # 1. 僵尸熔断：枪毙没有主键 Email 的行
        self.df = self.df.dropna(subset=['email'])
        print(f"[TELEMETRY] 1. 僵尸熔断完毕. 剩余高价值资产: {len(self.df)} 行.")

        # 2. 降维去重：林指挥官的“信息密度排序去重”神级算法
        self.df['valid_info_count'] = self.df.notna().sum(axis=1)
        self.df = self.df.sort_values(by=['email', 'valid_info_count'], ascending=[True, False])
        self.df = self.df.drop_duplicates(subset=['email'], keep='first')
        self.df = self.df.drop(columns=['valid_info_count'])
        print(f"[TELEMETRY] 2. 信息密度排序去重完毕. 独一主权资产: {len(self.df)} 行.")

        # 3. 跨舱并网：调用 helpers 进行正则技术提白
        if 'skills' in self.df.columns:
            self.df['standard_skills'] = self.df['skills'].apply(
                lambda x: extract_skills_tags(x, self.tech_pattern)
            )
            self.df = self.df.drop(columns=['skills'])
            print(f"[TELEMETRY] 3. 跨舱并网成功。标准技能标签提取已合拢.")

        # 4. 补丁抢救：拯救有价值的偏才资产
        safe_fill_rules = {k: v for k, v in self.fill_rules.items() if k in self.df.columns}
        self.df = self.df.fillna(safe_fill_rules)
        print(f"[TELEMETRY] 4. 静态补丁依据中央宪法填充完毕.")

    def export_deliverable(self):
        print("\n--- 🔒 [STAGE 3] 后端落锁维护出货 ---")
        # 终极拦截：剔除假空幽灵行
        self.df = self.df.dropna(how='all')
        
        # 终极碾平断层：重铺索引，防匹配错位
        self.df = self.df.reset_index(drop=True)
        
        # 动态强开输出文件夹（防路径暴毙）
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        
        # 物理落盘
        self.df.to_csv(self.output_path, index=False, encoding='utf-8')
        print(f"[TELEMETRY] 物理落锁成功！生成纯净化黄金数据: {len(self.df)} 行.")
        print(f"➡️ 终极交付地址: {self.output_path}")
