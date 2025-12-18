---
title: 获取 Docker Desktop 
keywords: 概念, 容器, docker desktop
description: 本概念页面将教你下载 Docker Desktop 并在 Windows、Mac 和 Linux 上安装
summary: |
  启动并运行 Docker Desktop 是开发人员进入容器化领域的第一步，它提供了无缝且用户友好的界面来管理 Docker 容器。Docker Desktop 简化了在容器中构建、共享和运行应用程序的过程，确保不同环境之间的一致性。
weight: 1
aliases:
 - /getting-started/get-docker-desktop/
---

{{< youtube-embed C2bPVhiNU-0 >}}

## 说明

Docker Desktop 是一个一体化软件包，用于构建镜像、运行容器以及更多功能。本指南将引导你完成安装过程，让你亲身体验 Docker Desktop。

> **Docker Desktop 使用条款**
>
> 大型企业（超过 250 名员工或年收入超过 1000 万美元）商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/?_gl=1*1nyypal*_ga*MTYxMTUxMzkzOS4xNjgzNTM0MTcw*_ga_XJWPQMJYHQ*MTcxNjk4MzU4Mi4xMjE2LjEuMTcxNjk4MzkzNS4xNy4wLjA.)。

<div class="not-prose">
{{< card
  title="Docker Desktop for Mac"
  description="[下载 (Apple Silicon)](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-arm64) | [下载 (Intel)](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-amd64) | [安装说明](/desktop/setup/install/mac-install)"
  icon="/icons/AppleMac.svg" >}}

{{< card
  title="Docker Desktop for Windows"
  description="[下载](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-windows) | [安装说明](/desktop/setup/install/windows-install)"
  icon="/icons/Windows.svg" >}}

{{< card
  title="Docker Desktop for Linux"
  description="[安装说明](/desktop/setup/install/linux/)"
  icon="/icons/Linux.svg" >}}
</div>

安装完成后，完成设置过程，你就可以开始运行 Docker 容器了。

## 动手试试

在本实践指南中，你将学习如何使用 Docker Desktop 运行 Docker 容器。

按照说明使用 CLI 运行容器。

## 运行你的第一个容器

打开你的 CLI 终端，通过运行 `docker run` 命令启动一个容器：

```console
$ docker run -d -p 8080:80 docker/welcome-to-docker
```

## 访问前端

对于这个容器，前端可通过端口 `8080` 访问。要在浏览器中打开网站，请访问 [http://localhost:8080](http://localhost:8080)。

![Nginx web 服务器的登录页面截图，来自正在运行的容器](../docker-concepts/the-basics/images/access-the-frontend.webp?border=true)

## 使用 Docker Desktop 管理容器

1. 打开 Docker Desktop，选择左侧边栏中的 **Containers** 字段。
2. 你可以查看容器的信息，包括日志、文件，甚至通过选择 **Exec** 选项卡来访问 shell。

   ![Docker Desktop 中正在运行的容器的 exec 截图](images/exec-into-docker-container.webp?border=true)

3. 选择 **Inspect** 字段以获取容器的详细信息。你可以执行各种操作，如暂停、恢复、启动或停止容器，或探索 **Logs**、**Bind mounts**、**Exec**、**Files** 和 **Stats** 选项卡。

![Docker Desktop 中正在运行的容器的检查截图](images/inspecting-container.webp?border=true)

Docker Desktop 通过简化应用程序在不同环境中的设置、配置和兼容性，简化了开发人员的容器管理，从而解决了环境不一致和部署挑战的痛点。

## 下一步是什么？

现在你已经安装了 Docker Desktop 并运行了你的第一个容器，是时候开始使用容器进行开发了。

{{< button text="使用容器开发" url="develop-with-containers" >}}
