---
aliases:
  - /dhi/core-concepts/sbom/
title: Software Bill of Materials (SBOMs)（软件物料清单）
linktitle: SBOMs
description: 了解什么是 SBOM、为何重要，以及 Docker Hardened Images 如何包含已签名的 SBOM 以支持透明度和合规性。
keywords: sbom docker image, software bill of materials, signed sbom, container sbom verification, sbom compliance
---

## What is an SBOM?（什么是 SBOM？）

SBOM 是一份详细清单，列出了构建软件应用程序所使用的所有组件、库和依赖项。它通过记录每个组件的版本、来源以及与其他组件的关系，提供对软件供应链的透明度。可以将其视为软件的“配方”，详细列出每种成分以及它们如何组合在一起。

SBOM 中为描述软件制品而包含的元数据可能有：

- 制品名称
- 版本
- 许可证类型
- 作者
- 唯一的包标识符

## Why are SBOMs important?（为何 SBOM 很重要？）

在当今的软件格局中，应用程序通常由来自各种来源的众多组件构成，包括开源库、第三方服务和专有代码。这种复杂性可能掩盖对潜在漏洞的可见性，并使合规工作复杂化。SBOM 通过提供应用程序内所有组件的详细清单来应对这些挑战。


SBOM 的重要性由几个关键因素凸显：

- 增强透明度：SBOM 全面展示了构成应用程序的所有组件，使组织能够识别并评估与第三方库和依赖项相关的风险。

- 主动的漏洞管理：通过维护最新的 SBOM，组织可以迅速识别并解决软件组件中的漏洞，缩短面临潜在漏洞利用的暴露窗口。

- 法规合规：许多法规和行业标准现在要求组织控制其使用的软件组件。SBOM 通过提供清晰且可访问的记录来促进合规。

- 改进的事件响应：在发生安全漏洞时，SBOM 使组织能够快速识别受影响的组件并采取适当措施，将潜在损害降至最低。

## Docker Hardened Image SBOMs（Docker Hardened Image 的 SBOM）

Docker Hardened Images 带有 SBOM，确保镜像中的每个组件都有文档且可验证。这些 SBOM 经过加密签名，提供镜像内容的防篡改记录。这种集成简化了审计并增强了对软件供应链的信任。

## View SBOMs in Docker Hardened Images（在 Docker Hardened Images 中查看 SBOM）

要查看 Docker Hardened Image 的 SBOM，你可以使用 `docker scout sbom` 命令。将 `<image-name>:<tag>` 替换为镜像名称和标签。

```console
$ docker scout sbom dhi.io/<image-name>:<tag>
```

## Verify the SBOM of a Docker Hardened Image（验证 Docker Hardened Image 的 SBOM）

由于 Docker Hardened Images 附带已签名的 SBOM，你可以使用 Docker Scout 验证附加到镜像的 SBOM 的真实性和完整性。这确保了 SBOM 未被篡改，并且镜像内容是可信的。

要使用 Docker Scout 验证 Docker Hardened Image 的 SBOM，请使用以下命令：

```console
$ docker scout attest get dhi.io/<image-name>:<tag> \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify --platform <platform>
```

例如，要验证 `node:20.19-debian12` 镜像的 SBOM 证明：

```console
$ docker scout attest get dhi.io/node:20.19-debian12 \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify --platform linux/amd64
```

## Resources（资源）

有关 SBOM 证明和 Docker Build 的更多详细信息，请参阅 [SBOM attestations](/build/metadata/attestations/sbom/)。

要了解有关 Docker Scout 和处理 SBOM 的更多信息，请参阅 [Docker Scout SBOMs](../../../scout/how-tos/view-create-sboms.md)。
