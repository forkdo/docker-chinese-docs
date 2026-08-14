# 使用 Docker Hardened Images 加固 Backstage 应用程序


本指南介绍如何使用 Docker Hardened Images（DHI）加固 Backstage 应用程序。Backstage 是一个 CNCF 开源开发者门户，被数千家组织用于管理其软件目录、模板和开发者工具。

完成本指南后，你将获得一个 Backstage 容器镜像：它是 distroless 的，默认以非 root 用户运行，并且相比标准的 `node:24-trixie-slim` 基础镜像拥有显著更少的 CVE，同时仍能支持 Backstage 所需的原生模块编译。

## 先决条件

- Docker Desktop 或启用了 BuildKit 的 Docker Engine
- 已通过 `docker login` 和 `docker login dhi.io` 认证的 Docker Hub 账户
- 使用 `@backstage/create-app` 创建的 Backstage 项目

## Backstage 为何需要定制

DHI 迁移示例涵盖了一些直接替换基础镜像即可正常运行的应用。Backstage 则不同。它使用了 `better-sqlite3` 及其他在安装时编译原生 Node.js 模块的包，这意味着构建阶段需要 `g++`、`make`、`python3` 和 `sqlite-dev`——而这些都不在基础的 `dhi.io/node` 镜像中。运行时镜像只需要被编译的原生模块所链接的共享库（`sqlite-libs`）。

这是一种常见模式。任何依赖原生插件（如 `bcrypt`、`sharp`、`sqlite3` 或 `node-canvas`）的 Node.js 应用都会面临同样的挑战。本指南中的方法适用于所有这些应用。

## 步骤 1：检查原始 Dockerfile

Backstage 官方文档推荐使用基于 `node:24-trixie-slim`（Debian）的多阶段 Dockerfile。一个典型的设置如下：

```dockerfile
# Stage 1 - Create yarn install skeleton layer
FROM node:24-trixie-slim AS packages
WORKDIR /app
COPY backstage.json package.json yarn.lock ./
COPY .yarn ./.yarn
COPY .yarnrc.yml ./
COPY packages packages
COPY plugins plugins
RUN find packages \! -name "package.json" -mindepth 2 -maxdepth 2 \
    -exec rm -rf {} \+

# Stage 2 - Install dependencies and build packages
FROM node:24-trixie-slim AS build
ENV PYTHON=/usr/bin/python3
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 g++ build-essential && \
    rm -rf /var/lib/apt/lists/*
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*
USER node
WORKDIR /app
COPY --from=packages --chown=node:node /app .
RUN --mount=type=cache,target=/home/node/.cache/yarn,sharing=locked,uid=1000,gid=1000 \
    yarn install --immutable
COPY --chown=node:node . .
RUN yarn tsc
RUN yarn --cwd packages/backend build
RUN mkdir packages/backend/dist/skeleton packages/backend/dist/bundle \
    && tar xzf packages/backend/dist/skeleton.tar.gz \
       -C packages/backend/dist/skeleton \
    && tar xzf packages/backend/dist/bundle.tar.gz \
       -C packages/backend/dist/bundle

# Stage 3 - Build the actual backend image
FROM node:24-trixie-slim
ENV PYTHON=/usr/bin/python3
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 g++ build-essential && \
    rm -rf /var/lib/apt/lists/*
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*
USER node
WORKDIR /app
COPY --from=build --chown=node:node /app/.yarn ./.yarn
COPY --from=build --chown=node:node /app/.yarnrc.yml ./
COPY --from=build --chown=node:node /app/backstage.json ./
COPY --from=build --chown=node:node /app/yarn.lock \
     /app/package.json \
     /app/packages/backend/dist/skeleton/ ./
RUN --mount=type=cache,target=/home/node/.cache/yarn,sharing=locked,uid=1000,gid=1000 \
    yarn workspaces focus --all --production
COPY --from=build --chown=node:node /app/packages/backend/dist/bundle/ ./
CMD ["node", "packages/backend", "--config", "app-config.yaml"]
```

运行此镜像并查看容器内部可用的内容：

