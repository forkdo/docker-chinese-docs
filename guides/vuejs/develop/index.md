# 使用容器进行 Vue.js 开发

## 前提条件

已完成[容器化 Vue.js 应用程序](containerize.md)。

---

## 概述

在本节中，您将使用 Docker Compose 为您的 Vue.js 应用程序设置生产环境和开发环境。这种方法简化了您的工作流程——在生产环境中通过 Nginx 提供轻量级的静态站点，并在开发环境中使用 Compose Watch 提供快速、实时重载的开发服务器以实现高效的本地开发。

您将学习如何：
- 配置隔离的环境：设置针对生产用例和开发用例优化的独立容器。
- 在开发中进行实时重载：使用 Compose Watch 自动同步文件更改，无需手动干预即可实现实时更新。
- 轻松预览和调试：在容器内进行开发，提供无缝的预览和调试体验——无需在每次更改后重新构建。

---

## 自动更新服务（开发模式）

利用 Compose Watch 在您的本地机器和容器化的 Vue.js 开发环境之间启用实时文件同步。这个强大的功能消除了手动重建或重新启动容器的需要，提供快速、无缝且高效的工作流程。

使用 Compose Watch，您的代码更新会立即反映在容器内——非常适合快速测试、调试和实时预览更改。

## 步骤 1：创建开发 Dockerfile

在项目根目录中创建一个名为 `Dockerfile.dev` 的文件，内容如下：

```dockerfile
# =========================================
# 阶段 1：开发 Vue.js 应用程序
# =========================================
ARG NODE_VERSION=23.11.0-alpine

# 使用轻量级 Node.js 镜像进行开发
FROM node:${NODE_VERSION} AS dev

# 设置环境变量以指示开发模式
ENV NODE_ENV=development

# 设置容器内的工作目录
WORKDIR /app

# 首先复制与包相关的文件以利用 Docker 的缓存机制
COPY package.json package-lock.json ./

# 安装项目依赖项
RUN --mount=type=cache,target=/root/.npm npm install

# 将应用程序源代码的其余部分复制到容器中
COPY . .

# 将应用程序目录的所有权更改为 node 用户
RUN chown -R node:node /app

# 切换到 node 用户
USER node

# 暴露 Vite 开发服务器使用的端口
EXPOSE 5173

# 使用默认命令，可以在 Docker compose.yml 文件中覆盖
CMD [ "npm", "run", "dev", "--", "--host" ]

```

此文件使用开发服务器为您的 Vue.js 应用程序设置轻量级开发环境。

### 步骤 2：更新您的 `compose.yaml` 文件

打开您的 `compose.yaml` 文件并定义两个服务：一个用于生产 (`vuejs-prod`)，一个用于开发 (`vuejs-dev`)。

以下是 Vue.js 应用程序的配置示例：

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
- `vuejs-prod` 服务使用 Nginx 构建并提供您的静态生产应用程序。
- `vuejs-dev` 服务运行您的 Vue.js 开发服务器，具有实时重载和热模块替换功能。
- `watch` 触发与 Compose Watch 的文件同步。

> [!NOTE]
> 有关更多详细信息，请参阅官方指南：[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

完成前面的步骤后，您的项目目录现在应包含以下文件：

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

从项目根目录运行以下命令以在观察模式下启动容器

```console
$ docker compose watch vuejs-dev
```

### 步骤 5：使用 Vue.js 测试 Compose Watch

要确认 Compose Watch 是否正常运行：

1. 在您的文本编辑器中打开 `src/App.vue` 文件。

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

您应该会看到更新后的文本立即出现，而无需手动重建容器。这证实了文件观察和自动同步按预期工作。

---

## 总结

在本节中，您使用 Docker 和 Docker Compose 为您的 Vue.js 应用程序设置了完整的开发和生产工作流程。

以下是您完成的工作：
- 创建了 `Dockerfile.dev` 以通过热重载简化本地开发
- 在您的 `compose.yaml` 文件中定义了独立的 `vuejs-dev` 和 `vuejs-prod` 服务
- 使用 Compose Watch 启用了实时文件同步，以获得更流畅的开发体验
- 通过修改和预览组件验证了实时更新是否无缝工作

通过此设置，您现在可以完全在容器内构建、运行和迭代您的 Vue.js 应用程序——在不同环境中高效且一致地进行。

---

## 相关资源

通过这些指南加深您的知识并改进您的容器化开发工作流程：

- [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md) – 在开发过程中自动同步源代码更改
- [多阶段构建](/manuals/build/building/multi-stage.md) – 创建高效、可用于生产的 Docker 镜像
- [Dockerfile 最佳实践](/build/building/best-practices/) – 编写干净、安全且优化的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) – 了解用于在 `compose.yaml` 中配置服务的完整语法和选项。
- [Docker 卷](/storage/volumes/) – 在容器运行之间持久化和管理数据

## 下一步

在下一节中，您将学习如何在 Docker 容器内为您的 Vue.js 应用程序运行单元测试。这可确保在所有环境中进行一致的测试，并消除对本地机器设置的依赖。
