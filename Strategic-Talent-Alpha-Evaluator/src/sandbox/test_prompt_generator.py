import os
from config.schema_config import AIPromptRegistry

def generate_test_prompt():
    # 1. 读取极品脏简历
    with open("test_dirty_resume.txt", "r", encoding="utf-8") as f:
        dirty_resume = f.read()
    
    # 2. 调取你写好的宪法模板
    template = AIPromptRegistry.EVALUATION_PROMPT_TEMPLATE
    
    # 3. 🚀 核心修复：放弃 .format()，使用最暴力的纯文本物理替换！
    # 这样 Python 就不会去多管闲事解析 JSON 里的 {} 了。
    final_prompt = template.replace("{resume_text}", dirty_resume)
    
    # 4. 打印最终组装好的指令
    print("\n" + "="*50)
    print("🔥 组装完毕的终极 Prompt (请复制以下全部内容发给大模型):")
    print("="*50 + "\n")
    print(final_prompt)
    print("\n" + "="*50)

if __name__ == "__main__":
    generate_test_prompt()