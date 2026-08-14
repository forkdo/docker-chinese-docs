---
aliases:
  - /dhi/core-concepts/signatures/
title: Code signing（代码签名）
description: 了解 Docker Hardened Images 如何使用 Cosign 进行加密签名，以验证真实性、完整性和安全来源。
keywords: container image signing, cosign docker image, verify image signature, signed container image, sigstore cosign
---

## What is code signing?（什么是代码签名？）

代码签名是对软件制品（例如 Docker 镜像）应用加密签名的过程，用于验证其完整性和真实性。通过对镜像签名，你可以确保镜像自签名以来未被篡改，并且来自受信任的来源。

在 Docker Hardened Images（DHI）的语境下，代码签名是通过 [Cosign](https://docs.sigstore.dev/) 实现的，这是一个由 Sigstore 项目开发的工具。Cosign 支持对容器镜像进行安全且可验证的签名，增强了软件供应链中的信任与安全性。

## Why is code signing important?（为何代码签名很重要？）

代码签名在现代软件开发和网络安全中扮演着关键角色：

- 真实性（Authenticity）：验证镜像是否由受信任的来源创建。
- 完整性（Integrity）：确保镜像自签名以来未被篡改。
- 合规性（Compliance）：有助于满足法规和组织的安全要求。

## Docker Hardened Image code signing（Docker Hardened Image 代码签名）

每个 DHI 都使用 Cosign 进行加密签名，确保镜像未被篡改且来自受信任的来源。

## Why sign your own images?（为何要对自己的镜像签名？）

Docker Hardened Images 由 Docker 签名以证明其来源和完整性，但如果你正在构建以 DHI 为基础镜像或扩展 DHI 的应用程序镜像，你也应该对自己的镜像进行签名。

通过对自己的镜像签名，你可以：

- 证明镜像由你的团队或流水线构建
- 确保镜像在推送后未被篡改
- 支持 SLSA 等软件供应链框架
- 在部署工作流中启用镜像验证

这在你频繁构建和推送镜像的 CI/CD 环境中，或任何镜像来源必须可审计的场景中尤为重要。

## How to view and use code signatures（如何查看和使用代码签名）

### View signatures（查看签名）

你可以使用 Docker Scout 或 Cosign 验证 Docker Hardened Image 是否已签名且可信。

要列出附加到镜像的所有证明（包括签名元数据），请使用以下命令：

```console
$ docker scout attest list <image-name>:<tag>
```

> [!NOTE]
>
> 如果镜像存在于你设备的本地，必须在镜像名称前加上 `registry://` 前缀。例如，使用
> `registry://dhi.io/python` 而不是 `dhi.io/python`。

要验证特定的已签名证明（例如 SBOM、VEX、provenance）：

```console
$ docker scout attest get \
  --predicate-type <predicate-uri> \
  --verify \
  <image-name>:<tag>
```

> [!NOTE]
>
> 如果镜像存在于你设备的本地，必须在镜像名称前加上 `registry://` 前缀。例如，使用
> `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

例如：

```console
$ docker scout attest get \
  --predicate-type https://openvex.dev/ns/v0.2.0 \
  --verify \
  dhi.io/python:3.13
```

如果有效，Docker Scout 将确认签名并显示签名载荷，以及用于验证镜像的等效 Cosign 命令。

### Sign images（对镜像签名）

要对 Docker 镜像签名，请使用 [Cosign](https://docs.sigstore.dev/)。将 `<image-name>:<tag>` 替换为镜像名称和标签。

```console
$ cosign sign <image-name>:<tag>
```

该命令会提示你通过 OIDC 提供商（例如 GitHub、Google 或 Microsoft）进行身份验证。身份验证成功后，Cosign 将生成短期证书并对镜像签名。该签名将存储在透明日志（transparency log）中，并与仓库中的镜像关联。
