---
description: 管理内容信任的密钥
keywords: 信任, 安全, 根密钥, 密钥, 仓库
title: 管理内容信任的密钥
---

对镜像标签的信任通过密钥进行管理。Docker 的内容信任使用五种不同类型的密钥：

| 密钥类型   | 描述 |                                                                                                                                                                                                                         
|:-----------|:----------- |
| 根密钥 (root key)   | 镜像标签内容信任的根。启用内容信任后，您只需创建一次根密钥。也称为离线密钥，因为它应保持离线状态。 |
| 目标密钥 (targets)    | 此密钥允许您为镜像标签签名，管理委托（包括委托密钥或许可的委托路径）。也称为仓库密钥，因为此密钥决定了哪些标签可以签名到镜像仓库中。 |
| 快照密钥 (snapshot)   | 此密钥对当前的镜像标签集合进行签名，防止混合攻击。 |                                                                                                                                         
| 时间戳密钥 (timestamp)  | 此密钥允许 Docker 镜像仓库在不需要客户端定期刷新内容的情况下提供时效性安全保证。 |
| 委托密钥 (delegation) | 委托密钥是可选的标签密钥，允许您将为镜像标签签名的权限委托给其他发布者，而无需共享您的目标密钥。 |

首次启用内容信任进行 `docker push` 时，会自动为镜像仓库生成根密钥、目标密钥、快照密钥和时间戳密钥：

- 根密钥和目标密钥在本地客户端生成并存储。

- 时间戳密钥和快照密钥在 Docker 注册表旁部署的签名服务器中安全生成和存储。这些密钥在不直接暴露于互联网的后端服务中生成，并且静态加密。使用 Notary CLI 可以[在本地管理您的快照密钥](https://github.com/theupdateframework/notary/blob/master/docs/advanced_usage.md#rotate-keys)。

委托密钥是可选的，不会作为正常 `docker` 工作流的一部分生成。需要[手动创建并添加到仓库中](trust_delegation.md#creating-delegation-keys)。

## 选择密码短语

为根密钥和仓库密钥选择的密码短语应随机生成并存储在密码管理器中。拥有仓库密钥允许用户为仓库中的镜像标签签名。密码短语用于加密静态存储的密钥，确保丢失的笔记本电脑或意外的备份不会危及私钥材料。

## 备份您的密钥

所有 Docker 信任密钥都使用您在创建时提供的密码短语加密存储。即便如此，您仍应小心备份位置。良好的做法是创建两个加密的 USB 密钥。

> [!WARNING]
>
> 将密钥备份到安全、可靠的位置非常重要。仓库密钥的丢失是可恢复的，但根密钥的丢失是不可恢复的。

Docker 客户端将密钥存储在 `~/.docker/trust/private` 目录中。备份前，应先将它们打包成 tar 归档文件：

```console
$ umask 077; tar -zcvf private_keys_backup.tar.gz ~/.docker/trust/private; umask 022
```

## 硬件存储和签名

Docker 内容信任可以将根密钥存储在 Yubikey 4 中并从中进行签名。Yubikey 优先于存储在文件系统中的密钥。当您使用内容信任初始化新仓库时，Docker Engine 会在本地查找根密钥。如果未找到密钥且存在 Yubikey 4，Docker Engine 会在 Yubikey 4 中创建根密钥。更多详细信息请参阅 [Notary 文档](https://github.com/theupdateframework/notary/blob/master/docs/advanced_usage.md#use-a-yubikey)。

在 Docker Engine 1.11 之前，此功能仅在实验分支中提供。

## 密钥丢失

> [!WARNING]
>
> 如果发布者丢失密钥，意味着失去为相关仓库镜像签名的能力。如果您丢失了密钥，请发送邮件至 [Docker Hub 支持](mailto:hub-support@docker.com)。提醒一下，根密钥的丢失是不可恢复的。

此丢失还要求之前从受影响仓库下载过已签名内容的每个消费者手动干预。
镜像消费者会收到以下错误：

```console
Warning: potential malicious behavior - trust data has insufficient signatures for remote repository docker.io/my/image: valid signatures did not meet threshold
```

要纠正此问题，他们需要下载使用新密钥签名的新镜像标签。

## 相关信息

* [Docker 中的内容信任](index.md)
* [内容信任的自动化](trust_automation.md)
* [内容信任的委托](trust_delegation.md)
* [在内容信任沙箱中体验](trust_sandbox.md)