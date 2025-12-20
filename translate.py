import os
import random
import argparse
import time
import threading
import logging
import atexit
from queue import Queue
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from openai import OpenAI
import tomllib
import yaml

# ==================== 默认系统提示词 ====================
DEFAULT_SYSTEM_PROMPT = """
你是一个专业的技术文档翻译专家。请将以下英文 Markdown 文档翻译成流畅、自然的简体中文。

严格要求：
1. 保留完整的 Markdown 格式，包括标题、列表、表格、代码块、链接、图片等一切结构完全不变。
2. 代码块、命令行、文件名、路径、API 名称、配置文件内容、技术术语等保持原样（不要翻译）。
3. 专有名词（如产品名、框架名、软件名，例如 Traefik、Docker、Kubernetes）保持英文原名。
4. 对于 YAML frontmatter（文档开头的 --- 之间的内容）：
   - 只翻译实际的字符串值内容（如 title、description 等字段的值）。
   - 严格保留原文档中的所有字段、键名、结构、格式、缩进和所有机制（包括已有的 YAML 锚点 &xxx 和别名 *xxx）。
   - 如果原文档中已有锚点定义，则在翻译该锚点对应的字符串值时保留锚点标记（如 &desc）；别名引用（如 *desc）保持原样不变。
   - 如果原文档中没有锚点或别名，则翻译后绝对不得新增任何锚点、别名、params 块或其他额外字段。
   - 绝对不得添加、删除或修改任何原有字段、锚点、别名或 params 等结构，仅对需要翻译的字符串值进行翻译。
   - `aliases`、`keywords`、`tags` 等列表字段中的值，**无论原始值是英文还是中文，都保持原样，绝对不要进行任何翻译或改动。**
5. 翻译要准确、专业、易懂，技术术语使用业界通用中文表达。
6. 只输出翻译后的完整 Markdown 内容，不要添加任何说明、注释或多余文本。
"""

# ==================== 配置加载 ====================
def load_config(config_path: str = "config.toml") -> Dict[str, Any]:
    if not os.path.exists(config_path):
        print(f"错误：配置文件 {config_path} 不存在！")
        exit(1)

    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    return {
        "root_dir": os.path.abspath(data["root_dir"]),
        "output_dir": os.path.abspath(data["output_dir"]),
        "output_mode": data["output_mode"].lower(),
        "exclude_dirs": [d.strip() for d in data.get("exclude_dir", "").split(",") if d.strip()],
        "system_prompt": data.get("system_prompt", DEFAULT_SYSTEM_PROMPT).strip(),
        "max_tokens": int(data.get("max_tokens", 8192)),
        "log_file": data.get("log_file", "translation.log").strip(),
        "raw_providers": data.get("providers", [])
    }

config = load_config()
ROOT_DIR = config["root_dir"]
OUTPUT_DIR = config["output_dir"]
OUTPUT_MODE = config["output_mode"]
EXCLUDE_DIRS = config["exclude_dirs"]
SYSTEM_PROMPT = config["system_prompt"]
MAX_TOKENS = config["max_tokens"]
LOG_FILE = config["log_file"]

# YAML Frontmatter fields to preserve (do not translate their values)
PRESERVE_FIELDS = ["tags", "keywords", "aliases"]

# ==================== 日志与记录管理 ====================
# Setup Logging
log_dir = os.path.dirname(LOG_FILE)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(threadName)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        # logging.StreamHandler() # 不输出到控制台，保持 CLI 简洁
    ]
)
logger = logging.getLogger("Translator")

