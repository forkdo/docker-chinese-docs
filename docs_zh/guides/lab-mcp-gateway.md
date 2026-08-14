---
title: "实验：Docker MCP Gateway"
linkTitle: "实验：Docker MCP Gateway"
description: |
  在这个动手实践的交互式实验中，使用 Docker MCP Gateway 安全可靠地运行
  容器化的 MCP 服务器。
summary: |
  动手实验：使用 Docker MCP Gateway 配置、保护 MCP 服务器，并将其连接到你的智能体
  应用。
keywords: AI, Docker, MCP, MCP Gateway, MCP servers, lab, labspace
aliases:
  - /labs/docker-for-ai/mcp-gateway/
params:
  tags: [labs]
  time: 20 minutes
---

本实验全面、动手地介绍 Docker MCP Gateway，
它让你能够安全可靠地运行容器化的 MCP 服务器。学习
如何配置、保护 MCP 服务器，并将其连接到你的智能体应用。

## 启动实验

{{< labspace-launch image="dockersamples/labspace-mcp-gateway" >}}

## 你将学到什么

- 了解 Docker MCP Gateway 及其架构
- 使用一个简单的 MCP 服务器运行 MCP Gateway
- 安全地向 MCP 服务器注入密钥
- 过滤工具以减少噪音、节省 token
- 使用主流智能体框架将 MCP Gateway 接入你的应用
- 配置并使用自定义 MCP 服务器

## 模块

| # | 模块 | 说明 |
|---|--------|-------------|
| 1 | 引言 | MCP Gateway 概览及其重要性 |
| 2 | 添加简单的 MCP 服务器 | 从基础的 MCP 服务器配置开始上手 |
| 3 | 添加复杂的 MCP 服务器 | 配置带有密钥和高级选项的 MCP 服务器 |
| 4 | 过滤可用工具 | 通过过滤工具可见性减少噪音、节省 token |
| 5 | 将 MCP Gateway 接入你的应用 | 将 MCP Gateway 与智能体框架集成 |
| 6 | 使用自定义 MCP 服务器 | 构建并运行你自己的自定义 MCP 服务器 |
| 7 | 结语 | 总结与后续步骤 |
