---
title: Gordon 使用场景与示例
linkTitle: 使用场景
description: 常见 Docker 工作流的示例提示词
weight: 10
---

{{< summary-bar feature_name="Gordon" >}}

Gordon 通过自然对话处理 Docker 工作流。在 Docker Desktop 中，你可以从侧边栏访问 Gordon 进行开放式会话，也可以从 Containers、Images、Builds 和 Volumes 等视图中的上下文入口访问它。从这些视图中选择 Gordon 时，会打开一个已预加载当前查看项上下文的对话。你也可以在 CLI 中使用 `docker ai` 提出同样的问题。

## 调试失败的容器

你正在 Containers 视图中，某个容器崩溃了或行为异常。从容器行打开 Gordon，询问该容器的状态和配置：

- "Why did this container exit?"
- "What environment variables are set in this container?"
- "How long did this container run?"
- "What security settings are applied to this container?"

从 CLI：

```console
$ docker ai "why is my postgres container crashing on startup?"
```

## 调试失败的构建

你正在 Builds 视图中查看一个失败的或比预期慢的构建。从该构建打开 Gordon，检查 Dockerfile、构建参数和缓存行为：

- "Why did this build fail?"
- "How can I improve cache usage for this build?"
- "What Dockerfile instructions were used?"
- "What build arguments were used?"

从 CLI：

```console
$ docker ai "my build is failing at the pip install step, what's wrong?"
```

## 检查镜像

你正在 Images 视图中，想在运行镜像之前了解其中的内容，或者想评估某个基础镜像：

- "How do I run this image in the CLI?"
- "What environment variables are configured?"
- "What entrypoint is configured?"
- "What's the base architecture of this image?"
- "Is there a lighter version of this image?"

从 CLI：

```console
$ docker ai "compare my python:3.12 image to python:3.12-slim"
```

## 管理卷和资源

在 Volumes 视图中，可以询问 Gordon 存储了什么内容、哪些容器在使用某个卷，或如何进行清理。在任意视图中，你都可以使用 Gordon 侧边栏来检查更广泛的环境：

- "Which containers are using this volume?"
- "Show me all my containers and their status"
- "How much disk space is Docker using?"
- "List my images sorted by size"

从 CLI：

```console
$ docker ai "clean up all unused Docker resources"
```

## 构建与容器化

对于新项目，可以在 Gordon 侧边栏中开始对话，或在项目目录下通过 `docker ai` 启动。Gordon 会读取你的工作目录并提出合适的文件方案：

- "Containerize my Node.js app"
- "Create a docker-compose for my stack"
- "Set up a dev environment with Postgres and Redis"

从 CLI：

```console
$ cd ~/my-project
$ docker ai "create a Dockerfile for this application"
```

## 开发与优化

让 Gordon 审查并改进现有的 Dockerfile 或服务定义。你可以从 Images 视图（针对已构建的镜像）开始，也可以从带有项目上下文的 Gordon 侧边栏开始：

- "Optimize this Dockerfile"
- "Add a health check to my service"
- "Make my Dockerfile more secure"

从 CLI：

```console
$ docker ai "rate my Dockerfile and suggest improvements"
```

## 学习 Docker

对于概念性问题，可使用 Gordon 侧边栏或 CLI。Gordon 会结合你的环境来解释概念，而不是给出通用答案：

- "What is a Docker volume?"
- "Explain multi-stage builds"
- "How does networking work in Docker?"

从 CLI：

```console
$ docker ai "what's the difference between COPY and ADD in a Dockerfile?"
```

## 编写有效的提示词

要具体：

- 包含相关上下文："my postgres container" 而不是 "the database"
- 说明你的目标："make my build faster" 而不是 "optimize"
- 调试时附上错误信息

当你描述想要达成的目标而非具体做法时，Gordon 的效果最好。Gordon 在整个对话中会保持上下文，因此你可以继续追问澄清或提出相关问题，而无需重复说明。

### 工作目录上下文

在 CLI 中使用 `docker ai` 时，Gordon 会将你当前的工作目录作为文件操作的默认上下文。启动 Gordon 前请切换到你的项目目录，以确保它能访问正确的文件：

```console
$ cd ~/my-project
$ docker ai "review my Dockerfile"
```

你也可以使用 `-C` 标志覆盖工作目录。详情参见[通过 CLI 使用 Gordon](./how-to/cli.md#working-directory)。
