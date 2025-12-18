---
title: 安装 Docker Engine
linkTitle: 安装
weight: 10
description: 了解如何选择最适合您的方式安装 Docker Engine。这个客户端-服务器应用程序可在 Linux、Mac、Windows 和静态二进制文件上使用。
keywords: install engine, docker engine install, install docker engine, docker engine
  installation, engine install, docker ce installation, docker ce install, engine
  installer, installing docker engine, docker server install, docker desktop vs docker engine
aliases:
- /cs-engine/
- /cs-engine/1.12/
- /cs-engine/1.12/upgrade/
- /cs-engine/1.13/
- /cs-engine/1.13/upgrade/
- /ee/docker-ee/oracle/
- /ee/supported-platforms/
- /en/latest/installation/
- /engine/installation/
- /engine/installation/frugalware/
- /engine/installation/linux/
- /engine/installation/linux/archlinux/
- /engine/installation/linux/cruxlinux/
- /engine/installation/linux/docker-ce/
- /engine/installation/linux/docker-ee/
- /engine/installation/linux/docker-ee/oracle/
- /engine/installation/linux/frugalware/
- /engine/installation/linux/gentoolinux/
- /engine/installation/linux/oracle/
- /engine/installation/linux/other/
- /engine/installation/oracle/
- /enterprise/supported-platforms/
- /install/linux/docker-ee/oracle/
---

本节介绍如何在 Linux 上安装 Docker Engine，也就是 Docker CE。Docker Engine 也可通过 Docker Desktop 在 Windows、macOS 和 Linux 上使用。有关如何安装 Docker Desktop 的说明，请参阅：[Docker Desktop 概述](/manuals/desktop/_index.md)。

## 受支持平台的安装步骤

点击平台链接查看相应的安装步骤。

| 平台                                       | x86_64 / amd64 | arm64 / aarch64 | arm (32位) | ppc64le | s390x |
| :--------------------------------------------- | :------------: | :-------------: | :----------: | :-----: | :---: |
| [CentOS](centos.md)                            |       ✅       |       ✅        |              |   ✅    |       |
| [Debian](debian.md)                            |       ✅       |       ✅        |      ✅      |   ✅    |       |
| [Fedora](fedora.md)                            |       ✅       |       ✅        |              |   ✅    |       |
| [Raspberry Pi OS (32位)](raspberry-pi-os.md) |                |                 |      ⚠️      |         |       |
| [RHEL](rhel.md)                                |       ✅       |       ✅        |              |         |  ✅   |
| [SLES](sles.md)                                |                |                 |              |         |  ❌   |
| [Ubuntu](ubuntu.md)                            |       ✅       |       ✅        |      ✅      |   ✅    |  ✅   |
| [二进制文件](binaries.md)                        |       ✅       |       ✅        |      ✅      |         |       |

### 其他 Linux 发行版

> [!NOTE]
>
> 尽管以下说明可能有效，但 Docker 未测试或验证在发行版衍生版本上的安装。

- 如果您使用 Debian 衍生版本，如 "BunsenLabs Linux"、"Kali Linux" 或 "LMDE"（基于 Debian 的 Mint），应遵循 [Debian](debian.md) 的安装说明，将您的发行版版本替换为相应的 Debian 发行版。请参考您发行版的文档，找到与您的衍生版本对应的 Debian 发行版。
- 同样，如果您使用 Ubuntu 衍生版本，如 "Kubuntu"、"Lubuntu" 或 "Xubuntu"，应遵循 [Ubuntu](ubuntu.md) 的安装说明，将您的发行版版本替换为相应的 Ubuntu 发行版。请参考您发行版的文档，找到与您的衍生版本对应的 Ubuntu 发行版。
- 某些 Linux 发行版通过其软件包仓库提供 Docker Engine 的软件包。这些软件包由 Linux 发行版的软件包维护者构建和维护，可能在配置上有所不同或由修改的源代码构建。Docker 不参与发布这些软件包，您应向 Linux 发行版的问题跟踪器报告任何与这些软件包相关的错误或问题。

Docker 提供 [二进制文件](binaries.md) 用于手动安装 Docker Engine。这些二进制文件是静态链接的，您可以在任何 Linux 发行版上使用。

## 发布渠道

Docker Engine 有两种更新渠道，**稳定版** 和 **测试版**：

* **稳定版** 渠道为您提供最新发布的通用可用版本。
* **测试版** 渠道为您提供预发布版本，这些版本在通用可用之前已准备好进行测试。

请谨慎使用测试渠道。预发布版本包含实验性和早期访问功能，可能会有破坏性变更。

## 支持

Docker Engine 是一个开源项目，由 Moby 项目维护者和社区成员支持。Docker 不提供 Docker Engine 的支持。Docker 为其产品提供支持，包括 Docker Desktop，它使用 Docker Engine 作为其组件之一。

有关开源项目的详细信息，请参阅 [Moby 项目网站](https://mobyproject.org/)。

### 升级路径

补丁版本始终与其主要和次要版本向后兼容。

### 许可

在大型企业（员工超过 250 人或年收入超过 1000 万美元）中商业使用通过 Docker Desktop 获得的 Docker Engine，需要 [付费订阅](https://www.docker.com/pricing/)。Apache License, Version 2.0。请参阅 [LICENSE](https://github.com/moby/moby/blob/master/LICENSE) 了解完整许可证。

## 报告安全问题

如果您发现安全问题，我们请求您立即向我们报告。

请勿提交公开问题。相反，请将您的报告私下发送至 security@docker.com。

我们非常感谢您的安全报告，Docker 将公开感谢您。

## 开始使用

设置 Docker 后，您可以通过 [Docker 入门](/get-started/introduction/_index.md) 学习基础知识。