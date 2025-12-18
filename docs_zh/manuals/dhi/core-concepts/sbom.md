---
title: 软件物料清单 (SBOM)
linktitle: SBOM
description: 了解 SBOM 是什么、为什么重要，以及 Docker Hardened Images 如何包含已签名的 SBOM 以支持透明度和合规性。
keywords: sbom docker image, 软件物料清单, 已签名 sbom, 容器 sbom 验证, sbom 合规性
---

## 什么是 SBOM？

SBOM 是一份详细的清单，列出了构建软件应用程序时使用的所有组件、库和依赖项。它通过记录每个组件的版本、来源及其与其他组件的关系，提供软件供应链的透明度。可以将其视为软件的“配方”，详细说明了每一种“原料”以及它们如何组合在一起。

SBOM 中可能包含用于描述软件制品的元数据有：

- 制品名称
- 版本
- 许可类型
- 作者
- 唯一包标识符

## 为什么 SBOM 很重要？

在当今的软件环境中，应用程序通常由来自不同来源的众多组件组成，包括开源库、第三方服务和专有代码。这种复杂性可能使潜在漏洞的可见性变得模糊，并使合规工作复杂化。SBOM 通过提供应用程序内所有组件的详细清单来解决这些挑战。

SBOM 的重要性体现在以下几个关键因素：

- 增强透明度：SBOM 提供了构成应用程序的所有组件的全面视图，使组织能够识别和评估与第三方库和依赖项相关的风险。

- 主动漏洞管理：通过维护最新的 SBOM，组织可以快速识别和解决软件组件中的漏洞，减少暴露于潜在攻击的时间窗口。

- 监管合规：许多法规和行业标准现在要求组织对其使用的软件组件进行控制。SBOM 通过提供清晰且可访问的记录来促进合规。

- 改进事件响应：在发生安全漏洞时，SBOM 使组织能够快速识别受影响的组件并采取适当行动，将潜在损害降至最低。

## Docker Hardened Image SBOM

Docker Hardened Images 内置了 SBOM，确保镜像中的每个组件都有据可查且可验证。这些 SBOM 经过加密签名，提供了防篡改的镜像内容记录。这种集成为审计提供了便利，并增强了软件供应链的信任度。

## 查看 Docker Hardened Image 中的 SBOM

要查看 Docker Hardened Image 的 SBOM，可以使用 `docker scout sbom` 命令。将 `<image-name>:<tag>` 替换为镜像名称和标签。

```console
$ docker scout sbom dhi.io/<image-name>:<tag>
```

## 验证 Docker Hardened Image 的 SBOM

由于 Docker Hardened Images 附带已签名的 SBOM，您可以使用 Docker Scout 来验证附加到镜像的 SBOM 的真实性和完整性。这确保了 SBOM 未被篡改，镜像内容值得信赖。

要使用 Docker Scout 验证 Docker Hardened Image 的 SBOM，请使用以下命令：

```console
$ docker scout attest get dhi.io/<image-name>:<tag> \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify --platform <platform>
```

例如，验证 `node:20.19-debian12` 镜像的 SBOM 证明：

```console
$ docker scout attest get dhi.io/node:20.19-debian12 \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify --platform linux/amd64
```

## 资源

有关 SBOM 证明和 Docker Build 的更多详细信息，请参阅 [SBOM 证明](/build/metadata/attestations/sbom/)。

要了解有关 Docker Scout 和 SBOM 操作的更多信息，请参阅 [Docker Scout SBOM](../../scout/how-tos/view-create-sboms.md)。