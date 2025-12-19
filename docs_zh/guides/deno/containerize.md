---
title: 将 Deno 应用程序容器化
linkTitle: 容器化你的应用程序
weight: 10
keywords: deno, containerize, initialize
description: 了解如何将 Deno 应用程序容器化。
aliases:
  - /language/deno/containerize/
---

## 先决条件

* 你有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用的是基于命令行的 Git 客户端，但你可以使用任何客户端。

## 概览

长期以来，Node.js 一直是服务端 JavaScript 应用程序的首选运行时。然而，近年来出现了新的替代运行时，包括 [Deno](https://deno.land/)。与 Node.js 类似，Deno 也是一个 JavaScript 和 TypeScript 运行时，但它采用了全新的方法，具有现代安全特性、内置标准库以及对 TypeScript 的原生支持。

为什么要使用 Docker 开发 Deno 应用程序？拥有多种运行时选择令人兴奋，但在不同环境中一致地管理多个运行时及其依赖项可能很棘手。这正是 Docker 的价值所在。使用容器按需创建和销毁环境可以简化运行时管理并确保一致性。此外，随着 Deno 的不断发展，Docker 有助于建立一个可靠且可重现的开发环境，最大限度地减少设置挑战并简化工作流程。

## 获取示例应用程序

克隆示例应用程序以配合本指南使用。打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/dockersamples/docker-deno.git && cd docker-deno
```

现在你的 `deno-docker` 目录中应该包含以下内容：

```text
├── deno-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── server.ts
│ └── README.md
```

## 了解示例应用程序

示例应用程序是一个简单的 Deno 应用程序，它使用 Oak 框架创建一个返回 JSON 响应的简单 API。该应用程序监听 8000 端口，当你在浏览器中访问该应用程序时，会返回消息 `{"Status" : "OK"}`。

```typescript
// server.ts
import { Application, Router } from "https://deno.land/x/oak@v12.0.0/mod.ts";

const app = new Application();
const router = new Router();

// 定义一个返回 JSON 的路由
router.get("/", (context) => {
  context.response.body = { Status: "OK" };
  context.response.type = "application/json";
});

app.use(router.routes());
app.use(router.allowedMethods());

console.log("Server running on http://localhost:8000");
await app.listen({ port: 8000 });
```

## 创建 Dockerfile

在创建 Dockerfile 之前，你需要选择一个基础镜像。你可以使用 [Deno Docker 官方镜像](https://hub.docker.com/r/denoland/deno) 或来自 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog) 的 Docker Hardened Image (DHI)。

选择 DHI 的优势在于它是一个生产就绪的镜像，轻量且安全。更多信息，请参阅 [Docker Hardened Images](https://docs.docker.com/dhi/)。

{{< tabs >}}
{{< tab name="使用 Docker Hardened Images" >}}

Docker Hardened Images (DHIs) 在 [Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog/dhi/deno) 中提供 Deno 版本。你可以直接从 `dhi.io` 注册表拉取 DHIs。

1. 登录 DHI 注册表：

   ```console
   $ docker login dhi.io
   ```

2. 拉取 Deno DHI 作为 `dhi.io/deno:2`。此示例中的标签 (`2`) 指的是 Deno 最新 2.x 版本。

   ```console
   $ docker pull dhi.io/deno:2
   ```

有关其他可用版本，请参阅[目录](https://hub.docker.com/hardened-images/catalog/dhi/deno)。

```dockerfile
# 使用 DHI Deno 镜像作为基础镜像
FROM dhi.io/deno:2

# 设置工作目录
WORKDIR /app

# 将服务器代码复制到容器中
COPY server.ts .

# 设置权限（可选，但出于安全考虑推荐）
USER deno

# 暴露 8000 端口
EXPOSE 8000

# 运行 Deno 服务器
CMD ["run", "--allow-net", "server.ts"]
```

{{< /tab >}}
{{< tab name="使用官方镜像" >}}

使用 Docker 官方镜像很简单。在以下 Dockerfile 中，你会注意到 `FROM` 指令使用 `denoland/deno:latest` 作为基础镜像。

这是 Deno 的官方镜像。该镜像[可在 Docker Hub 上获得](https://hub.docker.com/r/denoland/deno)。

```dockerfile
# 使用官方 Deno 镜像
FROM denoland/deno:latest

# 设置工作目录
WORKDIR /app

# 将服务器代码复制到容器中
COPY server.ts .

# 设置权限（可选，但出于安全考虑推荐）
USER deno

# 暴露 8000 端口
EXPOSE 8000

# 运行 Deno 服务器
CMD ["run", "--allow-net", "server.ts"]
```

{{< /tab >}}
{{< /tabs >}}

除了指定基础镜像外，Dockerfile 还：

- 将容器中的工作目录设置为 `/app`。
- 将 `server.ts` 复制到容器中。
- 将用户设置为 `deno`，以非 root 用户身份运行应用程序。
- 暴露 8000 端口以允许访问应用程序的流量。
- 使用 `CMD` 指令运行 Deno 服务器。
- 使用 `--allow-net` 标志允许应用程序的网络访问。`server.ts` 文件使用 Oak 框架创建一个监听 8000 端口的简单 API。

## 运行应用程序

确保你在 `deno-docker` 目录中。在终端中运行以下命令来构建并运行应用程序。

```console
$ docker compose up --build
```

打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 查看应用程序。你将在浏览器中看到消息 `{"Status" : "OK"}`。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

你可以通过添加 `-d` 选项使应用程序在终端后台运行。在 `deno-docker` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 查看应用程序。

在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

## 总结

在本节中，你学习了如何使用 Docker 容器化并运行你的 Deno 应用程序。

相关信息：

 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)
 - [Docker Compose 概览](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)
 - [Docker Hardened Images](/dhi/)

## 下一步

在下一节中，你将学习如何使用容器开发你的应用程序。