---
title: 测试您的 PHP 部署
linkTitle: 测试您的部署
weight: 50
keywords: deploy, php, local, development
description: 了解如何部署您的应用程序
aliases:
  - /language/php/deploy/
  - /guides/language/php/deploy/
---

## 先决条件

- 完成本指南的所有先前部分，从 [容器化 PHP 应用程序](containerize.md) 开始。
- 在 Docker Desktop 中 [开启 Kubernetes](/manuals/desktop/use-desktop/kubernetes.md#enable-kubernetes)。

## 概述

在本节中，您将学习如何使用 Docker Desktop 将您的应用程序部署到开发机器上功能齐全的 Kubernetes 环境中。这允许您在部署之前在本地 Kubernetes 上测试和调试您的工作负载。

## 创建 Kubernetes YAML 文件

在您的 `docker-php-sample` 目录中，创建一个名为 `docker-php-kubernetes.yaml` 的文件。在 IDE 或文本编辑器中打开该文件，并添加以下内容。将 `DOCKER_USERNAME/REPO_NAME` 替换为您的 Docker 用户名和您在 [为您的 PHP 应用程序配置 CI/CD](configure-ci-cd.md) 中创建的仓库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-php-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      hello-php: web
  template:
    metadata:
      labels:
        hello-php: web
    spec:
      containers:
        - name: hello-site
          image: DOCKER_USERNAME/REPO_NAME
          imagePullPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: php-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    hello-php: web
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30001
```

在这个 Kubernetes YAML 文件中，有两个对象，由 `---` 分隔：

- 一个 Deployment，描述了一组可扩展的相同 Pod。在这种情况下，您将只获得一个副本或 Pod 的拷贝。该 Pod 在 `template` 下描述，其中只有一个容器。该容器由 GitHub Actions 在 [为您的 PHP 应用程序配置 CI/CD](configure-ci-cd.md) 中构建的镜像创建。
- 一个 NodePort 服务，它将主机上的端口 30001 的流量路由到它所路由到的 Pod 内部的端口 80，允许您从网络访问您的应用程序。

要了解更多关于 Kubernetes 对象的信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

## 部署并检查您的应用程序

1. 在终端中，导航到 `docker-php-sample` 目录，并将您的应用程序部署到 Kubernetes。

   ```console
   $ kubectl apply -f docker-php-kubernetes.yaml
   ```

   您应该会看到类似以下内容的输出，表明您的 Kubernetes 对象已成功创建。

   ```text
   deployment.apps/docker-php-demo created
   service/php-entrypoint created
   ```

2. 通过列出您的部署来确保一切正常。

   ```console
   $ kubectl get deployments
   ```

   您的部署应如下所示列出：

   ```text
   NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
   docker-php-demo      1/1     1            1           6s
   ```

   这表明所有的 Pod 都已启动并正在运行。对您的服务也进行同样的检查。

   ```console
   $ kubectl get services
   ```

   您应该会得到类似以下的输出。

   ```text
   NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP          7d22h
   php-entrypoint    NodePort    10.111.101.229   <none>        80:30001/TCP     33s
   ```

   除了默认的 `kubernetes` 服务外，您还可以看到您的 `php-entrypoint` 服务。`php-entrypoint` 服务正在端口 30001/TCP 上接收流量。

3. 打开浏览器并访问您的应用程序，地址为
   [http://localhost:30001/hello.php](http://localhost:30001/hello.php)。您
   应该会看到您的应用程序。

4. 运行以下命令以拆除您的应用程序。

   ```console
   $ kubectl delete -f docker-php-kubernetes.yaml
   ```

## 总结

在本节中，您学习了如何使用 Docker Desktop 将您的应用程序部署到开发机器上功能齐全的 Kubernetes 环境中。

相关信息：

- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/use-desktop/kubernetes.md)
- [Swarm 模式概述](/manuals/engine/swarm/_index.md)