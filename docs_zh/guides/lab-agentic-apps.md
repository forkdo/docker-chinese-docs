---
title: "实验：使用 Docker 构建智能体应用"
linkTitle: "实验：构建智能体应用"
description: |
  在这个动手实践的交互式实验中，使用 Docker Model Runner、MCP Gateway 和 Compose
  构建智能体应用。
summary: |
  动手实验：使用 Docker Model Runner、MCP Gateway 和 Compose 构建智能体应用。
  了解模型、工具和智能体框架。
keywords: AI, Docker, Model Runner, MCP Gateway, agentic apps, lab, labspace
aliases:
  - /labs/docker-for-ai/agentic-apps/
params:
  tags: [labs]
  time: 20 minutes
---

快速上手，使用 Compose、Docker Model Runner 和 Docker MCP Gateway 构建智能体应用。
这个动手实验将带你从理解 AI 模型一路走到构建完整的智能体应用。

## 启动实验

{{< labspace-launch image="dockersamples/labspace-agentic-apps-with-docker" model-download="true" >}}

## 你将学到什么

本实验涵盖智能体应用开发的三个核心领域：

**模型**：什么是模型、如何与模型交互、在 Compose 中配置 Docker
Model Runner，以及编写连接 Model Runner 的代码

**工具**：理解工具及其工作原理、MCP（Model Context
Protocol）如何融入其中、配置 Docker MCP Gateway，以及在代码中连接
MCP Gateway

**代码**：什么是智能体框架、在 Compose
文件中定义模型和工具，以及配置应用使用这些模型和工具

## 模块

| # | 模块 | 说明 |
|---|--------|-------------|
| 1 | 引言 | 智能体应用与 Docker AI 技术栈概览 |
| 2 | 理解模型交互 | 学习如何与 AI 模型交互 |
| 3 | Docker Model Runner | 配置并结合 Compose 使用 Docker Model Runner |
| 4 | 理解工具与 MCP | 深入了解工具、工具调用与 MCP |
| 5 | Docker MCP Gateway | 搭建并配置 MCP Gateway |
| 6 | 融会贯通 | 构建一个完整的智能体应用 |
| 7 | 结语 | 总结与后续步骤 |
