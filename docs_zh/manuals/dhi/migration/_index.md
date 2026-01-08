---
title: 迁移
description: 了解如何将现有应用程序迁移到 Docker Hardened Images
weight: 18
keywords: migrate, docker hardened images, dhi, migration guide
aliases:
- /dhi/how-to/migrate/
params:
  grid_migration_paths:
  - title: 使用 Docker 的 AI 助手进行迁移
    description: 使用 Docker 的 AI 助手，在指导和建议下自动将您的 Dockerfile 迁移到 Docker Hardened Images。
    icon: smart_toy
    link: /dhi/migration/migrate-with-ai/
  - title: 从 Alpine 或 Debian 镜像迁移
    description: 从 Docker 官方镜像（基于 Alpine 或 Debian）迁移到 Docker Hardened Images 的手动迁移指南。
    icon: code
    link: /dhi/migration/migrate-from-doi/
  - title: 从 Wolfi 迁移
    description: 从基于 Wolfi 的镜像过渡到 Docker Hardened Images 的手动迁移指南。
    icon: transform
    link: /dhi/migration/migrate-from-wolfi/
  grid_migration_resources:
  - title: 迁移检查清单
    description: 全面的迁移注意事项清单，确保成功过渡到 Docker Hardened Images。
    icon: checklist
    link: /dhi/migration/checklist/
  - title: 示例
    description: 针对不同编程语言和框架的 Dockerfile 迁移示例，为您的迁移过程提供指导。
    icon: preview
    link: /dhi/migration/examples/
---

本节提供将您的应用程序迁移到 Docker Hardened Images (DHI) 的指导。迁移到 DHI 可通过利用具有内置安全功能的强化基础镜像，增强容器化应用程序的安全状况。

## 迁移路径

选择最适合您需求的迁移方法：

{{< grid items="grid_migration_paths" >}}

## 资源

{{< grid items="grid_migration_resources" >}}