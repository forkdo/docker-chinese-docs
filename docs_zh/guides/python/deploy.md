---
title: 测试您的 Python 部署
linkTitle: 测试您的部署
weight: 50
keywords: deploy, kubernetes, python
description: 学习如何使用 Kubernetes 进行本地开发
aliases:
  - /language/python/deploy/
  - /guides/language/python/deploy/
---

## 前提条件

- 完成本指南的所有先前部分，从 [为 Python 开发使用容器](develop.md) 开始。
- 在 Docker Desktop 中 [开启 Kubernetes](/manuals/desktop/use-desktop/kubernetes.md#enable-kubernetes)。

## 概述

在本节中，您将学习如何使用 Docker Desktop 将您的应用程序部署到开发机器上功能齐全的 Kubernetes 环境中。这允许您在部署之前在本地 Kubernetes 上测试和调试您的工作负载。

## 创建 Kubernetes YAML 文件

在您的 `python-docker-dev-example` 目录中，创建一个名为 `docker-postgres-kubernetes.yaml` 的文件。在 IDE 或文本编辑器中打开该文件，并添加以下内容。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:18
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              value: example
            - name: POSTGRES_USER
              value: postgres
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: POSTGRES_PASSWORD
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql
      volumes:
        - name: postgres-data
          persistentVolumeClaim:
            claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: default
spec:
  ports:
    - port: 5432
  selector:
    app: postgres
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: default
type: Opaque
data:
  POSTGRES_PASSWORD: cG9zdGdyZXNfcGFzc3dvcmQ= # Base64 encoded password (e.g., 'postgres_password')
```

在您的 `python-docker-dev-example` 目录中，创建一个名为 `docker-python-kubernetes.yaml` 的文件。将 `DOCKER_USERNAME/REPO_NAME` 替换为您的 Docker 用户名和您在 [为您的 Python 应用程序配置 CI/CD](./configure-github-actions.md) 中创建的仓库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-python-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: fastapi
  template:
    metadata:
      labels:
        service: fastapi
    spec:
      containers:
        - name: fastapi-service
          image: DOCKER_USERNAME/REPO_NAME
          imagePullPolicy: Always
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: POSTGRES_PASSWORD
            - name: POSTGRES_USER
              value: postgres
            - name: POSTGRES_DB
              value: example
            - name: POSTGRES_SERVER
              value: postgres
            - name: POSTGRES_PORT
              value: "5432"
          ports:
            - containerPort: 8001
---
apiVersion: v1
kind: Service
metadata:
  name: service-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    service: fastapi
  ports:
    - port: 8001
      targetPort: 8001
      nodePort: 30001
```

在这些 Kubernetes YAML 文件中，有各种由 `---` 分隔的对象：

- 一个 Deployment，描述了一组可扩展的相同 Pod。在这种情况下，您将只获得一个副本或 Pod 的拷贝。该 Pod 在 `template` 下描述，其中只有一个容器。该容器由 GitHub Actions 在 [为您的 Python 应用程序配置 CI/CD](configure-github-actions.md) 中构建的镜像创建。
- 一个 Service，它将定义端口如何在容器中映射。
- 一个 PersistentVolumeClaim，用于定义一个在数据库重启期间保持持久性的存储。
- 一个 Secret，使用 Kubernetes Secret 资源将数据库密码作为示例进行保存。
- 一个 NodePort 服务，它将主机上的端口 30001 的流量路由到它所路由到的 Pod 内部的端口 8001，允许您从网络访问您的应用程序。

要了解更多关于 Kubernetes 对象的信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

> [!NOTE]
>
> - `NodePort` 服务适用于开发/测试目的。对于生产环境，您应该实现一个 [ingress-controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)。

## 部署并检查您的应用程序

1. 在终端中，导航到 `python-docker-dev-example` 并将您的数据库部署到 Kubernetes。

   ```console
   $ kubectl apply -f docker-postgres-kubernetes.yaml
   ```

   您应该看到类似以下的输出，表明您的 Kubernetes 对象已成功创建。

   ```console
   deployment.apps/postgres created
   service/postgres created
   persistentvolumeclaim/postgres-pvc created
   secret/postgres-secret created
   ```

   现在，部署您的 Python 应用程序。

   ```console
   kubectl apply -f docker-python-kubernetes.yaml
   ```

   您应该看到类似以下的输出，表明您的 Kubernetes 对象已成功创建。

   ```console
   deployment.apps/docker-python-demo created
   service/service-entrypoint created
   ```

2. 通过列出您的部署来确保一切正常。

   ```console
   $ kubectl get deployments
   ```

   您的部署应如下所示：

   ```console
   NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
   docker-python-demo   1/1     1            1           48s
   postgres             1/1     1            1           2m39s
   ```

   这表明您在 YAML 中要求的所有 Pod 都已启动并运行。对您的服务执行相同的检查。

   ```console
   $ kubectl get services
   ```

   您应该得到类似以下的输出。

   ```console
   NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
   kubernetes           ClusterIP   10.43.0.1      <none>        443/TCP          13h
   postgres             ClusterIP   10.43.209.25   <none>        5432/TCP         3m10s
   service-entrypoint   NodePort    10.43.67.120   <none>        8001:30001/TCP   79s
   ```

   除了默认的 `kubernetes` 服务外，您还可以看到您的 `service-entrypoint` 服务，它在端口 30001/TCP 上接收流量，以及内部的 `ClusterIP` `postgres`，端口 `5432` 已打开以接受来自您 Python 应用程序的连接。

3. 在终端中，使用 curl 访问该服务。请注意，此示例中未部署数据库。

   ```console
   $ curl http://localhost:30001/
   Hello, Docker!!!
   ```

4. 运行以下命令以拆除您的应用程序。

   ```console
   $ kubectl delete -f docker-python-kubernetes.yaml
   $ kubectl delete -f docker-postgres-kubernetes.yaml
   ```

## 总结

在本节中，您学习了如何使用 Docker Desktop 将您的应用程序部署到开发机器上功能齐全的 Kubernetes 环境中。

相关信息：

- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/use-desktop/kubernetes.md)
- [Swarm 模式概述](/manuals/engine/swarm/_index.md)