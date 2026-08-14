---
title: 使用加固系统包
linkTitle: 使用加固包
weight: 32
keywords: hardened images, DHI, hardened packages, packages, alpine, apk, debian, apt
description: 了解如何在使用和验证 Docker 的加固系统包。
---

Docker 加固系统包由 Docker 从源代码构建。这通过消除来自可能被入侵的公共软件包的风险，确保整个镜像技术栈的供应链完整性。

对加固包的访问权限因订阅而异：

- **DHI Community**：在基础镜像中包含加固包。可以配置公共软件包仓库以在自定义镜像中访问相同的软件包。
- **DHI Select**：包含全部 Community 软件包，外加通过镜像自定义 UI 访问额外合规相关软件包（例如 FIPS 变体）和 Docker 修补的软件包。
- **DHI Enterprise**：包含全部 Select 软件包，外加能够直接在自己镜像中配置企业软件包仓库，以完整访问合规和安全修补的软件包。

要浏览 Docker 公共加固软件包仓库中当前可用的软件包，请参阅以下索引：

- [Debian 软件包索引](https://dhi.io/deb/debian/main/index.html)
- [Alpine 软件包索引](https://dhi.io/apk/alpine/v3.24/main/index.html)

Docker 不断添加新的加固软件包。如果您需要的软件包尚不可用，可以在 [DHI catalog 仓库中提交请求](https://github.com/docker-hardened-images/catalog/issues)。

## 内置软件包

Docker 加固镜像（DHI）的受支持发行版会自动包含加固系统包。无需额外配置。只需像往常一样拉取和使用镜像即可。

这些镜像中的所有软件包均由 Docker 从源代码构建，保持与基础镜像本身相同的安全标准。

## 将加固包添加到您的镜像

您可以通过以下两种方式将加固包添加到您自己的镜像中。

### 通过镜像自定义添加软件包

{{< summary-bar feature_name="Docker Hardened Images" >}}

使用 DHI Select 或 DHI Enterprise 自定义 Docker 加固镜像时，您可以通过自定义界面为基于 Alpine 的镜像添加加固包。请按照以下步骤[创建镜像自定义](./customize.md#create-an-image-customization)，并在自定义过程中选择加固包。

### 配置包管理器

您可以将包管理器配置为从 Docker 的加固软件包仓库拉取。这使您可以在自己的镜像中安装加固包。

#### 公共仓库

要在您自己的镜像中使用 Docker 的公共加固软件包仓库，请在 Dockerfile 中配置您的包管理器以安装 DHI 签名密钥并添加 DHI 仓库。

配置过程涉及三个步骤：

1. 安装[签名密钥](https://github.com/docker-hardened-images/keyring)
2. 配置软件包仓库
3. 更新并安装软件包

{{< tabs group="os" >}}
{{< tab name="Alpine" >}}

以下示例展示了如何在 Dockerfile 中配置 Alpine 包管理器以使用 Docker 的公共加固软件包仓库：

```dockerfile
FROM alpine:3.23

# 安装签名密钥
RUN cd /etc/apk/keys && \
    wget https://dhi.io/keyring/dhi-apk@docker-0F81AD7700D99184.rsa.pub

# 用加固软件包仓库替换默认仓库
RUN echo "https://dhi.io/apk/alpine/v3.23/main" > /etc/apk/repositories

# 更新并安装软件包
RUN apk update && \
    apk add libpng
```

在两处（基础镜像标签和仓库 URL）将 `3.23` 替换为您的 Alpine 版本。受支持的版本包括 Alpine 3.23 和 3.24。

要验证配置，请构建并运行镜像：

```console
$ docker build -t myapp:latest .
$ docker run -it myapp:latest sh
```

在容器内部，检查配置的仓库：

```console
/ # cat /etc/apk/repositories
https://dhi.io/apk/alpine/v3.23/main
```

这确保所有软件包都从 Docker 的加固仓库安装。

{{< /tab >}}
{{< tab name="Debian" >}}

以下示例展示了如何在 Dockerfile 中配置 Debian 包管理器以使用 Docker 的公共加固软件包仓库：

```dockerfile
FROM debian:trixie-slim

# 安装签名密钥
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://dhi.io/keyring/dhi-deb-gpg.D46852F6925E9F71.key \
    | gpg --dearmor -o /usr/share/keyrings/dhi-deb.gpg

# 添加加固软件包仓库
RUN echo "deb [signed-by=/usr/share/keyrings/dhi-deb.gpg] https://dhi.io/deb/debian/main trixie main" \
    > /etc/apt/sources.list.d/dhi.list

# 更新并安装软件包
RUN apt-get update && apt-get install -y jq \
    && rm -rf /var/lib/apt/lists/*
```

要验证配置，请构建并运行镜像：

```console
$ docker build -t myapp:latest .
$ docker run -it myapp:latest bash
```

在容器内部，检查配置的仓库：

```console
root@myapp:/# cat /etc/apt/sources.list.d/dhi.list
deb [signed-by=/usr/share/keyrings/dhi-deb.gpg] https://dhi.io/deb/debian/main trixie main
```

当 DHI 仓库提供某个软件包的加固版本时，`apt` 会自动优先选择它而非上游 Debian 版本。您可以使用 `apt-cache policy <package>` 确认这一点，它会显示一个来自 `https://dhi.io/deb/debian/main` 的带有 `+dhi` 或 `dhi` 版本后缀的候选版本。

并非每个 Debian 软件包都作为加固系统包提供。当某个软件包不在 DHI 仓库中时，`apt` 会透明地回退到基础镜像中配置的上游 Debian 镜像。

{{< /tab >}}
{{< /tabs >}}

从 Docker 加固镜像仓库安装的所有软件包均由 Docker 从源代码构建，并包含完整的溯源信息。

#### 企业仓库

{{< summary-bar feature_name="Docker Hardened Images Enterprise" >}}

使用 DHI Enterprise，您可以访问一个额外的软件包仓库，其中包含用于合规变体（例如 FIPS）的加固软件包，以及额外的安全补丁。

配置过程涉及五个步骤：

1. 安装[签名密钥](https://github.com/docker-hardened-images/keyring)
2. 配置基础软件包仓库
3. 添加企业安全仓库
4. 使用身份验证配置软件包安装
5. 使用 DHI CLI 将凭据作为 secret 传入来构建镜像

{{< tabs group="os" >}}
{{< tab name="Alpine" >}}

以下示例展示了如何在 Dockerfile 中配置 Alpine 包管理器以使用 Docker 的企业加固软件包仓库：

```dockerfile
FROM alpine:3.23

# 安装签名密钥
RUN cd /etc/apk/keys && \
    wget https://dhi.io/keyring/dhi-apk@docker-0F81AD7700D99184.rsa.pub

# 用加固软件包仓库替换默认仓库
RUN echo "https://dhi.io/apk/alpine/v3.23/main" > /etc/apk/repositories

# 更新并安装企业配置包以添加安全仓库
RUN apk update && \
    apk add dhi-enterprise-conf

# 使用身份验证从安全仓库安装软件包
RUN --mount=type=secret,id=http_auth \
    HTTP_AUTH="$(cat /run/secrets/http_auth)" \
    apk update && \
    apk add openssl-fips
```

使用作为构建 secret 安全传入的身份验证信息构建镜像：

```console
$ docker dhi auth apk > http_auth.txt
$ docker build --secret id=http_auth,src=http_auth.txt -t myapp-enterprise:latest .
$ rm http_auth.txt
```

`--secret` 标志在构建期间安全地挂载身份验证凭据，而不会将其存储在镜像层或元数据中。

{{< /tab >}}
{{< tab name="Debian" >}}

以下示例展示了如何在 Dockerfile 中配置 Debian 包管理器以使用 Docker 的企业加固软件包仓库。在 `/etc/apt/auth.conf.d/dhi.conf` 挂载凭据；当文件权限为 `0600` 时，`apt` 会自动读取 `/etc/apt/auth.conf.d/` 中的文件：

```dockerfile
FROM debian:trixie-slim

# 安装签名密钥
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://dhi.io/keyring/dhi-deb-gpg.D46852F6925E9F71.key \
    | gpg --dearmor -o /usr/share/keyrings/dhi-deb.gpg
RUN curl -fsSL https://dhi.io/keyring/dhi-deb-sec-gpg.D46852F6925E9F71.key \
    | gpg --dearmor -o /usr/share/keyrings/dhi-deb-sec.gpg

# 添加加固软件包仓库和企业安全仓库
RUN echo "deb [signed-by=/usr/share/keyrings/dhi-deb.gpg] https://dhi.io/deb/debian/main trixie main" \
    > /etc/apt/sources.list.d/dhi.list
RUN echo "deb [signed-by=/usr/share/keyrings/dhi-deb-sec.gpg] https://dhi.io/deb/debian/security trixie main" \
    > /etc/apt/sources.list.d/dhi-sec.list

# 使用身份验证从安全仓库安装软件包
RUN --mount=type=secret,id=netrc,target=/etc/apt/auth.conf.d/dhi.conf,mode=0600 \
    apt-get update && apt-get install -y openssl \
    && rm -rf /var/lib/apt/lists/*
```

通过环境变量将凭据作为构建 secret 安全传入来构建镜像：

```console
$ NETRC=$(docker dhi auth deb) docker build \
    --secret id=netrc,env=NETRC \
    -t myapp-enterprise:latest .
```

`--secret id=netrc,env=NETRC` 形式在构建期间安全地挂载身份验证凭据，而不会将其存储在镜像层或元数据中。

{{< /tab >}}
{{< /tabs >}}

## 验证软件包

每个加固包都经过加密签名，并包含证明其溯源和构建完整性的元数据。您可以验证签名并查看元数据，以确保您的软件包来自 Docker 受信任的构建基础设施。

### 查看软件包元数据

要查看加固包的信息：

{{< tabs group="os" >}}
{{< tab name="Alpine" >}}

```console
$ apk info -L <package-name>
```

{{< /tab >}}
{{< tab name="Debian" >}}

```console
$ dpkg -L <package-name>
```

{{< /tab >}}
{{< /tabs >}}

这会显示软件包中包含的文件及其元数据。

### 验证软件包签名

加固包由 Docker 进行加密签名。当您按照前述方式安装签名密钥并配置包管理器时，包管理器会在安装过程中自动验证签名。

如果某个软件包签名验证失败，包管理器将拒绝安装它，从而保护您免受被篡改或泄露的软件包影响。

### 构建溯源与加密验证

Docker 加固包由 Docker 受信任的基础设施构建，并包含可验证的元数据和加密签名。

要查看已安装软件包的此元数据：

{{< tabs group="os" >}}
{{< tab name="Alpine" >}}

```console
$ apk info -a <package-name>
```

{{< /tab >}}
{{< tab name="Debian" >}}

```console
$ apt-cache show <package-name>
```

{{< /tab >}}
{{< /tabs >}}

或者要查看安装前软件包的元数据：

{{< tabs group="os" >}}
{{< tab name="Alpine" >}}

```console
$ apk fetch --stdout <package-name> | tar -xzO .PKGINFO
```

{{< /tab >}}
{{< tab name="Debian" >}}

```console
$ apt-get download <package-name>
$ dpkg-deb -I <package-name>_*.deb
```

{{< /tab >}}
{{< /tabs >}}

软件包签名密钥确保软件包在构建后未被篡改。当您安装签名密钥并配置包管理器时，所有软件包都会在安装前自动验证。

### 软件包证明

每个加固包都包含自己的证明，类似于[镜像证明](./verify.md)。这些证明为单个软件包提供溯源和构建信息，使您能够将供应链追踪到软件包级别。

您可以先从镜像的 SLSA 溯源中提取软件包信息，然后使用软件包摘要来访问其证明。

#### 从镜像证明中提取软件包信息

要从镜像的 SLSA 溯源证明中获取特定软件包的溯源信息，您首先需要检索镜像的溯源，然后针对您感兴趣的特定软件包进行筛选。

SLSA 溯源证明包含一个 `materials` 数组，其中列出所有构建输入，包括软件包。您可以使用 `jq` 针对特定软件包筛选此数组：

```console
$ docker scout attest get dhi.io/golang:1.26-alpine3.23 \
    --predicate-type https://slsa.dev/provenance/v0.2 | \
    jq '.predicate.materials[] | select( .uri == "https://dhi.io/apk/alpine/v3.23/main/aarch64/golang-1.26-1.26.0-r0.apk" )'
```

将 `select()` 筛选器中的软件包 URI 替换为您要查找的特定软件包。您可以先不带 `select()` 筛选器运行命令以查看所有 materials，从而找到可用的软件包。

这会返回软件包 URI 及其 SHA-256 摘要：

```json
{
  "uri": "https://dhi.io/apk/alpine/v3.23/main/aarch64/golang-1.26-1.26.0-r0.apk",
  "digest": {
    "sha256": "4082a2500abc2e7b8435f9398d3514d760044fa52ca3d10cf80015469124a838"
  }
}
```

#### 列出软件包的可用证明

使用上一节中的软件包摘要，您可以列出该软件包所有可用的证明：

```console
$ curl -s https://dhi.io/apk/alpine/v3.23/main/sha256:4082a2500abc2e7b8435f9398d3514d760044fa52ca3d10cf80015469124a838/attestations/list | jq .
```

这会返回有关该软件包及其可用证明的信息：

```json
{
  "subject": {
    "name": "pkg:apk/alpine/golang-1.26@1.26.0-r0?os_name=&os_version=",
    "digest": {
      "sha256": "4082a2500abc2e7b8435f9398d3514d760044fa52ca3d10cf80015469124a838"
    }
  },
  "attestations": [
    {
      "predicate_type": "https://slsa.dev/provenance/v1",
      "digest": {
        "sha256": "97c919cf0edb27087739bbabeea4c1ef88d069cd41791476ba64b69280d63a32"
      },
      "url": "https://dhi.io/apk/alpine/v3.23/main/sha256:4082a2500abc2e7b8435f9398d3514d760044fa52ca3d10cf80015469124a838/attestations/sha256:97c919cf0edb27087739bbabeea4c1ef88d069cd41791476ba64b69280d63a32"
    }
  ]
}
```

#### 检索软件包证明

要检索实际的证明内容，请使用证明列表中提供的 URL：

```console
$ curl -s https://dhi.io/apk/alpine/v3.23/main/sha256:4082a2500abc2e7b8435f9398d3514d760044fa52ca3d10cf80015469124a838/attestations/sha256:97c919cf0edb27087739bbabeea4c1ef88d069cd41791476ba64b69280d63a32 | jq .
```

这会返回该软件包的完整 SLSA 溯源证明，其中包含有关该软件包如何构建、其依赖项以及其他构建材料的信息。

您可以递归地继续此过程，将供应链一直追踪到用于创建该软件包的编译器和其他构建工具。
