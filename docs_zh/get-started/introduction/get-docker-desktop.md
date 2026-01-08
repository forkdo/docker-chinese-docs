---
title: 获取 Docker Desktop
keywords: concepts, container, docker desktop
description: 本概念页面将指导您下载 Docker Desktop 并在 Windows、Mac 和 Linux 上进行安装
summary: '启动并运行 Docker Desktop 是开发者迈入容器化领域的首要关键步骤，它提供了一个无缝且用户友好的界面来管理 Docker 容器。Docker Desktop 简化了在容器中构建、共享和运行应用程序的过程，确保了不同环境之间的一致性。

  '
weight: 1
aliases:
- /getting-started/get-docker-desktop/
---

{{< youtube-embed C2bPVhiNU-0 >}}

## 解释

Docker Desktop 是用于构建镜像、运行容器等操作的一站式软件包。
本指南将引导您完成安装过程，让您能够亲身体验 Docker Desktop。

> **Docker Desktop 使用条款**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/?_gl=1*1nyypal*_ga*MTYxMTUxMzkzOS4xNjgzNTM0MTcw*_ga_XJWPQMJYHQ*MTcxNjk4MzU4Mi4xMjE2LjEuMTcxNjk4MzkzNS4xNy4wLjA.)。

<div class="not-prose">
{{< card
  title="适用于 Mac 的 Docker Desktop"
  description="[下载 (Apple Silicon)](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-arm64) | [下载 (Intel)](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-amd64) | [安装说明](/desktop/setup/install/mac-install)"
  icon="/icons/AppleMac.svg" >}}

{{< card
  title="适用于 Windows 的 Docker Desktop"
  description="[下载](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-windows) | [安装说明](/desktop/setup/install/windows-install)"
  icon="/icons/Windows.svg" >}}

{{< card
  title="适用于 Linux 的 Docker Desktop"
  description="[安装说明](/desktop/setup/install/linux/)"
  icon="/icons/Linux.svg" >}}
</div>

安装完成后，完成设置过程，您就可以运行 Docker 容器了。

## 动手尝试

在本实践指南中，您将了解如何使用 Docker Desktop 运行 Docker 容器。

按照说明使用 CLI 运行容器。

## 运行您的第一个容器

打开您的 CLI 终端，通过运行 `docker run` 命令来启动一个容器：

```console
$ docker run -d -p 8080:80 docker/welcome-to-docker
```

## 访问前端

对于此容器，前端可在端口 `8080` 上访问。要打开网站，请在浏览器中访问 [http://localhost:8080](http://localhost:8080)。

![来自正在运行的容器的 Nginx Web 服务器登录页面截图](../docker-concepts/the-basics/images/access-the-frontend.webp?border=true)

## 使用 Docker Desktop 管理容器

1. 打开 Docker Desktop 并在左侧边栏中选择 **Containers**（容器）区域。
2. 您可以查看有关容器的信息，包括日志和文件，甚至可以通过选择 **Exec**（执行）选项卡访问 shell。

   ![在 Docker Desktop 中进入正在运行的容器的截图](images/exec-into-docker-container.webp?border=true)

3. 选择 **Inspect**（检查）区域以获取有关容器的详细信息。您可以执行各种操作，例如暂停、恢复、启动或停止容器，或者浏览 **Logs**（日志）、**Bind mounts**（绑定挂载）、**Exec**（执行）、**Files**（文件）和 **Stats**（统计信息）选项卡。

![在 Docker Desktop 中检查正在运行的容器的截图](images/inspecting-container.webp?border=true)

Docker Desktop 通过简化应用程序在不同环境中的设置、配置和兼容性，为开发人员简化了容器管理，从而解决了环境不一致和部署挑战的痛点。

## 下一步是什么？

现在您已经安装了 Docker Desktop 并运行了您的第一个容器，是时候开始使用容器进行开发了。

{{< button text="使用容器进行开发" url="develop-with-containers" >}}