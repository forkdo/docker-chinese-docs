---
title: 使用 OpenTelemetry 为 JavaScript 应用添加遥测
description: *desc 了解如何在容器化环境中使用 OpenTelemetry 为 JavaScript 应用添加遥测。
keywords: OpenTelemetry, 可观测性, 追踪
linktitle: 使用 OpenTelemetry 为 JS 应用添加遥测
summary: *desc
tags: [app-dev, observability]
languages: [js]
params:
  time: 10 分钟
---

OpenTelemetry (OTel) 是一个开源的可观测性框架，提供了一套 API、SDK 和工具，用于从应用中收集遥测数据，如指标、日志和追踪。通过 OpenTelemetry，开发者可以深入了解其服务在生产环境或本地开发期间的性能表现。

OpenTelemetry 的一个关键组件是 OpenTelemetry 协议 (OTLP)，它是一种通用的、与供应商无关的协议，旨在高效可靠地传输遥测数据。OTLP 通过 HTTP 或 gRPC 支持多种数据类型（追踪、指标、日志），使其成为仪器化应用、OpenTelemetry Collector 和后端（如 Jaeger 或 Prometheus）之间通信的默认和推荐协议。

本指南将引导你如何使用 OpenTelemetry 为一个简单的 Node.js 应用添加遥测，并使用 Docker 运行应用和 Collector。这种设置非常适合在本地开发和测试可观测性，然后再集成到 Prometheus、Jaeger 或 Grafana 等外部可观测性平台。

在本指南中，你将学习如何：

- 如何在 Node.js 应用中设置 OpenTelemetry。
- 如何在 Docker 中运行 OpenTelemetry Collector。
- 如何使用 Jaeger 可视化追踪。
- 如何使用 Docker Compose 管理完整的可观测性栈。

## 使用 Docker 运行 OpenTelemetry

[OpenTelemetry 的 Docker 官方镜像](https://hub.docker.com/r/otel/opentelemetry-collector-contrib) 提供了一种便捷的方式来部署和管理 Dex 实例。OpenTelemetry 支持多种 CPU 架构，包括 amd64、armv7 和 arm64，确保与不同设备和平台的兼容性。[Jaeger 的 Docker 镜像](https://hub.docker.com/r/jaegertracing/jaeger) 也是如此。

## 前置条件

[Docker Compose](/compose/)：推荐用于管理多容器 Docker 应用。

具备 Node.js 和 Docker 的基础知识。

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

初始化一个基本的 Node.js 应用：

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

创建追踪配置文件：

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

现在，在 `app/` 文件夹内添加 `Dockerfile`：

```dockerfile
# app/Dockerfile
FROM node:18

WORKDIR /usr/src/app
COPY . .
RUN npm install

CMD ["node", "app.js"]
```

## 启动栈

使用 Docker Compose 启动所有服务：

```bash
docker compose up --build
```

服务启动后：

在 [http://localhost:3000](http://localhost:3000) 访问你的应用

在 Jaeger UI [http://localhost:16686](http://localhost:16686) 查看追踪

## 在 Jaeger 中验证追踪

访问应用的根端点后，打开 Jaeger 的 UI，搜索服务（默认通常是 `unknown_service`，除非明确命名），并检查追踪。

你应该能看到 HTTP 请求、中间件和自动仪器化库的跨度。

## 结论

你现在有了一个使用 Docker Compose 的完整功能的 OpenTelemetry 设置。你已经为一个基本的 JavaScript 应用添加了遥测以导出追踪，并使用 Jaeger 可视化了它们。这种架构可以扩展到更复杂的应用和使用 Prometheus、Grafana 或云原生导出器的可观测性管道。

有关自定义跨度创建、指标和日志等高级主题，请查阅 OpenTelemetry JavaScript 文档。