```console
docker build -t backstage:init .
docker run -d \
    -e APP_CONFIG_backend_database_client='better-sqlite3' \
    -e APP_CONFIG_backend_database_connection=':memory:' \
    -e APP_CONFIG_auth_providers_guest_dangerouslyAllowOutsideDevelopment='true' \
    -p 7007:7007 \
    -u 1000 \
    --cap-drop=ALL \
    --read-only \
    --tmpfs /tmp \
    backstage:init
```

这能正常工作，但运行时容器自带了一个 shell、一个包管理器和 yarn。而运行 Backstage 并不需要这些。运行 `docker exec` 来查看容器内部可访问的内容：

```console
docker exec -it <container-id> sh
$ cat /etc/shells
# /etc/shells: valid login shells
/bin/sh
/usr/bin/sh
/bin/bash
/usr/bin/bash
/bin/rbash
/usr/bin/rbash
/usr/bin/dash
$ yarn --version
4.12.0
$ dpkg --version
dpkg version 1.22.11 (arm64).
$ whoami
node
$ id
uid=1000(node) gid=1000(node) groups=1000(node)
```

`node:24-trixie-slim` 镜像自带三个 shell（`dash`、`bash` 和 `rbash`）、一个包管理器（`dpkg`）和 `yarn`。这些工具中的每一个都会扩大攻击面。获得该容器访问权限的攻击者可以利用它们在你的基础设施中进行横向移动。

## 步骤 2：将构建阶段切换到 DHI

用 DHI 等价物替换全部三个阶段。DHI Node.js 镜像同时提供 Alpine 和 Debian 变体。本指南使用 Alpine 变体（`dhi.io/node:24-alpine3.23`），因为它生成的镜像更小。如果你出于兼容性原因需要停留在 Debian 上，请使用 `dhi.io/node:24-bookworm` 并保留 `apt-get` 而非 `apk`。

```dockerfile
# Stage 1: prepare packages
FROM --platform=$BUILDPLATFORM dhi.io/node:24-alpine3.23-dev AS packages
WORKDIR /app
COPY backstage.json package.json yarn.lock ./
COPY .yarn ./.yarn
COPY .yarnrc.yml ./
COPY packages packages
COPY plugins plugins
RUN find packages \! -name "package.json" -mindepth 2 -maxdepth 2 \
    -exec rm -rf {} \+

# Stage 2: build the application
FROM --platform=$BUILDPLATFORM dhi.io/node:24-alpine3.23-dev AS build
ENV PYTHON=/usr/bin/python3
RUN apk add --no-cache g++ make python3 sqlite-dev && \
    rm -rf /var/lib/apk/lists/*
WORKDIR /app
COPY --from=packages --chown=node:node /app .
RUN --mount=type=cache,target=/home/node/.cache/yarn,sharing=locked,uid=1000,gid=1000 \
    yarn install --immutable
COPY --chown=node:node . .
RUN yarn tsc
RUN yarn --cwd packages/backend build
RUN mkdir packages/backend/dist/skeleton packages/backend/dist/bundle \
    && tar xzf packages/backend/dist/skeleton.tar.gz \
       -C packages/backend/dist/skeleton \
    && tar xzf packages/backend/dist/bundle.tar.gz \
       -C packages/backend/dist/bundle

# Final Stage: create the runtime image
FROM dhi.io/node:24-alpine3.23-dev
ENV PYTHON=/usr/bin/python3
RUN apk add --no-cache g++ make python3 sqlite-dev && \
    rm -rf /var/lib/apk/lists/*
WORKDIR /app
COPY --from=build --chown=node:node /app/.yarn ./.yarn
COPY --from=build --chown=node:node /app/.yarnrc.yml ./
COPY --from=build --chown=node:node /app/backstage.json ./
COPY --from=build --chown=node:node /app/yarn.lock \
     /app/package.json \
     /app/packages/backend/dist/skeleton/ ./
RUN --mount=type=cache,target=/home/node/.cache/yarn,sharing=locked,uid=1000,gid=1000 \
    yarn workspaces focus --all --production \
    && rm -rf "$(yarn cache clean)"
COPY --from=build --chown=node:node /app/packages/backend/dist/bundle/ ./
CMD ["node", "packages/backend", "--config", "app-config.yaml"]
```

构建并标记该版本：

```console
docker build -t backstage:dhi-dev .
```

