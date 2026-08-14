# 使用 Claude Code 与 Docker MCP Toolkit 生成 Docker Compose 文件


本指南介绍如何把 Claude Code 与 Docker MCP Toolkit 结合使用，让 Claude 能够实时搜索
Docker Hub，并从自然语言生成完整的 `docker-compose.yaml`。

你不必手动编写 YAML 或查找镜像标签，只需一次性描述你的技术栈——Claude 会使用模型上下文
协议（MCP）查询 Docker Hub 并构建一个可用于生产的 Compose 文件。

在本指南中，你将学会：

- 在 Docker Desktop 中启用 Docker MCP Toolkit  
- 添加 Docker Hub MCP 服务器  
- 把 Claude Code 连接到 MCP Gateway（图形界面或命令行）  
- 在 Claude 内部验证 MCP 连通性  
- 让 Claude 为一个 Node.js + PostgreSQL 应用生成并保存 Compose 文件  
- 用 `docker compose up` 立即部署  

---

## 使用 Claude Code 与 Docker MCP Toolkit 从自然语言生成 Docker Compose 文件


- 准备：启用 MCP Toolkit → 添加 Docker Hub MCP 服务器 → 连接 Claude Code  
- 使用 Claude：用平实的语言描述你的技术栈  
- 自动化：Claude 通过 MCP 查询 Docker Hub 并构建完整的 `docker-compose.yaml`  
- 部署：运行 `docker compose up` → Node.js + PostgreSQL 在 `localhost:3000` 上运行  
- 收益：无需编写 YAML，无需搜索镜像。描述一次 → Claude 帮你构建。

预计用时：约 15 分钟

---

## 1. 你将构建什么

目标很简单：结合使用 Claude Code 与 Docker MCP Toolkit 来搜索 Docker Hub 镜像，并为
Node.js 和 PostgreSQL 的组合生成一个完整的 Docker Compose 文件。

模型上下文协议（MCP）在 Claude Code 与 Docker Desktop 之间架起桥梁，让 Claude 能够实时
访问 Docker 的工具。你不必在 Docker、终端命令和 YAML 编辑器之间来回切换，只需描述一次
需求，Claude 就会处理基础设施细节。

为什么这很重要：这种模式可以扩展到复杂的多服务配置、数据库迁移、网络、安全策略——全部
通过对话式提示完成。

---

## 2. 前提条件

请确保你具备：

