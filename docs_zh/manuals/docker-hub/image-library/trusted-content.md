---
description: 了解 Docker Hub 的可信内容。
keywords: Docker Hub, Hub, 可信内容
title: 可信内容
weight: 15
aliases:
- /trusted-content/official-images/using/
- /trusted-content/official-images/
---

Docker Hub 的可信内容提供了一组经过精心挑选的高质量、安全的镜像，旨在让开发者对其使用的资源的可靠性和安全性充满信心。这些镜像稳定、定期更新，并遵循行业最佳实践，是构建和部署应用程序的坚实基础。Docker Hub 的可信内容包括 Docker 官方镜像、已验证发布者镜像，以及 Docker 赞助的开源软件镜像。

## Docker 官方镜像

> [!NOTE]
>
> Docker 正在逐步淘汰 Docker 官方镜像 (DOI) 的 Docker 内容信任 (DCT) 功能。
> 从 2025 年 8 月 8 日起，最老的 DOI DCT 签名证书将开始过期。如果您在使用 `docker trust` 命令操作 DOI 时，可能已经看到了过期警告。这些证书一旦被 Docker 客户端缓存，就不会再刷新，使得证书轮换变得不切实际。如果您将 `DOCKER_CONTENT_TRUST` 环境变量设置为 true (`DOCKER_CONTENT_TRUST=1`)，DOI 的拉取操作将开始失败。解决方法是取消设置 `DOCKER_CONTENT_TRUST` 环境变量。使用 `docker trust inspect` 命令也会开始失败，不应再用于 DOI。
>
> 更多详情，请参阅
> https://www.docker.com/blog/retiring-docker-content-trust/。

Docker 官方镜像是托管在 Docker Hub 上的一组经过精心挑选的 Docker 仓库。

Docker 建议您在项目中使用 Docker 官方镜像。这些镜像文档清晰，促进最佳实践，并且会定期更新。Docker 官方镜像支持大多数常见的使用场景，非常适合新 Docker 用户。高级用户也可以受益于更专业化的镜像变体，并且可以在学习 `Dockerfile` 的过程中参考 Docker 官方镜像。

