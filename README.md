# Docker 中文文档

本文档使用 AI 翻译

## 项目流程

### 首次使用
1. 创建空分支
```bash
git switch --orphan docs
```

2. 创建 `README.md`
```bash
cat > README.md <<EOF
# 中文文档

本文档使用 AI 翻译
EOF
```

3. 首次提交
```bash
git add README.md
git commit -am init
git push origin docs
```

4. 拉取上游源码
```bash
mkdir docsite
pushd docsite
git init
git remote add upstream https://github.com/docker/docs.git
git pull upstream main
popd
```

5. 复制源文档
```bash
cp -r docsite/content .
rm -rf docs
mv content docs
```

5. 增量翻译
```bash
rm -rf docs
mv content docs
git diff docs/
```

6. 本地测试
```bash
git clone https://github.com/docker/docs.git docsite
cp -r docs_zh/* ./docsite/content
cd docsite
npm install

# 构建 0.141.0
hugo build
```

### 2. AI 翻译
- 安装 CLI 工具 （增量更新直接使用 AI CLI 工具直接对比）
```bash
# npm install -g npm
npm install -g @google/gemini-cli
npm install -g @qwen-code/qwen-code
```
- 使用 UV Python 脚本翻译
```bash
curl -L fx4.cn/uv | bash
uv sync

# 翻译全局
uv run translate.py

# 翻译单文件
uv run translate.py hello.py
```

1. 设置环境变量 [`config.toml`](config.example.toml)
```bash
root_dir = "./docs" # 文档所在目录
exclude_dir = "update-notes, node_modules" # 支持多个，用逗号分隔；留空 "" 表示不排除
output_mode = "new_folder" # 或 "overwrite" 覆盖原文件，"new_folder" 新建文件夹
output_dir = "docs_zh" # 最终翻译文档输出目录
max_tokens = 8192   # 全局 max_tokens 配置，可根据文档大小调整
log_file = "logs/translation.log" # 自定义日志路径（可省略，默认 translation.log）

# 系统提示词（支持多行，使用 """ 包裹）
system_prompt = """
你是一个专业的技术文档翻译专家。请将以下英文 Markdown 文档翻译成流畅、自然的简体中文。
...
"""

[[providers]]
name = "grok"
api_key = "xxx"
base_url = "https://api.x.ai/v1"
model = "grok-3"
concurrency = 4 # 线程数
rate_delay = 3.0 # 每个请求后等待 1.0 秒（可根据限流调整）
```

2. AI 翻译

## 文档管理器
- [Hugo](https://github.com/gohugoio/hugo) （已内置）
```bash
hugo build
```
