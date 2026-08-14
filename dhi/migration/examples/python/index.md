# Python


本示例展示如何将 Python 应用程序迁移到 Docker 强化镜像。

以下示例展示了迁移到 Docker 强化镜像前后的 Dockerfile。每个示例包含五种变体：

- 迁移前 (Ubuntu)：使用基于 Ubuntu 的镜像的示例 Dockerfile，迁移到 DHI 之前
- 迁移前 (Wolfi)：使用 Wolfi 发行版镜像的示例 Dockerfile，迁移到 DHI 之前
- 迁移前 (DOI)：使用 Docker Official Images 的示例 Dockerfile，迁移到 DHI 之前
- 迁移后 (多阶段)：迁移到 DHI 后使用多阶段构建的示例 Dockerfile（推荐用于最小化、安全的镜像）
- 迁移后 (单阶段)：迁移到 DHI 后使用单阶段构建的示例 Dockerfile（更简单，但会生成更大的镜像，攻击面更广）

> [!NOTE]
>
> 大多数用例推荐使用多阶段构建。为简化操作也支持单阶段构建，但在镜像大小和安全性方面需要权衡。
>
> 在拉取 Docker 强化镜像之前，必须先向 `dhi.io` 进行身份验证。
> 使用您的 Docker ID 凭据（与您用于 Docker Hub 的用户名和密码相同）。如果您没有 Docker 账户，请[免费创建一个](../../../accounts/create-account.md)。
> 运行 `docker login dhi.io` 进行身份验证。

**迁移前 (Ubuntu)**



```dockerfile
#syntax=docker/dockerfile:1

FROM ubuntu:24.04 AS builder

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv --no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python3 -m venv /app/venv
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM ubuntu:24.04

RUN apt-get update && apt-get install -y python3 --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY app.py ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python3", "/app/app.py" ]
```

**迁移前 (Wolfi)**



```dockerfile
#syntax=docker/dockerfile:1

FROM cgr.dev/chainguard/python:latest-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

# 如果需要，使用 apk 安装任何额外的包
# RUN apk add --no-cache gcc musl-dev

RUN pip install --no-cache-dir -r requirements.txt

FROM cgr.dev/chainguard/python:latest

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY app.py ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/app.py" ]
```

**迁移前 (DOI)**



```dockerfile
#syntax=docker/dockerfile:1

FROM python:latest AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

# 如果需要，使用 apt 安装任何额外的包
# RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

FROM python:latest

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY app.py ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/app.py" ]
```

**迁移后 (多阶段)**



```dockerfile
#syntax=docker/dockerfile:1

# === 构建阶段：安装依赖并创建虚拟环境 ===
FROM dhi.io/python:3.13-alpine3.23-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

# 如果需要，使用 apk 安装任何额外的包
# RUN apk add --no-cache gcc musl-dev

RUN pip install --no-cache-dir -r requirements.txt

# === 最终阶段：创建最小运行时镜像 ===
FROM dhi.io/python:3.13-alpine3.23

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY app.py ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/app.py" ]
```

**迁移后 (单阶段)**



```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/python:3.13-alpine3.23-dev

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

# 如果需要，使用 apk 安装任何额外的包
# RUN apk add --no-cache gcc musl-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

ENTRYPOINT [ "python", "/app/app.py" ]
```



