# 使用默认的 Compose Bridge 转换





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 4.43.0 and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



Compose Bridge 包含一个内置的转换功能，可以自动将您的 Compose 配置转换为一套 Kubernetes 清单文件。

基于您的 `compose.yaml` 文件，它会生成：

- 一个 [Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)，以便所有您的资源都被隔离，不会与其他部署的资源发生冲突。
- 一个 [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)，其中为您的 Compose 应用程序中的每个 [config](/reference/compose-file/configs.md) 资源都包含一个条目。
- 为应用程序服务生成 [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)。这可以确保在 Kubernetes 集群中维护指定数量的应用程序实例。
- 为您的服务暴露的端口生成 [Services](https://kubernetes.io/docs/concepts/services-networking/service/)，用于服务间通信。
- 为您的服务发布的端口生成 [Services](https://kubernetes.io/docs/concepts/services-networking/service/)，其类型为 `LoadBalancer`，以便 Docker Desktop 也在主机上暴露相同的端口。
- [Network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) 用于复制在您的 `compose.yaml` 文件中定义的网络拓扑。
- 为您的卷生成 [PersistentVolumeClaims](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)，使用 `hostpath` 存储类，以便 Docker Desktop 管理卷的创建。
- [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) 包含经过编码的机密信息。这专为测试环境中的本地使用而设计。

它还提供了一个专用于 Docker Desktop 的 Kustomize overlay，其中包含：
 - `Loadbalancer` 用于需要在主机上暴露端口的服务。
 - 一个 `PersistentVolumeClaim`，用于使用 Docker Desktop 的存储供应器 `desktop-storage-provisioner` 来更有效地处理卷的供应。
 - 一个 `Kustomization.yaml` 文件，用于将所有资源链接在一起。

如果您的 Compose 文件为某个服务定义了 `models` 部分，Compose Bridge 会自动配置您的部署，以便您的服务可以通过 Docker Model Runner 定位并使用其模型。

对于每个声明的模型，该转换会注入两个环境变量：

- `<MODELNAME>_URL`：Docker Model Runner 提供该模型的端点
- `<MODELNAME>_MODEL`：模型的名称或标识符

您可以选择使用 `endpoint_var` 和 `model_var` 来自定义这些变量名。

默认转换会生成两种不同的 overlay - 一种用于使用本地 Docker Model Runner 实例的 Docker Desktop，另一种是 `model-runner` overlay，其中包含在 pod 中部署 Docker Model Runner 所需的所有相关 Kubernetes 资源。

| 环境    | Endpoint                                        |
| -------------- | ----------------------------------------------- |
| Docker Desktop | `http://host.docker.internal:12434/engines/v1/` |
| Kubernetes     | `http://model-runner/engines/v1/`               |


更多详情，请参阅 [使用 Model Runner](use-model-runner.md)。

## 使用默认的 Compose Bridge 转换

要使用默认转换转换您的 Compose 文件：

```console
$ docker compose bridge convert
```

Compose 会在当前目录中查找 `compose.yaml` 文件并生成 Kubernetes 清单文件。

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

所有生成的文件都存储在您项目的 `/out` 目录中。

## 部署生成的清单文件

> [!IMPORTANT]
>
> 在部署您的 Compose Bridge 转换之前，请确保您已在 Docker Desktop 中[启用 Kubernetes](/manuals/desktop/settings-and-maintenance/settings.md#kubernetes)。

清单文件生成后，将它们部署到本地 Kubernetes 集群：

```console
$ kubectl apply -k out/overlays/desktop/
```

> [!TIP]
>
> 您可以从 Compose 文件查看器转换并部署您的 Compose 项目到 Kubernetes 集群。
> 
> 请确保您已登录 Docker 账户，在 **容器** 视图中导航到您的容器，然后在右上角选择 **查看配置**，再选择 **转换并部署到 Kubernetes**。 

## 其他命令

转换位于另一个目录中的 `compose.yaml` 文件：

```console
$ docker compose -f <path-to-file>/compose.yaml bridge convert
```

要查看所有可用的标志，请运行：

```console
$ docker compose bridge convert --help
```

## 接下来做什么？

- [探索如何自定义 Compose Bridge](customize.md)
- [使用 Model Runner](use-model-runner.md).
