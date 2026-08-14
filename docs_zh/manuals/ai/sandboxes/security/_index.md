<!-- FILE: manuals/ai/sandboxes/security/_index.md -->

---
title: 安全模型
linkTitle: 安全模型
weight: 80
description: Docker Sandboxes 的信任边界、隔离层和安全属性。
keywords: docker sandboxes, security model, isolation, trust boundaries, microVM
---

Docker Sandboxes 在 microVM 中运行 AI agent，使它们能够执行代码、安装包和使用工具，而无需访问你的宿主系统。多层隔离保护着你的宿主系统。

## 信任边界

主要的信任边界是 microVM。agent 在 VM 内部拥有完全的控制权，包括 sudo 权限。VM 边界阻止 agent 触达你宿主上的任何东西，除非被显式共享。

跨越边界进入 VM 的内容：

- **工作区目录：** 挂载进 VM。默认的直接挂载是读写——agent 就地编辑你的工作树。使用 [`--clone`](../usage.md#clone-mode) 时，你的仓库以只读方式挂载，agent 在一个私有的克隆上工作。
- **凭据：** 宿主侧的代理将鉴权头部注入到出站 HTTP 请求中。原始的凭据值永远不会进入 VM。
- **网络访问：** 发往[允许域](defaults/)的 HTTP 和 HTTPS 请求通过宿主代理转发。
- **共享 agent 技能：** 一个持久的宿主侧存储以读写方式挂载到 agent 的技能目录，除非你在创建沙盒时选择退出。其他沙盒中的受支持 agent 会挂载同一个存储。
- **MCP 网关流量：** 受支持的 agent 连接到宿主侧的 MCP 网关端点。该网关负责代理访问已注册的 MCP 服务器。

跨越边界回到宿主的内容：

- **工作区文件更改：** 使用默认的直接挂载时，在你的宿主上实时可见。
- **HTTP/HTTPS 请求：** 通过宿主代理发送到允许的域。
- **共享技能更改：** 写入宿主侧存储，并对共享它的其他沙盒可见。

在工作区和共享技能存储之外，agent 无法访问你的宿主文件系统。它也无法访问你的宿主 Docker 守护进程、宿主网络或 localhost，或任何不在允许列表中的域。沙盒之间不能通过直接网络进行通信。原始的 TCP、UDP 和 ICMP 在网络层被阻止。

MCP 服务器是一个显式的集成点。远程 MCP 服务器运行在 Docker Sandboxes 之外，而本地 stdio MCP 服务器运行在宿主上，而不是在沙盒 VM 内部。agent 可以通过 MCP 网关调用这些服务器暴露的工具，当组织管控生效时，需受 MCP 策略约束。将本地 MCP 服务器视为受信任的宿主集成。

![沙盒安全模型，展示沙盒 VM 与宿主系统之间的 hypervisor 边界。工作区目录以读写方式共享。agent 进程、Docker Engine、包和 VM 文件系统都在 VM 内部。宿主的文件系统、进程、Docker Engine 和网络都在 VM 外部且不可访问。一个代理强制执行允许/拒绝策略并向出站请求注入凭据。](../images/sbx-security.png)

## 隔离层

沙盒安全模型有五层。有关每一层的技术细节，请参阅 [隔离层](isolation/)。

- **Hypervisor 隔离：** 每个沙盒拥有独立的内核。与宿主之间没有共享内存或进程。
- **网络隔离：** 所有 HTTP/HTTPS 流量通过宿主转发。[默认拒绝策略](defaults/)。非 HTTP 协议被完全阻止。
- **Docker Engine 隔离：** 每个沙盒拥有自己的 Docker Engine，与宿主守护进程之间没有路径。
- **工作区隔离**（通过 `--clone` 选择加入）：agent 在一个私有的 VM 内克隆上工作，你的仓库以只读方式挂载。默认的直接模式不施加任何工作区边界——agent 就地编辑你的工作树。
- **凭据隔离：** API 密钥由宿主侧代理注入到 HTTP 头部中。凭据值永远不会进入 VM。

## agent 在沙盒内部能做什么

在 VM 内部，agent 拥有完全权限：sudo 访问、包安装、一个私有的 Docker Engine，以及对工作区的读写访问。安装的包、Docker 镜像和其他 VM 状态在重启之间持续存在。有关允许和阻止内容的完整说明，请参阅 [默认安全态势](defaults/)。

## 默认情况下未被隔离的内容

沙盒将 agent 与你的宿主系统隔离开来，但 agent 的操作仍可以通过共享工作区和允许的网络通道影响你。

在直接模式下，工作区更改实时存在于你的宿主上。在默认的直接挂载下，agent 编辑的是你在宿主上看到的相同文件。这包括在正常开发期间隐式执行的文件：Git hooks、CI 配置、IDE 任务配置、AI 项目配置和设置、`Makefile`、`package.json` 脚本以及类似的构建文件。在运行任何被修改的代码之前，请审查更改。注意 Git hooks 位于 `.git/` 内部，不会出现在 `git diff` 输出中——请单独检查它们。请参阅 [工作区隔离](isolation/#workspace-isolation) 获取完整列表以及替代的克隆模式边界。

默认的允许域包含宽泛的通配符。一些默认值如 `*.googleapis.com` 覆盖了许多超出 AI API 的服务。运行 `sbx policy ls` 查看活动规则的完整列表，并移除你不需要的条目。请参阅 [默认安全态势](defaults/)。

Kit 以 root 权限在沙盒内部运行安装命令。为限制供应链风险，`sbx` 将 kit 安装限制在默认仅 Docker Hub 的来源允许列表中。请参阅 [限制 kit 来源](../customize/kits.md#restrict-kit-sources)。

共享 agent 技能对跨沙盒隔离构成了一个狭窄的例外。该存储以读写方式挂载，因此一个沙盒可以修改另一个沙盒稍后加载的指令或脚本。这不会暴露宿主文件系统的其余部分，也不会在沙盒之间创建直接的网络路径，但它确实将参与其中的沙盒置于同一个信任边界中。请参阅 [共享 agent 技能](../workflows.md#share-agent-skills) 了解详情以及每个沙盒的退出方式。

本地 stdio MCP 服务器运行在沙盒 VM 之外。如果你注册了一个会启动宿主进程或宿主 Docker 容器的本地 MCP 服务器，该进程或容器使用的是宿主权限和宿主隔离，而非沙盒隔离。请参阅 [MCP 网关](../mcp-gateway.md)。

## 组织级控制

在单个开发者的机器上，安全和策略在本地配置——例如使用 `sbx policy` 设置的网络和文件系统规则。管理员可以将这些控制移到组织级别，使安全、策略和访问在你的每个开发者的沙盒中一致地应用，而不是依赖于本地配置。

有关组织管理员可用的控制，请参阅 [管控](../governance/)。

## 了解更多

- [隔离层](isolation/)：hypervisor、网络、Docker、工作区和凭据隔离如何工作
- [默认安全态势](defaults/)：一个全新的沙盒允许什么、阻止什么
- [凭据](credentials/)：如何提供和管理 API 密钥
- [管控](../governance/)：在本地或跨组织配置网络、文件系统和 MCP 访问控制
