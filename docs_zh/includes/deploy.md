现在我们已经配置好了 CI/CD 流水线，接下来让我们看看如何部署应用程序。Docker 支持将容器部署到 Azure ACI 和 AWS ECS。如果你在 Docker Desktop 中启用了 Kubernetes，也可以将应用程序部署到 Kubernetes。

## Docker 和 Azure ACI

Docker Azure 集成允许开发人员在构建云原生应用程序时，使用原生 Docker 命令在 Azure 容器实例（ACI）中运行应用程序。这种新体验提供了 Docker Desktop 与 Microsoft Azure 之间的紧密集成，使开发人员能够快速使用 Docker CLI 或 VS Code 扩展无缝地从本地开发切换到云部署。

详细说明请参见 [在 Azure 上部署 Docker 容器](/cloud/aci-integration/)。

## Docker 和 AWS ECS

Docker ECS 集成允许开发人员在构建云原生应用程序时，使用 Docker Compose CLI 中的原生 Docker 命令在 Amazon EC2 容器服务（ECS）中运行应用程序。

Docker 与 Amazon ECS 之间的集成为开发人员提供了使用 Docker Compose CLI 设置 AWS 上下文的功能，只需一个 Docker 命令即可在本地上下文和云上下文之间切换，从而快速轻松地运行应用程序，简化了使用 Compose 文件在 Amazon ECS 上进行多容器应用程序开发。

详细说明请参见 [在 ECS 上部署 Docker 容器](/cloud/ecs-integration/)。

## Kubernetes

Docker Desktop 包含一个独立的 Kubernetes 服务器和客户端，以及 Docker CLI 集成，可在你的机器上运行。启用 Kubernetes 后，你可以在 Kubernetes 上测试你的工作负载。

启用 Kubernetes 的步骤：

1. 从 Docker 菜单中选择 **Settings**（设置）。
2. 选择 **Kubernetes**（Kubernetes），然后点击 **Enable Kubernetes**（启用 Kubernetes）。

    这将在 Docker Desktop 启动时启动一个 Kubernetes 单节点集群。

详细信息请参见 [在 Kubernetes 上部署](/manuals/desktop/use-desktop/kubernetes.md) 和 [使用 Kubernetes YAML 描述应用程序](/guides/deployment-orchestration/kube-deploy/#describing-apps-using-kubernetes-yaml)。