class TranslationRecorder:
    def __init__(self, translated_file="translated_files.txt", failed_file="failed_translations.txt"):
        self.translated_file = translated_file
        self.failed_file = failed_file
        self.translated_lock = threading.Lock()
        self.failed_lock = threading.Lock()
        
        self.translated_set = set()
        self.failed_set = set()
        
        self._load_existing()
        
        # 保持文件句柄打开，减少 IO 开销
        self.f_translated = open(self.translated_file, "a", encoding="utf-8", buffering=1)
        self.f_failed = open(self.failed_file, "a", encoding="utf-8", buffering=1)
        
        atexit.register(self.close)

    def _load_existing(self):
        if os.path.exists(self.translated_file):
            with open(self.translated_file, "r", encoding="utf-8") as f:
                for line in f:
                    path = line.strip()
                    if path: self.translated_set.add(path)
        
        if os.path.exists(self.failed_file):
            with open(self.failed_file, "r", encoding="utf-8") as f:
                for line in f:
                    path = line.strip()
                    if path: self.failed_set.add(path)

    def is_translated(self, abs_path):
        return abs_path in self.translated_set

    def record_success(self, abs_path):
        with self.translated_lock:
            if abs_path not in self.translated_set:
                self.translated_set.add(abs_path)
                self.f_translated.write(abs_path + "\n")
        
        # 成功后尝试从失败列表中移除（如果存在）
        self.remove_from_failed(abs_path)

    def record_failure(self, abs_path):
        with self.failed_lock:
            if abs_path not in self.failed_set:
                self.failed_set.add(abs_path)
                self.f_failed.write(abs_path + "\n")

    def remove_from_failed(self, abs_path):
        # 检查是否在失败集合中，如果在则移除并重写文件
        # 注意：这里涉及到重写文件，性能较低，但成功操作相对低频且必要
        with self.failed_lock:
            if abs_path in self.failed_set:
                self.failed_set.remove(abs_path)
                # 关闭追加句柄，重写，再重新打开
                self.f_failed.close()
                with open(self.failed_file, "w", encoding="utf-8") as f:
                    for p in self.failed_set:
                        f.write(p + "\n")
                self.f_failed = open(self.failed_file, "a", encoding="utf-8", buffering=1)

    def close(self):
        try:
            self.f_translated.close()
            self.f_failed.close()
        except:
            pass

recorder = TranslationRecorder()

# ==================== Provider 初始化 ====================
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

PROVIDERS = [] # Global list to be populated

def initialize_providers(skip_check: bool):
    global PROVIDERS # Declare intent to modify global PROVIDERS list
    if skip_check:
        print("Skipping API Provider checks.")
        # Just load providers without testing, assuming they are valid
        for p in config["raw_providers"]:
            api_key = p["api_key"].strip()
            base_url = p["base_url"].strip().rstrip("/")
            if not api_key or not base_url: continue
            PROVIDERS.append({
                "name": p.get("name", p.get("model", "unknown")),
                "api_key": api_key,
                "model": p.get("model", "unknown").strip(),
                "base_url": base_url,
                "concurrency": max(1, int(p.get("concurrency", 1))),
                "rate_delay": float(p.get("rate_delay", 3.0))
            })
    else:
        print("Checking API Providers...")
        for p in config["raw_providers"]:
            api_key = p["api_key"].strip()
            base_url = p["base_url"].strip().rstrip("/")
            if not api_key or not base_url: continue
            
            provider_config = {
                "name": p.get("name", p.get("model", "unknown")),
                "api_key": api_key,
                "model": p.get("model", "unknown").strip(),
                "base_url": base_url,
                "concurrency": max(1, int(p.get("concurrency", 1))),
                "rate_delay": float(p.get("rate_delay", 3.0))
            }
            
            if test_provider(provider_config):
                print(f"✅ [{provider_config['name']}] Ready")
                PROVIDERS.append(provider_config)
            else:
                print(f"❌ [{provider_config['name']}] Unavailable")

    if not PROVIDERS:
        print("Error: No providers available.")
        exit(1)

    print(f"Total {len(PROVIDERS)} providers available.")
# ==================== 全局状态 ====================
file_queue = Queue()
SINGLE_FILE_MODE = False
FORCE_TRANSLATE = False
RETRY_FAILED_MODE = False

