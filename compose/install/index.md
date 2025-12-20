# Docker Compose 安装概述

本文总结了根据您的平台和需求，安装 Docker Compose 的不同方法。

## 安装场景

### Docker Desktop（推荐）

获取 Docker Compose 最简单且推荐的方法是安装 Docker Desktop。

Docker Desktop 包含 Docker Compose 以及 Docker Engine 和 Docker CLI，这些是 Compose 的必备组件。

Docker Desktop 适用于：
- [Linux](/manuals/desktop/setup/install/linux/_index.md)
- [Mac](/manuals/desktop/setup/install/mac-install.md)
- [Windows](/manuals/desktop/setup/install/windows-install.md)

> [!TIP]
> 
> 如果您已安装 Docker Desktop，可以通过从 Docker 菜单 





<img
  loading="lazy"
  src="../../desktop/images/whale-x.svg"
  alt="whale menu"
  
  class="inline my-0 not-prose"
/>
 中选择 **About Docker Desktop** 来检查您拥有的 Compose 版本。

### 插件（仅限 Linux）

> [!IMPORTANT]
>
> 此方法仅在 Linux 上可用。

如果您已安装 Docker Engine 和 Docker CLI，可以通过命令行安装 Docker Compose 插件，方法如下：
- [使用 Docker 的软件仓库](linux.md#install-using-the-repository)
- [手动下载并安装](linux.md#install-the-plugin-manually)

### 独立（旧版）

> [!WARNING]
>
> 不建议使用此安装场景，仅出于向后兼容目的提供支持。

您可以在 Linux 或 Windows Server 上[安装 Docker Compose 独立版](standalone.md)。

- [安装 Docker Compose 插件](/compose/install/linux/)

- [安装独立的 Docker Compose（旧版）](/compose/install/standalone/)

- [卸载 Docker Compose](/compose/install/uninstall/)

