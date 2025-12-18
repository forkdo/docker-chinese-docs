---
description: 内容信任的委托
keywords: 信任, 安全, 委托, 密钥, 仓库
title: 内容信任的委托
aliases:
- /ee/dtr/user/access-dtr/configure-your-notary-client/
---

Docker 内容信任 (DCT) 中的委托允许您控制谁可以或不可以为镜像标签签名。委托将有一对私钥和公钥。委托可以包含多对密钥和贡献者，以 a) 允许多个用户成为委托的一部分，以及 b) 支持密钥轮换。

Docker 内容信任中最重要的委托是 `targets/releases`。这被视为可信镜像标签的规范来源，如果贡献者的密钥不在此委托下，他们将无法为标签签名。

幸运的是，当使用 `$ docker trust` 命令时，我们会自动初始化仓库、管理仓库密钥，并通过 `docker trust signer add` 将贡献者的密钥添加到 `targets/releases` 委托中。

## 配置 Docker 客户端

默认情况下，`$ docker trust` 命令期望的 notary 服务器 URL 与镜像标签中指定的注册表 URL 相同（遵循与 `$ docker push` 类似的逻辑）。在使用 Docker Hub 或 DTR 时，notary 服务器 URL 与注册表 URL 相同。但是，对于自托管环境或第三方注册表，您需要指定 notary 服务器的替代 URL。这可以通过以下方式完成：

```console
$ export DOCKER_CONTENT_TRUST_SERVER=https://<URL>:<PORT>
```

如果您在自托管环境中未导出此变量，您可能会看到如下错误：

```console
$ docker trust signer add --key cert.pem jeff registry.example.com/admin/demo
Adding signer "jeff" to registry.example.com/admin/demo...
<...>
Error: trust data missing for remote repository registry.example.com/admin/demo or remote repository not found: timestamp key trust data unavailable.  Has a notary repository been initialized?

$ docker trust inspect registry.example.com/admin/demo --pretty
WARN[0000] Error while downloading remote metadata, using cached timestamp - this might not be the latest version available remotely
<...>
```

如果您为 notary 服务器启用了身份验证，或者正在使用 DTR，您需要在将数据推送到 notary 服务器之前登录。

```console
$ docker login registry.example.com/user/repo
Username: admin
Password:

Login Succeeded

$ docker trust signer add --key cert.pem jeff registry.example.com/user/repo
Adding signer "jeff" to registry.example.com/user/repo...
Initializing signed repository for registry.example.com/user/repo...
Successfully initialized "registry.example.com/user/repo"
Successfully added signer: jeff to registry.example.com/user/repo
```

如果您未登录，您将看到：

```console
$ docker trust signer add --key cert.pem jeff registry.example.com/user/repo
Adding signer "jeff" to registry.example.com/user/repo...
Initializing signed repository for registry.example.com/user/repo...
you are not authorized to perform this operation: server returned 401.

Failed to add signer to: registry.example.com/user/repo
```

## 配置 Notary 客户端

DCT 的一些高级功能需要 Notary CLI。要安装和配置 Notary CLI：

