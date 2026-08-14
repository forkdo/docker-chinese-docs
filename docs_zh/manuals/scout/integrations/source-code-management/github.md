---
title: 将 Docker Scout 与 GitHub 集成
linkTitle: GitHub
description: 使用 GitHub 应用集成 Docker Scout，直接在代码仓库中获取修复建议
keywords: scout, github, integration, image analysis, supply chain, remediation, source code
params:
  sidebar:
    badge:
      color: gray
      text: Retired
---

> [!IMPORTANT]
>
> Docker Scout 的 GitHub 集成已于 2026 年 7 月 1 日停止服务。对于基础镜像更新，请使用
> 配置了 `package-ecosystem: "docker"` 的 GitHub Dependabot。对于镜像到源代码的
> 关联，请使用 `--provenance=mode=max` 进行构建。

> [!NOTE]
>
> 此停止服务仅适用于 Docker Scout GitHub 应用集成。
> 用于 CI 流水线的 [`docker/scout-action`](https://github.com/docker/scout-action) GitHub
> Action 不受影响，将继续工作。

## 从 GitHub 集成迁移

该集成提供两项能力，每项都有对应的替代方案。

### 基础镜像摘要重钉 (Base-image digest repinning)

使用配置了 `package-ecosystem: "docker"` 的 GitHub Dependabot。Dependabot 会按预定计划
打开 PR 以更新基础镜像标签和摘要。当您以 `FROM image:tag@sha256:...` 的形式固定时，
标签和摘要都会被更新。而 Scout 集成仅更新摘要。

最小 `.github/dependabot.yml`：

```yaml
version: 2
updates:
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
```

请参阅 [配置 Dependabot 版本更新](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuring-dependabot-version-updates)。

### 镜像到源代码的关联

使用 `--provenance=mode=max` 进行构建。Docker Scout 读取生成的来源
证明，从而无需 GitHub 应用即可将镜像关联回其源代码仓库。

```console
$ docker build --provenance=mode=max -t myimage:tag .
```

请参阅 [SLSA 来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。
