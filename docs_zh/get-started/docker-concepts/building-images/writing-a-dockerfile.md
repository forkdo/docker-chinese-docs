---
title: 编写 Dockerfile
keywords: 概念, 构建, 镜像, 容器, Docker Desktop
description: 本概念页面将教你如何使用 Dockerfile 创建镜像。
summary: |
  掌握 Dockerfile 实践对于有效利用容器技术至关重要，可提升应用可靠性并支持 DevOps 和 CI/CD 方法。在本指南中，你将学习如何编写 Dockerfile，如何定义基础镜像和设置指令，包括软件安装和复制必要文件。
weight: 2
aliases: 
 - /guides/docker-concepts/building-images/writing-a-dockerfile/
---

{{< youtube-embed Jx8zoIhiP4c >}}

## 说明

Dockerfile 是一个基于文本的文档，用于创建容器镜像。它向镜像构建器提供指令，说明要运行的命令、要复制的文件、启动命令等。

例如，以下 Dockerfile 将生成一个可直接运行的 Python 应用：

```dockerfile
FROM python:3.13
WORKDIR /usr/local/app

# 安装应用依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src ./src
EXPOSE 8080

# 设置应用用户，使容器不以 root 用户运行
RUN useradd app
USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 常见指令

Dockerfile 中一些最常用的指令包括：

- `FROM <image>` - 指定构建将扩展的基础镜像。
- `WORKDIR <path>` - 指令指定“工作目录”，即镜像中复制文件和执行命令的路径。
- `COPY <host-path> <image-path>` - 指令告诉构建器从主机复制文件并放入容器镜像。
- `RUN <command>` - 指令告诉构建器运行指定命令。
- `ENV <name> <value>` - 指令设置运行容器将使用的环境变量。
- `EXPOSE <port-number>` - 指令设置镜像的配置，指示镜像希望暴露的端口。
- `USER <user-or-uid>` - 指令设置所有后续指令的默认用户。
- `CMD ["<command>", "<arg1>"]` - 指令设置使用此镜像的容器的默认命令。

要了解所有指令或更详细的说明，请查看 [Dockerfile 参考文档](https://docs.docker.com/engine/reference/builder/)。

## 动手尝试

正如你之前看到的例子，Dockerfile 通常遵循以下步骤：

1. 确定你的基础镜像
2. 安装应用依赖
3. 复制相关源代码和/或二进制文件
4. 配置最终镜像

在本快速实践指南中，你将编写一个构建简单 Node.js 应用的 Dockerfile。如果你不熟悉基于 JavaScript 的应用，不用担心。这并不影响你跟随本指南。

### 准备工作

[下载此 ZIP 文件](https://github.com/docker/getting-started-todo-app/archive/refs/heads/build-image-from-scratch.zip) 并将内容解压到你机器上的一个目录中。

如果你不想下载 ZIP 文件，可以克隆 https://github.com/docker/getting-started-todo-app 项目并检出 `build-image-from-scratch` 分支。

### 创建 Dockerfile

现在你有了项目，接下来创建 `Dockerfile`。

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

2. 检查项目。

   探索 `getting-started-todo-app/app/` 的内容。你会注意到已经存在一个 `Dockerfile`。它是一个简单的文本文件，可以用任何文本或代码编辑器打开。

3. 删除现有的 `Dockerfile`。

   对于本次练习，你将假装从头开始，创建一个新的 `Dockerfile`。

4. 在 `getting-started-todo-app/app/` 文件夹中创建一个名为 `Dockerfile` 的文件。

    > **Dockerfile 文件扩展名**
    >
    > 重要提示：`Dockerfile` _没有_ 文件扩展名。某些编辑器会自动添加扩展名（或抱怨它没有扩展名）。

5. 在 `Dockerfile` 中，通过添加以下行定义你的基础镜像：

    ```dockerfile
    FROM node:22-alpine
    ```

6. 现在，使用 `WORKDIR` 指令定义工作目录。这将指定未来命令运行的位置以及文件复制到容器镜像中的目录：

    ```dockerfile
    WORKDIR /app
    ```

7. 使用 `COPY` 指令将你项目中的所有文件从你的机器复制到容器镜像中：

    ```dockerfile
    COPY . .
    ```

8. 使用 `yarn` CLI 和包管理器安装应用依赖。使用 `RUN` 指令运行命令：

    ```dockerfile
    RUN yarn install --production
    ```

9. 最后，使用 `CMD` 指令指定默认命令：

    ```dockerfile
    CMD ["node", "./src/index.js"]
    ```
    这样，你应该得到以下 Dockerfile：

    ```dockerfile
    FROM node:22-alpine
    WORKDIR /app
    COPY . .
    RUN yarn install --production
    CMD ["node", "./src/index.js"]
    ```

> **此 Dockerfile 尚未为生产环境准备**
>
> 重要提示：此 Dockerfile 尚未遵循所有最佳实践（这是有意设计的）。它可以构建应用，但构建速度不会最快，镜像也不会最安全。
>
> 继续阅读以了解如何使镜像最大化利用构建缓存、以非 root 用户运行，以及多阶段构建。

> **使用 `docker init` 快速容器化新项目**
>
> `docker init` 命令将分析你的项目并快速创建 Dockerfile、`compose.yaml` 和 `.dockerignore`，帮助你快速上手。由于你在这里专门学习 Dockerfile，现在不会使用它。但可以[在此处了解更多信息](/engine/reference/commandline/init/)。

## 额外资源

要了解有关编写 Dockerfile 的更多信息，请访问以下资源：

* [Dockerfile 参考文档](/reference/dockerfile/)
* [Dockerfile 最佳实践](/develop/develop-images/dockerfile_best-practices/)
* [基础镜像](/build/building/base-images/)
* [Docker Init 入门](/reference/cli/docker/init/)

## 下一步

现在你已经创建了 Dockerfile 并学习了基础知识，是时候学习如何构建、标记和推送镜像了。

{{< button text="构建、标记和发布镜像" url="build-tag-and-publish-an-image" >}}

