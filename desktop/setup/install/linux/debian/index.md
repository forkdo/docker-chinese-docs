# 在 Debian 上安装 Docker Desktop

> **Docker Desktop 条款**
>
> 在大型企业（超过 250 名员工或年度收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页包含有关如何在 Debian 发行版上安装、启动和升级 Docker Desktop 的信息。

## 先决条件

要成功安装 Docker Desktop，您必须：

- 满足[通用系统要求](_index.md#general-system-requirements)。
- 拥有 64 位版本的 Debian 12。
- 对于 Gnome 桌面环境，您还必须安装 AppIndicator 和 KStatusNotifierItem [Gnome 扩展](https://extensions.gnome.org/extension/615/appindicator-support/)。
- 如果您不使用 GNOME，则必须安装 `gnome-terminal` 以启用从 Docker Desktop 访问终端：

  ```console
  $ sudo apt install gnome-terminal
  ```

## 安装 Docker Desktop

在 Debian 上安装 Docker Desktop 的推荐方法：

1. 设置 Docker 的 `apt` 仓库。
   参见[使用 `apt` 仓库安装](/manuals/engine/install/debian.md#install-using-the-repository)中的第一步。

2. 下载最新的 [DEB 包](https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64)。有关校验和，请参阅[发行说明](/manuals/desktop/release-notes.md)。

3. 使用 `apt` 安装软件包：

  ```console
  $ sudo apt-get update
  $ sudo apt-get install ./docker-desktop-amd64.deb
  ```

  > [!NOTE]
  >
  > 在安装过程结束时，`apt` 会因安装下载的软件包而显示错误。您可以忽略此错误消息。
  >
  > ```text
  > N: Download is performed unsandboxed as root, as file '/home/user/Downloads/docker-desktop.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
  > ```

   默认情况下，Docker Desktop 安装在 `/opt/docker-desktop`。

RPM 软件包包含一个安装后脚本，可自动完成其他设置步骤。

安装后脚本：

- 在 Docker Desktop 二进制文件上设置 capabilities，以映射特权端口和设置资源限制。
- 将 Kubernetes 的 DNS 名称添加到 `/etc/hosts`。
- 从 `/usr/local/bin/com.docker.cli` 创建一个指向 `/usr/bin/docker` 的符号链接。
  这是因为经典的 Docker CLI 安装在 `/usr/bin/docker`。Docker Desktop 安装程序还会安装一个包含云集成能力的 Docker CLI 二进制文件，它本质上是 Compose CLI 的包装器，位于 `/usr/local/bin/com.docker.cli`。该符号链接确保包装器可以访问经典的 Docker CLI。

## 启动 Docker Desktop



要启动 Docker Desktop for Linux：

1.  在您的 Gnome/KDE 桌面中找到 Docker Desktop 应用程序。
2.  选择 **Docker Desktop** 以启动 Docker。

    此时将显示 Docker 订阅服务协议。

3.  选择 **接受** 继续。接受条款后，Docker Desktop 将会启动。

    请注意，如果您不同意该条款，Docker Desktop 将无法运行。您可以通过稍后打开 Docker Desktop 来选择接受条款。

    更多信息，请参阅 [Docker Desktop 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)。建议您同时阅读 [常见问题解答](https://www/docker.com/pricing/faq)。

或者，打开终端并运行：

```console
$ systemctl --user start docker-desktop
```

当 Docker Desktop 启动时，它会创建一个专用的 [上下文](/engine/context/working-with-contexts)，供 Docker CLI 作为目标使用，并将其设置为当前正在使用的上下文。这样做是为了避免与可能在 Linux 主机上运行并使用默认上下文的本地 Docker Engine 发生冲突。关闭时，Docker Desktop 会将当前上下文重置为之前的上下文。

Docker Desktop 安装程序会更新主机上的 Docker Compose 和 Docker CLI 二进制文件。它会安装 Docker Compose V2，并允许用户通过设置面板选择将其链接为 docker-compose。Docker Desktop 会在 `/usr/local/bin/com.docker.cli` 安装包含云集成功能的新版 Docker CLI 二进制文件，并在 `/usr/local/bin` 创建指向经典 Docker CLI 的符号链接。

成功安装 Docker Desktop 后，您可以通过运行以下命令来检查这些二进制文件的版本：

```console
$ docker compose version
Docker Compose version v2.39.4

$ docker --version
Docker version 28.4.0, build d8eb465

$ docker version
Client:
 Version:           28.4.0
 API version:       1.51
 Go version:        go1.24.7
<...>
```

要让 Docker Desktop 在登录时自动启动，请从 Docker 菜单中选择 **设置** > **常规** > **登录计算机时启动 Docker Desktop**。

或者，打开终端并运行：

```console
$ systemctl --user enable docker-desktop
```

要停止 Docker Desktop，请选择 Docker 菜单图标以打开 Docker 菜单，然后选择 **退出 Docker Desktop**。

或者，打开终端并运行：

```console
$ systemctl --user stop docker-desktop
```

## 升级 Docker Desktop

一旦发布了 Docker Desktop 的新版本，Docker UI 会显示通知。
每次要升级 Docker Desktop 时，都需要下载新软件包并运行：

```console
$ sudo apt-get install ./docker-desktop-amd64.deb
```

## 下一步

- 探索 [Docker 的订阅](https://www.docker.com/pricing/)，了解 Docker 可以为您提供什么。
- 查看 [Docker 研讨会](/get-started/workshop/_index.md)，了解如何构建镜像并将其作为容器化应用程序运行。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 描述了常见问题、解决方法、如何运行和提交诊断信息以及提交问题。
- [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供了常见问题的答案。
- [发行说明](/manuals/desktop/release-notes.md) 列出了与 Docker Desktop 版本相关的组件更新、新功能和改进。
- [备份和恢复数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了有关备份和恢复与 Docker 相关的数据的说明。
