---
title: Docker 官方镜像
description: '本文介绍了 Docker 官方镜像（Docker Official Images）是如何创建的，

  以及如何参与贡献或提供反馈。

  '
keywords: docker official images, doi, contributing, upstream, open source
aliases:
- /trusted-content/official-images/contributing/
- /docker-hub/official_repos/
- /docker-hub/official_images/
---

> [!NOTE]
>
> Docker 正在逐步停用 Docker 官方镜像（DOI）的 Docker Content Trust (DCT)。
> 您应开始规划迁移到其他镜像签名和验证解决方案（例如 [Sigstore](https://www.sigstore.dev/) 或
> [Notation](https://github.com/notaryproject/notation#readme)）。Docker 将很快发布迁移指南，
> 以帮助您完成这一过渡。DCT 的完全弃用时间表正在最终确定，并将很快公布。
>
> 更多详情，请参阅
> https://www.docker.com/blog/retiring-docker-content-trust/。

Docker, Inc. 赞助了一个专门团队，负责审核并发布所有 Docker 官方镜像的内容。该团队与上游软件维护者、安全专家以及更广泛的 Docker 社区密切合作。

虽然理想情况下由上游软件作者维护其 Docker 官方镜像，但这并非强制性要求。创建和维护 Docker 官方镜像是一个协作过程，
在 [GitHub 上公开进行](https://github.com/docker-library/official-images)，并鼓励社区参与。任何人都可以提供反馈、贡献代码、
建议流程变更，甚至提议一个新的官方镜像。

## 创建 Docker 官方镜像

从高层次来看，官方镜像最初是以一组 GitHub Pull Request 的形式提出的。以下 GitHub 仓库详细说明了提案要求：

- [GitHub 上的 Docker 官方镜像仓库](https://github.com/docker-library/official-images#readme)
- [Docker 官方镜像文档](https://github.com/docker-library/docs#readme)

Docker 官方镜像团队在社区贡献者的帮助下，对每个提案进行正式审核，并向作者提供反馈。这一初步审核过程可能较为漫长，
在提案被接受前通常需要多次反复沟通。

审核过程中存在一些主观考量。这些主观问题最终归结为基本问题："这个镜像是否具有普遍用途？" 例如，
[Python](https://hub.docker.com/_/python/) Docker 官方镜像对更广泛的 Python 开发者社区是"普遍有用"的，
而上周用 Python 编写的某个冷门文字冒险游戏则不是。

一旦新提案被接受，作者需负责保持其镜像和文档的更新，并响应用户反馈。Docker 负责在 Docker Hub 上构建和发布这些镜像。
对 Docker 官方镜像的更新遵循与新镜像相同的 Pull Request 流程，但更新审核流程更为简化。Docker 官方镜像团队最终对所有变更进行把关，
这有助于确保一致性、质量和安全性。

## 为 Docker 官方镜像提交反馈

所有 Docker 官方镜像在其文档中都包含一个 **用户反馈（User Feedback）** 部分，涵盖该特定仓库的详细信息。
在大多数情况下，包含官方镜像 Dockerfile 的 GitHub 仓库也设有活跃的问题追踪系统。

关于 Docker 官方镜像的常规反馈和支持问题，应提交至 [Docker 社区 Slack](https://dockr.ly/comm-slack) 中的 `#general` 频道。

如果您是 Docker 官方镜像的维护者或贡献者，并寻求帮助或建议，请使用 [Libera.Chat IRC](https://libera.chat) 上的 `#docker-library` 频道。