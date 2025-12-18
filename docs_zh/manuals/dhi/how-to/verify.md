---
title: 验证 Docker Hardened 镜像或图表
linktitle: 验证镜像或图表
description: 使用 Docker Scout 或 cosign 验证 Docker Hardened 镜像和图表的签名声明，例如 SBOM、来源和漏洞数据。
weight: 40
keywords: 验证容器镜像, docker scout attest, cosign verify, sbom 验证, 已签名容器声明, helm 图表验证
---

Docker Hardened Images (DHI) 和图表包含签名声明，用于验证构建过程、内容和安全状况。这些声明适用于每个镜像变体和图表，可以使用 [cosign](https://docs.sigstore.dev/) 或 Docker Scout CLI 进行验证。

Docker 用于 DHI 镜像和图表的公钥发布在：

- https://registry.scout.docker.com/keyring/dhi/latest.pub
- https://github.com/docker-hardened-images/keyring

> [!IMPORTANT]
>
> 您必须登录到 Docker Hardened Images 镜像仓库（`dhi.io`）才能拉取镜像。使用您的 Docker ID 凭据（与 Docker Hub 相同的用户名和密码）登录。如果您没有 Docker 账户，请[免费创建一个](../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

## 使用 Docker Scout 验证镜像声明

您可以使用 [Docker Scout](/scout/) CLI 列出和检索 Docker Hardened Images 的声明。

> [!NOTE]
>
> 在运行 `docker scout attest` 命令之前，请确保您本地拉取的任何镜像都与远程镜像保持最新。您可以通过运行 `docker pull` 来实现这一点。如果不这样做，您可能会看到 `No attestation found`。

### 为什么使用 Docker Scout 而不是直接使用 cosign？

虽然您可以使用 cosign 手动验证声明，但 Docker Scout CLI 在处理 Docker Hardened Images 和图表时具有以下关键优势：

- 专用体验：Docker Scout 了解 DHI 声明和命名约定的结构，因此您无需手动构造完整的摘要或 URI。

- 自动平台解析：使用 Scout，您可以指定平台（例如 `--platform linux/amd64`），它会自动验证正确的镜像变体。而 cosign 要求您自己查找摘要。

- 人类可读的摘要：Scout 返回声明内容的摘要（例如包数量、来源步骤），而 cosign 仅返回原始签名验证输出。

- 一步验证：`docker scout attest get` 中的 `--verify` 标志验证声明并显示等效的 cosign 命令，使您更容易理解幕后发生的事情。

- 与 Docker Hub 和 DHI 信任模型集成：Docker Scout 与 Docker 的声明基础设施和公钥环紧密集成，确保兼容性并简化 Docker 生态系统内用户的验证。

简而言之，Docker Scout 简化了验证过程，减少了人为错误的可能性，同时仍然为您提供完整的可见性，并在需要时可以选择回退到 cosign。

### 列出可用的声明

要列出镜像化的 DHI 镜像的声明：

> [!NOTE]
>
> 如果镜像存在于您设备上的本地，您必须在镜像名称前加上 `registry://` 前缀。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

```console
$ docker scout attest list dhi.io/<image>:<tag>
```

此命令显示所有可用的声明，包括 SBOM、来源、漏洞报告等。

### 检索特定声明

要检索特定声明，请使用 `--predicate-type` 标志和完整的断言类型 URI：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/<image>:<tag>
```

> [!NOTE]
>
> 如果镜像存在于您设备上的本地，您必须在镜像名称前加上 `registry://` 前缀。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

例如：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/python:3.13
```

仅检索断言体：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --predicate \
  dhi.io/<image>:<tag>
```

例如：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --predicate \
  dhi.io/python:3.13
```

### 使用 Docker Scout 验证声明

要使用 Docker Scout 验证声明，您可以使用 `--verify` 标志：

```console
$ docker scout attest get dhi.io/<image>:<tag> \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

> [!NOTE]
>
> 如果镜像存在于您设备上的本地，您必须在镜像名称前加上 `registry://` 前缀。例如，使用 `registry://dhi.io/node:20.19-debian12` 而不是 `dhi.io/node:20.19-debian12`。

例如，验证 `dhi.io/node:20.19-debian12` 镜像的 SBOM 声明：

```console
$ docker scout attest get dhi.io/node:20.19-debian12 \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

#### 处理缺失的透明度日志条目

使用 `--verify` 时，您有时可能会看到如下错误：

```text
ERROR no matching signatures: signature not found in transparency log
```

这是因为 Docker Hardened Images 并不总是将声明记录在公共 [Rekor](https://docs.sigstore.dev/logging/overview/) 透明度日志中。在某些情况下，如果声明包含私人用户信息（例如，您组织的镜像引用中的命名空间），将其写入 Rekor 将公开该信息。

即使 Rekor 条目缺失，声明仍然使用 Docker 的公钥签名，并且可以通过跳过 Rekor 透明度日志检查来离线验证。

要跳过透明度日志检查并针对 Docker 的密钥验证，请使用 `--skip-tlog` 标志：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/<image>:<tag> \
  --verify --skip-tlog
```

> [!NOTE]
>
> `--skip-tlog` 标志仅在 Docker Scout CLI 版本 1.18.2 及更高版本中可用。
>
> 如果镜像存在于您设备上的本地，您必须在镜像名称前加上 `registry://` 前缀。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

这等同于使用 `cosign` 和 `--insecure-ignore-tlog=true` 标志，它针对 Docker 发布的公钥验证签名，但忽略透明度日志检查。

### 显示等效的 cosign 命令

使用 `--verify` 标志时，它还会打印相应的 [cosign](https://docs.sigstore.dev/) 命令来验证镜像签名：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --verify \
  dhi.io/<image>:<tag>
```

> [!NOTE]
>
> 如果镜像存在于您设备上的本地，您必须在镜像名称前加上 `registry://` 前缀。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

例如：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --verify \
  dhi.io/python:3.13
```

如果验证成功，Docker Scout 会打印完整的 `cosign verify` 命令。

示例输出：

```console
    v SBOM obtained from attestation, 101 packages found
    v Provenance obtained from attestation
    v cosign verify ...
```

> [!IMPORTANT]
>
> 使用 cosign 时，您必须首先登录到 DHI 镜像仓库和 Docker Scout 镜像仓库。
>
> 例如：
>
> ```console
> $ docker login dhi.io
> $ docker login registry.scout.docker.com
> $ cosign verify ...
> ```

## 使用 Docker Scout 验证 Helm 图表声明

Docker Hardened Image Helm 图表包含与容器镜像相同的综合声明。图表的验证过程与镜像相同，使用相同的 Docker Scout CLI 命令。

### 列出可用的图表声明

要列出 DHI Helm 图表的声明：

```console
$ docker scout attest list oci://dhi.io/<chart>:<version>
```

例如，列出 Redis HA 图表的声明：

```console
$ docker scout attest list oci://dhi.io/redis-ha-chart:0.1.0
```

此命令显示所有可用的图表声明，包括 SBOM、来源、漏洞报告等。

### 检索特定图表声明

要从 Helm 图表检索特定声明，请使用 `--predicate-type` 标志和完整的断言类型 URI：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  oci://dhi.io/<chart>:<version>
```

例如：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  oci://dhi.io/redis-ha-chart:0.1.0
```

仅检索断言体：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --predicate \
  oci://dhi.io/<chart>:<version>
```

### 使用 Docker Scout 验证图表声明

要使用 Docker Scout 验证图表声明，请使用 `--verify` 标志：

```console
$ docker scout attest get oci://dhi.io/<chart>:<version> \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

例如，验证 Redis HA 图表的 SBOM 声明：

```console
$ docker scout attest get oci://dhi.io/redis-ha-chart:0.1.0 \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

在需要时，[处理缺失的透明度日志条目](#handle-missing-transparency-log-entries) 中描述的相同 `--skip-tlog` 标志也可以与图表声明一起使用。

## 可用的 DHI 声明

请参阅 [可用声明](../core-concepts/attestations.md#image-attestations) 以获取每个 DHI 镜像的可用声明列表，以及 [Helm 图表声明](../core-concepts/attestations.md#helm-chart-attestations) 以获取每个 DHI 图表的可用声明列表。

## 在 Docker Hub 上探索声明

您还可以在 [浏览镜像变体](./explore.md#view-image-variant-details) 时直观地浏览声明。**声明**部分列出了每个可用声明的：

- 类型（例如 SBOM、VEX）
- 断言类型 URI
- 用于 `cosign` 的摘要引用

这些声明作为 Docker Hardened Image 或图表构建过程的一部分自动生成和签名。