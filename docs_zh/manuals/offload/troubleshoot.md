---
title: 故障排除 Docker Offload
linktitle: 故障排除
weight: 800
description: 了解如何排查 Docker Offload 相关问题。
tags:
- Troubleshooting
keywords: cloud, troubleshooting, cloud mode, Docker Desktop, cloud builder, usage
---

Docker Offload 需要满足以下条件：

- 身份验证
- 活跃的互联网连接
- 没有限制性代理或防火墙阻止通往 Docker Cloud 的流量
- 访问 Docker Offload 的权限
- Docker Desktop 4.50 或更高版本

Docker Desktop 使用 Offload 在云端运行构建和容器。
如果构建或容器运行失败、回退到本地运行或报告会话错误，请使用以下步骤来帮助解决问题。

1. 确保在 Docker Desktop 中启用了 Docker Offload：

   1. 打开 Docker Desktop 并登录。
   2. 前往 **Settings** > **Docker Offload**。
   3. 确保 **Enable Docker Offload** 已开启。

2. 使用以下命令检查连接是否活跃：

   ```console
   $ docker offload status
   ```

3. 要获取更多信息，请运行以下命令：

   ```console
   $ docker offload diagnose
   ```

4. 如果未连接，请启动一个新会话：

   ```console
   $ docker offload start
   ```

5. 使用 `docker login` 验证身份验证。

6. 如果需要，您可以先登出再重新登录：

   ```console
   $ docker logout
   $ docker login
   ```

7. 验证您的使用情况和账单。更多信息，请参阅 [Docker Offload 使用情况](/offload/usage/)。