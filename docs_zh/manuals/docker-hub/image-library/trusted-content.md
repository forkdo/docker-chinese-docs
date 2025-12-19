---
description: 了解 Docker Hub 的可信内容。
keywords: Docker Hub, Hub, trusted content
title: 可信内容
weight: 15
aliases:
- /trusted-content/official-images/using/
- /trusted-content/official-images/
---

Docker Hub 的可信内容提供了一系列经过精心挑选的高质量、安全的镜像，旨在让开发者对所依赖资源的可靠性和安全性充满信心。这些镜像稳定、定期更新，并遵循行业最佳实践，是构建和部署应用程序的坚实基础。Docker Hub 的可信内容包括 Docker Official Images、已验证发布者镜像（Verified Publisher images）以及 Docker 赞助的开源软件镜像（Docker-Sponsored Open Source Software images）。

## Docker Official Images

Docker Official Images 是托管在 Docker Hub 上的一组经过精心挑选的 Docker 仓库。

Docker 建议您在项目中使用 Docker Official Images。这些镜像拥有清晰的文档、倡导最佳实践，并定期更新。Docker Official Images 支持大多数常见用例，非常适合 Docker 新手用户。高级用户也可以从更专业的镜像变体中受益，并将 Docker Official Images 作为 `Dockerfile` 学习过程的一部分进行审查。

