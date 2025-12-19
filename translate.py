import os
import argparse
import time
import threading
from queue import Queue
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from openai import OpenAI
import tomllib

# ==================== 默认系统提示词 ====================
DEFAULT_SYSTEM_PROMPT = """
你是一个专业的技术文档翻译专家。请将以下英文 Markdown 文档翻译成流畅、自然的简体中文。

严格要求：
1. 保留完整的 Markdown 格式，包括标题、列表、表格、代码块、链接、图片等一切结构完全不变。
2. 代码块、命令行、文件名、路径、API 名称、配置文件内容、技术术语等保持原样（不要翻译）。
3. 专有名词（如产品名、框架名、软件名，例如 Traefik、Docker、Kubernetes）保持英文原名。
4. 对于 YAML frontmatter（文档开头的 --- 之间的内容）：
   - 只翻译实际的字符串值内容。
   - 如果出现 YAML 锚点（&xxx）和别名（*xxx）机制，必须完整保留：
     • 锚点定义处的字符串值进行翻译（例如 &desc 后面的内容）。
     • 别名引用（如 *desc）必须保持原样不翻译、不删除、不展开。
   - 其他字段（如 keywords、tags、params 等）按正常规则处理：keywords 和 tags 中的专有名词不翻译。
5. 翻译要准确、专业、易懂，技术术语使用业界通用中文表达。
6. 只输出翻译后的完整 Markdown 内容，不要添加任何说明、注释或多余文本。
"""

# ==================== 持久化记录文件 ====================
TRANSLATED_RECORD_FILE = "translated_files.txt"
FAILED_RECORD_FILE = "failed_translations.txt"  # 新增：失败记录文件

translated_lock = threading.Lock()
failed_lock = threading.Lock()
translated_files = set()
failed_files = set()

def load_translated_files():
    if os.path.exists(TRANSLATED_RECORD_FILE):
        with open(TRANSLATED_RECORD_FILE, "r", encoding="utf-8") as f:
            for line in f:
                path = line.strip()
                if path:
                    translated_files.add(path)

def save_translated_file(file_path: str):
    abs_path = os.path.abspath(file_path)
    with translated_lock:
        if abs_path not in translated_files:
            translated_files.add(abs_path)
            with open(TRANSLATED_RECORD_FILE, "a", encoding="utf-8") as f:
                f.write(abs_path + "\n")

def load_failed_files():
    if os.path.exists(FAILED_RECORD_FILE):
        with open(FAILED_RECORD_FILE, "r", encoding="utf-8") as f:
            for line in f:
                path = line.strip()
                if path and os.path.exists(path):  # 只加载存在的文件
                    failed_files.add(path)

def save_failed_file(file_path: str):
    abs_path = os.path.abspath(file_path)
    with failed_lock:
        if abs_path not in failed_files:
            failed_files.add(abs_path)
            with open(FAILED_RECORD_FILE, "a", encoding="utf-8") as f:
                f.write(abs_path + "\n")

def remove_from_failed(file_path: str):
    abs_path = os.path.abspath(file_path)
    with failed_lock:
        if abs_path in failed_files:
            failed_files.remove(abs_path)
            # 重写文件去除已成功的条目（保持干净）
            remaining = [p for p in failed_files if p != abs_path]
            with open(FAILED_RECORD_FILE, "w", encoding="utf-8") as f:
                for p in remaining:
                    f.write(p + "\n")

load_translated_files()
load_failed_files()

# ==================== 日志记录 ====================
log_lock = threading.Lock()
SINGLE_FILE_MODE = False
FORCE_TRANSLATE = False
RETRY_FAILED_MODE = False  # 新增：是否为重试失败模式

def log_translation(provider_name: str, rel_path: str, save_path: str, success: bool, log_file: str):
    if SINGLE_FILE_MODE:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    thread_name = threading.current_thread().name
    status = "成功" if success else "失败"
    log_line = f"[{timestamp}] [{thread_name}] [{provider_name}] {status} | {rel_path} → {save_path}\n"
    
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    with log_lock:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_line)

