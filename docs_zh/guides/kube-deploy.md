---
title: 部署到 Kubernetes
keywords: kubernetes, pods, deployments, kubernetes services
description: 学习如何使用 Kubernetes 描述和部署一个简单应用。
aliases:
  - /get-started/kube-deploy/
  - /guides/deployment-orchestration/kube-deploy/
summary: |
  学习如何使用 Kubernetes 部署和编排 Docker 容器。
tags: [deploy]
params:
  time: 10 分钟
---

## 前置条件

- 按照 [获取 Docker](/get-started/get-docker.md) 中的说明下载并安装 Docker Desktop。
- 完成 [第 2 部分](02_our_app.md) 中的应用容器化操作。
- 确保 Docker Desktop 中已启用 Kubernetes：
  如果 Kubernetes 未运行，请按照 [编排](orchestration.md) 中的说明完成设置。

## 介绍

现在你已经证明了应用的各个组件可以作为独立容器运行，是时候安排它们由 Kubernetes 这样的编排器来管理了。Kubernetes 提供了许多工具来扩展、网络化、保护和维护你的容器化应用，其能力远超容器本身。

为了验证你的容器化应用在 Kubernetes 上运行良好，你将使用 Docker Desktop 内置的 Kubernetes 环境在开发机器上部署应用，然后再将其部署到生产环境中的完整 Kubernetes 集群上。Docker Desktop 创建的 Kubernetes 环境是_功能完整的_，意味着它具备你的应用在真实集群上运行时的所有 Kubernetes 功能，你可以直接从开发机器上方便地访问。

## 使用 Kubernetes YAML 描述应用

Kubernetes 中的所有容器都作为 Pod 调度，Pod 是共享某些资源的同处容器组。此外，在实际应用中，你几乎从不创建单个 Pod。相反，你的大部分工作负载都作为部署（Deployments）调度，它们是可扩展的 Pod 组，由 Kubernetes 自动维护。最后，所有 Kubernetes 对象都应（且应该）在称为 Kubernetes YAML 文件的清单中描述。这些 YAML 文件描述了你的 Kubernetes 应用的所有组件和配置，可用于在任何 Kubernetes 环境中创建和销毁你的应用。

你已经在本教程的编排概述部分编写了一个基本的 Kubernetes YAML 文件。现在，你可以编写一个稍微复杂的 YAML 文件来运行和管理你的 Todo 应用，即在快速入门教程的 [第 2 部分](02_our_app.md) 中创建的 `getting-started` 容器镜像。将以下内容保存到名为 `bb.yaml` 的文件中：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bb-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      bb: web
  template:
    metadata:
      labels:
        bb: web
    spec:
      containers:
        - name: bb-site
          image: getting-started
          imagePullPolicy: Never
---
apiVersion: v1
kind: Service
metadata:
  name: bb-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    bb: web
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30001
```

在此 Kubernetes YAML 文件中，有两个对象，由 `---` 分隔：

- 一个 `Deployment`，描述一个可扩展的相同 Pod 组。在这种情况下，你将只得到一个 `replica`（副本），即你的 Pod，而该 Pod（在 `template:` 键下描述）只有一个容器，基于你在本教程上一步中创建的 `getting-started` 镜像。
- 一个 `NodePort` 服务，它将从主机的 30001 端口路由流量到 Pod 内部的 3000 端口，允许你从网络访问你的 Todo 应用。

另外，请注意，虽然 Kubernetes YAML 一开始看起来可能又长又复杂，但它几乎总是遵循相同的模式：

- `apiVersion`，指示解析此对象的 Kubernetes API
- `kind`，指示对象的类型
- 一些 `metadata`，用于为对象命名等
- `spec`，指定对象的所有参数和配置

## 部署并检查你的应用

1. 在终端中，导航到你创建 `bb.yaml` 的位置，将应用部署到 Kubernetes：

   ```console
   $ kubectl apply -f bb.yaml
   ```

   你应该看到类似以下的输出，表示你的 Kubernetes 对象已成功创建：

   ```shell
   deployment.apps/bb-demo created
   service/bb-entrypoint created
   ```

2. 通过列出你的部署来确保一切正常：

   ```console
   $ kubectl get deployments
   ```

   如果一切正常，你的部署应如下所示列出：

   ```shell
   NAME      READY   UP-TO-DATE   AVAILABLE   AGE
   bb-demo   1/1     1            1           40s
   ```

   这表示你在 YAML 中请求的所有 Pod 都已启动并运行。对你的服务执行相同的检查：

   ```console
   $ kubectl get services

   NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   bb-entrypoint   NodePort    10.106.145.116   <none>        3000:30001/TCP   53s
   kubernetes      ClusterIP   10.96.0.1        <none>        443/TCP          138d
   ```

   除了默认的 `kubernetes` 服务外，我们看到我们的 `bb-entrypoint` 服务正在接受 30001/TCP 端口的流量。

3. 打开浏览器，访问 `localhost:30001` 上的 Todo 应用。你应该看到你的 Todo 应用，与你在教程的 [第 2 部分](02_our_app.md) 中将其作为独立容器运行时相同。

4. 满意后，拆除你的应用：

   ```console
   $ kubectl delete -f bb.yaml
   ```

## 结论

至此，你已成功使用 Docker Desktop 将应用部署到开发机器上的完全功能的 Kubernetes 环境。现在你可以向应用添加其他组件，并充分利用 Kubernetes 的所有功能和强大能力，就在你的机器上。

除了部署到 Kubernetes 外，你还使用 Kubernetes YAML 文件描述了你的应用。这个简单的文本文件包含以运行状态创建应用所需的一切。你可以将其检入版本控制并与同事共享。这让你能够将应用分发到其他集群（比如在开发环境之后的测试和生产集群）。

## Kubernetes 参考资料

本文使用的所有新 Kubernetes 对象的进一步文档可在此处找到：

- [Kubernetes Pod](https://kubernetes.io/docs/concepts/workloads/pods/pod/)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)