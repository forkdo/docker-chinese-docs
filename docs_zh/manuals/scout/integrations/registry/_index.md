---
build:
  render: never
title: 容器镜像仓库
---

# Container registries

A container registry is a storage and distribution system for named Docker images. Those images can be tagged and pushed to the registry by users, and then pulled by Docker clients.

# 容器镜像仓库

容器镜像仓库是用于存储和分发已命名 Docker 镜像的系统。用户可以为这些镜像打上标签并推送到镜像仓库，然后由 Docker 客户端拉取。

## Official registries

The following registries are officially supported by Docker:

## 官方镜像仓库

Docker 官方支持以下镜像仓库：

| Registry                                                                 | Description                                                                                                      |
| :----------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- |
| [Docker Hub](https://hub.docker.com/)                                    | The default global registry.                                                                                     |
| [Docker Trusted Registry (DTR)](https://www.docker.com/products/docker-trusted-registry) | A commercial registry that can be installed on-premises.                                                         |
| [Amazon EC2 Container Registry (ECR)](https://aws.amazon.com/ecr/)       | A private registry service provided by Amazon Web Services (AWS).                                                |
| [Google Container Registry (GCR)](https://cloud.google.com/container-registry/) | A private registry service provided by Google Cloud Platform (GCP).                                              |
| [Azure Container Registry (ACR)](https://azure.microsoft.com/en-us/services/container-registry/) | A private registry service provided by Microsoft Azure.                                                          |
| [Quay.io](https://quay.io/)                                              | A registry for building, pushing, and holding Docker images. Often used for public and private repositories.      |

| 仓库                                                                       | 描述                                                                                                             |
| :------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- |
| [Docker Hub](https://hub.docker.com/)                                      | 默认的全局仓库。                                                                                                 |
| [Docker Trusted Registry (DTR)](https://www.docker.com/products/docker-trusted-registry) | 可在本地部署的商业仓库。                                                                                         |
| [Amazon EC2 Container Registry (ECR)](https://aws.amazon.com/ecr/)         | 由 Amazon Web Services (AWS) 提供的私有仓库服务。                                                                 |
| [Google Container Registry (GCR)](https://cloud.google.com/container-registry/) | 由 Google Cloud Platform (GCP) 提供的私有仓库服务。                                                               |
| [Azure Container Registry (ACR)](https://azure.microsoft.com/en-us/services/container-registry/) | 由 Microsoft Azure 提供的私有仓库服务。                                                                           |
| [Quay.io](https://quay.io/)                                                | 用于构建、推送和保存 Docker 镜像的仓库。常用于公共和私有仓库。                                                   |

## Other registries

You can also connect to other registries, including your own private registry.

## 其他仓库

您也可以连接到其他仓库，包括您自己的私有仓库。

### Connect to a registry

To connect to a registry, you use the `docker login` command:

### 连接到仓库

使用 `docker login` 命令连接到仓库：

```bash
docker login [OPTIONS] [SERVER]
```

The `SERVER` argument is the registry domain, for example `localhost:5000` or `registry.example.com`. The default server is `https://index.docker.io/v1/`.

`SERVER` 参数是仓库域名，例如 `localhost:5000` 或 `registry.example.com`。默认服务器为 `https://index.docker.io/v1/`。

### Tag and push images

After you connect to a registry, you can tag and push images.

### 为镜像打标签并推送

连接到仓库后，您可以为镜像打标签并推送。

1.  List your local images:

    列出本地镜像：

    ```bash
    docker images
    ```

2.  Tag an image for the registry:

    为镜像仓库中的镜像打标签：

    ```bash
    docker tag SOURCE_IMAGE[:TAG] REGISTRY_HOST[:REGISTRY_PORT]/[PROJECT/]IMAGE[:TAG]
    ```

    For example, to tag a local image `my-image` with the tag `v1` for a registry at `localhost:5000`:

    例如，为 `localhost:5000` 处的仓库为本地镜像 `my-image` 打上标签 `v1`：

    ```bash
    docker tag my-image:v1 localhost:5000/my-image:v1
    ```

3.  Push the image to the registry:

    将镜像推送到仓库：

    ```bash
    docker push REGISTRY_HOST[:REGISTRY_PORT]/[PROJECT/]IMAGE[:TAG]
    ```

    For example:

    例如：

    ```bash
    docker push localhost:5000/my-image:v1
    ```

### Pull images

To pull an image from a registry, use the `docker pull` command:

### 拉取镜像

使用 `docker pull` 命令从仓库拉取镜像：

```bash
docker pull [OPTIONS] NAME[:TAG]
```

For example:

例如：

```bash
docker pull localhost:5000/my-image:v1
```

## Related information

## 相关信息

*   [Docker Hub](/docker-hub/)
*   [Docker Trusted Registry](/docker-trusted-registry/)
*   [ECR](/engine/reference/commandline/login/#amazon-ecr)
*   [GCR](/engine/reference/commandline/login/#google-container-registry)
*   [ACR](/engine/reference/commandline/login/#azure-container-registry)
*   [Quay.io](/engine/reference/commandline/login/#quayio)

*   [Docker Hub](/docker-hub/)
*   [Docker Trusted Registry](/docker-trusted-registry/)
*   [ECR](/engine/reference/commandline/login/#amazon-ecr)
*   [GCR](/engine/reference/commandline/login/#google-container-registry)
*   [ACR](/engine/reference/commandline/login/#azure-container-registry)
*   [Quay.io](/engine/reference/commandline/login/#quayio)