# 安装 Docker Engine

本节介绍如何在 Linux 上安装 Docker Engine，也称为 Docker CE。Docker Engine 也可通过 Docker Desktop 在 Windows、macOS 和 Linux 上使用。有关如何安装 Docker Desktop 的说明，请参阅：[Docker Desktop 概述](/manuals/desktop/_index.md)。

## 支持平台的安装过程

单击平台链接以查看相关的安装过程。

| 平台                                             | x86_64 / amd64 | arm64 / aarch64 | arm (32-bit) | ppc64le | s390x |
| :----------------------------------------------- | :------------: | :-------------: | :----------: | :-----: | :---: |
| [CentOS](centos.md)                              |       ✅       |       ✅        |              |   ✅    |       |
| [Debian](debian.md)                              |       ✅       |       ✅        |      ✅      |   ✅    |       |
| [Fedora](fedora.md)                              |       ✅       |       ✅        |              |   ✅    |       |
| [Raspberry Pi OS (32-bit)](raspberry-pi-os.md)   |                |                 |      ⚠️      |         |       |
| [RHEL](rhel.md)                                  |       ✅       |       ✅        |              |         |  ✅   |
| [SLES](sles.md)                                  |                |                 |              |         |  ❌   |
| [Ubuntu](ubuntu.md)                              |       ✅       |       ✅        |      ✅      |   ✅    |  ✅   |
| [Binaries](binaries.md)                          |       ✅       |       ✅        |      ✅      |         |       |

### 其他 Linux 发行版

> [!NOTE]
>
> 虽然以下说明可能有效，但 Docker 不会测试或验证在发行版衍生版本上的安装。

- 如果您使用 Debian 衍生版本，例如 "BunsenLabs Linux"、"Kali Linux" 或 "LMDE"（基于 Debian 的 Mint），应遵循 [Debian](debian.md) 的安装说明，将您的发行版版本替换为相应的 Debian 版本。请查阅您的发行版文档，以确定哪个 Debian 版本与您的衍生版本相对应。
- 同样，如果您使用 Ubuntu 衍生版本，例如 "Kubuntu"、"Lubuntu" 或 "Xubuntu"，应遵循 [Ubuntu](ubuntu.md) 的安装说明，将您的发行版版本替换为相应的 Ubuntu 版本。请查阅您的发行版文档，以确定哪个 Ubuntu 版本与您的衍生版本相对应。
- 一些 Linux 发行版通过其软件包仓库提供 Docker Engine 软件包。这些软件包由 Linux 发行版的软件包维护者构建和维护，可能在配置上存在差异，或者是由修改后的源代码构建的。Docker 不参与发布这些软件包，您应将任何与这些软件包相关的错误或问题报告给您的 Linux 发行版的问题跟踪器。

Docker 提供用于手动安装 Docker Engine 的[二进制文件](binaries.md)。这些二进制文件是静态链接的，可以在任何 Linux 发行版上使用。

## 发布渠道

Docker Engine 有两种类型的更新渠道：**稳定版 (stable)** 和 **测试版 (test)**：

* **稳定版**渠道提供一般可用性 (GA) 的最新版本。
* **测试版**渠道提供在一般可用性之前可供测试的预发布版本。

请谨慎使用测试版渠道。预发布版本包含实验性和早期访问功能，可能会发生重大变更。

## 支持

Docker Engine 是一个开源项目，由 Moby 项目维护者和社区成员提供支持。Docker 不为 Docker Engine 提供支持。Docker 为其产品（包括使用 Docker Engine 作为其组件之一的 Docker Desktop）提供支持。

有关开源项目的信息，请参阅 [Moby 项目网站](https://mobyproject.org/)。

### 升级路径

补丁版本始终与其主版本和次版本向后兼容。

### 许可

在大型企业（员工人数超过 250 人或年收入超过 1000 万美元）中，通过 Docker Desktop 获得的 Docker Engine 的商业使用需要[付费订阅](https://www.docker.com/pricing/)。Apache License, Version 2.0。完整许可证请参见 [LICENSE](https://github.com/moby/moby/blob/master/LICENSE)。

## 报告安全问题

如果您发现安全问题，我们要求您立即提请我们注意。

请不要提交公开问题。请将您的报告私密地发送至 security@docker.com。

安全报告将不胜感激，Docker 将公开致谢。

## 开始使用

设置 Docker 后，您可以通过[使用 Docker 入门](/get-started/introduction/_index.md)学习基础知识。

- [在 Ubuntu 上安装 Docker Engine](/engine/install/ubuntu/)

- [在 Debian 上安装 Docker Engine](/engine/install/debian/)

- [在 RHEL 上安装 Docker Engine](/engine/install/rhel/)

- [在 Fedora 上安装 Docker Engine](/engine/install/fedora/)

- [在 Raspberry Pi OS (32-bit / armhf) 上安装 Docker Engine](/engine/install/raspberry-pi-os/)

- [在 CentOS 上安装 Docker Engine](/engine/install/centos/)

- [Docker Engine 在 SLES (s390x) 上](/engine/install/sles/)

- [通过二进制文件安装 Docker Engine](/engine/install/binaries/)

- [Docker Engine 的 Linux 安装后步骤](/engine/install/linux-postinstall/)

