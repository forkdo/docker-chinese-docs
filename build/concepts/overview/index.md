# Docker Build 概述


Docker Build 采用客户端-服务器架构，其中：

- 客户端：Buildx 是客户端，也是用于运行和管理构建的用户界面。
- 服务器：BuildKit 是服务器，也即处理构建执行的构建器。

当你发起一次构建时，Buildx 客户端会向 BuildKit 后端发送构建请求。BuildKit 解析构建指令并执行构建步骤。构建输出要么返回给客户端，要么上传到 Docker Hub 等镜像仓库。

Buildx 和 BuildKit 都随 Docker Desktop 和 Docker Engine 开箱即用地安装。当你调用 `docker build` 命令时，你正在使用 Buildx 借助 Docker 捆绑的默认 BuildKit 来运行构建。

## Buildx

Buildx 是你用来运行构建的 CLI 工具。`docker build` 命令是 Buildx 的一层封装。当你调用 `docker build` 时，Buildx 解析构建选项，并向 BuildKit 后端发送构建请求。

Buildx 客户端能做的不仅仅是运行构建。你还可以使用 Buildx 创建和管理称为 builder 的 BuildKit 后端。它还支持管理镜像仓库中镜像以及并发运行多个构建的功能。

Docker Buildx 默认随 Docker Desktop 一起安装。你也可以从源代码构建该 CLI 插件，或从 GitHub 仓库获取二进制文件手动安装。更多信息请参阅 GitHub 上的 [Buildx README](https://github.com/docker/buildx#manual-download)。

> [!NOTE]
> 虽然 `docker build` 在底层调用了 Buildx，但该命令与规范的 `docker buildx build` 之间存在细微差别。有关详情，请参阅 [<code>docker build</code> 与 <code>docker buildx build</code> 的区别](../builders/_index.md#difference-between-docker-build-and-docker-buildx-build)。

## BuildKit

BuildKit 是执行构建工作负载的守护进程。

一次构建执行始于调用 `docker build` 命令。Buildx 解析你的构建命令，并向 BuildKit 后端发送构建请求。构建请求包括：

- Dockerfile
- 构建参数
- 导出选项
- 缓存选项

BuildKit 解析构建指令并执行构建步骤。在 BuildKit 执行构建期间，Buildx 监控构建状态并将进度打印到终端。

如果构建需要来自客户端的资源（例如本地文件或构建密钥），BuildKit 会向 Buildx 请求它所需的资源。

这是与早期 Docker 版本中使用的旧版构建器相比，BuildKit 更高效的一个方面。BuildKit 只在需要时才请求构建所需的资源。相比之下，旧版构建器总是复制一份本地文件系统。

BuildKit 可以向 Buildx 请求的资源示例包括：

- 本地文件系统构建上下文
- 构建密钥
- SSH 套接字
- 镜像仓库认证令牌

有关 BuildKit 的更多信息，请参阅 [BuildKit](/manuals/build/buildkit/_index.md)。

