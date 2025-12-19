---
_build:
  list: never
  publishResources: false
  render: never
---

这是为了简化 protect-access.md 文档中 TLS（HTTPS）示例测试的初步尝试。

目前这需要手动操作，我一直在 boot2docker 中运行它。

我的操作流程如下：

    $ boot2docker ssh
    root@boot2docker:/# git clone https://github.com/moby/moby
    root@boot2docker:/# cd docker/docs/articles/https
    root@boot2docker:/# make cert

会看到很多提示信息，需要手动回答，因为 openssl 需要交互式操作

> [!NOTE]：当提示输入 `Computer Name` 时，请确保输入主机名（我的情况是 `boot2docker`）

    root@boot2docker:/# sudo make run

启动另一个终端：

    $ boot2docker ssh
    root@boot2docker:/# cd docker/docs/articles/https
    root@boot2docker:/# make client

最后的命令会先使用 `--tls` 连接，然后使用 `--tlsverify` 连接，两者都应该成功。