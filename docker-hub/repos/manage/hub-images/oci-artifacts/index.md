# Docker Hub 上的软件制品

您可以使用 Docker Hub 存储任何类型的软件制品，而不仅仅是容器镜像。软件制品是指在软件开发过程中产生的、有助于软件创建、维护或理解的任何项目。Docker Hub 通过利用镜像清单 (image manifest) 中的 config 属性来支持 OCI 制品。

## 什么是 OCI 制品？

OCI 制品是与软件应用程序相关的任何文件。一些示例包括：

- Helm charts
- 软件物料清单
- 数字签名
- 来源数据
- 证明
- 漏洞报告

Docker Hub 支持 OCI 制品意味着您可以使用一个仓库来存储和分发容器镜像以及其他资产。

OCI 制品的一个常见用例是 [Helm charts](https://helm.sh/docs/topics/charts/)。Helm charts 是一种打包格式，用于为应用程序定义 Kubernetes 部署。由于 Kubernetes 是一种流行的容器运行时，因此将应用程序镜像和部署模板都托管在一个地方是合理的。

## 在 Docker Hub 中使用 OCI 制品

您管理 Docker Hub 上的 OCI 制品的方式与管理容器镜像的方式类似。

向仓库推送和从仓库拉取 OCI 制品是通过仓库客户端 完成的。[ORAS CLI](https://oras.land/docs/installation) 是一个命令行工具，提供了在仓库中管理 OCI 制品的功能。如果您使用 Helm charts，[Helm CLI](https://helm.sh/docs/intro/install/) 提供了内置功能，用于向仓库推送和从仓库拉取 chart。

仓库客户端会向 Docker Hub 仓库 API 发起 HTTP 请求。该仓库 API 符合 [OCI 分发规范](https://github.com/opencontainers/distribution-spec) 中定义的标准协议。

## 示例

本节介绍了一些在 Docker Hub 中使用 OCI 制品的示例。

### 推送 Helm chart

以下过程展示了如何将 Helm chart 作为 OCI 制品推送到 Docker Hub。

先决条件：

- Helm 3.0.0 或更高版本

步骤：

1. 创建一个新的 Helm chart

   ```console
   $ helm create demo
   ```

   此命令会生成一个样板模板 chart。

2. 将 Helm chart 打包成一个 tar 包。

   ```console
   $ helm package demo
   Successfully packaged chart and saved it to: /Users/hubuser/demo-0.1.0.tgz
   ```

3. 使用您的 Docker 凭证通过 Helm 登录 Docker Hub。

   ```console
   $ helm registry login registry-1.docker.io -u hubuser
   ```

4. 将 chart 推送到 Docker Hub 仓库。

   ```console
   $ helm push demo-0.1.0.tgz oci://registry-1.docker.io/docker
   ```

   这会将 Helm chart tar 包上传到 `docker` 命名空间下的 `demo` 仓库中。

5. 转到 Docker Hub 上的仓库页面。页面的 **Tags** 部分会显示 Helm chart 标签。

   ![仓库标签列表](./images/oci-helm.png)

6. 选择标签名称以转到该标签的页面。

   该页面列出了一些用于处理 Helm charts 的有用命令。

   ![Helm chart 制品的标签页面](./images/oci-helm-tagview.png)

### 推送卷

以下过程展示了如何将容器卷作为 OCI 制品推送到 Docker Hub。

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

   这会将卷上传到 `docker` 命名空间下的 `demo` 仓库中。`--artifact-type` 标志指定了一种特殊的媒体类型，使 Docker Hub 将该制品识别为容器卷。

4. 转到 Docker Hub 上的仓库页面。该页面上的 **Tags** 部分会显示卷标签。

   ![仓库页面显示标签列表中的一个卷](./images/oci-volume.png)

### 推送通用制品文件

以下过程展示了如何将通用 OCI 制品推送到 Docker Hub。

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

4. 转到 Docker Hub 上的仓库页面。该页面上的 **Tags** 部分会显示制品标签。

   ![仓库页面显示标签列表中的一个制品](./images/oci-artifact.png)
