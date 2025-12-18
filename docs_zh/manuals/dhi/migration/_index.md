---
title: 迁移
description: 了解如何将现有应用程序迁移到 Docker Hardened Images
weight: 18
keywords: 迁移, docker hardened images, dhi, 迁移指南
aliases:
  - /dhi/how-to/migrate/
params:
  grid_migration_paths:
    - title: 使用 Docker AI 助手迁移
      description: 使用 Docker AI 助手自动将您的 Dockerfile 迁移到 Docker Hardened Images，并获得指导和建议。
      icon: smart_toy
      link: /dhi/migration/migrate-with-ai/
    - title: 从 Alpine 或 Debian 镜像迁移
      description: 从 Docker 官方镜像（基于 Alpine 或 Debian）迁移到 Docker Hardened Images 的手动迁移指南。
      icon: code
      link: /dhi/migration/migrate-from-doi/
    - title: 从 Wolfi 迁移
      description: 从基于 Wolfi 的镜像迁移到 Docker Hardened Images 的手动迁移指南。
      icon: transform
      link: /dhi/migration/migrate-from-wolfi/
  
  grid_migration_resources:
    - title: 迁移清单
      description: 一份全面的迁移注意事项清单，确保您成功过渡到 Docker Hardened Images。
      icon: checklist
      link: /dhi/migration/checklist/
    - title: 示例
      description: 不同编程语言和框架的 Dockerfile 迁移示例，指导您的迁移过程。
      icon: preview
      link: /dhi/migration/examples/
---

本节提供将您的应用程序迁移到 Docker Hardened Images (DHI) 的指导。通过利用具有内置安全功能的加固基础镜像，迁移到 DHI 可以增强您容器化应用程序的安全性。

## 迁移路径

选择最适合您需求的迁移方式：

{{< grid items="grid_migration_paths" >}}

## 资源

{{< grid items="grid_migration_resources" >}}