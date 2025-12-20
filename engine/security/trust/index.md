# Docker 中的内容信任

在联网系统之间传输数据时，信任是一个核心问题。特别是通过互联网等不受信任的介质进行通信时，确保系统所操作的所有数据的完整性和发布者身份至关重要。您使用 Docker Engine 将镜像（数据）推送到公共或私有仓库或从中拉取。内容信任使您能够验证通过任何通道从仓库接收的所有数据的完整性和发布者。

## 关于 Docker 内容信任 (DCT)

Docker 内容信任 (DCT) 提供了对发送到远程 Docker 仓库和从远程 Docker 仓库接收的数据使用数字签名的能力。这些签名允许在客户端或运行时验证特定镜像标签的完整性和发布者。

通过 DCT，镜像发布者可以对其镜像进行签名，而镜像消费者可以确保他们拉取的镜像是经过签名的。发布者可以是手动签署其内容的个人或组织，也可以是作为其发布过程一部分签署内容的自动化软件供应链。

> [!NOTE]
>
> Docker 正在逐步淘汰 Docker 官方镜像 (DOI) 的 DCT。您应开始计划过渡到不同的镜像签名和验证解决方案（例如 [Sigstore](https://www.sigstore.dev/) 或 [Notation](https://github.com/notaryproject/notation#readme)）。DCT 完全弃用的时间表正在最终确定，并将很快公布。
>
> 有关更多信息，请参阅 [逐步淘汰 Docker 内容信任](https://www.docker.com/blog/retiring-docker-content-trust/)。

### 镜像标签和 DCT

单个镜像记录具有以下标识符：

```text
[REGISTRY_HOST[:REGISTRY_PORT]/]REPOSITORY[:TAG]
```

一个特定的镜像 `REPOSITORY` 可以有多个标签。例如，`latest` 和 `3.1.2` 都是 `mongo` 镜像的标签。镜像发布者可以多次构建镜像和标签组合，每次构建都更改镜像。

DCT 与镜像的 `TAG` 部分相关联。每个镜像仓库都有一组密钥，镜像发布者使用这些密钥对镜像标签进行签名。镜像发布者可以自行决定对哪些标签进行签名。

一个镜像仓库可以包含一个已签名的带标签镜像和另一个未签名的镜像。例如，考虑 [Mongo 镜像仓库](https://hub.docker.com/_/mongo/tags/)。`latest` 标签可能未签名，而 `3.1.6` 标签可能已签名。决定镜像标签是否签名是镜像发布者的责任。在此表示中，一些镜像标签已签名，另一些则没有：

![已签名的标签](images/tag_signing.png)

发布者可以选择对特定标签进行签名，也可以不签名。因此，未签名标签的内容与同名的已签名标签的内容可能不匹配。例如，发布者可以推送一个带标签的镜像 `someimage:latest` 并对其进行签名。稍后，同一个发布者可以推送一个未签名的 `someimage:latest` 镜像。这第二次推送会替换最后一个未签名的 `latest` 标签，但不会影响已签名的 `latest` 版本。选择对哪些标签进行签名的能力允许发布者在正式签名之前迭代镜像的未签名版本。

镜像消费者可以启用 DCT 来确保他们使用的镜像是经过签名的。如果消费者启用了 DCT，他们只能拉取、运行或使用受信任的镜像进行构建。启用 DCT 就像是为您的仓库应用了一个“过滤器”。消费者只能“看到”已签名的镜像标签，而不太理想的未签名镜像标签对他们来说是“不可见”的。

![信任视图](images/trust_view.png)

对于未启用 DCT 的消费者，他们使用 Docker 镜像的方式不会有任何变化。无论镜像是否签名，所有镜像都是可见的。

### Docker 内容信任密钥

镜像标签的信任是通过使用签名密钥来管理的。首次调用使用 DCT 的操作时会创建一组密钥。密钥集由以下几类密钥组成：

- 一个离线密钥，它是镜像标签 DCT 的根
- 对标签进行签名的仓库或标签密钥
- 服务器管理的密钥，例如时间戳密钥，它为您的仓库提供新鲜度安全性保证

下图描述了各种签名密钥及其关系：

![内容信任组件](images/trust_components.png)

> [!WARNING]
>
> 根密钥一旦丢失便无法恢复。如果您丢失了任何其他密钥，请发送电子邮件至 [Docker Hub 支持](mailto:hub-support@docker.com)。此丢失还需要在丢失之前使用过来自此仓库的已签名标签的每个消费者进行手动干预。

您应将根密钥备份在安全的地方。鉴于它仅在创建新仓库时才需要，最好将其离线存储在硬件中。有关保护和备份密钥的详细信息，请务必阅读如何[管理 DCT 的密钥](trust_key_mng.md)。

## 使用 Docker 内容信任对镜像进行签名

在 Docker CLI 中，我们可以使用 `$ docker trust` 命令语法来签名和推送容器镜像。这是建立在 Notary 功能集之上的。有关更多信息，请参阅 [Notary GitHub 存储库](https://github.com/theupdateframework/notary)。

对镜像进行签名的先决条件是 Docker Registry 附带 Notary 服务器（例如 Docker Hub）。请参阅[部署 Notary](/engine/security/trust/deploying_notary/) 以获取说明。

> [!NOTE]
>
> Docker 正在逐步淘汰 Docker 官方镜像 (DOI) 的 DCT。您应开始计划过渡到不同的镜像签名和验证解决方案（例如 [Sigstore](https://www.sigstore.dev/) 或 [Notation](https://github.com/notaryproject/notation#readme)）。DCT 完全弃用的时间表正在最终确定，并将很快公布。
>
> 有关更多信息，请参阅 [逐步淘汰 Docker 内容信任](https://www.docker.com/blog/retiring-docker-content-trust/)。

要对 Docker 镜像进行签名，您需要一个委派密钥对。这些密钥可以使用 `$ docker trust key generate` 在本地生成，也可以由证书颁发机构生成。

首先，我们将委派私钥添加到本地 Docker 信任仓库。（默认情况下，它存储在 `~/.docker/trust/` 中）。如果您使用 `$ docker trust key generate` 生成委派密钥，私钥会自动添加到本地信任存储中。如果您要导入单独的密钥，则需要使用 `$ docker trust key load` 命令。

```console
$ docker trust key generate jeff
Generating key for jeff...
Enter passphrase for new jeff key with ID 9deed25:
Repeat passphrase for new jeff key with ID 9deed25:
Successfully generated and loaded private key. Corresponding public key available: /home/ubuntu/Documents/mytrustdir/jeff.pub
```

或者，如果您有一个现有的密钥：

```console
$ docker trust key load key.pem --name jeff
Loading key from "key.pem"...
Enter passphrase for new jeff key with ID 8ae710e:
Repeat passphrase for new jeff key with ID 8ae710e:
Successfully imported key from key.pem
```

接下来，我们需要将委派公钥添加到 Notary 服务器；这特定于 Notary 中称为全局唯一名称 (GUN) 的特定镜像仓库。如果这是您第一次向该仓库添加委派，此命令还将使用本地 Notary 规范根密钥来启动仓库。要了解有关启动仓库和委派角色的更多信息，请前往[内容信任的委派](trust_delegation.md)。

```console
$ docker trust signer add --key cert.pem jeff registry.example.com/admin/demo
Adding signer "jeff" to registry.example.com/admin/demo...
Enter passphrase for new repository key with ID 10b5e94:
```

最后，我们将使用委派私钥对特定标签进行签名，并将其推送到仓库。

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

或者，一旦密钥被导入，可以通过导出 DCT 环境变量，使用 `$ docker push` 命令推送镜像。

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

可以使用 `$ docker trust inspect` 命令查看标签或仓库的远程信任数据：

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

可以使用 `$ docker trust revoke` 命令删除标签的远程信任数据：

```console
$ docker trust revoke registry.example.com/admin/demo:1
Enter passphrase for signer key with ID 8ae710e:
Successfully deleted signature for registry.example.com/admin/demo:1
```

## 使用 Docker 内容信任进行客户端强制执行

内容信任在 Docker 客户端中默认禁用。要启用它，请将 `DOCKER_CONTENT_TRUST` 环境变量设置为 `1`。这会阻止用户使用带标签的镜像，除非它们包含签名。

当在 Docker 客户端中启用 DCT 时，对带标签镜像进行操作的 `docker` CLI 命令必须包含内容签名或显式内容哈希。使用 DCT 的命令是：

* `push`
* `build`
* `create`
* `pull`
* `run`

例如，启用 DCT 后，`docker pull someimage:latest` 仅在 `someimage:latest` 已签名时才会成功。但是，只要哈希存在，使用显式内容哈希的操作总是会成功：

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

* [内容信任的委派](trust_delegation.md)
* [内容信任的自动化](trust_automation.md)
* [管理内容信任的密钥](trust_key_mng.md)
* [在内容信任沙盒中体验](trust_sandbox.md)

- [使用 Compose 部署 Notary Server](https://docs.docker.com/engine/security/trust/deploying_notary/)

- [使用内容信任实现自动化](https://docs.docker.com/engine/security/trust/trust_automation/)

- [内容信任的委托](https://docs.docker.com/engine/security/trust/trust_delegation/)

- [在内容信任沙盒中进行操作](https://docs.docker.com/engine/security/trust/trust_sandbox/)

- [管理内容信任的密钥](https://docs.docker.com/engine/security/trust/trust_key_mng/)

