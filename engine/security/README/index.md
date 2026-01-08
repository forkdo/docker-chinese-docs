# 
build:
  list: never
  publishResources: false
  render: never---
build:
  list: never
  publishResources: false
  render: never---
这是为了更方便地测试 protect-access.md 文档中的 TLS (HTTPS) 示例所做的初步尝试。

目前，这是一个手动操作的过程，我一直在 boot2docker 中运行它。

我的操作流程如下：

    $ boot2docker ssh
    root@boot2docker:/# git clone https://github.com/moby/moby
    root@boot2docker:/# cd docker/docs/articles/https
    root@boot2docker:/# make cert

有很多内容需要查看并手动回答，因为 openssl 需要交互式操作

> [!NOTE]: 确保在提示输入 `Computer Name` 时输入主机名（在我的情况下是 `boot2docker`）

    root@boot2docker:/# sudo make run

启动另一个终端：

    $ boot2docker ssh
    root@boot2docker:/# cd docker/docs/articles/https
    root@boot2docker:/# make client

最后一步首先使用 `--tls` 连接，然后使用 `--tlsverify` 连接，两者都应该成功。
