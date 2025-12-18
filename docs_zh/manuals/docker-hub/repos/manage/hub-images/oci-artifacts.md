---
title: Docker Hub 上的软件制品
linkTitle: 软件制品
weight: 20
keywords: oci, 制品, docker hub
description: 您可以使用 Docker Hub 存储打包为 OCI 制品的任何软件制品。
aliases:
- /docker-hub/oci-artifacts/
---

您可以使用 Docker Hub 存储各种软件制品，而不仅仅是容器镜像。软件制品是指软件开发过程中产生的任何有助于软件创建、维护或理解的项目。Docker Hub 通过利用镜像清单中的 config 属性来支持 OCI 制品。

## 什么是 OCI 制品？

OCI 制品是与软件应用程序相关的任何任意文件。一些示例包括：

- Helm 图表
- 软件物料清单 (SBOM)
- 数字签名
- 来源数据
- 证明
- 漏洞报告

Docker Hub 支持 OCI 制品意味着您可以在一个仓库中存储和分发容器镜像以及其他资产。

OCI 制品的一个常见用例是 [Helm 图表](https://helm.sh/docs/topics/charts/)。Helm 图表是一种定义应用程序在 Kubernetes 上部署的打包格式。由于 Kubernetes 是容器的流行运行时，因此将应用程序镜像和部署模板存储在同一位置是合理的。

## 在 Docker Hub 上使用 OCI 制品

您可以通过类似管理容器镜像的方式来管理 Docker Hub 上的 OCI 制品。

推送和拉取 OCI 制品到/从注册表是通过注册表客户端完成的。[ORAS CLI](https://oras.land/docs/installation) 是一个命令行工具，提供在注册表中管理 OCI 制品的功能。如果您使用 Helm 图表，[Helm CLI](https://helm.sh/docs/intro/install/) 提供了将图表推送到注册表和从注册表拉取的内置功能。

注册表客户端向 Docker Hub 注册表 API 发出 HTTP 请求。注册表 API 符合 [OCI 分发规范](https://github.com/opencontainers/distribution-spec) 中定义的标准协议。

## 示例

本节展示一些在 Docker Hub 上使用 OCI 制品的示例。

### 推送 Helm 图表

以下过程展示如何将 Helm 图表作为 OCI 制品推送到 Docker Hub。

先决条件：

- Helm 3.0.0 或更高版本

步骤：

1. 创建一个新的 Helm 图表

   ```console
   $ helm create demo
   ```

   此命令生成一个样板模板图表。

2. 将 Helm 图表打包为 tarball。

   ```console
   $ helm package demo
   Successfully packaged chart and saved it to: /Users/hubuser/demo-0.1.0.tgz
   ```

3. 使用您的 Docker 凭据登录 Docker Hub。

   ```console
   $ helm registry login registry-1.docker.io -u hubuser
   ```

4. 将图表推送到 Docker Hub 仓库。

   ```console
   $ helm push demo-0.1.0.tgz oci://registry-1.docker.io/docker
   ```

   这会将 Helm 图表 tarball 上传到 `docker` 命名空间中的 `demo` 仓库。

5. 访问 Docker Hub 上的仓库页面。页面的 **Tags** 部分显示 Helm 图表标签。

   ![仓库标签列表](./images/oci-helm.png)

6. 选择标签名称以进入该标签的页面。

   页面列出了一些处理 Helm 图表的有用命令。

   ![Helm 图表制品的标签页面](./images/oci-helm-tagview.png)

### 推送卷

以下过程展示如何将容器卷作为 OCI 制品推送到 Docker Hub。

先决条件：

- ORAS CLI 0.15 或更高版本

步骤：

1. 创建一个虚拟文件用作卷内容。

   ```console
   $ touch myvolume.txt
   ```

2. 使用 ORAS CLI 登录 Docker Hub。

   ```console
   $ oras login -u hubuser registry-1.docker.io
   ```

3. 将文件推送到 Docker Hub。

   ```console
   $ oras push registry-1.docker.io/docker/demo:0.0.1 \
     --artifact-type=application/vnd.docker.volume.v1+tar.gz \
     myvolume.txt:text/plain
   ```

   这会将卷上传到 `docker` 命名空间中的 `demo` 仓库。`--artifact-type` 标志指定一种特殊媒体类型，使 Docker Hub 将该制品识别为容器卷。

4. 访问 Docker Hub 上的仓库页面。页面的 **Tags** 部分显示卷标签。

   ![仓库页面在标签列表中显示卷](./images/oci-volume.png)

### 推送通用制品文件

以下过程展示如何将通用 OCI 制品推送到 Docker Hub。

先决条件：

- ORAS CLI 0.15 或更高版本

步骤：

1. 创建您的制品文件。

   ```console
   $ touch myartifact.txt
   ```

2. 使用 ORAS CLI 登录 Docker Hub。

   ```console
   $ oras login -u hubuser registry-1.docker.io
   ```

3. 将文件推送到 Docker Hub。

   ```console
   $ oras push registry-1.docker.io/docker/demo:0.0.1 myartifact.txt:text/plain
   ```

4. 访问 Docker Hub 上的仓库页面。页面的 **Tags** 部分显示制品标签。

   ![仓库页面在标签列表中显示制品](./images/oci-artifact.png)