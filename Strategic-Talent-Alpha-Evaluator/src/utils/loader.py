# src/utils/loader.py (重构版)

class DataLoader:
    def __init__(self, input_dir='data/01_input_source', raw_dir='data/02_raw'):
        self.input_dir = input_dir
        self.raw_dir = raw_dir
        self.chunksize = 10000  # 核心参数：每次处理 1 万行

    def process_large_file(self, file_path, output_path):
        """流式处理：洗一块，吐一块，内存永不爆炸"""
        # 使用 iterator=True 进行分块读取
        reader = pd.read_csv(file_path, chunksize=self.chunksize)
        
        # 第一次写入：保存头部信息
        first_chunk = True
        for chunk in reader:
            # 在这里可以加入极简的清洗逻辑（比如简单去重或过滤）
            # ... 你的清洗代码 ...
            
            # 模式：'w' 代表覆盖重写，'a' 代表追加
            mode = 'w' if first_chunk else 'a'
            header = first_chunk
            chunk.to_csv(output_path, mode=mode, index=False, header=header)
            first_chunk = False
        
        print(f"✅ [流式处理]：{file_path} 已分块落地至 {output_path}")

