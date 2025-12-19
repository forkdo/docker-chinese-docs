---
title: 自定义代码质量检查工作流
linkTitle: 自定义工作流
summary: 调整 GitHub 和 SonarQube 工作流，重点关注特定质量问题，与 CI/CD 集成，并设置自定义阈值。
description: 了解如何针对特定质量问题自定义提示词、按文件模式过滤、设置质量阈值，并将工作流与 GitHub Actions 集成以实现自动化代码质量检查。
weight: 20
---

现在您已经了解了如何在 E2B 沙箱中使用 GitHub 和 SonarQube 自动化代码质量工作流的基础知识，可以根据需要自定义工作流。

## 重点关注特定质量问题

修改提示词以优先处理某些问题类型：

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

```typescript
const prompt = `Using SonarQube and GitHub MCP tools:

Focus only on:
- Security vulnerabilities (CRITICAL priority)
- Bugs (HIGH priority)
- Skip code smells for this iteration

Analyze "${repoPath}" and fix the highest priority issues first.`;
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
prompt = f"""Using SonarQube and GitHub MCP tools:

Focus only on:
- Security vulnerabilities (CRITICAL priority)
- Bugs (HIGH priority)
- Skip code smells for this iteration

Analyze "{repo_path}" and fix the highest priority issues first."""
```

{{< /tab >}}
{{< /tabs >}}

## 与 CI/CD 集成

将此工作流添加到 GitHub Actions，以便在拉取请求时自动运行：

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

```yaml
name: Automated quality checks
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
name: Automated quality checks
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
const prompt = `Analyze code quality but only consider:
- Files in src/**/*.js
- Exclude test files (*.test.js, *.spec.js)
- Exclude build artifacts in dist/

Focus on production code only.`;
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
prompt = """Analyze code quality but only consider:
- Files in src/**/*.js
- Exclude test files (*.test.js, *.spec.js)
- Exclude build artifacts in dist/

Focus on production code only."""
```

{{< /tab >}}
{{< /tabs >}}

## 设置质量阈值

定义何时应创建 PR：

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

```typescript
const prompt = `Quality gate thresholds:
- Only create PR if:
  * Bug count decreases by at least 1
  * No new security vulnerabilities introduced
  * Code coverage does not decrease
  * Technical debt reduces by at least 15 minutes

If changes do not meet these thresholds, explain why and skip PR creation.`;
```

{{< /tab >}}
{{< tab name="Python" >}}

```python
prompt = """Quality gate thresholds:
- Only create PR if:
  * Bug count decreases by at least 1
  * No new security vulnerabilities introduced
  * Code coverage does not decrease
  * Technical debt reduces by at least 15 minutes

If changes do not meet these thresholds, explain why and skip PR creation."""
```

{{< /tab >}}
{{< /tabs >}}

## 后续步骤

了解如何排查常见问题。