# ==================== 加载配置 ====================
def load_config(config_path: str = "config.toml") -> Dict[str, Any]:
    if not os.path.exists(config_path):
        print(f"错误：配置文件 {config_path} 不存在！")
        exit(1)

    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    root_dir = os.path.abspath(data["root_dir"])
    output_dir = os.path.abspath(data["output_dir"])
    output_mode = data["output_mode"].lower()
    max_tokens = int(data.get("max_tokens", 8192))
    log_file = data.get("log_file", "translation.log").strip()

    exclude_str = data.get("exclude_dir", "").strip()
    exclude_dirs = [d.strip() for d in exclude_str.split(",") if d.strip()]

    system_prompt = data.get("system_prompt", DEFAULT_SYSTEM_PROMPT).strip()

    raw_providers = data.get("providers", [])
    providers = []
    for p in raw_providers:
        api_key = p["api_key"].strip()
        model = p.get("model", "unknown-model").strip()
        base_url = p["base_url"].strip().rstrip("/")

        name = p.get("name", model).strip() or model
        concurrency = max(1, int(p.get("concurrency", 1)))
        rate_delay = float(p.get("rate_delay", 3.0))

        if not api_key or not base_url:
            print(f"警告：跳过无效的 provider（缺少 api_key 或 base_url）")
            continue

        providers.append({
            "name": name,
            "api_key": api_key,
            "model": model,
            "base_url": base_url,
            "concurrency": concurrency,
            "rate_delay": rate_delay
        })

    if not providers:
        print("错误：未配置任何 API providers")
        exit(1)

    return {
        "root_dir": root_dir,
        "output_dir": output_dir,
        "output_mode": output_mode,
        "exclude_dirs": exclude_dirs,
        "system_prompt": system_prompt,
        "max_tokens": max_tokens,
        "log_file": log_file,
        "raw_providers": providers
    }

config = load_config()
ROOT_DIR = config["root_dir"]
OUTPUT_DIR = config["output_dir"]
OUTPUT_MODE = config["output_mode"]
EXCLUDE_DIRS = config["exclude_dirs"]
SYSTEM_PROMPT = config["system_prompt"]
MAX_TOKENS = config["max_tokens"]
LOG_FILE = config["log_file"]
RAW_PROVIDERS = config["raw_providers"]

# 初始化日志
log_dir = os.path.dirname(LOG_FILE)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write(f"# 翻译日志 - 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Provider 测试
def test_provider(provider: Dict) -> bool:
    try:
        client = OpenAI(api_key=provider["api_key"], base_url=provider["base_url"])
        client.chat.completions.create(
            model=provider["model"],
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5,
            timeout=30
        )
        return True
    except:
        return False

PROVIDERS = [p for p in RAW_PROVIDERS if test_provider(p)]
if not PROVIDERS:
    print("错误：所有 API providers 均不可用！")
    exit(1)

print(f"共 {len(PROVIDERS)} 个 provider 可用，将用于翻译。")

# ==================== 收集文件 ====================
def collect_files() -> List[str]:
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        current_rel = os.path.relpath(dirpath, ROOT_DIR)
        if any(ex in current_rel.split(os.sep) for ex in EXCLUDE_DIRS):
            continue
        for filename in filenames:
            if filename.endswith((".md", ".mdx")):
                files.append(os.path.join(dirpath, filename))
    return files

# ==================== 全局状态 ====================
file_queue = Queue()

def is_likely_chinese(content: str) -> bool:
    return sum(1 for c in content if '\u4e00' <= c <= '\u9fff') > 100

# ==================== 翻译工作者 ====================
def translate_worker(provider: Dict):
    name = threading.current_thread().name
    provider_name = provider["name"]
    rate_delay = provider["rate_delay"]
    client = OpenAI(api_key=provider["api_key"], base_url=provider["base_url"])

    while True:
        file_path = file_queue.get()
        if file_path is None:
            break

        rel_path = os.path.relpath(file_path, ROOT_DIR)
        abs_path = os.path.abspath(file_path)

        # 增量检查（重试失败模式下也尊重已翻译记录）
        with translated_lock:
            if abs_path in translated_files and not FORCE_TRANSLATE:
                print(f"[{name}] [{provider_name}] 跳过已翻译: {rel_path}")
                file_queue.task_done()
                continue
            translated_files.add(abs_path)  # 提前标记，避免重复

        print(f"[{name}] [{provider_name}] 开始翻译: {rel_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            msg = f"读取失败: {e}"
            print(f"[{name}] [{provider_name}] {msg} - {rel_path}")
            if not SINGLE_FILE_MODE:
                log_translation(provider_name, rel_path, msg, False, LOG_FILE)
            save_failed_file(file_path)
            file_queue.task_done()
            time.sleep(rate_delay)
            continue

        if not FORCE_TRANSLATE and is_likely_chinese(content):
            print(f"[{name}] [{provider_name}] 跳过中文文件: {rel_path}")
            if not SINGLE_FILE_MODE:
                log_translation(provider_name, rel_path, "已翻译（跳过）", True, LOG_FILE)
            file_queue.task_done()
            time.sleep(rate_delay)
            continue

        success = False
        translated = None
        for retry in range(3):
            try:
                response = client.chat.completions.create(
                    model=provider["model"],
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": content}
                    ],
                    temperature=0.3,
                    max_tokens=MAX_TOKENS,
                    timeout=600
                )
                translated = response.choices[0].message.content.strip()
                success = True
                break
            except Exception as e:
                print(f"[{name}] [{provider_name}] 第 {retry+1} 次失败: {e}")
                time.sleep(15)

        if not success:
            msg = "翻译失败（多次重试后）"
            print(f"[{name}] [{provider_name}] {msg}: {rel_path}")
            if not SINGLE_FILE_MODE:
                log_translation(provider_name, rel_path, msg, False, LOG_FILE)
            save_failed_file(file_path)
            # 失败移除已翻译标记
            with translated_lock:
                translated_files.discard(abs_path)
            file_queue.task_done()
            time.sleep(rate_delay)
            continue

        # 保存翻译结果
        if OUTPUT_MODE == "new_folder":
            rel_dir = os.path.dirname(rel_path)
            save_dir = os.path.join(OUTPUT_DIR, rel_dir) if rel_dir != "." else OUTPUT_DIR
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, os.path.basename(file_path))
        else:
            save_path = file_path

        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(translated)
            print(f"[{name}] [{provider_name}] 翻译完成 → {save_path}")
            if not SINGLE_FILE_MODE:
                log_translation(provider_name, rel_path, save_path, True, LOG_FILE)
            save_translated_file(abs_path)
            remove_from_failed(file_path)  # 成功后从失败列表移除
        except Exception as e:
            msg = f"写入失败: {e}"
            print(f"[{name}] [{provider_name}] {msg} - {save_path}")
            if not SINGLE_FILE_MODE:
                log_translation(provider_name, rel_path, msg, False, LOG_FILE)
            save_failed_file(file_path)
            with translated_lock:
                translated_files.discard(abs_path)

        file_queue.task_done()
        time.sleep(rate_delay)

