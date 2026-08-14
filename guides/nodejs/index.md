# Node.js 语言专项指南


[Node.js](https://nodejs.org/en) 是一个用于构建服务器端应用的 JavaScript 运行时。本指南介绍如何使用 Docker 容器化一个 TypeScript 编写的 Node.js 应用，从一个简单的 Express API 开始，逐步添加数据库等功能。

本指南侧重于后端 Node.js API。如果您正在构建独立的前端应用，Docker 提供了针对 [React.js](/guides/reactjs/)、[Vue.js](/guides/vuejs/)、[Angular](/guides/angular/) 和 [Next.js](/guides/nextjs/) 的专门指南。

> **致谢**
>
> Docker 感谢 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 对本指南的贡献。

## 您将学到什么？

在本指南中，您将学习如何：

- 使用 Docker 容器化并运行 Node.js 应用。
- 使用容器搭建本地开发环境。
- 在 Docker 容器内运行测试。

首先从容器化一个 Node.js 应用开始。

## 前提条件

- 对 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 和 [TypeScript](https://www.typescriptlang.org/) 有基本了解。
- 对 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm) 有基本了解。
- 熟悉镜像、容器、Dockerfile 等 Docker 概念。如果您是 Docker 新手，请从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

## 容器化一个 Node.js 应用

### 前提条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您熟悉基本的 Docker 概念。如果您是 Docker 新手，请从 [入门](/get-started/introduction/) 开始。

### 概述

容器化您的应用意味着将其与依赖、配置和运行时一起打包成一个可移植的单元，称为容器镜像。运行该镜像会创建一个容器，这是一个在任何机器上都表现一致的隔离进程，无论是您的笔记本、CI 运行器还是生产服务器。

在本节中，您将容器化一个简单的用 TypeScript 编写的 [Express.js](https://expressjs.com/) API。您将编写一个描述如何构建镜像的 `Dockerfile`，添加一个定义 Docker 如何运行容器的 `compose.yaml` 文件，然后用一条命令构建并启动应用。

您将使用 [Docker Hardened Images](/dhi/) 作为基础。这些是由 Docker 维护的最小、安全的 Node.js 镜像。

本指南侧重于后端 Node.js API。如果您正在构建独立的前端应用，Docker 提供了针对 [React.js](/guides/reactjs/)、[Vue.js](/guides/vuejs/)、[Angular](/guides/angular/) 和 [Next.js](/guides/nextjs/) 的专门指南。

### 创建应用

示例应用是一个最小的 Express API，具有一个返回 JSON 问候语的单端点。在一个新的 `nodejs-docker-example` 目录中创建以下文件。要一次性创建所有文件，请在文件浏览器中切换到 **Scaffold script** 标签页并复制 shell 命令。

**`nodejs-docker-example/`**

`src/index.ts` (new):

```typescript
// 一个最小的 Express 应用。
// 根端点 (GET /) 返回一个 JSON 问候语。
// 框架参考见 https://expressjs.com/

import express, { type Request, type Response } from "express";

const app = express();
const port = parseInt(process.env.PORT ?? "3000", 10);

app.get("/", (_req: Request, res: Response) => {
  res.json({ message: "Hello World" });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```

`package.json` (new):

```json
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
```

`tsconfig.json` (new):

```json
{
  // Node.js 应用的 TypeScript 编译器配置。
  // 将 src/ 编译为 dist/，作为面向 ES2022 的 CommonJS 模块。
  // 所有选项见 https://www.typescriptlang.org/tsconfig/

  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

`.gitignore` (new):

```text
# Git 应忽略的文件和目录。涵盖 Node.js 依赖、
# TypeScript 构建输出、环境文件和常见编辑器产物。
# 语法参考见 https://git-scm.com/docs/gitignore

node_modules/
dist/
.env
*.log
.DS_Store
coverage/
db/password.txt
```



如果您已安装 Node.js，并希望在容器化之前验证应用可用，可以在本地运行它。

以热重载开发模式运行：

```console
$ npm install
$ npm run dev
```

运行编译后的生产构建（与 Dockerfile 所做的一致）：

```console
$ npm install
$ npm run build
$ npm start
```

然后在浏览器中打开 [http://localhost:3000](http://localhost:3000)。您应该看到 `{"message":"Hello World"}`。

如果您没有安装 Node.js，请跳到下一步。其余步骤在容器中运行应用，无需本地 Node.js。

### 创建 Docker 资产

登录 DHI 镜像仓库，以便 Docker 在构建期间能够拉取 Node.js 基础镜像。可用的 Node.js 镜像列在 [目录](https://hub.docker.com/hardened-images/catalog/dhi/node) 中。

```console
$ docker login dhi.io
```

将以下三个文件添加到您的 `nodejs-docker-example` 目录。`Dockerfile` 描述如何构建镜像，`compose.yaml` 定义 Docker 如何运行容器，`.dockerignore` 将不需要的文件排除在构建上下文之外。

> [!TIP]
>
> [Gordon](/ai/gordon/)（Docker 的 AI 助手）可以为您的项目生成 Docker 资产。请 Gordon 为您创建适配您应用的 Dockerfile、Compose 文件和 `.dockerignore`。

**`nodejs-docker-example/`**

`src/index.ts`:

```typescript
// 一个最小的 Express 应用。
// 根端点 (GET /) 返回一个 JSON 问候语。
// 框架参考见 https://expressjs.com/

import express, { type Request, type Response } from "express";

const app = express();
const port = parseInt(process.env.PORT ?? "3000", 10);

app.get("/", (_req: Request, res: Response) => {
  res.json({ message: "Hello World" });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```

`package.json`:

```json
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
```

`tsconfig.json`:

```json
{
  // Node.js 应用的 TypeScript 编译器配置。
  // 将 src/ 编译为 dist/，作为面向 ES2022 的 CommonJS 模块。
  // 所有选项见 https://www.typescriptlang.org/tsconfig/

  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

`Dockerfile` (new):

```dockerfile
# syntax=docker/dockerfile:1

# 本文件中的注释可帮助您入门。
# 如需更多帮助，请访问 Dockerfile 参考指南：
# https://docs.docker.com/go/dockerfile-reference/

# 本 Dockerfile 使用 Docker Hardened Images (DHI) 以增强安全性。
# 更多信息见 https://docs.docker.com/dhi/

# 构建阶段：安装所有依赖并编译 TypeScript。
FROM dhi.io/node:24-alpine3.23-dev AS builder

WORKDIR /app

# 将安装依赖作为单独的步骤，以利用 Docker 的缓存。
# 利用到 /root/.npm 的缓存挂载来加速后续构建。
# 利用到 package.json 的绑定挂载，避免将其复制到该层中。
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install
# 在本地运行 npm install 生成 package-lock.json 后，切换到 npm ci 并绑定这两个文件：
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci

# 将源代码复制到容器中并编译 TypeScript。
COPY . .
RUN npm run build


# 依赖阶段：仅安装生产依赖。
FROM dhi.io/node:24-alpine3.23-dev AS deps

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install --omit=dev
# 在本地运行 npm install 生成 package-lock.json 后，切换到 npm ci 并绑定这两个文件：
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci --omit=dev


# 运行阶段：包含已编译应用和生产依赖的最小运行时镜像。
FROM dhi.io/node:24-alpine3.23 AS runner

ENV PATH=/app/node_modules/.bin:$PATH

WORKDIR /app

COPY --from=deps --chown=node:node /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/dist ./dist

# 暴露应用监听的端口。
EXPOSE 3000

# 运行应用。
CMD ["node", "dist/index.js"]
```

`compose.yaml` (new):

```yaml
# 本文件中的注释可帮助您入门。
# 如需更多帮助，请访问 Docker Compose 参考指南：
# https://docs.docker.com/go/compose-spec-reference/

# 这里的指令将您的应用定义为名为 "server" 的服务。
# 该服务从当前目录中的 Dockerfile 构建。
# 您可以在此处添加应用可能依赖的其他服务，如数据库或缓存。
# 示例见 Awesome Compose 仓库：
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 3000:3000
```

`.dockerignore` (new):

```text
# 在此处包含您不希望被复制到容器中的任何文件或目录
# （例如本地构建产物、临时文件等）。
#
# 如需更多帮助，请访问 .dockerignore 文件参考指南：
# https://docs.docker.com/go/build-context-dockerignore/

node_modules/
dist/
.env
.git
.gitignore
.DS_Store
npm-debug.log*
coverage/
db/
```

`.gitignore`:

```text
# Git 应忽略的文件和目录。涵盖 Node.js 依赖、
# TypeScript 构建输出、环境文件和常见编辑器产物。
# 语法参考见 https://git-scm.com/docs/gitignore

node_modules/
dist/
.env
*.log
.DS_Store
coverage/
db/password.txt
```



`Dockerfile` 使用三个阶段。`builder` 阶段安装所有依赖并编译 TypeScript。`deps` 阶段全新安装仅生产依赖。`runner` 阶段将编译输出和生产 node_modules 复制到一个仅包含 Node.js 的最小运行时镜像中。

要了解每个文件的更多信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

### 运行应用

在 `nodejs-docker-example` 目录中，在终端运行以下命令。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:3000](http://localhost:3000) 查看应用。您应该看到 `{"message":"Hello World"}`。

在终端中按 `ctrl`+`c` 停止应用。

#### 在后台运行应用

您可以通过添加 `-d` 选项使应用脱离终端运行。在 `nodejs-docker-example` 目录中，在终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，在 [http://localhost:3000](http://localhost:3000) 查看应用。

在终端中运行以下命令停止应用。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/)。

## 使用容器进行 Node.js 开发

### 前提条件

完成 [容器化一个 Node.js 应用](#containerize-a-nodejs-application)。

### 概述

一旦您的应用在容器中运行，下一步就是让容器成为您日常开发工作流的一部分。代码更改应能快速体现，并且应用所依赖的服务（如数据库）应与应用一同运行。

在本节中，您将通过把 `builder` 阶段重命名为 `dev` 并将 Compose 指向它，来调整 Dockerfile 以用于本地开发。您还将更新应用以连接到 PostgreSQL 数据库，向 `compose.yaml` 添加数据库服务，在命名卷中持久化数据，启用 Compose Watch 以便编辑器中的更改无需手动重建即可被拾取，并设置 Node.js 调试以便您可以附加 VS Code 或 Chrome DevTools 到运行中的容器。

### 更新应用

您将更新应用以连接到 PostgreSQL 数据库。继续在您的 `nodejs-docker-example` 目录中工作。

将 `src/index.ts` 和 `package.json` 替换为以下内容。文件浏览器仅显示此步骤中更改的文件。

> [!NOTE]
>
> 此步骤之后应用还不会运行。它尝试连接一个不存在的 PostgreSQL 数据库。接下来的两节将添加数据库服务以及一起运行所有内容所需的 Docker 配置。

**`nodejs-docker-example/`**

`src/index.ts` (modified):

```typescript
// 由 PostgreSQL 数据库支撑的 Express 应用。
// 在启动时创建一个 heroes 表。
// 端点：GET /（问候）、GET /health（健康检查）、POST /heroes/（创建）、GET /heroes/（列表）。
// 参见 https://expressjs.com/ 和 https://node-postgres.com/

import express, { type Request, type Response } from "express";
import { Pool } from "pg";
import { readFileSync } from "fs";

const app = express();
const port = parseInt(process.env.PORT ?? "3000", 10);

app.use(express.json());

function getPassword(): string {
  const passwordFile = process.env.POSTGRES_PASSWORD_FILE;
  if (passwordFile) {
    return readFileSync(passwordFile, "utf8").trim();
  }
  return process.env.POSTGRES_PASSWORD ?? "";
}

const pool = new Pool({
  host: process.env.POSTGRES_SERVER,
  port: 5432,
  database: process.env.POSTGRES_DB,
  user: process.env.POSTGRES_USER,
  password: getPassword(),
});

pool
  .query(
    `CREATE TABLE IF NOT EXISTS heroes (
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      secret_name TEXT NOT NULL,
      age INTEGER
    )`,
  )
  .catch(console.error);

app.get("/", (_req: Request, res: Response) => {
  res.json({ message: "Hello World" });
});

app.get("/health", (_req: Request, res: Response) => {
  res.json({ status: "ok" });
});

app.post("/heroes/", async (req: Request, res: Response) => {
  const { name, secret_name, age } = req.body as {
    name: string;
    secret_name: string;
    age?: number;
  };
  const result = await pool.query(
    "INSERT INTO heroes (name, secret_name, age) VALUES ($1, $2, $3) RETURNING *",
    [name, secret_name, age],
  );
  res.json(result.rows[0]);
});

app.get("/heroes/", async (_req: Request, res: Response) => {
  const result = await pool.query("SELECT * FROM heroes");
  res.json(result.rows);
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```

`package.json` (modified):

```json
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2",
    "pg": "^8.16.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "@types/pg": "^8.11.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
```



### 更新 Docker 资产

将 `Dockerfile` 和 `compose.yaml` 替换为以下内容。

**`nodejs-docker-example/`**

`Dockerfile` (modified):

```dockerfile
# syntax=docker/dockerfile:1

# 本文件中的注释可帮助您入门。
# 如需更多帮助，请访问 Dockerfile 参考指南：
# https://docs.docker.com/go/dockerfile-reference/

# 本 Dockerfile 使用 Docker Hardened Images (DHI) 以增强安全性。
# 更多信息见 https://docs.docker.com/dhi/

# 开发阶段：安装所有依赖，编译 TypeScript，并
# 以热重载方式提供服务。在开发中通过 compose.yaml 直接使用。
FROM dhi.io/node:24-alpine3.23-dev AS dev

WORKDIR /app

# 将安装依赖作为单独的步骤，以利用 Docker 的缓存。
# 利用到 /root/.npm 的缓存挂载来加速后续构建。
# 利用到 package.json 的绑定挂载，避免将其复制到该层中。
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install
# 在本地运行 npm install 生成 package-lock.json 后，切换到 npm ci 并绑定这两个文件：
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci

# 将源代码复制到容器中并编译 TypeScript。
COPY . .
RUN npm run build

# 暴露应用监听的端口。
EXPOSE 3000

# 以开发模式运行应用。
CMD ["npm", "run", "dev"]


# 依赖阶段：仅安装生产依赖。
FROM dhi.io/node:24-alpine3.23-dev AS deps

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install --omit=dev
# 在本地运行 npm install 生成 package-lock.json 后，切换到 npm ci 并绑定这两个文件：
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci --omit=dev


# 运行阶段：包含已编译应用和生产依赖的最小运行时镜像。
FROM dhi.io/node:24-alpine3.23 AS runner

ENV PATH=/app/node_modules/.bin:$PATH

WORKDIR /app

COPY --from=deps --chown=node:node /app/node_modules ./node_modules
COPY --from=dev --chown=node:node /app/dist ./dist

# 暴露应用监听的端口。
EXPOSE 3000

# 运行应用。
CMD ["node", "dist/index.js"]
```

`compose.yaml` (modified):

```yaml
services:
  # 应用服务。`target: dev` 行构建开发镜像
  # （包含 tsx 和开发工具）；Dockerfile 的 runner 阶段在开发中不使用。
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
```



#### 关于这些更改

容器化阶段的 `builder` 阶段被重命名为 `dev`，并增加了 `EXPOSE 3000` 和 `CMD ["npm", "run", "dev"]`，后者运行 `tsx watch` 以实现热重载。`deps` 和 `runner` 阶段保持不变。

在 `compose.yaml` 中，新的 `target: dev` 行告诉 Compose 在开发期间构建并运行 `dev` 阶段。与生产镜像不同，开发镜像包含 `tsx` 和其他开发工具。如果您需要在运行中的生产容器中获取 shell，请改用 [Docker Debug](/reference/cli/docker/debug/)。

构建步骤运行 `tsc`，它将每个 TypeScript 文件编译为对应的 JavaScript 文件。[esbuild](https://esbuild.github.io/) 是一个流行的替代方案，它把所有内容打包成单个输出文件并且构建速度显著更快。要切换，请将 `package.json` 中的 `tsc` 调用替换为 esbuild 命令，并更新 `runner` 阶段中的 `COPY --from=dev` 路径以匹配 esbuild 的输出。

### 添加本地数据库并持久化数据

您可以使用容器来搭建本地服务，如数据库。在本节中，您将更新 `compose.yaml` 文件以定义一个数据库服务和一个用于持久化数据的卷，并添加一个保存数据库密码的 `db/password.txt` 文件。

**`nodejs-docker-example/`**

`compose.yaml` (modified):

```yaml
services:
  # 应用服务。`target: dev` 行构建开发镜像
  # （包含 tsx 和开发工具）；Dockerfile 的 runner 阶段在开发中不使用。
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
  # 数据库服务。从挂载在 /run/secrets/db-password 的 Docker secret 读取密码。
  # Compose 通过 server 的 depends_on 等待健康检查通过后再启动 server。
  db:
    image: dhi.io/postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

`db/password.txt` (new):

```text
mysecretpassword
```



> [!NOTE]
>
> 要了解 Compose 文件中指令的更多信息，请参阅 [Compose 文件参考](/reference/compose-file/)。

现在，运行以下 `docker compose up` 命令启动您的应用。

```console
$ docker compose up --build
```

现在测试您的 API 端点。打开一个新的终端，使用 curl 命令向服务器发起请求。

使用 POST 请求创建一个对象：

```console
$ curl -X 'POST' \
  'http://localhost:3000/heroes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "my hero",
  "secret_name": "austing",
  "age": 12
}'
```

您应该收到以下响应：

```json
{
  "id": 1,
  "name": "my hero",
  "secret_name": "austing",
  "age": 12
}
```

现在发起一个 GET 请求：

```console
$ curl http://localhost:3000/heroes/
```

您应该收到相同的响应，因为它是数据库中唯一的对象。

在终端中按 `ctrl`+`c` 停止应用。

### 自动更新服务

使用 Compose Watch 在您编辑并保存代码时自动更新运行中的 Compose 服务。有关 Compose Watch 的更多详情，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开您的 `compose.yaml` 文件，并添加高亮的 Compose Watch 指令。

**`nodejs-docker-example/`**

`compose.yaml` (modified):

```yaml
services:
  # 应用服务。`target: dev` 行构建开发镜像
  # （包含 tsx 和开发工具）；Dockerfile 的 runner 阶段在开发中不使用。
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
  db:
    image: dhi.io/postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```



运行以下命令以使用 Compose Watch 运行应用。

```console
$ docker compose watch
```

在终端中，curl 应用以获取响应。

```console
$ curl http://localhost:3000
{"message":"Hello World"}
```

现在您本地机器上对应用源文件的任何更改都会立即反映到运行中的容器中。

在 IDE 或文本编辑器中打开 `nodejs-docker-example/src/index.ts`，并通过添加几个感叹号来更新 `Hello World` 字符串。

```diff
-  res.json({ message: 'Hello World' });
+  res.json({ message: 'Hello World!!!' });
```

保存对 `src/index.ts` 的更改，然后等待几秒钟让应用重新加载。再次 curl 应用并验证更新后的文本是否出现。

```console
$ curl http://localhost:3000
{"message":"Hello World!!!"}
```

在终端中按 `ctrl`+`c` 停止应用。

### 调试您的应用

`tsx watch` 支持 Node.js inspector 协议，因此您可以从 VS Code 或 Chrome DevTools 附加调试器，并直接在 TypeScript 源文件中设置断点。

更新 `package.json` 中的 `dev` 脚本以启动 inspector。`--inspect=0.0.0.0:9229` 标志告诉 Node.js 在所有网络接口的 9229 端口监听调试器连接。使用 `0.0.0.0` 而不是 `localhost` 是必要的，这样调试器才能从容器的外部访问。同时在 `compose.yaml` 中暴露调试端口，并添加一个 `.vscode/launch.json` 文件，告诉 VS Code 如何附加到运行中的 inspector。

**`nodejs-docker-example/`**

`package.json` (modified):

```json
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch --inspect=0.0.0.0:9229 src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2",
    "pg": "^8.16.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "@types/pg": "^8.11.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
```

`.vscode/launch.json` (new):

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Docker Container",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "address": "localhost",
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "/app",
      "protocol": "inspector",
      "restart": true,
      "sourceMaps": true,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

`compose.yaml` (modified):

```yaml
services:
  # 应用服务。`target: dev` 行构建开发镜像
  # （包含 tsx 和开发工具）；Dockerfile 的 runner 阶段在开发中不使用。
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
      - 9229:9229
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
  db:
    image: dhi.io/postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```



使用更新后的配置重建并重启：

```console
$ docker compose up --build
```

当 inspector 就绪时，您会在日志中看到类似如下的一行：

```text
Debugger listening on ws://0.0.0.0:9229/...
```

#### VS Code

配置好 `.vscode/launch.json` 后，使用 Debug 面板附加调试器。

打开 Debug 面板（Windows 和 Linux 上为 `Ctrl+Shift+D`，Mac 上为 `Cmd+Shift+D`），选择 **Attach to Docker Container**，然后按 `F5`。您现在可以在 `src/` 下的 TypeScript 源文件中设置断点。

#### Chrome DevTools

您也可以在不进行任何编辑器配置的情况下，使用 Chrome 内置的 Node.js inspector。

1. 打开 Chrome 并访问 `chrome://inspect`。

2. 选择 **Configure** 并添加 `localhost:9229`。

3. 当您的 Node.js 目标出现在列表中时，选择 **inspect**。

#### 调试器故障排查

如果调试器无法连接，请验证容器是否正在运行以及端口是否正确映射：

```console
$ docker compose ps
$ docker compose logs server
```

日志应包含类似如下的一行：

```text
Debugger listening on ws://0.0.0.0:9229/...
```

如果缺少该行，请确认 `package.json` 中的 `dev` 脚本包含 `--inspect=0.0.0.0:9229`，并且 `compose.yaml` 中 `server` 服务的 `ports` 列表包含 `9229:9229`。

有关 Node.js 调试的更多详情，请参阅 [Node.js 调试指南](https://nodejs.org/en/docs/guides/debugging-getting-started)。

## 在容器中运行 Node.js 测试

### 前提条件

完成本指南的所有前面章节，从 [容器化一个 Node.js 应用](#containerize-a-nodejs-application) 开始。

### 概述

测试是构建可靠软件的核心部分。Docker 让您能够轻松地在 CI 和生产所用的相同环境中运行测试，从而在问题到达用户之前就被捕获。

在本节中，您将向项目添加 [Vitest](https://vitest.dev/) 并在本地和容器内运行测试。

### 更新应用

您将重构 `src/index.ts` 以导出 Express 的 `app` 实例，以便测试可以在不启动服务器的情况下导入它。添加一个测试文件并更新 `package.json` 以添加 Vitest 和用于 HTTP 请求的测试运行器。文件浏览器仅显示此步骤中更改的文件。

**`nodejs-docker-example/`**

`src/index.ts` (modified):

```typescript
// 由 PostgreSQL 数据库支撑的 Express 应用。
// 在启动时创建一个 heroes 表。
// 端点：GET /（问候）、GET /health（健康检查）、POST /heroes/（创建）、GET /heroes/（列表）。
// 参见 https://expressjs.com/ 和 https://node-postgres.com/

import express, { type Request, type Response } from "express";
import { Pool } from "pg";
import { readFileSync } from "fs";

export const app = express();
const port = parseInt(process.env.PORT ?? "3000", 10);

app.use(express.json());

function getPassword(): string {
  const passwordFile = process.env.POSTGRES_PASSWORD_FILE;
  if (passwordFile) {
    return readFileSync(passwordFile, "utf8").trim();
  }
  return process.env.POSTGRES_PASSWORD ?? "";
}

const pool = new Pool({
  host: process.env.POSTGRES_SERVER,
  port: 5432,
  database: process.env.POSTGRES_DB,
  user: process.env.POSTGRES_USER,
  password: getPassword(),
});

if (process.env.POSTGRES_SERVER) {
  pool
    .query(
      `CREATE TABLE IF NOT EXISTS heroes (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        secret_name TEXT NOT NULL,
        age INTEGER
      )`,
    )
    .catch(console.error);
}

app.get("/", (_req: Request, res: Response) => {
  res.json({ message: "Hello World" });
});

app.get("/health", (_req: Request, res: Response) => {
  res.json({ status: "ok" });
});

app.post("/heroes/", async (req: Request, res: Response) => {
  const { name, secret_name, age } = req.body as {
    name: string;
    secret_name: string;
    age?: number;
  };
  const result = await pool.query(
    "INSERT INTO heroes (name, secret_name, age) VALUES ($1, $2, $3) RETURNING *",
    [name, secret_name, age],
  );
  res.json(result.rows[0]);
});

app.get("/heroes/", async (_req: Request, res: Response) => {
  const result = await pool.query("SELECT * FROM heroes");
  res.json(result.rows);
});

// 仅当直接运行此文件时才启动服务器。
if (require.main === module) {
  app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
  });
}
```

`src/index.test.ts` (new):

```typescript
// Express 应用的单元测试。
// 在不启动服务器的情况下测试根端点。
// 测试框架参考见 https://vitest.dev/

import { describe, it, expect } from "vitest";
import request from "supertest";
import { app } from "./index";

describe("GET /", () => {
  it("returns a JSON greeting", async () => {
    const response = await request(app).get("/");
    expect(response.status).toBe(200);
    expect(response.body).toEqual({ message: "Hello World" });
  });
});
```

`package.json` (modified):

```json
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts",
    "test": "vitest run"
  },
  "dependencies": {
    "express": "^4.21.2",
    "pg": "^8.16.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "@types/pg": "^8.11.0",
    "supertest": "^7.0.0",
    "@types/supertest": "^6.0.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3",
    "vitest": "^3.0.0"
  }
}
```



### 在本地运行测试

运行以下命令在本地运行测试：

```console
$ npm install
$ npm test
```

您应该看到类似如下的输出：

```console
 RUN  v3.0.0 /app

 ✓ src/index.test.ts (1)
   ✓ GET / (1)
     ✓ returns a JSON greeting

 Test Files  1 passed (1)
      Tests  1 passed (1)
   Start at  12:00:00
   Duration  500ms
```

### 在容器中运行测试

使用 Dockerfile 的 dev 阶段运行测试：

```console
$ docker compose run --build --rm --no-deps server npm test
```

`--no-deps` 标志跳过启动数据库，因为单元测试不需要它。`--rm` 标志在测试完成后移除容器。

您应该看到与本地运行相同的测试输出。

### 在构建时运行测试

要在 Docker 构建过程中运行测试，请在 Dockerfile 中 dev 阶段之后添加一个 `test` 阶段。

```dockerfile {hl_lines="32-36"}
FROM dhi.io/node:24-alpine3.23-dev AS dev

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "dev"]


FROM dhi.io/node:24-alpine3.23-dev AS deps
WORKDIR /app
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install --omit=dev

FROM dhi.io/node:24-alpine3.23 AS runner
ENV PATH=/app/node_modules/.bin:$PATH
WORKDIR /app
COPY --from=deps --chown=node:node /app/node_modules ./node_modules
COPY --from=dev --chown=node:node /app/dist ./dist

EXPOSE 3000
CMD ["node", "dist/index.js"]


FROM dev AS test

ENV CI=true

CMD ["npm", "test"]
```

然后构建并运行 test 阶段：

```console
$ docker build --target test -t nodejs-app-test .
$ docker run --rm nodejs-app-test
```

### 总结

在本节中，您学习了如何在本地开发和容器内运行测试。

相关信息：

- [Dockerfile 参考](/reference/dockerfile/)
- [Compose 文件参考](/compose/compose-file/)
- [`docker compose run` CLI 参考](/reference/cli/docker/compose/run/)
