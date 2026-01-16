---
title: 使用容器进行 Vue.js 开发
linkTitle: 开发您的应用
weight: 30
keywords: vuejs, development, node
description: 了解如何使用容器在本地开发您的 Vue.js 应用程序。

---

## 前提条件

完成 [容器化 Vue.js 应用程序](containerize.md)。

---

## 概述

在本节中，您将使用 Docker Compose 为您的 Vue.js 应用程序设置生产和开发环境。这种方法简化了您的工作流程——在生产环境中通过 Nginx 提供轻量级的静态网站，在本地开发中提供快速的实时重载开发服务器和 Compose Watch。

您将学习如何：
- 配置隔离环境：设置针对生产和开发用例优化的独立容器。
- 开发中的实时重载：使用 Compose Watch 自动同步文件更改，实现无需手动干预的实时更新。
- 轻松预览和调试：在容器内开发，获得无缝的预览和调试体验——每次更改后无需重建。

---

## 自动更新服务（开发模式）

利用 Compose Watch 在本地机器和容器化的 Vue.js 开发环境之间启用实时文件同步。这个强大的功能消除了手动重建或重启容器的需要，提供快速、无缝且高效的开发工作流程。

通过 Compose Watch，您的代码更新会立即在容器内反映——非常适合快速测试、调试和实时预览更改。

## 步骤 1：创建开发 Dockerfile

在项目根目录创建一个名为 `Dockerfile.dev` 的文件，内容如下：

```dockerfile
# =========================================
# Stage 1: Develop the Vue.js Application
# =========================================
ARG NODE_VERSION=24.12.0-alpine

# Use a lightweight Node.js image for development
FROM node:${NODE_VERSION} AS dev

# Set environment variable to indicate development mode
ENV NODE_ENV=development

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Install project dependencies
RUN --mount=type=cache,target=/root/.npm npm install

# Copy the rest of the application source code into the container
COPY . .

# Change ownership of the application directory to the node user
RUN chown -R node:node /app

# Switch to the node user
USER node

# Expose the port used by the Vite development server
EXPOSE 5173

# Use a default command, can be overridden in Docker compose.yml file
CMD [ "npm", "run", "dev", "--", "--host" ]

```

此文件使用开发服务器为您的 Vue.js 应用程序设置轻量级开发环境。

### 步骤 2：更新您的 `compose.yaml` 文件

打开您的 `compose.yaml` 文件并定义两个服务：一个用于生产（`vuejs-prod`）和一个用于开发（`vuejs-dev`）。

以下是 Vue.js 应用程序的示例配置：

```yaml
services:
  vuejs-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-vuejs-sample
    ports:
      - "8080:8080"

  vuejs-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    develop:
      watch:
        - path: ./src
          target: /app/src
          action: sync
        - path: ./package.json
          target: /app/package.json
          action: restart
        - path: ./vite.config.js
          target: /app/vite.config.js
          action: restart
```
- `vuejs-prod` 服务使用 Nginx 构建和提供您的静态生产应用程序。
- `vuejs-dev` 服务运行您的 Vue.js 开发服务器，支持实时重载和热模块替换。
- `watch` 使用 Compose Watch 触发文件同步。

> [!NOTE]
> 更多详情，请参阅官方指南：[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

完成前面的步骤后，您的项目目录现在应该包含以下文件：

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

### 步骤 4：启动 Compose Watch

从项目根目录运行以下命令以在监视模式下启动容器

```console
$ docker compose watch vuejs-dev
```

### 步骤 5：使用 Vue.js 测试 Compose Watch

要确认 Compose Watch 正常工作：

1. 在文本编辑器中打开 `src/App.vue` 文件。

2. 找到以下行：

    ```html
    <HelloWorld msg="You did it!" />
    ```

3. 将其更改为：

    ```html
    <HelloWorld msg="Hello from Docker Compose Watch" />
    ```

4. 保存文件。

5. 在浏览器中打开 [http://localhost:5173](http://localhost:5173)。

您应该会看到更新的文本立即出现，无需手动重建容器。这确认了文件监视和自动同步按预期工作。

---

## 总结

在本节中，您使用 Docker 和 Docker Compose 为您的 Vue.js 应用程序设置了一个完整的开发和生产工作流程。

您完成了以下内容：
- 创建了 `Dockerfile.dev` 以使用热重载简化本地开发
- 在 `compose.yaml` 文件中定义了独立的 `vuejs-dev` 和 `vuejs-prod` 服务
- 使用 Compose Watch 启用实时文件同步，获得更流畅的开发体验
- 通过修改和预览组件验证了实时更新无缝工作

通过此设置，您现在可以在容器内完全构建、运行和迭代您的 Vue.js 应用程序——在不同环境中高效且一致地进行。

---

## 相关资源

通过这些指南加深您的知识并改进您的容器化开发工作流程：

- [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md) – 在开发期间自动同步源代码更改
- [多阶段构建](/manuals/build/building/multi-stage.md) – 创建高效、生产就绪的 Docker 镜像
- [Dockerfile 最佳实践](/build/building/best-practices/) – 编写干净、安全和优化的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) – 了解为 `compose.yaml` 中的服务配置可用的完整语法和选项。
- [Docker 卷](/storage/volumes/) – 在容器运行之间持久化和管理数据

## 下一步

在下一节中，您将学习如何在 Docker 容器内运行 Vue.js 应用程序的单元测试。这确保了所有环境中的测试一致性，并消除了对本地机器设置的依赖。