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

6. 全量翻译
```bash
aitr
```

7. 本地测试与构建
```bash
git clone https://github.com/docker/docs.git docsite
cp -r docs_zh/* ./docsite/content
cd docsite
npm install

# 构建 0.154.2
hugo build

# 本地测试
hugo server -D
```

### 2. AI 翻译
- 安装 [**CLI**](https://git.jetsung.com/jetsung/ai-translator) 工具 （增量更新直接使用 AI CLI 工具直接对比）
```bash
curl -L https://fx4.cn/aitr | bash
```

1. 设置环境变量 [`config.toml`](config.example.toml)
```bash
...
[[providers]]
enabled = true
name = "grok"
api_key = "xxx"
base_url = "https://api.x.ai/v1"
model = "grok-3"
concurrency = 1 # 线程数
rate_delay = 3.0 # 每个请求后等待 1.0 秒（可根据限流调整）
```

2. AI 翻译
```bash
aitr
```

## 文档管理器
- [Hugo](https://github.com/gohugoio/hugo) （已内置）
```bash
hugo build
```
