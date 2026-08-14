---
aliases:
  - /dhi/core-concepts/fips/
title: FIPS
description: 了解 Docker Hardened Images 如何通过经过验证的加密模块支持 FIPS 140，从而帮助组织满足合规要求。
keywords: docker fips, fips 140 images, fips docker images, docker compliance, secure container images
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

## What is FIPS 140?（什么是 FIPS 140？）

[FIPS 140](https://csrc.nist.gov/publications/detail/fips/140/3/final) 是美国政府制定的标准，定义了用于保护敏感信息的加密模块的安全要求。它被广泛应用于政府、医疗和金融服务等受监管的环境中。

FIPS 认证由 [NIST Cryptographic Module Validation Program（CMVP，加密模块验证计划）](https://csrc.nist.gov/projects/cryptographic-module-validation-program) 管理，该计划确保加密模块满足严格的安全标准。

## Why FIPS compliance matters（为何 FIPS 合规很重要）

在许多必须保护敏感数据的受监管环境中（如政府、医疗、金融和国防），FIPS 140 合规是必需或强烈推荐的。这些标准确保加密操作使用经过审查、受信任的算法，并在安全的模块中实现。

使用依赖经过验证的加密模块的软件组件，可以帮助组织：

- 满足联邦和行业强制要求，例如 FedRAMP，这些要求需要或强烈建议使用经过 FIPS 140 验证的加密技术。
- 证明审计准备度，提供基于标准的安全加密实践的可验证证据。
- 降低安全风险，通过阻止未批准或不安全的算法（例如 MD5），并确保跨环境行为一致。

## How Docker Hardened Images support FIPS compliance（Docker Hardened Images 如何支持 FIPS 合规）

虽然 Docker Hardened Images 面向所有人开放，但 FIPS 变体需要付费的 Docker Hardened Images 订阅。

Docker Hardened Images（DHI）包含使用经过 FIPS 140 验证的加密模块的变体。这些镜像旨在通过整合符合该标准的组件，帮助组织满足合规要求。

- FIPS 镜像变体使用的加密模块已经过 FIPS 140 验证。
- 这些变体由 Docker 构建和维护，以支持具有法规或合规需求的环境。
- Docker 提供已签名的测试证明（attestation），记录经过验证的加密模块的使用情况。这些证明可用于内部审计和合规报告。
- 熵源（用于加密操作的随机数生成）因基础镜像而异。基于 Debian 的镜像使用 OpenSSL 熵源，而基于 Alpine 的镜像则从宿主机内核获取熵。

> [!NOTE]
>
> 使用 FIPS 镜像变体有助于满足合规要求，但并不能使应用程序或系统完全合规。合规性取决于镜像在更大系统中如何被集成和使用。

## Identify images that support FIPS（识别支持 FIPS 的镜像）

支持 FIPS 的 Docker Hardened Images 在 Docker Hardened Images 目录中标记为 **FIPS** 合规。

要查找带有 FIPS 镜像变体的 DHI 仓库，请[搜索目录](../../how-to/search-evaluate.md)并：

- 使用目录页面上的 **FIPS** 筛选器
- 在单个镜像列表中查找 **FIPS** 合规标识

这些标识可帮助你快速定位支持基于 FIPS 的合规需求的仓库。包含 FIPS 支持的镜像变体将带有以 `-fips` 结尾的标签，例如 `3.13-fips`。

## Use a FIPS variant（使用 FIPS 变体）

要使用 FIPS 变体，你必须先[镜像](../../how-to/mirror.md)该仓库，然后从你镜像的仓库中拉取 FIPS 镜像。

## View the FIPS attestation（查看 FIPS 证明）

Docker Hardened Images 的 FIPS 变体包含一个 FIPS 证明，其中列出了镜像中包含的实际加密模块。

你可以使用 Docker Scout CLI 检索并检查 FIPS 证明：

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
