---
title: 什么是注册表？
weight: 30
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 什么是注册表？本文档将解释注册表的概念，探讨其互操作性，并指导你与注册表交互。
aliases:
- /guides/walkthroughs/run-hub-images/
- /guides/walkthroughs/publish-your-image/
- /guides/docker-concepts/the-basics/what-is-a-registry/
---

{{< youtube-embed 2WDl10Wv5rs >}}

## 解释

现在你已经了解了容器镜像的概念及其工作原理，你可能会想——这些镜像应该存储在哪里？

你可以将容器镜像存储在本地计算机上，但如果你想与朋友共享，或在其他机器上使用，该怎么办？这时就需要用到镜像注册表（registry）。

镜像注册表是一个集中存储和共享容器镜像的地方，可以是公开的，也可以是私有的。[Docker Hub](https://hub.docker.com) 是一个任何人都可以使用的公共注册表，也是默认的注册表。

虽然 Docker Hub 是一个流行的选择，但如今还有许多其他可用的容器注册表，包括 [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/)、[Azure Container Registry (ACR)](https://azure.microsoft.com/en-in/products/container-registry) 和 [Google Container Registry (GCR)](https://cloud.google.com/artifact-registry)。你甚至可以在本地系统或组织内部运行自己的私有注册表，例如 Harbor、JFrog Artifactory、GitLab 容器注册表等。

### 注册表 vs 仓库

在使用注册表时，你可能会听到“注册表”（registry）和“仓库”（repository）这两个术语被当作同义词使用。尽管它们相关，但并不完全相同。

**注册表** 是集中存储和管理容器镜像的位置，而 **仓库** 是注册表中相关容器镜像的集合。可以将其理解为按项目组织镜像的文件夹。每个仓库包含一个或多个容器镜像。

下图展示了注册表、仓库和镜像之间的关系。

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
> 使用 Docker Hub 的免费版本，你可以创建一个私有仓库和无限数量的公共仓库。更多信息请访问 [Docker Hub 订阅页面](https://www.docker.com/pricing/)。

## 动手实践

在本实践环节中，你将学习如何构建 Docker 镜像并将其推送到 Docker Hub 仓库。

### 注册免费的 Docker 账户

1. 如果你还没有账户，前往 [Docker Hub](https://hub.docker.com) 页面注册新账户。

    ![Docker Hub 官方页面的注册页面截图](images/dockerhub-signup.webp?border)

    你可以使用 Google 或 GitHub 账户进行认证。

### 创建你的第一个仓库

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 点击右上角的 **Create repository**（创建仓库）按钮。
3. 选择命名空间（通常是你的用户名），并将仓库名称设置为 `docker-quickstart`。

    ![Docker Hub 页面创建公共仓库的截图](images/create-hub-repository.webp?border)

4. 将可见性设置为 **Public**（公开）。
5. 点击 **Create**（创建）按钮创建仓库。

搞定！你已成功创建了第一个仓库。🎉

目前这个仓库是空的。接下来，你将通过推送镜像来解决这个问题。

### 使用 Docker Desktop 登录

1. 如果尚未安装，请[下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。
2. 在 Docker Desktop GUI 中，点击右上角的 **Sign in**（登录）按钮。

### 克隆示例 Node.js 代码

要创建镜像，首先需要一个项目。为了快速开始，你将使用 [github.com/dockersamples/helloworld-demo-node](https://github.com/dockersamples/helloworld-demo-node) 中的示例 Node.js 项目。该仓库包含构建 Docker 镜像所需的预构建 Dockerfile。

暂时不需要深入了解 Dockerfile 的具体细节，你将在后续章节中学习相关内容。

1. 使用以下命令克隆 GitHub 仓库：

    ```console
    git clone https://github.com/dockersamples/helloworld-demo-node
    ```

2. 进入新创建的目录：

    ```console
    cd helloworld-demo-node
    ```

3. 运行以下命令构建 Docker 镜像，将 `<YOUR_DOCKER_USERNAME>` 替换为你的用户名：

    ```console
    docker build -t <YOUR_DOCKER_USERNAME>/docker-quickstart .
    ```

    > [!NOTE]
    >
    > 确保 `docker build` 命令末尾包含点（.），这告诉 Docker 在哪里查找 Dockerfile。

4. 运行以下命令列出新创建的 Docker 镜像：

    ```console
    docker images
    ```

    你会看到类似以下的输出：

    ```console
    REPOSITORY                                 TAG       IMAGE ID       CREATED         SIZE
    <YOUR_DOCKER_USERNAME>/docker-quickstart   latest    476de364f70e   2 minutes ago   170MB
    ```

5. 运行以下命令启动容器以测试镜像（将用户名替换为你的用户名）：

    ```console
    docker run -d -p 8080:8080 <YOUR_DOCKER_USERNAME>/docker-quickstart 
    ```

    你可以在浏览器中访问 [http://localhost:8080](http://localhost:8080) 来验证容器是否正常工作。

6. 使用 [`docker tag`](/reference/cli/docker/image/tag/) 命令为 Docker 镜像打标签。Docker 标签允许你为镜像添加标签和版本：

    ```console 
    docker tag <YOUR_DOCKER_USERNAME>/docker-quickstart <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0 
    ```

7. 最后，使用 [`docker push`](/reference/cli/docker/image/push/) 命令将新构建的镜像推送到 Docker Hub 仓库：

    ```console 
    docker push <YOUR_DOCKER_USERNAME>/docker-quickstart:1.0
    ```

8. 打开 [Docker Hub](https://hub.docker.com) 并导航到你的仓库。进入 **Tags**（标签）部分，查看你刚推送的镜像。

    ![Docker Hub 页面显示新添加镜像标签的截图](images/dockerhub-tags.webp?border=true) 

在本次实践环节中，你注册了 Docker 账户，创建了第一个 Docker Hub 仓库，并构建、打标签和推送了容器镜像到你的 Docker Hub 仓库。

## 额外资源

- [Docker Hub 快速入门](/docker-hub/quickstart/)
- [管理 Docker Hub 仓库](/docker-hub/repos/)

## 下一步

现在你已经了解了容器和镜像的基础知识，接下来可以学习 Docker Compose。

{{< button text="什么是 Docker Compose？" url="what-is-Docker-Compose" >}}
