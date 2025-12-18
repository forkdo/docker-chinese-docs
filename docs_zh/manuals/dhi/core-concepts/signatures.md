---
title: 代码签名
description: 了解 Docker Hardened Images 如何使用 Cosign 进行加密签名，以验证其真实性、完整性和安全来源。
keywords: 容器镜像签名, cosign docker 镜像, 验证镜像签名, 已签名容器镜像, sigstore cosign
---

## 什么是代码签名？

代码签名是为软件制品（如 Docker 镜像）应用加密签名的过程，用于验证其完整性和真实性。通过对镜像签名，您可以确保它自签名以来未被篡改，并且来自可信来源。

在 Docker Hardened Images (DHI) 的上下文中，代码签名通过 [Cosign](https://docs.sigstore.dev/) 实现，这是由 Sigstore 项目开发的工具。Cosign 能够安全且可验证地为容器镜像签名，增强软件供应链的信任和安全性。

## 为什么代码签名很重要？

代码签名在现代软件开发和网络安全中起着关键作用：

- 真实性：验证镜像由可信来源创建。
- 完整性：确保镜像自签名后未被篡改。
- 合规性：帮助满足监管和组织安全要求。

## Docker Hardened Image 代码签名

每个 DHI 都使用 Cosign 进行加密签名，确保镜像未被篡改且来自可信来源。

## 为什么要签名您自己的镜像？

Docker Hardened Images 由 Docker 签名以证明其来源和完整性，但如果您正在构建扩展或使用 DHI 作为基础的应用镜像，您也应该为您自己的镜像签名。

通过为您自己的镜像签名，您可以：

- 证明镜像由您的团队或流水线构建
- 确保构建在推送后未被篡改
- 支持 SLSA 等软件供应链框架
- 在部署工作流中启用镜像验证

这在频繁构建和推送镜像的 CI/CD 环境中尤其重要，或在任何需要可审计镜像来源的场景中。

## 如何查看和使用代码签名

### 查看签名

您可以使用 Docker Scout 或 Cosign 验证 Docker Hardened Image 是否已签名且可信。

要列出附加到镜像的所有证明（包括签名元数据），请使用以下命令：

```console
$ docker scout attest list <image-name>:<tag>
```

> [!NOTE]
>
> 如果镜像存在于您的本地设备上，您必须在镜像名称前加上 `registry://`。例如，使用
> `registry://dhi.io/python` 而不是 `dhi.io/python`。

要验证特定的已签名证明（例如 SBOM、VEX、来源）：

```console
$ docker scout attest get \
  --predicate-type <predicate-uri> \
  --verify \
  <image-name>:<tag>
```

> [!NOTE]
>
> 如果镜像存在于您的本地设备上，您必须在镜像名称前加上 `registry://`。例如，使用
> `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

例如：

```console
$ docker scout attest get \
  --predicate-type https://openvex.dev/ns/v0.2.0 \
  --verify \
  dhi.io/python:3.13
```

如果有效，Docker Scout 将确认签名并显示签名载荷，以及验证镜像的等效 Cosign 命令。

### 签名镜像

要为 Docker 镜像签名，请使用 [Cosign](https://docs.sigstore.dev/)。将 `<image-name>:<tag>` 替换为镜像名称和标签。

```console
$ cosign sign <image-name>:<tag>
```

此命令将提示您通过 OIDC 提供商（如 GitHub、Google 或 Microsoft）进行身份验证。成功认证后，Cosign 将生成一个短期证书并为镜像签名。签名将存储在透明度日志中并与注册表中的镜像关联。