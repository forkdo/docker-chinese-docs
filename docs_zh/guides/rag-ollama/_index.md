---
description: 使用 Ollama 和 Docker 容器化 RAG 应用
keywords: python, 生成式人工智能, genai, llm, ollama, rag, qdrant
title: 使用 Ollama 和 Docker 构建 RAG 应用
linkTitle: RAG Ollama 应用
summary: |
  本指南演示如何使用 Docker 部署 Ollama 的检索增强生成（RAG）模型。
tags: [ai]
aliases:
  - /guides/use-case/rag-ollama/
params:
  time: 20 分钟
---

检索增强生成（Retrieval Augmented Generation，简称 RAG）指南教你如何使用 Docker 容器化现有的 RAG 应用。示例应用是一个类似侍酒师的 RAG 应用，可为你提供最佳的葡萄酒与食物搭配建议。在本指南中，你将学习如何：

- 容器化并运行 RAG 应用
- 设置本地环境，以便在本地运行完整的 RAG 栈进行开发

首先，让我们容器化一个现有的 RAG 应用。