> [!NOTE]
>
> 使用 Docker 官方镜像需遵守 [Docker 服务条款](https://www.docker.com/legal/docker-terms-service/)。

这些镜像提供了重要的基础仓库，作为大多数用户的起点。

这些镜像包括操作系统，如 [Ubuntu](https://hub.docker.com/_/ubuntu/) 和 [Alpine](https://hub.docker.com/_/alpine/)，编程语言运行时，如 [Python](https://hub.docker.com/_/python) 和 [Node](https://hub.docker.com/_/node)，以及其他重要工具，如 [memcached](https://hub.docker.com/_/memcached) 和 [MySQL](https://hub.docker.com/_/mysql)。

这些镜像是 Docker Hub 上[最安全的镜像](https://www.docker.com/blog/enhancing-security-and-transparency-with-docker-official-images/)之一。这一点尤为重要，因为 Docker 官方镜像是 Docker Hub 上最受欢迎的镜像之一。通常，Docker 官方镜像包含的 CVE 包很少或没有。

这些镜像展示了 [Dockerfile 最佳实践](/manuals/build/building/best-practices.md)，并提供清晰的文档，为其他 Dockerfile 作者提供参考。

属于此计划的镜像在 Docker Hub 上有特殊的徽章，便于您识别哪些项目属于 Docker 官方镜像。

![Docker 官方镜像徽章](../images/official-image-badge-iso.png)

### 支持的标签和对应的 Dockerfile 链接

每个 Docker 官方镜像的仓库描述中都有一个 **Supported tags and respective Dockerfile links**（支持的标签和对应的 Dockerfile 链接）部分，列出了所有当前标签以及创建这些标签的 Dockerfile 链接。此部分的目的是展示有哪些镜像变体可用。

![示例：Ubuntu 支持的标签](../images/supported_tags.webp)

同一行中列出的标签都指向同一个底层镜像。多个标签可以指向同一个镜像。例如，在上一张截图（来自 `ubuntu` Docker 官方镜像仓库）中，标签 `24.04`、`noble-20240225`、`noble` 和 `devel` 都指向同一个镜像。

Docker 官方镜像的 `latest` 标签通常针对易用性进行了优化，包含大量有用的软件，如开发工具和构建工具。将镜像标记为 `latest`，镜像维护者本质上是建议将该镜像用作默认镜像。换句话说，如果您不知道该使用哪个标签，或者不熟悉底层软件，那么您应该从 `latest` 镜像开始。随着您对软件和镜像变体的理解加深，您可能会发现其他镜像变体更符合您的需求。

### 瘦身镜像

许多语言栈，如 [Node.js](https://hub.docker.com/_/node/)、[Python](https://hub.docker.com/_/python/) 和 [Ruby](https://hub.docker.com/_/ruby/)，都提供了 `slim` 标签变体，旨在提供一个轻量级、适合生产的、包含较少软件包的基础镜像。

`slim` 镜像的典型使用模式是作为 [多阶段构建](https://docs.docker.com/build/building/multi-stage/) 最终阶段的基础镜像。例如，您在构建的第一阶段使用 `latest` 变体构建应用程序，然后将应用程序复制到基于 `slim` 变体的最终阶段。以下是一个示例 `Dockerfile`。

```dockerfile
FROM node:latest AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . ./
FROM node:slim
WORKDIR /app
COPY --from=build /app /app
CMD ["node", "app.js"]
```

### Alpine 镜像

许多 Docker 官方镜像仓库还提供 `alpine` 变体。这些镜像基于 [Alpine Linux](https://www.alpinelinux.org/) 发行版构建，而不是 Debian 或 Ubuntu。Alpine Linux 专注于为容器镜像提供一个小型、简单和安全的基础，Docker 官方镜像的 `alpine` 变体通常只安装必要的软件包。因此，Docker 官方镜像的 `alpine` 变体通常比 `slim` 变体更小。

主要需要注意的是，Alpine Linux 使用 [musl libc](https://musl.libc.org/) 而不是 [glibc](https://www.gnu.org/software/libc/)。此外，为了最小化镜像大小，Alpine 基础镜像通常不包含 Git 或 Bash 等工具。根据您的程序对 libc 的依赖深度或假设，您可能会发现由于缺少库或工具而遇到问题。

当您使用 Alpine 镜像作为基础时，考虑以下选项以使您的程序与 Alpine Linux 和 musl 兼容：

- 针对 musl libc 编译您的程序
- 将 glibc 库静态链接到您的程序中
- 完全避免 C 依赖（例如，构建时不启用 CGO 的 Go 程序）
- 在您的 Dockerfile 中自行添加所需的软件。

如果您不熟悉如何安装软件包，请参考 Docker Hub 上 `alpine` 镜像的 [描述](https://hub.docker.com/_/alpine) 了解示例。

### 代号

标签中包含看起来像《玩具总动员》角色的单词（例如 `bookworm`、`bullseye` 和 `trixie`）或形容词（如 `jammy` 和 `noble`），表示它们所使用的基础镜像的 Linux 发行版代号。Debian 发行版的代号基于《玩具总动员》角色，而 Ubuntu 的代号形式为“形容词+动物”。例如，Ubuntu 24.04 的代号是“Noble Numbat”。

Linux 发行版指示器很有用，因为许多 Docker 官方镜像提供基于多个底层发行版版本的变体（例如，`postgres:bookworm` 和 `postgres:bullseye`）。

### 其他标签

除了此处描述的之外，Docker 官方镜像标签可能还包含其他提示其镜像变体用途的标签。通常，这些标签变体在 Docker 官方镜像仓库文档中有说明。阅读“如何使用此镜像”和“镜像变体”部分将帮助您了解如何使用这些变体。

## 已验证发布者镜像

Docker 已验证发布者计划提供由 Docker 验证的商业发布者提供的高质量镜像。

这些镜像帮助开发团队构建安全的软件供应链，尽早最大限度地减少恶意内容的暴露，从而在后期节省时间和金钱。

属于此计划的镜像在 Docker Hub 上有特殊的徽章，便于用户识别 Docker 已验证的高质量商业发布者项目。

![Docker 已验证发布者徽章](../images/verified-publisher-badge-iso.png)

## Docker 赞助的开源软件镜像

Docker 赞助的开源软件 (OSS) 计划提供由 Docker 赞助的开源项目发布和维护的镜像。

属于此计划的镜像在 Docker Hub 上有特殊的徽章，便于用户识别 Docker 已验证的可信、安全和活跃的开源项目。

![Docker 赞助开源徽章](../images/sponsored-badge-iso.png)