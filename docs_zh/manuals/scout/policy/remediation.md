---
title: 使用 Docker Scout 进行修复
description: 了解 Docker Scout 如何通过提供基于策略评估结果的建议来自动帮助您改善软件质量
keywords: scout, 供应链, 安全, 修复, 自动化
---

{{< summary-bar feature_name="使用 Docker Scout 进行修复" >}}

Docker Scout 通过提供基于策略评估结果的建议来帮助您修复供应链或安全问题。这些建议是您可以采取的行动，以改善策略合规性，或为镜像添加元数据，从而使 Docker Scout 能够提供更好的评估结果和建议。

Docker Scout 为以下策略类型的默认策略提供修复建议：

- [最新的基础镜像](#最新的基础镜像-修复)
- [供应链证明](#供应链证明-修复)

<!-- TODO(dvdksn): verify the following -->
> [!NOTE]
> 引导式修复不支持自定义策略。

对于违反策略的镜像，建议侧重于解决合规问题和修复违规。对于 Docker Scout 无法确定合规性的镜像，建议会显示如何满足先决条件，以确保 Docker Scout 能够成功评估策略。

## 查看建议

建议会显示在 Docker Scout 仪表板的策略详细信息页面上。要进入此页面：

1. 前往 Docker Scout 仪表板中的 [策略页面](https://scout.docker.com/reports/policy)。
2. 在列表中选择一个策略。

策略详细信息页面根据策略状态将评估结果分为两个不同的标签页：

- 违规
- 合规性未知

**违规**标签页列出不符合所选策略的镜像。**合规性未知**标签页列出 Docker Scout 无法确定合规状态的镜像。当合规性未知时，Docker Scout 需要有关镜像的更多信息。

要查看镜像的建议操作，请将鼠标悬停在列表中的一个镜像上，以显示 **查看修复** 按钮。

![策略违规的修复](../images/remediation.png)

选择 **查看修复** 按钮会打开包含镜像建议操作的修复侧边栏。

如果有多个建议可用，主要建议会显示为 **推荐的修复**。其他建议会列为 **快速修复**。快速修复通常是提供临时解决方案的操作。

侧边栏还可能包含一个或多个与可用建议相关的帮助部分。

## 最新的基础镜像 修复

**最新的基础镜像** 策略检查您使用的基础镜像是否为最新版本。在修复侧边栏中显示的建议操作取决于 Docker Scout 对您镜像的了解程度。可用信息越多，建议就越好。

以下场景概述了根据镜像可用信息的不同建议。

### 无可信证明

为了让 Docker Scout 能够评估此策略，您必须为镜像添加 [可信证明](/manuals/build/metadata/attestations/slsa-provenance.md)。如果您的镜像没有可信证明，合规性就无法确定。

<!--
  TODO(dvdksn): no support for the following, yet

  当无可信证明时，Docker Scout 会在修复侧边栏中提供通用的、尽力而为的建议。这些建议基于镜像分析结果中的信息来估算您的基础镜像。基础镜像版本未知，但您可以在修复侧边栏中手动选择您使用的版本。这使得 Docker Scout 能够评估在镜像分析中检测到的基础镜像是否与您选择的版本保持最新。

  https://github.com/docker/docs/pull/18961#discussion_r1447186845
-->

### 可信证明可用

添加可信证明后，Docker Scout 可以正确检测您正在使用的基础镜像版本。在证明中找到的版本会与相应标签的当前版本进行交叉引用，以确定它是否为最新版本。

如果有策略违规，建议操作会显示如何将您的基础镜像版本更新到最新版本，同时将基础镜像版本固定到特定摘要。有关更多信息，请参阅 [固定基础镜像版本](/manuals/build/building/best-practices.md#pin-base-image-versions)。

### 启用 GitHub 集成

如果您在 GitHub 上托管镜像的源代码，可以启用 [GitHub 集成](../integrations/source-code-management/github.md)。此集成使 Docker Scout 能够提供更有用的修复建议，并允许您直接从 Docker Scout 仪表板启动违规修复。

启用 GitHub 集成后，您可以使用修复侧边栏在镜像的 GitHub 仓库中发起拉取请求。拉取请求会自动在您的 Dockerfile 中将基础镜像版本更新到最新版本。

这种自动修复会将您的基础镜像固定到特定摘要，同时帮助您在新版本可用时保持最新。将基础镜像固定到摘要是确保可重现性的重要步骤，有助于避免不需要的更改进入您的供应链。

有关基础镜像固定化的更多信息，请参阅 [固定基础镜像版本](/manuals/build/building/best-practices.md#pin-base-image-versions)。

<!--
  TODO(dvdksn): no support for the following, yet

  启用 GitHub 集成还允许 Docker Scout 在 Docker Scout 仪表板中可视化修复工作流。从拉取请求被提出到镜像被部署到环境的每一步，都会在检查镜像时显示在修复侧边栏中。

  https://github.com/docker/docs/pull/18961#discussion_r1447189475
-->

## 供应链证明 修复

默认的 **供应链证明** 策略要求镜像具有完整的可信证明和 SBOM 证明。如果您的镜像缺少证明，或者证明不包含足够的信息，策略就会被违反。

修复侧边栏中可用的建议有助于指导您采取必要的行动来解决问题。例如，如果您的镜像具有可信证明，但证明不包含足够的信息，建议您使用 [`mode=max`](/manuals/build/metadata/attestations/slsa-provenance.md#max) 可信证明重新构建您的镜像。