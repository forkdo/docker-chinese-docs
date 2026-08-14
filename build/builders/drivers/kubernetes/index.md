# Kubernetes 驱动


Kubernetes 驱动让你可以将本地开发或 CI 环境连接到 Kubernetes 集群中的 builder，从而获得更强大的计算资源，还可以选择使用多个原生架构。

## 概要（Synopsis）

运行以下命令来创建一个名为 `kube`、使用 Kubernetes 驱动的新 builder：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=[key=value,...]
```

下表描述了你可以传递给 `--driver-opt` 的可用驱动专属选项：

| Parameter                                  | Type         | Default                                 | Description                                                                                                                                                                                                   |
| ------------------------------------------ | ------------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image`                                    | String       |                                         | 设置用于运行 BuildKit 的镜像。                                                                                                                                                                                 |
| `namespace`                                | String       | 当前 Kubernetes 上下文中的命名空间       | 设置 Kubernetes 命名空间。                                                                                                                                                                                     |
| `default-load`                             | Boolean      | `false`                                 | 自动将镜像加载到 Docker Engine 镜像存储。                                                                                                                                                                      |
| `replicas`                                 | Integer      | 1                                       | 设置要创建的 Pod 副本数。参见 [scaling BuildKit][1]                                                                                                                                                           |
| `requests.cpu`                             | CPU units    |                                         | 设置以 Kubernetes CPU 单位指定的请求 CPU 值。例如 `requests.cpu=100m` 或 `requests.cpu=2`                                                                                                                     |
| `requests.memory`                          | Memory size  |                                         | 设置以字节或有效后缀指定的请求内存值。例如 `requests.memory=500Mi` 或 `requests.memory=4G`                                                                                                                   |
| `requests.ephemeral-storage`               | Storage size |                                         | 设置以字节或有效后缀指定的请求临时存储值。例如 `requests.ephemeral-storage=2Gi`                                                                                                                              |
| `persistent-volume-claim.requests.storage` | Storage size |                                         | 设置对持久卷声明（persistent volume claim）的请求大小。设置后，Buildx 会创建一个 `StatefulSet` 并将 BuildKit 构建缓存存储在该声明中。例如 `persistent-volume-claim.requests.storage=20Gi`                |
| `limits.cpu`                               | CPU units    |                                         | 设置以 Kubernetes CPU 单位指定的限制 CPU 值。例如 `requests.cpu=100m` 或 `requests.cpu=2`                                                                                                                    |
| `limits.memory`                            | Memory size  |                                         | 设置以字节或有效后缀指定的限制内存值。例如 `requests.memory=500Mi` 或 `requests.memory=4G`                                                                                                                   |
| `limits.ephemeral-storage`                 | Storage size |                                         | 设置以字节或有效后缀指定的限制临时存储值。例如 `requests.ephemeral-storage=100M`                                                                                                                             |
| `buildkit-root-volume-memory`              | Memory size  | 使用常规文件系统                        | 将 `/var/lib/buildkit` 挂载到由 `emptyDir` 提供支持的内存卷上，并将 `SizeLimit` 作为值。例如 `buildkit-root-folder-memory=6G`                                                                               |
| `nodeselector`                             | CSV string   |                                         | 设置 Pod 的 `nodeSelector` 标签。参见 [node assignment][2]。                                                                                                                                                  |
| `annotations`                              | CSV string   |                                         | 在 `Deployment` 或 `StatefulSet` 以及 Pod 上设置额外的注解。                                                                                                                                                  |
| `labels`                                   | CSV string   |                                         | 在 `Deployment` 或 `StatefulSet` 以及 Pod 上设置额外的标签。                                                                                                                                                  |
| `tolerations`                              | CSV string   |                                         | 配置 Pod 的污点容忍（taint toleration）。参见 [node assignment][2]。                                                                                                                                         |
| `serviceaccount`                           | String       |                                         | 设置 Pod 的 `serviceAccountName`。                                                                                                                                                                            |
| `schedulername`                            | String       |                                         | 设置负责调度该 Pod 的调度器。                                                                                                                                                                                 |
| `timeout`                                  | Time         | `120s`                                  | 设置在构建前 Buildx 等待 Pod 就绪的超时限制。                                                                                                                                                                 |
| `rootless`                                 | Boolean      | `false`                                 | 以非 root 用户运行容器。参见 [rootless mode][3]。                                                                                                                                                             |
| `loadbalance`                              | String       | `sticky`                                | 负载均衡策略（`sticky` 或 `random`）。如果设置为 `sticky`，则使用上下文路径的哈希值选择 Pod。                                                                                                                |
| `qemu.install`                             | Boolean      | `false`                                 | 安装 QEMU 仿真以支持多平台。参见 [QEMU][4]。                                                                                                                                                                  |
| `qemu.image`                               | String       | `tonistiigi/binfmt:latest`              | 设置 QEMU 仿真镜像。参见 [QEMU][4]。                                                                                                                                                                          |

[1]: #scaling-buildkit
[2]: #node-assignment
[3]: #rootless-mode
[4]: #qemu

