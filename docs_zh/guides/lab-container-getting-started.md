---
title: "实验：Docker 入门"
linkTitle: "实验：Docker 基础"
description: |
  通过运行容器、了解容器
  生命周期，并把一个真实的 Node.js 应用打包成自己的自定义镜像，学习 Docker 基础知识。
summary: |
  动手实验：运行你的第一个容器，编写 Dockerfile，从 Node.js 应用构建自定义
  镜像，并可选地将其推送到 Docker Hub。
keywords: Docker, containers, Dockerfile, images, getting started, lab, labspace
params:
  tags: [labs]
  time: 30 minutes
---

从零开始，学习 Docker 的核心组成要素。你将运行预构建的
容器，编写 `Dockerfile` 来打包一个 Node.js 应用，构建自己的
镜像，并亲眼见识容器的不可变性和隔离性。

## 启动实验

{{< labspace-launch image="dockersamples/labspace-container-getting-started" >}}

## 你将学到什么

完成本 Labspace 后，你将掌握以下内容：

- 理解什么是容器，以及它与虚拟机的区别
- 在后台运行容器，检查其日志和文件系统，并管理其生命周期
- 编写 `Dockerfile` 打包应用，并利用层缓存实现快速重建
- 使用 `docker build` 构建自定义镜像并以容器方式运行
- 可选地将镜像发布到 Docker Hub

## 模块

| #   | 模块                      | 说明                                                                           |
| --- | ------------------------- | ------------------------------------------------------------------------------ |
| 1   | 欢迎来到 Docker           | 容器简介，并运行你的第一个 `hello-world` 容器                                  |
| 2   | 运行容器                  | 启动 Nginx，查看日志和内部结构，并管理容器生命周期                             |
| 3   | 构建你的第一个镜像        | 编写 `Dockerfile`，从 Node.js 应用构建自定义镜像                               |
| 4   | 运行你的应用              | 运行你的镜像，体验容器隔离性，并可选地推送到 Docker Hub                        |
| 5   | 总结                      | 关键概念回顾与后续步骤                                                         |
