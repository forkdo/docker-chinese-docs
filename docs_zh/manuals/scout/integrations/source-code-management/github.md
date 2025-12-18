---
title: 与 GitHub 集成 Docker Scout
linkTitle: GitHub
description: 使用 GitHub 应用集成 Docker Scout，在你的仓库中直接获得修复建议
keywords: scout, github, integration, image analysis, supply chain, remediation, source code
---

{{< summary-bar feature_name="Docker Scout GitHub" >}}

Docker Scout 的 GitHub 应用集成将 Docker Scout 与你在 GitHub 上的源代码仓库连接起来。这种增强的可见性使 Docker Scout 能够为你提供自动化且上下文相关的修复建议。

## 工作原理

启用 GitHub 集成后，Docker Scout 可以直接将镜像分析结果与源代码关联起来。

分析镜像时，Docker Scout 会检查 [来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)，以确定镜像的源代码仓库位置。如果找到了源位置，并且你已启用 GitHub 应用，Docker Scout 会解析用于构建镜像的 Dockerfile。

解析 Dockerfile 可以揭示用于构建镜像的基础镜像标签。通过了解所使用的基础镜像标签，Docker Scout 可以检测该标签是否已过期，即它是否已更改为不同的镜像摘要。例如，假设你使用 `alpine:3.18` 作为基础镜像，稍后镜像维护者发布了包含安全修复的 `3.18` 补丁版本。你正在使用的 `alpine:3.18` 标签就变成了过期版本；你使用的 `alpine:3.18` 不再是最新版本。

发生这种情况时，Docker Scout 会检测到差异，并通过 [基础镜像更新策略](/manuals/scout/policy/_index.md#up-to-date-base-images-policy) 显示出来。启用 GitHub 集成后，你还会收到如何更新基础镜像的自动化建议。有关 Docker Scout 如何帮助你自动改进供应链行为和安全态势的更多信息，请参阅 [修复](../../policy/remediation.md)。

## 设置

要将 Docker Scout 与你的 GitHub 组织集成：

1. 前往 Docker Scout 仪表板上的 [GitHub 集成](https://scout.docker.com/settings/integrations/github/)。
2. 选择 **Integrate GitHub app** 按钮以打开 GitHub。
3. 选择你想要集成的组织。
4. 选择是要集成 GitHub 组织中的所有仓库，还是手动选择特定仓库。
5. 选择 **Install & Authorize** 以将 Docker Scout 应用添加到组织中。

   这会将你重定向回 Docker Scout 仪表板，其中列出了你的活跃 GitHub 集成。

GitHub 集成现已激活。