> [!NOTE]
>
> `-dev` 变体包含 shell 和包管理器，这正是 `apk add` 能够生效的原因。Backstage 在运行时镜像中需要 `python3` 和原生构建工具，因为 `yarn workspaces focus --all --production` 会在生产安装过程中重新编译原生模块。这是 Backstage 构建流程特有的——大多数 Node.js 应用可以使用标准（非 dev）DHI 运行时变体，无需额外包。

DHI 镜像附带了原始 `node:24-trixie-slim` 镜像所没有的证明（attestation）。检查附带了哪些内容：

```console
docker scout attest list dhi.io/node:24-alpine3.23
```

DHI 镜像附带 15 项证明，包括 CycloneDX SBOM、SLSA 来源证明（provenance）、OpenVEX、Scout 健康报告、密钥扫描、病毒/恶意软件报告，以及一份 SLSA 验证摘要。

## 步骤 3：添加 Socket Firewall 防护

DHI 为 Node.js 镜像提供 `-sfw`（Socket Firewall）变体。Socket Firewall 在构建期间拦截 `npm` 和 `yarn` 命令，以在恶意包执行安装脚本之前检测并阻止它们。

要启用 Socket Firewall，需将三个阶段中的 `-dev` 标签改为 `-sfw-dev`。使用 SFW 版本的 Dockerfile：

```dockerfile
# Stage 1: prepare packages
FROM --platform=$BUILDPLATFORM dhi.io/node:24-alpine3.23-sfw-dev AS packages
WORKDIR /app
COPY backstage.json package.json yarn.lock ./
COPY .yarn ./.yarn
COPY .yarnrc.yml ./
COPY packages packages
COPY plugins plugins
RUN find packages \! -name "package.json" -mindepth 2 -maxdepth 2 \
    -exec rm -rf {} \+

# Stage 2: build the packages
FROM --platform=$BUILDPLATFORM dhi.io/node:24-alpine3.23-sfw-dev AS build-packages
ENV PYTHON=/usr/bin/python3
RUN apk add --no-cache g++ make python3 sqlite-dev && \
    rm -rf /var/lib/apk/lists/*
WORKDIR /app
COPY --from=packages --chown=node:node /app .
RUN --mount=type=cache,target=/home/node/.cache/yarn,sharing=locked,uid=1000,gid=1000 \
    yarn install --immutable
COPY --chown=node:node . .
RUN yarn tsc
RUN yarn --cwd packages/backend build
RUN mkdir packages/backend/dist/skeleton packages/backend/dist/bundle \
    && tar xzf packages/backend/dist/skeleton.tar.gz \
       -C packages/backend/dist/skeleton \
    && tar xzf packages/backend/dist/bundle.tar.gz \
       -C packages/backend/dist/bundle

# Final Stage: create the runtime image
FROM dhi.io/node:24-alpine3.23-sfw-dev
ENV PYTHON=/usr/bin/python3
RUN apk add --no-cache g++ make python3 sqlite-dev && \
    rm -rf /var/lib/apk/lists/*
WORKDIR /app
COPY --from=build-packages --chown=node:node /app/.yarn ./.yarn
COPY --from=build-packages --chown=node:node /app/.yarnrc.yml ./
COPY --from=build-packages --chown=node:node /app/backstage.json ./
COPY --from=build-packages --chown=node:node /app/yarn.lock \
     /app/package.json \
     /app/packages/backend/dist/skeleton/ ./
RUN --mount=type=cache,target=/home/node/.cache/yarn,sharing=locked,uid=1000,gid=1000 \
    yarn workspaces focus --all --production \
    && rm -rf "$(yarn cache clean)"
COPY --from=build-packages --chown=node:node /app/packages/backend/dist/bundle/ ./
CMD ["node", "packages/backend", "--config", "app-config.yaml"]
```

构建该版本：

```console
docker build -t backstage:dhi-sfw-dev .
```

构建时，你会在构建输出中看到 Socket Firewall 消息：对于 Dockerfile 中或在运行中的容器内执行的任何 `yarn` 和 `npm` 命令，都会显示 `Protected by Socket Firewall`。

> [!TIP]
>
> `-sfw-dev` 变体更大（1.9 GB 对 1.72 GB），因为 Socket Firewall 增加了监控工具。在 `yarn install` 期间获得的安全收益超过了体积增加带来的代价。