## 扩展 BuildKit（Scaling BuildKit）

Kubernetes 驱动的主要优势之一是你可以扩展 builder 副本的数量，以应对增加的构建负载。扩展可通过以下驱动选项配置：

- `replicas=N`

  这会将 BuildKit Pod 的数量扩展到所需大小。默认情况下，它只创建一个 Pod。增加副本数让你可以利用集群中的多个节点。

- `requests.cpu`、`requests.memory`、`requests.ephemeral-storage`、`limits.cpu`、`limits.memory`、`limits.ephemeral-storage`

  这些选项允许根据[官方 Kubernetes 文档](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)来请求和限制每个 BuildKit Pod 可用的资源。

例如，要创建 4 个副本的 BuildKit Pod：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,replicas=4
```

列出 Pod，你会看到：

```console
$ kubectl -n buildkit get deployments
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
kube0   4/4     4            4           8s

$ kubectl -n buildkit get pods
NAME                     READY   STATUS    RESTARTS   AGE
kube0-6977cdcb75-48ld2   1/1     Running   0          8s
kube0-6977cdcb75-rkc6b   1/1     Running   0          8s
kube0-6977cdcb75-vb4ks   1/1     Running   0          8s
kube0-6977cdcb75-z4fzs   1/1     Running   0          8s
```

此外，你可以使用 `loadbalance=(sticky|random)` 选项来控制存在多个副本时的负载均衡行为。`random` 从节点池中随机选择节点，从而在副本之间实现均匀的工作负载分布。`sticky`（默认）会尝试将多次执行的同一构建每次都连接到同一个节点，从而更好地利用本地缓存。

有关可扩展性的更多信息，请参阅
[`docker buildx create`](/reference/cli/docker/buildx/create/#driver-opt) 的选项。

## 持久化存储（Persistent storage）

设置 `persistent-volume-claim.requests.storage` 驱动选项，可以将 BuildKit 构建缓存存储到持久卷声明中，而不是 Pod 的文件系统。当你设置此选项时，Buildx 会创建一个 `StatefulSet` 而非 `Deployment`。

如果你同时设置了 `replicas`，每个副本都会获得自己的持久卷声明。这会在各次重启之间将构建缓存保留在每个 Pod 本地。

例如，要为每个副本创建具有 20 GiB 持久化存储的 builder：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,replicas=4,persistent-volume-claim.requests.storage=20Gi
```

## 节点分配（Node assignment）

Kubernetes 驱动允许你使用 `nodeSelector` 和 `tolerations` 驱动选项来控制 BuildKit Pod 的调度。
如果你希望完全使用自定义调度器，还可以设置 `schedulername` 选项。

你可以使用 `annotations` 和 `labels` 驱动选项，将额外的元数据应用到托管你的 builder 的 `Deployment` 或 `StatefulSet` 以及 Pod 上。

`nodeSelector` 参数的值是一个以逗号分隔的键值对字符串，其中键是节点标签，值是标签文本。例如：`"nodeselector=kubernetes.io/arch=arm64"`

`tolerations` 参数是一个以分号分隔的污点（taint）列表。它接受与 Kubernetes manifest 相同的值。每个 `tolerations` 条目指定一个污点键以及值、运算符或效果。例如：
`"tolerations=key=foo,value=bar;key=foo2,operator=exists;key=foo3,effect=NoSchedule"`

这些选项接受以 CSV 分隔的字符串作为值。由于 shell 命令的引号规则，你必须用单引号将值包裹起来。你甚至可以将整个 `--driver-opt` 用单引号包裹，例如：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  '--driver-opt="nodeselector=label1=value1,label2=value2","tolerations=key=key1,value=value1"'
```

## 多平台构建（Multi-platform builds）

Kubernetes 驱动支持创建[多平台镜像](/manuals/build/building/multi-platform.md)，
既可以使用 QEMU，也可以利用节点的原生架构。

### QEMU

与 `docker-container` 驱动一样，Kubernetes 驱动也支持使用
[QEMU](https://www.qemu.org/)（用户模式）来构建非原生平台的镜像。包含 `--platform` 标志并指定要输出的平台。

例如，要为 `amd64` 和 `arm64` 构建一个 Linux 镜像：

```console
$ docker buildx build \
  --builder=kube \
  --platform=linux/amd64,linux/arm64 \
  -t <user>/<image> \
  --push .
```

> [!WARNING]
>
> QEMU 对非原生平台执行完整的 CPU 仿真，比原生构建慢得多。计算密集型任务（如编译和压缩/解压缩）可能会遭受较大的性能损失。

在构建中使用自定义 BuildKit 镜像或调用非原生二进制文件，可能需要你在创建 builder 时通过 `qemu.install` 选项显式开启 QEMU：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,qemu.install=true
```

### 原生（Native）

如果你可以访问不同架构的集群节点，Kubernetes 驱动可以利用这些节点进行原生构建。为此，请使用 `docker buildx create` 的 `--append` 标志。

