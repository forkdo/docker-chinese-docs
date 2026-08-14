# Deno 语言专项指南


这份 Deno 入门指南将教你如何使用 Docker 创建一个容器化的 Deno 应用。

> **致谢**
>
> Docker 在此感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 对本指南的贡献。

## 你将学到什么？

- 使用 Docker 容器化并运行 Deno 应用
- 使用容器搭建本地环境来开发 Deno 应用
- 使用 Docker Compose 运行应用。

## 前提条件

- 假定你对 JavaScript 有基本了解。
- 你需要熟悉容器、镜像、Dockerfile 等 Docker 概念。如果你是 Docker 新手，可以从
  [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md)指南开始。

完成 Deno 入门模块后，你应该能够参照本指南提供的示例和说明，容器化你自己的 Deno 应用。

首先从容器化一个现有的 Deno 应用开始。

## Containerize a Deno application（容器化 Deno 应用）

### 前提条件

- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git
  客户端，但你可以使用任意客户端。

### 概述

长期以来，Node.js 一直是服务端 JavaScript 应用的首选运行时。然而近年来出现了新的替代
运行时，其中包括 [Deno](https://deno.land/)。与 Node.js 一样，Deno 是 JavaScript 和
TypeScript 运行时，但它采用了全新的思路，具备现代化的安全特性、内置标准库以及对
TypeScript 的原生支持。

为什么要用 Docker 来开发 Deno 应用？拥有多种运行时选择令人兴奋，但要在各种环境中一致地
管理多个运行时及其依赖却相当棘手。这正是 Docker 展现价值的地方。使用容器按需创建和销毁
环境，可以简化运行时管理并确保一致性。此外，随着 Deno 不断成长演进，Docker 有助于建立
可靠、可复现的开发环境，最大限度减少环境搭建的困难并简化工作流。

### 获取示例应用

克隆本指南使用的示例应用。打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/dockersamples/docker-deno.git && cd docker-deno
```

现在你的 `deno-docker` 目录中应该有以下内容。

```text
├── deno-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── server.ts
│ └── README.md
```

### 了解示例应用

这个示例应用是一个简单的 Deno 应用，它使用 Oak 框架创建了一个返回 JSON 响应的简单 API。
应用监听 8000 端口，当你在浏览器中访问该应用时会返回消息 `{"Status" : "OK"}`。

```typescript
// server.ts
import { Application, Router } from "https://deno.land/x/oak@v12.0.0/mod.ts";

const app = new Application();
const router = new Router();

// Define a route that returns JSON
router.get("/", (context) => {
  context.response.body = { Status: "OK" };
  context.response.type = "application/json";
});

app.use(router.routes());
app.use(router.allowedMethods());

console.log("Server running on http://localhost:8000");
await app.listen({ port: 8000 });
```

### 创建 Dockerfile

在创建 Dockerfile 之前，你需要选择一个基础镜像。你可以使用
[Deno 官方 Docker 镜像](https://hub.docker.com/r/denoland/deno)，或者使用
[Hardened Image 目录](https://hub.docker.com/hardened-images/catalog)中的
Docker Hardened Image（DHI）。

选择 DHI 的优势在于获得一个轻量且安全的生产就绪镜像。更多信息参阅
[Docker Hardened Images](https://docs.docker.com/dhi/)。

**Using Docker Hardened Images**



Deno 的 Docker Hardened Images（DHI）可在
[Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog/dhi/deno)
中获取。你可以直接从 `dhi.io` 镜像仓库拉取 DHI。

1. 登录 DHI 镜像仓库：

   ```console
   $ docker login dhi.io
   ```

2. 拉取 Deno DHI，即 `dhi.io/deno:2`。本例中的标签（`2`）表示 Deno 最新的 2.x 版本。

   ```console
   $ docker pull dhi.io/deno:2
   ```

其他可用版本请参阅[目录](https://hub.docker.com/hardened-images/catalog/dhi/deno)。

```dockerfile
# Use the DHI Deno image as the base image
FROM dhi.io/deno:2

# Set the working directory
WORKDIR /app

# Copy server code into the container
COPY server.ts .

# Set permissions (optional but recommended for security)
USER deno

# Expose port 8000
EXPOSE 8000

# Run the Deno server
CMD ["run", "--allow-net", "server.ts"]
```

**Using the official image**



使用官方 Docker 镜像很简单。在下面的 Dockerfile 中，你会看到 `FROM` 指令使用
`denoland/deno:latest` 作为基础镜像。

这是 Deno 的官方镜像，可[在 Docker Hub 上获取](https://hub.docker.com/r/denoland/deno)。

```dockerfile
# Use the official Deno image
FROM denoland/deno:latest

# Set the working directory
WORKDIR /app

# Copy server code into the container
COPY server.ts .

# Set permissions (optional but recommended for security)
USER deno

# Expose port 8000
EXPOSE 8000

# Run the Deno server
CMD ["run", "--allow-net", "server.ts"]
```



除了指定基础镜像，这个 Dockerfile 还：

- 把容器中的工作目录设为 `/app`。
- 把 `server.ts` 复制到容器中。
- 把用户设为 `deno`，以非 root 用户身份运行应用。
- 暴露 8000 端口，以允许流量访问应用。
- 使用 `CMD` 指令运行 Deno 服务器。
- 使用 `--allow-net` 标志允许应用进行网络访问。`server.ts` 文件使用 Oak 框架创建了一个
  监听 8000 端口的简单 API。

### 运行应用

确保你处于 `deno-docker` 目录中。在终端运行以下命令来构建并运行应用。

```console
$ docker compose up --build
```

打开浏览器访问 [http://localhost:8000](http://localhost:8000) 查看应用。你会在浏览器中
看到消息 `{"Status" : "OK"}`。

在终端中按 `ctrl`+`c` 停止应用。

#### 在后台运行应用

你可以加上 `-d` 选项，让应用与终端分离后运行。在 `deno-docker` 目录中，于终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器访问 [http://localhost:8000](http://localhost:8000) 查看应用。

在终端中运行以下命令停止应用。

```console
$ docker compose down
```

## 使用容器进行 Deno 开发

### 前提条件

完成 [Containerize a Deno application](#containerize-a-deno-application)。

### 概述

在本节中，你将学习如何为容器化应用搭建开发环境。这包括：

- 配置 Compose，使其在你编辑并保存代码时自动更新正在运行的 Compose 服务

### 获取示例应用

克隆本指南使用的示例应用。打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/dockersamples/docker-deno.git && cd docker-deno
```

### 自动更新服务

使用 Compose Watch，在你编辑并保存代码时自动更新正在运行的 Compose 服务。有关
Compose Watch 的更多细节，参阅[使用 Compose
Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开你的 `compose.yml` 文件，然后添加 Compose Watch 指令。
下面的示例展示了如何把 Compose Watch 添加到 `compose.yml` 文件中。

```yaml {hl_lines="9-12",linenos=true}
services:
  server:
    image: deno-server
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    develop:
      watch:
        - action: rebuild
          path: .
```

运行以下命令，以 Compose Watch 方式运行你的应用。

```console
$ docker compose watch
```

现在，如果你修改 `server.ts`，就能实时看到变化，而无需重新构建镜像。

要测试这一点，用你喜欢的文本编辑器打开 `server.ts` 文件，把消息从 `{"Status" : "OK"}`
改为 `{"Status" : "Updated"}`。保存文件并刷新浏览器中的 `http://localhost:8000`。
你应该会看到更新后的消息。

在终端中按 `ctrl+c` 停止应用。

### 小结

在本节中，你还学习了如何使用 Compose Watch，在更新代码时自动重新构建并运行容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose file watch](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

