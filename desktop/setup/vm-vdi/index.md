# 在 VM 或 VDI 环境中运行适用于 Windows 的 Docker Desktop

Docker 建议在 Mac、Linux 或 Windows 上原生运行 Docker Desktop。但是，只要虚拟桌面配置得当，适用于 Windows 的 Docker Desktop 可以在虚拟桌面内运行。

要在虚拟桌面环境中运行 Docker Desktop，根据是否支持嵌套虚拟化，您有两个选择：

- 如果您的环境支持嵌套虚拟化，您可以使用其默认的本地 Linux VM 运行 Docker Desktop。
- 如果不支持嵌套虚拟化，Docker 建议订阅并使用 Docker Offload。

## 使用 Docker Offload

[Docker Offload](/offload/) 可让您将容器工作负载卸载到高性能、完全托管的云环境中，从而实现无缝的混合体验。

在不支持嵌套虚拟化的虚拟桌面环境中，Docker Offload 非常有用。在这些环境中，Docker Desktop 可以使用 Docker Offload，确保您无需依赖本地虚拟化即可构建和运行容器。

Docker Offload 将 Docker Desktop 客户端与 Docker Engine 解耦，允许 Docker CLI 和 Docker Desktop Dashboard 与基于云的资源进行交互，就像它们是本地资源一样。当您运行容器时，Docker 会配置一个安全、隔离且短暂的云环境，该环境通过 SSH 隧道连接到 Docker Desktop。尽管是远程运行，但绑定挂载和端口转发等功能仍能无缝工作，提供类似本地的体验。要使用 Docker Offload：

要开始使用 Docker Offload，请参阅 [Docker Offload 快速入门](/offload/quickstart/)。

## 使用嵌套虚拟化时的虚拟桌面支持

> [!NOTE]
>
> 运行 Docker Desktop 仅在 VMware ESXi 或 Azure VM 上向 Docker Business 客户提供虚拟桌面支持。

Docker 支持在 VM 内安装和运行 Docker Desktop，前提是正确启用了嵌套虚拟化。唯一经过成功测试的管理程序是 VMware ESXi 和 Azure，不支持其他 VM。有关 Docker Desktop 支持的更多信息，请参阅 [获取支持](/manuals/support/_index.md)。

对于超出 Docker 控制范围的故障排除问题和间歇性故障，您应联系您的管理程序供应商。每个管理程序供应商提供不同级别的支持。例如，Microsoft 支持在本地和 Azure 上运行嵌套 Hyper-V，但有一些版本限制。VMware ESXi 可能并非如此。

Docker 不支持在 VM 或 VDI 环境中的同一台机器上运行多个 Docker Desktop 实例。

> [!TIP]
>
> 如果您在 Citrix VDI 内运行 Docker Desktop，请注意 Citrix 可与各种底层管理程序一起使用，例如 VMware、Hyper-V、Citrix Hypervisor/XenServer。Docker Desktop 需要嵌套虚拟化，而 Citrix Hypervisor/XenServer 不支持嵌套虚拟化。
>
> 请咨询您的 Citrix 管理员或 VDI 基础架构团队，以确认正在使用哪个管理程序，以及是否启用了嵌套虚拟化。

## 开启嵌套虚拟化

在不会使用 Docker Cloud 的虚拟机上安装 Docker Desktop 之前，必须开启嵌套虚拟化。

### 在 VMware ESXi 上开启嵌套虚拟化

在 vSphere VM 中嵌套虚拟化其他管理程序（如 Hyper-V）[不是受支持的场景](https://kb.vmware.com/s/article/2009916)。但是，在 VMware ESXi VM 中运行 Hyper-V VM 在技术上是可行的，并且根据版本不同，ESXi 包含作为受支持功能的硬件辅助虚拟化。内部测试使用了具有 1 个 CPU（4 个核心）和 12GB 内存的 VM。

有关如何将硬件辅助虚拟化暴露给客户操作系统的步骤，请参阅 [VMware 的文档](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/7-0/expose-hardware-assisted-virtualization.html)。

### 在 Azure 虚拟机上开启嵌套虚拟化

Microsoft 支持在 Azure VM 内部运行 Hyper-V 的嵌套虚拟化。

对于 Azure 虚拟机，[请检查所选 VM 大小是否支持嵌套虚拟化](https://docs.microsoft.com/en-us/azure/virtual-machines/sizes)。Microsoft 提供了 [Azure VM 大小的有用列表](https://docs.microsoft.com/en-us/azure/virtual-machines/acu)，并突出显示了当前支持嵌套虚拟化的大小。内部测试使用了 D4s_v5 机器。为获得 Docker Desktop 的最佳性能，请使用此规格或更高规格。

## Nutanix 支持的 VDI 上的 Docker Desktop 支持

只要底层 Windows 环境支持 WSL 2 或 Windows 容器模式，就可以在 Nutanix 支持的 VDI 环境中使用 Docker Desktop。由于 Nutanix 官方支持 WSL 2，只要 WSL 2 在 VDI 环境中正确运行，Docker Desktop 就应该按预期工作。

如果使用 Windows 容器模式，请确认 Nutanix 环境支持 Hyper-V 或其他 Windows 容器后端。

### 支持的配置

Docker Desktop 遵循[前面](#使用嵌套虚拟化时的虚拟桌面支持)概述的 VDI 支持定义：

- **持久性 VDI 环境（受支持）**：您在会话之间接收相同的虚拟桌面实例，保留已安装的软件和配置。
- **非持久性 VDI 环境（不受支持）**：Docker Desktop 不支持在会话之间重置操作系统、每次都需要重新安装或重新配置的环境。

### 支持范围和责任

对于与 WSL 2 相关的问题，请联系 Nutanix 支持。对于 Docker Desktop 特定的问题，请联系 Docker 支持。

## 其他资源

- [Microsoft Dev Box 上的 Docker Desktop](/manuals/enterprise/enterprise-deployment/dev-box.md)
