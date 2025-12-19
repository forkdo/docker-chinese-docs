---
title: 测试您的 React.js 部署
linkTitle: 测试您的部署
weight: 60
keywords: deploy, kubernetes, react, react.js
description: 了解如何在本地部署以测试和调试您的 Kubernetes 部署

---

## 先决条件

在开始之前，请确保您已完成以下操作：
- 完成本指南的所有先前部分，从 [容器化 React.js 应用程序](containerize.md) 开始。
- 在 Docker Desktop 中 [启用 Kubernetes](/manuals/desktop/use-desktop/kubernetes.md#enable-kubernetes)。

> **初次接触 Kubernetes？**  
> 请访问 [Kubernetes 基础教程](https://kubernetes.io/docs/tutorials/kubernetes-basics/)，以熟悉集群、Pod、部署和服务的工作原理。

---

## 概述

本节将指导您使用 [Docker Desktop 内置的 Kubernetes](/desktop/kubernetes/) 在本地部署容器化的 React.js 应用程序。在本地 Kubernetes 集群中运行您的应用程序，可以让您密切模拟真实的生产环境，从而在将工作负载提升到暂存或生产环境之前，充满信心地进行测试、验证和调试。

---

## 创建 Kubernetes YAML 文件

请按照以下步骤定义您的部署配置：

1. 在项目的根目录中，创建一个名为：reactjs-sample-kubernetes.yaml 的新文件。

2. 在您的 IDE 或首选文本编辑器中打开该文件。

3. 添加以下配置，并务必将 `{DOCKER_USERNAME}` 和 `{DOCKERHUB_PROJECT_NAME}` 替换为您在上一节 [使用 GitHub Actions 自动化构建](configure-github-actions.md) 中的实际 Docker Hub 用户名和仓库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: reactjs-sample
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: reactjs-sample
  template:
    metadata:
      labels:
        app: reactjs-sample
    spec:
      containers:
        - name: reactjs-container
          image: {DOCKER_USERNAME}/{DOCKERHUB_PROJECT_NAME}:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name:  reactjs-sample-service
  namespace: default
spec:
  type: NodePort
  selector:
    app:  reactjs-sample
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30001
```

此清单定义了两个关键的 Kubernetes 资源，由 `---` 分隔：

- **Deployment (部署)**
  在 Pod 内部部署您的 React.js 应用程序的单个副本。该 Pod 使用由您的 GitHub Actions CI/CD 工作流构建并推送的 Docker 镜像（请参阅 [使用 GitHub Actions 自动化构建](configure-github-actions.md)）。
  容器监听端口 `8080`，该端口通常由 [Nginx](https://nginx.org/en/docs/) 用于提供您的生产环境 React 应用。

- **Service (服务) (NodePort)**
  将部署的 Pod 暴露给您的本地机器。
  它将主机上的端口 `30001` 的流量转发到容器内部的端口 `8080`。
  这让您可以访问浏览器中的应用程序：[http://localhost:30001](http://localhost:30001)。

> [!NOTE]
> 要了解有关 Kubernetes 对象的更多信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

---

## 部署并检查您的应用程序

请按照以下步骤将容器化的 React.js 应用程序部署到本地 Kubernetes 集群，并验证其是否正常运行。

### 步骤 1. 应用 Kubernetes 配置

在您的终端中，导航到 `reactjs-sample-kubernetes.yaml` 文件所在的目录，然后使用以下命令部署资源：

```console
  $ kubectl apply -f reactjs-sample-kubernetes.yaml
```

如果一切配置正确，您将看到确认 Deployment 和 Service 均已创建：

```shell
  deployment.apps/reactjs-sample created
  service/reactjs-sample-service created
```
   
此输出意味着 Deployment 和 Service 均已成功创建，现在正在您的本地集群中运行。

### 步骤 2. 检查 Deployment 状态

运行以下命令检查您的部署状态：
   
```console
  $ kubectl get deployments
```

您应该会看到类似以下的输出：

```shell
  NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
  reactjs-sample       1/1     1            1           14s
```

这确认您的 Pod 已启动并正在运行，且有一个可用的副本。

### 步骤 3. 验证 Service 暴露情况

检查 NodePort 服务是否将您的应用程序暴露给本地机器：

```console
$ kubectl get services
```

您应该会看到类似以下内容：

```shell
NAME                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
reactjs-sample-service   NodePort    10.100.244.65    <none>        8080:30001/TCP   1m
```

此输出确认您的应用程序可通过端口 30001 上的 NodePort 访问。

### 步骤 4. 在浏览器中访问您的应用程序

打开浏览器并导航至 [http://localhost:30001](http://localhost:30001)。

您应该会看到您的生产就绪的 React.js 示例应用程序正在运行——由您的本地 Kubernetes 集群提供服务。

### 步骤 5. 清理 Kubernetes 资源

测试完成后，您可以使用以下命令删除部署和服务：

```console
  $ kubectl delete -f reactjs-sample-kubernetes.yaml
```

预期输出：

```shell
  deployment.apps "reactjs-sample" deleted
  service "reactjs-sample-service" deleted
```

这确保您的集群保持整洁，并为下一次部署做好准备。
   
---

## 总结

在本节中，您学习了如何使用 Docker Desktop 将您的 React.js 应用程序部署到本地 Kubernetes 集群。此设置允许您在将应用程序部署到云之前，在类似生产的环境中测试和调试容器化应用程序。

您完成的任务：

- 为您的 React.js 应用程序创建了 Kubernetes Deployment 和 NodePort Service
- 使用 `kubectl apply` 在本地部署应用程序
- 验证应用程序正在运行，并且可以通过 `http://localhost:30001` 访问
- 测试后清理了 Kubernetes 资源

---

## 相关资源

探索官方参考资料和最佳实践，以优化您的 Kubernetes 部署工作流：

- [Kubernetes 文档](https://kubernetes.io/docs/home/) – 了解核心概念、工作负载、服务等。
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/use-desktop/kubernetes.md) – 使用 Docker Desktop 的内置 Kubernetes 支持进行本地测试和开发。
- [`kubectl` CLI 参考](https://kubernetes.io/docs/reference/kubectl/) – 从命令行管理 Kubernetes 集群。
- [Kubernetes Deployment 资源](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) – 了解如何使用 Deployment 管理和扩展应用程序。
- [Kubernetes Service 资源](https://kubernetes.io/docs/concepts/services-networking/service/) – 了解如何将您的应用程序暴露给内部和外部流量。