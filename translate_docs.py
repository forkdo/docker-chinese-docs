import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

# ==================== 请修改这里 ====================
API_KEY = os.getenv("API_KEY")  # ← 把你的 API Key 填在这里
MODEL = os.getenv("MODEL")  # 或者 "grok-3"，根据你的权限选择
ROOT_DIR = os.getenv("ROOT_DIR")  # 仓库根目录，通常是当前目录 "."
EXCLUDE_DIR = os.getenv("EXCLUDE_DIR")  # 要排除的目录名
OUTPUT_MODE = os.getenv("OUTPUT_MODE")  # "overwrite" 直接覆盖原文件；"new_folder" 保存到 OUTPUT_DIR 新目录
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "translated") # 保存的目标文件夹
# ====================================================

API_URL = os.getenv("API_URL")

system_prompt = """
你是一个专业的技术文档翻译专家。请将以下英文 Markdown 文档翻译成流畅、自然的简体中文。
要求：
- 保留完整的 Markdown 格式（标题、列表、表格、代码块、链接等完全不变）
- 代码块、命令行、文件名、API 名称等技术术语保持原样（不要翻译）
- 专有名词（如产品名、框架名）保持英文原名
- 翻译要准确、专业、易懂
- 只输出翻译后的完整 Markdown 内容，不要添加任何说明
"""

def translate_text(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3,
        "max_tokens": 4096
    }
    
    for retry in range(3):  # 重试机制
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                print(f"API 错误 {response.status_code}: {response.text}")
                time.sleep(5)
        except Exception as e:
            print(f"请求异常: {e}")
            time.sleep(5)
    return None

def main():
    translated_count = 0
    
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        # 排除 update-notes 目录及其子目录
        if EXCLUDE_DIR in dirpath.split(os.sep):
            continue
            
        for filename in filenames:
            if filename.endswith((".md", ".mdx")):
                file_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(file_path, ROOT_DIR)
                
                # 读取原文件
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    print(f"读取失败: {rel_path} - {e}")
                    continue
                
                # 如果已经是中文（简单判断），可跳过
                if "语言" in content or "翻译" in content:
                    print(f"跳过（疑似已翻译）: {rel_path}")
                    continue
                
                print(f"正在翻译: {rel_path}")
                translated = translate_text(content)
                
                if translated is None:
                    print(f"翻译失败: {rel_path}")
                    continue
                
                # 保存翻译结果
                if OUTPUT_MODE == "new_folder":
                    os.makedirs(OUTPUT_DIR, exist_ok=True)
                    save_path = os.path.join(OUTPUT_DIR, rel_path)
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                else:
                    save_path = file_path
                
                try:
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(translated)
                    print(f"翻译完成: {rel_path} → {save_path}")
                    translated_count += 1
                except Exception as e:
                    print(f"写入失败: {save_path} - {e}")
                
                # 避免触发 API 限流
                time.sleep(2)
    
    print(f"\n全部完成！共翻译 {translated_count} 个文件。")

if __name__ == "__main__":
    main()