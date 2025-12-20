# 优化 Docker Offload 使用

Docker Offload 会在远程构建和运行您的容器，而不是在您调用命令的机器上。这意味着文件必须通过网络从您的本地系统传输到云端。

与本地传输相比，通过网络传输文件会带来更高的延迟和更低的带宽。

即使经过优化，大型项目或较慢的网络连接也可能导致更长的传输时间。以下是优化 Docker Offload 设置的几种方法：

- [使用 `.dockerignore` 文件](#dockerignore-files)
- [选择精简的基础镜像](#slim-base-images)
- [使用多阶段构建](#multi-stage-builds)
- [在构建期间获取远程文件](#fetch-remote-files-in-build)
- [利用多线程工具](#multi-threaded-tools)

有关 Dockerfile 的一般技巧，请参阅[构建最佳实践](/manuals/build/building/best-practices.md)。

## dockerignore 文件

[`.dockerignore` 文件](/manuals/build/concepts/context.md#dockerignore-files) 让您可以指定哪些本地文件*不应*包含在构建上下文中。被这些模式排除的文件在构建期间不会上传到 Docker Offload。

典型的忽略项包括：

- `.git` – 避免传输您的版本历史记录。（注意：您将无法在构建中运行 `git` 命令。）
- 构建产物或本地生成的二进制文件。
- 依赖文件夹，例如 `node_modules`，如果这些在构建过程中被恢复。

根据经验，您的 `.dockerignore` 应该与您的 `.gitignore` 类似。

## 精简的基础镜像

`FROM` 指令中使用较小的基础镜像可以减小最终镜像的大小并提高构建性能。[`alpine`](https://hub.docker.com/_/alpine) 镜像是一个极简基础镜像的良好示例。

对于完全静态的二进制文件，您可以使用 [`scratch`](https://hub.docker.com/_/scratch)，这是一个空的基础镜像。

## 多阶段构建

[多阶段构建](/build/building/multi-stage/) 允许您在 Dockerfile 中分离构建时和运行时环境。这不仅减小了最终镜像的大小，还允许在构建期间并行执行阶段。

使用 `COPY --from` 从早期阶段或外部镜像复制文件。这种方法有助于最小化不必要的层并减小最终镜像的大小。

## 在构建期间获取远程文件

如果可能，请在构建本身期间从互联网下载大文件，而不是将它们捆绑在本地上下文中。这避免了从您的客户端到 Docker Offload 的网络传输。

您可以使用以下方法实现此目的：

- Dockerfile [`ADD` 指令](/reference/dockerfile/#add)
- `RUN` 命令，例如 `wget`、`curl` 或 `rsync`

### 多线程工具

一些构建工具，例如 `make`，默认是单线程的。如果工具支持，请将其配置为并行运行。例如，使用 `make --jobs=4` 来同时运行四个作业。

利用云中可用的 CPU 资源可以显著缩短构建时间。
