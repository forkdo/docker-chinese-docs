---
description: 使用 Ollama 和 Docker 容器化 RAG 应用程序
keywords: python, generative ai, genai, llm, ollama, rag, qdrant
title: 使用 Ollama 和 Docker 构建 RAG 应用程序
linkTitle: RAG Ollama 应用程序
summary: |
  本指南演示如何使用 Docker 部署检索增强生成 (RAG) 模型与 Ollama。
tags: [ai]
aliases:
  - /guides/use-case/rag-ollama/
params:
  time: 20 分钟
---

检索增强生成 (RAG) 指导您如何使用 Docker 容器化现有的 RAG 应用程序。示例应用程序是一个像侍酒师一样的 RAG，为您提供葡萄酒和食物的最佳搭配。在本指南中，您将学习如何：

- 容器化并运行 RAG 应用程序
- 设置本地环境以在本地运行完整的 RAG 堆栈进行开发

首先容器化现有的 RAG 应用程序。