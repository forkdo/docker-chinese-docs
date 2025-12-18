---
title: 测试你的 Bun 部署
linkTitle: 测试你的部署
weight: 50
keywords: deploy, kubernetes, bun
description: 了解如何使用 Kubernetes 在本地开发
aliases:
- /language/bun/deploy/
---

## 前置条件

- 完成本指南的所有前面章节，从 [容器化 Bun 应用](containerize.md) 开始。
- 在 Docker Desktop 中[启用 Kubernetes](/manuals//desktop/use-desktop/kubernetes.md#enable-kubernetes)。

## 概述

在本节中，你将学习如何使用 Docker Desktop 将你的应用部署到开发机器上的完整 Kubernetes 环境。这让你可以在本地对 Kubernetes 上的工作负载进行测试和调试，然后再部署到生产环境。

## 创建 Kubernetes YAML 文件

在你的 `bun-docker` 目录中，创建一个名为 `docker-kubernetes.yml` 的文件。在 IDE 或文本编辑器中打开该文件，添加以下内容。将 `DOCKER_USERNAME/REPO_NAME` 替换为你的 Docker 用户名和在 [为你的 Bun 应用配置 CI/CD](configure-ci-cd.md) 中创建的仓库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-bun-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: bun-api
  template:
    metadata:
      labels:
        app: bun-api
    spec:
      containers:
       - name: bun-api
         image: DOCKER_USERNAME/REPO_NAME
         imagePullPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: service-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    app: bun-api
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 30001
```

在这个 Kubernetes YAML 文件中，有两个对象，由 `---` 分隔：

 - 一个 Deployment，描述一组可扩展的相同 Pod。在本例中，你将只获得一个副本，即你的 Pod 的一个副本。在 `template` 下描述的该 Pod 只包含一个容器。该容器是从 GitHub Actions 在 [为你的 Bun 应用配置 CI/CD](configure-ci-cd.md) 中构建的镜像创建的。
 - 一个 NodePort 服务，它将把主机上的 30001 端口的流量路由到 Pod 内的 3000 端口，允许你从网络访问你的应用。

要了解有关 Kubernetes 对象的更多信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

## 部署并检查你的应用

1. 在终端中，导航到 `bun-docker` 目录，将你的应用部署到 Kubernetes。

   ```console
   $ kubectl apply -f docker-kubernetes.yml
   ```

   你应该看到类似以下的输出，表明你的 Kubernetes 对象已成功创建。

   ```text
   deployment.apps/docker-bun-demo created
   service/service-entrypoint created
   ```

2. 通过列出你的部署来确保一切正常。

   ```console
   $ kubectl get deployments
   ```

   你的部署应该如下所示：

   ```shell
   NAME                 READY   UP-TO-DATE   AVAILABLE    AGE
   docker-bun-demo       1/1     1            1           10s
   ```

   这表明你在 YAML 中请求的所有 Pod 都已启动并运行。对你的服务也进行同样的检查。

   ```console
   $ kubectl get services
   ```

   你应该得到类似以下的输出。

   ```shell
   NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   kubernetes           ClusterIP   10.96.0.1        <none>        443/TCP          88m
   service-entrypoint   NodePort    10.105.145.223   <none>        3000:30001/TCP   83s
   ```

   除了默认的 `kubernetes` 服务外，你还可以看到你的 `service-entrypoint` 服务，它在 30001/TCP 端口接收流量。

3. 在浏览器中访问以下地址。你应该看到消息 `{"Status" : "OK"}`。

   ```console
   http://localhost:30001/
   ```

4. 运行以下命令来拆除你的应用。

   ```console
   $ kubectl delete -f docker-kubernetes.yml
   ```

## 总结

在本节中，你学习了如何使用 Docker Desktop 将你的 Bun 应用部署到开发机器上的完整 Kubernetes 环境。

相关信息：
   - [Kubernetes 文档](https://kubernetes.io/docs/home/)
   - [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/use-desktop/kubernetes.md)
   - [Swarm 模式概述](/manuals/engine/swarm/_index.md)