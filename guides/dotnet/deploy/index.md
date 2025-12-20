# 测试 .NET 部署

## 先决条件

- 完成本指南的所有先前部分，从[容器化 .NET 应用程序](containerize.md)开始。
- 在 Docker Desktop 中[开启 Kubernetes](/manuals/desktop/use-desktop/kubernetes.md#enable-kubernetes)。

## 概述

在本节中，您将学习如何使用 Docker Desktop 将您的应用程序部署到开发机器上功能齐全的 Kubernetes 环境中。这允许您在部署之前在本地测试和调试工作负载。

## 创建 Kubernetes YAML 文件

在您的 `docker-dotnet-sample` 目录中，创建一个名为 `docker-dotnet-kubernetes.yaml` 的文件。在 IDE 或文本编辑器中打开该文件，并添加以下内容。将 `DOCKER_USERNAME/REPO_NAME` 替换为您的 Docker 用户名和在[为您的 .NET 应用程序配置 CI/CD](configure-ci-cd.md) 中创建的仓库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    service: server
  name: server
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: server
  strategy: {}
  template:
    metadata:
      labels:
        service: server
    spec:
      initContainers:
        - name: wait-for-db
          image: busybox:1.28
          command:
            [
              "sh",
              "-c",
              'until nc -zv db 5432; do echo "waiting for db"; sleep 2; done;',
            ]
      containers:
        - image: DOCKER_USERNAME/REPO_NAME
          name: server
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
              hostPort: 8080
              protocol: TCP
          resources: {}
      restartPolicy: Always
status: {}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    service: db
  name: db
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: db
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        service: db
    spec:
      containers:
        - env:
            - name: POSTGRES_DB
              value: example
            - name: POSTGRES_PASSWORD
              value: example
          image: postgres:18
          name: db
          ports:
            - containerPort: 5432
              protocol: TCP
          resources: {}
      restartPolicy: Always
status: {}
---
apiVersion: v1
kind: Service
metadata:
  labels:
    service: server
  name: server
  namespace: default
spec:
  type: NodePort
  ports:
    - name: "8080"
      port: 8080
      targetPort: 8080
      nodePort: 30001
  selector:
    service: server
status:
  loadBalancer: {}
---
apiVersion: v1
kind: Service
metadata:
  labels:
    service: db
  name: db
  namespace: default
spec:
  ports:
    - name: "5432"
      port: 5432
      targetPort: 5432
  selector:
    service: db
status:
  loadBalancer: {}
```

在这个 Kubernetes YAML 文件中，有四个对象，由 `---` 分隔。除了数据库的 Service 和 Deployment 外，另外两个对象是：

- 一个 Deployment，描述了一组可扩展的相同 Pod。在本例中，您将只获得一个副本或 Pod 的副本。该 Pod 在 `template` 下描述，其中只有一个容器。该容器是根据在[为您的 .NET 应用程序配置 CI/CD](configure-ci-cd.md) 中由 GitHub Actions 构建的镜像创建的。
- 一个 NodePort 服务，它将主机上的端口 30001 的流量路由到它所路由到的 Pod 内部的端口 8080，允许您从网络访问您的应用程序。

要了解更多关于 Kubernetes 对象的信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

## 部署并检查您的应用程序

1. 在终端中，导航到 `docker-dotnet-sample` 目录，并将您的应用程序部署到 Kubernetes。

   ```console
   $ kubectl apply -f docker-dotnet-kubernetes.yaml
   ```

   您应该会看到类似以下内容的输出，表明您的 Kubernetes 对象已成功创建。

   ```shell
   deployment.apps/db created
   service/db created
   deployment.apps/server created
   service/server created
   ```

2. 通过列出您的部署来确保一切正常。

   ```console
   $ kubectl get deployments
   ```

   您的部署应如下所示列出：

   ```shell
   NAME     READY   UP-TO-DATE   AVAILABLE   AGE
   db       1/1     1            1           76s
   server   1/1     1            1           76s
   ```

   这表明所有的 Pod 都已启动并运行。对您的服务执行相同的检查。

   ```console
   $ kubectl get services
   ```

   您应该会得到类似以下的输出。

   ```shell
   NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
   db           ClusterIP   10.96.156.90    <none>        5432/TCP         2m8s
   kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP          164m
   server       NodePort    10.102.94.225   <none>        8080:30001/TCP   2m8s
   ```

   除了默认的 `kubernetes` 服务外，您还可以看到您的 `server` 服务和 `db` 服务。`server` 服务正在端口 30001/TCP 上接收流量。

3. 打开浏览器并访问您的应用程序，地址为 `localhost:30001`。您应该能看到您的应用程序。

4. 运行以下命令以拆除您的应用程序。

   ```console
   $ kubectl delete -f docker-dotnet-kubernetes.yaml
   ```

## 总结

在本节中，您学习了如何使用 Docker Desktop 将您的应用程序部署到开发机器上功能齐全的 Kubernetes 环境中。

相关信息：

- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/use-desktop/kubernetes.md)
- [Swarm 模式概述](/manuals/engine/swarm/_index.md)
