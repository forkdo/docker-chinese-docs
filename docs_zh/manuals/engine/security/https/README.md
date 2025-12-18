---
_build:
  list: never
  publishResources: false
  render: never
---

这是一个初步尝试，旨在简化测试 protect-access.md 文档中 TLS（HTTPS）示例的过程。

目前这还是一个手动操作，我一直在 boot2docker 中运行它。

我的操作流程如下：

    $ boot2docker ssh
    root@boot2docker:/# git clone https://github.com/moby/moby
    root@boot2docker:/# cd docker/docs/articles/https
    root@boot2docker:/# make cert

会看到很多输出，需要手动回答一些问题，因为 openssl 需要交互式操作

> [!NOTE]: 确保在提示输入 `Computer Name` 时输入主机名（我的情况是 `boot2docker`）

    root@boot2docker:/# sudo make run

再打开一个终端：

    $ boot2docker ssh
    root@boot2docker:/# cd docker/docs/articles/https
    root@boot2docker:/# make client

最后一步会先用 `--tls` 连接，然后用 `--tlsverify` 连接，两者都应该成功。