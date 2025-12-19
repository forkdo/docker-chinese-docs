---
title: Python
description: 将 Python 应用程序迁移到 Docker Hardened Images
weight: 20
keywords: python, migration, dhi
---

本示例展示如何将 Python 应用程序迁移到 Docker Hardened Images。

以下示例展示了迁移到 Docker Hardened Images 前后的 Dockerfile。每个示例包含四种变体：

- 迁移前 (Wolfi)：使用 Wolfi 发行版镜像的示例 Dockerfile，迁移到 DHI 之前
- 迁移前 (DOI)：使用 Docker Official Images 的示例 Dockerfile，迁移到 DHI 之前
- 迁移后 (多阶段)：迁移到 DHI 后使用多阶段构建的示例 Dockerfile（推荐用于最小化、安全的镜像）
- 迁移后 (单阶段)：迁移到 DHI 后使用单阶段构建的示例 Dockerfile（更简单，但会生成更大的镜像，攻击面更广）

> [!NOTE]
>
> 大多数用例推荐使用多阶段构建。为简化操作也支持单阶段构建，但在镜像大小和安全性方面需要权衡。
>
> 在拉取 Docker Hardened Images 之前，必须先向 `dhi.io` 进行身份验证。
> 运行 `docker login dhi.io` 进行身份验证。

{{< tabs >}}
{{< tab name="迁移前 (Wolfi)" >}}

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

{{< /tab >}}
{{< tab name="迁移前 (DOI)" >}}

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

{{< /tab >}}
{{< tab name="迁移后 (多阶段)" >}}

```dockerfile
#syntax=docker/dockerfile:1

# === 构建阶段：安装依赖并创建虚拟环境 ===
FROM dhi.io/python:3.13-alpine3.21-dev AS builder

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
FROM dhi.io/python:3.13-alpine3.21

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY app.py ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/app.py" ]
```

{{< /tab >}}
{{< tab name="迁移后 (单阶段)" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/python:3.13-alpine3.21-dev

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

{{< /tab >}}
{{< /tabs >}}