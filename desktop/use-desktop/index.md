# 探索 Docker Desktop

打开 Docker Desktop 时，会显示 Docker Desktop Dashboard。

![容器视图中的 Docker Desktop Dashboard](../images/dashboard.webp) 

它提供了一个集中式界面，用于管理您的[容器](container.md)、[镜像](images.md)、[卷](volumes.md)、[构建](builds.md)和[Kubernetes 资源](kubernetes.md)。

此外，Docker Desktop Dashboard 还允许您：

- 使用 [Ask Gordon](/manuals/ai/gordon/_index.md)，这是一个嵌入在 Docker Desktop 和 Docker CLI 中的个人 AI 助手。它旨在简化您的工作流程，并帮助您充分利用 Docker 生态系统。
- 导航至 **Settings**（设置）菜单以配置您的 Docker Desktop 设置。在 Dashboard 标题栏中选择 **Settings** 图标。
- 访问 **Troubleshoot**（故障排除）菜单以进行调试和执行重启操作。在 Dashboard 标题栏中选择 **Troubleshoot** 图标。
- 在 **Notifications center**（通知中心）中接收新版本、安装进度更新等通知。在 Docker Desktop Dashboard 的右下角选择铃铛图标以访问通知中心。
- 从 Dashboard 标题栏访问 **Learning center**（学习中心）。它通过快速的应用内导览帮助您入门，并提供其他学习 Docker 的资源。

  有关入门的更详细指南，请参阅[入门](/get-started/introduction/_index.md)。
- 访问 [Docker Hub](/manuals/docker-hub/_index.md) 以搜索、浏览、拉取、运行或查看镜像详情。
- 进入 [Docker Scout](../../scout/_index.md) 仪表板。
- 导航至 [Docker Extensions](/manuals/extensions/_index.md)。

## Docker 终端

从 Docker Dashboard 底部栏，您可以直接在 Docker Desktop 中使用集成终端。

集成终端：

- 如果您导航到 Docker Desktop Dashboard 的另一部分然后返回，会保留您的会话。
- 支持复制、粘贴、搜索和清除会话。

#### 打开集成终端

要打开集成终端，可以：

- 将鼠标悬停在正在运行的容器上，在 **Actions**（操作）列下，选择 **Show container actions**（显示容器操作）菜单。从下拉菜单中，选择 **Open in terminal**（在终端中打开）。
- 或者，选择位于右下角、版本号旁边的 **Terminal**（终端）图标。

要使用外部终端，请导航至 **Settings**（设置）中的 **General**（常规）选项卡，并在 **Choose your terminal**（选择您的终端）下选择 **System default**（系统默认）选项。

## 快速搜索

使用位于 Docker Dashboard 标题栏中的快速搜索（Quick Search）来搜索：

- 本地系统上的任何容器或 Compose 应用程序。您可以查看相关环境变量的概述，或执行快速操作，例如启动、停止或删除。

- 公共 Docker Hub 镜像、本地镜像以及来自远程仓库的镜像（您在 Hub 中所属组织的私有仓库）。根据您选择的镜像类型，您可以按标签拉取镜像、查看文档、转到 Docker Hub 获取更多详情，或使用该镜像运行新容器。

- 扩展。从这里，您可以了解有关该扩展的更多信息，并一键安装。或者，如果您已经安装了扩展，可以直接从搜索结果中打开它。

- 任何卷。从这里您可以查看关联的容器。

- 文档。直接从 Docker Desktop 查找 Docker 官方文档的帮助。

## Docker 菜单

Docker Desktop 还包含一个托盘图标，称为 Docker 菜单 





<img
  loading="lazy"
  src="../../assets/images/whale-x.svg"
  alt="whale menu"
  
  class="inline my-0 not-prose"
/>
，用于快速访问。

在任务栏中选择 





<img
  loading="lazy"
  src="../../assets/images/whale-x.svg"
  alt="whale menu"
  
  class="inline my-0 not-prose"
/>
 图标以打开选项，例如：

- **Dashboard**（仪表板）。这将带您进入 Docker Desktop Dashboard。
- **Sign in/Sign up**（登录/注册）
- **Settings**（设置）
- **Check for updates**（检查更新）
- **Troubleshoot**（故障排除）
- **Give feedback**（提供反馈）
- **Switch to Windows containers**（切换到 Windows 容器）（如果您在 Windows 上）
- **About Docker Desktop**（关于 Docker Desktop）。包含您正在运行的版本信息，以及例如订阅服务协议的链接。
- **Docker Hub**
- **Documentation**（文档）
- **Extensions**（扩展）
- **Kubernetes**
- **Restart**（重启）
- **Quit Docker Desktop**（退出 Docker Desktop）

- [探索 Docker Desktop 中的“容器”视图](https://docs.docker.com/desktop/use-desktop/container/)

- [探索 Docker Desktop 中的 Images 视图](https://docs.docker.com/desktop/use-desktop/images/)

- [在 Docker Desktop 中探索卷视图](https://docs.docker.com/desktop/use-desktop/volumes/)

- [探索 Docker Desktop 中的构建视图](https://docs.docker.com/desktop/use-desktop/builds/)

- [探索 Kubernetes 视图](https://docs.docker.com/desktop/use-desktop/kubernetes/)

- [Docker Desktop 的资源节省模式](https://docs.docker.com/desktop/use-desktop/resource-saver/)

- [暂停 Docker Desktop](https://docs.docker.com/desktop/use-desktop/pause/)

