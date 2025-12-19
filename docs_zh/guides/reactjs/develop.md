---
title: 使用容器进行 React.js 开发
linkTitle: 开发您的应用程序
weight: 30
keywords: react.js, development, node
description: 了解如何使用容器在本地开发 React.js 应用程序。

---

## 先决条件

已完成[容器化 React.js 应用程序](containerize.md)。

---

## 概述

在本节中，您将学习如何使用 Docker Compose 为容器化的 React.js 应用程序设置生产和开发环境。此设置允许您通过 Nginx 提供静态生产构建，并使用 Compose Watch 在容器内通过实时重载开发服务器进行高效开发。

您将学习如何：
- 为生产和开发配置独立的容器
- 在开发模式下启用使用 Compose Watch 的自动文件同步
- 无需手动重新构建，即可实时调试和预览更改

---

## 自动更新服务（开发模式）

使用 Compose Watch 将源文件更改自动同步到容器化的开发环境中。这提供了一种无缝、高效的开发体验，无需手动重启或重建容器。

## 步骤 1：创建开发 Dockerfile

在项目根目录中创建一个名为 `Dockerfile.dev` 的文件，内容如下：

```dockerfile
# =========================================
# 阶段 1：开发 React.js 应用程序
# =========================================
ARG NODE_VERSION=24.7.0-alpine

# 使用轻量级 Node.js 镜像进行开发
FROM node:${NODE_VERSION} AS dev

# 在容器内设置工作目录
WORKDIR /app

# 首先复制与包相关的文件以利用 Docker 的缓存机制
COPY package.json package-lock.json ./

# 安装项目依赖项
RUN --mount=type=cache,target=/root/.npm npm install

# 将应用程序源代码的其余部分复制到容器中
COPY . .

# 暴露 Vite 开发服务器使用的端口
EXPOSE 5173

# 使用默认命令，可以在 Docker compose.yml 文件中覆盖
CMD ["npm", "run", "dev"]
```

此文件使用开发服务器为您的 React 应用设置了一个轻量级的开发环境。


### 步骤 2：更新您的 `compose.yaml` 文件

打开您的 `compose.yaml` 文件并定义两个服务：一个用于生产 (`react-prod`)，一个用于开发 (`react-dev`)。

以下是 React.js 应用程序的配置示例：

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
- `react-prod` 服务使用 Nginx 构建并提供您的静态生产应用程序。
- `react-dev` 服务运行您的 React 开发服务器，具有实时重载和热模块替换功能。
- `watch` 触发 Compose Watch 的文件同步。

> [!NOTE]
> 有关更多详细信息，请参阅官方指南：[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

### 步骤 3：更新 vite.config.ts 以确保其在 Docker 内正常工作

为了使 Vite 的开发服务器在 Docker 内可靠运行，您需要使用正确的设置更新您的 vite.config.ts。

打开项目根目录中的 `vite.config.ts` 文件，并按如下方式进行更新：

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
> `vite.config.ts` 中的 `server` 选项对于在 Docker 内运行 Vite 至关重要：
> - `host: true` 允许从容器外部访问开发服务器。
> - `port: 5173` 设置一致的开发端口（必须与 Docker 中暴露的端口匹配）。
> - `strictPort: true` 确保如果端口不可用，Vite 会明确失败，而不是静默切换。
> 
> 有关完整详细信息，请参阅 [Vite 服务器配置文档](https://vitejs.dev/config/server-options.html)。


完成前面的步骤后，您的项目目录现在应包含以下文件：

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

从项目根目录运行以下命令以在监视模式下启动容器：

```console
$ docker compose watch react-dev
```

### 步骤 5：使用 React 测试 Compose Watch

要验证 Compose Watch 是否正常工作：

1. 在文本编辑器中打开 `src/App.tsx` 文件。

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

您应该会看到更新后的文本立即出现，而无需手动重建容器。这证实了文件监视和自动同步按预期工作。

---

## 总结

在本节中，您使用 Docker 和 Docker Compose 为您的 React.js 应用程序设置了一个完整的开发和生产工作流。

以下是您实现的目标：
- 创建了 `Dockerfile.dev` 以通过热重载简化本地开发
- 在 `compose.yaml` 文件中定义了独立的 `react-dev` 和 `react-prod` 服务
- 使用 Compose Watch 启用了实时文件同步，以获得更流畅的开发体验
- 通过修改和预览组件，验证了实时更新是否无缝工作

通过此设置，您现在可以完全在容器内构建、运行和迭代您的 React.js 应用程序——在所有环境中高效且一致地进行。

---

## 相关资源

通过这些指南加深您的知识并改进容器化开发工作流：

- [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md) – 在开发过程中自动同步源代码更改
- [多阶段构建](/manuals/build/building/multi-stage.md) – 创建高效、生产就绪的 Docker 镜像
- [Dockerfile 最佳实践](/build/building/best-practices/) – 编写干净、安全且优化的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) – 了解用于在 `compose.yaml` 中配置服务的完整语法和可用选项。
- [Docker 卷](/storage/volumes/) – 在容器运行之间持久保存和管理数据

## 下一步

在下一节中，您将学习如何在 Docker 容器内为您的 React.js 应用程序运行单元测试。这确保了在所有环境中进行一致的测试，并消除了对本地机器设置的依赖。