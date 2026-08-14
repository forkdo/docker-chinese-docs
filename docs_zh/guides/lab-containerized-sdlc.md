---
title: "实验：容器化的软件开发生命周期"
linkTitle: "实验：容器化的 SDLC"
description: |
  构建一个 Node.js API，并将软件开发
  生命周期的每个阶段都容器化——本地开发、集成测试、CI/CD 以及 Kubernetes
  部署。
summary: |
  动手实验：使用 Docker Compose、Testcontainers、Gitea Actions CI/CD 和 kubectl，
  把一个 Node.js 应用从源码一路送到 Kubernetes 上线部署——
  在 SDLC 的每个阶段都用上容器。
keywords: Docker, Compose, Testcontainers, Kubernetes, CI/CD, SDLC, lab, labspace
params:
  tags: [labs]
  time: 60 minutes
---

构建一个真实的 Node.js API，然后在软件
开发生命周期的每个阶段应用容器。你将为本地开发编写 Compose 文件、
使用 Testcontainers 编写集成测试、搭建 CI/CD 流水线，并编写 Kubernetes
清单——且全程使用同一个容器镜像。

## 启动实验

{{< labspace-launch image="dockersamples/labspace-containerized-sdlc" browserUrl="http://dockerlabs.xyz" >}}

## 你将学到什么

完成本 Labspace 后，你将掌握以下内容：

- 使用 Docker Compose 和 Compose Watch 搭建容器化的本地开发环境
- 编写集成测试，用 Testcontainers 启动一个真实的数据库
- 构建 CI/CD 流水线，自动完成测试、构建并推送容器镜像
- 编写 Kubernetes 清单，并把应用部署到 k3s 集群上线运行
- 配置流水线，使每次推送到 `main` 都触发自动部署

## 模块

| #   | 模块                                      | 说明                                                                     |
| --- | ----------------------------------------- | ------------------------------------------------------------------------ |
| 1   | 引言：认识应用                            | 浏览 TaskFlow API，了解接下来的 SDLC 旅程                                |
| 2   | 使用 Docker Compose 进行本地开发          | 编写 `compose.yaml`，准备本地数据库和可视化工具                          |
| 3   | 容器化你的开发环境                        | 将应用加入 Compose，并通过 Compose Watch 实现热重载                      |
| 4   | 使用 Testcontainers 进行集成测试          | 编写自包含测试，启动真实的 PostgreSQL 容器                               |
| 5   | 使用 Gitea Actions 进行持续集成           | 搭建流水线，完成测试、构建并推送容器镜像                                 |
| 6   | 部署到 Kubernetes                         | 编写清单并部署到 k3s 集群，实现自动化滚动发布                            |
| 7   | 容器化的 SDLC：回顾                       | 回顾在可移植性、一致性和可复现性方面的收益                               |
