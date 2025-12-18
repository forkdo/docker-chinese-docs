# Docker 中文文档

本文档使用 AI 翻译

## 项目流程

### 1. 拉取上游文档
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
git add .
git commit -am init
git push origin docs
```

4. 设置上游仓库
```bash
# GitHub fork Codespaces 方式已自动设置
git remote add upstream https://github.com/docker/docs.git
git fetch upstream main
git checkout upstream/main -- content
```

5. 增量翻译
```bash
rm -rf docs
mv content docs
git diff docs
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
uv run translate_docs.py
```

1. 设置环境变量 `.env`
```bash
API_KEY=
MODEL=
API_URL=https://openrouter.ai/api/v1/chat/completions

ROOT_DIR=./docs
EXCLUDE_DIR=
OUTPUT_MODE=new_folder
```

2. AI 翻译

## 文档管理器
- [Docusaurus](https://docusaurus.io/zh-CN/) （已内置）
```bash
hugo build
```
