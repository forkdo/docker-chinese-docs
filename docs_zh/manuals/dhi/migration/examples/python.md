---
title: Python
description: 将 Python 应用程序迁移到 Docker Hardened Images
weight: 20
keywords: python, migration, dhi
---

本示例展示了如何将 Python 应用程序迁移到 Docker Hardened Images。

以下示例展示了迁移前后的 Dockerfile。每个示例包含四种变体：

- 迁移前（Wolfi）：使用 Wolfi 发行版镜像的示例 Dockerfile，迁移前状态
- 迁移前（DOI）：使用 Docker 官方镜像的示例 Dockerfile，迁移前状态
- 迁移后（多阶段）：使用多阶段构建迁移至 DHI 的示例 Dockerfile（推荐用于最小化、安全的镜像）
- 迁移后（单阶段）：使用单阶段构建迁移至 DHI 的示例 Dockerfile（更简单但镜像更大，攻击面更广）

> [!NOTE]
>
> 多阶段构建适用于大多数场景。单阶段构建为简化而支持，但存在体积和安全性方面的权衡。
>
> 在拉取 Docker Hardened Images 之前，必须先对 `dhi.io` 进行身份验证。
> 运行 `docker login dhi.io` 进行认证。

{{< tabs >}}
{{< tab name="Before (Wolfi)" >}}

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

# Install any additional packages if needed using apk
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
{{< tab name="Before (DOI)" >}}

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

# Install any additional packages if needed using apt
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
{{< tab name="After (multi-stage)" >}}

```dockerfile
#syntax=docker/dockerfile:1

# === Build stage: Install dependencies and create virtual environment ===
FROM dhi.io/python:3.13-alpine3.21-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

# Install any additional packages if needed using apk
# RUN apk add --no-cache gcc musl-dev

RUN pip install --no-cache-dir -r requirements.txt

# === Final stage: Create minimal runtime image ===
FROM dhi.io/python:3.13-alpine3.21

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

COPY app.py ./
COPY --from=builder /app/venv /app/venv

ENTRYPOINT [ "python", "/app/app.py" ]
```

{{< /tab >}}
{{< tab name="After (single-stage)" >}}

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

# Install any additional packages if needed using apk
# RUN apk add --no-cache gcc musl-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

ENTRYPOINT [ "python", "/app/app.py" ]
```

{{< /tab >}}
{{< /tabs >}}