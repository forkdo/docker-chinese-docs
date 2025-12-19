---
title: 测试你的 Java 部署
linkTitle: 测试你的部署
weight: 50
keywords: deploy, kubernetes, java
description: 学习如何在本地使用 Kubernetes 进行开发
aliases:
  - /language/java/deploy/
  - /guides/language/java/deploy/
---

## 前提条件

- 完成本指南的所有先前部分，从[容器化你的应用](containerize.md)开始。
- 在 Docker Desktop 中[开启 Kubernetes](/manuals/desktop/use-desktop/kubernetes.md#enable-kubernetes)。

## 概述

在本节中，你将学习如何使用 Docker Desktop 将你的应用部署到开发机器上功能齐全的 Kubernetes 环境中。这让你可以在部署之前，在本地 Kubernetes 环境中测试和调试你的工作负载。

## 创建 Kubernetes YAML 文件

在你的 `spring-petclinic` 目录中，创建一个名为 `docker-java-kubernetes.yaml` 的文件。在 IDE 或文本编辑器中打开该文件，并添加以下内容。将 `DOCKER_USERNAME/REPO_NAME` 替换为你的 Docker 用户名和你在[为你的 Java 应用配置 CI/CD](configure-ci-cd.md) 中创建的仓库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-java-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: server
  template:
    metadata:
      labels:
        service: server
    spec:
      containers:
        - name: server-service
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
    service: server
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30001
```

在这个 Kubernetes YAML 文件中，有两个对象，由 `---` 分隔：

- 一个 Deployment，描述了一组可扩展的相同 Pod。在这种情况下，你将只获得一个副本（replica），即你的 Pod 的一个拷贝。该 Pod 在 `template` 下描述，其中只有一个容器。该容器由 GitHub Actions 在[为你的 Java 应用配置 CI/CD](configure-ci-cd.md) 中构建的镜像创建。
- 一个 NodePort 服务，它将主机上 30001 端口的流量路由到它所路由到的 Pod 内部的 8080 端口，允许你从网络访问你的应用。

要了解更多关于 Kubernetes 对象的信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

## 部署并检查你的应用

1. 在终端中，导航到 `spring-petclinic` 并将你的应用部署到 Kubernetes。

   ```console
   $ kubectl apply -f docker-java-kubernetes.yaml
   ```

   你应该会看到类似以下内容的输出，表明你的 Kubernetes 对象已成功创建。

   ```shell
   deployment.apps/docker-java-demo created
   service/service-entrypoint created
   ```

2. 通过列出你的部署来确保一切正常。

   ```console
   $ kubectl get deployments
   ```

   你的部署应如下所示列出：

   ```shell
   NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
   docker-java-demo     1/1     1            1           15s
   ```

   这表明你在 YAML 中请求的所有 Pod 都已启动并运行。对你的服务执行同样的检查。

   ```console
   $ kubectl get services
   ```

   你应该会得到类似以下的输出。

   ```shell
   NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
   kubernetes           ClusterIP   10.96.0.1       <none>        443/TCP          23h
   service-entrypoint   NodePort    10.99.128.230   <none>        8080:30001/TCP   75s
   ```

   除了默认的 `kubernetes` 服务，你还可以看到你的 `service-entrypoint` 服务，它在端口 30001/TCP 上接收流量。

3. 在终端中，使用 curl 访问该服务。请注意，此示例中未部署数据库。

   ```console
   $ curl --request GET \
     --url http://localhost:30001/actuator/health \
     --header 'content-type: application/json'
   ```

   你应该会得到类似以下的输出。

   ```console
   {"status":"UP","groups":["liveness","readiness"]}
   ```

4. 运行以下命令以拆除你的应用。

   ```console
   $ kubectl delete -f docker-java-kubernetes.yaml
   ```

## 总结

在本节中，你学习了如何使用 Docker Desktop 将你的应用部署到开发机器上功能齐全的 Kubernetes 环境中。

相关信息：

- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/use-desktop/kubernetes.md)
- [Swarm 模式概述](/manuals/engine/swarm/_index.md)