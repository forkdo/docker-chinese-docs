# 旧版本发行说明

此页面包含 Docker Desktop for Windows 旧版本的发行说明。

## 2018 年稳定版

### Docker Community Edition 18.06.1-ce-win73 2018-08-29

* 升级
  - [Docker 18.06.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.06.1-ce)

* Bug 修复和微小改动
  - 修复 VM 活动检测中的 Bug，防止 Docker Desktop 启动。修复 [docker/for-win#2404](https://github.com/docker/for-win/issues/2404)
  - 修复当 Windows 服务未运行时的检测 Bug，并建议重启服务。
  - 修复容器内部本地 DNS 解析失败的问题。修复 [docker/for-win#2301](https://github.com/docker/for-win/issues/2301), [docker/for-win#2304](https://github.com/docker/for-win/issues/2304)
  - 修复重置为出厂默认值后 Kubernetes 状态显示问题
  - 修复在某些情况下 `host.docker.internal` 无法解析的 Bug。修复 [docker/for-win#2402](https://github.com/docker/for-win/issues/2402)
  - 使用 1MB 的 vhdx 块大小代替默认的 32MB。参见 [docker/for-win#244](https://github.com/docker/for-win/issues/244)。另请参阅 [Microsoft 在 Hyper-V 上运行 Linux 的最佳实践](https://docs.microsoft.com/en-us/windows-server/virtualization/hyper-v/best-practices-for-running-linux-on-hyper-v)
  - 修复在特定情况下当 Windows 服务未启动时的诊断问题。
  - 更改 Samba 默认文件权限，以避免权限过于开放的问题。修复 [docker/for-win#2170](https://github.com/docker/for-win/issues/2170)
  - 在 RS5 Insider 版本上，修复了错误检测到缺少 "Containers" 功能的问题，该问题要求您安装该功能然后重新启动。

### Docker Community Edition 18.06.0-ce-win72 2018-07-26

* 新增
  - 更新了签名证书。在更新后的证书被列入白名单之前，安装程序可能会显示 Windows Defender 弹窗。点击“更多信息”查看应用由“Docker Inc”发布，然后运行它。

* Bug 修复和微小改动
  - 修复了在启动 Docker Desktop 时，如果 "Hyper-V" 和 "Containers" Windows 功能尚未启用，自动启用功能的 Bug。

### Docker Community Edition 18.06.0-ce-win70 2018-07-25

* 升级
  - [Docker 18.06.0-ce](https://github.com/docker/docker-ce/releases/tag/v18.06.0-ce)
  - [Docker Machine 0.15.0](https://github.com/docker/machine/releases/tag/v0.15.0)
  - [Docker compose 1.22.0](https://github.com/docker/compose/releases/tag/1.22.0)
  - [LinuxKit v0.4](https://github.com/linuxkit/linuxkit/releases/tag/v0.4)
  - Linux Kernel 4.9.93，启用了 CEPH、DRBD、RBD、MPLS_ROUTING 和 MPLS_IPTUNNEL

* 新增
  - Kubernetes 支持。您现在可以从 Docker for Windows 设置中的 "Kubernetes" 面板运行单节点 Kubernetes 集群，并使用 kubectl 命令以及 Docker 命令。参见 [Kubernetes 部分](/manuals/desktop/use-desktop/kubernetes.md)

* Bug 修复和微小改动
  - AUFS 存储驱动在 Docker Desktop 中已弃用，AUFS 支持将在下一个主要版本中移除。您可以在 Docker Desktop 18.06.x 中继续使用 AUFS，但在更新到下一个主要更新之前，您需要重置磁盘映像（在“设置”>“重置”菜单中）。您可以查阅文档以[保存映像](/reference/cli/docker/image/save/#examples)和[备份卷](/manuals/engine/storage/volumes.md#back-up-restore-or-migrate-data-volumes)
  - 修复在某些情况下导致虚拟机日志写入 RAM 而不是磁盘，并导致虚拟机挂起的 Bug。
  - 修复与 docker 服务的命名管道连接的安全问题。
  - 修复 VPNKit 内存泄漏。修复 [docker/for-win#2087](https://github.com/docker/for-win/issues/2087), [moby/vpnkit#371](https://github.com/moby/vpnkit/issues/371)
  - 修复在最新的 1709 Windows 更新中使用 Windows 快速启动时的重启问题。修复 [docker/for-win#1741](https://github.com/docker/for-win/issues/1741), [docker/for-win#1741](https://github.com/docker/for-win/issues/1741)
  - DNS 名称 `host.docker.internal` 可用于从 Windows 容器解析主机。修复 [docker/for-win#1976](https://github.com/docker/for-win/issues/1976)
  - 修复诊断窗口中的损坏链接。
  - 为虚拟机内的 docker-ce 日志添加了日志轮转。
  - 更改了 smb 权限，以避免在容器中尝试使用不同用户操作文件时出现问题。修复 [docker/for-win#2170](https://github.com/docker/for-win/issues/2170)

### Docker Community Edition 18.03.1-ce-win65 2018-04-30

* 升级
  - [Docker 18.03.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.1-ce)
  - [Docker compose 1.21.1](https://github.com/docker/compose/releases/tag/1.21.1)
  - [Notary 0.6.1](https://github.com/docker/notary/releases/tag/v0.6.1)

* Bug 修复和微小改动
  - 修复当 HOME 环境变量已定义时（通常从命令行启动）的启动失败问题。修复 [docker/for-win#1880](https://github.com/docker/for-win/issues/1880)
  - 修复因与其他程序（如 Razer Synapse 3）不兼容导致的启动失败。修复 [docker/for-win#1723](https://github.com/docker/for-win/issues/1723)

### Docker Community Edition 18.03.1-ce-win64 2018-04-26

* 升级
  - [Docker 18.03.1-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.1-ce)
  - [Docker compose 1.21.0](https://github.com/docker/compose/releases/tag/1.21.0)
  - [Notary 0.6.1](https://github.com/docker/notary/releases/tag/v0.6.1)

* Bug 修复和微小改动
  - 修复当 HOME 环境变量已定义时（通常从命令行启动）的启动失败问题。修复 [docker/for-win#1880](https://github.com/docker/for-win/issues/1880)
  - 修复因与其他程序（如 Razer Synapse 3）不兼容导致的启动失败。修复 [docker/for-win#1723](https://github.com/docker/for-win/issues/1723)

### Docker Community Edition 18.03.0-ce-win59 2018-03-26

* 升级
  - [Docker 18.03.0-ce](https://github.com/docker/docker-ce/releases/tag/v18.03.0-ce)
  - [Docker Machine 0.14.0](https://github.com/docker/machine/releases/tag/v0.14.0)
  - [Docker compose 1.20.1](https://github.com/docker/compose/releases/tag/1.20.1)
  - [Notary 0.6.0](https://github.com/docker/notary/releases/tag/v0.6.0)
  - Linux Kernel 4.9.87
  - AUFS 20180312

* 新增
  - 可在设置中更改虚拟机磁盘大小。修复 [docker/for-win#105](https://github.com/docker/for-win/issues/105)
  - 可在设置中更改虚拟机交换区大小。
  - 新增重启 Docker 的菜单项。
  - 支持 NFS 卷共享。参见 [docker/for-win#1700](https://github.com/docker/for-win/issues/1700)
  - 允许在安装期间激活 Windows 容器（当仅处理 Windows 容器时，避免创建虚拟机磁盘和启动虚拟机）。参见 [docker/for-win#217](https://github.com/docker/for-win/issues/217)。
  - 实验性功能：LCOW 容器现在可以与 Windows 容器并行运行（在 Windows RS3 build 16299 及更高版本上）。在 Windows 容器模式下使用 `--platform=linux` 来运行 Windows 上的 Linux 容器。请注意，LCOW 是实验性的；它需要守护程序的 `experimental` 选项。

* Bug 修复和微小改动
  - 修复在 Windows 10 build 16299 安装 KB4074588 后的 Windows 容器端口转发问题。修复 [docker/for-win#1707](https://github.com/docker/for-win/issues/1707), [docker/for-win#1737](https://github.com/docker/for-win/issues/1737)
  - 修复在设置 TLS 相关选项时守护程序无法正常启动的问题。
  - DNS 名称 `host.docker.internal` 应用于从容器解析主机。旧的别名（仍然有效）已弃用，推荐使用此名称。（参见 https://tools.ietf.org/html/draft-west-let-localhost-be-localhost-06）。
  - 修复在使用 "localhost" 名称（例如 `host.docker.internal`）时的 HTTP/S 透明代理问题。修复 [docker/for-win#1130](https://github.com/docker/for-win/issues/1130)
  - 修复在 Windows RS4 Insider 上启动 Linuxkit 的问题。修复 [docker/for-win#1458](https://github.com/docker/for-win/issues/1458), [docker/for-win#1514](https://github.com/docker/for-win/issues/1514), [docker/for-win#1640](https://github.com/docker/for-win/issues/1640)
  - 修复权限提升风险。(https://www.tenable.com/sc-report-templates/microsoft-windows-unquoted-service-path-vulnerability)
  - docker-users 组中的所有用户现在都可以使用 Docker。修复 [docker/for-win#1732](https://github.com/docker/for-win/issues/1732)
  - Docker For Windows 安装程序中不再提供 Docker Toolbox 镜像的迁移（仍然可以手动迁移 Toolbox 镜像）。
  - 在重置/卸载时更好地清理 Windows 容器和镜像。修复 [docker/for-win#1580](https://github.com/docker/for-win/issues/1580), [docker/for-win#1544](https://github.com/docker/for-win/issues/1544), [docker/for-win#191](https://github.com/docker/for-win/issues/191)
  - 安装程序中桌面图标的创建是可选的；在升级时不重新创建桌面图标（在下次升级时生效）。修复 [docker/for-win#246](https://github.com/docker/for-win/issues/246), [docker/for-win#925](https://github.com/docker/for-win/issues/925), [docker/for-win#1551](https://github.com/docker/for-win/issues/1551)

### Docker Community Edition 17.12.0-ce-win47 2018-01-12

* Bug 修复和微小改动
  - 修复 linuxkit 端口转发器有时无法启动的问题。修复 [docker/for-win#1506](https://github.com/docker/for-win/issues/1506)
  - 修复连接到私有注册表时的证书管理问题。修复 [docker/for-win#1512](https://github.com/docker/for-win/issues/1512)
  - 修复挂载兼容性问题，当使用 `-v //c/...` 挂载驱动器时，现在在 linuxkit 虚拟机中挂载到 /host_mnt/c。修复 [docker/for-win#1509](https://github.com/docker/for-win/issues/1509), [docker/for-win#1516](https://github.com/docker/for-win/issues/1516), [docker/for-win#1497](https://github.com/docker/for-win/issues/1497)
  - 修复图标显示边缘问题。修复 [docker/for-win#1508](https://github.com/docker/for-win/issues/1508)

### Docker Community Edition 17.12.0-ce-win46 2018-01-09

* 升级
  - [Docker 17.12.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.12.0-ce)
  - [Docker compose 1.18.0](https://github.com/docker/compose/releases/tag/1.18.0)
  - [Docker Machine 0.13.0](https://github.com/docker/machine/releases/tag/v0.13.0)
  - Linux Kernel 4.9.60

* 新增
  - 虚拟机完全由 linuxkit 构建
  - 为 Windows 添加 localhost 端口转发器（感谢 @simonferquel）。当可用时（Insider build RS4）使用 Microsoft localhost 端口转发器。

* Bug 修复和微小改动
  - 在“关于”框中显示各种组件版本。
  - 修复当用户名包含空格时的 vpnkit 问题。参见 [docker/for-win#1429](https://github.com/docker/for-win/issues/1429)
  - 诊断改进，在 VM 关闭前获取 VM 日志。
  - 修复安装程序对不支持的 Windows `CoreCountrySpecific` 版本的检查。
  - 修复一类启动失败问题，即数据库启动失败。参见 [docker/for-win#498](https://github.com/docker/for-win/issues/498)
  - 更新变更日志中的链接现在打开默认浏览器而不是 IE。（修复 [docker/for-win#1311](https://github.com/docker/for-win/issues/1311)）

## 2017 年稳定版

### Docker Community Edition 17.09.1-ce-win42 2017-12-11

* 升级
  - [Docker 17.09.1-ce](https://github.com/docker/docker-ce/releases/tag/v17.09.1-ce)
  - [Docker compose 1.17.1](https://github.com/docker/compose/releases/tag/1.17.1)
  - [Docker Machine 0.13.0](https://github.com/docker/machine/releases/tag/v0.13.0)

* Bug 修复和微小改动
  - 修复 Windows 快速启动过程中的 Bug。修复 [for-win/#953](https://github.com/docker/for-win/issues/953)
  - 修复卸载程序问题（在某些特定情况下 dockerd 进程未被正确终止）
  - 修复 Net Promoter Score Gui Bug。修复 [for-win/#1277](https://github.com/docker/for-win/issues/1277)
  - 修复 `docker.for.win.localhost` 在代理设置中不起作用的问题。修复 [for-win/#1130](https://github.com/docker/for-win/issues/1130)
  - 将虚拟机启动超时时间增加到 2 分钟。

### Docker Community Edition 17.09.0-ce-win33 2017-10-06

* Bug 修复
  - 修复 Docker For Windows 在某些情况下无法启动的问题：移除了有时导致 vpnkit 进程死亡的 libgmp 的使用。

### Docker Community Edition 17.09.0-ce-win32 2017-10-02

* 升级
  - [Docker 17.09.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.09.0-ce)
  - [Docker Compose 1.16.1](https://github.com/docker/compose/releases/tag/1.16.1)
  - [Docker Machine 0.12.2](https://github.com/docker/machine/releases/tag/v0.12.2)
  - [Docker Credential Helpers 0.6.0](https://github.com/docker/docker-credential-helpers/releases/tag/v0.6.0)
  - Linux Kernel 4.9.49
  - AUFS 20170911

* 新增
  - Windows Docker 守护程序现在作为服务启动，以实现更好的生命周期管理
  - 将 Linux 守护程序配置存储在 ~\.docker\daemon.json 中，而不是设置文件中
  - 将 Windows 守护程序配置存储在 C:\ProgramData\Docker\config\daemon.json 中，而不是设置文件中
  - VPNKit：添加对 ping 的支持！
  - VPNKit：添加 slirp/port-max-idle-timeout，允许调整超时甚至禁用
  - VPNKit：桥接模式现在在所有地方都是默认模式
  - 在更新窗口中添加 `跳过此版本` 按钮

* 安全修复
  - VPNKit：安全修复，以降低 DNS 缓存中毒攻击的风险（由 Hannes Mehnert https://hannes.nqsb.io/ 报告）

* Bug 修复和微小改动
  - 内核：启用 TASK_XACCT 和 TASK_IO_ACCOUNTING
  - 更频繁地轮转虚拟机中的日志 (docker/for-win#244)
  - 重置为默认值会停止所有引擎并删除设置，包括所有 daemon.json 文件
  - 更好的后端服务检查（与 https://github.com/docker/for-win/issues/953 相关）
  - 修复自动更新复选框，无需重启应用程序
  - 修复当自动更新禁用时检查更新菜单的问题
  - VPNKit：当 ICMP 权限被拒绝时，不要阻止启动。（修复 docker/for-win#1036, docker/for-win#1035, docker/for-win#1040）
  - VPNKit：更改协议以支持从服务器报告的错误消息
  - VPNKit：修复一个 Bug，如果相应的 TCP 连接空闲超过 5 分钟，会导致套接字泄漏（与 [docker/for-mac#1374](https://github.com/docker/for-mac/issues/1374) 相关）
  - VPNKit：改进围绕 UNIX 域套接字连接的日志记录
  - VPNKit：自动修剪整数或布尔数据库键的空白
  - 启动时不要将凭证移入凭证存储

### Docker Community Edition 17.06.2-ce-win27 2017-09-06

* 升级
  - [Docker 17.06.2-ce](https://github.com/docker/docker-ce/releases/tag/v17.06.2-ce)
  - [Docker Machine 0.12.2](https://github.com/docker/machine/releases/tag/v0.12.2)

### Docker Community Edition 17.06.1-ce-rc1-win24 2017-08-24

**升级**

- [Docker 17.06.1-ce-rc1](https://github.com/docker/docker-ce/releases/tag/v17.06.1-ce-rc1)
- Linux Kernel 4.9.36
- AUFS 20170703

**Bug 修复和微小改动**

- 修复锁定的容器 ID 文件（修复 [docker/for-win#818](https://github.com/docker/for-win/issues/818)）
- 避免在 PATH 环境变量中扩展变量（修复 [docker/for-win#859](https://github.com/docker/for-win/issues/859)）

### Docker Community Edition 17.06.0-ce-win18 2017-06-28

**升级**

- [Docker 17.06.0-ce](https://github.com/docker/docker-ce/releases/tag/v17.06.0-ce)
- [Docker Credential Helpers 0.5.2](https://github.com/docker/docker-credential-helpers/releases/tag/v0.5.2)
- [Docker Machine 0.12.0](https://github.com/docker/machine/releases/tag/v0.12.0)
- [Docker compose 1.14.0](https://github.com/docker/compose/releases/tag/1.14.0)
- Linux Kernel 4.9.31

**新增**

- Windows Server 2016 支持
- Windows 10586 标记为已弃用；在未来的稳定版中不再支持
- 与 Docker Cloud 集成，能够从本地命令行界面 (CLI) 控制远程 Swarm 并查看您的存储库
- Docker CLI 和 Docker Hub、Docker Cloud 之间的统一登录。
- 共享驱动器可以在请求挂载时按需完成
- 添加一个用于主机的实验性 DNS 名称：docker.for.win.localhost
- 支持用于验证注册表访问的客户端（即“登录”）证书（修复 [docker/for-win#569](https://github.com/docker/for-win/issues/569)）
- 新的安装程序体验

**Bug 修复和微小改动**

- 修复了使用 Active Directory 登录的用户的组访问检查（修复 [docker/for-win#785](https://github.com/docker/for-win/issues/785)）
- 检查环境变量，并在日志中添加一些警告，如果它们可能导致 docker 失败
- 许多以前以管理员模式运行的进程现在以用户身份运行
- 云联合命令行现在在用户主目录中打开
- 命名管道现在使用限制性更强的安全描述符创建，以提高安全性
- 安全修复：用户必须是特定组 "docker-users" 的成员才能运行 Docker for Windows
- 重置为默认值/卸载也会重置 Docker cli 设置，并从 Docker Cloud 和注册表注销用户
- 检测到阻止 Windows 容器工作的 bitlocker 策略
- 修复了在 vmswitch 接口上显式禁用时的文件共享问题
- 修复了当计算机名称非常长时虚拟机无法启动的问题
- 修复了 Windows daemon.json 文件未被写入的 Bug（修复 [docker/for-win#670](https://github.com/docker/for-win/issues/670)）
- 为内核添加了补丁以修复 VMBus 崩溃
- 命名管道客户端连接在 `docker run` 时 stdin 中有数据的情况下不应再触发死锁
- 当 docker 客户端请求升级到原始流时，应正确处理缓冲数据

### Docker Community Edition 17.03.1-ce-win12  2017-05-12

**升级**

- CVE-2017-7308 安全修复

### Docker Community Edition 17.03.0, 2017-03-02

**新增**

- 重命名为 Docker Community Edition
- 与 Docker Cloud 集成：从本地 CLI 控制远程 Swarm 并查看您的存储库。此功能将逐步向所有用户推出

**升级**

- [Docker 17.03.0-ce](https://github.com/docker/docker/releases/tag/v17.03.0-ce)
- [Docker Compose 1.11.2](https://github.com/docker/compose/releases/tag/1.11.2)
- [Docker Machine 0.10.0](https://github.com/docker/machine/releases/tag/v0.10.0)
- Linux kernel 4.9.12

**Bug 修复和微小改动**

- 通过 ID 而不是名称匹配 Hyper-V 集成服务
- 服务停止时不消耗 100% CPU
- 上传时记录诊断 ID
- 改进防火墙处理：停止列出规则，因为这可能需要很长时间
- 当所需引擎启动失败时，不要回滚到之前的引擎
- 不要在 Linux 虚拟机内部使用端口 4222
- 修复了 Set-VMFirmware 中的 ObjectNotFound 启动错误
- 配置防火墙时添加详细日志
- 添加了指向实验性功能文档的链接
- 修复了“关于”对话框中的版权
- VPNKit：修复包含指向标签指针的指针的 DNS 数据包的解组
- VPNKit：在来自缓存的 DNS 响应上设置“可用递归”位
- VPNKit：避免诊断捕获过多数据
- VPNKit：修复虚拟以太网链路上偶尔丢包（截断）的来源
- 修复了 TimeSync 协议版本的协商（通过内核更新）

### Docker for Windows 1.13.1, 2017-02-09

- [Docker 1.13.1](https://github.com/docker/docker/releases/tag/v1.13.1)
- [Docker Compose 1.11.1](https://github.com/docker/compose/releases/tag/1.11.1)
- Linux kernel 4.9.8

**Bug 修复和微小改动**

- 添加指向实验性功能的链接
- 新的 1.13 可取消操作现在应由桌面 Docker 正确处理
- 各种错别字修复
- 修复 Hyper-V VM 设置（应修复 `ObjectNotFound` 错误）

### Docker for Windows 1.13.0, 2017-01-19
- [Docker 1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)
- [Docker Compose 1.10](https://github.com/docker/compose/releases/tag/1.10.0)
- [Docker Machine 0.9.0](https://github.com/docker/machine/releases/tag/v0.9.0)
- [Notary 0.4.3](https://github.com/docker/notary/releases/tag/v0.4.3)
- Linux kernel 4.9.4

**新增**

- Windows 容器
- 改进的 Daemon.json 编辑 UI
- 包含镜像和非主机挂载卷的 VHDX 文件可以移动（使用 UI 中的“高级”选项卡）
- 支持使用 qemu 的 arm、aarch64、ppc64le 架构
- 磁盘 TRIM 支持（缩小虚拟磁盘）
- 主机从睡眠模式唤醒后强制进行虚拟机时间同步
- 可以切换 Docker 实验模式

**Bug 修复和微小改动**

- 改进的代理 UI
- 改进的日志记录和诊断
- “关于”框现在支持复制/粘贴
- 改进的驱动器共享代码
- 优化的启动过程
- Trend Micro Office Scan 使 API 代理认为没有共享驱动器
- 显示指向虚拟化文档的链接
- 在出厂重置时始终删除磁盘
- VPNKit：改进的诊断
- VPNKit：转发的 UDP 数据报具有正确的源端口号
- VPNKit：如果一个请求失败，允许其他并发请求成功。例如，这允许 IPv4 服务器即使在 IPv6 损坏时也能工作。
- VPNKit：修复可能导致连接跟踪低估活动连接数的 Bug
- VPNKit：添加 DNS 响应的本地缓存

## 2016 年稳定版

### Docker for Windows 1.12.5, 2016-12-20
- Docker 1.12.5
- Docker Compose 1.9.0

### 跳过 Docker for Windows 1.12.4

我们没有分发 1.12.4 稳定版

### Docker for Windows 1.12.3, 2016-11-09

**新增**

- 用户更改后恢复虚拟机的配置

- 检测可能阻止文件共享的防火墙配置

- 发送更多 GUI 使用统计信息以帮助我们改进产品

- HyperV 磁盘的路径不再是硬编码，使 Toolbox 导入可以在非标准路径下工作

- 验证所有 HyperV 功能是否已启用

- 将 Moby 控制台添加到日志

- 将当前引擎与其他设置一起保存

- 安装了 Notary 版本 0.4.2

- 重新设计了文件共享对话框和底层机制
  - 预填充用户名
  - 当用户/密码无效时，反馈更快、更可靠
  - 更好地支持域用户
  - 当文件共享因其他原因失败时，在日志中显示错误消息

**升级**

- Docker 1.12.3
- Linux Kernel 4.4.27
- Docker Machine 0.8.2
- Docker Compose 1.8.1
- aufs 20160912

**Bug 修复和微小改动**

**常规**

- 将设置添加到诊断中

- 确保我们没有使用 GAC 中的旧 Nlog 库

- 修复了密码转义回归

- 支持向数据库写入大值，特别是受信任的 CA

- 保留 Powershell 堆栈跟踪

- 在每个日志文件的顶部写入操作系统和应用程序版本

- 如果仅设置了 DNS 服务器，则不重新创建虚拟机

- 如果未能正确停止服务，卸载程序现在会终止该服务

- 改进的调试信息

**网络**

- 如果 VpnKit 停止，现在会重新启动

- VpnKit：施加连接限制以避免耗尽文件描述符

- VpnKit：处理大于 2035 字节的 UDP 数据报

- VpnKit：减少 DNS 消耗的文件描述符数量

**文件共享**

- 共享驱动器的挂载/卸载速度更快

- 为挂载/卸载共享驱动器添加了超时

**Hyper-V**

- 确保不使用无效的 "DockerNat" 交换机

**Moby**

- 增加默认的 ulimit 用于 memlock（修复 [https://github.com/docker/for-mac/issues/801](https://github.com/docker/for-mac/issues/801)）

### Docker for Windows 1.12.1, 2016-09-16

**新增**

* 为了透明地支持受信任的注册表，Windows 主机上的所有受信任 CA（根或中间）都会自动复制到 Moby

* `重置凭证` 也会取消共享驱动器

* 日志现在每天轮转

* 支持多个 DNS 服务器

* 添加了 `mfsymlinks` SMB 选项以支持绑定挂载文件夹上的符号链接

* 添加了 `nobrl` SMB 选项以支持绑定挂载文件夹上的 `sqlite`

* 检测过时的 Kitematic 版本

**升级**

* Docker 1.12.1
* Docker machine 0.8.1
* Linux kernel 4.4.20
* aufs 20160905

**Bug 修复和微小改动**

**常规**

* 上传诊断现在在设置中显示正确的状态消息

* 升级后 Docker 停止询问是否从 Toolbox 导入

* Docker 现在可以在 HyperV 激活后立即从 Toolbox 导入

* 向诊断添加了更多调试信息

* 当 Mixpanel 不可用时，发送匿名统计信息不再挂起

* 支持发行说明中的换行符

* 改进当 Docker 守护程序无响应时的错误消息

* 配置数据库现在存储在内存中

* 保留 PowerShell 错误的堆栈跟踪

* 在错误窗口中显示服务堆栈跟踪

**网络**

* 改进名称服务器发现
* VpnKit 支持搜索域
* VpnKit 现在使用 OCaml 4.03 而不是 4.02.3 编译

**文件共享**

* 将 `cifs` 版本设置为 3.02

* VnpKit：减少 UDP NAT 使用的套接字数量，降低概率

* `slirp`：减少 UDP NAT 使用的套接字数量，降低 NAT 规则比预期更早超时的概率

* 修复了主机文件系统共享的密码处理

**Hyper-V**

* 自动禁用阻止 Docker 启动或使用网络的残留网络适配器

* 在 `重置为出厂默认值` 时自动删除重复的 MobyLinuxVM

* 改进了 HyperV 检测和激活机制

**Moby**

* 修复了 Moby 诊断和更新内核

* 使用默认的 `sysfs` 设置，禁用透明大页

* `Cgroup` 挂载以支持容器中的 `systemd`

**已知问题**

* Docker 会自动禁用残留的网络适配器。删除它们的唯一方法是手动使用 `devmgmt.msc`。

### Docker for Windows 1.12.0, 2016-07-28

- 首个稳定版

**组件**

* Docker 1.12.0
* Docker Machine 0.8.0
* Docker Compose 1.8.0
