现在我们已经配置好了 CI/CD 流水线，接下来让我们看看如何部署应用程序。Docker 支持将容器部署到 Azure ACI 和 AWS ECS。如果你已经在 Docker Desktop 中启用了 Kubernetes，也可以将应用程序部署到 Kubernetes。

## Docker 与 Azure ACI

Docker Azure 集成功能使开发人员能够在构建云原生应用程序时，使用原生的 Docker 命令在 Azure 容器实例（ACI）中运行应用程序。这种新体验在 Docker Desktop 和 Microsoft Azure 之间提供了紧密集成，允许开发人员使用 Docker CLI 或 VS Code 扩展快速运行应用程序，从而能够从本地开发无缝切换到云部署。

详细操作步骤，请参阅[在 Azure 上部署 Docker 容器](/cloud/aci-integration/)。

## Docker 与 AWS ECS

Docker ECS 集成功能使开发人员能够在构建云原生应用程序时，使用 Docker Compose CLI 中的原生 Docker 命令在 Amazon EC2 容器服务（ECS）中运行应用程序。

Docker 与 Amazon ECS 的集成允许开发人员使用 Docker Compose CLI 通过一条 Docker 命令设置 AWS 上下文，从而能够从本地上下文切换到云上下文，快速轻松地运行应用程序，使用 Compose 文件简化在 Amazon ECS 上的多容器应用程序开发。

详细操作步骤，请参阅[在 ECS 上部署 Docker 容器](/cloud/ecs-integration/)。

## Kubernetes

Docker Desktop 包含一个独立的 Kubernetes 服务器和客户端，以及运行在你机器上的 Docker CLI 集成。启用 Kubernetes 后，你可以在 Kubernetes 上测试你的工作负载。

要启用 Kubernetes：

1. 从 Docker 菜单中选择 **Settings**。
2. 选择 **Kubernetes** 并点击 **Enable Kubernetes**。

    这会在 Docker Desktop 启动时启动一个 Kubernetes 单节点集群。

详细信息，请参阅[在 Kubernetes 上部署](/manuals/desktop/use-desktop/kubernetes.md)和[使用 Kubernetes YAML 描述应用程序](/guides/deployment-orchestration/kube-deploy/#describing-apps-using-kubernetes-yaml)。