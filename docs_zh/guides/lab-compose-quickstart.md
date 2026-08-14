---
title: "实验：Docker Compose 快速上手"
linkTitle: "实验：Docker Compose 快速上手"
description: |
  使用 Docker Compose 从零构建一个 Flask 与 Redis 组成的多容器应用。
  学习健康检查、watch 模式、命名卷以及多文件
  配置。
summary: |
  动手实验：使用 Docker Compose 定义并运行多容器应用。
  从一个最简 compose.yaml 出发，逐步加入健康检查、借助 watch 模式的
  实时开发、数据持久化，以及模块化的 Compose 文件组合。
keywords: Docker, Compose, multi-container, Flask, Redis, watch mode, volumes, lab, labspace
params:
  tags: [labs]
  time: 45 minutes
---

使用 Docker Compose 构建一个 Python Flask 与 Redis 的访问计数应用，从一个
最简的 `compose.yaml` 开始，在每一步中逐步加入生产级
特性。

## 启动实验

{{< labspace-launch image="dockersamples/labspace-compose-quickstart" >}}

## 你将学到什么

完成本 Labspace 后，你将掌握以下内容：

- 在 `compose.yaml` 文件中定义多服务应用，并用 Compose 命令管理它
- 使用健康检查和 `depends_on` 条件控制服务的启动顺序
- 使用 Compose watch 模式迭代代码，无需手动重新构建
- 使用命名卷让数据在容器重启后依然保留
- 使用 `include` 指令将技术栈拆分到多个文件中实现模块化
- 使用 `config`、`logs` 和 `exec` 检查并调试运行中的技术栈

## 模块

| #   | 模块                             | 说明                                                                  |
| --- | -------------------------------- | --------------------------------------------------------------------- |
| 1   | 引言                             | 浏览初始应用并验证环境                                                |
| 2   | 定义服务                         | 编写第一个 `compose.yaml`，启动 Flask 与 Redis 技术栈                 |
| 3   | 健康检查与启动顺序               | 添加 Redis 健康检查和 `depends_on`，消除竞态条件                      |
| 4   | 使用 watch 模式实时开发          | 配置 watch 模式，无需手动重建即可同步代码变更                         |
| 5   | 持久化与调试                     | 添加命名卷，让 Redis 数据在 `docker compose down` 后依然保留          |
| 6   | 使用多个 Compose 文件            | 将 Redis 抽取到 `infra.yaml`，并用 `include` 组合各文件               |
| 7   | 其他命令                         | 使用 `config`、`logs -f` 和 `exec` 检查运行中的技术栈                 |
| 8   | 回顾                             | 回顾所构建的内容并探索后续步骤                                        |
