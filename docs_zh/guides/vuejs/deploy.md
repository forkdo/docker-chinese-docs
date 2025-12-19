---
title: 测试 Vue.js 部署
linkTitle: 测试部署
weight: 60
keywords: deploy, kubernetes, vue, vue.js
description: 了解如何本地部署以测试和调试 Kubernetes 部署

---

## 先决条件

开始前，请确保已完成以下步骤：
- 完成本指南的所有先前章节，从[容器化 Vue.js 应用程序](containerize.md)开始。
- 在 Docker Desktop 中[启用 Kubernetes](/manuals/desktop/use-desktop/kubernetes.md#enable-kubernetes)。

> **Kubernetes 新手？**  
> 访问 [Kubernetes 基础教程](https://kubernetes.io/docs/tutorials/kubernetes-basics/) 以熟悉集群、Pod、Deployment 和 Service 的工作原理。

---

## 概述

本节指导您使用 [Docker Desktop 内置的 Kubernetes](/desktop/kubernetes/) 在本地部署容器化的 Vue.js 应用程序。在本地 Kubernetes 集群中运行应用程序可以高度模拟真实生产环境，让您在将工作负载推进到预发布或生产环境之前，能够自信地测试、验证和调试。

---

## 创建 Kubernetes YAML 文件

按照以下步骤定义部署配置：

1. 在项目根目录创建一个名为 `vuejs-sample-kubernetes.yaml` 的新文件

2. 在 IDE 或您喜欢的文本编辑器中打开该文件

3. 添加以下配置，并确保将 `{DOCKER_USERNAME}` 和 `{DOCKERHUB_PROJECT_NAME}` 替换为实际的 Docker Hub 用户名和上一章节[使用 GitHub Actions 自动化构建](configure-github-actions.md)中的仓库名称


```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vuejs-sample
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vuejs-sample
  template:
    metadata:
      labels:
        app: vuejs-sample
    spec:
      containers:
        - name: vuejs-container
          image: {DOCKER_USERNAME}/{DOCKERHUB_PROJECT_NAME}:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: "500m"
              memory: "256Mi"
            requests:
              cpu: "250m"
              memory: "128Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: vuejs-sample-service
  namespace: default
spec:
  type: NodePort
  selector:
    app: vuejs-sample
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30001
```

此清单定义了两个关键的 Kubernetes 资源，由 `---` 分隔：

- Deployment  
  在 Pod 中部署单个副本的 Vue.js 应用程序。该 Pod 使用 GitHub Actions CI/CD 工作流构建并推送的 Docker 镜像  
  （参见[使用 GitHub Actions 自动化构建](configure-github-actions.md)）。  
  容器监听端口 `8080`，通常由 [Nginx](https://nginx.org/en/docs/) 用于提供生产环境的 Vue.js 应用。

- Service (NodePort)  
  将部署的 Pod 暴露给本地机器。  
  它将主机端口 `30001` 的流量转发到容器内的端口 `8080`。  
  这样您就可以通过浏览器访问 [http://localhost:30001](http://localhost:30001) 来访问应用程序。

> [!NOTE]
> 要了解有关 Kubernetes 对象的更多信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

---

## 部署并检查应用程序

按照以下步骤将容器化的 Vue.js 应用程序部署到本地 Kubernetes 集群，并验证其是否正常运行。

### 步骤 1. 应用 Kubernetes 配置

在终端中，导航到 `vuejs-sample-kubernetes.yaml` 文件所在目录，然后使用以下命令部署资源：

```console
  $ kubectl apply -f vuejs-sample-kubernetes.yaml
```

如果一切配置正确，您将看到 Deployment 和 Service 已创建的确认信息：

```shell
  deployment.apps/vuejs-sample created
  service/vuejs-sample-service created
```
   
这确认了 Deployment 和 Service 已成功创建，并正在本地集群中运行。

### 步骤 2. 检查 Deployment 状态

运行以下命令检查部署状态：
   
```console
  $ kubectl get deployments
```

您应该看到类似以下输出：

```shell
  NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
  vuejs-sample         1/1     1            1           1m14s
```

这确认您的 Pod 已启动并运行，有一个副本可用。

### 步骤 3. 验证 Service 暴露情况

检查 NodePort Service 是否将应用程序暴露给本地机器：

```console
$ kubectl get services
```

您应该看到类似以下内容：

```shell
NAME                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
vuejs-sample-service     NodePort    10.98.233.59    <none>        8080:30001/TCP   1m
```

此输出确认您的应用程序已通过 NodePort 在端口 30001 上可用。

### 步骤 4. 在浏览器中访问应用程序

打开浏览器并导航至 [http://localhost:30001](http://localhost:30001)。

您应该看到生产就绪的 Vue.js 示例应用程序正在运行 —— 由本地 Kubernetes 集群提供服务。

### 步骤 5. 清理 Kubernetes 资源

测试完成后，可以使用以下命令删除 Deployment 和 Service：

```console
  $ kubectl delete -f vuejs-sample-kubernetes.yaml
```

预期输出：

```shell
  deployment.apps "vuejs-sample" deleted
  service "vuejs-sample-service" deleted
```

这确保您的集群保持清洁，为下一次部署做好准备。
   
---

## 总结

在本节中，您学习了如何使用 Docker Desktop 将 Vue.js 应用程序部署到本地 Kubernetes 集群。此设置允许您在将应用程序部署到云端之前，在类似生产的环境中测试和调试容器化应用。

您已完成的工作：

- 为 Vue.js 应用程序创建了 Kubernetes Deployment 和 NodePort Service  
- 使用 `kubectl apply` 在本地部署应用程序  
- 验证应用程序正在运行并可通过 `http://localhost:30001` 访问  
- 测试后清理 Kubernetes 资源

---

## 相关资源

探索官方参考和最佳实践，以提升您的 Kubernetes 部署工作流：

- [Kubernetes 文档](https://kubernetes.io/docs/home/) – 了解核心概念、工作负载、Service 等。  
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals) – 利用 Docker Desktop 内置的 Kubernetes 支持进行本地测试和开发。
- [`kubectl` CLI 参考](https://kubernetes.io/docs/reference/kubectl/) – 从命令行管理 Kubernetes 集群。  
- [Kubernetes Deployment 资源](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) – 了解如何使用 Deployment 管理和扩展应用程序。  
- [Kubernetes Service 资源](https://kubernetes.io/docs/concepts/services-networking/service/) – 学习如何将应用程序暴露给内部和外部流量。