1. 下载 [客户端](https://github.com/theupdateframework/notary/releases) 并确保它在您的路径中可用。

2. 在 `~/.notary/config.json` 创建一个配置文件，内容如下：

```json
{
  "trust_dir" : "~/.docker/trust",
  "remote_server": {
    "url": "https://registry.example.com",
    "root_ca": "../.docker/ca.pem"
  }
}
```

新创建的配置文件包含有关本地 Docker 信任数据位置和 notary 服务器 URL 的信息。

有关如何在 Docker 内容信任用例之外使用 notary 的更详细信息，请参阅 [Notary CLI 文档](https://github.com/theupdateframework/notary/blob/master/docs/command_reference.md)

## 创建委托密钥

添加第一个贡献者的先决条件是一对委托密钥。这些密钥可以使用 `$ docker trust` 本地生成，也可以由证书颁发机构生成。

### 使用 Docker Trust 生成密钥

Docker trust 内置了委托密钥对生成器，`$ docker trust generate <name>`。运行此命令将自动将委托私钥加载到本地 Docker 信任存储中。

```console
$ docker trust key generate jeff

Generating key for jeff...
Enter passphrase for new jeff key with ID 9deed25: 
Repeat passphrase for new jeff key with ID 9deed25: 
Successfully generated and loaded private key. Corresponding public key available: /home/ubuntu/Documents/mytrustdir/jeff.pub
```

### 手动生成密钥

如果您需要手动生成私钥（RSA 或 ECDSA）和包含公钥的 X.509 证书，您可以使用本地工具如 openssl 或 cfssl 以及本地或公司范围的证书颁发机构。

以下是如何生成 2048 位 RSA 部分密钥的示例（所有 RSA 密钥必须至少为 2048 位）：

```console
$ openssl genrsa -out delegation.key 2048

Generating RSA private key, 2048 bit long modulus
....................................................+++
............+++
e is 65537 (0x10001)
```

他们应该将 `delegation.key` 保密，因为它用于签名标签。

然后他们需要生成包含公钥的 x509 证书，这是您需要从他们那里获得的。以下是生成 CSR（证书签名请求）的命令：

```console
$ openssl req -new -sha256 -key delegation.key -out delegation.csr
```

然后他们可以将其发送给他们信任的 CA 来签署证书，或者他们可以自签名证书（在此示例中，创建一个有效期为 1 年的证书）：

```console
$ openssl x509 -req -sha256 -days 365 -in delegation.csr -signkey delegation.key -out delegation.crt
```

然后他们需要将 `delegation.crt` 给您，无论它是自签名的还是由 CA 签名的。

最后，您需要将私钥添加到您的本地 Docker 信任存储中。

```console
$ docker trust key load delegation.key --name jeff

Loading key from "delegation.key"...
Enter passphrase for new jeff key with ID 8ae710e: 
Repeat passphrase for new jeff key with ID 8ae710e: 
Successfully imported key from delegation.key
```

### 查看本地委托密钥

要列出已导入本地 Docker 信任存储的密钥，我们可以使用 Notary CLI。

```console
$ notary key list

ROLE       GUN                          KEY ID                                                              LOCATION
----       ---                          ------                                                              --------
root                                    f6c6a4b00fefd8751f86194c7d87a3bede444540eb3378c4a11ce10852ab1f96    /home/ubuntu/.docker/trust/private
jeff                                    9deed251daa1aa6f9d5f9b752847647cf8d705da0763aa5467650d0987ed5306    /home/ubuntu/.docker/trust/private
```

## 管理 Notary 服务器中的委托

当使用 `$ docker trust` 将第一个委托添加到 Notary 服务器时，我们会自动为仓库启动信任数据。这包括创建 notary 目标和快照密钥，以及将快照密钥轮换为由 notary 服务器管理。有关这些密钥的更多信息，请参阅
[管理内容信任的密钥](trust_key_mng.md)。

在启动仓库时，您将需要本地 Notary 规范根密钥的密钥和密码短语。如果您之前没有启动过仓库，因此没有 Notary 根密钥，`$ docker trust` 将为您创建一个。

> [!IMPORTANT]
>
> 请务必保护和备份您的 [Notary 规范根密钥](trust_key_mng.md)。

### 启动仓库

要将第一个密钥上传到委托，同时启动仓库，您可以使用 `$ docker trust signer add` 命令。这将把贡献者的公钥添加到 `targets/releases` 委托中，并创建第二个 `targets/<name>` 委托。

对于 DCT，第二个委托的名称（在下面的示例中为 `jeff`）有助于您跟踪密钥的所有者。在 Notary 的更高级用例中，额外的委托用于层次结构。

```console
$ docker trust signer add --key cert.pem jeff registry.example.com/admin/demo

Adding signer "jeff" to registry.example.com/admin/demo...
Initializing signed repository for registry.example.com/admin/demo...
Enter passphrase for root key with ID f6c6a4b: 
Enter passphrase for new repository key with ID b0014f8: 
Repeat passphrase for new repository key with ID b0014f8: 
Successfully initialized "registry.example.com/admin/demo"
Successfully added signer: jeff to registry.example.com/admin/demo
```

您可以使用 `$ docker trust inspect` 命令查看每个仓库推送到 Notary 服务器的密钥。

```console
$ docker trust inspect --pretty registry.example.com/admin/demo

No signatures for registry.example.com/admin/demo


List of signers and their keys for registry.example.com/admin/demo

SIGNER              KEYS
jeff                1091060d7bfd

Administrative keys for registry.example.com/admin/demo

  Repository Key:	b0014f8e4863df2d028095b74efcb05d872c3591de0af06652944e310d96598d
  Root Key:	64d147e59e44870311dd2d80b9f7840039115ef3dfa5008127d769a5f657a5d7
```

您也可以使用 Notary CLI 列出委托和密钥。在这里，您可以清楚地看到密钥已附加到 `targets/releases` 和 `targets/jeff`。

```console
$ notary delegation list registry.example.com/admin/demo

ROLE                PATHS             KEY IDS                                                             THRESHOLD
----                -----             -------                                                             ---------
targets/jeff        "" <all paths>    1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1    1
                                          
targets/releases    "" <all paths>    1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1    1 
```

### 添加额外的签名者

Docker Trust 允许您为每个仓库配置多个委托，以便您管理委托的生命周期。当使用 `$ docker trust` 添加额外的委托时，协作者的密钥将再次添加到 `targets/release` 角色中。

> 注意您将需要仓库密钥的密码短语；这在您首次启动仓库时配置。

```console
$ docker trust signer add --key ben.pub ben registry.example.com/admin/demo

Adding signer "ben" to registry.example.com/admin/demo...
Enter passphrase for repository key with ID b0014f8: 
Successfully added signer: ben to registry.example.com/admin/demo
```

检查以证明现在有 2 个委托（签名者）。

```console
$ docker trust inspect --pretty registry.example.com/admin/demo

No signatures for registry.example.com/admin/demo

List of signers and their keys for registry.example.com/admin/demo

SIGNER              KEYS
ben                 afa404703b25
jeff                1091060d7bfd

Administrative keys for registry.example.com/admin/demo

  Repository Key:	b0014f8e4863df2d028095b74efcb05d872c3591de0af06652944e310d96598d
  Root Key:	64d147e59e44870311dd2d80b9f7840039115ef3dfa5008127d769a5f657a5d7
```

### 向现有委托添加密钥

为了支持密钥轮换和过期/退役密钥等操作，您可以为每个委托发布多个贡献者密钥。这里的唯一先决条件是确保您使用相同的委托名称，在此情况下为 `jeff`。Docker trust 将自动处理将这个新密钥添加到 `targets/releases`。

> [!NOTE]
>
> 您将需要仓库密钥的密码短语；这在您首次启动仓库时配置。

```console
$ docker trust signer add --key cert2.pem jeff registry.example.com/admin/demo

Adding signer "jeff" to registry.example.com/admin/demo...
Enter passphrase for repository key with ID b0014f8: 
Successfully added signer: jeff to registry.example.com/admin/demo
```

检查以证明委托（签名者）现在包含多个密钥 ID。

```console
$ docker trust inspect --pretty registry.example.com/admin/demo

No signatures for registry.example.com/admin/demo


List of signers and their keys for registry.example.com/admin/demo

SIGNER              KEYS
jeff                1091060d7bfd, 5570b88df073

Administrative keys for registry.example.com/admin/demo

  Repository Key:	b0014f8e4863df2d028095b74efcb05d872c3591de0af06652944e310d96598d
  Root Key:	64d147e59e44870311dd2d80b9f7840039115ef3dfa5008127d769a5f657a5d7
```

### 删除委托

如果您需要删除委托，包括附加到 `targets/releases` 角色的贡献者密钥，您可以使用 `$ docker trust signer remove` 命令。

> [!NOTE]
>
> 被删除委托签名的标签需要由活跃的委托重新签名

```console
$ docker trust signer remove ben registry.example.com/admin/demo
Removing signer "ben" from registry.example.com/admin/demo...
Enter passphrase for repository key with ID b0014f8: 
Successfully removed ben from registry.example.com/admin/demo
```

#### 故障排除

1) 如果您看到 `targets/releases` 中没有可用密钥的错误，您需要使用 `docker trust signer add` 添加额外的委托，然后才能重新签名镜像。

   ```text
   WARN[0000] role targets/releases has fewer keys than its threshold of 1; it will not be usable until keys are added to it
   ```

2) 如果您已经添加了额外的委托并且看到 `targest/releases` 中没有有效签名的错误消息，您需要使用 Notary CLI 重新签名 `targets/releases` 委托文件。

   ```text
   WARN[0000] Error getting targets/releases: valid signatures did not meet threshold for targets/releases 
   ```

   使用 `$ notary witness` 命令重新签名委托文件

   ```console
   $ notary witness registry.example.com/admin/demo targets/releases --publish
   ```

   有关 `notary witness` 命令的更多信息，请参阅
   [Notary 客户端高级使用指南](https://github.com/theupdateframework/notary/blob/master/docs/advanced_usage.md#recovering-a-delegation)

### 从委托中删除贡献者的密钥

作为委托密钥轮换的一部分，您可能想要删除单个密钥但保留委托。这可以使用 Notary CLI 完成。

请记住，您必须从 `targets/releases` 角色和特定于该签名者的角色 `targets/<name>` 中删除密钥。

1) 我们需要从 Notary 服务器获取密钥 ID

   ```console
   $ notary delegation list registry.example.com/admin/demo

   ROLE                PATHS             KEY IDS                                                             THRESHOLD
   ----                -----             -------                                                             ---------
   targets/jeff        "" <all paths>    8fb597cbaf196f0781628b2f52bff6b3912e4e8075720378fda60d17232bbcf9    1
                                         1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1    
   targets/releases    "" <all paths>    8fb597cbaf196f0781628b2f52bff6b3912e4e8075720378fda60d17232bbcf9    1
                                         1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f3d6df44c02d1    
   ```

2) 从 `targets/releases` 委托中删除

   ```console
   $ notary delegation remove registry.example.com/admin/demo targets/releases 1091060d7bfd938dfa5be703fa057974f9322a4faef6f580334f