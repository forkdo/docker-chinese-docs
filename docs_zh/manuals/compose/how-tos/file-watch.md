---
description: 使用文件监控自动更新运行中的服务
keywords: compose, file watch, experimental
title: 使用 Compose Watch
weight: 50
aliases:
- /compose/file-watch/
---

{{< summary-bar feature_name="Compose file watch" >}}

{{% include "compose/watch.md" %}}

`watch` 遵循以下文件路径规则：
* 所有路径都相对于项目目录，忽略文件模式除外
* 目录会被递归监控
* 不支持 glob 模式
* `.dockerignore` 中的规则仍然适用
  * 使用 `ignore` 选项定义额外的忽略路径（语法相同）
  * 常见 IDE（Vim、Emacs、JetBrains 等）的临时/备份文件会自动被忽略
  * `.git` 目录会自动被忽略

你不需要为 Compose 项目中的所有服务都启用 `watch`。在某些情况下，只有项目的部分（例如 JavaScript 前端）适合自动更新。

Compose Watch 专为使用 `build` 属性从本地源代码构建的服务而设计。它不会追踪依赖 `image` 属性指定的预构建镜像的服务的更改。

## Compose Watch 与绑定挂载

Compose 支持在服务容器内共享主机目录。Watch 模式并不会取代此功能，而是作为容器开发的补充功能而存在。

更重要的是，`watch` 允许比绑定挂载更精细的控制。Watch 规则允许你忽略被监控目录树中的特定文件或整个目录。

例如，在 JavaScript 项目中忽略 `node_modules/` 目录有两个好处：
* 性能：包含大量小文件的文件树在某些配置中可能造成高 I/O 负载
* 跨平台：如果主机操作系统或架构与容器不同，则编译产物无法共享

例如，在 Node.js 项目中，不建议同步 `node_modules/` 目录。即使 JavaScript 是解释型语言，`npm` 包也可能包含不可跨平台移植的原生代码。

## 配置

`watch` 属性定义了一组规则列表，用于根据本地文件更改控制自动服务更新。

每条规则都需要一个 `path` 模式和检测到修改时要执行的 `action`。`watch` 有两种可能的操作，
根据 `action` 的不同，可能需要或接受额外的字段。

Watch 模式可用于多种不同的语言和框架。特定路径和规则会因项目而异，但概念保持一致。

### 前提条件

为了正常工作，`watch` 依赖于常见的可执行文件。请确保你的服务镜像包含以下二进制文件：
* stat
* mkdir
* rmdir

`watch` 还要求容器的 `USER` 能够写入目标路径，以便更新文件。常见的模式是使用 Dockerfile 中的 `COPY` 指令将初始内容复制到容器中。为确保这些文件由配置的用户拥有，请使用 `COPY --chown` 标志：

```dockerfile
# 以非特权用户运行
FROM node:18
RUN useradd -ms /bin/sh -u 1001 app
USER app

# 安装依赖
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

# 将源文件复制到应用程序目录
COPY --chown=app:app . /app
```

### `action`

#### Sync（同步）

如果 `action` 设置为 `sync`，Compose 会确保在主机上对文件所做的任何更改都会自动与服务容器中的对应文件保持一致。

`sync` 非常适合支持"热重载"或等效功能的框架。

更一般地说，`sync` 规则可以替代许多开发用例中的绑定挂载。

#### Rebuild（重建）

如果 `action` 设置为 `rebuild`，Compose 会自动使用 BuildKit 构建新镜像并替换正在运行的服务容器。

行为与运行 `docker compose up --build <svc>` 相同。

Rebuild 非常适合编译型语言，或作为特定文件修改的回退方案（例如 `package.json`），这些修改需要完整的镜像重建。

#### Sync + Restart（同步并重启）

如果 `action` 设置为 `sync+restart`，Compose 会将你的更改与服务容器同步并重启它们。

