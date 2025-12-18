---
description: 在 Docker 中启用内容信任
keywords: 内容, 信任, 安全, docker, 文档
title: Docker 中的内容信任
aliases:
- /engine/security/trust/content_trust/
- /notary/getting_started/
- /notary/advanced_usage/
- /notary/service_architecture/
- /notary/running_a_service/
- /notary/changelog/
- /notary/reference/server-config/
- /notary/reference/signer-config/
- /notary/reference/client-config/
- /notary/reference/common-configs/
---

在网路系统之间传输数据时，信任是一个核心问题。特别是当通过像互联网这样的不可信媒介通信时，确保系统所操作的所有数据的完整性和发布者至关重要。你使用 Docker Engine 向公共或私有注册表推送和拉取镜像（数据）。内容信任让你能够验证从注册表通过任何通道接收到的所有数据的完整性和发布者。

## 关于 Docker 内容信任（DCT）

Docker 内容信任（DCT）提供了对发送到和从远程 Docker 注册表接收的数据进行数字签名的能力。这些签名允许客户端或运行时验证特定镜像标签的完整性和发布者。

通过 DCT，镜像发布者可以对其镜像进行签名，镜像消费者可以确保他们拉取的镜像是已签名的。发布者可能是手动签名其内容的个人或组织，也可能是作为其发布过程一部分签名内容的自动化软件供应链。

