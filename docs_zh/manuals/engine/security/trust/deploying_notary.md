---
description: 部署 Notary
keywords: trust, security, notary, deployment
title: 使用 Compose 部署 Notary Server
---

部署 Notary Server 最简单的方法是使用 Docker Compose。要执行本页面的步骤，你必须已经[安装 Docker Compose](/manuals/compose/install/_index.md)。

1. 克隆 Notary 仓库。

   ```console
   $ git clone https://github.com/theupdateframework/notary.git
   ```

2. 使用示例证书构建并启动 Notary Server。

   ```console
   $ docker compose up -d 
   ```

   有关如何部署 Notary Server 的更详细文档，请参阅[运行 Notary 服务的说明](https://github.com/theupdateframework/notary/blob/master/docs/running_a_service.md)，以及[Notary 仓库](https://github.com/theupdateframework/notary)获取更多信息。

3. 在尝试与 Notary 服务器交互之前，请确保你的 Docker 或 Notary 客户端信任 Notary Server 的证书。

请参阅 [Docker](/reference/cli/docker/#notary) 或 [Notary](https://github.com/docker/notary#using-notary) 的说明，具体取决于你使用的是哪一个。

## 如果你想在生产环境中使用 Notary

请在 Notary Server 发布正式稳定版本后，回到此处查看说明。若要提前开始在生产环境中部署 Notary，可参阅[Notary 仓库](https://github.com/theupdateframework/notary)。