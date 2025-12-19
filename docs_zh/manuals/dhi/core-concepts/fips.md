---
title: 'FIPS <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>'
linkTitle: FIPS
description: 了解 Docker Hardened Images 如何通过经验证的加密模块支持 FIPS 140，以帮助组织满足合规要求。
keywords: docker fips, fips 140 images, fips docker images, docker compliance, secure container images
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

## 什么是 FIPS 140？

[FIPS 140](https://csrc.nist.gov/publications/detail/fips/140/3/final) 是一项美国政府标准，用于定义保护敏感信息的加密模块的安全要求。它广泛应用于政府、医疗保健和金融服务等受监管的环境。

FIPS 认证由 [NIST 加密模块验证计划 (CMVP)](https://csrc.nist.gov/projects/cryptographic-module-validation-program) 管理，该计划确保加密模块符合严格的安全标准。

## 为什么 FIPS 合规性很重要

在许多受监管的环境中，例如政府、医疗保健、金融和国防领域，FIPS 140 合规性是必需或强烈推荐的，这些环境中的敏感数据必须得到保护。这些标准确保加密操作使用经过审查、可信赖的算法，并在安全的模块中实现。

使用依赖经验证的加密模块的软件组件可以帮助组织：

- 满足联邦和行业法规要求，例如 FedRAMP，它要求或强烈推荐使用 FIPS 140 验证的加密技术。
- 通过可验证的、基于标准的安全加密实践证据，证明已做好审计准备。
- 通过阻止未经批准或不安全的算法（例如 MD5）并确保跨环境行为的一致性，来降低安全风险。

## Docker Hardened Images 如何支持 FIPS 合规性

虽然 Docker Hardened Images 对所有用户开放，但 FIPS 变体需要 Docker Hardened Images Enterprise 订阅。

Docker Hardened Images (DHI) 包含使用经 FIPS 140 验证的加密模块的变体。这些镜像旨在通过整合符合该标准的组件，帮助组织满足合规要求。

- FIPS 镜像变体使用已通过 FIPS 140 验证的加密模块。
- 这些变体由 Docker 构建和维护，以支持具有监管或合规需求的环境。
- Docker 提供签名的测试证明，记录了经验证的加密模块的使用情况。这些证明可以支持内部审计和合规报告。

> [!NOTE]
>
> 使用 FIPS 镜像变体有助于满足合规要求，但并不能使应用程序或系统完全合规。合规性取决于镜像在更广泛的系统中如何被集成和使用。

## 识别支持 FIPS 的镜像

支持 FIPS 的 Docker Hardened Images 在 Docker Hardened Images 目录中被标记为 **FIPS** 合规。

要查找具有 FIPS 镜像变体的 DHI 仓库，请[探索镜像](../how-to/explore.md)并：

- 在目录页面上使用 **FIPS** 筛选器
- 在单个镜像列表中查找 **FIPS** 合规标识

这些指示器可帮助您快速定位支持基于 FIPS 合规需求的仓库。包含 FIPS 支持的镜像变体将有一个以 `-fips` 结尾的标签，例如 `3.13-fips`。

## 使用 FIPS 变体

要使用 FIPS 变体，您必须[镜像](../how-to/mirror.md)该仓库，然后从您的镜像仓库中拉取 FIPS 镜像。

## 查看 FIPS 证明

Docker Hardened Images 的 FIPS 变体包含一个 FIPS 证明，其中列出了镜像中包含的实际加密模块。

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

证明输出是一个 JSON 数组，描述了镜像中包含的加密模块及其合规状态。例如：

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