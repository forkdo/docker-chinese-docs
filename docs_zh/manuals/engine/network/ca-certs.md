---
title: 在 Docker 中使用 CA 证书
linkTitle: CA 证书
description: 了解如何在 Docker 主机和 Linux 容器中安装和使用 CA 证书
keywords: docker, networking, ca, certs, host, container, proxy
---

> [!CAUTION]
> 在生产环境中使用中间人（MITM）CA 证书时，应遵循最佳实践。如果证书被泄露，攻击者可能会拦截敏感数据、伪造受信任的服务，或执行中间人攻击。在继续之前，请咨询您的安全团队。

如果您的公司使用检查 HTTPS 流量的代理，您可能需要将所需的根证书添加到主机和 Docker 容器或镜像中。这是因为 Docker 及其容器在拉取镜像或发出网络请求时，需要信任代理的证书。

在主机上添加根证书可确保所有 Docker 命令（如 `docker pull`）能够正常工作。对于容器，您需要在构建过程或运行时将根证书添加到容器的信任存储中。这确保了容器内运行的应用程序能够通过代理通信，而不会遇到安全警告或连接失败。

## 向主机添加 CA 证书

以下部分描述了如何在 macOS 或 Windows 主机上安装 CA 证书。对于 Linux，请参考您发行版的文档。

### macOS

1. 下载 MITM 代理软件的 CA 证书。
2. 打开 **Keychain Access** 应用。
3. 在 Keychain Access 中，选择 **System**，然后切换到 **Certificates** 标签页。
4. 将下载的证书拖放到证书列表中。如果提示，请输入密码。
5. 找到新添加的证书，双击它，展开 **Trust** 部分。
6. 将证书设置为 **Always Trust**。如果提示，请输入密码。
7. 启动 Docker Desktop 并验证 `docker pull` 是否正常工作（假设 Docker Desktop 已配置为使用 MITM 代理）。

### Windows

选择使用 Microsoft 管理控制台（MMC）或您的 Web 浏览器来安装证书。

{{< tabs >}}
{{< tab name="MMC" >}}

1. 下载 MITM 代理软件的 CA 证书。
2. 打开 Microsoft 管理控制台（`mmc.exe`）。
3. 在 MMC 中添加 **Certificates Snap-In**：
   1. 选择 **File** → **Add/Remove Snap-in**，然后选择 **Certificates** → **Add >**。
   2. 选择 **Computer Account**，然后选择 **Next**。
   3. 选择 **Local computer**，然后选择 **Finish**。
4. 导入 CA 证书：
   1. 从 MMC 中，展开 **Certificates (Local Computer)**。
   2. 展开 **Trusted Root Certification Authorities** 部分。
   3. 右键点击 **Certificates**，选择 **All Tasks** 和 **Import…**。
   4. 按照提示导入您的 CA 证书。
5. 选择 **Finish**，然后选择 **Close**。
6. 启动 Docker Desktop 并验证 `docker pull` 是否成功（假设 Docker Desktop 已配置为使用 MITM 代理服务器）。

> [!NOTE]
> 根据使用的 SDK 和/或运行时/框架，除了将 CA 证书添加到操作系统的信任存储外，可能还需要进一步的步骤。

{{< /tab >}}
{{< tab name="Web browser" >}}

1. 下载 MITM 代理软件的 CA 证书。
2. 打开您的 Web 浏览器，进入 **Settings**，打开 **Manage certificates**。
3. 选择 **Trusted Root Certification Authorities** 标签页。
4. 选择 **Import**，然后浏览下载的 CA 证书。
5. 选择 **Open**，然后选择 **Place all certificates in the following store**。
6. 确保选择了 **Trusted Root Certification Authorities**，然后选择 **Next**。
7. 选择 **Finish**，然后选择 **Close**。
8. 启动 Docker Desktop 并验证 `docker pull` 是否成功（假设 Docker Desktop 已配置为使用 MITM 代理服务器）。

{{< /tab >}}
{{< /tabs >}}

## 向 Linux 镜像和容器添加 CA 证书

如果您需要运行依赖内部或自定义证书的容器化工作负载，例如在使用企业代理或安全服务的环境中，您必须确保容器信任这些证书。如果不添加必要的 CA 证书，容器内的应用程序在尝试连接到 HTTPS 端点时可能会遇到请求失败或安全警告。

通过在构建时[向镜像添加 CA 证书](#add-certificates-to-images)，您可以确保从该镜像启动的任何容器都信任指定的证书。这对于需要在生产环境中无缝访问内部 API、数据库或其他服务的应用程序尤其重要。

在无法重建镜像的情况下，您可以直接[向容器添加证书](#add-certificates-to-containers)。但是，运行时添加的证书在容器被销毁或重新创建后不会保留，因此此方法通常用于临时修复或测试场景。

## 向镜像添加证书

> [!NOTE]
> 以下命令适用于 Ubuntu 基础镜像。如果您的构建使用不同的 Linux 发行版，请使用相应的包管理命令（`apt-get`、`update-ca-certificates` 等）。

要在构建容器镜像时添加 CA 证书，在 Dockerfile 中添加以下指令：

```dockerfile
# 安装 ca-certificate 包
RUN apt-get update && apt-get install -y ca-certificates
# 从上下文复制 CA 证书到构建容器
COPY your_certificate.crt /usr/local/share/ca-certificates/
# 更新容器中的 CA 证书
RUN update-ca-certificates
```

### 向容器添加证书

> [!NOTE]
> 以下命令适用于基于 Ubuntu 的容器。如果您的容器使用不同的 Linux 发行版，请使用相应的包管理命令（`apt-get`、`update-ca-certificates` 等）。

要向运行中的 Linux 容器添加 CA 证书：

1. 下载 MITM 代理软件的 CA 证书。
2. 如果证书格式不是 `.crt`，请将其转换为 `.crt` 格式：

   ```console {title="示例命令"}
   $ openssl x509 -in cacert.der -inform DER -out myca.crt
   ```

3. 将证书复制到运行中的容器：

    ```console
    $ docker cp myca.crt <containerid>:/tmp
    ```

4. 附加到容器：

    ```console
    $ docker exec -it <containerid> sh
    ```

5. 确保已安装 `ca-certificates` 包（更新证书所需）：

    ```console
    # apt-get update && apt-get install -y ca-certificates
    ```

6. 将证书复制到 CA 证书的正确位置：

    ```console
    # cp /tmp/myca.crt /usr/local/share/ca-certificates/root_cert.crt
    ```

7. 更新 CA 证书：

    ```console
    # update-ca-certificates
    ```

    ```plaintext {title="示例输出"}
    Updating certificates in /etc/ssl/certs...
    rehash: warning: skipping ca-certificates.crt, it does not contain exactly one certificate or CRL
    1 added, 0 removed; done.
    ```

8. 验证容器能否通过 MITM 代理通信：

    ```console
    # curl https://example.com
    ```

    ```plaintext {title="示例输出"}
    <!doctype html>
    <html>
    <head>
        <title>Example Domain</title>
    ...
    ```