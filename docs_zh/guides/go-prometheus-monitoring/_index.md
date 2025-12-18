---
description: 容器化 Golang 应用并使用 Prometheus 和 Grafana 进行监控。
keywords: golang, prometheus, grafana, 监控
title: 使用 Prometheus 和 Grafana 监控 Golang 应用
summary: |
  学习如何容器化 Golang 应用并使用 Prometheus 和 Grafana 进行监控。
linkTitle: 使用 Prometheus 和 Grafana 监控
languages: [go]
params:
  time: 45 分钟
---

本指南将教你如何容器化 Golang 应用并使用 Prometheus 和 Grafana 进行监控。

> **致谢**
>
> Docker 感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 对本指南的贡献。

## 概述

为了确保你的应用按预期运行，监控非常重要。其中最流行的监控工具之一是 Prometheus。Prometheus 是一个开源的监控和告警工具包，专为可靠性和可扩展性而设计。它通过从这些目标的 HTTP 端点拉取指标来收集监控目标的指标。为了可视化这些指标，你可以使用 Grafana。Grafana 是一个开源的监控和可观测性平台，允许你查询、可视化、告警并理解你的指标，无论它们存储在哪里。

在本指南中，你将创建一个带有若干端点的 Golang 服务器来模拟一个真实世界的应用。然后，你将使用 Prometheus 从服务器暴露指标。最后，你将使用 Grafana 可视化这些指标。你将容器化 Golang 应用，并使用 Docker Compose 文件连接所有服务：Golang、Prometheus 和 Grafana。

## 你将学到什么？

* 创建一个带有自定义 Prometheus 指标的 Golang 应用。
* 容器化 Golang 应用。
* 使用 Docker Compose 运行多个服务并将它们连接在一起，使用 Prometheus 和 Grafana 监控 Golang 应用。
* 使用 Grafana 仪表板可视化指标。

## 前置条件

- 假设你具备良好的 Golang 理解能力。
- 你必须熟悉 Prometheus 以及在 Grafana 中创建仪表板。
- 你必须熟悉 Docker 概念，如容器、镜像和 Dockerfile。如果你是 Docker 新手，可以从 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

## 后续步骤

你将创建一个 Golang 服务器并使用 Prometheus 暴露指标。