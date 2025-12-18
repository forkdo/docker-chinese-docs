---
title: 'FIPS <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>'
linkTitle: FIPS
description: 了解 Docker Hardened Images 如何通过经过验证的加密模块支持 FIPS 140，帮助组织满足合规要求。
keywords: docker fips, fips 140 images, fips docker images, docker compliance, secure container images
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

## 什么是 FIPS 140？

[FIPS 140](https://csrc.nist.gov/publications/detail/fips/140/3/final) 是美国政府制定的标准，定义了保护敏感信息的加密模块所需满足的安全要求。它在政府、医疗和金融服务等受监管环境中被广泛使用。

FIPS 认证由 [NIST 加密模块验证计划 (CMVP)](https://csrc.nist.gov/projects/cryptographic-module-validation-program) 管理，确保加密模块符合严格的安全标准。

## 为什么 FIPS 合规很重要

在需要保护敏感数据的许多受监管环境中，例如政府、医疗、金融和国防领域，FIPS 140 合规是必需的或被强烈推荐的。这些标准确保加密操作使用经过审查、受信任的算法，并在安全模块中实现。

使用依赖经过验证的加密模块的软件组件可以帮助组织：

- 满足联邦和行业法规要求，例如 FedRAMP，这些要求需要或强烈建议使用 FIPS 140 验证的加密技术。
- 展示审计就绪性，提供基于标准的加密实践的可验证证据。
- 降低安全风险，通过阻止未批准或不安全的算法（例如 MD5），确保在不同环境中行为一致。

## Docker Hardened Images 如何支持 FIPS 合规

虽然 Docker Hardened Images 对所有用户可用，但 FIPS 变体需要 Docker Hardened Images Enterprise 订阅。

Docker Hardened Images (DHI) 包含使用 FIPS 140 下已验证加密模块的变体。这些镜像旨在通过集成符合标准的组件，帮助组织满足合规要求。

- FIPS 镜像变体使用已在 FIPS 140 下验证的加密模块。
- 这些变体由 Docker 构建和维护，以支持具有监管或合规需求的环境。
- Docker 提供签名测试证明，记录使用已验证的加密模块。这些证明可用于支持内部审计和合规报告。

> [!NOTE]
>
> 使用 FIPS 镜像变体有助于满足合规要求，但不会使应用程序或系统完全合规。合规性取决于镜像在更广泛系统中的集成和使用方式。

## 识别支持 FIPS 的镜像

在 Docker Hardened Images 目录中，支持 FIPS 的 Docker Hardened Images 被标记为 **FIPS** 合规。

要查找支持 FIPS 镜像变体的 DHI 仓库，请[浏览镜像](../how-to/explore.md)并：

- 在目录页面上使用 **FIPS** 筛选器
- 在单个镜像列表中查找 **FIPS** 合规标识

这些标识可帮助您快速定位支持 FIPS 合规需求的仓库。包含 FIPS 支持的镜像变体将具有以 `-fips` 结尾的标签，例如 `3.13-fips`。

## 使用 FIPS 变体

要使用 FIPS 变体，您必须[镜像](../how-to/mirror.md)仓库，然后从您的镜像仓库中拉取 FIPS 镜像。

## 查看 FIPS 证明

Docker Hardened Images 的 FIPS 变体包含一份 FIPS 证明，列出镜像中包含的实际加密模块。

您可以使用 Docker Scout CLI 检索和检查 FIPS 证明：

```console
$ docker scout attest get \
  --predicate-type https://docker.com/dhi/fips/v0.1 \
  --predicate \
  dhi.io/<image>:<tag>
```

例如：

```console
$ docker scout attest get \
  --predicate-type https://docker.com/dhi/fips/v0.1 \
  --predicate \
  dhi.io/python:3.13-fips
```

证明输出是一个 JSON 数组，描述镜像中包含的加密模块及其合规状态。例如：

```json
[
  {
    "certification": "CMVP #4985",
    "certificationUrl": "https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4985",
    "name": "OpenSSL FIPS Provider",
    "package": "pkg:dhi/openssl-provider-fips@3.1.2",
    "standard": "FIPS 140-3",
    "status": "active",
    "sunsetDate": "2030-03-10",
    "version": "3.1.2"
  }
]
```