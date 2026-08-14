# 自定义 Dockerfile 语法


## Dockerfile 前端（Dockerfile frontend）

BuildKit 支持从容器镜像中动态加载前端。要使用外部 Dockerfile 前端，你的 [Dockerfile](/reference/dockerfile.md) 的第一行需要设置 [`syntax` 指令](/reference/dockerfile.md#syntax)，指向你想要使用的具体镜像：

```dockerfile
# syntax=[remote image reference]
```

例如：

```dockerfile
# syntax=docker/dockerfile:1
# syntax=docker.io/docker/dockerfile:1
# syntax=example.com/user/repo:tag@sha256:abcdef...
```

你也可以使用预定义的 `BUILDKIT_SYNTAX` 构建参数在命令行上设置前端镜像引用：

```console
$ docker build --build-arg BUILDKIT_SYNTAX=docker/dockerfile:1 .
```

这定义了用于构建 Dockerfile 的 Dockerfile 语法位置。BuildKit 后端允许无缝使用作为 Docker 镜像分发并在容器沙箱环境中执行的外部实现。

自定义 Dockerfile 实现使你能够：

- 无需更新 Docker 守护进程即可自动获取 bug 修复
- 确保所有用户都使用相同的实现来构建你的 Dockerfile
- 无需更新 Docker 守护进程即可使用最新功能
- 在功能集成到 Docker 守护进程之前试用新功能或第三方功能
- 使用 [替代的构建定义，或创建你自己的定义](https://github.com/moby/buildkit#exploring-llb)
- 构建带有自定义功能的你自己的 Dockerfile 前端

> [!NOTE]
>
> BuildKit 自带一个内置的 Dockerfile 前端，但建议使用外部镜像，以确保所有用户在构建器上使用相同版本，并在无需等待 BuildKit 或 Docker Engine 新版本的情况下自动获取 bug 修复。

## 官方发布版本

Docker 在 Docker Hub 的 `docker/dockerfile` 仓库下分发可用于构建 Dockerfile 的官方镜像版本。新镜像通过两个渠道发布：`stable` 和 `labs`。

### Stable 渠道

`stable` 渠道遵循 [语义化版本](https://semver.org)。例如：

- `docker/dockerfile:1` - 与最新的 `1.x.x` 次版本 _和_ 补丁版本保持同步更新。
- `docker/dockerfile:1.2` - 与最新的 `1.2.x` 补丁版本保持同步更新，并在 `1.3.0` 版本发布后停止接收更新。
- `docker/dockerfile:1.2.1` - 不可变：永不更新。

我们建议使用 `docker/dockerfile:1`，它始终指向版本 1 语法的最新稳定发布版本，并接收版本 1 发布周期内的 "次版本" 和 "补丁" 更新。BuildKit 在执行构建时会自动检查该语法的更新，确保你使用的是最新版本。

如果使用特定版本，例如 `1.2` 或 `1.2.1`，则需要手动更新 Dockerfile 才能继续接收 bug 修复和新功能。旧版本的 Dockerfile 仍与新版本的构建器兼容。

### Labs 渠道

`labs` 渠道提供对 `stable` 渠道中尚不可用的 Dockerfile 功能的抢先体验。`labs` 镜像与稳定版同时发布，并遵循相同的版本模式，但使用 `-labs` 后缀，例如：

- `docker/dockerfile:labs` - `labs` 渠道上的最新发布版本。
- `docker/dockerfile:1-labs` - 与 `dockerfile:1` 相同，但启用了实验性功能。
- `docker/dockerfile:1.2-labs` - 与 `dockerfile:1.2` 相同，但启用了实验性功能。
- `docker/dockerfile:1.2.1-labs` - 不可变：永不更新。与 `dockerfile:1.2.1` 相同，但启用了实验性功能。

选择最适合你需求的渠道。如果你想受益于新功能，请使用 `labs` 渠道。`labs` 渠道中的镜像包含 `stable` 渠道中的所有功能，外加抢先体验功能。`labs` 渠道中的稳定功能遵循 [语义化版本](https://semver.org)，但抢先体验功能不遵循，且较新的发布版本可能不向后兼容。固定版本号以避免处理破坏性更改。

## 其他资源

有关 `labs` 功能、master 构建和每日功能发布的文档，请参阅 [GitHub 上的 BuildKit 源代码仓库中的说明](https://github.com/moby/buildkit/blob/master/README.md)。有关可用镜像的完整列表，请访问 [Docker Hub 上的 `docker/dockerfile` 仓库](https://hub.docker.com/r/docker/dockerfile)，以及用于开发构建的 [Docker Hub 上的 `docker/dockerfile-upstream` 仓库](https://hub.docker.com/r/docker/dockerfile-upstream)。

