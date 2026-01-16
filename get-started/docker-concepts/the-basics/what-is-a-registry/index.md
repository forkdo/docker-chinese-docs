---
title: 什么是镜像仓库？
url: /get-started/docker-concepts/the-basics/what-is-a-registry/
parent:
  title: 开始使用
  url: /get-started/
breadcrumbs:
  - title: 开始使用
    url: /get-started/
  - title: 什么是镜像仓库？
    url: /get-started/docker-concepts/the-basics/what-is-a-registry/
next:
  title: 什么是镜像？
  url: /get-started/docker-concepts/the-basics/what-is-an-image/
prev:
  title: 什么是 Docker Compose？
  url: /get-started/docker-concepts/the-basics/what-is-docker-compose/
---




## 说明

现在您已经了解了容器镜像的定义及其工作原理，可能会产生疑问：这些镜像存储在哪里？

您可以将容器镜像存储在本地计算机系统中，但如果想要与朋友共享镜像或在其他机器上使用镜像，该怎么办？这时就需要使用镜像仓库。

镜像仓库是用于存储和共享容器镜像的集中化位置。它可以是公共的，也可以是私有的。[Docker Hub](https://hub.docker.com) 是一个任何人都可以使用的公共镜像仓库，也是默认的镜像仓库。

虽然 Docker Hub 是一个流行的选择，但如今还有许多其他可用的容器镜像仓库，包括 [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/)、[Azure Container Registry (ACR)](https://azure.microsoft.com/en-in/products/container-registry) 和 [Google Container Registry (GCR)](https://cloud.google.com/artifact-registry)。您甚至可以在本地系统或组织内部运行私有镜像仓库。例如 Harbor、JFrog Artifactory、GitLab Container Registry 等。

### 镜像仓库 vs. 镜像仓库

在使用镜像仓库时，您可能会听到 _registry_ 和 _repository_ 这两个术语，它们看起来可以互换使用。尽管两者相关，但它们并不完全相同。

_镜像仓库_ 是存储和管理容器镜像的集中化位置，而 _镜像仓库_ 是镜像仓库中一组相关的容器镜像。可以将其想象为一个文件夹，您根据项目在其中组织镜像。每个镜像仓库包含一个或多个容器镜像。

下图展示了镜像仓库、镜像仓库和镜像之间的关系。

```goat {class="text-sm"}
+---------------------------------------+
|               Registry                |
|---------------------------------------|
|                                       |
|    +-----------------------------+    |
|    |        Repository A         |    |
|    |-----------------------------|    |
|    |   Image: project-a:v1.0     |    |
|    |   Image: project-a:v2.0     |    |
|    +-----------------------------+    |
|                                       |
|    +-----------------------------+    |
|    |        Repository B         |    |
|    |-----------------------------|    |
|    |   Image: project-b:v1.0     |    |
|    |   Image: project-b:v1.1     |    |
|    |   Image: project-b:v2.0     |    |
|    +-----------------------------+    |
|                                       |
+---------------------------------------+
```

> [!NOTE]
>
> 您可以使用 Docker Hub 的免费版本创建一个私有镜像仓库和无限数量的公共镜像仓库。更多信息请访问 [Docker Hub 订阅页面](https://www.docker.com/pricing/)。

## 动手实践

在本动手实践中，您将学习如何构建 Docker 镜像并将其推送到 Docker Hub 镜像仓库。

### 注册免费的 Docker 账户

1. 如果尚未创建账户，请访问 [Docker Hub](https://hub.docker.com) 页面注册新的 Docker 账户。

    ![Docker Hub 官方页面截图，显示注册页面](images/dockerhub-signup.webp?border)

    您可以使用 Google 或 GitHub 账户进行身份验证。

### 创建您的第一个镜像仓库

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 点击右上角的 **Create repository** 按钮。
3. 选择您的命名空间（很可能是您的用户名），并将镜像仓库名称设置为 `docker-quickstart`。

    ![Docker Hub 页面截图，显示如何创建公共镜像仓库](images/create-hub-repository.webp?border)

4. 将可见性设置为 **Public**。
5. 点击 **Create** 按钮创建镜像仓库。

就是这样。您已成功创建第一个镜像仓库。🎉

目前该镜像仓库为空。接下来，您将通过推送镜像来填充它。

### 使用 Docker Desktop 登录

1. 如果尚未安装，请 [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。
2. 在 Docker Desktop 图形界面中，点击右上角的 **Sign in** 按钮。

### 克隆示例 Node.js 代码

要创建镜像，首先需要一个项目。为了帮助您快速开始，您将使用位于 [github.com/dockersamples/helloworld-demo-node](https://github.com/dockersamples/helloworld-demo-node) 的示例 Node.js 项目。该仓库包含一个预构建的 Dockerfile，用于构建 Docker 镜像。

不用担心 Dockerfile 的具体细节，您将在后续章节中学习相关内容。

1. 使用以下命令克隆 GitHub 仓库：

    ```console
    git clone https://github.com/dockersamples/helloworld-demo-node
    ```

2. 进入新创建的目录。

    ```console
    cd helloworld-demo-node
    ```

3. 运行以下命令构建 Docker 镜像，将 `YOUR_DOCKER_USERNAME` 替换为您的用户名。

    ```console
    docker build -t <YOUR_DOCKER_USERNAME>/docker-quickstart .
    ```

    > [!NOTE]
    >
    > 确保在 `docker build` 命令末尾包含点号 (.)。这告诉 Docker 在哪里查找 Dockerfile。

4. 运行以下命令列出新创建的 Docker 镜像：

    ```console
    docker images
    ```

    您将看到类似以下的输出：

    ```console
    REPOSITORY                                 TAG       IMAGE ID       CREATED         SIZE
    <YOUR_DOCKER_USERNAME>/docker-quickstart   latest    476de364f70e   2 minutes ago   170MB
    ```

5. 启动容器以测试镜像，运行以下命令（将用户名替换为您自己的用户名）：

    ```console
    docker run -d -p 8080:8080 <YOUR_DOCKER_USERNAME>/docker-quickstart 
    ```

    您可以通过浏览器访问 [http://localhost:8080](http://localhost:8080) 来验证容器是否正常工作。

6. 使用 [`docker tag`](/reference/cli/docker/image/tag/) 命令为 Docker 镜像打标签。Docker 标签允许您为镜像添加标签和版本。

    ```console 
    docker tag <YOUR_DOCKER_USERNAME>/docker-quickstart <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0 
    ```

7. 最后，使用 [`docker push`](/reference/cli/docker/image/push/) 命令将新构建的镜像推送到您的 Docker Hub 镜像仓库：

    ```console 
    docker push <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0
    ```

8. 打开 [Docker Hub](https://hub.docker.com) 并导航到您的镜像仓库。进入 **Tags** 部分，查看新推送的镜像。

    ![Docker Hub 页面截图，显示新添加的镜像标签](images/dockerhub-tags.webp?border=true) 

在本实践指南中，您注册了 Docker 账户，创建了第一个 Docker Hub 镜像仓库，并构建、标记和推送了容器镜像到您的 Docker Hub 镜像仓库。

## 其他资源

- [Docker Hub 快速入门](/docker-hub/quickstart/)
- [管理 Docker Hub 镜像仓库](/docker-hub/repos/)

## 下一步

现在您已经理解了容器和镜像的基础知识，可以开始学习 Docker Compose。

[什么是 Docker Compose？](what-is-Docker-Compose)

