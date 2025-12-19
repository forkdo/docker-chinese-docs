---
title: 构建镜像
weight: 20
keywords: 构建镜像, Dockerfile, 层, 标签, 推送, 缓存, 多阶段构建
description: |
  学习如何从 Dockerfile 构建 Docker 镜像。你将了解 Dockerfile 的结构、如何构建镜像以及如何自定义构建过程。
summary: |
  构建容器镜像既是一门技术也是一门艺术。你既要保持镜像的小巧和专注以提高安全态势，同时还需要平衡潜在的权衡，比如缓存影响。在本系列中，你将深入探索镜像的奥秘、它们的构建方式以及最佳实践。
layout: series
params:
  skill: 初级
  time: 25 分钟
  prereq: 无
---

## 关于本系列

学习如何构建适合生产的、精简高效的 Docker 镜像，这对于最小化开销并增强生产环境中的部署至关重要。

## 你将学到什么

- 理解镜像层
- 编写 Dockerfile
- 构建、标记和发布镜像
- 使用构建缓存
- 多阶段构建