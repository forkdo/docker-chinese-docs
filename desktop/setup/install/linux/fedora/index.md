# 在 Fedora 上安装 Docker Desktop

> **Docker Desktop 使用条款**
>
> 大型企业（超过 250 名员工或年收入超过 1000 万美元）商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页面包含如何在 Fedora 发行版上安装、启动和升级 Docker Desktop 的信息。

## 前置条件

要成功安装 Docker Desktop，您必须：

- 满足[通用系统要求](_index.md#general-system-requirements)。
- 拥有 64 位版本的 Fedora 41 或 Fedora 42。
- 对于 GNOME 桌面环境，您必须安装 AppIndicator 和 KStatusNotifierItem [GNOME 扩展](https://extensions.gnome.org/extension/615/appindicator-support/)。
- 如果您未使用 GNOME，则必须安装 `gnome-terminal` 以启用 Docker Desktop 的终端访问：

   ```console
   $ sudo dnf install gnome-terminal
   ```

## 安装 Docker Desktop

在 Fedora 上安装 Docker Desktop：

1. 设置 [Docker 的软件包仓库](/manuals/engine/install/fedora.md#set-up-the-repository)。

2. 下载最新的 [RPM 包](https://desktop.docker.com/linux/main/amd64/docker-desktop-x86_64.rpm?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64)。校验和信息请参阅 [发布说明](/manuals/desktop/release-notes.md)。

3. 使用 dnf 安装该包：

   ```console
   $ sudo dnf install ./docker-desktop-x86_64.rpm
   ```

   默认情况下，Docker Desktop 安装在 `/opt/docker-desktop`。

RPM 包包含一个 post-install 脚本，自动完成额外的设置步骤。

post-install 脚本会：

- 为 Docker Desktop 二进制文件设置权限，以映射特权端口并设置资源限制。
- 为 Kubernetes 添加 DNS 名称到 `/etc/hosts`。
- 创建从 `/usr/local/bin/com.docker.cli` 到 `/usr/bin/docker` 的符号链接。
  这是因为经典 Docker CLI 安装在 `/usr/bin/docker`。Docker Desktop 安装程序还会在 `/usr/local/bin/com.docker.cli` 安装一个 Docker CLI 二进制文件，该文件包含云集成功能，本质上是 Compose CLI 的包装器。此符号链接确保包装器可以访问经典 Docker CLI。

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

Docker Desktop 发布新版本后，Docker UI 会显示通知。您需要先卸载旧版本，然后下载新包来升级 Docker Desktop。运行：

```console
$ sudo dnf remove docker-desktop
$ sudo dnf install ./docker-desktop-x86_64.rpm
```

## 后续步骤

- 探索 [Docker 订阅](https://www.docker.com/pricing/) 了解 Docker 可为您提供什么。
- 查看 [Docker 工作坊](/get-started/workshop/_index.md) 学习如何构建镜像并将其作为容器化应用程序运行。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 描述了常见问题、变通方案、如何运行和提交诊断信息以及提交问题。
- [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供了常见问题的答案。
- [发布说明](/manuals/desktop/release-notes.md) 列出了与 Docker Desktop 发布相关的组件更新、新功能和改进。
- [备份和还原数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了与 Docker 相关的数据备份和还原说明。