## 步骤 4：使用 DHI 定制移除 shell 和包管理器

前面的步骤仍将 `-dev` 或 `-sfw-dev` 变体作为运行时镜像使用，而它们包含 shell 和包管理器。DHI 定制允许你从基础（非 dev）镜像——它没有 shell 也没有包管理器——起步，仅添加你的应用所需的运行时库和语言运行时。

> [!IMPORTANT]
>
> 创建定制时，只添加你的应用在运行时所需的内容：
>
> - **系统包（System packages）** - 添加共享库（如 `sqlite-libs`）以及来自 DHI 目录的语言运行时（如 `python-3.14`）。
>   不要添加构建工具（如来自 Alpine 的 `g++`、`make` 或 `python3`）。
> - **构建工具（Build tools）** - 仅保留在 `-dev` 构建阶段。绝不要将它们添加到运行时定制中。
>
> 从 DHI 加固包源安装的语言运行时经过了补丁修复，并会被记录在镜像 SBOM 中，这正是它们可作为系统包被接受的原因。
> 来自 Alpine 或 Debian 包源的构建工具未经加固，绝不应出现在运行时镜像中。

对于 Backstage，运行时镜像需要：

- **sqlite-libs** - 被编译后的 `better-sqlite3` 原生模块所链接的共享库（作为系统包添加）。
- **Python** - 如果你的 Backstage 插件或配置在运行时需要 Python，则添加来自 DHI 目录的 `python-3.14` 系统包。与通过 `apk` 安装的 `python3` 不同，该包由 Docker 打补丁并记录在镜像 SBOM 中。

Docker 将持续以 SLSA Level 3 合规性构建这些定制镜像，并在 CVE 修补的保证 SLA 内为其打补丁。

要创建定制，可使用以下方法之一。

**Docker Hub UI**



将 Node.js DHI 仓库镜像到你的组织命名空间之后：

1. 在 Docker Hub 中打开被镜像的 Node.js 仓库。
2. 选择 **Customize**（定制）并选择 `node:24-alpine3.23` 标签。
3. 在 **Packages**（包）下，添加 `sqlite-libs` 和 `python-3.14`。
4. 创建该定制。

更多信息，请参阅 [定制镜像](/dhi/how-to/customize/)。

**dhictl CLI**



`dhictl` 是 Docker 用于管理 Docker Hardened Images 的命令行工具。它允许你浏览 DHI 目录、镜像镜像，并直接从终端创建定制。你可以将 `dhictl` 集成到 CI/CD 流水线和基础设施即代码（IaC）工作流中。你可以将 `dhictl` 作为独立二进制文件安装，或作为 Docker CLI 插件（`docker dhi`）安装；安装说明请参阅 [使用 DHI CLI](/dhi/how-to/cli/)。

与其手动编写定制 YAML，不如使用 `dhictl` 来生成一个起点：

```console
dhictl customization prepare --org YOUR_ORG node 24-alpine3.23 \
    --destination YOUR_ORG/dhi-node \
    --name "backstage" \
    --tag-suffix "_backstage" \
    --output node-backstage.yaml
```

编辑生成的文件以添加运行时库：

```yaml
name: backstage

source: dhi/node
tag_definition_id: node/alpine-3.23/24

destination: YOUR_ORG/dhi-node
tag_suffix: _backstage

platforms:
  - linux/amd64
  - linux/arm64

contents:
  packages:
    - sqlite-libs
    - python-3.14

accounts:
  root: true
  runs-as: node
  users:
    - name: node
      uid: 1000
  groups:
    - name: node
      gid: 1000

```

然后创建该定制：

```console
dhictl customization create --org YOUR_ORG node-backstage.yaml
```

使用 create 输出中的定制 ID 监控构建进度。要查找该 ID，请运行：

```console
dhictl customization list --org YOUR_ORG
```

然后监控构建：

```console
dhictl customization build list <customization-id> --org YOUR_ORG
```

Docker 在其安全基础设施上构建定制镜像，并将其发布为 `YOUR_ORG/dhi-node:24-alpine3.23_backstage`。

