---
title: 下一步
keywords: concepts, build, images, container, docker desktop
description: 探索循序渐进的指南，帮助你深入理解 Docker 的核心概念、构建镜像以及运行容器。
aliases:
 - /guides/getting-started/whats-next/
summary: |
  现在你已经安装并配置了 Docker Desktop，使用容器进行开发，并构建和推送了你的第一个镜像，接下来可以更深入地了解容器的工作原理。
notoc: true
weight: 4

the-basics:
- title: 什么是容器？
  description: 学习如何运行你的第一个容器。
  link: /get-started/docker-concepts/the-basics/what-is-a-container/
- title: 什么是镜像？
  description: 了解镜像层的基础知识。
  link: /get-started/docker-concepts/the-basics/what-is-an-image/
- title: 什么是注册中心？
  description: 了解容器注册中心，探索它们的互操作性，并与注册中心进行交互。
  link: /get-started/docker-concepts/the-basics/what-is-a-registry/
- title: 什么是 Docker Compose？
  description: 更深入地了解 Docker Compose。
  link: /get-started/docker-concepts/the-basics/what-is-docker-compose/

building-images:
- title: 理解镜像层
  description: 了解容器镜像的分层结构。
  link: /get-started/docker-concepts/building-images/understanding-image-layers/
- title: 编写 Dockerfile
  description: 学习如何使用 Dockerfile 创建镜像。
  link: /get-started/docker-concepts/building-images/writing-a-dockerfile/
- title: 构建、标记并发布镜像
  description: 学习如何构建、标记并推送到 Docker Hub 或其他注册中心。
  link: /get-started/docker-concepts/building-images/build-tag-and-publish-an-image/
- title: 使用构建缓存
  description: 了解构建缓存、哪些更改会失效缓存，以及如何有效利用构建缓存。
  link: /get-started/docker-concepts/building-images/using-the-build-cache/
- title: 多阶段构建
  description: 更深入地了解多阶段构建及其优势。
  link: /get-started/docker-concepts/building-images/multi-stage-builds/

running-containers:
- title: 发布端口
  description: 理解在 Docker 中发布和暴露端口的重要性。
  link: /get-started/docker-concepts/running-containers/publishing-ports/
- title: 覆盖容器默认值
  description: 学习如何使用 `docker run` 命令覆盖容器的默认设置。
  link: /get-started/docker-concepts/running-containers/overriding-container-defaults/
- title: 持久化容器数据
  description: 学习 Docker 中数据持久化的重要性。
  link: /get-started/docker-concepts/running-containers/persisting-container-data/
- title: 与容器共享本地文件
  description: 探索 Docker 中可用的各种存储选项及其常见用法。
  link: /get-started/docker-concepts/running-containers/sharing-local-files/
- title: 多容器应用
  description: 了解多容器应用的重要性，以及它们与单容器应用的区别。
  link: /get-started/docker-concepts/running-containers/multi-container-applications/
---

以下部分提供了循序渐进的指南，帮助你深入理解 Docker 的核心概念、构建镜像以及运行容器。

## 基础知识

从学习容器、镜像、注册中心和 Docker Compose 的核心概念开始。

{{< grid items="the-basics" >}}

## 构建镜像

使用 Dockerfile、构建缓存和多阶段构建，打造优化的容器镜像。

{{< grid items="building-images" >}}

## 运行容器

掌握暴露端口、覆盖默认值、持久化数据、共享文件以及管理多容器应用的关键技术。

{{< grid items="running-containers" >}}