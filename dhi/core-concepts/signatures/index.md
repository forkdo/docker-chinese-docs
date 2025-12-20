# 代码签名

## 什么是代码签名？

代码签名是对软件制品（如 Docker 镜像）应用加密签名的过程，用于验证其完整性和真实性。通过对镜像进行签名，您可以确保自签名以来镜像未被篡改，并且来自可信来源。

在 Docker Hardened Images (DHIs) 的上下文中，代码签名使用 [Cosign](https://docs.sigstore.dev/) 实现，这是由 Sigstore 项目开发的一个工具。Cosign 支持对容器镜像进行安全且可验证的签名，从而增强软件供应链中的信任和安全性。

## 为什么代码签名很重要？

代码签名在现代软件开发和网络安全中起着至关重要的作用：

- 真实性：验证镜像是否由可信来源创建。
- 完整性：确保自签名以来镜像未被篡改。
- 合规性：有助于满足监管和组织的安全要求。

## Docker Hardened Image 代码签名

每个 DHI 都使用 Cosign 进行加密签名，确保镜像未被篡改，并且来自可信来源。

## 为什么需要对自己的镜像进行签名？

Docker Hardened Images 由 Docker 签名以证明其来源和完整性，但如果您正在构建基于或使用 DHIs 作为基础的应用程序镜像，您也应该对自己的镜像进行签名。

通过对自己的镜像进行签名，您可以：

- 证明镜像是由您的团队或流水线构建的
- 确保推送后构建未被篡改
- 支持像 SLSA 这样的软件供应链框架
- 在部署工作流中启用镜像验证

在频繁构建和推送镜像的 CI/CD 环境中，或在任何需要审计镜像来源的场景中，这尤其重要。

## 如何查看和使用代码签名

### 查看签名

您可以使用 Docker Scout 或 Cosign 验证 Docker Hardened Image 是否已签名并受信任。

要列出附加到镜像的所有证明（包括签名元数据），请使用以下命令：

```console
$ docker scout attest list <image-name>:<tag>
```

> [!NOTE]
>
> 如果镜像存在于您的设备上，您必须在镜像名称前加上 `registry://`。例如，使用
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
> 如果镜像存在于您的设备上，您必须在镜像名称前加上 `registry://`。例如，使用
> `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

例如：

```console
$ docker scout attest get \
  --predicate-type https://openvex.dev/ns/v0.2.0 \
  --verify \
  dhi.io/python:3.13
```

如果有效，Docker Scout 将确认签名并显示签名有效载荷，以及用于验证镜像的等效 Cosign 命令。

### 签名镜像

要对 Docker 镜像进行签名，请使用 [Cosign](https://docs.sigstore.dev/)。将 `<image-name>:<tag>` 替换为镜像名称和标签。

```console
$ cosign sign <image-name>:<tag>
```

此命令将提示您通过 OIDC 提供商（如 GitHub、Google 或 Microsoft）进行身份验证。成功验证后，Cosign 将生成一个短期证书并签署镜像。签名将存储在透明日志中，并与注册表中的镜像关联。