# ==================== 单文件翻译 ====================
def translate_single_file(file_path: str):
    global SINGLE_FILE_MODE
    SINGLE_FILE_MODE = True
    if not PROVIDERS:
        print("错误：无可用 Provider")
        return
    provider = PROVIDERS[0]
    temp_queue = Queue()
    temp_queue.put(file_path)
    temp_queue.put(None)
    translate_worker(provider)
    SINGLE_FILE_MODE = False

# ==================== 批量翻译（含重试失败模式） ====================
def translate_all_parallel():
    global RETRY_FAILED_MODE

    if RETRY_FAILED_MODE:
        if not failed_files:
            print("没有发现上次翻译失败的文件（failed_translations.txt 为空或无有效路径）")
            return
        pending = list(failed_files)
        print(f"重试模式：发现 {len(pending)} 个上次翻译失败的文件")
    else:
        files = collect_files()
        if not files:
            print("未找到任何 Markdown 文件")
            return

        pending = [f for f in files if os.path.abspath(f) not in translated_files or FORCE_TRANSLATE]
        skipped = len(files) - len(pending)
        print(f"发现 {len(files)} 个文件，已完成 {skipped} 个，待翻译 {len(pending)} 个")

        if not pending:
            print("所有文件已翻译完成！")
            return

    for f in pending:
        file_queue.put(f)

    total_threads = sum(p["concurrency"] for p in PROVIDERS)
    print(f"启动 {total_threads} 个线程进行并发翻译...")

    with ThreadPoolExecutor(max_workers=total_threads, thread_name_prefix="Worker") as executor:
        for provider in PROVIDERS:
            for _ in range(provider["concurrency"]):
                executor.submit(translate_worker, provider)

        for _ in range(total_threads):
            file_queue.put(None)

    print(f"\n全部完成！")
    print(f"日志文件: {os.path.abspath(LOG_FILE)}")
    print(f"已翻译记录: {os.path.abspath(TRANSLATED_RECORD_FILE)}")
    if os.path.exists(FAILED_RECORD_FILE):
        print(f"失败记录文件: {os.path.abspath(FAILED_RECORD_FILE)}（可使用 --retry-failed 重试）")

# ==================== main ====================
def main():
    parser = argparse.ArgumentParser(description="Markdown 文档翻译工具")
    parser.add_argument("file", nargs="?", help="指定单个要翻译的文件")
    parser.add_argument("--config", default="config.toml", help="配置文件路径")
    parser.add_argument("--force", action="store_true", help="强制重新翻译所有文件")
    parser.add_argument("--retry-failed", action="store_true", help="仅重试上次翻译失败的文件（从 failed_translations.txt 读取）")

    args = parser.parse_args()

    global FORCE_TRANSLATE, RETRY_FAILED_MODE
    FORCE_TRANSLATE = args.force
    RETRY_FAILED_MODE = args.retry_failed

    print(f"强制重新翻译 → {'是' if FORCE_TRANSLATE else '否'}")
    if RETRY_FAILED_MODE:
        print("模式：仅重试上次失败的文件")
    print(f"已成功翻译文件数: {len(translated_files)}")
    if os.path.exists(FAILED_RECORD_FILE):
        print(f"上次失败文件数: {len(failed_files)}")

    if args.file:
        translate_single_file(args.file)
    else:
        translate_all_parallel()

if __name__ == "__main__":
    main()