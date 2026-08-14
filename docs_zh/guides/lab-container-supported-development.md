---
title: "实验：容器辅助开发"
linkTitle: "实验：容器辅助开发"
description: |
  通过运行 PostgreSQL
  数据库、编写 Compose 文件并添加 pgAdmin 开发工具，学习如何用容器进行本地开发——无需在本地
  安装任何软件。
summary: |
  动手实验：在本地开发过程中用容器运行依赖服务。
  启动 PostgreSQL 数据库、编写 compose.yaml，并添加一个数据库
  可视化工具——全程无需在主机上安装任何东西。
keywords: Docker, Compose, local development, PostgreSQL, pgAdmin, containers, lab, labspace
params:
  tags: [labs]
  time: 30 minutes
---

用容器运行应用所依赖的服务——数据库、缓存、
消息队列——无需在本地安装任何软件。本实验将带你
在容器中运行 PostgreSQL，编写一份可供整个团队共享的 `compose.yaml`，
并向开发技术栈中加入 pgAdmin 可视化工具。

## 启动实验

{{< labspace-launch image="dockersamples/labspace-container-supported-development" >}}

## 你将学到什么

完成本 Labspace 后，你将掌握以下内容：

- 无需本地安装，在容器中运行 PostgreSQL 数据库
- 使用绑定挂载，在启动时为数据库注入表结构和初始数据
- 编写 `compose.yaml`，把整个开发技术栈固化下来供团队使用
- 添加 pgAdmin 容器来可视化和检查数据库
- 理解容器化开发技术栈如何缩短上手时间、减少环境漂移

## 模块

| #   | 模块                             | 说明                                                                            |
| --- | -------------------------------- | ------------------------------------------------------------------------------- |
| 1   | 引言                             | 认识示例应用，理解容器辅助开发的思路                                            |
| 2   | 运行容器化数据库                 | 启动 PostgreSQL、连接应用，并使用绑定挂载为数据库注入初始数据                   |
| 3   | 用 Compose 让工作更轻松          | 用共享的 `compose.yaml` 取代 `docker run` 命令                                  |
| 4   | 添加开发工具                     | 向 Compose 技术栈中加入 pgAdmin 以实现数据库可视化                              |
| 5   | 回顾                             | 回顾关键要点并探索相关指南                                                      |
