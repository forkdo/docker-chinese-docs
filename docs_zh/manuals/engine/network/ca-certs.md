---
title: 在 Docker 中使用 CA 证书
linkTitle: CA 证书
description: 了解如何在 Docker 主机和 Linux 容器中安装和使用 CA 证书
keywords: docker, networking, ca, certs, host, container, proxy
---

> [!CAUTION]
> 在生产容器中使用中间人 (MITM) CA 证书时，应遵循最佳实践。如果证书泄露，攻击者可能会拦截敏感数据、欺骗受信任的服务或执行中间人攻击。在继续操作之前，请咨询您的安全团队。

如果您的公司使用代理来检查 HTTPS 流量，您可能需要将所需的根证书添加到您的主机机器以及 Docker 容器或镜像中。这是因为 Docker 及其容器在拉取镜像或发出网络请求时，需要信任代理的证书。

在主机上添加根证书可确保任何 Docker 命令（如 `docker pull`）都能正常工作。对于容器，您需要在构建过程或运行时将根证书添加到容器的信任存储中。这确保了容器内运行的应用程序可以通过代理进行通信，而不会遇到安全警告或连接失败。

## 将 CA 证书添加到主机

以下部分介绍如何在 macOS 或 Windows 主机上安装 CA 证书。对于 Linux，请参阅您所用发行版的文档。

### macOS

1. 下载 MITM 代理软件的 CA 证书。
2. 打开 **钥匙串访问 (Keychain Access)** 应用。
3. 在钥匙串访问中，选择 **系统 (System)**，然后切换到 **证书 (Certificates)** 选项卡。
4. 将下载的证书拖放到证书列表中。如果提示，请输入您的密码。
5. 找到新添加的证书，双击它，然后展开 **信任 (Trust)** 部分。
6. 将证书设置为 **始终信任 (Always Trust)**。如果提示，请输入您的密码。
7. 启动 Docker Desktop 并验证 `docker pull` 是否有效（假设 Docker Desktop 已配置为使用 MITM 代理）。

### Windows

选择是使用 Microsoft 管理控制台 (MMC) 还是 Web 浏览器安装证书。

{{< tabs >}}
{{< tab name="MMC" >}}

1. 下载 MITM 代理软件的 CA 证书。
2. 打开 Microsoft 管理控制台 (`mmc.exe`)。
3. 在 MMC 中添加 **证书管理单元 (Certificates Snap-In)**。
   1. 选择 **文件 (File)** → **添加/删除管理单元 (Add/Remove Snap-in)**，然后选择 **证书 (Certificates)** → **添加 > (Add >)**。
   2. 选择 **计算机帐户 (Computer Account)**，然后选择 **下一步 (Next)**。
   3. 选择 **本地计算机 (Local computer)**，然后选择 **完成 (Finish)**。
4. 导入 CA 证书：
   1. 在 MMC 中，展开 **证书(本地计算机) (Certificates (Local Computer))**。
   2. 展开 **受信任的根证书颁发机构 (Trusted Root Certification Authorities)** 部分。
   3. 右键单击 **证书 (Certificates)**，选择 **所有任务 (All Tasks)** 和 **导入... (Import…)**。
   4. 按照提示导入您的 CA 证书。
5. 选择 **完成 (Finish)**，然后选择 **关闭 (Close)**。
6. 启动 Docker Desktop 并验证 `docker pull` 是否成功（假设 Docker Desktop 已配置为使用 MITM 代理服务器）。

> [!NOTE]
> 根据使用的 SDK 和/或运行时/框架，除了将 CA 证书添加到操作系统的信任存储之外，可能还需要采取进一步的步骤。

{{< /tab >}}
{{< tab name="Web browser" >}}

1. 下载 MITM 代理软件的 CA 证书。
2. 打开您的 Web 浏览器，转到 **设置 (Settings)** 并打开 **管理证书 (Manage certificates)**。
3. 选择 **受信任的根证书颁发机构 (Trusted Root Certification Authorities)** 选项卡。
4. 选择 **导入 (Import)**，然后浏览找到下载的 CA 证书。
5. 选择 **打开 (Open)**，然后选择 **将所有证书放入下列存储区 (Place all certificates in the following store)**。
6. 确保选中 **受信任的根证书颁发机构 (Trusted Root Certification Authorities)**，然后选择 **下一步 (Next)**。
7. 选择 **完成 (Finish)**，然后选择 **关闭 (Close)**。
8. 启动 Docker Desktop 并验证 `docker pull` 是否成功（假设 Docker Desktop 已配置为使用 MITM 代理服务器）。

{{< /tab >}}
{{< /tabs >}}

## 将 CA 证书添加到 Linux 镜像和容器

如果您需要运行依赖内部或自定义证书的容器化工作负载（例如在具有公司代理或安全服务的环境中），您必须确保容器信任这些证书。如果未添加必要的 CA 证书，容器内的应用程序在尝试连接到 HTTPS 端点时可能会遇到请求失败或安全警告。

通过在构建时[将 CA 证书添加到镜像](#add-certificates-to-images)，您可以确保从该镜像启动的任何容器都将信任指定的证书。这对于在生产期间需要无缝访问内部 API、数据库或其他服务的应用程序尤为重要。

如果重新构建镜像不可行，您可以改为直接[将证书添加到容器](#add-certificates-to-containers)。但是，在运行时添加的证书如果容器被销毁或重新创建将不会保留，因此此方法通常用于临时修复或测试场景。

## 将证书添加到镜像

> [!NOTE]
> 以下命令适用于 Ubuntu 基础镜像。如果您的构建使用不同的 Linux 发行版，请使用等效的包管理命令（`apt-get`、`update-ca-certificates` 等）。

要在构建容器镜像时添加 CA 证书，请将以下指令添加到您的 Dockerfile 中。

```dockerfile
# 安装 ca-certificate 软件包
RUN apt-get update && apt-get install -y ca-certificates
# 将 CA 证书从上下文复制到构建容器中
COPY your_certificate.crt /usr/local/share/ca-certificates/
# 更新容器中的 CA 证书
RUN update-ca-certificates
```

### 将证书添加到容器

> [!NOTE]
> 以下命令适用于基于 Ubuntu 的容器。如果您的容器使用不同的 Linux 发行版，请使用等效的包管理命令（`apt-get`、`update-ca-certificates` 等）。

要将 CA 证书添加到正在运行的 Linux 容器：

1. 下载 MITM 代理软件的 CA 证书。
2. 如果证书格式不是 `.crt`，请将其转换为 `.crt` 格式：

   ```console {title="示例命令"}
   $ openssl x509 -in cacert.der -inform DER -out myca.crt
   ```

3. 将证书复制到正在运行的容器中：

    ```console
    $ docker cp myca.crt <containerid>:/tmp
    ```

4. 附加到容器：

    ```console
    $ docker exec -it <containerid> sh
    ```

5. 确保已安装 `ca-certificates` 软件包（更新证书所必需）：

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

8. 验证容器是否可以通过 MITM 代理进行通信：

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