> [!NOTE]
>
> 使用 Docker Official Images 需遵守 [Docker 服务条款](https://www.docker.com/legal/docker-terms-service/)。

这些镜像提供了基础仓库，是大多数用户的起点。

包括操作系统，如 [Ubuntu](https://hub.docker.com/_/ubuntu/) 和 [Alpine](https://hub.docker.com/_/alpine/)，编程语言运行时，如 [Python](https://hub.docker.com/_/python) 和 [Node](https://hub.docker.com/_/node)，以及其他基本工具，如 [memcached](https://hub.docker.com/_/memcached) 和 [MySQL](https://hub.docker.com/_/mysql)。

这些镜像是 Docker Hub 上[最安全的镜像](https://www.docker.com/blog/enhancing-security-and-transparency-with-docker-official-images/)之一。这一点尤为重要，因为 Docker Official Images 是 Docker Hub 上最受欢迎的镜像之一。通常，Docker Official 镜像包含很少或没有 CVE 的软件包。

这些镜像体现了 [Dockerfile 最佳实践](/manuals/build/building/best-practices.md)，并提供清晰的文档，为其他 Dockerfile 作者提供参考。

属于该计划的项目在 Docker Hub 上有一个特殊标记，便于您识别属于 Docker Official Images 的项目。

![Docker official image badge](../images/official-image-badge-iso.png)

### 支持的标签及对应的 Dockerfile 链接

每个 Docker Official Image 的仓库描述中都包含一个**支持的标签及对应的 Dockerfile 链接**部分，列出了所有当前标签以及指向创建这些标签镜像的 Dockerfile 的链接。该部分的目的是展示可用的镜像变体。

![示例：Ubuntu 支持的标签](../images/supported_tags.webp)

同一行上列出的标签都指向相同的基础镜像。多个标签可以指向同一个镜像。例如，在前面的截图中，来自 `ubuntu` Docker Official Images 仓库的标签 `24.04`、`noble-20240225`、`noble` 和 `devel` 都指向同一个镜像。

Docker Official Image 的 `latest` 标签通常针对易用性进行了优化，并包含各种有用的软件，如开发者和构建工具。通过将镜像标记为 `latest`，镜像维护者实质上是在建议将该镜像作为默认使用。换句话说，如果您不知道该使用哪个标签或对底层软件不熟悉，您应该从 `latest` 镜像开始。随着您对软件和镜像变体的理解加深，您可能会发现其他镜像变体更适合您的需求。

### Slim 镜像

一些语言栈，如 [Node.js](https://hub.docker.com/_/node/)、[Python](https://hub.docker.com/_/python/) 和 [Ruby](https://hub.docker.com/_/ruby/)，提供了 `slim` 标签变体，旨在提供轻量级、生产就绪的基础镜像，包含更少的软件包。

`slim` 镜像的典型使用模式是作为[多阶段构建](https://docs.docker.com/build/building/multi-stage/)最终阶段的基础镜像。例如，您可以在构建的第一阶段使用 `latest` 变体构建应用程序，然后将应用程序复制到基于 `slim` 变体的最终阶段。以下是一个示例 `Dockerfile`。

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

许多 Docker Official Images 仓库也提供 `alpine` 变体。这些镜像基于 [Alpine Linux](https://www.alpinelinux.org/) 发行版构建，而不是 Debian 或 Ubuntu。Alpine Linux 专注于为容器镜像提供小型、简单且安全的基础，Docker Official Images 的 `alpine` 变体通常只安装必要的软件包。因此，Docker Official Images 的 `alpine` 变体通常比 `slim` 变体更小。

需要注意的主要问题是，Alpine Linux 使用 [musl libc](https://musl.libc.org/) 而不是 [glibc](https://www.gnu.org/software/libc/)。此外，为了最小化镜像大小，基于 Alpine 的镜像通常默认不包含 Git 或 Bash 等工具。根据您的程序对 libc 要求的深度或假设，您可能会遇到缺少库或工具的问题。

当您使用 Alpine 镜像作为基础时，请考虑以下选项，以使您的程序兼容 Alpine Linux 和 musl：

- 使用 musl libc 编译您的程序
- 将 glibc 库静态链接到您的程序中
- 完全避免 C 依赖（例如，构建不使用 CGO 的 Go 程序）
- 在您的 Dockerfile 中自行添加所需的软件。

如果您不熟悉如何安装软件包，请参考 Docker Hub 上 `alpine` 镜像的[描述](https://hub.docker.com/_/alpine)中的示例。

### 代号

带有看起来像《玩具总动员》角色（例如 `bookworm`、`bullseye` 和 `trixie`）或形容词（例如 `jammy` 和 `noble`）的标签，表示它们用作基础镜像的 Linux 发行版的代号。Debian 的发行代号[基于《玩具总动员》角色](https://en.wikipedia.org/wiki/Debian_version_history#Naming_convention)，而 Ubuntu 的代号采用“形容词+动物”的形式。例如，Ubuntu 24.04 的代号是“Noble Numbat”。

Linux 发行版指示符很有用，因为许多 Docker Official Images 提供了基于多个底层发行版版本的变体（例如 `postgres:bookworm` 和 `postgres:bullseye`）。

### 其他标签

除了此处描述的标签外，Docker Official Images 的标签可能还包含其他关于其镜像变体用途的提示。通常，这些标签变体在 Docker Official Images 仓库文档中有解释。阅读“如何使用此镜像”和“镜像变体”部分将帮助您理解如何使用这些变体。

### 解决拉取失败问题

如果您在拉取 Docker Official Images 时遇到问题，请检查 `DOCKER_CONTENT_TRUST` 环境变量是否设置为 `1`。从 2025 年 8 月起，Docker Official Images 的 Docker Content Trust 签名证书开始过期。要解决拉取失败问题，请取消设置 `DOCKER_CONTENT_TRUST` 环境变量。有关更多详细信息，请参阅 [DCT 退役博客文章](https://www.docker.com/blog/retiring-docker-content-trust/)。

## 已验证发布者镜像（Verified Publisher images）

Docker 已验证发布者计划（Docker Verified Publisher program）提供了由 Docker 验证的商业发布者的高质量镜像。

这些镜像帮助开发团队构建安全的软件供应链，在早期阶段最大限度地减少对恶意内容的暴露，从而节省后续时间和成本。

属于该计划的项目在 Docker Hub 上有一个特殊标记，便于用户识别 Docker 已验证为高质量商业发布者的项目。

![Docker-Verified Publisher badge](../images/verified-publisher-badge-iso.png)

## Docker 赞助的开源软件镜像（Docker-Sponsored Open Source Software images）

Docker 赞助的开源软件（OSS）计划提供了由 Docker 赞助的开源项目发布和维护的镜像。

属于该计划的项目在 Docker Hub 上有一个特殊标记，便于用户识别 Docker 已验证为可信、安全且活跃的开源项目。

![Docker-Sponsored Open Source badge](../images/sponsored-badge-iso.png)