> [!NOTE]
>
> 如果你的 Backstage 配置在运行时不需要 Python，可以从包列表中省略 `python-3.14`。仅 `sqlite-libs` 包就足以配合 `better-sqlite3` 运行 Backstage。



### 更新 Dockerfile

仅更新 Dockerfile 的最后一个阶段以使用定制镜像：

```dockerfile
# Final Stage: create the runtime image
FROM YOUR_ORG/dhi-node:24-alpine3.23_backstage
WORKDIR /app
COPY --from=build --chown=node:node /app/node_modules ./node_modules
COPY --from=build --chown=node:node /app/packages/backend/dist/bundle/ ./
CMD ["node", "packages/backend", "--config", "app-config.yaml"]
```

构建该版本：

```console
docker build -t backstage:dhi .
```

由于该定制仅包含运行时库和 OCI 制品——没有构建工具、没有包管理器、没有 shell——生成的镜像因此是 distroless 的：

```console
docker run --rm YOUR_ORG/dhi-node:24-alpine3.23_backstage sh -c "echo hello"
docker: Error response from daemon: ... exec: "sh": executable file not found in $PATH
```

使用 Enterprise 定制时：

- 运行时镜像为 distroless——没有 shell，没有包管理器。
- 当基础的 Node.js 镜像或其任意包收到安全补丁时，Docker 会自动重建你的定制镜像。
- 完整信任链得以维系，包括 SLSA Build Level 3 来源证明。
- Node.js 和 Python 运行时都被记录在镜像 SBOM 中。

确认容器不再拥有 shell 访问权限：

```console
docker exec -it <container-id> sh
OCI runtime exec failed: exec failed: unable to start container process: ...
```

如果你需要排查一个正在运行的 distroless 容器，请使用 [Docker Debug](/dhi/how-to/troubleshoot/#general-debugging)。

> [!NOTE]
>
> 如果你的组织需要符合 FIPS/STIG 的镜像，DHI Enterprise 中也提供该选项。

## 步骤 5：验证结果

使用 Docker Scout 将基于 DHI 的镜像与原始镜像进行对比：

```console
docker scout compare backstage:dhi \
    --to backstage:init \
    --platform linux/amd64 \
    --ignore-unchanged
```

跨各种方案的典型对比结果类似于以下内容：

| 指标 | 原始 | DHI -dev | DHI -sfw-dev | Enterprise |
|--------|----------|----------|--------------|------------|
| 磁盘占用 | 1.61 GB | 1.72 GB | 1.9 GB | 1.49 GB |
| 内容大小 | 268 MB | 288 MB | 328 MB | 247 MB |
| 运行时含 shell | 是 | 是 | 是 | 否 |
| 包管理器 | 是 | 是 | 是 | 否 |
| 默认非 root | 否 | 否 | 否 | 是 |
| Socket Firewall | 否 | 否 | 是（构建期） | 是（构建期）/ 否（运行时） |
| SLSA 来源证明 | 否 | 仅基础 | 仅基础 | 完整（Level 3） |

> [!NOTE]
>
> `-sfw-dev` 变体更大，因为 Socket Firewall 向镜像中添加了监控工具。增加的体积位于构建阶段，而在 `yarn install` 期间获得的安全收益超过了体积增加带来的代价。

要进行更彻底的评估，请使用多种工具进行扫描：

```console
trivy image backstage:dhi
grype backstage:dhi
docker scout quickview backstage:dhi
```

不同的扫描器会检测到不同的问题。同时运行这三者能让你对自己的安全态势获得最完整的视图。

## 后续步骤

- [定制镜像](/dhi/how-to/customize/) — 关于 Enterprise 定制 UI 的完整参考。
- [创建并构建 DHI](/dhi/how-to/build/) — 学习如何编写 DHI 定义文件、在本地构建镜像。
- [使用 DHI CLI](/dhi/how-to/cli/) — 从命令行管理 DHI 镜像、镜像源和定制。
- [迁移到 DHI](/dhi/migration/) — 适用于无需额外包即可配合标准 DHI 镜像工作的应用。
- [对比镜像](/dhi/how-to/search-evaluate/#compare-and-evaluate-images) — 评估原始镜像与加固镜像之间的安全改进。
- [Docker Debug](/dhi/how-to/troubleshoot/#general-debugging) — 排查没有 shell 的 distroless 容器。

