---
title: 编写 Dockerfile
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 本概念页面将指导您如何使用 Dockerfile 创建镜像。
summary: |
  掌握 Dockerfile 实践对于有效利用容器技术至关重要，
  这能提升应用程序的可靠性，并支持 DevOps 和
  CI/CD 方法论。在本指南中，您将学习如何编写 Dockerfile、
  如何定义基础镜像以及设置指令，包括安装软件
  和复制必要的文件。
weight: 2
aliases: 
 - /guides/docker-concepts/building-images/writing-a-dockerfile/
---

{{< youtube-embed Jx8zoIhiP4c >}}

## 解释

Dockerfile 是一种基于文本的文档，用于创建容器镜像。它向镜像构建器提供指令，说明要运行哪些命令、要复制哪些文件、启动命令等。

例如，以下 Dockerfile 将生成一个可立即运行的 Python 应用程序：

```dockerfile
FROM python:3.13
WORKDIR /usr/local/app

# 安装应用程序依赖项
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src ./src
EXPOSE 8080

# 设置 app 用户，这样容器就不会以 root 用户身份运行
RUN useradd app
USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 常用指令

`Dockerfile` 中一些最常见的指令包括：

- `FROM <image>` - 指定构建将扩展的基础镜像。
- `WORKDIR <path>` - 指定“工作目录”或镜像中将复制文件和执行命令的路径。
- `COPY <host-path> <image-path>` - 告诉构建器从主机复制文件并将其放入容器镜像中。
- `RUN <command>` - 告诉构建器运行指定的命令。
- `ENV <name> <value>` - 设置运行容器将使用的环境变量。
- `EXPOSE <port-number>` - 在镜像上设置配置，指示镜像希望暴露的端口。
- `USER <user-or-uid>` - 为所有后续指令设置默认用户。
- `CMD ["<command>", "<arg1>"]` - 设置使用此镜像的容器将运行的默认命令。

要阅读所有指令或了解更详细的信息，请查看 [Dockerfile 参考](https://docs.docker.com/engine/reference/builder/)。

## 动手尝试

正如您在前面的示例中看到的，Dockerfile 通常遵循以下步骤：

1. 确定您的基础镜像
2. 安装应用程序依赖项
3. 复制任何相关的源代码和/或二进制文件
4. 配置最终镜像

在这个快速的实践指南中，您将编写一个构建简单 Node.js 应用程序的 Dockerfile。如果您不熟悉基于 JavaScript 的应用程序，也不必担心。这并不影响您跟随本指南进行操作。

### 设置

[下载此 ZIP 文件](https://github.com/docker/getting-started-todo-app/archive/refs/heads/build-image-from-scratch.zip) 并将内容解压缩到您机器上的一个目录中。

如果您不想下载 ZIP 文件，可以克隆 https://github.com/docker/getting-started-todo-app 项目并检出 `build-image-from-scratch` 分支。

### 创建 Dockerfile

现在您已经有了项目，可以准备创建 `Dockerfile` 了。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

2. 检查项目。

   探索 `getting-started-todo-app/app/` 的内容。您会注意到已经存在一个 `Dockerfile`。它是一个简单的文本文件，您可以在任何文本或代码编辑器中打开它。

3. 删除现有的 `Dockerfile`。

   在本练习中，我们将假设您是从零开始，并创建一个新的 `Dockerfile`。

4. 在 `getting-started-todo-app/app/` 文件夹中创建一个名为 `Dockerfile` 的文件。

    > **Dockerfile 文件扩展名**
    >
    > 请注意，`Dockerfile` *没有*文件扩展名。某些编辑器会自动为文件添加扩展名（或者会因为它没有扩展名而发出警告）。

5. 在 `Dockerfile` 中，通过添加以下行来定义您的基础镜像：

    ```dockerfile
    FROM node:22-alpine
    ```

6. 现在，使用 `WORKDIR` 指令定义工作目录。这将指定未来命令的运行位置以及文件在容器镜像内部的复制目录。

    ```dockerfile
    WORKDIR /app
    ```

7. 使用 `COPY` 指令将您机器上项目中的所有文件复制到容器镜像中：

    ```dockerfile
    COPY . .
    ```

8. 使用 `yarn` CLI 和包管理器安装应用程序的依赖项。为此，使用 `RUN` 指令运行一个命令：

    ```dockerfile
    RUN yarn install --production
    ```

9. 最后，使用 `CMD` 指令指定要运行的默认命令：

    ```dockerfile
    CMD ["node", "./src/index.js"]
    ```
    至此，您应该拥有以下 Dockerfile：

    ```dockerfile
    FROM node:22-alpine
    WORKDIR /app
    COPY . .
    RUN yarn install --production
    CMD ["node", "./src/index.js"]
    ```

> **此 Dockerfile 尚未准备好用于生产**
>
> 请注意，此 Dockerfile *尚未*遵循所有最佳实践（这是有意为之）。它可以构建应用程序，但其构建速度和镜像安全性可能无法达到最佳状态。
>
> 请继续阅读，以了解如何通过最大化利用构建缓存、以非 root 用户身份运行以及使用多阶段构建来优化镜像。

> **使用 `docker init` 快速容器化新项目**
>
> `docker init` 命令会分析您的项目并快速创建 Dockerfile、`compose.yaml` 和 `.dockerignore`，帮助您快速上手。由于您目前正在专门学习 Dockerfile，因此现在不会使用它。但是，您可以[在此处了解更多信息](/engine/reference/commandline/init/)。

## 其他资源

要了解有关编写 Dockerfile 的更多信息，请访问以下资源：

* [Dockerfile 参考](/reference/dockerfile/)
* [Dockerfile 最佳实践](/develop/develop-images/dockerfile_best-practices/)
* [基础镜像](/build/building/base-images/)
* [Docker Init 入门](/reference/cli/docker/init/)

## 下一步

现在您已经创建了 Dockerfile 并学习了基础知识，是时候学习构建、标记和推送镜像了。

{{< button text="构建、标记和发布镜像" url="build-tag-and-publish-an-image" >}}