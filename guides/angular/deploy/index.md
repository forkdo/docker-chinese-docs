# 测试你的 Angular 部署

## 先决条件

在开始之前，请确保你已完成以下步骤：
- 完成本指南的所有先前章节，从 [容器化 Angular 应用程序](containerize.md) 开始。
- 在 Docker Desktop 中 [启用 Kubernetes](/manuals/desktop/use-desktop/kubernetes.md#enable-kubernetes)。

> **初次接触 Kubernetes？**  
> 请访问 [Kubernetes 基础教程](https://kubernetes.io/docs/tutorials/kubernetes-basics/)，以熟悉集群、Pod、Deployment 和 Service 的工作原理。

---

## 概述

本节将指导你使用 [Docker Desktop 内置的 Kubernetes](/desktop/kubernetes/) 在本地部署容器化的 Angular 应用程序。在本地 Kubernetes 集群中运行你的应用程序，可以非常逼真地模拟真实的生产环境，使你能够在将工作负载提升到暂存或生产环境之前，充满信心地进行测试、验证和调试。

---

## 创建 Kubernetes YAML 文件

按照以下步骤定义你的部署配置：

1. 在项目的根目录中，创建一个名为：angular-sample-kubernetes.yaml 的新文件。

2. 在你的 IDE 或首选文本编辑器中打开该文件。

3. 添加以下配置，并务必将 `{DOCKER_USERNAME}` 和 `{DOCKERHUB_PROJECT_NAME}` 替换为你在上一节 [使用 GitHub Actions 自动化构建](configure-github-actions.md) 中的实际 Docker Hub 用户名和仓库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: angular-sample
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: angular-sample
  template:
    metadata:
      labels:
        app: angular-sample
    spec:
      containers:
        - name: angular-container
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
  name: angular-sample-service
  namespace: default
spec:
  type: NodePort
  selector:
    app: angular-sample
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30001
```

此清单定义了两个关键的 Kubernetes 资源，由 `---` 分隔：

- **Deployment**
  在 Pod 内部署 Angular 应用程序的一个副本。该 Pod 使用由你的 GitHub Actions CI/CD 工作流构建并推送的 Docker 镜像（参考 [使用 GitHub Actions 自动化构建](configure-github-actions.md)）。
  容器监听端口 `8080`，该端口通常由 [Nginx](https://nginx.org/en/docs/) 用于提供你的生产环境 Angular 应用。

- **Service (NodePort)**
  将部署的 Pod 暴露给你的本地机器。
  它将主机上的端口 `30001` 的流量转发到容器内的端口 `8080`。
  这使你可以在浏览器中通过 [http://localhost:30001](http://localhost:30001) 访问该应用程序。

> [!NOTE]
> 要了解更多关于 Kubernetes 对象的信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

---

## 部署并检查你的应用程序

按照以下步骤将容器化的 Angular 应用部署到本地 Kubernetes 集群，并验证其是否正常运行。

### 步骤 1. 应用 Kubernetes 配置

在你的终端中，导航到 `angular-sample-kubernetes.yaml` 文件所在的目录，然后使用以下命令部署资源：

```console
  $ kubectl apply -f angular-sample-kubernetes.yaml
```

如果一切配置正确，你将看到确认 Deployment 和 Service 均已创建的消息：

```shell
  deployment.apps/angular-sample created
  service/angular-sample-service created
```
   
这确认了 Deployment 和 Service 都已成功创建，并且现在正在你的本地集群中运行。

### 步骤 2. 检查 Deployment 状态

运行以下命令检查你的部署状态：
   
```console
  $ kubectl get deployments
```

你应该会看到类似以下的输出：

```shell
  NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
  angular-sample       1/1     1            1           14s
```

这确认了你的 Pod 已启动并正在运行，且有一个可用的副本。

### 步骤 3. 验证 Service 暴露情况

检查 NodePort 服务是否将你的应用暴露给本地机器：

```console
$ kubectl get services
```

你应该会看到类似以下的内容：

```shell
NAME                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
angular-sample-service   NodePort    10.100.185.105    <none>        8080:30001/TCP   1m
```

此输出确认了你的应用可以通过端口 30001 上的 NodePort 访问。

### 步骤 4. 在浏览器中访问你的应用

打开浏览器并导航到 [http://localhost:30001](http://localhost:30001)。

你应该会看到你的生产就绪的 Angular 示例应用程序正在运行——由你的本地 Kubernetes 集群提供服务。

### 步骤 5. 清理 Kubernetes 资源

测试完成后，你可以使用以下命令删除 deployment 和 service：

```console
  $ kubectl delete -f angular-sample-kubernetes.yaml
```

预期输出：

```shell
  deployment.apps "angular-sample" deleted
  service "angular-sample-service" deleted
```

这确保了你的集群保持干净，并为下一次部署做好准备。
   
---

## 总结

在本节中，你学习了如何使用 Docker Desktop 将 Angular 应用程序部署到本地 Kubernetes 集群。这种设置允许你在将容器化应用部署到云端之前，在类似生产的环境中进行测试和调试。

你完成的任务包括：

- 为你的 Angular 应用创建了 Kubernetes Deployment 和 NodePort Service
- 使用 `kubectl apply` 在本地部署应用程序
- 验证了应用正在运行，并且可以通过 `http://localhost:30001` 访问
- 测试后清理了 Kubernetes 资源

---

## 相关资源

探索官方参考资料和最佳实践，以优化你的 Kubernetes 部署工作流：

- [Kubernetes 文档](https://kubernetes.io/docs/home/) – 学习核心概念、工作负载、服务等。
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/use-desktop/kubernetes.md) – 使用 Docker Desktop 的内置 Kubernetes 支持进行本地测试和开发。
- [`kubectl` CLI 参考](https://kubernetes.io/docs/reference/kubectl/) – 从命令行管理 Kubernetes 集群。
- [Kubernetes Deployment 资源](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) – 了解如何使用 Deployment 管理和扩展应用程序。
- [Kubernetes Service 资源](https://kubernetes.io/docs/concepts/services-networking/service/) – 学习如何将你的应用程序暴露给内部和外部流量。
