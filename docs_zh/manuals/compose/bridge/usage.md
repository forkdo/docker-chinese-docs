---
title: 使用默认的 Compose Bridge 转换
linkTitle: 使用方法
weight: 10
description: 了解如何使用默认的 Compose Bridge 转换将 Compose 文件转换为 Kubernetes 清单
keywords: docker compose bridge, compose kubernetes transform, kubernetes from compose, compose bridge convert, compose.yaml to kubernetes
---

{{< summary-bar feature_name="Compose bridge" >}}

Compose Bridge 包含一个内置转换器，可自动将您的 Compose 配置转换为一组 Kubernetes 清单。

根据您的 `compose.yaml` 文件，它会生成：

- 一个 [Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)，确保所有资源相互隔离，不会与其他部署的资源冲突。
- 一个 [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)，其中包含 Compose 应用中每个 [config](/reference/compose-file/configs.md) 资源的条目。
- 应用服务的 [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)，确保在 Kubernetes 集群中维持指定数量的应用实例。
- 服务暴露端口的 [Services](https://kubernetes.io/docs/concepts/services-networking/service/)，用于服务间通信。
- 服务发布端口的 [Services](https://kubernetes.io/docs/concepts/services-networking/service/)，类型为 `LoadBalancer`，因此 Docker Desktop 也会在主机上暴露相同端口。
- [Network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)，以复制 `compose.yaml` 文件中定义的网络拓扑。
- 卷的 [PersistentVolumeClaims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)，使用 `hostpath` 存储类，由 Docker Desktop 管理卷的创建。
- [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)，包含您的加密密钥。专为测试环境的本地使用而设计。

它还提供了一个专用于 Docker Desktop 的 Kustomize 叠加层，包含：
 - 需要在主机上暴露端口的服务的 `Loadbalancer`。
 - 一个 `PersistentVolumeClaim`，使用 Docker Desktop 存储供应器 `desktop-storage-provisioner` 更有效地处理卷供应。
 - 一个 `Kustomization.yaml` 文件，将所有资源关联在一起。

如果您的 Compose 文件为服务定义了 `models` 部分，Compose Bridge 会自动配置您的部署，使服务能够通过 Docker Model Runner 定位和使用其模型。

对于每个声明的模型，转换器注入两个环境变量：

- `<MODELNAME>_URL`：Docker Model Runner 提供该模型的端点
- `<MODELNAME>_MODEL`：模型的名称或标识符

您可以选择使用 `endpoint_var` 和 `model_var` 自定义这些变量名。

默认转换生成两种不同的叠加层 - 一种用于在使用本地 Docker Model Runner 实例时的 Docker Desktop，另一种是 `model-runner` 叠加层，包含在 Pod 中部署 Docker Model Runner 的所有相关 Kubernetes 资源。

| 环境 | 端点 |
| -------------- | ----------------------------------------------- |
| Docker Desktop | `http://host.docker.internal:12434/engines/v1/` |
| Kubernetes | `http://model-runner/engines/v1/` |

更多详情，请参阅 [使用 Model Runner](use-model-runner.md)。

## 使用默认的 Compose Bridge 转换

要使用默认转换转换您的 Compose 文件：

```console
$ docker compose bridge convert
```

Compose 在当前目录中查找 `compose.yaml` 文件并生成 Kubernetes 清单。

示例输出：

```console
$ docker compose -f compose.yaml bridge convert
Kubernetes resource backend-deployment.yaml created
Kubernetes resource frontend-deployment.yaml created
Kubernetes resource backend-expose.yaml created
Kubernetes resource frontend-expose.yaml created
Kubernetes resource 0-my-project-namespace.yaml created
Kubernetes resource default-network-policy.yaml created
Kubernetes resource backend-service.yaml created
Kubernetes resource frontend-service.yaml created
Kubernetes resource kustomization.yaml created
Kubernetes resource backend-deployment.yaml created
Kubernetes resource frontend-deployment.yaml created
Kubernetes resource backend-service.yaml created
Kubernetes resource frontend-service.yaml created
Kubernetes resource kustomization.yaml created
Kubernetes resource model-runner-configmap.yaml created
Kubernetes resource model-runner-deployment.yaml created
Kubernetes resource model-runner-service.yaml created
Kubernetes resource model-runner-volume-claim.yaml created
Kubernetes resource kustomization.yaml created
```

所有生成的文件都存储在项目中的 `/out` 目录中。

## 部署生成的清单

> [!IMPORTANT]
>
> 在部署 Compose Bridge 转换之前，请确保您已在 Docker Desktop 中[启用 Kubernetes](/manuals/desktop/settings-and-maintenance/settings.md#kubernetes)。

清单生成后，将它们部署到您的本地 Kubernetes 集群：

```console
$ kubectl apply -k out/overlays/desktop/
```

> [!TIP]
>
> 您可以从 Compose 文件查看器中将 Compose Bridge 转换并部署到 Kubernetes 集群。
> 
> 确保您已登录 Docker 账户，在 **Containers** 视图中导航到您的容器，然后在右上角选择 **View configurations**，再选择 **Convert and Deploy to Kubernetes**。

## 其他命令

转换位于其他目录中的 `compose.yaml` 文件：

```console
$ docker compose -f <path-to-file>/compose.yaml bridge convert
```

要查看所有可用标志，请运行：

```console
$ docker compose bridge convert --help
```

## 接下来是什么？

- [探索如何自定义 Compose Bridge](customize.md)
- [使用 Model Runner](use-model-runner.md)