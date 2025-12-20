# 管理内容信任的密钥

通过密钥管理镜像标签的信任。Docker 的内容信任使用了五种不同类型的密钥：

| 密钥        | 描述 |                                                                                                                                                                                                                         
|:-----------|:----------- |
| root key   | 镜像标签内容信任的根密钥。启用内容信任时，需创建一次根密钥。也称为离线密钥，因为应保持离线存储。 |
| targets    | 该密钥允许您对镜像标签进行签名，管理委托（包括委托密钥或允许的委托路径）。也称为仓库密钥，因为此密钥决定了哪些标签可以签名到镜像仓库中。 |
| snapshot   | 该密钥对当前镜像标签集合进行签名，防止混合和匹配攻击。 |                                                                                                                                         
| timestamp  | 该密钥允许 Docker 镜像仓库在不要求客户端定期刷新内容的情况下，提供新鲜性安全保证。 |
| delegation | 委托密钥是可选的标签密钥，允许您将镜像标签签名委托给其他发布者，而无需共享您的 targets 密钥。 |

首次启用内容信任执行 `docker push` 时，系统会自动为镜像仓库生成 root、targets、snapshot 和 timestamp 密钥：

- root 和 targets 密钥在客户端本地生成并存储。

- timestamp 和 snapshot 密钥在部署于 Docker 注册表旁的签名服务器中安全生成并存储。这些密钥在不会直接暴露于互联网的后台服务中生成，并以加密形式静态存储。使用 Notary CLI [在本地管理 snapshot 密钥](https://github.com/theupdateframework/notary/blob/master/docs/advanced_usage.md#rotate-keys)。

委托密钥是可选的，不会作为常规 `docker` 工作流的一部分生成。您需要[手动生成并添加到仓库](trust_delegation.md#creating-delegation-keys)。

## 选择密码

为 root 密钥和仓库密钥选择的密码应为随机生成，并存储在密码管理器中。拥有仓库密钥的用户可以对该仓库的镜像标签进行签名。密码用于加密静态存储的密钥，确保丢失笔记本电脑或意外备份不会导致私钥材料泄露。

## 备份密钥

所有 Docker 信任密钥在创建时均使用您提供的密码进行加密存储。即便如此，您仍需谨慎选择备份位置。良好实践是创建两个加密的 USB 密钥。

> [!WARNING]
>
> 将密钥备份到安全、可靠的位置非常重要。
丢失仓库密钥可恢复，但丢失 root 密钥则不可恢复。

Docker 客户端将密钥存储在 `~/.docker/trust/private` 目录中。备份前，您应将其打包为归档文件：

```console
$ umask 077; tar -zcvf private_keys_backup.tar.gz ~/.docker/trust/private; umask 022
```

## 硬件存储和签名

Docker 内容信任可使用 Yubikey 4 存储和签名 root 密钥。Yubikey 优先于文件系统中的密钥。使用内容信任初始化新仓库时，Docker 引擎会本地查找 root 密钥。如果未找到密钥且存在 Yubikey 4，Docker 引擎会在 Yubikey 4 中创建 root 密钥。更多详情请查阅 [Notary 文档](https://github.com/theupdateframework/notary/blob/master/docs/advanced_usage.md#use-a-yubikey)。

在 Docker 引擎 1.11 之前，此功能仅存在于实验分支中。

## 密钥丢失

> [!WARNING]
>
> 如果发布者丢失密钥，意味着将失去为相关仓库镜像签名的能力。如果丢失密钥，请发送邮件至 [Docker Hub 支持](mailto:hub-support@docker.com)。
需要提醒的是，root 密钥丢失不可恢复。

此丢失还需此前使用过该仓库签名标签的每个消费者手动干预。  
镜像消费者从受影响的仓库下载内容时会收到以下错误：

```console
Warning: potential malicious behavior - trust data has insufficient signatures for remote repository docker.io/my/image: valid signatures did not meet threshold
```

要解决此问题，他们需下载使用新密钥签名的新镜像标签。

## 相关信息

* [Docker 中的内容信任](index.md)
* [内容信任的自动化](trust_automation.md)
* [内容信任的委托](trust_delegation.md)
* [在内容信任沙箱中实践](trust_sandbox.md)
