# 锁定 Swarm 以保护其加密密钥

Swarm 管理节点使用的 Raft 日志默认在磁盘上加密。这种静态加密可保护服务的配置和数据，防止攻击者访问加密的 Raft 日志。引入此功能的原因之一是为了支持 [Docker 密钥](secrets.md) 功能。

当 Docker 重启时，用于加密 Swarm 节点间通信的 TLS 密钥以及用于加密和解密磁盘上 Raft 日志的密钥都会加载到每个管理节点的内存中。Docker 能够通过让您拥有这些密钥的所有权并要求手动解锁管理节点来保护相互 TLS 加密密钥以及用于静态加密和解密 Raft 日志的密钥。此功能称为自动锁定。

当 Docker 重启时，您必须首先使用 Docker 在锁定 Swarm 时生成的密钥加密密钥 [解锁 Swarm](#unlock-a-swarm)。您可以随时轮换此密钥加密密钥。

> [!NOTE]
>
> 当新节点加入 Swarm 时，您无需解锁 Swarm，因为密钥会通过相互 TLS 传播给它。

## 初始化启用自动锁定的 Swarm

初始化新 Swarm 时，可以使用 `--autolock` 标志在 Docker 重启时启用 Swarm 管理节点的自动锁定。

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

请将密钥存储在安全的地方，例如密码管理器中。

当 Docker 重启时，您需要 [解锁 Swarm](#unlock-a-swarm)。当您尝试启动或重启服务时，锁定的 Swarm 会导致如下错误：

```console
$ sudo service docker restart

$ docker service ls

Error response from daemon: Swarm is encrypted and needs to be unlocked before it can be used. Use "docker swarm unlock" to unlock it.
```

## 在现有 Swarm 上启用或禁用自动锁定

要在现有 Swarm 上启用自动锁定，请将 `autolock` 标志设置为 `true`。

```console
$ docker swarm update --autolock=true

Swarm updated.
To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-+MrE8NgAyKj5r3NcR4FiQMdgu+7W72urH0EZeSmP/0Y

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

要禁用自动锁定，请将 `--autolock` 设置为 `false`。相互 TLS 密钥以及用于读写 Raft 日志的加密密钥将以未加密形式存储在磁盘上。在静态存储未加密密钥的风险与无需解锁每个管理节点即可重启 Swarm 的便利性之间需要权衡。

```console
$ docker swarm update --autolock=false
```

禁用自动锁定后，请保留解锁密钥一小段时间，以防管理节点在使用旧密钥配置锁定期间宕机。

## 解锁 Swarm

要解锁锁定的 Swarm，请使用 `docker swarm unlock`。

```console
$ docker swarm unlock

Please enter unlock key:
```

输入在锁定 Swarm 或轮换密钥时在命令输出中生成并显示的加密密钥，Swarm 将解锁。

## 查看运行中 Swarm 的当前解锁密钥

考虑这样一种情况：您的 Swarm 正常运行，然后一个管理节点变得不可用。您排查问题并将物理节点重新联机，但您需要通过提供解锁密钥来解锁管理节点以读取加密凭据和 Raft 日志。

如果自节点离开 Swarm 以来密钥未被轮换，并且 Swarm 中有法定数量的功能性管理节点，您可以使用 `docker swarm unlock-key` 不带任何参数查看当前解锁密钥。

```console
$ docker swarm unlock-key

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-8jDgbUNlJtUe5P/lcr9IXGVxqZpZUXPzd+qzcGp4ZYA

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

如果 Swarm 节点变得不可用后密钥已被轮换，并且您没有前一个密钥的记录，则可能需要强制管理节点离开 Swarm 并以新管理节点身份重新加入 Swarm。

## 轮换解锁密钥

您应定期轮换锁定 Swarm 的解锁密钥。

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
> 轮换解锁密钥时，请保留旧密钥记录几分钟，以便如果管理节点在获取新密钥之前宕机，仍可使用旧密钥解锁。
