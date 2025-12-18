---
title: 容器化 Deno 应用
linkTitle: 容器化你的应用
weight: 10
keywords: deno, containerize, initialize
description: 了解如何容器化 Deno 应用。
aliases:
  - /language/deno/containerize/
---

## 前置条件

* 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但你可以使用任意客户端。

## 概述

长期以来，Node.js 一直是服务端 JavaScript 应用的首选运行时。然而，近年来出现了新的替代运行时，包括 [Deno](https://deno.land/)。与 Node.js 一样，Deno 也是 JavaScript 和 TypeScript 运行时，但它采用了更现代的安全特性、内置标准库以及对 TypeScript 的原生支持。

为什么使用 Docker 开发 Deno 应用？拥有多种运行时选择令人兴奋，但在不同环境中一致地管理多个运行时及其依赖可能比较棘手。Docker 在这方面非常有价值。使用容器按需创建和销毁环境可以简化运行时管理并确保一致性。此外，随着 Deno 持续发展和演进，Docker 有助于建立可靠且可复现的开发环境，减少设置难题并简化工作流。

## 获取示例应用

克隆示例应用以配合本指南使用。打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/dockersamples/docker-deno.git && cd docker-deno
```

现在你的 `deno-docker` 目录中应包含以下内容：

```text
├── deno-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── server.ts
│ └── README.md
```

## 了解示例应用

示例应用是一个简单的 Deno 应用，使用 Oak 框架创建一个返回 JSON 响应的简单 API。应用监听 8000 端口，当在浏览器中访问时返回消息 `{"Status" : "OK"}`。

```typescript
// server.ts
import { Application, Router } from "https://deno.land/x/oak@v12.0.0/mod.ts";

const app = new Application();
const router = new Router();

// 定义返回 JSON 的路由
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

在创建 Dockerfile 之前，你需要选择一个基础镜像。你可以使用 [Deno Docker 官方镜像](https://hub.docker.com/r/denoland/deno)，或者从 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog) 中选择 Docker Hardened Image (DHI)。

选择 DHI 的优势在于它是一个生产就绪的镜像，体积轻量且安全。更多信息请参见 [Docker Hardened Images](https://docs.docker.com/dhi/)。

{{< tabs >}}
{{< tab name="使用 Docker Hardened Images" >}}
Docker Hardened Images (DHIs) 可在 [Docker Hub](https://hub.docker.com/hardened-images/catalog/dhi/deno) 上获取 Deno 版本。与使用 Docker 官方镜像不同，你必须先将 Deno 镜像镜像到你的组织中，然后将其用作基础镜像。请按照 [DHI 快速入门](/dhi/get-started/) 中的说明为 Deno 创建镜像仓库。

镜像仓库必须以 `dhi-` 开头，例如：`FROM <your-namespace>/dhi-deno:<tag>`。在以下 Dockerfile 中，`FROM` 指令使用 `<your-namespace>/dhi-deno:2` 作为基础镜像。

```dockerfile
# 使用 DHI Deno 镜像作为基础镜像
FROM <your-namespace>/dhi-deno:2

# 设置工作目录
WORKDIR /app

# 将服务器代码复制到容器中
COPY server.ts .

# 设置权限（可选，但推荐用于安全）
USER deno

# 暴露 8000 端口
EXPOSE 8000

# 运行 Deno 服务器
CMD ["run", "--allow-net", "server.ts"]
```

{{< /tab >}}
{{< tab name="使用官方镜像" >}}

使用 Docker 官方镜像非常直接。在以下 Dockerfile 中，你会注意到 `FROM` 指令使用 `denoland/deno:latest` 作为基础镜像。

这是 Deno 的官方镜像。该镜像在 [Docker Hub](https://hub.docker.com/r/denoland/deno) 上可用。

```dockerfile
# 使用官方 Deno 镜像
FROM denoland/deno:latest

# 设置工作目录
WORKDIR /app

# 将服务器代码复制到容器中
COPY server.ts .

# 设置权限（可选，但推荐用于安全）
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
- 将用户设置为 `deno`，以非 root 用户身份运行应用。
- 暴露 8000 端口以允许流量访问应用。
- 使用 `CMD` 指令运行 Deno 服务器。
- 使用 `--allow-net` 标志允许应用的网络访问。`server.ts` 文件使用 Oak 框架创建一个监听 8000 端口的简单 API。

## 运行应用

确保你位于 `deno-docker` 目录中。在终端中运行以下命令构建并运行应用：

```console
$ docker compose up --build
```

打开浏览器，访问 [http://localhost:8000](http://localhost:8000)。你将在浏览器中看到消息 `{"Status" : "OK"}`。

在终端中按 `ctrl`+`c` 停止应用。

### 在后台运行应用

你可以通过添加 `-d` 选项使应用在后台运行，与终端分离。在 `deno-docker` 目录中，终端运行以下命令：

```console
$ docker compose up --build -d
```

打开浏览器，访问 [http://localhost:8000](http://localhost:8000)。

在终端中运行以下命令停止应用：

```console
$ docker compose down
```

## 小结

在本节中，你学习了如何使用 Docker 容器化并运行 Deno 应用。

相关信息：

 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)
 - [Docker Compose 概述](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)
 - [Docker Hardened Images](/dhi/)

## 后续步骤

在下一节中，你将学习如何使用容器开发应用。