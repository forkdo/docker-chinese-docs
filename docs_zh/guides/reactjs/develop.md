---
title: 使用容器进行 React.js 开发
linkTitle: 开发你的应用
weight: 30
keywords: react.js, development, node
description: 了解如何使用容器在本地开发你的 React.js 应用。

---

## 前置条件

完成 [使用容器打包 React.js 应用](containerize.md)。

---

## 概述

在本节中，你将学习如何使用 Docker Compose 为你的容器化 React.js 应用设置生产环境和开发环境。此设置允许你通过 Nginx 提供静态生产构建，并使用 Compose Watch 在容器内进行高效开发，支持实时重载的开发服务器。

你将学习如何：
- 为生产和开发配置独立的容器
- 使用 Compose Watch 在开发中启用自动文件同步
- 实时调试和预览你的更改，无需手动重建

---

## 自动更新服务（开发模式）

使用 Compose Watch 自动将源文件的更改同步到你的容器化开发环境中。这提供了无缝、高效的开发体验，无需手动重启或重建容器。

## 步骤 1：创建开发用 Dockerfile

在你的项目根目录中创建一个名为 `Dockerfile.dev` 的文件，内容如下：

```dockerfile
# =========================================
# Stage 1: Develop the React.js Application
# =========================================
ARG NODE_VERSION=24.7.0-alpine

# Use a lightweight Node.js image for development
FROM node:${NODE_VERSION} AS dev

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json ./

# Install project dependencies
RUN --mount=type=cache,target=/root/.npm npm install

# Copy the rest of the application source code into the container
COPY . .

# Expose the port used by the Vite development server
EXPOSE 5173

# Use a default command, can be overridden in Docker compose.yml file
CMD ["npm", "run", "dev"]
```

此文件使用开发服务器为你的 React 应用设置了一个轻量级的开发环境。


### 步骤 2：更新你的 `compose.yaml` 文件

打开你的 `compose.yaml` 文件，定义两个服务：一个用于生产（`react-prod`），一个用于开发（`react-dev`）。

以下是一个 React.js 应用的示例配置：

```yaml
services:
  react-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-reactjs-sample
    ports:
      - "8080:8080"

  react-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    develop:
      watch:
        - action: sync
          path: .
          target: /app

```
- `react-prod` 服务使用 Nginx 构建并提供你的静态生产应用。
- `react-dev` 服务运行你的 React 开发服务器，支持实时重载和热模块替换。
- `watch` 使用 Compose Watch 触发文件同步。

> [!NOTE]
> 更多详细信息，请参阅官方指南：[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

### 步骤 3：更新 vite.config.ts 以确保在 Docker 内部正常工作

为了使 Vite 的开发服务器在 Docker 内部可靠运行，你需要使用正确的设置更新你的 vite.config.ts。

打开项目根目录中的 `vite.config.ts` 文件，并按如下方式更新：

```ts
/// <reference types="vitest" />

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/",
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    strictPort: true,
  },
});
```

> [!NOTE]
> `vite.config.ts` 中的 `server` 选项对于在 Docker 内部运行 Vite 至关重要：
> - `host: true` 允许开发服务器从容器外部访问。
> - `port: 5173` 设置一致的开发端口（必须与 Docker 中暴露的端口匹配）。
> - `strictPort: true` 确保如果端口不可用，Vite 会明确失败，而不是静默切换。
> 
> 详细信息请参考 [Vite 服务器配置文档](https://vitejs.dev/config/server-options.html)。

完成上述步骤后，你的项目目录现在应包含以下文件：

```text
├── docker-reactjs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

### 步骤 4：启动 Compose Watch

从你的项目根目录运行以下命令，以 watch 模式启动你的容器：

```console
$ docker compose watch react-dev
```

### 步骤 5：使用 React 测试 Compose Watch

为了验证 Compose Watch 是否正常工作：

1. 在你的文本编辑器中打开 `src/App.tsx` 文件。

2. 找到以下行：

    ```html
    <h1>Vite + React</h1>
    ```

3. 将其更改为：

    ```html
    <h1>Hello from Docker Compose Watch</h1>
    ```

4. 保存文件。

5. 在浏览器中打开 [http://localhost:5173](http://localhost:5173)。

你应该看到更新的文本立即出现，无需手动重建容器。这确认了文件监视和自动同步按预期工作。

---

## 总结

在本节中，你为你的 React.js 应用设置了一个完整的开发和生产工作流，使用 Docker 和 Docker Compose。

你实现了以下内容：
- 创建了 `Dockerfile.dev` 以使用热重载简化本地开发
- 在 `compose.yaml` 文件中定义了独立的 `react-dev` 和 `react-prod` 服务
- 使用 Compose Watch 启用实时文件同步，获得更流畅的开发体验
- 通过修改和预览组件验证了实时更新无缝工作

有了这个设置，你现在已准备好完全在容器内构建、运行和迭代你的 React.js 应用——在所有环境中高效且一致。

---

## 相关资源

通过以下指南加深你的知识，改进你的容器化开发工作流：

- [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md) – 在开发期间自动同步源更改
- [多阶段构建](/manuals/build/building/multi-stage.md) – 创建高效、生产就绪的 Docker 镜像
- [Dockerfile 最佳实践](/build/building/best-practices/) – 编写干净、安全、优化的 Dockerfile
- [Compose 文件参考](/compose/compose-file/) – 了解在 `compose.yaml` 中配置服务的完整语法和选项
- [Docker 卷](/storage/volumes/) – 在容器运行之间持久化和管理数据

## 下一步

在下一节中，你将学习如何在 Docker 容器内运行 React.js 应用的单元测试。这确保了在所有环境中的一致测试，并消除了对本地机器设置的依赖。