---
title: 自定义代码质量检查工作流
linkTitle: 自定义工作流
summary: 调整你的 GitHub 和 SonarQube 工作流，重点关注特定质量缺陷，集成 CI/CD，并设置自定义阈值。
description: 学习如何自定义提示以聚焦特定质量缺陷，按文件模式过滤，设置质量阈值，并将工作流集成到 GitHub Actions 中，实现自动代码质量检查。
weight: 20
---

现在你已经了解了在 E2B 沙箱中使用 GitHub 和 SonarQube 自动化代码质量工作流的基础知识，你可以根据自身需求自定义该工作流。

## 聚焦特定质量缺陷

修改提示词，优先处理某些类型的缺陷：

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

```typescript
const prompt = `使用 SonarQube 和 GitHub MCP 工具：

仅关注：
- 安全漏洞（CRITICAL 优先级）
- Bug（HIGH 优先级）
- 本次迭代跳过代码异味

分析 "${repoPath}"，并优先修复最高优先级的缺陷。`;
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
prompt = f"""使用 SonarQube 和 GitHub MCP 工具：

仅关注：
- 安全漏洞（CRITICAL 优先级）
- Bug（HIGH 优先级）
- 本次迭代跳过代码异味

分析 "{repo_path}"，并优先修复最高优先级的缺陷。"""
```

{{< /tab >}}
{{< /tabs >}}

## 集成 CI/CD

在 GitHub Actions 中添加此工作流，使其在拉取请求时自动运行：

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

```yaml
name: 自动化质量检查
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "18"
      - run: npm install
      - run: npx tsx 06-quality-gated-pr.ts
        env:
          E2B_API_KEY: ${{ secrets.E2B_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONARQUBE_TOKEN: ${{ secrets.SONARQUBE_TOKEN }}
          GITHUB_OWNER: ${{ github.repository_owner }}
          GITHUB_REPO: ${{ github.event.repository.name }}
          SONARQUBE_ORG: your-org-key
```

{{< /tab >}}
{{< tab name="Python" >}}

```yaml
name: 自动化质量检查
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.8"
      - run: pip install e2b python-dotenv
      - run: python 06_quality_gated_pr.py
        env:
          E2B_API_KEY: ${{ secrets.E2B_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONARQUBE_TOKEN: ${{ secrets.SONARQUBE_TOKEN }}
          GITHUB_OWNER: ${{ github.repository_owner }}
          GITHUB_REPO: ${{ github.event.repository.name }}
          SONARQUBE_ORG: your-org-key
```

{{< /tab >}}
{{< /tabs >}}

## 按文件模式过滤

针对代码库的特定部分：

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

```typescript
const prompt = `分析代码质量，但仅考虑：
- src/**/*.js 中的文件
- 排除测试文件（*.test.js, *.spec.js）
- 排除 dist/ 中的构建产物

仅关注生产代码。`;
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
prompt = """分析代码质量，但仅考虑：
- src/**/*.js 中的文件
- 排除测试文件（*.test.js, *.spec.js）
- 排除 dist/ 中的构建产物

仅关注生产代码。"""
```

{{< /tab >}}
{{< /tabs >}}

## 设置质量阈值

定义何时应创建拉取请求：

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

```typescript
const prompt = `质量门禁阈值：
- 仅在满足以下条件时创建 PR：
  * Bug 数量至少减少 1 个
  * 未引入新的安全漏洞
  * 代码覆盖率未下降
  * 技术债务至少减少 15 分钟

若变更不满足这些阈值，说明原因并跳过 PR 创建。`;
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
prompt = """质量门禁阈值：
- 仅在满足以下条件时创建 PR：
  * Bug 数量至少减少 1 个
  * 未引入新的安全漏洞
  * 代码覆盖率未下降
  * 技术债务至少减少 15 分钟

若变更不满足这些阈值，说明原因并跳过 PR 创建。"""
```

{{< /tab >}}
{{< /tabs >}}

## 后续步骤

学习如何排查常见问题。