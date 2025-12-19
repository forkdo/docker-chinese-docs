---
description: 部署 Notary
keywords: trust, security, notary, deployment
title: 使用 Compose 部署 Notary Server
---

部署 Notary Server 最简单的方法是使用 Docker Compose。要执行本页的操作，您必须已经[安装了 Docker Compose](/manuals/compose/install/_index.md)。

1. 克隆 Notary 仓库。
   
   ```console
   $ git clone https://github.com/theupdateframework/notary.git
   ```

2. 使用示例证书构建并启动 Notary Server。

   ```console
   $ docker compose up -d 
   ```

   有关如何部署 Notary Server 的更详细文档，请参阅[运行 Notary 服务的说明](https://github.com/theupdateframework/notary/blob/master/docs/running_a_service.md)，以及[ Notary 仓库](https://github.com/theupdateframework/notary)以获取更多信息。

3. 在尝试与 Notary 服务器交互之前，请确保您的 Docker 或 Notary 客户端信任 Notary Server 的证书。

根据您使用的是 Docker 还是 Notary，请参见 [Docker 的说明](/reference/cli/docker/#notary)或 [Notary 的说明](https://github.com/docker/notary#using-notary)。

## 如果您想在生产环境中使用 Notary

在 Notary Server 发布官方稳定版本后，请返回此处查看相关说明。若您希望提前了解如何在生产环境中部署 Notary，请参阅[ Notary 仓库](https://github.com/theupdateframework/notary)。