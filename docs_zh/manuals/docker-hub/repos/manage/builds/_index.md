---
description: 自动构建的工作原理
keywords: docker hub, automated builds
title: 自动构建
weight: 90
aliases:
- /docker-hub/builds/how-builds-work/
---

{{< summary-bar feature_name="Automated builds" >}}

Docker Hub 可以自动从外部仓库中的源代码构建镜像，并将构建好的镜像自动推送到您的 Docker 仓库。

![自动构建仪表板](images/index-dashboard.png)

当您设置自动构建（也称为 autobuilds）时，您需要创建一个分支和标签的列表，这些分支和标签将被构建成 Docker 镜像。当您将代码推送到源代码分支（例如在 GitHub 中）时，如果该分支对应于您列出的某个镜像标签，则该推送操作会使用 webhook 触发一次新的构建，从而生成一个 Docker 镜像。随后，构建好的镜像会被推送到 Docker Hub。

> [!NOTE]
>
> 您仍然可以使用 `docker push` 将预构建的镜像推送到已配置自动构建的仓库中。

如果您配置了自动化测试，这些测试将在构建之后、推送到注册表之前运行。您可以使用这些测试来创建一个持续集成工作流：如果构建未能通过测试，则不会推送构建的镜像。自动化测试本身不会将镜像推送到注册表。[了解更多关于自动化镜像测试的信息](automated-testing.md)。

根据您的[订阅计划](https://www.docker.com/pricing)，您可能会获得并发构建能力，这意味着可以同时运行 `N` 个自动构建。`N` 的值根据您的订阅计划进行配置。一旦有 `N+1` 个构建正在运行，任何额外的构建将进入队列，稍后运行。

队列中待处理构建的最大数量为 30，Docker Hub 会丢弃超出此数量的后续请求。Pro 订阅的并发构建数为 5，Team 和 Business 订阅的并发构建数为 15。
自动构建可以处理最大 10 GB 大小的镜像。