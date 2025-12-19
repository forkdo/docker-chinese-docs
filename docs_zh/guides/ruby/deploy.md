---
title: 测试您的 Ruby on Rails 部署
linkTitle: 测试您的部署
weight: 50
keywords: 部署, kubernetes, ruby
description: 了解如何使用 Kubernetes 进行本地开发
aliases:
  - /language/ruby/deploy/
  - /guides/language/ruby/deploy/
---

## 前提条件

- 完成本指南之前的所有部分，从 [容器化 Ruby on Rails 应用程序](containerize.md) 开始。
- 在 Docker Desktop 中 [开启 Kubernetes](/manuals/desktop/use-desktop/kubernetes.md#enable-kubernetes)。

## 概述

在本节中，您将学习如何使用 Docker Desktop 将应用程序部署到开发机器上功能齐全的 Kubernetes 环境。这样您就可以在部署到生产环境之前，在本地测试和调试您在 Kubernetes 上的工作负载。

## 创建 Kubernetes YAML 文件

在您的 `docker-ruby-on-rails` 目录中，创建一个名为
`docker-ruby-on-rails-kubernetes.yaml` 的文件。在 IDE 或文本编辑器中打开该文件并添加
以下内容。将 `DOCKER_USERNAME/REPO_NAME` 替换为您的 Docker
用户名和您在 [为您的 Ruby on Rails 应用程序配置 CI/CD](configure-github-actions.md) 中创建的仓库名称。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-ruby-on-rails-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: ruby-on-rails
  template:
    metadata:
      labels:
        service: ruby-on-rails
    spec:
      containers:
        - name: ruby-on-rails-container
          image: DOCKER_USERNAME/REPO_NAME
          imagePullPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: docker-ruby-on-rails-demo
  namespace: default
spec:
  type: NodePort
  selector:
    service: ruby-on-rails
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30001
```

在这个 Kubernetes YAML 文件中，有两个对象，由 `---` 分隔：

- 一个 Deployment，描述一组可扩展的相同 Pod。在本例中，
  您将只得到一个副本，或您 Pod 的一个拷贝。该 Pod 在 `template` 下描述，
  其中只有一个容器。该容器是由 GitHub Actions 在 [为您的 Ruby on Rails 应用程序配置 CI/CD](configure-github-actions.md) 中构建的镜像创建的。
- 一个 NodePort 服务，它将来自您主机上端口 30001 的流量路由到
  它所指向的 Pod 内部的端口 8001，从而允许您通过网络访问您的应用程序。

要了解更多关于 Kubernetes 对象的信息，请参阅 [Kubernetes 文档](https://kubernetes.io/docs/home/)。

## 部署并检查您的应用程序

1.  在终端中，导航到 `docker-ruby-on-rails` 并将您的应用程序部署到
    Kubernetes。

    ```console
    $ kubectl apply -f docker-ruby-on-rails-kubernetes.yaml
    ```

    您应该会看到如下输出，表明您的 Kubernetes 对象已成功创建。

    ```shell
    deployment.apps/docker-ruby-on-rails-demo created
    service/docker-ruby-on-rails-demo created
    ```

2.  通过列出您的部署来确保一切正常工作。

    ```console
    $ kubectl get deployments
    ```

    您的部署应如下所示列出：

    ```shell
    NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
    docker-ruby-on-rails-demo  1/1     1            1           15s
    ```

    这表明您在 YAML 中请求的所有 Pod（在此例中为一个）都已启动并正在运行。对您的服务执行相同的检查。

    ```console
    $ kubectl get services
    ```

    您应该会得到类似以下的输出。

    ```shell
    NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
    kubernetes                  ClusterIP   10.96.0.1       <none>        443/TCP          23h
    docker-ruby-on-rails-demo   NodePort    10.99.128.230   <none>        3000:30001/TCP   75s
    ```

    除了默认的 `kubernetes` 服务外，您还可以看到您的 `docker-ruby-on-rails-demo` 服务，它正在端口 30001/TCP 上接受流量。

3.  要在运行于 Kubernetes 上的 Ruby on Rails 应用程序中创建并迁移数据库，您需要遵循以下步骤。

    **获取当前的 Pods**：
    首先，您需要识别在 Kubernetes 集群中运行的 Pod。执行以下命令以列出 `default` 命名空间中的当前 Pod：

    ```sh
    # 获取集群中 default 命名空间下的当前 Pod
    $ kubectl get pods
    ```

    该命令将显示 `default` 命名空间中所有 Pod 的列表。查找以 `docker-ruby-on-rails-demo-` 为前缀的 Pod。这是一个示例输出：

    ```console
    NAME                                         READY   STATUS    RESTARTS      AGE
    docker-ruby-on-rails-demo-7cbddb5d6f-qh44l   1/1     Running   2 (22h ago)   9d
    ```

    **执行迁移命令**：
    识别出正确的 Pod 后，使用 `kubectl exec` 命令在 Pod 内部运行数据库迁移。

    ```sh
    $ kubectl exec -it docker-ruby-on-rails-demo-7cbddb5d6f-qh44l -- rails db:migrate RAILS_ENV=development
    ```

    此命令会在指定的 Pod 中打开一个交互式终端会话 (`-it`)，并以环境设置为 development (`RAILS_ENV=development`) 来运行 `rails db:migrate` 命令。

    通过遵循这些步骤，您可以确保在 Kubernetes 集群中运行的 Ruby on Rails 应用程序内的数据库被正确迁移。此过程有助于在部署和更新期间维护应用程序数据结构的完整性和一致性。

4.  打开浏览器并访问 [http://localhost:30001](http://localhost:30001)，您应该能看到 ruby on rails 应用程序正在运行。

5.  运行以下命令来销毁您的应用程序。

    ```console
    $ kubectl delete -f docker-ruby-on-rails-kubernetes.yaml
    ```

## 总结

在本节中，您学习了如何使用 Docker Desktop 将应用程序部署到开发机器上功能齐全的 Kubernetes 环境。

相关信息：

- [Kubernetes 文档](https://kubernetes.io/docs/home/)
- [使用 Docker Desktop 在 Kubernetes 上部署](/manuals/desktop/use-desktop/kubernetes.md)
- [Swarm 模式概述](/manuals/engine/swarm/_index.md)