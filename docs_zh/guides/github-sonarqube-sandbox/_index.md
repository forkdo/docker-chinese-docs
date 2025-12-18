---
title: 如何使用 SonarQube 和 E2B 构建 AI 驱动的代码质量工作流
linkTitle: 构建 AI 驱动的代码质量工作流
summary: 使用 Docker 的 MCP 目录中的 E2B 沙箱构建 AI 驱动的代码质量工作流，自动集成 GitHub 和 SonarQube。
description: 了解如何创建带有 MCP 服务器的 E2B 沙箱，使用 SonarQube 分析代码质量，并通过 GitHub 生成质量门控的拉取请求——全部通过与 Claude 的自然语言交互完成。
tags: [devops]
params:
  time: 40 分钟
  image:
  resource_links:
    - title: E2B 文档
      url: https://e2b.dev/docs
    - title: Docker MCP 目录
      url: https://hub.docker.com/mcp
    - title: 沙箱
      url: https://docs.docker.com/ai/mcp-catalog-and-toolkit/sandboxes/
---

本指南演示了如何使用 Docker 的 MCP 目录中的 [E2B 沙箱](https://e2b.dev/docs) 构建 AI 驱动的代码质量工作流。你将创建一个系统，使用 SonarQube 自动分析 GitHub 仓库中的代码质量问题，然后生成包含修复建议的拉取请求。

## 你将构建的内容

你将构建一个 Node.js 脚本，启动一个 E2B 沙箱，连接 GitHub 和 SonarQube MCP 服务器，并使用 Claude Code 分析代码质量并提出改进建议。MCP 服务器是容器化的，作为 E2B 沙箱的一部分运行。

## 你将学到的内容

在本指南中，你将学习：

- 如何使用多个 MCP 服务器创建 E2B 沙箱
- 如何配置 GitHub 和 SonarQube MCP 服务器以支持 AI 工作流
- 如何在沙箱内使用 Claude Code 与外部工具交互
- 如何构建自动生成质量门控拉取请求的自动化代码审查工作流

## 为什么使用 E2B 沙箱？

在 E2B 沙箱中运行此工作流相比本地执行具有多个优势：

- 安全性：AI 生成的代码在隔离的容器中运行，保护你的本地环境和凭据
- 零配置：无需在本地安装 SonarQube、GitHub CLI 或管理依赖项
- 可扩展性：代码扫描等资源密集型操作在云端运行，不消耗本地资源

## 了解更多

阅读 Docker 的博客文章：[Docker + E2B：构建可信 AI 的未来](https://www.docker.com/blog/docker-e2b-building-the-future-of-trusted-ai/)。