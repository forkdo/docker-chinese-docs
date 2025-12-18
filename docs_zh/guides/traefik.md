---
title: 使用 Traefik 进行 HTTP 路由
description: *desc 使用 Traefik 轻松在多个容器或非容器化工作负载之间路由流量
keywords: traefik, container-supported development
linktitle: 使用 Traefik 进行 HTTP 路由
summary: *desc
tags: [networking]
params:
  time: 20 minutes
---

## 简介

在本地开发过程中，经常需要运行多个 HTTP 服务。你可能同时拥有 API 和前端应用、用于模拟数据端点的 WireMock 服务，或数据库可视化工具（如 phpMyAdmin 或 pgAdmin）。在许多开发环境中，这些服务通过不同端口暴露，这不仅需要你记住哪个端口对应哪个服务，还可能引发其他问题（如 CORS）。

反向代理可以通过作为唯一暴露的服务，根据请求 URL（按路径或主机名）将请求路由到相应服务，从而显著简化这种设置。[Traefik](https://traefik.io/traefik/) 是一个现代的云原生反向代理和负载均衡器，可简化多服务应用的开发和部署。本指南将展示如何在 Docker 中使用 Traefik 来增强你的开发环境。

在本指南中，你将学习如何：

1. 使用 Docker 启动 Traefik
2. 配置路由规则，在两个容器之间分配流量
3. 在容器化开发环境中使用 Traefik
4. 使用 Traefik 向非容器化工作负载发送请求

## 前置要求

要完成本指南，需要满足以下前置条件：

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js](https://nodejs.org/en/download/package-manager) 和 [yarn](https://yarnpkg.com/)
- Docker 基础知识

## 在 Docker 中使用 Traefik

Traefik 的独特功能之一是支持多种配置方式。使用 Docker 提供者时，Traefik 会从其他运行中的容器获取配置，这些配置通过 [标签](https://docs.docker.com/config/labels-custom-metadata/) 定义。Traefik 会监听引擎事件（容器启动和停止），提取标签并更新其配置。

虽然 Traefik 监控的标签有 [很多](https://doc.traefik.io/traefik/routing/providers/docker/)，但最常用的两个是：

- `traefik.http.routers.<service-name>.rule` - 用于指示路由规则（[查看所有可用规则](https://doc.traefik.io/traefik/routing/routers/#rule)）
- `traefik.http.services.<service-name>.loadbalancer.server.port` - 指示 Traefik 应将请求转发到的端口。注意，此容器端口无需在主机上暴露（[阅读端口检测相关内容](https://doc.traefik.io/traefik/providers/docker/#port-detection)））

让我们快速演示如何启动 Traefik，然后配置两个额外的容器，使其可通过不同主机名访问。

1. 为了让两个容器能够相互通信，它们需要在同一网络中。使用 `docker network create` 命令创建名为 `traefik-demo` 的网络：

   ```console
   $ docker network create traefik-demo
   ```

2. 使用以下命令启动 Traefik 容器。该命令将 Traefik 暴露在 80 端口，挂载 Docker 套接字（用于监控容器以更新配置），并传递 `--providers.docker` 参数配置 Traefik 使用 Docker 提供者。

   ```console
   $ docker run -d --network=traefik-demo -p 80:80 -v /var/run/docker.sock:/var/run/docker.sock traefik:v3.6.2 --providers.docker
   ```

3. 现在，启动一个简单的 Nginx 容器，并定义 Traefik 监控的标签以配置 HTTP 路由。注意，Nginx 容器未暴露任何端口。

   ```console
   $ docker run -d --network=traefik-demo --label 'traefik.http.routers.nginx.rule=Host(`nginx.localhost`)' nginx
   ```

   容器启动后，在浏览器中打开 [http://nginx.localhost](http://nginx.localhost) 查看应用（所有基于 Chromium 的浏览器都会将 \*.localhost 请求路由到本地，无需额外配置）。

4. 启动第二个应用，使用不同的主机名。

   ```console
   $ docker run -d --network=traefik-demo --label 'traefik.http.routers.welcome.rule=Host(`welcome.localhost`)' docker/welcome-to-docker
   ```

   容器启动后，在浏览器中打开 http://welcome.localhost。你应该能看到 "Welcome to Docker" 网站。

## 在开发中使用 Traefik

现在你已经体验了 Traefik，接下来尝试在开发环境中使用它。在本示例中，你将使用一个前后端分离的示例应用。该应用栈的配置如下：

1. 所有到 /api 的请求路由到 API 服务
2. 所有到 localhost 的其他请求路由到前端客户端
3. 由于应用使用 MySQL，db.localhost 应提供 phpMyAdmin，以便在开发期间轻松访问数据库

![架构图显示 Traefik 根据请求路径将请求路由到其他容器](./images/traefik-in-development.webp)

该应用可在 GitHub 上获取：[docksamples/easy-http-routing-with-traefik](https://github.com/dockersamples/easy-http-routing-with-traefik)。

1. 在 `compose.yaml` 文件中，Traefik 使用以下配置：

   ```yaml
   services:
     proxy:
       image: traefik:v3.6.2
       command: --providers.docker
       ports:
         - 80:80
       volumes:
         - /var/run/docker.sock:/var/run/docker.sock
   ```

   注意，这与之前使用的配置基本相同，但现在使用 Compose 语法。

2. 客户端服务有以下配置，该配置将启动容器并提供标签，使其在 localhost 接收请求。

   ```yaml {hl_lines=[7,8]}
   services:
     # …
     client:
       image: nginx:alpine
       volumes:
         - "./client:/usr/share/nginx/html"
       labels:
         traefik.http.routers.client.rule: "Host(`localhost`)"
   ```

3. API 服务有类似配置，但你会注意到路由规则有两个条件 - 主机必须是 "localhost"，URL 路径必须有 "api" 前缀。由于此规则更具体，Traefik 会比客户端规则更优先评估它。

   ```yaml {hl_lines=[7,8]}
   services:
     # …
     api:
       build: ./dev/api
       volumes:
         - "./api:/var/www/html/api"
       labels:
         traefik.http.routers.api.rule: "Host(`localhost`) && PathPrefix(`/api`)"
   ```

4. 最后，`phpmyadmin` 服务配置为在主机名 "db.localhost" 接收请求。该服务还定义了环境变量以自动登录，使其更容易进入应用。

   ```yaml {hl_lines=[5,6]}
   services:
     # …
     phpmyadmin:
       image: phpmyadmin:5.2.1
       labels:
         traefik.http.routers.db.rule: "Host(`db.localhost`)"
       environment:
         PMA_USER: root
         PMA_PASSWORD: password
   ```

5. 在启动栈之前，如果 Nginx 容器仍在运行，请停止它。

就是这样。现在，你只需使用 `docker compose up` 启动 Compose 栈，所有服务和应用都将准备好进行开发。

## 向非容器化工作负载发送流量

在某些情况下，你可能希望将请求转发到未在容器中运行的应用。在以下架构图中，使用了之前相同的应用，但 API 和 React 应用现在在主机上原生运行。

![架构图显示多个组件及其之间的路由。Traefik 能够向容器化和非容器化工作负载发送请求](images/traefik-non-containerized-workload-architecture.webp)

要实现这一点，Traefik 需要使用另一种方法来配置自身。[文件提供者](https://doc.traefik.io/traefik/providers/file/) 允许你通过 YAML 文档定义路由规则。以下是一个示例文件：

```yaml
http:
  routers:
    native-api:
      rule: "Host(`localhost`) && PathPrefix(`/api`)"
      service: native-api
    native-client:
      rule: "Host(`localhost`)"
      service: native-client

  services:
    native-api:
      loadBalancer:
        servers:
          - url: "http://host.docker.internal:3000/"
    native-client:
      loadBalancer:
        servers:
          - url: "http://host.docker.internal:5173/"
```

此配置表示对 `localhost/api` 的请求将被转发到名为 `native-api` 的服务，然后该服务将请求转发到 http://host.docker.internal:3000。主机名 `host.docker.internal` 是 Docker Desktop 提供的，用于将请求发送到主机。

有了此文件，Traefik 的 Compose 配置只需更改一处。具体有两个变化：

1. 配置文件挂载到 Traefik 容器中（确切的目标路径由你决定）
2. `command` 更新为添加文件提供者并指向配置文件的位置

```yaml
services:
  proxy:
    image: traefik:v3.6.2
    command: --providers.docker --providers.file.filename=/config/traefik-config.yaml --api.insecure
    ports:
      - 80:80
      - 8080:8080
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./dev/traefik-config.yaml:/config/traefik-config.yaml
```

### 启动示例应用

要运行将请求从 Traefik 转发到原生运行应用的示例应用，请按以下步骤操作：

1. 如果 Compose 栈仍在运行，请使用以下命令停止它：

   ```console
   $ docker compose down
   ```

2. 使用提供的 `compose-native.yaml` 文件启动应用：

   ```console
   $ docker compose -f compose-native.yaml up
   ```

   打开 [http://localhost](http://localhost) 会返回 502 Bad Gateway，因为其他应用尚未运行。

3. 通过运行以下步骤启动 API：

   ```console
   cd api
   yarn install
   yarn dev
   ```

4. 在新终端中（从项目根目录开始）运行以下步骤启动前端：

   ```console
   cd client
   yarn install
   yarn dev
   ```

5. 在 [http://localhost](http://localhost) 打开应用。你应该能看到一个从 [http://localhost/api/messages](http://localhost/api/messages) 获取消息的应用。你也可以打开 [http://db.localhost](http://db.localhost) 直接从 Mongo 数据库查看或调整可用消息。Traefik 将确保请求被正确路由到正确的容器或应用。

6. 完成后，运行 `docker compose down` 停止容器，并按 `ctrl+c` 停止 Yarn 应用。

## 回顾

运行多个服务不必需要复杂的端口配置和良好的记忆力。使用 Traefik 等工具，可以轻松启动所需服务并轻松访问它们 - 无论是应用本身的服务（如前端和后端），还是用于额外开发工具的服务（如 phpMyAdmin）。