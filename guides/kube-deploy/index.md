# 部署到 Kubernetes

## 先决条件

- 根据 [Get Docker](/get-started/get-docker.md) 中的描述下载并安装 Docker Desktop。
- 完成 [第 2 部分](02_our_app.md) 中将应用容器化的内容。
- 确保已在 Docker Desktop 中开启 Kubernetes：
  如果 Kubernetes 未运行，请按照 [编排](orchestration.md) 中的说明完成设置。

## 简介

既然你已经证明了应用程序的各个组件可以作为独立的容器运行，那么是时候让它们由像 Kubernetes 这样的编排器来管理了。Kubernetes 提供了许多工具来扩展、联网、保护和维护你的容器化应用程序，其能力远超容器本身。

为了验证你的容器化应用程序在 Kubernetes 上能否良好运行，你将在你的开发机器上使用 Docker Desktop 内置的 Kubernetes 环境来部署你的应用程序，然后再将其移交到生产环境的完整 Kubernetes 集群上运行。Docker Desktop 创建的 Kubernetes 环境_功能齐全_，这意味着它拥有你的应用程序在真实集群上所能享有的所有 Kubernetes 功能，并且可以方便地从你的开发机器上访问。

## 使用 Kubernetes YAML 描述应用

Kubernetes 中的所有容器都被调度为 Pod，Pod 是一组共享某些资源的共址容器。此外，在实际应用程序中，你几乎从不创建单个的 Pod。相反，你大部分的工作负载会被调度为 Deployment，这是由 Kubernetes 自动维护的可扩展的 Pod 组。最后，所有 Kubernetes 对象都可以也应该在名为 Kubernetes YAML 文件的清单文件中进行描述。这些 YAML 文件描述了你的 Kubernetes 应用程序的所有组件和配置，可用于在任何 Kubernetes 环境中创建和销毁你的应用程序。

你已在本教程的编排概述部分编写了一个基本的 Kubernetes YAML 文件。现在，你可以编写一个稍微复杂一点的 YAML 文件来运行和管理你的 Todo 应用，该应用使用了在快速入门教程[第 2 部分](02_our_app.md)中创建的 `getting-started` 容器镜像。将以下内容放入一个名为 `bb.yaml` 的文件中：

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

在这个 Kubernetes YAML 文件中，有两个对象，由 `---` 分隔：

- 一个 `Deployment`，描述一组可扩展的相同 Pod。在本例中，你将只得到一个 `replica`（副本）或你的 Pod 的一个拷贝，并且该 Pod（在 `template:` 键下描述）中只有一个容器，该容器基于本教程上一步中创建的 `getting-started` 镜像。
- 一个 `NodePort` Service，它将把你主机上 30001 端口的流量路由到其目标 Pod 内部的 3000 端口，从而允许你从网络访问你的 Todo 应用。

另外，请注意，虽然 Kubernetes YAML 文件乍一看可能又长又复杂，但它几乎总是遵循相同的模式：

- `apiVersion`，表明解析此对象的 Kubernetes API
- `kind`，表明这是哪种类型的对象
- 一些 `metadata`，用于为你的对象应用名称等设置
- `spec`，指定你对象的所有参数和配置。

## 部署并检查你的应用程序

1.  在终端中，导航到你创建 `bb.yaml` 的位置，并将你的应用程序部署到 Kubernetes：

    ```console
    $ kubectl apply -f bb.yaml
    ```

    你应该会看到类似于以下内容的输出，这表明你的 Kubernetes 对象已成功创建：

    ```shell
    deployment.apps/bb-demo created
    service/bb-entrypoint created
    ```

2.  通过列出你的部署来确保一切正常工作：

    ```console
    $ kubectl get deployments
    ```

    如果一切正常，你的部署应该如下所示：

    ```shell
    NAME      READY   UP-TO-DATE   AVAILABLE   AGE
    bb-demo   1/1     1            1           40s
    ```

    这表明你在 YAML 中要求的所有 Pod（一个）都已启动并正在运行。对你的 Service 做同样的检查：

    ```console
    $ kubectl get services

    NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
    bb-entrypoint   NodePort    10.106.145.116   <none>        3000:30001/TCP   53s
    kubernetes      ClusterIP   10.96.0.1        <none>        443/TCP          138d
    ```

    除了默认的 `kubernetes` 服务，我们还看到了我们的 `bb-entrypoint` 服务，它正在 30001/TCP 端口上接收流量。

3.  打开浏览器，访问 `localhost:30001` 上的 Todo 应用。你应该能看到你的 Todo 应用程序，与你在教程[第 2 部分](02_our_app.md)中将其作为独立容器运行时看到的一样。

4.  确认无误后，拆除你的应用程序：

    ```console
    $ kubectl delete -f bb.yaml
    ```

## 结论

至此，你已经成功地使用 Docker Desktop 将你的应用程序部署到了开发机器上一个功能齐全的 Kubernetes 环境中。现在，你可以在自己的机器上为你的应用程序添加其他组件，并充分利用 Kubernetes 的所有功能和强大能力。

除了部署到 Kubernetes，你还将你的应用程序描述为一个 Kubernetes YAML 文件。这个简单的文本文件包含了创建处于运行状态的应用程序所需的一切。你可以将其检入版本控制并与你的同事分享。这使你可以将你的应用程序分发到其他集群（例如，可能在开发环境之后的测试和生产集群）。

## Kubernetes 参考

本文中使用的所有新 Kubernetes 对象的更多文档可在以下链接找到：

- [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
