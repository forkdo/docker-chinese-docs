# Go 语言专用指南

本指南将向你展示如何使用 Docker 创建、测试和部署容器化的 Go 应用程序。

> **致谢**
>
> Docker 感谢 [Oliver Frolovs](https://www.linkedin.com/in/ofr/) 对本指南的贡献。

## 你将学到什么？

在本指南中，你将学习如何：

- 创建一个 `Dockerfile`，其中包含为 Go 编写的程序构建容器镜像的指令。
- 在本地 Docker 实例中将镜像作为容器运行，并管理容器的生命周期。
- 使用多阶段构建来高效地构建小镜像，同时保持 Dockerfile 易于阅读和维护。
- 使用 Docker Compose 在开发环境中协调多个相关容器的运行。
- 使用 [GitHub Actions](https://docs.github.com/en/actions) 为你的应用程序配置 CI/CD 流水线。
- 部署你的容器化 Go 应用程序。

## 先决条件

假定你对 Go 及其工具链有基本的了解。这不是 Go 教程。如果你是 : languages: 的新手，[Go 官网](https://golang.org/) 是一个很好的探索场所，所以 _go_（双关语）去看看吧！

你还必须了解一些基本的 [Docker 概念](/get-started/docker-concepts/the-basics/what-is-a-container.md)，并且至少对 [Dockerfile 格式](/manuals/build/concepts/dockerfile.md) 有大致的了解。

你的 Docker 设置必须启用 BuildKit。BuildKit 在 [Docker Desktop](/manuals/desktop/_index.md) 上默认对所有用户启用。如果你已经安装了 Docker Desktop，则无需手动启用 BuildKit。如果你在 Linux 上运行 Docker，请查看 BuildKit [入门指南](/manuals/build/buildkit/_index.md#getting-started)。

还期望你对命令行有一定的熟悉度。

## 下一步是什么？

本指南的目的是提供足够的示例和说明，让你能够容器化自己的 Go 应用程序并将其部署到云端。

从构建你的第一个 Go 镜像开始。

- [构建您的 Go 镜像](/guides/golang/build-images/)

- [以容器形式运行 Go 镜像](/guides/golang/run-containers/)

- [使用容器进行 Go 开发](/guides/golang/develop/)

- [使用 Go test 运行测试](/guides/golang/run-tests/)

- [为您的 Go 应用程序配置 CI/CD](/guides/golang/configure-ci-cd/)

- [测试你的 Go 部署](/guides/golang/deploy/)

