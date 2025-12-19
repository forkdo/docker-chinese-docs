---
title: 使用 Docker Scout 进行修复
description: 了解 Docker Scout 如何通过修复功能自动帮助您提升软件质量
keywords: scout, supply chain, security, remediation, automation
---

{{< summary-bar feature_name="Remediation with Docker Scout" >}}

Docker Scout 通过基于策略评估结果提供建议，帮助您修复供应链或安全问题。建议是您可以采取的旨在提升策略合规性的操作，或是为镜像添加元数据的操作，这能让 Docker Scout 提供更优质的评估结果和建议。

Docker Scout 为以下策略类型的默认策略提供修复建议：

- [最新的基础镜像](#up-to-date-base-images-remediation)
- [供应链证明](#supply-chain-attestations-remediation)

<!-- TODO(dvdksn): verify the following -->
> [!NOTE]
> Docker Scout 目前不支持对自定义策略进行引导式修复。

对于违反策略的镜像，建议侧重于解决合规性问题和修复违规行为。对于 Docker Scout 无法确定合规性的镜像，建议会向您展示如何满足先决条件，以确保 Docker Scout 能够成功评估策略。

## 查看建议

建议显示在 Docker Scout 仪表盘的策略详情页上。要访问此页面：

1. 前往 Docker Scout 仪表盘中的 [策略页面](https://scout.docker.com/reports/policy)。
2. 在列表中选择一个策略。

策略详情页根据策略状态将评估结果分为两个不同的选项卡：

- 违规 (Violations)
- 合规性未知 (Compliance unknown)

**违规**选项卡列出了不符合所选策略的镜像。**合规性未知**选项卡列出了 Docker Scout 无法确定其合规性状态的镜像。当合规性未知时，Docker Scout 需要有关镜像的更多信息。

要查看镜像的推荐操作，请将鼠标悬停在列表中的某个镜像上，以显示**查看修复方案 (View fixes)**按钮。

![策略违规的修复方案](../images/remediation.png)

选择**查看修复方案**按钮，会打开修复侧面板，其中包含针对您镜像的推荐操作。

如果有多个可用建议，主要建议会显示为**推荐修复方案 (Recommended fix)**。其他建议则列为**快速修复方案 (Quick fixes)**。快速修复方案通常是提供临时解决方案的操作。

侧面板还可能包含一个或多个与可用建议相关的帮助部分。

## 最新的基础镜像修复

**最新的基础镜像**策略会检查您使用的基础镜像是否为最新版本。修复侧面板中显示的推荐操作取决于 Docker Scout 对您的镜像掌握的信息量。信息越丰富，建议就越精准。

以下场景根据镜像的可用信息概述了不同的建议。

### 无来源证明

为了让 Docker Scout 能够评估此策略，您必须为镜像添加[来源证明 (provenance attestations)](/manuals/build/metadata/attestations/slsa-provenance.md)。如果您的镜像没有来源证明，则无法确定其合规性。

<!--
  TODO(dvdksn): no support for the following, yet

  When provenance attestations are unavailable, Docker Scout provides generic,
  best-effort recommendations in the remediation side panel. These
  recommendations estimate your base using information from image analysis
  results. The base image version is unknown, but you can manually select the
  version you use in the remediation side panel. This lets Docker Scout evaluate
  whether the base image detected in the image analysis is up-to-date with the
  version you selected.

  https://github.com/docker/docs/pull/18961#discussion_r1447186845
-->

### 有可用的来源证明

添加来源证明后，Docker Scout 就能正确检测您正在使用的基础镜像版本。证明中找到的版本会与相应标签的当前版本进行交叉引用，以确定其是否为最新版本。

如果存在策略违规，推荐的操作会展示如何将您的基础镜像版本更新到最新版本，同时将基础镜像版本固定到特定的摘要（digest）。更多信息，请参阅[固定基础镜像版本](/manuals/build/building/best-practices.md#pin-base-image-versions)。

### 已启用 GitHub 集成

如果您将镜像的源代码托管在 GitHub 上，您可以启用 [GitHub 集成](../integrations/source-code-management/github.md)。此集成使 Docker Scout 能够提供更有用的修复建议，并允许您直接从 Docker Scout 仪表盘启动违规修复。

启用 GitHub 集成后，您可以使用修复侧面板在镜像的 GitHub 仓库中发起一个拉取请求（pull request）。该拉取请求会自动将您 Dockerfile 中的基础镜像版本更新为最新版本。

这种自动化修复会将您的基础镜像固定到特定的摘要，同时帮助您在新版本可用时保持最新状态。将基础镜像固定到摘要对于可重现性非常重要，并有助于避免不必要的更改进入您的供应链。

有关基础镜像固定的更多信息，请参阅[固定基础镜像版本](/manuals/build/building/best-practices.md#pin-base-image-versions)。

<!--
  TODO(dvdksn): no support for the following, yet

  Enabling the GitHub integration also allows Docker Scout to visualize the
  remediation workflow in the Docker Scout Dashboard. Each step, from the pull
  request being raised to the image being deployed to an environment, is
  displayed in the remediation sidebar when inspecting the image.

  https://github.com/docker/docs/pull/18961#discussion_r1447189475
-->

## 供应链证明修复

默认的**供应链证明**策略要求镜像具备完整的来源证明和 SBOM（软件物料清单）证明。如果您的镜像缺少证明，或者证明包含的信息不足，则视为违反策略。

修复侧面板中的可用建议会指导您采取何种操作来解决问题。例如，如果您的镜像有来源证明，但证明包含的信息不足，系统会建议您使用 [`mode=max`](/manuals/build/metadata/attestations/slsa-provenance.md#max) 来源证明重新构建镜像。