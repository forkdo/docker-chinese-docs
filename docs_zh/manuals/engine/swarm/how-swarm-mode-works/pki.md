---
description: Swarm 模式中 PKI 的工作原理
keywords: swarm, security, tls, pki,
title: 使用公钥基础设施 (PKI) 管理 Swarm 安全
---

Docker 内置的 Swarm 模式公钥基础设施 (PKI) 系统使您能够轻松安全地部署容器编排系统。Swarm 中的节点使用相互传输层安全 (TLS) 来验证、授权并与 Swarm 中的其他节点进行加密通信。

当您通过运行 `docker swarm init` 创建 Swarm 时，Docker 将自身指定为管理器节点。默认情况下，管理器节点会生成一个新的根证书颁发机构 (CA) 及其密钥对，用于保护与其他加入 Swarm 的节点之间的通信安全。如果您愿意，也可以使用 `docker swarm init` 命令的 `--external-ca` 标志指定您自己生成的外部根 CA。

管理器节点还会生成两个令牌，用于将其他节点加入 Swarm：一个工作节点令牌和一个管理器令牌。每个令牌包含根 CA 证书的摘要和一个随机生成的密钥。当节点加入 Swarm 时，加入的节点使用摘要来验证来自远程管理器的根 CA 证书。远程管理器使用密钥确保加入的节点是已获批准的节点。

每当有新节点加入 Swarm 时，管理器会向该节点颁发证书。该证书包含一个随机生成的节点 ID，用作证书通用名称 (CN) 下的节点标识符和组织单位 (OU) 下的角色。节点 ID 在节点当前 Swarm 生命周期内作为加密安全的节点标识。

下图说明了管理器节点和工作节点如何使用至少 TLS 1.2 来加密通信：

![TLS diagram](/engine/swarm/images/tls.webp?w=600)

以下示例显示了工作节点证书的信息：

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

默认情况下，Swarm 中的每个节点每三个月会自动续订其证书。您可以通过运行 `docker swarm update --cert-expiry <TIME PERIOD>` 命令来配置此间隔。最小轮换值为 1 小时。详细信息请参考 [docker swarm update](/reference/cli/docker/swarm/update.md) CLI 参考文档。

## 轮换 CA 证书

> [!NOTE]
>
> Mirantis Kubernetes Engine (MKE)，以前称为 Docker UCP，为 Swarm 提供外部证书管理器服务。如果您在 MKE 上运行 Swarm，则不应手动轮换 CA 证书。请改用联系 Mirantis 支持以轮换证书。

在集群 CA 密钥或管理器节点遭到泄露的情况下，您可以轮换 Swarm 根 CA，使所有节点不再信任由旧根 CA 签名的证书。

运行 `docker swarm ca --rotate` 以生成新的 CA 证书和密钥。如果您愿意，可以传递 `--ca-cert` 和 `--external-ca` 标志来指定根证书并使用 Swarm 外部的根 CA。或者，您也可以传递 `--ca-cert` 和 `--ca-key` 标志来指定 Swarm 要使用的精确证书和密钥。

当您发出 `docker swarm ca --rotate` 命令时，以下事件按顺序发生：

1.  Docker 生成一个交叉签名的证书。这意味着新根 CA 证书的一个版本使用旧根 CA 证书签名。这个交叉签名的证书用作所有新节点证书的中间证书。这确保了仍然信任旧根 CA 的节点仍然可以验证由新 CA 签名的证书。

2.  Docker 还告诉所有节点立即续订其 TLS 证书。此过程可能需要几分钟，具体取决于 Swarm 中节点的数量。

3.  在 Swarm 中的每个节点都获得由新 CA 签名的新 TLS 证书后，Docker 会忘记旧 CA 证书和密钥材料，并告诉所有节点仅信任新 CA 证书。

    这也会导致 Swarm 加入令牌的变化。之前的加入令牌不再有效。

从这一点开始，所有新颁发的节点证书都由新根 CA 签名，不包含任何中间证书。

## 了解更多

* 了解 [节点](nodes.md) 的工作原理。
* 了解 Swarm 模式 [服务](services.md) 的工作原理。