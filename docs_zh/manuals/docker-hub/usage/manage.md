---
description: 了解如何优化和管理您的 Docker Hub 使用情况。
keywords: Docker Hub, 限制, 使用
title: 优化 Docker Hub 使用情况的最佳实践
linkTitle: 优化使用
weight: 40
---

请使用以下步骤来帮助优化和管理个人及组织的 Docker Hub 使用情况：

1. [查看您的 Docker Hub 使用情况](https://hub.docker.com/usage)。

2. 使用 Docker Hub 使用数据来识别哪些账户消耗的数据最多，确定使用的高峰期，并识别与最大数据使用量相关的镜像。此外，查找使用趋势，例如：

   - 低效的拉取行为：识别频繁访问的仓库，以评估是否可以优化缓存实践或整合使用以减少拉取次数。
   - 低效的自动化系统：检查哪些自动化工具（如 CI/CD 流水线）可能导致较高的拉取频率，并配置它们以避免不必要的镜像拉取。

3. 通过以下方式优化镜像拉取：

   - 使用缓存：通过 [镜像](/docker-hub/mirror/) 或在 CI/CD 流水线中实现本地镜像缓存，以减少冗余拉取。
   - 自动化手动工作流：通过配置自动化系统仅在有新版本镜像可用时才拉取，以避免不必要的拉取。

4. 通过以下方式优化存储：

    - 定期审核并 [删除整个仓库](../repos/delete.md)，移除未标记、未使用或过时的镜像。
    - 使用 [镜像管理](../repos/manage/hub-images/manage.md) 删除仓库中的陈旧和过时镜像。

5. 对于组织，请通过以下方式监控并执行组织策略：

   - 定期 [查看 Docker Hub 使用情况](https://hub.docker.com/usage) 以监控使用情况。
   - [强制登录](/security/for-admins/enforce-sign-in/) 以确保您可以监控用户的使用情况，并让用户获得更高的使用限制。
   - 查找 Docker 中的重复用户账户，并根据需要从您的组织中移除账户。