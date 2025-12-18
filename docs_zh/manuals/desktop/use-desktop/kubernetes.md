---
description: 了解如何在 Docker Desktop 上部署到 Kubernetes
keywords: 部署, kubernetes, kubectl, 编排, Docker Desktop
title: 探索 Kubernetes 视图
linkTitle: Kubernetes
aliases:
- /docker-for-windows/kubernetes/
- /docker-for-mac/kubernetes/
- /desktop/kubernetes/
- /desktop/features/kubernetes/
weight: 50
---

Docker Desktop 包含一个独立的 Kubernetes 服务器和客户端，以及 Docker CLI 集成，使您可以直接在本地机器上进行 Kubernetes 开发和测试。

Kubernetes 服务器作为单节点或多节点集群在 Docker 容器内运行。这种轻量级设置帮助您探索 Kubernetes 功能、测试工作负载，并与其他 Docker 功能并行使用容器编排。

## 启用 Kubernetes

使用 Docker Desktop 4.51 及更高版本，您可以直接从 Docker Desktop Dashboard 的 **Kubernetes** 视图管理 Kubernetes。

1. 打开 Docker Desktop Dashboard，选择 **Kubernetes** 视图。
2. 选择 **Create cluster**（创建集群）。
3. 选择集群类型：
   - **Kubeadm** 创建单节点集群，版本由 Docker Desktop 设置。
   - **kind** 创建多节点集群，您可以设置版本和节点数量。
   有关每种集群类型的详细信息，请参阅 [集群供应方法](#cluster-provisioning-method)。
4. 可选：选择 **Show system containers (advanced)**（显示系统容器（高级））以在使用 Docker 命令时查看内部容器。
5. 选择 **Create**（创建）。

这将设置 Kubernetes 服务器作为容器运行所需的镜像，并在您的系统上安装 `kubectl` 命令行工具，位置为 `/usr/local/bin/kubectl`（Mac）或 `C:\Program Files\Docker\Docker\resources\bin\kubectl.exe`（Windows）。如果您使用 Homebrew 或其他方法安装了 `kubectl` 并遇到冲突，请删除 `/usr/local/bin/kubectl`。

   > [!NOTE]
   >
   > Docker Desktop for Linux 默认不包含 `kubectl`。您可以按照 [Kubernetes 安装指南](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) 单独安装。确保 `kubectl` 二进制文件安装在 `/usr/local/bin/kubectl`。

启用 Kubernetes 后，Docker Desktop Dashboard 底部和 Docker 菜单中会显示其状态。

您可以使用以下命令检查当前的 Kubernetes 版本：

```console
$ kubectl version
```

### 集群供应方法

Docker Desktop Kubernetes 可以使用 `kubeadm` 或 `kind` 供应器进行供应。

`kubeadm` 是较旧的供应器。它支持单节点集群，您无法选择 Kubernetes 版本，供应速度比 `kind` 慢，并且不支持 [增强容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/index.md)（ECI），这意味着如果启用了 ECI，集群可以工作但不受 ECI 保护。

`kind` 是较新的供应器。它支持多节点集群（更真实的 Kubernetes 设置），您可以选择 Kubernetes 版本，供应速度比 `kubeadm` 快，并且支持 ECI —— 启用 ECI 时，Kubernetes 集群在非特权 Docker 容器中运行，因此更安全。

| 功能 | `kubeadm` | `kind` |
| :------ | :-----: | :--: |
| 多节点集群支持 | 否 | 是 |
| Kubernetes 版本选择器 | 否 | 是 |
| 供应速度 | ~1 分钟 | ~30 秒 |
| ECI 支持 | 否 | 是 |
| 支持 containerd 镜像存储 | 是 | 是 |
| 支持 Docker 镜像存储 | 是 | 否 |

## 仪表板视图

启用 Kubernetes 集群后，**Kubernetes** 视图会显示一个实时仪表板视图，包括：

- 顶部的命名空间选择器
- 所选命名空间中资源的实时列表 —— Pod、服务、部署
- 资源创建、删除或修改时的自动更新

## 验证安装

确认您的集群正在运行：

```console
$ kubectl get nodes
NAME                 STATUS    ROLES            AGE       VERSION
docker-desktop       Ready     control-plane    3h        v1.29.1
```

如果 kubectl 指向其他环境，请切换到 Docker Desktop 上下文：

```console
$ kubectl config use-context docker-desktop
```

>[!TIP]
>
> 如果没有显示上下文，请尝试：
>
> - 在命令提示符或 PowerShell 中运行命令。
> - 将 `KUBECONFIG` 环境变量设置为指向您的 `.kube/config` 文件。

有关 `kubectl` 的更多信息，请参阅 [`kubectl` 文档](https://kubernetes.io/docs/reference/kubectl/overview/)。

## 编辑或停止您的集群

启用 Kubernetes 后：

- 选择 **Edit cluster**（编辑集群）以修改配置。例如，在 **kubeadm** 和 **kind** 之间切换，或更改节点数量。
- 选择 **Stop**（停止）以禁用集群。将显示进度，**Kubernetes** 视图返回到 **Create cluster** 屏幕。这将停止并删除 Kubernetes 容器，同时删除 `/usr/local/bin/kubectl` 命令。

## 升级您的集群

Kubernetes 集群不会随 Docker Desktop 更新自动升级。要升级集群，您必须在 **Kubernetes** 设置中手动选择 **Reset cluster**（重置集群）。

## 为 Kubernetes 控制平面镜像配置自定义镜像仓库

Docker Desktop 使用容器运行 Kubernetes 控制平面。默认情况下，Docker Desktop 从 Docker Hub 拉取相关容器镜像。拉取的镜像取决于 [集群供应模式](#cluster-provisioning-method)。

例如，在 `kind` 模式下需要以下镜像：

```console
docker.io/kindest/node:<tag>
docker.io/envoyproxy/envoy:<tag>
docker.io/docker/desktop-cloud-provider-kind:<tag>
docker.io/docker/desktop-containerd-registry-mirror:<tag>
```

在 `kubeadm` 模式下需要以下镜像：

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

镜像标签由 Docker Desktop 自动选择，基于多个因素，包括所使用的 Kubernetes 版本。每个镜像的标签可能不同，并且可能在 Docker Desktop 发布之间更改。要保持了解最新信息，请关注 Docker Desktop 发布说明。

为了适应无法访问 Docker Hub 的场景，管理员可以使用 [KubernetesImagesRepository](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md#kubernetes) 设置配置 Docker Desktop 从不同的仓库（例如，镜像）拉取上述镜像，如下所示。

镜像名称可以分解为 `[registry[:port]/][namespace/]repository[:tag]` 组件。`KubernetesImagesRepository` 设置允许用户覆盖镜像名称的 `[registry[:port]/][namespace]` 部分。

例如，如果 Docker Desktop Kubernetes 配置为 `kind` 模式，并且 `KubernetesImagesRepository` 设置为 `my-registry:5000/kind-images`，那么 Docker Desktop 将从以下位置拉取镜像：

```console
my-registry:5000/kind-images/node:<tag>
my-registry:5000/kind-images/envoy:<tag>
my-registry:5000/kind-images/desktop-cloud-provider-kind:<tag>
my-registry:5000/kind-images/desktop-containerd-registry-mirror:<tag>
```

这些镜像应该从 Docker Hub 中的相应镜像克隆/镜像而来。标签也必须与 Docker Desktop 期望的匹配。

推荐的设置方法如下：

1. 使用所需的集群供应方法（`kubeadm` 或 `kind`）启动 Kubernetes。
2. Kubernetes 启动后，使用 `docker ps` 查看 Docker Desktop 用于 Kubernetes 控制平面的容器镜像。
3. 将这些镜像（带匹配标签）克隆或镜像到您的自定义仓库。
4. 停止 Kubernetes 集群。
5. 配置 `KubernetesImagesRepository` 设置以指向您的自定义仓库。
6. 重启 Docker Desktop。
7. 使用 `docker ps` 命令验证 Kubernetes 集群是否正在使用自定义仓库镜像。

> [!NOTE]
>
> `KubernetesImagesRepository` 设置仅适用于 Docker Desktop 用于设置 Kubernetes 集群的控制平面镜像。它对其他 Kubernetes Pod 没有效果。

> [!NOTE]
>
> 在 Docker Desktop 4.43 或更早版本中，使用 `KubernetesImagesRepository` 并启用 [增强容器隔离 (ECI)](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md) 时，将以下镜像添加到 [ECI Docker 套接字挂载镜像列表](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md#enhanced-container-isolation)：
>
> `[imagesRepository]/desktop-cloud-provider-kind:`
> `[imagesRepository]/desktop-containerd-registry-mirror:`
>
> 这些容器挂载 Docker 套接字，因此您必须将镜像添加到 ECI 镜像列表。否则，ECI 将阻止挂载，Kubernetes 将无法启动。

## 故障排除

- 如果 Kubernetes 启动失败，请确保 Docker Desktop 有足够的分配资源在运行。检查 **Settings** > **Resources**。
- 如果 `kubectl` 命令返回错误，请确认上下文已设置为 `docker-desktop`
   ```console
   $ kubectl config use-context docker-desktop
   ```
   然后您可以尝试检查 Kubernetes 系统容器的日志（如果您已启用该设置）。
- 如果更新后遇到集群问题，请重置 Kubernetes 集群。重置 Kubernetes 集群有助于通过将集群恢复到干净状态来解决问题，清除可能导致问题的错误配置、损坏的数据或卡住的资源。如果问题仍然存在，您可能需要清理和清除数据，然后重启 Docker Desktop。