首先，创建一个明确支持单一架构（例如 `amd64`）的 builder：

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --platform=linux/amd64 \
  --node=builder-amd64 \
  --driver-opt=namespace=buildkit,nodeselector="kubernetes.io/arch=amd64"
```

这会创建一个名为 `kube` 的 Buildx builder，其中包含一个名为 `builder-amd64` 的构建节点。使用 `--node` 分配节点名称是可选的。如果你不提供，Buildx 会生成随机的节点名称。

请注意，这里 Buildx 的节点概念与 Kubernetes 的节点概念不同。在这种情况下，一个 Buildx 节点可以将多个相同架构的 Kubernetes 节点连接在一起。

创建了 `kube` builder 后，你现在可以使用 `--append` 引入另一种架构。例如，要添加 `arm64`：

```console
$ docker buildx create \
  --append \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --platform=linux/arm64 \
  --node=builder-arm64 \
  --driver-opt=namespace=buildkit,nodeselector="kubernetes.io/arch=arm64"
```

列出你的 builder 会显示 `kube` builder 的两个节点：

```console
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT                                         STATUS   PLATFORMS
kube            kubernetes
  builder-amd64 kubernetes:///kube?deployment=builder-amd64&kubeconfig= running  linux/amd64*, linux/amd64/v2, linux/amd64/v3, linux/386
  builder-arm64 kubernetes:///kube?deployment=builder-arm64&kubeconfig= running  linux/arm64*
```

你现在可以通过在构建命令中一起指定这些平台，来构建多架构的 `amd64` 和 `arm64` 镜像：

```console
$ docker buildx build --builder=kube --platform=linux/amd64,linux/arm64 -t <user>/<image> --push .
```

你可以根据需要，重复执行 `buildx create --append` 命令来支持任意多种架构。

## Rootless 模式（Rootless mode）

Kubernetes 驱动支持 rootless 模式。有关 rootless 模式的工作原理及其要求的更多信息，请参阅
[Rootless Buildkit 文档](https://github.com/moby/buildkit/blob/master/docs/rootless.md)。

要在你的集群中开启它，可以使用 `rootless=true` 驱动选项：

```console
$ docker buildx create \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,rootless=true
```

这将创建不带 `securityContext.privileged` 的 Pod。

需要 Kubernetes 1.19 或更高版本。建议使用 Ubuntu 作为主机内核。

## 示例：在 Kubernetes 中创建 Buildx builder（Example: Creating a Buildx builder in Kubernetes）

本指南展示了如何：

- 为你的 Buildx 资源创建一个命名空间
- 创建一个 Kubernetes builder
- 列出可用的 builder
- 使用你的 Kubernetes builder 构建一个镜像

先决条件：

- 你已有一个现成的 Kubernetes 集群。如果你还没有，可以通过安装
  [minikube](https://minikube.sigs.k8s.io/docs/) 来跟随操作。
- 你要连接的集群可以通过 `kubectl` 命令访问，并且在必要时已适当设置
  [`KUBECONFIG` 环境变量](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/#set-the-kubeconfig-environment-variable)。

1. 创建一个 `buildkit` 命名空间。

   创建一个独立的命名空间有助于将你的 Buildx 资源与集群中的其他资源分开。

   ```console
   $ kubectl create namespace buildkit
   namespace/buildkit created
   ```

2. 使用 Kubernetes 驱动创建一个新 builder：

   ```console
   $ docker buildx create \
     --bootstrap \
     --name=kube \
     --driver=kubernetes \
     --driver-opt=namespace=buildkit
   ```

   > [!NOTE]
   >
   > 记得在驱动选项中指定命名空间。

3. 使用 `docker buildx ls` 列出可用的 builder

   ```console
   $ docker buildx ls
   NAME/NODE                DRIVER/ENDPOINT STATUS  PLATFORMS
   kube                     kubernetes
     kube0-6977cdcb75-k9h9m                 running linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
   default *                docker
     default                default         running linux/amd64, linux/386
   ```

4. 使用 `kubectl` 检查由构建驱动创建的正在运行的 Pod。

   ```console
   $ kubectl -n buildkit get deployments
   NAME    READY   UP-TO-DATE   AVAILABLE   AGE
   kube0   1/1     1            1           32s

   $ kubectl -n buildkit get pods
   NAME                     READY   STATUS    RESTARTS   AGE
   kube0-6977cdcb75-k9h9m   1/1     Running   0          32s
   ```

   构建驱动会在指定命名空间（本例中为 `buildkit`）中创建必要的资源，同时将你的驱动配置保留在本地。

5. 在运行 buildx 命令时包含 `--builder` 标志来使用你的新 builder。例如： ：

   ```console
   # Replace <registry> with your Docker username
   # and <image> with the name of the image you want to build
   docker buildx build \
     --builder=kube \
     -t <registry>/<image> \
     --push .
   ```

就这样：你现在使用 Buildx 从一个 Kubernetes Pod 构建了一个镜像。

## 延伸阅读（Further reading）

有关 Kubernetes 驱动的更多信息，请参阅
[buildx 参考](/reference/cli/docker/buildx/create/#driver)。

