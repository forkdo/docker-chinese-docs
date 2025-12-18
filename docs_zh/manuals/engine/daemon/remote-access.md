---
description:
  配置远程访问允许 Docker 接受来自远程主机的请求，方法是配置它监听 IP 地址和端口以及 Unix 套接字
keywords: configuration, daemon, remote access, engine
title: 为 Docker 守护进程配置远程访问
aliases:
  - /config/daemon/remote-access/
---

默认情况下，Docker 守护进程监听 Unix 套接字上的连接，以接受来自本地客户端的请求。你可以通过配置 Docker 监听 IP 地址和端口以及 Unix 套接字，使其接受来自远程客户端的请求。

<!-- prettier-ignore -->
> [!WARNING]
>
> 配置 Docker 接受来自远程客户端的连接可能会使你面临来自网络的未授权访问和其他攻击。
>
> 理解开放 Docker 到网络带来的安全影响至关重要。如果不采取措施保护连接，远程非 root 用户可能获得主机的 root 访问权限。
>
> 不使用 TLS 的远程访问 **不推荐**，并且在未来的版本中需要明确选择启用。有关如何使用 TLS 证书保护此连接的更多信息，请参阅
> [保护 Docker 守护进程套接字](/manuals/engine/security/protect-access.md)。

## 启用远程访问

你可以使用 `docker.service` systemd 单元文件（适用于使用 systemd 的 Linux 发行版）或 `daemon.json` 文件（如果你的发行版不使用 systemd）来启用对守护进程的远程访问。

使用 systemd 单元文件和 `daemon.json` 文件配置 Docker 监听连接会导致冲突，阻止 Docker 启动。

### 使用 systemd 单元文件配置远程访问

1. 使用命令 `sudo systemctl edit docker.service` 在文本编辑器中打开 `docker.service` 的覆盖文件。

2. 添加或修改以下行，替换为你自己的值：

   ```systemd
   [Service]
   ExecStart=
   ExecStart=/usr/bin/dockerd -H fd:// -H tcp://127.0.0.1:2375
   ```

3. 保存文件。

4. 重新加载 `systemctl` 配置。

   ```console
   $ sudo systemctl daemon-reload
   ```

5. 重启 Docker。

   ```console
   $ sudo systemctl restart docker.service
   ```

6. 验证更改是否生效。

   ```console
   $ sudo netstat -lntp | grep dockerd
   tcp        0      0 127.0.0.1:2375          0.0.0.0:*               LISTEN      3758/dockerd
   ```

### 使用 `daemon.json` 配置远程访问

1. 在 `/etc/docker/daemon.json` 中设置 `hosts` 数组，以连接到 Unix 套接字和 IP 地址，如下所示：

   ```json
   {
     "hosts": ["unix:///var/run/docker.sock", "tcp://127.0.0.1:2375"]
   }
   ```

2. 重启 Docker。

3. 验证更改是否生效。

   ```console
   $ sudo netstat -lntp | grep dockerd
   tcp        0      0 127.0.0.1:2375          0.0.0.0:*               LISTEN      3758/dockerd
   ```

### 允许通过防火墙访问远程 API

如果你在运行 Docker 的同一主机上运行防火墙，并且希望从另一个远程主机访问 Docker 远程 API，则必须配置防火墙以允许在 Docker 端口上建立传入连接。如果你使用 TLS 加密传输，默认端口是 `2376`，否则为 `2375`。

两种常见的防火墙守护进程是：

- [Uncomplicated Firewall (ufw)](https://help.ubuntu.com/community/UFW)，通常用于 Ubuntu 系统。
- [firewalld](https://firewalld.org)，通常用于基于 RPM 的系统。

请查阅你的操作系统和防火墙的文档。以下信息可能有助于你开始。此处使用的设置是宽松的，你可能希望使用锁定更严格的不同配置。

- 对于 ufw，在配置中设置 `DEFAULT_FORWARD_POLICY="ACCEPT"`。

- 对于 firewalld，将类似以下内容的规则添加到你的策略中。一个用于传入请求，一个用于传出请求。

  ```xml
  <direct>
    [ <rule ipv="ipv6" table="filter" chain="FORWARD_direct" priority="0"> -i zt0 -j ACCEPT </rule> ]
    [ <rule ipv="ipv6" table="filter" chain="FORWARD_direct" priority="0"> -o zt0 -j ACCEPT </rule> ]
  </direct>
  ```

  确保接口名称和链名称正确。

## 附加信息

有关守护进程远程访问配置选项的更详细信息，请参考
[dockerd CLI 参考](/reference/cli/dockerd/#bind-docker-to-another-hostport-or-a-unix-socket)。