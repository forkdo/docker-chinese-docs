---
title: 如何使用 SonarQube 和 E2B 构建 AI 驱动的代码质量工作流
linkTitle: 构建 AI 驱动的代码质量工作流
summary: 使用 E2B 沙盒与 Docker 的 MCP 目录构建 AI 驱动的代码质量工作流，实现 GitHub 和 SonarQube 的自动化集成。
description: 学习如何创建带有 MCP 服务器的 E2B 沙盒，使用 SonarQube 分析代码质量，并通过 GitHub 生成质量门禁拉取请求——所有操作均可通过与 Claude 的自然语言交互完成。
tags:
- devops
params:
  time: 40 分钟
  image: null
  resource_links:
  - title: E2B Documentation
    url: https://e2b.dev/docs
  - title: Docker MCP Catalog
    url: https://hub.docker.com/mcp
  - title: Sandboxes
    url: https://docs.docker.com/ai/mcp-catalog-and-toolkit/sandboxes/
---

本指南演示如何使用 [E2B 沙盒](https://e2b.dev/docs) 和 Docker 的 MCP 目录构建 AI 驱动的代码质量工作流。您将创建一个系统，该系统使用 SonarQube 自动分析 GitHub 仓库中的代码质量问题，然后生成包含修复方案的拉取请求。

## 您将构建什么

您将构建一个 Node.js 脚本，该脚本启动 E2B 沙盒，连接 GitHub 和 SonarQube MCP 服务器，并使用 Claude Code 分析代码质量并提出改进建议。这些 MCP 服务器以容器形式运行，作为 E2B 沙盒的一部分。

## 您将学到什么

在本指南中，您将学习：

- 如何创建带有多个 MCP 服务器的 E2B 沙盒
- 如何为 AI 工作流配置 GitHub 和 SonarQube MCP 服务器
- 如何在沙盒内使用 Claude Code 与外部工具交互
- 如何构建自动化的代码审查工作流以创建质量门禁拉取请求

## 为何使用 E2B 沙盒？

在 E2B 沙盒中运行此工作流相比本地执行具有以下优势：

- **安全性**：AI 生成的代码在隔离的容器中运行，保护您的本地环境和凭证
- **零设置**：无需在本地安装 SonarQube、GitHub CLI 或管理依赖项
- **可扩展性**：代码扫描等资源密集型操作在云端运行，不消耗本地资源

## 了解更多

阅读 Docker 的博客文章：[Docker + E2B：构建可信 AI 的未来](https://www.docker.com/blog/docker-e2b-building-the-future-of-trusted-ai/)。