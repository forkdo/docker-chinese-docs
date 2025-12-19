---
description: PKI 在 swarm 模式下的工作原理
keywords: swarm, security, tls, pki,
title: 使用公钥基础设施 (PKI) 管理 swarm 安全性
---

Docker 内置的 Swarm 模式公钥基础设施 (PKI) 系统
使得安全部署容器编排系统变得简单。Swarm 中的节点
使用相互传输层安全协议 (TLS) 来验证、授权
并加密与 swarm 中其他节点的通信。

当您通过运行 `docker swarm init` 创建 swarm 时，Docker 将自身指定为
管理器节点。默认情况下，管理器节点会生成一个新的根证书颁发机构 (CA)
以及一个密钥对，用于保护与加入 swarm 的其他节点的通信。如果愿意，您可以
使用 [docker swarm init](/reference/cli/docker/swarm/init.md) 命令的 `--external-ca` 标志
指定您自己外部生成的根 CA。

管理器节点还会生成两个令牌，用于将其他节点加入 swarm：
一个工作器令牌和一个管理器令牌。每个令牌
包含根 CA 证书的摘要以及随机生成的
密钥。当节点加入 swarm 时，加入节点使用该摘要来
验证来自远程管理器的根 CA 证书。远程管理器
使用该密钥来确保加入节点是已获批准的节点。

每当有新节点加入 swarm 时，管理器都会向该节点颁发证书。
该证书包含一个随机生成的节点 ID，用于在证书通用名 (CN) 下
标识节点，并在组织单位 (OU) 下标识角色。节点 ID 在节点于当前 swarm 中的
整个生命周期内充当加密安全的节点身份。

下图说明了管理器节点和工作器节点如何使用至少 TLS 1.2 来加密
通信。

![TLS diagram](/engine/swarm/images/tls.webp?w=600)

以下示例显示了来自工作器节点的证书信息：

```text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            3b:1c:06:91:73:fb:16:ff:69:c3:f7:a2:fe:96:c1:73:e2:80:97:3b
        Signature Algorithm: ecdsa-with-SHA256
        Issuer: CN=swarm-ca
        Validity
            Not Before: Aug 30 02:39:00 2016 GMT
            Not After : Nov 28 03:39:00 2016 GMT
        Subject: O=ec2adilxf4ngv7ev8fwsi61i7, OU=swarm-worker, CN=dw02poa4vqvzxi5c10gm4pq2g
...snip...
```

默认情况下，swarm 中的每个节点每三个月续订一次其证书。
您可以通过运行 `docker swarm update --cert-expiry <TIME PERIOD>` 命令
配置此间隔。最小轮换值为 1 小时。有关详细信息，请参阅
[docker swarm update](/reference/cli/docker/swarm/update.md) CLI
参考。

## 轮换 CA 证书

> [!NOTE]
>
> Mirantis Kubernetes Engine (MKE)，前身为 Docker UCP，为 swarm 提供了外部
> 证书管理器服务。如果您在 MKE 上运行 swarm，则不应
> 手动轮换 CA 证书。如果您需要轮换证书，请联系 Mirantis 支持部门。

如果集群 CA 密钥或管理器节点遭到入侵，您可以
轮换 swarm 根 CA，这样所有节点都不再信任
由旧根 CA 签名的证书。

运行 `docker swarm ca --rotate` 以生成新的 CA 证书和密钥。如果
愿意，您可以传递 `--ca-cert` 和 `--external-ca` 标志来指定
根证书并使用 swarm 外部的根 CA。或者，
您可以传递 `--ca-cert` 和 `--ca-key` 标志来指定您希望 swarm 使用的确切
证书和密钥。

当您发出 `docker swarm ca --rotate` 命令时，以下事情会按顺序发生：

1.  Docker 生成一个交叉签名的证书。这意味着新根 CA 证书的
    一个版本由旧根 CA 证书签名。
    此交叉签名证书用作所有新节点证书的中间证书。这确保了
    仍然信任旧根 CA 的节点仍然可以验证由新 CA 签名的证书。

2.  Docker 还会告诉所有节点立即续订其 TLS 证书。
    此过程可能需要几分钟，具体取决于 swarm 中的节点数量。

3.  在 swarm 中的每个节点都拥有由新 CA 签名的新 TLS 证书后，
    Docker 会忘记旧的 CA 证书和密钥材料，并告诉
    所有节点仅信任新的 CA 证书。

    这也会导致 swarm 的加入令牌发生更改。之前的
    加入令牌不再有效。

从此时起，所有颁发的新节点证书都由新的根 CA 签名，
并且不包含任何中间证书。

## 了解更多

* 阅读有关[节点](nodes.md)工作原理的内容。
* 了解 Swarm 模式[服务](services.md)的工作原理。