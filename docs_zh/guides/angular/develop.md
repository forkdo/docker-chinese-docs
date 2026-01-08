---
title: 使用容器进行 Angular 开发
linkTitle: 开发你的应用
weight: 30
keywords: angular, development, node
description: 学习如何使用容器在本地开发你的 Angular 应用。
---

## 先决条件

完成 [容器化 Angular 应用](containerize.md)。

---

## 概述

在本节中，你将学习如何使用 Docker Compose 为你的容器化 Angular 应用设置生产和开发环境。此设置允许你通过 Nginx 提供静态生产构建版本，并使用带有 Compose Watch 的实时重载开发服务器在容器内高效开发。

你将学习如何：
- 为生产和开发配置独立的容器
- 在开发中使用 Compose Watch 启用自动文件同步
- 实时调试和预览你的更改，无需手动重建

---

## 自动更新服务

使用 Compose Watch 自动将源文件更改同步到你的容器化开发环境中。这提供了无缝、高效的开发体验，无需手动重启或重建容器。

## 步骤 1：创建一个开发 Dockerfile

在项目根目录中创建一个名为 `Dockerfile.dev` 的文件，内容如下：

```dockerfile
# =========================================
# Stage 1: Development - Angular Application
# =========================================

# Define the Node.js version to use (Alpine for a small footprint)
ARG NODE_VERSION=24.7.0-alpine

# Set the base image for development
FROM node:${NODE_VERSION} AS dev

# Set environment variable to indicate development mode
ENV NODE_ENV=development

# Set the working directory inside the container
WORKDIR /app

# Copy only the dependency files first to optimize Docker caching
COPY package.json package-lock.json ./

# Install dependencies using npm with caching to speed up subsequent builds
RUN --mount=type=cache,target=/root/.npm npm install

# Copy all application source files into the container
COPY . .

# Expose the port Angular uses for the dev server (default is 4200)
EXPOSE 4200

# Start the Angular dev server and bind it to all network interfaces
CMD ["npm", "start", "--", "--host=0.0.0.0"]

```

此文件使用开发服务器为你的 Angular 应用设置了一个轻量级的开发环境。


### 步骤 2：更新你的 `compose.yaml` 文件

打开你的 `compose.yaml` 文件并定义两个服务：一个用于生产 (`angular-prod`)，一个用于开发 (`angular-dev`)。

以下是一个 Angular 应用的配置示例：

```yaml
services:
  angular-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-angular-sample
    ports:
      - "8080:8080"

  angular-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "4200:4200"
    develop:
      watch:
        - action: sync
          path: .
          target: /app
```
- `angular-prod` 服务使用 Nginx 构建并提供你的静态生产应用。
- `angular-dev` 服务运行你的 Angular 开发服务器，支持实时重载和热模块替换。
- `watch` 触发与 Compose Watch 的文件同步。

> [!NOTE]
> 有关更多详细信息，请参阅官方指南：[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

完成前面的步骤后，你的项目目录现在应包含以下文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

### 步骤 4：启动 Compose Watch

从项目根目录运行以下命令，以在 watch 模式下启动容器

```console
$ docker compose watch angular-dev
```

### 步骤 5：使用 Angular 测试 Compose Watch

要验证 Compose Watch 是否正常工作：

1. 在你的文本编辑器中打开 `src/app/app.component.html` 文件。

2. 找到以下行：

    ```html
    <h1>Docker Angular Sample Application</h1>
    ```

3. 将其更改为：

    ```html
    <h1>Hello from Docker Compose Watch</h1>
    ```

4. 保存文件。

5. 在浏览器中打开 [http://localhost:4200](http://localhost:4200)。

你应该会看到更新后的文本立即出现，无需手动重建容器。这确认了文件监听和自动同步正在按预期工作。

---

## 总结

在本节中，你使用 Docker 和 Docker Compose 为你的 Angular 应用设置了一个完整的开发和生产工作流。

以下是你的成就：
- 创建了一个 `Dockerfile.dev`，通过热重载简化了本地开发
- 在你的 `compose.yaml` 文件中定义了独立的 `angular-dev` 和 `angular-prod` 服务
- 使用 Compose Watch 启用实时文件同步，以获得更流畅的开发体验
- 通过修改和预览一个组件，验证了实时更新可以无缝工作

有了此设置，你现在完全可以跨环境高效、一致地在容器内构建、运行和迭代你的 Angular 应用。

---

## 相关资源

通过这些指南深化你的知识并改进你的容器化开发工作流：

- [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md) – 在开发期间自动同步源代码更改
- [多阶段构建](/manuals/build/building/multi-stage.md) – 创建高效的、可用于生产的 Docker 镜像
- [Dockerfile 最佳实践](/build/building/best-practices/) – 编写整洁、安全且优化的 Dockerfiles。
- [Compose 文件参考](/compose/compose-file/) – 了解在 `compose.yaml` 中配置服务可用的完整语法和选项。
- [Docker 卷](/storage/volumes/) – 在容器运行之间持久化和管理数据  

## 后续步骤

在下一节中，你将学习如何在 Docker 容器内为你的 Angular 应用运行单元测试。这确保了在所有环境中进行一致的测试，并消除了对本地机器设置的依赖。