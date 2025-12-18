---
description: 如何配置和使用证书来验证注册表访问
keywords: 使用, 注册表, 仓库, 客户端, 根证书, docker, apache, ssl, tls, 文档, 示例, 文章, 教程
title: 使用证书验证仓库客户端
aliases:
- /articles/certificates/
- /engine/articles/certificates/
---

在[使用 HTTPS 运行 Docker](protect-access.md)一文中，您了解到默认情况下，Docker 通过非网络化的 Unix 套接字运行，必须启用 TLS 才能让 Docker 客户端和守护进程通过 HTTPS 安全通信。TLS 确保注册表端点的真实性，并保证与注册表之间的流量是加密的。

本文演示如何确保 Docker 注册表服务器与 Docker 守护进程（注册表服务器的客户端）之间的流量是加密的，并使用基于证书的客户端-服务器身份验证进行正确验证。

我们向您展示如何安装注册表的证书颁发机构（CA）根证书，以及如何设置用于验证的客户端 TLS 证书。

## 了解配置

通过在 `/etc/docker/certs.d` 下创建与注册表主机名相同的目录（例如 `localhost`）来配置自定义证书。所有 `*.crt` 文件都会添加到此目录作为 CA 根证书。

> [!NOTE]
>
> 在 Linux 上，任何根证书颁发机构都会与系统默认设置合并，包括主机的根 CA 集。如果您在 Windows Server 上运行 Docker，或在 Windows 上使用 Windows 容器运行 Docker Desktop，则仅在未配置自定义根证书时使用系统默认证书。

存在一个或多个 `<filename>.key/cert` 对表明 Docker 需要自定义证书才能访问目标仓库。

> [!NOTE]
>
> 如果存在多个证书，将按字母顺序依次尝试。如果遇到 4xx 级或 5xx 级身份验证错误，Docker 会继续尝试下一个证书。

以下示例说明了使用自定义证书的配置：

```text
    /etc/docker/certs.d/        <-- 证书目录
    └── localhost:5000          <-- 主机名:端口
       ├── client.cert          <-- 客户端证书
       ├── client.key           <-- 客户端密钥
       └── ca.crt               <-- 签署注册表证书的根 CA，PEM 格式
```

上述示例是特定于操作系统的，仅用于说明目的。您应查阅操作系统文档以创建操作系统提供的捆绑证书链。

## 创建客户端证书

使用 OpenSSL 的 `genrsa` 和 `req` 命令首先生成 RSA 密钥，然后使用该密钥创建证书。

```console
$ openssl genrsa -out client.key 4096
$ openssl req -new -x509 -text -key client.key -out client.cert
```

> [!NOTE]
>
> 这些 TLS 命令仅在 Linux 上生成可用的证书集。macOS 中的 OpenSSL 版本与 Docker 所需的证书类型不兼容。

## 故障排除提示

Docker 守护进程将 `.crt` 文件解释为 CA 证书，将 `.cert` 文件解释为客户端证书。如果 CA 证书意外使用了 `.cert` 扩展名而不是正确的 `.crt` 扩展名，Docker 守护进程会记录以下错误消息：

```text
缺少客户端证书 CERT_NAME 的密钥 KEY_NAME。CA 证书应使用扩展名 .crt。
```

如果访问 Docker 注册表时未指定端口号，请不要在目录名中添加端口。以下显示了在默认端口 443 上的注册表配置，通过 `docker login my-https.registry.example.com` 访问：

```text
    /etc/docker/certs.d/
    └── my-https.registry.example.com          <-- 不带端口的主机名
       ├── client.cert
       ├── client.key
       └── ca.crt
```

## 相关信息

* [使用受信任的镜像](trust/_index.md)
* [保护 Docker 守护进程套接字](protect-access.md)