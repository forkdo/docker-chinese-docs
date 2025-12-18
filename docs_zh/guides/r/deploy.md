---
title: 测试你的 R 部署
linkTitle: 测试你的部署
weight: 50
keywords: 部署, kubernetes, R
description: 了解如何在本地使用 Kubernetes 进行开发
aliases:
  - /language/r/deploy/
  - /guides/language/r/deploy/
---

## 前置条件

- 完成本指南之前的所有章节，从 [容器化 R 应用](containerize.md) 开始。
- 在 Docker Desktop 中 [启用 Kubernetes](/manuals/desktop/use-desktop/kubernetes.md#enable-kubernetes)。

## 概述

在本节中，你将学习如何使用 Docker Desktop 将你的应用部署到开发机器上的完整 Kubernetes 环境。这让你可以在本地测试和调试工作负载，然后再部署到生产环境。

## 创建 Kubernetes YAML 文件

在你的 `r-docker-dev` 目录中，创建一个名为 `docker-r-kubernetes.yaml` 的文件。在 IDE 或文本编辑器中打开该文件，并添加以下内容。将 `DOCKER_USERNAME/REPO_NAME` 替换为你的 Docker 用户名和在 [为你的 R 应用配置 CI/CD](configure-ci-cd.md) 中创建的仓库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-r-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: shiny
  template:
    metadata:
      labels:
        service: shiny
    spec:
      containers:
        - name: shiny-service
          image: DOCKER_USERNAME/REPO_NAME
          imagePullPolicy: Always
          env:
            - name: POSTGRES_PASSWORD
              value: mysecretpassword
---
apiVersion: v1
kind: Service
metadata:
  name: service-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    service: shiny
  ports:
    - port: 3838
      targetPort: 3838
      nodePort: 30001
```

在这个 Kubernetes YAML 文件中，有两个对象，用 `---` 分隔：

- 一个 Deployment，描述一组可扩展的相同 Pod。在本例中，你将只得到一个副本，即你的 Pod 的一个副本。在 `template` 下描述的 Pod 中只有一个容器。该容器是从 GitHub Actions 在 [为你的 R 应用配置 CI/CD](configure-ci-cd.md) 中构建的镜像创建的。
- 一个 NodePort 服务，它将把主机上的 30001 端口的流量路由到 Pod 内部的 3838 端口，允许你从网络访问你的应用。

要了解有关 Kubernetes 对象的更多信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

## 部署并检查你的应用

1. 在终端中，导航到 `r-docker-dev` 目录，将你的应用部署到 Kubernetes。

   ```console
   $ kubectl apply -f docker-r-kubernetes.yaml
   ```

   你应该看到类似以下的输出，表示你的 Kubernetes 对象已成功创建。

   ```text
   deployment.apps/docker-r-demo created
   service/service-entrypoint created
   ```

2. 通过列出你的部署来确保一切正常。

   ```console
   $ kubectl get deployments
   ```

   你的部署应该如下所示：

   ```shell
   NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
   docker-r-demo   1/1     1            1           15s
   ```

   这表示你在 YAML 中请求的所有 Pod 都已启动并运行。对你的服务也进行同样的检查。

   ```console
   $ kubectl get services
   ```

   你应该得到类似以下的输出。

   ```shell
   NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
   kubernetes           ClusterIP   10.96.0.1       <none>        443/TCP          23h
   service-entrypoint   NodePort    10.99.128.230   <none>        3838:30001/TCP   75s
   ```

   除了默认的 `kubernetes` 服务外，你还可以看到你的 `service-entrypoint` 服务，它接受 30001/TCP 端口的流量。

3. 在浏览器中访问以下地址。注意，在此示例中没有部署数据库。

   ```console
   http://localhost:30001/
   ```

4. 运行以下命令来拆除你的应用。

   ```console
   $ kubectl delete -f docker-r-kubernetes.yaml
   ```

## 总结

在本节中，你学习了如何使用 Docker Desktop 将你的应用部署到开发机器上的完整 Kubernetes 环境。

相关信息：

- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/use-desktop/kubernetes.md)
- [Swarm 模式概述](/manuals/engine/swarm/_index.md)
