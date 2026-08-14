---
title: "实验：构建容器镜像"
linkTitle: "实验：构建容器镜像"
description: |
  学习使用 Dockerfile 最佳实践构建生产级容器镜像——层缓存、
  多阶段构建、非 root 用户、基础镜像选择，以及安全的
  构建期密钥处理。
summary: |
  动手实验：把一个基础 Dockerfile 改造成生产可用的镜像。
  掌握层缓存、多阶段构建、.dockerignore、非 root 用户、
  基础镜像选择和构建密钥。
keywords: Docker, Dockerfile, images, multi-stage builds, layer caching, build secrets, lab, labspace
params:
  tags: [labs]
  time: 45 minutes
---

从一个能用但很朴素的 Dockerfile 出发，逐步将它改进为
生产级镜像。每一节引入一项技术，并应用到
一个真实的 Python Flask 应用上，让你直观看到效果。

## 启动实验

{{< labspace-launch image="dockersamples/labspace-building-images" >}}

## 你将学到什么

完成本 Labspace 后，你将掌握以下内容：

- 读懂镜像的层历史，理解层清理的陷阱
- 重构 Dockerfile，实现快速、高效利用缓存的增量构建
- 编写 `.dockerignore` 文件，并以非 root 用户运行容器
- 使用多阶段构建，把测试作为构建关卡，并大幅缩减镜像体积
- 为生产环境选择合适的基础镜像，包括 Docker Hardened Images
- 使用 `--mount=type=secret` 在构建期安全注入密钥

## 模块

| #   | 模块                       | 说明                                                                   |
| --- | -------------------------- | ---------------------------------------------------------------------- |
| 1   | 欢迎与首次构建             | 了解示例应用并构建初始镜像                                             |
| 2   | 理解镜像层                 | 用 `docker history` 检查镜像层，认识层清理的陷阱                       |
| 3   | Dockerfile 最佳实践        | 修正缓存顺序、添加 `.dockerignore`，并切换到非 root 用户               |
| 4   | 多阶段构建                 | 把测试作为构建关卡，并为生产阶段使用精简基础镜像                       |
| 5   | 选择基础镜像               | 对比 slim、Alpine 和 Docker Hardened Images                            |
| 6   | 构建密钥                   | 说明 `ARG` 为何会泄露密钥，并安全地使用 `--mount=type=secret`          |
| 7   | 总结                       | 回顾完整的最佳实践清单与后续步骤                                       |
