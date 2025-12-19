---
title: 使用 OpenTelemetry 对 JavaScript 应用进行可观测性插桩
description: &desc 学习如何在 Docker 环境中使用 OpenTelemetry 对 JavaScript 应用进行可观测性插桩。
keywords: OpenTelemetry, observability, tracing
linktitle: 使用 OpenTelemetry 对 JS 应用进行插桩
summary: *desc
tags: [app-dev, observability]
languages: [js]
params:
  time: 10 分钟
---

OpenTelemetry (OTel) 是一个开源的可观测性框架，提供了一组 API、SDK 和工具，用于从应用程序中收集遥测数据，例如指标（metrics）、日志（logs）和追踪（traces）。借助 OpenTelemetry，开发人员可以在生产环境或本地开发期间深入了解其服务的性能表现。

OpenTelemetry 的一个关键组件是 OpenTelemetry 协议（OTLP），这是一种通用、与供应商无关的协议，旨在高效可靠地传输遥测数据。OTLP 支持通过 HTTP 或 gRPC 传输多种数据类型（追踪、指标、日志），因此它是插桩应用、OpenTelemetry Collector 以及 Jaeger 或 Prometheus 等后端之间通信的默认且推荐的协议。

本指南将引导您完成如何使用 OpenTelemetry 对简单的 Node.js 应用进行插桩，并使用 Docker 同时运行应用和 Collector。此设置非常适合在集成 Prometheus、Jaeger 或 Grafana 等外部可观测性平台之前进行本地开发和测试。

在本指南中，您将学习如何：

- 在 Node.js 应用中设置 OpenTelemetry。
- 在 Docker 中运行 OpenTelemetry Collector。
- 使用 Jaeger 可视化追踪。
- 使用 Docker Compose 管理完整的可观测性栈。

## 在 Docker 中使用 OpenTelemetry

[OpenTelemetry 的 Docker 官方镜像](https://hub.docker.com/r/otel/opentelemetry-collector-contrib) 提供了一种便捷的方式来部署和管理 OpenTelemetry 实例。OpenTelemetry 支持多种 CPU 架构，包括 amd64、armv7 和 arm64，确保与不同设备和平台的兼容性。[Jaeger 的 Docker 镜像](https://hub.docker.com/r/jaegertracing/jaeger) 同样如此。

## 先决条件

[Docker Compose](/compose/)：推荐用于管理多容器 Docker 应用。

对 Node.js 和 Docker 有基本了解。

## 项目结构

创建项目目录：
```bash
mkdir otel-js-app
cd otel-js-app
```

```bash
otel-js-app/
├── docker-compose.yaml
├── collector-config.yaml
├── app/
│   ├── package.json
│   ├── app.js
│   └── tracer.js
```

## 创建一个简单的 Node.js 应用

初始化一个基础的 Node.js 应用：

```bash
mkdir app && cd app
npm init -y
npm install express @opentelemetry/api @opentelemetry/sdk-node \
            @opentelemetry/auto-instrumentations-node \
            @opentelemetry/exporter-trace-otlp-http
```

现在，添加应用逻辑：

```js
// app/app.js
const express = require('express');
require('./tracer'); // 初始化 OpenTelemetry

const app = express();

app.get('/', (req, res) => {
  res.send('Hello from OpenTelemetry demo app!');
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`App listening at http://localhost:${PORT}`);
});
```

## 配置 OpenTelemetry 追踪

创建追踪器配置文件：

```js
// app/tracer.js
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: 'http://collector:4318/v1/traces',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

## 配置 OpenTelemetry Collector

在根目录创建 `collector-config.yaml` 文件：

```yaml
# collector-config.yaml
receivers:
  otlp:
    protocols:
      http:

exporters:
  logging:
    loglevel: debug
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [logging, jaeger]
```

## 添加 Docker Compose 配置

创建 `docker-compose.yaml` 文件：

```yaml
version: '3.9'

services:
  app:
    build: ./app
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    depends_on:
      - collector

  collector:
    image: otel/opentelemetry-collector:latest
    volumes:
      - ./collector-config.yaml:/etc/otelcol/config.yaml
    command: ["--config=/etc/otelcol/config.yaml"]
    ports:
      - "4318:4318" # OTLP

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686" # UI
      - "14250:14250" # Collector gRPC
```

现在，在 `app/` 文件夹中添加 `Dockerfile`：

```dockerfile
# app/Dockerfile
FROM node:18

WORKDIR /usr/src/app
COPY . .
RUN npm install

CMD ["node", "app.js"]
```

## 启动服务栈

使用 Docker Compose 启动所有服务：

```bash
docker compose up --build
```

服务启动后：

访问您的应用：[http://localhost:3000](http://localhost:3000)

在 Jaeger UI 中查看追踪：[http://localhost:16686](http://localhost:16686)

## 在 Jaeger 中验证追踪

访问应用根端点后，打开 Jaeger UI，搜索服务（默认通常为 `unknown_service`，除非显式命名），并检查追踪。

您应该能看到 HTTP 请求、中间件和自动插桩库生成的 span。

## 总结

您现在已拥有一个使用 Docker Compose 的完整 OpenTelemetry 设置。您已对一个基础的 JavaScript 应用进行插桩以导出追踪，并使用 Jaeger 进行了可视化。此架构可扩展到更复杂的应用程序和可观测性流水线，例如结合 Prometheus、Grafana 或云原生导出器。

如需了解自定义 span 创建、指标和日志等高级主题，请查阅 OpenTelemetry JavaScript 文档。