def is_likely_chinese(content: str) -> bool:
    return sum(1 for c in content if '\u4e00' <= c <= '\u9fff') > 100

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

        # 检查是否已翻译
        if not FORCE_TRANSLATE and recorder.is_translated(abs_path):
            # print(f"SKIP: {rel_path}") # 减少刷屏
            file_queue.task_done()
            continue

        # print(f"[{provider_name}] Start: {rel_path}") # 减少刷屏

        # Prepare frontmatter and body
        original_frontmatter_str = ""
        original_body = ""
        
        frontmatter_for_llm_dict = {} # Frontmatter without preserved fields, for LLM
        preserved_data = {} # Data to be re-inserted (from English frontmatter)

        # Get corresponding English file path
        # If ROOT_DIR is /root/test/docker-chinese-docs
        # and file_path is /root/test/docker-chinese-docs/docs_zh/manuals/foo.md
        # then rel_path is docs_zh/manuals/foo.md
        # english_abs_path should be /root/test/docker-chinese-docs/docs/manuals/foo.md
        # Corrected mapping:
        english_abs_path = os.path.join(ROOT_DIR, rel_path.replace("docs_zh", "docs", 1))
        
        english_frontmatter = {}
        has_english_frontmatter = False

        try:
            # Try to load English frontmatter for preserving fields
            if os.path.exists(english_abs_path):
                with open(english_abs_path, "r", encoding="utf-8") as f_en:
                    english_content = f_en.read()
                if english_content.startswith("---"):
                    parts_en = english_content.split("---", 2)
                    if len(parts_en) == 3:
                        english_frontmatter = yaml.safe_load(parts_en[1].strip())
                        has_english_frontmatter = True
                        # Extract preserved data from English frontmatter
                        preserved_data = {field: english_frontmatter.get(field) for field in PRESERVE_FIELDS if english_frontmatter.get(field) is not None}
            else:
                logger.warning(f"[{provider_name}] English equivalent not found for {rel_path} at {english_abs_path}. Cannot preserve fields from English source.")

            # Load Chinese content and frontmatter
            with open(file_path, "r", encoding="utf-8") as f_zh:
                content = f_zh.read()
            
            # Split frontmatter and body from Chinese content
            if content.startswith("---"):
                parts_zh = content.split("---", 2)
                if len(parts_zh) == 3:
                    original_frontmatter_str = parts_zh[1].strip()
                    original_body = parts_zh[2].strip()
                    
                    current_chinese_frontmatter = yaml.safe_load(original_frontmatter_str)

                    # Create frontmatter for LLM: start with current Chinese frontmatter, but remove PRESERVE_FIELDS
                    frontmatter_for_llm_dict = current_chinese_frontmatter.copy()
                    for field in PRESERVE_FIELDS:
                        if field in frontmatter_for_llm_dict:
                            del frontmatter_for_llm_dict[field]

                    # Construct content for LLM: only translated frontmatter + body
                    modified_content_for_llm = "---\n" + yaml.dump(frontmatter_for_llm_dict, allow_unicode=True, sort_keys=False) + "---\n" + original_body
                else: # No valid frontmatter, treat as plain markdown
                    original_body = content
                    modified_content_for_llm = content
            else: # No frontmatter, treat as plain markdown
                original_body = content
                modified_content_for_llm = content

        except Exception as e:
            logger.error(f"[{provider_name}] Read/Parse Error {rel_path}: {e}")
            print(f"❌ Read/Parse Error: {rel_path}")
            recorder.record_failure(abs_path)
            file_queue.task_done()
            continue
        
        if not FORCE_TRANSLATE and is_likely_chinese(original_body): # Check original_body if frontmatter was stripped
            logger.info(f"[{provider_name}] Skip (Chinese): {rel_path}")
            recorder.record_success(abs_path) # 标记为已处理
            file_queue.task_done()
            continue

        success = False
        translated_text = None
        
        for retry in range(3):
            try:
                response = client.chat.completions.create(
                    model=provider["model"],
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": modified_content_for_llm}
                    ],
                    temperature=0.3,
                    max_tokens=MAX_TOKENS,
                    timeout=600
                )
                translated_text = response.choices[0].message.content.strip()
                success = True
                break
            except Exception as e:
                logger.warning(f"[{provider_name}] Retry {retry+1}/3 {rel_path}: {e}")
                time.sleep(5) # 失败重试等待

        if not success:
            logger.error(f"[{provider_name}] Failed {rel_path}")
            print(f"❌ Failed: {rel_path}")
            recorder.record_failure(abs_path)
            file_queue.task_done()
            time.sleep(rate_delay)
            continue
        
        # Recombine translated content with preserved frontmatter fields from English source
        final_translated_content = translated_text
        if original_frontmatter_str: # If original file had frontmatter
            translated_body = translated_text # Default to full LLM response as body
            translated_frontmatter_from_llm = {} # Frontmatter actually returned by LLM
            
            # Attempt to split LLM response into frontmatter and body
            if translated_text.startswith("---"):
                parts_llm = translated_text.split("---", 2)
                if len(parts_llm) == 3:
                    try:
                        translated_frontmatter_from_llm = yaml.safe_load(parts_llm[1].strip())
                        translated_body = parts_llm[2].strip()
                    except yaml.YAMLError:
                        logger.warning(f"[{provider_name}] LLM returned invalid YAML frontmatter for {rel_path}. Processing as body only for robustness.")
                        translated_body = translated_text # Fallback: treat entire response as body
                else: # LLM returned --- but not valid structure
                    translated_body = translated_text

            # Start with the frontmatter that was sent to LLM (already has original structure and translated non-preserved fields)
            final_frontmatter_dict = frontmatter_for_llm_dict.copy()
            
            # Merge any successfully translated parts of the frontmatter from LLM's response
            # This handles fields like 'title', 'description' that LLM was supposed to translate
            for key, value in translated_frontmatter_from_llm.items():
                final_frontmatter_dict[key] = value

            # Re-insert preserved fields (from English source) into the final frontmatter dictionary
            # These values take precedence.
            for field, value in preserved_data.items():
                if value is not None:
                    final_frontmatter_dict[field] = value
            
            final_translated_content = "---\n" + yaml.dump(final_frontmatter_dict, allow_unicode=True, sort_keys=False) + "---\n" + translated_body
        
        # 保存
        save_path = file_path
        if OUTPUT_MODE == "new_folder":
            rel_dir = os.path.dirname(rel_path)
            save_dir = os.path.join(OUTPUT_DIR, rel_dir) if rel_dir != "." else OUTPUT_DIR
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, os.path.basename(file_path))

        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(final_translated_content)
            
            logger.info(f"[{provider_name}] Success {rel_path} -> {save_path}")
            print(f"✅ Translated: {rel_path}") # 只打印成功
            recorder.record_success(abs_path)
            
        except Exception as e:
            logger.error(f"[{provider_name}] Write Error {save_path}: {e}")
            print(f"❌ Write Error: {save_path}")
            recorder.record_failure(abs_path)

        file_queue.task_done()
        time.sleep(rate_delay)

