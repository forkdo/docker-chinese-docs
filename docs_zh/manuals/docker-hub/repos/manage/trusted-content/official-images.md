---
title: Docker 官方镜像
description: |
  本文介绍 Docker 官方镜像是如何创建的，
  以及如何参与贡献或提供反馈。
keywords: docker official images, doi, 贡献, 上游, 开源
aliases:
- /trusted-content/official_repos/
- /docker-hub/official_repos/
- /docker-hub/official_images/
---

> [!NOTE]
>
> Docker 正在逐步淘汰 Docker 官方镜像 (DOI) 的 Docker 内容信任 (DCT) 功能。
> 您应开始计划迁移到其他镜像签名和验证解决方案（如 [Sigstore](https://www.sigstore.dev/) 或
> [Notation](https://github.com/notaryproject/notation#readme)）。Docker 将很快发布迁移指南，
> 以帮助您完成这一工作。DCT 完全弃用的时间表正在最终确定，将很快公布。
>
> 更多详细信息，请参阅
> https://www.docker.com/blog/retiring-docker-content-trust/.

Docker 公司赞助了一个专门的团队，负责审查和发布 Docker 官方镜像中的所有内容。
该团队与上游软件维护者、安全专家和更广泛的 Docker 社区协作。

虽然最好由上游软件作者来维护他们的 Docker 官方镜像，但这并不是一个硬性要求。
为 Docker 官方镜像创建和维护镜像是一个协作过程。
它在 [GitHub 上公开进行](https://github.com/docker-library/official-images)，
鼓励社区参与。任何人都可以提供反馈、贡献代码、建议流程变更，甚至提议一个新的官方镜像。

## 创建 Docker 官方镜像

从高层次来看，官方镜像始于一组 GitHub Pull Request 形式的提案。以下 GitHub 仓库详细说明了提案要求：

- [GitHub 上的 Docker 官方镜像仓库](https://github.com/docker-library/official-images#readme)
- [Docker 官方镜像文档](https://github.com/docker-library/docs#readme)

Docker 官方镜像团队在社区贡献者的帮助下，正式审查每个提案并向作者提供反馈。
初始审查过程可能比较长，通常需要多次来回讨论，提案才能被接受。

审查过程中存在一些主观考虑因素。这些主观问题归结为一个基本问题：
“这个镜像是否具有普遍实用性？”例如，[Python](https://hub.docker.com/_/python/)
Docker 官方镜像对更广泛的 Python 开发者社区来说是“普遍有用的”，而上周用 Python 编写的一个晦涩的文字冒险游戏则不然。

一旦新提案被接受，作者就有责任保持其镜像和文档的更新，并响应用户反馈。
Docker 负责构建和在 Docker Hub 上发布镜像。Docker 官方镜像的更新遵循与新镜像相同的 Pull Request 流程，
尽管更新的审查流程更加简化。Docker 官方镜像团队最终充当所有变更的把关者，这有助于确保一致性、质量和安全性。

## 提交 Docker 官方镜像的反馈

所有 Docker 官方镜像的文档中都包含一个 **用户反馈** 部分，其中涵盖该特定仓库的详细信息。
在大多数情况下，包含官方镜像 Dockerfile 的 GitHub 仓库也有一个活跃的问题跟踪器。

关于 Docker 官方镜像的一般反馈和支持问题应提交到 [Docker 社区 Slack](https://dockr.ly/comm-slack) 的 `#general` 频道。

如果您是 Docker 官方镜像的维护者或贡献者，并且正在寻求帮助或建议，请使用 [Libera.Chat IRC](https://libera.chat) 上的 `#docker-library` 频道。