# 使用 Compose Watch





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="/compose/releases/release-notes/#2220">2.22.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>





`watch` 属性会在您编辑并保存代码时自动更新并预览正在运行的 Compose 服务。对于许多项目而言，一旦 Compose 开始运行，您就可以实现无需手动干预的开发工作流，因为服务会在您保存工作时自动更新。

`watch` 遵循以下文件路径规则：
* 所有路径相对于项目目录（忽略文件模式除外）
* 目录递归监视
* 不支持 glob 模式
* `.dockerignore` 中的规则适用
  * 使用 `ignore` 选项定义额外的忽略路径（语法相同）
  * 常见 IDE（Vim、Emacs、JetBrains 等）的临时/备份文件自动被忽略
  * `.git` 目录自动被忽略

使用 Compose 项目时，不需要为所有服务开启 `watch`。在某些情况下，只有项目的一部分（例如 JavaScript 前端）适合自动更新。

Compose Watch 专为使用 `build` 属性从本地源代码开发容器而设计。它不会跟踪依赖 `image` 属性指定的预构建镜像的服务的更改。

## Compose Watch 与绑定挂载的对比

Compose 支持在服务容器内共享主机目录。Watch 模式不会取代此功能，而是作为开发容器的补充功能。

更重要的是，`watch` 比绑定挂载提供了更精细的控制。Watch 规则允许您忽略被监视目录树中的特定文件或整个目录。

例如，在 JavaScript 项目中忽略 `node_modules/` 目录有两个好处：
* 性能：包含大量小文件的文件树在某些配置中可能导致高 I/O 负载
* 多平台：如果主机操作系统或架构与容器不同，则编译产物无法共享

例如，在 Node.js 项目中，不建议同步 `node_modules/` 目录。即使 JavaScript 是解释型语言，`npm` 包也可能包含不可跨平台移植的原生代码。

## 配置

`watch` 属性定义了一组规则列表，用于根据本地文件更改控制自动服务更新。

每条规则都需要一个 `path` 模式和检测到修改时采取的 `action`。`watch` 有两种可能的操作，
根据 `action` 的不同，可能需要或接受额外的字段。

Watch 模式可用于多种不同的语言和框架。特定路径和规则因项目而异，但概念保持一致。

### 前置条件

为了正常工作，`watch` 依赖于常见的可执行文件。确保您的服务镜像包含以下二进制文件：
* stat
* mkdir
* rmdir

`watch` 还要求容器的 `USER` 能够写入目标路径以更新文件。常见的模式是使用 Dockerfile 中的 `COPY` 指令将初始内容复制到容器中。为确保这些文件由配置的用户拥有，请使用 `COPY --chown` 标志：

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

#### Sync

如果 `action` 设置为 `sync`，Compose 确保主机上文件的任何更改自动与服务容器中的对应文件匹配。

`sync` 适用于支持 "Hot Reload" 或类似功能的框架。

更一般地，`sync` 规则可以替代许多开发用例中的绑定挂载。

#### Rebuild

如果 `action` 设置为 `rebuild`，Compose 使用 BuildKit 自动构建新镜像并替换正在运行的服务容器。

行为与运行 `docker compose up --build <svc>` 相同。

Rebuild 适用于编译语言，或作为特定文件修改需要完整镜像重建的回退方案（例如 `package.json`）。

#### Sync + Restart

如果 `action` 设置为 `sync+restart`，Compose 将您的更改与服务容器同步并重启它们。

`sync+restart` 适用于配置文件更改时，您不需要重建镜像，只需重启服务容器的主进程。例如，当您更新数据库配置或 `nginx.conf` 文件时，此操作效果良好。

>[!TIP]
>
> 通过 [镜像层缓存](/build/cache) 和 [多阶段构建](/build/building/multi-stage/) 优化您的 `Dockerfile`，实现快速的增量重建。

### `path` 和 `target`

`target` 字段控制路径如何映射到容器中。

对于 `path: ./app/html` 和 `./app/html/index.html` 的更改：

* `target: /app/html` -> `/app/html/index.html`
* `target: /app/static` -> `/app/static/index.html`
* `target: /assets` -> `/assets/index.html`

### `ignore`

`ignore` 模式相对于当前 `watch` 操作中定义的 `path`，而不是相对于项目目录。在示例 1 中，忽略路径相对于 `path` 属性中指定的 `./web` 目录。

### `initial_sync`

使用 `sync+x` 操作时，`initial_sync` 属性告诉 Compose 在启动新的 watch 会话之前，确保已定义 `path` 中的文件是最新的。

## 示例 1

此最小示例针对具有以下结构的 Node.js 应用程序：
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

在此示例中，运行 `docker compose up --watch` 时，`web` 服务的容器使用从项目根目录 `Dockerfile` 构建的镜像启动。`web` 服务运行 `npm start` 命令，然后启动应用程序的开发版本，其中在打包器（Webpack、Vite、Turbopack 等）中启用了热模块重载。

服务启动后，watch 模式开始监视目标目录和文件。然后，每当 `web/` 目录中的源文件更改时，Compose 将文件同步到容器内 `/src/web` 下的对应位置。例如，`./web/App.jsx` 被复制到 `/src/web/App.jsx`。

复制后，打包器在不重启的情况下更新正在运行的应用程序。

在这种情况下，`ignore` 规则将应用于 `myproject/web/node_modules/`，而不是 `myproject/node_modules/`。

与源代码文件不同，添加新依赖项无法实时完成，因此每当 `package.json` 更改时，Compose 会重建镜像并重新创建 `web` 服务容器。

此模式可应用于多种语言和框架，例如 Python 与 Flask：Python 源文件可以同步，而 `requirements.txt` 的更改应触发重建。

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

此设置演示了如何在 Docker Compose 中使用 `sync+restart` 操作，高效开发和测试带有前端 Web 服务器和后端服务的 Node.js 应用程序。配置确保应用程序代码和配置文件的更改能够快速同步并应用，`web` 服务在需要时重启以反映更改。

## 使用 `watch`



1. 在 `compose.yaml` 文件中的一个或多个服务中添加 `watch` 部分。
2. 运行 `docker compose up --watch` 命令来构建并启动 Compose 项目，同时启动文件监听模式。
3. 使用您首选的 IDE 或编辑器编辑服务源文件。

> [!NOTE]
>
> 如果您不希望应用程序日志与（重新）构建日志和文件系统同步事件混合，也可以使用专用的 `docker compose watch` 命令。

> [!TIP]
>
> 查看 [`dockersamples/avatars`](https://github.com/dockersamples/avatars) 或 [Docker 文档的本地设置](https://github.com/docker/docs/blob/main/CONTRIBUTING.md)，了解 Compose `watch` 的演示。

## 参考

- [Compose Develop 规范](/reference/compose-file/develop.md)