`sync+restart` 非常适合配置文件更改时，你不需要重建镜像，只需重启服务容器的主进程的情况。例如，当你更新数据库配置或 `nginx.conf` 文件时，这会非常有效。

>[!TIP]
>
> 通过 [镜像层缓存](/build/cache) 和 [多阶段构建](/build/building/multi-stage/) 优化你的 `Dockerfile`，以实现快速的增量重建。

### `path` 和 `target`

`target` 字段控制路径如何映射到容器中。

对于 `path: ./app/html` 和 `./app/html/index.html` 的更改：

* `target: /app/html` -> `/app/html/index.html`
* `target: /app/static` -> `/app/static/index.html`
* `target: /assets` -> `/assets/index.html`

### `ignore`

`ignore` 模式相对于当前 `watch` 操作中定义的 `path`，而不是相对于项目目录。在示例 1 中，忽略路径将相对于 `path` 属性中指定的 `./web` 目录。

### `initial_sync`

使用 `sync+x` 操作时，`initial_sync` 属性告诉 Compose 在启动新的监控会话之前，确保已定义 `path` 中的文件是最新的。

## 示例 1

这个最小示例针对一个具有以下结构的 Node.js 应用程序：
```text
myproject/
├── web/
│   ├── App.jsx
│   ├── index.js
│   └── node_modules/
├── Dockerfile
├── compose.yaml
└── package.json
```

```yaml
services:
  web:
    build: .
    command: npm start
    develop:
      watch:
        - action: sync
          path: ./web
          target: /src/web
          initial_sync: true
          ignore:
            - node_modules/
        - action: rebuild
          path: package.json
```

在此示例中，运行 `docker compose up --watch` 时，`web` 服务的容器会使用从项目根目录 `Dockerfile` 构建的镜像启动。`web` 服务运行 `npm start` 作为其命令，然后启动应用程序的开发版本，其中在打包器（Webpack、Vite、Turbopack 等）中启用了热模块重载。

服务启动后，监控模式开始监控目标目录和文件。然后，每当 `web/` 目录中的源文件更改时，Compose 会将文件同步到容器内 `/src/web` 下的对应位置。例如，`./web/App.jsx` 会被复制到 `/src/web/App.jsx`。

复制后，打包器会在不重启的情况下更新正在运行的应用程序。

在这种情况下，`ignore` 规则将应用于 `myproject/web/node_modules/`，而不是 `myproject/node_modules/`。

与源代码文件不同，添加新依赖项无法即时完成，因此每当 `package.json` 更改时，Compose 都会重建镜像并重新创建 `web` 服务容器。

这种模式可以遵循用于多种语言和框架，例如 Python 与 Flask：Python 源文件可以同步，而 `requirements.txt` 的更改应触发重建。

## 示例 2

调整前面的示例以演示 `sync+restart`：

```yaml
services:
  web:
    build: .
    command: npm start
    develop:
      watch:
        - action: sync
          path: ./web
          target: /app/web
          ignore:
            - node_modules/
        - action: sync+restart
          path: ./proxy/nginx.conf
          target: /etc/nginx/conf.d/default.conf

  backend:
    build:
      context: backend
      target: builder
```

此设置演示了如何在 Docker Compose 中使用 `sync+restart` 操作来高效开发和测试带有前端 Web 服务器和后端服务的 Node.js 应用程序。该配置确保应用程序代码和配置文件的更改能够快速同步并应用，`web` 服务在需要时重启以反映更改。

## 使用 `watch`

{{% include "compose/configure-watch.md" %}}

> [!NOTE]
>
> 如果你不想将应用程序日志与（重建）构建日志和文件系统同步事件混合，也可以使用专用的 `docker compose watch` 命令。

> [!TIP]
>
> 查看 [`dockersamples/avatars`](https://github.com/dockersamples/avatars) 或 [Docker 文档本地设置](https://github.com/docker/docs/blob/main/CONTRIBUTING.md)，了解 Compose `watch` 的演示。

## 参考

- [Compose Develop 规范](/reference/compose-file/develop.md)