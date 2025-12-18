---
description: 自动化构建的工作原理
keywords: docker hub, 自动化构建
title: 自动化构建
weight: 90
aliases:
- /docker-hub/builds/how-builds-work/
---

{{< summary-bar feature_name="Automated builds" >}}

Docker Hub 可以自动从外部仓库中的源代码构建镜像，并将构建好的镜像自动推送到你的 Docker 仓库。

![自动化构建仪表盘](images/index-dashboard.png)

当你配置自动化构建（也称为 autobuilds）时，你需要创建一个分支和标签列表，指定哪些需要构建为 Docker 镜像。当你向外部代码仓库（例如 GitHub）中的某个源代码分支推送代码时，推送操作会通过 webhook 触发一次新的构建，生成 Docker 镜像。构建好的镜像随后被推送到 Docker Hub。

> [!NOTE]
>
> 你仍然可以使用 `docker push` 将预构建的镜像推送到已配置自动化构建的仓库。

如果你配置了自动化测试，这些测试会在构建后、推送注册中心之前运行。你可以利用这些测试创建持续集成工作流，让测试失败的构建不会推送构建的镜像。自动化测试本身不会自行将镜像推送到注册中心。[了解自动化镜像测试](automated-testing.md)。

根据你的 [订阅计划](https://www.docker.com/pricing)，
你可能获得并发构建功能，这意味着可以同时运行 `N` 个自动化构建。`N` 的值根据你的订阅计划配置。一旦运行的构建数量达到 `N+1`，额外的构建将进入队列等待稍后执行。

队列中待处理构建的最大数量为 30，Docker Hub 会丢弃后续的请求。Pro 订阅的并发构建数量为 5，Team 和 Business 订阅为 15。
自动化构建可以处理最大 10 GB 的镜像。