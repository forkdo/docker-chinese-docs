---
title: Docker Offload 故障排除
linktitle: 故障排除
weight: 800
description: 了解如何解决 Docker Offload 的问题。
keywords: cloud, troubleshooting, cloud mode, Docker Desktop, cloud builder, usage
tags: [Troubleshooting]
---

Docker Offload 需要满足以下条件：

- 已认证
- 活跃的互联网连接
- 没有严格的代理或防火墙阻止与 Docker Cloud 的通信
- 已获得 Docker Offload 访问权限
- Docker Desktop 4.50 或更高版本

Docker Desktop 使用 Offload 在云端运行构建和容器。
如果构建或容器无法运行、回退到本地执行，或报告会话错误，请按照以下步骤解决该问题。

1. 确保 Docker Desktop 中已启用 Docker Offload：

   1. 打开 Docker Desktop 并登录。
   2. 进入 **Settings** > **Docker Offload**。
   3. 确保 **Enable Docker Offload** 已开启。

2. 使用以下命令检查连接是否处于活跃状态：

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

5. 使用 `docker login` 验证认证状态。

6. 如有必要，可以先退出再重新登录：

   ```console
   $ docker logout
   $ docker login
   ```

7. 检查使用情况和计费信息。更多信息请参阅 [Docker Offload 使用情况](/offload/usage/)。