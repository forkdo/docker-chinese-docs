---
title: 测试你的 PHP 部署
linkTitle: 测试你的部署
weight: 50
keywords: 部署, php, 本地, 开发
description: 学习如何部署你的应用程序
aliases:
  - /language/php/deploy/
  - /guides/language/php/deploy/
---

## 前置条件

- 完成本指南之前的所有章节，从 [容器化 PHP 应用](containerize.md) 开始。
- 在 Docker Desktop 中[启用 Kubernetes](/manuals/desktop/use-desktop/kubernetes.md#enable-kubernetes)。

## 概述

在本节中，你将学习如何使用 Docker Desktop 将你的应用程序部署到开发机器上的完整 Kubernetes 环境中。这让你可以在本地测试和调试工作负载，然后再部署到生产环境。

## 创建 Kubernetes YAML 文件

在你的 `docker-php-sample` 目录中，创建一个名为 `docker-php-kubernetes.yaml` 的文件。在 IDE 或文本编辑器中打开该文件，并添加以下内容。将 `DOCKER_USERNAME/REPO_NAME` 替换为你的 Docker 用户名和在 [为你的 PHP 应用配置 CI/CD](configure-ci-cd.md) 中创建的仓库名称。

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

在这个 Kubernetes YAML 文件中，有两个对象，用 `---` 分隔：

- 一个 Deployment，描述一组可扩展的相同 Pod。在本例中，你将只获得一个副本，也就是你的 Pod 的一个副本。这个 Pod 在 `template` 下描述，其中只有一个容器。该容器是从 GitHub Actions 在 [为你的 PHP 应用配置 CI/CD](configure-ci-cd.md) 中构建的镜像创建的。
- 一个 NodePort 服务，它将把主机上的 30001 端口的流量路由到 Pod 内部的 80 端口，允许你从网络访问你的应用。

要了解更多信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

## 部署并检查你的应用

1. 在终端中，导航到 `docker-php-sample` 目录并部署你的应用到 Kubernetes。

   ```console
   $ kubectl apply -f docker-php-kubernetes.yaml
   ```

   你应该看到类似以下的输出，表明你的 Kubernetes 对象已成功创建。

   ```text
   deployment.apps/docker-php-demo created
   service/php-entrypoint created
   ```

2. 通过列出你的部署来确保一切正常。

   ```console
   $ kubectl get deployments
   ```

   你的部署应该如下所示：

   ```text
   NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
   docker-php-demo      1/1     1            1           6s
   ```

   这表明所有 Pod 都已启动并运行。对你的服务也进行同样的检查。

   ```console
   $ kubectl get services
   ```

   你应该得到类似以下的输出。

   ```text
   NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP          7d22h
   php-entrypoint    NodePort    10.111.101.229   <none>        80:30001/TCP     33s
   ```

   除了默认的 `kubernetes` 服务外，你还可以看到你的 `php-entrypoint` 服务。`php-entrypoint` 服务正在 30001/TCP 端口上接受流量。

3. 打开浏览器并访问 [http://localhost:30001/hello.php](http://localhost:30001/hello.php) 上的应用。你应该能看到你的应用。

4. 运行以下命令来拆除你的应用。

   ```console
   $ kubectl delete -f docker-php-kubernetes.yaml
   ```

## 总结

在本节中，你学习了如何使用 Docker Desktop 将你的应用部署到开发机器上的完整 Kubernetes 环境中。

相关信息：

- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/use-desktop/kubernetes.md)
- [Swarm 模式概述](/manuals/engine/swarm/_index.md)