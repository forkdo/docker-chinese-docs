# 关于 Docker Offload




Docker Offload 是一项完全托管的服务，用于使用您已熟悉的 Docker 工具（包括 Docker Desktop、Docker CLI 和 Docker Compose）在云端构建和运行容器。它将您的本地开发工作流扩展到可扩展的、由云驱动的环境中，使开发者即使在虚拟桌面基础设施 (VDI) 环境或不支持嵌套虚拟化的系统中也能高效工作。

## 主要功能

Docker Offload 包含以下功能，以支持现代容器工作流：

- 临时云运行器：为每个容器会话自动配置和拆除云环境。
- 安全通信：使用 Docker Desktop 与云环境之间的加密隧道，并支持安全的 secrets 和镜像拉取。
- 端口转发和绑定挂载：即使在云端运行容器，也能保留本地开发体验。
- VDI 友好：在虚拟桌面环境或不支持嵌套虚拟化的系统中[使用 Docker Desktop](../desktop/setup/vm-vdi.md)。

有关更多信息，请参阅 [Docker Offload 产品页](https://www.docker.com/products/docker-offload/)。

## Docker Offload 工作原理

Docker Offload 通过将 Docker Desktop 连接到安全、专用的云资源，取代了在本地构建或运行容器的需求。

### 使用 Docker Offload 运行容器

当您使用 Docker Offload 构建或运行容器时，Docker Desktop 会创建一条安全的 SSH 隧道连接到在云端运行的 Docker 守护进程。您的容器完全在该远程环境中启动和管理。

过程如下：

1. Docker Desktop 连接到云端并触发容器创建。
2. Docker Offload 构建或拉取所需的镜像，并在云端启动容器。
3. 连接在容器运行且您保持活跃状态期间保持打开状态。
4. 当容器停止运行时，环境会自动关闭并清理。

这种设置避免了在本地运行容器的开销，即使在低性能机器（包括不支持嵌套虚拟化的机器）上也能实现快速、可靠的容器运行。这使得 Docker Offload 成为使用虚拟桌面、云托管开发机器或旧硬件等环境的开发者的理想选择。

尽管是远程运行，绑定挂载和端口转发等功能仍能无缝工作，在 Docker Desktop 和 CLI 中提供类似本地的体验。

### 云资源

Docker Offload 使用的云主机具有 4 个 vCPU 和 8 GiB 内存。如果您有不同需求，<a href="https://www.docker.com/pricing/contact-sales/" id="dkr_docs_cs_offload_about" class="link" rel="noopener">请联系 Docker</a> 了解可选项。

### 会话管理与空闲状态

Docker Offload 使用会话管理和空闲状态策略，以确保跨所有用户的云资源公平使用，请参阅[公平使用](#fair-use)。

每个用户一次只能运行一个 Docker Offload 会话。当 Docker Desktop 处于 **Offload 空闲** 状态时，它会等待 Docker API 上的活动，并且仅在需要时才会连接到云环境。一旦连接，会话将转入 **Offload 运行中** 状态，并在 Docker 检测到活动期间保持连接。活动包括任何 Docker API 调用、正在运行的容器或正在进行的构建。

#### 何时会出现提示

Docker Offload 运行期间，Docker Desktop 会在仪表板中显示提示，以确认您是否仍处于活跃状态。提示在两种情况下出现：

1. 超过 3 分钟未检测到活动。
2. 会话已运行很长时间。

当提示出现时，您可以：
   - 选择 **稍后再提醒我** 以确认您仍处于活跃状态并继续您的会话。
   - 选择 **现在空闲** 以立即返回空闲状态。
   - 不执行任何操作，会话将自动返回空闲状态。

#### 会话进入空闲状态后会发生什么

在您的会话返回空闲状态后，会有 5 分钟的宽限期。在此期间，您可以通过运行任何 Docker 命令来恢复会话。

> [!IMPORTANT]
> 如果空闲时间超过 5 分钟且没有活动，会话将被终止。Docker Offload 环境是临时的，因此远程环境及其中的任何容器、镜像或卷都会被删除。要在会话之间保留工作，请在会话结束前将镜像推送到 [Docker Hub](/docker-hub/) 等注册表。

#### 长会话提示

长会话提示会在会话期间每 3 小时出现一次。在一天内累计使用达到 8 小时后，提示会每小时出现一次。8 小时计数器在每天开始时重置。

## 公平使用

Docker Offload 强制执行公平使用策略，以防止资源滥用。公平使用定义为每个命名用户每天最多 8 个计算小时，在所有用户会话中累计计算。超出此阈值的使用可能会根据 Docker 的判断受到会话管理。

## 下一步

通过 [Docker Offload 快速入门](/offload/quickstart/)开始动手实践 Docker Offload。