# ==================== 主要逻辑 ====================
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?")
    parser.add_argument("--config", default="config.toml")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--retry-failed", action="store_true")
    parser.add_argument("--no-provider-check", action="store_true", help="Skip checking API provider availability.")

    args = parser.parse_args()

    global FORCE_TRANSLATE, RETRY_FAILED_MODE, SINGLE_FILE_MODE
    FORCE_TRANSLATE = args.force
    RETRY_FAILED_MODE = args.retry_failed
    # NO_PROVIDER_CHECK = args.no_provider_check # Removed, passed directly

    initialize_providers(args.no_provider_check) # Call after parsing args
    
    if args.file:
        SINGLE_FILE_MODE = True
        if not PROVIDERS: return
        print(f"Translating single file: {args.file}")
        
        provider = random.choice(PROVIDERS)
        print(f"Using Provider: {provider['name']}")
        
        file_queue.put(args.file)
        file_queue.put(None)
        translate_worker(provider)
    else:
        files = []
        if RETRY_FAILED_MODE:
            files = list(recorder.failed_set)
            print(f"Retry Mode: {len(files)} failed files.")
        else:
            all_files = collect_files()
            files = [f for f in all_files if FORCE_TRANSLATE or not recorder.is_translated(os.path.abspath(f))]
            print(f"Found {len(all_files)} files. To translate: {len(files)}")

        if not files:
            print("Nothing to translate.")
            return

        for f in files:
            file_queue.put(f)

        total_threads = sum(p["concurrency"] for p in PROVIDERS)
        print(f"Starting {total_threads} threads...")

        with ThreadPoolExecutor(max_workers=total_threads) as executor:
            for p in PROVIDERS:
                for _ in range(p["concurrency"]):
                    executor.submit(translate_worker, p)
            
            for _ in range(total_threads):
                file_queue.put(None)
        
        print("Done.")

if __name__ == "__main__":
    main()
