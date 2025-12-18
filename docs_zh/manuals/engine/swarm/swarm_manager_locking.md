---
description: 自动锁定 Swarm 管理节点以保护加密密钥
keywords: swarm, manager, lock, unlock, autolock, encryption
title: 锁定你的 Swarm 以保护其加密密钥
---

Swarm 管理节点使用的 Raft 日志默认在磁盘上加密。这种静态加密保护了你的服务配置和数据，防止攻击者获取到加密的 Raft 日志后进行破解。引入此功能的原因之一是为了支持 [Docker secrets](secrets.md) 功能。

当 Docker 重启时，用于加密节点间通信的 TLS 密钥和用于加密/解密磁盘上 Raft 日志的密钥都会被加载到每个管理节点的内存中。Docker 可以通过允许你自行管理这些密钥，并要求手动解锁管理节点，来保护这些静态存储的密钥。此功能称为自动锁定（autolock）。

当 Docker 重启时，你必须使用 Docker 在锁定 Swarm 时生成的密钥加密密钥来 [解锁 Swarm](#unlock-a-swarm)。你可以随时轮换此密钥加密密钥。

> [!NOTE]
>
> 当新节点加入 Swarm 时，不需要解锁 Swarm，因为密钥会通过相互 TLS 传播给它。

## 初始化启用自动锁定的 Swarm

当你初始化一个新的 Swarm 时，可以使用 `--autolock` 标志在 Docker 重启时启用 Swarm 管理节点的自动锁定功能。

```console
$ docker swarm init --autolock

Swarm initialized: current node (k1q27tfyx9rncpixhk69sa61v) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-0j52ln6hxjpxk2wgk917abcnxywj3xed0y8vi1e5m9t3uttrtu-7bnxvvlz2mrcpfonjuztmtts9 \
    172.31.46.109:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-WuYH/IX284+lRcXuoVf38viIDK3HJEKY13MIHX+tTt8
```

将此密钥安全存储，例如存储在密码管理器中。

当 Docker 重启时，你需要 [解锁 Swarm](#unlock-a-swarm)。锁定的 Swarm 会导致在尝试启动或重启服务时出现如下错误：

```console
$ sudo service docker restart

$ docker service ls

Error response from daemon: Swarm is encrypted and needs to be unlocked before it can be used. Use "docker swarm unlock" to unlock it.
```

## 在现有 Swarm 上启用或禁用自动锁定

要在现有 Swarm 上启用自动锁定，将 `autolock` 标志设置为 `true`。

```console
$ docker swarm update --autolock=true

Swarm updated.
To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-+MrE8NgAyKj5r3NcR4FiQMdgu+7W72urH0EZeSmP/0Y

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

要禁用自动锁定，将 `--autolock` 设置为 `false`。相互 TLS 密钥和用于读写 Raft 日志的加密密钥将以未加密形式存储在磁盘上。这需要在静态存储时未加密密钥的风险与无需解锁每个管理节点即可重启 Swarm 的便利性之间进行权衡。

```console
$ docker swarm update --autolock=false
```

在禁用自动锁定后，暂时保留解锁密钥，以防管理节点在仍配置为使用旧密钥锁定时发生故障。

## 解锁 Swarm

要解锁已锁定的 Swarm，请使用 `docker swarm unlock`。

```console
$ docker swarm unlock

Please enter unlock key:
```

输入锁定 Swarm 或轮换密钥时生成并显示的加密密钥，Swarm 将被解锁。

## 查看正在运行的 Swarm 的当前解锁密钥

考虑以下情况：你的 Swarm 正常运行，然后一个管理节点变得不可用。你排除故障并将物理节点重新上线，但需要提供解锁密钥来解锁管理节点，以便读取加密的凭据和 Raft 日志。

如果自节点离开 Swarm 后密钥未被轮换，且 Swarm 中有足够数量的正常管理节点，你可以使用 `docker swarm unlock-key`（不带参数）查看当前的解锁密钥。

```console
$ docker swarm unlock-key

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-8jDgbUNlJtUe5P/lcr9IXGVxqZpZUXPzd+qzcGp4ZYA

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

如果在节点不可用后轮换了密钥，且你没有旧密钥的记录，则可能需要强制管理节点离开 Swarm，并将其作为新管理节点重新加入 Swarm。

## 轮换解锁密钥

你应该定期轮换已锁定 Swarm 的解锁密钥。

```console
$ docker swarm unlock-key --rotate

Successfully rotated manager unlock key.

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-8jDgbUNlJtUe5P/lcr9IXGVxqZpZUXPzd+qzcGp4ZYA

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

> [!WARNING]
>
> 当你轮换解锁密钥时，保留旧密钥几分钟，以便如果管理节点在获取新密钥之前发生故障，仍可用旧密钥解锁。