> [!NOTE]
>
> Docker 正在弃用 Docker 官方镜像（DOI）的 DCT。
> 你应该开始计划迁移到其他镜像签名和验证解决方案（如 [Sigstore](https://www.sigstore.dev/) 或
> [Notation](https://github.com/notaryproject/notation#readme)）。DCT 完全弃用的时间表正在最终确定，很快将发布。
>
> 有关更多信息，请参阅 [弃用 Docker 内容信任](https://www.docker.com/blog/retiring-docker-content-trust/)。

### 镜像标签和 DCT

单个镜像记录具有以下标识符：

```text
[REGISTRY_HOST[:REGISTRY_PORT]/]REPOSITORY[:TAG]
```

特定的镜像 `REPOSITORY` 可以有多个标签。例如，`latest` 和 `3.1.2` 都是 `mongo` 镜像的标签。镜像发布者可以多次构建镜像和标签组合，并在每次构建时更改镜像。

DCT 与镜像的 `TAG` 部分关联。每个镜像仓库都有一组密钥，镜像发布者使用这些密钥来签名镜像标签。镜像发布者可以自行决定签名哪些标签。

一个镜像仓库可能包含一个已签名的标签和另一个未签名的标签。例如，考虑 [Mongo 镜像仓库](https://hub.docker.com/_/mongo/tags/)。`latest` 标签可能是未签名的，而 `3.1.6` 标签可能是已签名的。镜像发布者负责决定镜像标签是否已签名。在此表示中，某些镜像标签已签名，其他则未签名：

![Signed tags](images/tag_signing.png)

发布者可以选择签名特定标签或不签名。因此，具有相同名称的未签名标签内容和已签名标签内容可能不匹配。例如，发布者可以推送一个标签镜像 `someimage:latest` 并对其进行签名。稍后，同一发布者可以推送一个未签名的 `someimage:latest` 镜像。第二次推送会替换最后一个未签名的标签 `latest`，但不会影响已签名的 `latest` 版本。选择可以签名哪些标签的能力允许发布者在正式签名之前在未签名版本上进行迭代。

镜像消费者可以启用 DCT 以确保他们使用的镜像是已签名的。如果消费者启用了 DCT，他们只能拉取、运行或构建受信任的镜像。启用 DCT 就像对你的注册表应用一个“过滤器”。消费者“看到”的只是已签名的镜像标签，而不太理想的未签名镜像标签对他们来说是“不可见”的。

![Trust view](images/trust_view.png)

对于未启用 DCT 的消费者，他们使用 Docker 镜像的方式没有任何改变。无论镜像是否已签名，每个镜像都是可见的。

### Docker 内容信任密钥

镜像标签的信任通过使用签名密钥进行管理。首次调用使用 DCT 的操作时会创建一个密钥集。密钥集由以下类别的密钥组成：

- 作为镜像标签 DCT 根的离线密钥
- 签名标签的仓库或标签密钥
- 服务器管理的密钥，如时间戳密钥，为你的仓库提供新鲜度安全保证

下图描绘了各种签名密钥及其关系：

![Content Trust components](images/trust_components.png)

> [!WARNING]
>
> 一旦丢失根密钥就无法恢复。如果你丢失了任何其他密钥，请发送电子邮件至 [Docker Hub 支持](mailto:hub-support@docker.com)。这种丢失也需要每个在此丢失之前使用过此仓库签名标签的消费者进行手动干预。

你应该将根密钥备份到安全的地方。鉴于它仅用于创建新仓库，最好将其离线存储在硬件中。有关保护和备份密钥的详细信息，请确保你阅读了如何[管理 DCT 密钥](trust_key_mng.md)。

## 使用 Docker 内容信任签名镜像

在 Docker CLI 中，我们可以使用 `$ docker trust` 命令语法签名并推送容器镜像。这是基于 Notary 功能集构建的。有关更多信息，请参阅 [Notary GitHub 仓库](https://github.com/theupdateframework/notary)。

签名 Docker 镜像的先决条件是一个带有附加 Notary 服务器的 Docker 注册表（如 Docker Hub）。请参阅 [部署 Notary](/engine/security/trust/deploying_notary/) 获取说明。

> [!NOTE]
>
> Docker 正在弃用 Docker 官方镜像（DOI）的 DCT。
> 你应该开始计划迁移到其他镜像签名和验证解决方案（如 [Sigstore](https://www.sigstore.dev/) 或
> [Notation](https://github.com/notaryproject/notation#readme)）。DCT 完全弃用的时间表正在最终确定，很快将发布。
>
> 有关更多信息，请参阅 [弃用 Docker 内容信任](https://www.docker.com/blog/retiring-docker-content-trust/)。

要签名 Docker 镜像，你需要一个委托密钥对。这些密钥可以使用 `$ docker trust key generate` 本地生成，也可以由证书颁发机构生成。

首先，我们将委托私钥添加到本地 Docker 信任仓库。（默认情况下，这存储在 `~/.docker/trust/` 中）。如果你正在使用 `$ docker trust key generate` 生成委托密钥，私钥会自动添加到本地信任存储中。如果你正在导入单独的密钥，你需要使用 `$ docker trust key load` 命令。

```console
$ docker trust key generate jeff
Generating key for jeff...
Enter passphrase for new jeff key with ID 9deed25:
Repeat passphrase for new jeff key with ID 9deed25:
Successfully generated and loaded private key. Corresponding public key available: /home/ubuntu/Documents/mytrustdir/jeff.pub
```

或者，如果你有现有密钥：

```console
$ docker trust key load key.pem --name jeff
Loading key from "key.pem"...
Enter passphrase for new jeff key with ID 8ae710e:
Repeat passphrase for new jeff key with ID 8ae710e:
Successfully imported key from key.pem
```

接下来，我们需要将委托公钥添加到 Notary 服务器；这特定于 Notary 中的特定镜像仓库，称为全局唯一名称（GUN）。如果这是第一次向该仓库添加委托，此命令还将使用本地 Notary 规范根密钥初始化仓库。要了解有关初始化仓库和委托角色的更多信息，请访问[内容信任的委托](trust_delegation.md)。

```console
$ docker trust signer add --key cert.pem jeff registry.example.com/admin/demo
Adding signer "jeff" to registry.example.com/admin/demo...
Enter passphrase for new repository key with ID 10b5e94:
```

最后，我们将使用委托私钥对特定标签进行签名，并将其推送到注册表。

```console
$ docker trust sign registry.example.com/admin/demo:1
Signing and pushing trust data for local image registry.example.com/admin/demo:1, may overwrite remote trust data
The push refers to repository [registry.example.com/admin/demo]
7bff100f35cb: Pushed
1: digest: sha256:3d2e482b82608d153a374df3357c0291589a61cc194ec4a9ca2381073a17f58e size: 528
Signing and pushing trust metadata
Enter passphrase for signer key with ID 8ae710e:
Successfully signed registry.example.com/admin/demo:1
```

或者，一旦密钥被导入，可以通过导出 DCT 环境变量来使用 `$ docker push` 命令推送镜像。

```console
$ export DOCKER_CONTENT_TRUST=1

$ docker push registry.example.com/admin/demo:1
The push refers to repository [registry.example.com/admin/demo:1]
7bff100f35cb: Pushed
1: digest: sha256:3d2e482b82608d153a374df3357c0291589a61cc194ec4a9ca2381073a17f58e size: 528
Signing and pushing trust metadata
Enter passphrase for signer key with ID 8ae710e:
Successfully signed registry.example.com/admin/demo:1
```

远程信任数据可以通过 `$ docker trust inspect` 命令查看：

```console
$ docker trust inspect --pretty registry.example.com/admin/demo:1

Signatures for registry.example.com/admin/demo:1

SIGNED TAG          DIGEST                                                             SIGNERS
1                   3d2e482b82608d153a374df3357c0291589a61cc194ec4a9ca2381073a17f58e   jeff

List of signers and their keys for registry.example.com/admin/demo:1

SIGNER              KEYS
jeff                8ae710e3ba82

Administrative keys for registry.example.com/admin/demo:1

  Repository Key:	10b5e94c916a0977471cc08fa56c1a5679819b2005ba6a257aa78ce76d3a1e27
  Root Key:	84ca6e4416416d78c4597e754f38517bea95ab427e5f95871f90d460573071fc
```

远程信任数据可以通过 `$ docker trust revoke` 命令删除：

```console
$ docker trust revoke registry.example.com/admin/demo:1
Enter passphrase for signer key with ID 8ae710e:
Successfully deleted signature for registry.example.com/admin/demo:1
```

## Docker 内容信任的客户端强制

内容信任在 Docker 客户端中默认禁用。要启用它，将 `DOCKER_CONTENT_TRUST` 环境变量设置为 `1`。这可以防止用户在没有签名的情况下使用标签镜像。

当在 Docker 客户端中启用 DCT 时，对标签镜像操作的 `docker` CLI 命令必须包含内容签名或显式内容哈希。与 DCT 一起使用的命令有：

* `push`
* `build`
* `create`
* `pull`
* `run`

例如，启用 DCT 后，只有当 `someimage:latest` 已签名时，`docker pull someimage:latest` 才会成功。但是，只要哈希存在，带有显式内容哈希的操作总是会成功：

```console
$ docker pull registry.example.com/user/image:1
Error: remote trust data does not exist for registry.example.com/user/image: registry.example.com does not have trust data for registry.example.com/user/image

$ docker pull registry.example.com/user/image@sha256:d149ab53f8718e987c3a3024bb8aa0e2caadf6c0328f1d9d850b2a2a67f2819a
sha256:ee7491c9c31db1ffb7673d91e9fac5d6354a89d0e97408567e09df069a1687c1: Pulling from user/image
ff3a5c916c92: Pull complete
a59a168caba3: Pull complete
Digest: sha256:ee7491c9c31db1ffb7673d91e9fac5d6354a89d0e97408567e09df069a1687c1
Status: Downloaded newer image for registry.example.com/user/image@sha256:ee7491c9c31db1ffb7673d91e9fac5d6354a89d0e97408567e09df069a1687c1
```

## 相关信息

* [内容信任的委托](trust_delegation.md)
* [内容信任的自动化](trust_automation.md)
* [管理内容信任的密钥](trust_key_mng.md)
* [在内容信任沙箱中练习](trust_sandbox.md)
