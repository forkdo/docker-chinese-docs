---
title: 证明
keywords: build, attestations, sbom, provenance, metadata
description: |
  介绍 SBOM 和来源证明的基础知识，以及它们在 Docker Build 中的应用
weight: 50
---

{{< youtube-embed qOzcycbTs4o >}}

[构建证明](/manuals/build/metadata/attestations/_index.md) 为您提供有关镜像构建方式及其内容的详细信息。这些证明由 BuildKit 在构建时生成，并作为元数据附加到最终镜像上，使您能够检查镜像的来源、创建者和内容。这些信息帮助您对镜像的安全性和对供应链的影响做出明智的决策。

Docker Scout 使用这些证明来评估镜像的安全性和供应链状况，并提供问题修复建议。如果检测到问题（例如缺少或过时的证明），Docker Scout 可以指导您如何添加或更新它们，确保合规性并提高镜像安全状态的可见性。

有两种关键类型的证明：

- SBOM，列出镜像中的软件制品。
- 来源证明，详细说明镜像是如何构建的。

您可以使用 `docker buildx build` 命令并配合 `--provenance` 和 `--sbom` 标志来创建证明。证明会附加到镜像索引上，允许您在不拉取整个镜像的情况下检查它们。Docker Scout 利用这些元数据为您提供更精确的建议，并更好地控制镜像的安全性。

<div id="scout-lp-survey-anchor"></div>