- 已安装 Docker Desktop
- 已将 Docker Desktop 更新到支持 [MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/#setup) 的版本并启用

- 已安装 Claude Code

---

## 3. 安装 Docker Hub MCP 服务器

1. 打开 Docker Desktop  
1. 选择 **MCP Toolkit**  
1. 进入 **Catalog** 标签页  
1. 搜索 **Docker Hub**  
1. 选择 **Docker Hub** MCP 服务器
1. 添加该 MCP 服务器，然后打开 **Configuration** 标签页
1. 输入你的 Docker Hub 用户名
1. [创建一个只读的个人访问令牌](/security/access-tokens/#create-a-personal-access-token)，
   并在 **Secrets** 下输入你的访问令牌
1. 保存配置

![Docker Hub](images/genai-claude-code-mcp-catalog-docker-hub.avif "Docker Hub")

公开镜像无需凭据即可使用。对于私有仓库，你可以稍后再添加你的 Docker Hub 用户名和令牌。

![Docker Hub Secrets](images/genai-claude-code-mcp-dockerhub-secrets.avif "Docker Hub Secrets")


---

## 4. 把 Claude Code 连接到 Docker MCP Toolkit

你可以从 Docker Desktop 连接，也可以使用命令行连接。

### 方案 A：通过 Docker Desktop 连接

1. 打开 **MCP Toolkit**  
1. 进入 **Clients** 标签页  
1. 找到 Claude Code  
1. 选择 **Connect**

![Docker Connection](images/genai-claude-code-mcp-docker-connect-claude.avif)

### 方案 B：使用命令行连接

```console
$ claude mcp add MCP_DOCKER -s user -- docker mcp gateway run
```

---

## 5. 在 Claude Code 内部验证 MCP 服务器

1. 切换到你的项目文件夹：

```console
$ cd /path/to/project
```

1. 启动 Claude Code：

```console
$ claude
```

1. 在输入框中输入：

```console
/mcp
```

现在你应该会看到：

- MCP gateway（例如 `MCP_DOCKER`）
- Docker Hub MCP 服务器提供的工具

![mcp-docker](images/genai-claude-code-mcp-mcp-servers.avif)

如果没有看到，请重启 Claude Code，或检查 Docker Desktop 以确认连接状态。

---

## 6. 创建一个基础的 Node.js 应用

当 Claude Code 能够检视一个真实项目时，它生成的 Compose 文件会更准确。现在就把应用代码
准备好，以便后续智能体可以对其进行绑定挂载。

在项目文件夹中创建一个名为 `app` 的文件夹：

```console
$ mkdir app
$ cd app
$ npm init -y
$ npm install express
```

创建 `index.js`：

```console
const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Node.js, Docker, and MCP Toolkit are working together!");
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
```

在 `package.json` 中添加 start 脚本：

```console
"scripts": {
  "start": "node index.js"
}
```

应用准备好后，返回项目根目录（`cd ..`）。

---

## 7. 让 Claude Code 设计你的 Docker Compose 技术栈

把下面这段消息粘贴到 Claude Code 中：

```console
Using the Docker Hub MCP server:

Search Docker Hub for an official Node.js image and a PostgreSQL image.
Choose stable, commonly used tags such as the Node LTS version and a recent major Postgres version.

Generate a Docker Compose file (`docker-compose.yaml`) with:
- app:
  - runs on port 3000
  - bind mounts the existing ./app directory into /usr/src/app
  - sets /usr/src/app as the working directory and runs `npm install && npm start`
- db: running on port 5432 using a named volume

Include:
- Environment variables for Postgres
- A shared bridge network
- Healthchecks where appropriate
- Pin the image version using the tag + index digest
```

Claude 会通过 MCP 搜索镜像、检视 `app` 目录，并生成一个能挂载并运行你本地代码的
Compose 文件。

---

## 8. 保存生成的 Docker Compose 文件

告诉 Claude：

```console
Save the final Docker Compose file (docker-compose.yaml) into the current project directory.
```

你应该会看到类似下面的内容：

```console
services:
  app:
    image: node:<tag>
    working_dir: /usr/src/app
    volumes:
      - .:/usr/src/app
    ports:
      - "3000:3000"
    depends_on:
      - db
    networks:
      - app-net

  db:
    image: postgres:18
    environment:
      POSTGRES_USER: example
      POSTGRES_PASSWORD: example
      POSTGRES_DB: appdb
    volumes:
      - db-data:/var/lib/postgresql
    ports:
      - "5432:5432"
    networks:
      - app-net

volumes:
  db-data:

networks:
  app-net:
    driver: bridge
```

---

## 9. 运行 Docker Compose 技术栈

在项目根目录下：

```console
$ docker compose up
```

Docker 将会：

- 拉取通过 Docker Hub MCP 选定的 Node 和 Postgres 镜像  
- 创建网络和卷  
- 启动容器  

打开浏览器：

```console
http://localhost:3000
```
![Local Host](images/genai-claude-code-mcp-localhost.avif)

现在你的 Node.js 应用应该已经在运行了。

---

## 结语

把 Claude Code 与 Docker MCP Toolkit、Docker Desktop 以及 Docker Hub MCP 服务器结合起来，
你就可以用自然语言描述技术栈，并让 MCP 处理细节。这消除了上下文切换，取而代之的是由模型
上下文协议集成驱动的顺畅、有引导的工作流。

---

### 下一步

- 探索 [Docker MCP 目录](https://hub.docker.com/mcp)中提供的 220 多个 MCP 服务器
- 把 Claude Code 连接到你的数据库、内部 API 和团队工具  
- 与团队共享你的 MCP 配置，让大家的工作方式保持一致  

开发的未来不在于在各种工具之间切换，而在于让工具以简单、安全、可预测的方式协同工作。
Docker MCP Toolkit 把这样的未来带入你的日常工作流。



## 了解更多

- [浏览 MCP 目录](https://hub.docker.com/mcp)：发现容器化、经过安全加固的 MCP 服务器  
- [在 Docker Desktop 中开始使用 MCP Toolkit](https://hub.docker.com/open-desktop?url=https://open.docker.com/dashboard/mcp)：需要 4.48 或更新版本才能自动启动  
- [阅读 MCP Horror Stories 系列](https://www.docker.com/blog/mcp-horror-stories-the-supply-chain-attack/)：了解常见的 MCP 安全陷阱以及如何规避  

