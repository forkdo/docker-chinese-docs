---
title: Policy Evaluation
linkTitle: 策略评估
weight: 70
keywords: scout, supply chain, vulnerabilities, packages, cves, policy
description: |
  Docker Scout 中的策略评估让您能够为制品定义供应链规则，
  并评估镜像的合规性
---

Docker Scout 中的策略评估让您能够为制品定义供应链规则，并使用 `docker scout policy` 命令评估合规性。您可以在本地、CI 流水线中运行评估，也可以使用自定义 Rego 策略或 OCI 包 (bundles)。请参阅[评估策略](./local.md)。

## 策略评估的工作原理

当您运行 `docker scout policy` 时，CLI 会将镜像编入 SBOM 并用 CVE 和 VEX 数据对其进行丰富。然后它会针对这些数据在进程内评估每个已配置的策略。不会向 Scout 服务发送任何数据，大多数使用场景也不需要组织。

策略定义了您的制品应满足的镜像质量标准。例如，**No copyleft licenses** 策略会标记任何包含根据 Copyleft 许可证分发的软件包的镜像。如果一个镜像包含这样的软件包，它就不符该策略。

## 策略类型

Docker Scout 包含以下内置策略类型：

- [基于严重性的漏洞](#severity-based-vulnerability)
- [合规许可证](#compliant-licenses)
- [最新的基础镜像](#up-to-date-base-images)
- [高关注度漏洞](#high-profile-vulnerabilities)
- [供应链证明](#supply-chain-attestations)
- [默认非 root 用户](#default-non-root-user)
- [批准的基础镜像](#approved-base-images)

每种策略类型的配置选项，请参阅[评估策略](./local.md#configure-built-in-policies)。

<!-- vale Docker.HeadingSentenceCase = NO -->

### Severity-Based Vulnerability

**基于严重性的漏洞** 策略类型检查您的制品是否暴露于已知漏洞。默认情况下，它会标记存在修复版本的关键和高危漏洞。

可配置参数包括严重级别、针对新披露 CVE 的宽限期、仅可修复过滤以及软件包类型过滤。

### Compliant Licenses

**合规许可证** 策略类型检查您的镜像是否包含在不适当许可证下分发的软件包。您可以配置要标记的许可证列表，并添加软件包级别的例外。

### Up-to-Date Base Images

**最新的基础镜像** 策略类型检查您使用的基础镜像是否为最新版本。如果用于构建的标签指向的摘要与您正在使用的摘要不同，则该镜像不符合要求。

您的镜像需要来源证明 (provenance attestations) 才能成功评估此策略。更多信息，请参阅[无基础镜像数据](#no-base-image-data)。

### High-Profile Vulnerabilities

**高关注度漏洞** 策略类型检查您的镜像是否包含来自[精心筛选的、被广泛认可的高影响力 CVE 列表](./local.md#default-high-profile-cves)，包括 Log4Shell、Spring4Shell 和 XZ 后门。随着新的高关注度漏洞被披露，该列表会持续更新。

您可以配置哪些 CVE 被视为高关注度，并启用对 CISA 已知被利用漏洞 (Known Exploited Vulnerabilities) 目录的跟踪。

### Supply Chain Attestations

**供应链证明** 策略类型检查您的镜像是否具有 [SBOM](/manuals/build/metadata/attestations/sbom.md) 和[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。如果镜像缺少其中任何一种证明，则不符合要求。

为确保合规，请使用证明进行构建：

```console
$ docker buildx build --provenance=true --sbom=true -t <IMAGE> --push .
```

### Default Non-Root User

**默认非 root 用户** 策略类型检测配置为以 `root` 用户身份运行的镜像。请使用
[`USER`](/reference/dockerfile.md#user) Dockerfile 指令为运行时阶段设置一个
非 root 的默认用户。

### Approved Base Images

**批准的基础镜像** 策略类型确保您使用的基础镜像与可配置的 glob 模式允许列表相匹配。如果基础镜像引用与任何允许的模式都不匹配，则该镜像不符合要求。

您的镜像需要来源证明才能成功评估此策略。更多信息，请参阅[无基础镜像数据](#no-base-image-data)。

<!-- vale Docker.HeadingSentenceCase = YES -->

## No base image data

**最新的基础镜像** 和 **批准的基础镜像** 策略需要来源证明来确定您构建中使用的基础镜像。如果没有它们，这些策略将报告 **无数据**。

为确保 Docker Scout 始终拥有基础镜像信息，请在构建时附加来源证明：

```console
$ docker buildx build --provenance=true -t <IMAGE> --push .
```

## Policies page in the Dashboard

> [!IMPORTANT]
>
> `docker scout policy` 命令将策略评估直接带到您的 CLI，使您能够在本地、CI 中或使用自定义策略评估任意镜像，而无需 Dashboard。Dashboard 中的 Policies 页面已弃用，并将于 2026 年 9 月 1 日停止服务。请参阅[评估策略](./local.md)。

Docker Scout Dashboard 此前提供了一个可视化界面，用于跟踪您组织镜像的策略合规性。请参阅[使用 Dashboard 中的 Policies 页面](./dashboard.md)。
