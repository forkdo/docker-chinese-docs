# 在 Zscaler 环境中使用 Docker


在许多企业环境中，网络流量会被 HTTPS 代理（例如 Zscaler）拦截并监控。虽然 Zscaler
能够确保安全合规和网络管控，但它可能给使用 Docker 的开发者带来问题，尤其是在构建过程中
可能出现 SSL 证书校验错误。本指南说明如何配置 Docker 容器和构建，使其正确处理 Zscaler
的自定义证书，从而在受监控的环境中平稳运行。

## 证书在 Docker 中的作用

当 Docker 构建或运行容器时，它常常需要从互联网获取资源——无论是从镜像仓库拉取基础镜像、
下载依赖，还是与外部服务通信。在代理环境中，Zscaler 会拦截 HTTPS 流量，并用自己的证书
替换远程服务器的证书。然而，Docker 默认并不信任这个 Zscaler 证书，从而导致 SSL 错误。

```plaintext
x509: certificate signed by unknown authority
```

出现这些错误是因为 Docker 无法验证 Zscaler 所提供证书的有效性。要避免这种情况，你必须
配置 Docker 信任 Zscaler 的证书。

## 为 Docker Desktop 配置 Zscaler 代理

根据 Zscaler 的部署方式，你可能需要手动配置 Docker Desktop 的代理设置以使用 Zscaler 代理。

如果你通过 [Zscaler Client Connector](https://help.zscaler.com/zscaler-client-connector/what-is-zscaler-client-connector)
把 Zscaler 作为系统级代理使用，设备上的所有流量都会自动经由 Zscaler 路由，因此
Docker Desktop 会自动使用 Zscaler 代理，无需额外配置。

如果你没有把 Zscaler 作为系统级代理使用，请在 Docker Desktop 中手动配置代理设置。你可以
使用[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)
为组织内所有客户端统一配置代理设置，或在 Docker Desktop 图形界面的
[**Settings > Resources > Proxies**](/manuals/desktop/settings-and-maintenance/settings.md#proxies)
中编辑代理配置。

## 在 Docker 镜像中安装根证书

为了让容器能够使用并信任 Zscaler 代理，需要把证书嵌入镜像并配置镜像的信任库。在镜像构建
阶段安装证书是首选做法，因为这样无需在启动时进行配置，还能提供可审计、一致的环境。

### 获取根证书

获取根证书最简单的方式，是从管理员已安装该证书的机器上导出它。你可以使用 Web 浏览器或
系统的证书管理服务（例如 Windows 证书存储）。

#### 示例：使用 Google Chrome 导出证书

1. 在 Google Chrome 中访问 `chrome://certificate-manager/`。
2. 在 **Local certificates** 下，选择 **View imported certificates**。
3. 找到 Zscaler 根证书，通常标记为 **Zscaler Root CA**。
4. 打开证书详情并选择 **Export**。
5. 以 ASCII PEM 格式保存证书。
6. 用文本编辑器打开导出的文件，确认其中包含 `-----BEGIN CERTIFICATE-----` 和
   `-----END CERTIFICATE-----`。

获得证书后，把它保存在可访问的仓库中，例如 JFrog Artifactory 或 Git 仓库。也可以使用
AWS S3 之类的通用存储。

### 在构建中使用该证书

要在构建镜像时安装这些证书，需把证书复制到构建容器中并更新信任库。示例 Dockerfile 如下：

```dockerfile
FROM debian:bookworm
COPY zscaler-root-ca.crt /usr/local/share/ca-certificates/zscaler-root-ca.crt
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates
```

这里的 `zscaler-root-ca.crt` 就是根证书，位于构建上下文的根目录（通常在应用的 Git
仓库中）。

如果你使用制品仓库，可以用 `ADD` 指令直接获取证书。你还可以使用 `--checksum` 标志来
校验证书的内容摘要是否正确。

```dockerfile
FROM debian:bookworm
ADD --checksum=sha256:24454f830cdb571e2c4ad15481119c43b3cafd48dd869a9b2945d1036d1dc68d \
    https://artifacts.example/certs/zscaler-root-ca.crt /usr/local/share/ca-certificates/zscaler-root-ca.crt
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates
```

#### 使用多阶段构建

对于需要在最终运行时镜像中使用证书的多阶段构建，请确保证书安装发生在最后一个阶段。

```dockerfile
FROM debian:bookworm AS build
WORKDIR /build
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git
RUN --mount=target=. cmake -B output/

FROM debian:bookworm-slim AS final
ADD --checksum=sha256:24454f830cdb571e2c4ad15481119c43b3cafd48dd869a9b2945d1036d1dc68d \
    https://artifacts.example/certs/zscaler-root-ca.crt /usr/local/share/ca-certificates/zscaler-root-ca.crt
RUN apt-get update && \
    apt-get install -y ca-certificates && \
    update-ca-certificates
WORKDIR /app
COPY --from=build /build/output/bin .
ENTRYPOINT ["/app/bin"]
```

## 结语

把 Zscaler 根证书直接嵌入到你的 Docker 镜像中，可以确保容器在 Zscaler 代理环境中顺畅
运行。采用这种方式，你能减少潜在的运行时错误，并建立一致、可审计的配置，使 Docker
在受监控的网络中平稳工作。

