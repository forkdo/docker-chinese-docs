---
description: 启用嵌套虚拟化的操作指南
keywords: 嵌套虚拟化, Docker Desktop, windows, VM, VDI 环境
title: 在虚拟机或 VDI 环境中运行 Docker Desktop for Windows
linkTitle: 虚拟机或 VDI 环境
aliases:
  - /desktop/nested-virtualization/
  - /desktop/vm-vdi/
weight: 30
---

Docker 建议在 Mac、Linux 或 Windows 上直接运行 Docker Desktop。但是，只要正确配置虚拟桌面，Docker Desktop for Windows 也可以在虚拟桌面内运行。

要在虚拟桌面环境中运行 Docker Desktop，您可以根据是否支持嵌套虚拟化，选择以下两种方案：

- 如果您的环境支持嵌套虚拟化，您可以使用 Docker Desktop 默认的本地 Linux 虚拟机运行。
- 如果不支持嵌套虚拟化，Docker 建议您订阅并使用 Docker Offload。

## 使用 Docker Offload

[Docker Offload](/offload/) 让您能够将容器工作负载卸载到高性能、完全托管的云环境中，实现无缝的混合体验。

在不支持嵌套虚拟化的虚拟桌面环境中，Docker Offload 非常有用。在这些环境中，Docker Desktop 可以使用 Docker Offload 来确保您仍然可以构建和运行容器，而无需依赖本地虚拟化。

Docker Offload 将 Docker Desktop 客户端与 Docker Engine 解耦，允许 Docker CLI 和 Docker Desktop 仪表板与云资源交互，就像它们是本地资源一样。当您运行容器时，Docker 会通过 SSH 隧道配置一个安全、隔离且临时的云环境连接到 Docker Desktop。尽管是远程运行，绑定挂载和端口转发等功能仍能无缝工作，提供类似本地的体验。要使用 Docker Offload：

要开始使用 Docker Offload，请参阅 [Docker Offload 快速入门](/offload/quickstart/)。

## 使用嵌套虚拟化时的虚拟桌面支持

> [!NOTE]
>
> 在虚拟桌面中运行 Docker Desktop 的支持仅面向 Docker Business 客户，并且仅支持 VMware ESXi 或 Azure VM。

Docker 支持在虚拟机内安装和运行 Docker Desktop，前提是正确启用了嵌套虚拟化。目前仅成功测试了 VMware ESXi 和 Azure 这两种虚拟机管理程序，不支持其他虚拟机。有关 Docker Desktop 支持的更多信息，请参阅 [获取支持](/manuals/support/_index.md)。

对于 Docker 无法控制的问题和间歇性故障，您应联系您的虚拟机管理程序供应商。每个虚拟机管理程序供应商提供的支持级别不同。例如，Microsoft 支持在本地和 Azure 上运行嵌套的 Hyper-V，但有一些版本限制。VMware ESXi 可能不提供相同的支持。

Docker 不支持在虚拟机或 VDI 环境中的同一台机器上运行多个 Docker Desktop 实例。

> [!TIP]
>
> 如果您在 Citrix VDI 中运行 Docker Desktop，请注意 Citrix 可以与多种底层虚拟机管理程序（例如 VMware、Hyper-V、Citrix Hypervisor/XenServer）配合使用。Docker Desktop 需要嵌套虚拟化，而 Citrix Hypervisor/XenServer 不支持嵌套虚拟化。
>
> 请与您的 Citrix 管理员或 VDI 基础设施团队确认使用的是哪种虚拟机管理程序，以及是否启用了嵌套虚拟化。

## 启用嵌套虚拟化

在安装 Docker Desktop 之前，您必须先在不使用 Docker Cloud 的虚拟机上启用嵌套虚拟化。

### 在 VMware ESXi 上启用嵌套虚拟化

在 vSphere 虚拟机内嵌套其他虚拟机管理程序（如 Hyper-V）[不是受支持的场景](https://kb.vmware.com/s/article/2009916)。但是，在 VMware ESXi 虚拟机内运行 Hyper-V 虚拟机在技术上是可行的，根据版本不同，ESXi 包含硬件辅助虚拟化作为受支持的功能。内部测试使用了 1 个 CPU（4 核）和 12GB 内存的虚拟机。

有关如何向客户操作系统公开硬件辅助虚拟化的步骤，请参阅 [VMware 的文档](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/7-0/expose-hardware-assisted-virtualization.html)。

### 在 Azure 虚拟机上启用嵌套虚拟化

Microsoft 支持在 Azure 虚拟机内运行 Hyper-V 的嵌套虚拟化。

对于 Azure 虚拟机，[请检查所选的虚拟机大小是否支持嵌套虚拟化](https://docs.microsoft.com/en-us/azure/virtual-machines/sizes)。Microsoft 提供了 [Azure 虚拟机大小的有用列表](https://docs.microsoft.com/en-us/azure/virtual-machines/acu)，并标出了当前支持嵌套虚拟化的大小。内部测试使用了 D4s_v5 虚拟机。建议使用此规格或更高级别的规格以获得 Docker Desktop 的最佳性能。

## Docker Desktop 在 Nutanix 驱动的 VDI 中的支持

只要底层 Windows 环境支持 WSL 2 或 Windows 容器模式，Docker Desktop 就可以在 Nutanix 驱动的 VDI 环境中使用。由于 Nutanix 正式支持 WSL 2，只要 WSL 2 在 VDI 环境中正常运行，Docker Desktop 就应该能够按预期工作。

如果使用 Windows 容器模式，请确认 Nutanix 环境是否支持 Hyper-V 或其他 Windows 容器后端。

### 支持的配置

Docker Desktop 遵循 [之前](#virtual-desktop-support-when-using-nested-virtualization) 概述的 VDI 支持定义：

- 持久性 VDI 环境（支持）：您在会话之间获得相同的虚拟桌面实例，保留已安装的软件和配置。

- 非持久性 VDI 环境（不支持）：Docker Desktop 不支持操作系统在会话之间重置的环境，这种环境需要每次重新安装或重新配置。

### 支持范围和职责

对于 WSL 2 相关问题，请联系 Nutanix 支持。对于 Docker Desktop 特定问题，请联系 Docker 支持。

## 附加资源

- [Microsoft Dev Box 上的 Docker Desktop](/manuals/enterprise/enterprise-deployment/dev-box.md)