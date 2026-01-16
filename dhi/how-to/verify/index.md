---
title: 验证 Docker Hardened 镜像或图表
url: /dhi/how-to/verify/
parent:
  title: 操作指南
  url: /dhi/how-to/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Hardened Images
    url: /dhi/
  - title: 操作指南
    url: /dhi/how-to/
  - title: 验证 Docker Hardened 镜像或图表
    url: /dhi/how-to/verify/
next:
  title: 对比 Docker Hardened 镜像
  url: /dhi/how-to/compare/
prev:
  title: 扫描 Docker Hardened Images
  url: /dhi/how-to/scan/
---


Docker Hardened 镜像 (DHI) 和图表包含签名证明，用于验证构建过程、内容和安全态势。这些证明可用于每个镜像变体和图表，并且可以使用 [cosign](https://docs.sigstore.dev/) 或 Docker Scout CLI 进行验证。

Docker 用于 DHI 镜像和图表的公钥发布在以下位置：

- https://registry.scout.docker.com/keyring/dhi/latest.pub
- https://github.com/docker-hardened-images/keyring

> [!IMPORTANT]
>
> 您必须对 Docker Hardened 镜像注册表 (`dhi.io`) 进行身份验证才能拉取镜像。登录时请使用您的 Docker ID 凭据（与您用于 Docker Hub 的用户名和密码相同）。如果您没有 Docker 账户，请免费[创建一个](../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

## 使用 Docker Scout 验证镜像证明

您可以使用 [Docker Scout](/scout/) CLI 列出和检索 Docker Hardened 镜像的证明。

> [!NOTE]
>
> 在运行 `docker scout attest` 命令之前，请确保您本地拉取的任何镜像都与远程镜像保持同步。您可以通过运行 `docker pull` 来实现这一点。如果您不这样做，可能会看到 `No attestation found`。

### 为什么使用 Docker Scout 而不是直接使用 cosign？

虽然您可以使用 cosign 手动验证证明，但 Docker Scout CLI 在处理 Docker Hardened 镜像和图表时提供了几个关键优势：

- **专为 DHI 设计**：Docker Scout 理解 DHI 证明的结构和命名约定，因此您无需手动构造完整的摘要或 URI。
- **自动平台解析**：使用 Scout，您可以指定平台（例如 `--platform linux/amd64`），它会自动验证正确的镜像变体。Cosign 需要您自己查找摘要。
- **人类可读的摘要**：Scout 返回证明内容的摘要（例如，软件包数量、来源步骤），而 cosign 仅返回原始签名验证输出。
- **一步验证**：`docker scout attest get` 中的 `--verify` 标志会验证证明并显示等效的 cosign 命令，从而更轻松地理解幕后发生的事情。
- **与 Docker Hub 和 DHI 信任模型集成**：Docker Scout 与 Docker 的证明基础设施和公钥环紧密集成，确保兼容性并简化 Docker 生态系统内用户的验证。

简而言之，Docker Scout 简化了验证过程并减少了人为错误的机会，同时仍然为您提供完全的可见性，并在需要时可以选择回退到 cosign。

### 列出可用证明

要列出镜像的 DHI 镜像的证明：

> [!NOTE]
>
> 如果镜像在您的设备上本地存在，您必须在镜像名称前加上 `registry://`。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

```console
$ docker scout attest list dhi.io/<image>:<tag>
```

此命令显示所有可用的证明，包括 SBOM、来源、漏洞报告等。

### 检索特定证明

要检索特定证明，请使用 `--predicate-type` 标志和完整的谓词类型 URI：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/<image>:<tag>
```

> [!NOTE]
>
> 如果镜像在您的设备上本地存在，您必须在镜像名称前加上 `registry://`。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

例如：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/python:3.13
```

要仅检索谓词主体：

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

### 使用 Docker Scout 验证证明

要使用 Docker Scout 验证证明，您可以使用 `--verify` 标志：

```console
$ docker scout attest get dhi.io/<image>:<tag> \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

> [!NOTE]
>
> 如果镜像在您的设备上本地存在，您必须在镜像名称前加上 `registry://`。例如，使用 `registry://dhi.io/node:20.19-debian12` 而不是 `dhi.io/node:20.19-debian12`。

例如，要验证 `dhi.io/node:20.19-debian12` 镜像的 SBOM 证明：

```console
$ docker scout attest get dhi.io/node:20.19-debian12 \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

#### 处理缺少的透明日志条目

使用 `--verify` 时，有时可能会看到如下错误：

```text
ERROR no matching signatures: signature not found in transparency log
```

这是因为 Docker Hardened 镜像并不总是将证明记录在公共的 [Rekor](https://docs.sigstore.dev/logging/overview/) 透明日志中。在证明可能包含私有用户信息的情况下（例如，镜像引用中您组织的命名空间），将其写入 Rekor 会公开该信息。

即使缺少 Rekor 条目，证明仍然使用 Docker 的公钥签名，并且可以通过跳过 Rekor 透明日志检查进行离线验证。

要跳过透明日志检查并根据 Docker 的密钥进行验证，请使用 `--skip-tlog` 标志：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/<image>:<tag> \
  --verify --skip-tlog
```

> [!NOTE]
>
> `--skip-tlog` 标志仅在 Docker Scout CLI 1.18.2 及更高版本中可用。
>
> 如果镜像在您的设备上本地存在，您必须在镜像名称前加上 `registry://`。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

这相当于使用带有 `--insecure-ignore-tlog=true` 标志的 `cosign`，该标志根据 Docker 发布的公钥验证签名，但忽略透明日志检查。

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
> 如果镜像在您的设备上本地存在，您必须在镜像名称前加上 `registry://`。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

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
> 使用 cosign 时，您必须首先对 DHI 注册表和 Docker Scout 注册表进行身份验证。
>
> 例如：
>
> ```console
> $ docker login dhi.io
> $ docker login registry.scout.docker.com
> $ cosign verify ...
> ```

## 使用 Docker Scout 验证 Helm 图表证明

Docker Hardened 镜像 Helm 图表包含与容器镜像相同的全面证明。图表的验证过程与镜像相同，使用相同的 Docker Scout CLI 命令。

### 列出可用的图表证明

要列出 DHI Helm 图表的证明：

```console
$ docker scout attest list dhi.io/<chart>:<version>
```

例如，要列出 external-dns 图表的证明：

```console
$ docker scout attest list dhi.io/external-dns-chart:1.20.0
```

此命令显示所有可用的图表证明，包括 SBOM、来源、漏洞报告等。

### 检索特定的图表证明

要从 Helm 图表中检索特定证明，请使用 `--predicate-type` 标志和完整的谓词类型 URI：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/<chart>:<version>
```

例如：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/external-dns-chart:1.20.0
```

要仅检索谓词主体：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --predicate \
  dhi.io/<chart>:<version>
```

### 使用 Docker Scout 验证图表证明

要使用 Docker Scout 验证图表证明，请使用 `--verify` 标志：

```console
$ docker scout attest get dhi.io/<chart>:<version> \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

例如，要验证 external-dns 图表的 SBOM 证明：

```console
$ docker scout attest get dhi.io/external-dns-chart:1.20.0 \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

在[处理缺少的透明日志条目](#handle-missing-transparency-log-entries)中描述的相同 `--skip-tlog` 标志也可以在需要时用于图表证明。

## 可用的 DHI 证明

有关每个 DHI 图表可用的证明列表，请参阅[可用证明](../core-concepts/attestations.md#image-attestations)和[Helm 图表证明](../core-concepts/attestations.md#helm-chart-attestations)。

## 在 Docker Hub 上探索证明

您还可以在[探索镜像变体](./explore.md#view-image-variant-details)时以可视化方式浏览证明。**证明**部分列出了每个可用的证明及其：

- 类型（例如 SBOM、VEX）
- 谓词类型 URI
- 用于 `cosign` 的摘要引用

这些证明是在 Docker Hardened 镜像或图表构建过程中自动生成并签名的。
