# 探索 Kubernetes 视图

Docker Desktop 包含一个独立的 Kubernetes 服务器和客户端，以及 Docker CLI 集成，使您能够直接在您的机器上进行本地 Kubernetes 开发和测试。

Kubernetes 服务器作为单节点或多节点集群，在 Docker 容器内运行。这个轻量级的设置帮助您探索 Kubernetes 功能、测试工作负载，并与其他 Docker 功能并行地进行容器编排。

## 启用 Kubernetes

在 Docker Desktop 4.51 及更高版本中，您可以直接从 Docker Desktop 仪表板的 **Kubernetes** 视图中管理 Kubernetes。

1.  打开 Docker Desktop 仪表板并选择 **Kubernetes** 视图。
2.  选择 **Create cluster**。
3.  选择您的集群类型：
    - **Kubeadm** 创建一个单节点集群，版本由 Docker Desktop 设置。
    - **kind** 创建一个多节点集群，您可以设置版本和节点数量。
    有关每种集群类型的更多详细信息，请参阅 [集群置备方法](#cluster-provisioning-method)。
4.  可选：选择 **Show system containers (advanced)** 以在使用 Docker 命令时查看内部容器。
5.  选择 **Create**。

这会设置运行 Kubernetes 服务器所需的镜像，并在您的系统上安装 `kubectl` 命令行工具，位置在 `/usr/local/bin/kubectl` (Mac) 或 `C:\Program Files\Docker\Docker\resources\bin\kubectl.exe` (Windows)。如果您使用 Homebrew 或其他方法安装了 `kubectl` 并遇到冲突，请移除 `/usr/local/bin/kubectl`。

   > [!NOTE]
   >
   > 适用于 Linux 的 Docker Desktop 默认不包含 `kubectl`。您可以按照 [Kubernetes 安装指南](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) 单独安装它。确保 `kubectl` 二进制文件安装在 `/usr/local/bin/kubectl`。

以下操作也会在 Docker Desktop 后端和虚拟机中触发：

- 生成证书和集群配置
- 下载和安装 Kubernetes 内部组件
- 集群启动
- 安装用于网络和存储的额外控制器

当 Kubernetes 启用后，其状态会显示在 Docker Desktop 仪表板的页脚和 Docker 菜单中。

您可以使用以下命令检查您正在使用的 Kubernetes 版本：

```console
$ kubectl version
```

### 集群置备方法

Docker Desktop Kubernetes 可以使用 `kubeadm` 或 `kind`
置备程序进行置备。

`kubeadm` 是较旧的置备程序。它支持单节点集群，您无法选择 kubernetes
版本，它的置备速度比 `kind` 慢，并且不受 [增强容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/index.md) (ECI)
的支持，这意味着如果启用了 ECI，集群可以工作但不受 ECI 保护。

`kind` 是较新的置备程序。它支持多节点集群（为了
更真实的 Kubernetes 设置），您可以选择 Kubernetes 版本，它的
置备速度比 `kubeadm` 快，并且受 ECI 支持——当 ECI
启用时，Kubernetes 集群在非特权 Docker 容器中运行，因此
更加安全。

| 功能 | `kubeadm` | `kind` |
| :------ | :-----: | :--: |
| 多节点集群支持 | 否 | 是 |
| Kubernetes 版本选择器 | 否 | 是 |
| 置备速度 | ~1 分钟 | ~30 秒 |
| ECI 支持 | 否 | 是 |
| 与 containerd 镜像存储协同工作 | 是 | 是 |
| 与 Docker 镜像存储协同工作 | 是 | 否 |

## 仪表板视图

当启用 Kubernetes 集群时，**Kubernetes** 视图会显示一个实时仪表板，其中包含：

- 顶部的命名空间选择器
- 所选命名空间中资源的实时列表 - pods、services、deployments
- 资源被创建、删除或修改时自动更新

## 验证安装

确认您的集群正在运行：

```console
$ kubectl get nodes
NAME                 STATUS    ROLES            AGE       VERSION
docker-desktop       Ready     control-plane    3h        v1.29.1
```

如果 kubectl 指向另一个环境，请切换到 Docker Desktop 上下文：

```console
$ kubectl config use-context docker-desktop
```

>[!TIP]
>
> 如果没有出现任何上下文，请尝试：
>
> - 在命令提示符或 PowerShell 中运行该命令。
> - 将 `KUBECONFIG` 环境变量设置为指向您的 `.kube/config` 文件。

有关 `kubectl` 的更多信息，请参阅
[`kubectl` 文档](https://kubernetes.io/docs/reference/kubectl/overview/)。

## 编辑或停止您的集群

当 Kubernetes 启用时：

- 选择 **Edit cluster** 以修改配置。例如，在 **kubeadm** 和 **kind** 之间切换，或更改节点数量。
- 选择 **Stop** 以禁用集群。会显示进度，并且 **Kubernetes** 视图将返回到 **Create cluster** 屏幕。这会停止并移除 Kubernetes 容器，同时也会移除 `/usr/local/bin/kubectl` 命令。

## 升级您的集群

Kubernetes 集群不会随着 Docker Desktop 的更新而自动升级。要升级集群，您必须在 **Kubernetes** 设置中手动选择 **Reset cluster**。

## 为 Kubernetes 控制平面镜像配置自定义镜像仓库

Docker Desktop 使用容器来运行 Kubernetes 控制平面。默认情况下，Docker Desktop
从 Docker Hub 拉取关联的容器镜像。拉取的镜像取决于[集群置备模式](#cluster-provisioning-method)。

例如，在 `kind` 模式下，它需要以下镜像：

```console
docker.io/kindest/node:<tag>
docker.io/envoyproxy/envoy:<tag>
docker.io/docker/desktop-cloud-provider-kind:<tag>
docker.io/docker/desktop-containerd-registry-mirror:<tag>
```

在 `kubeadm` 模式下，它需要以下镜像：

```console
docker.io/registry.k8s.io/kube-controller-manager:<tag>
docker.io/registry.k8s.io/kube-apiserver:<tag>
docker.io/registry.k8s.io/kube-scheduler:<tag>
docker.io/registry.k8s.io/kube-proxy
docker.io/registry.k8s.io/etcd:<tag>
docker.io/registry.k8s.io/pause:<tag>
docker.io/registry.k8s.io/coredns/coredns:<tag>
docker.io/docker/desktop-storage-provisioner:<tag>
docker.io/docker/desktop-vpnkit-controller:<tag>
docker.io/docker/desktop-kubernetes:<tag>
```

镜像标签由 Docker Desktop 根据多个因素自动选择，包括所使用的 Kubernetes 版本。每个镜像的标签各不相同，并且可能在 Docker Desktop 版本之间发生变化。请关注 Docker Desktop 的发布说明以保持信息同步。

为了适应不允许访问 Docker Hub 的场景，管理员可以
使用 [KubernetesImagesRepository](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md#kubernetes) 设置将 Docker Desktop 配置为从不同的仓库（例如，镜像仓库）
拉取上述列出的镜像，如下所示。

一个镜像名称可以被分解为 `[registry[:port]/][namespace/]repository[:tag]` 组件。
`KubernetesImagesRepository` 设置允许用户覆盖镜像名称中的 `[registry[:port]/][namespace]`
部分。

例如，如果 Docker Desktop Kubernetes 配置为 `kind` 模式，并且
`KubernetesImagesRepository` 设置为 `my-registry:5000/kind-images`，那么
Docker Desktop 将从以下位置拉取镜像：

```console
my-registry:5000/kind-images/node:<tag>
my-registry:5000/kind-images/envoy:<tag>
my-registry:5000/kind-images/desktop-cloud-provider-kind:<tag>
my-registry:5000/kind-images/desktop-containerd-registry-mirror:<tag>
```

这些镜像应该从 Docker Hub 中各自的镜像进行克隆/镜像。标签也必须与 Docker Desktop 期望的一致。

设置此功能的推荐方法如下：

1.  使用所需的集群置备方法启动 Kubernetes：`kubeadm` 或 `kind`。
2.  Kubernetes 启动后，使用 `docker ps` 查看 Docker Desktop 用于 Kubernetes 控制平面的容器镜像。
3.  将这些镜像（连同匹配的标签）克隆或镜像到您的自定义仓库。
4.  停止 Kubernetes 集群。
5.  配置 `KubernetesImagesRepository` 设置以指向您的自定义仓库。
6.  重启 Docker Desktop。
7.  使用 `docker ps` 命令验证 Kubernetes 集群是否正在使用自定义仓库的镜像。

> [!NOTE]
>
> `KubernetesImagesRepository` 设置仅适用于 Docker Desktop 用于设置 Kubernetes 集群的控制平面镜像。它对其他 Kubernetes pods 没有影响。

> [!NOTE]
>
> 在 Docker Desktop 4.43 或更早版本中，当使用 `KubernetesImagesRepository` 并启用 [增强容器隔离 (ECI)](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)
> 时，请将以下镜像添加到 [ECI Docker socket 挂载镜像列表](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md#enhanced-container-isolation)：
>
> `[imagesRepository]/desktop-cloud-provider-kind:`
> `[imagesRepository]/desktop-containerd-registry-mirror:`
>
> 这些容器挂载了 Docker socket，因此您必须将这些镜像添加到 ECI 镜像列表中。否则，
> ECI 将阻止挂载，Kubernetes 将无法启动。

## 故障排除

- 如果 Kubernetes 无法启动，请确保 Docker Desktop 在分配了足够资源的情况下运行。检查 **Settings** > **Resources**。
- 如果 `kubectl` 命令返回错误，请确认上下文已设置为 `docker-desktop`
   ```console
   $ kubectl config use-context docker-desktop
   ```
   然后，如果您启用了该设置，可以尝试检查 Kubernetes 系统容器的日志。
- 如果在更新后遇到集群问题，请重置您的 Kubernetes 集群。重置 Kubernetes 集群可以通过将集群恢复到干净状态来帮助解决问题，从而清除可能导致问题的错误配置、损坏的数据或卡住的资源。如果问题仍然存在，您可能需要清理和清除数据，然后重启 Docker Desktop。
