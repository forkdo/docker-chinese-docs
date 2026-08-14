---
title: "实验：面向开发者的 AI 基础"
linkTitle: "实验：AI 基础"
description: |
  通过在实时环境中的动手练习，学习 AI 开发的核心概念——模型、提示工程、工具调用
  和 RAG。
summary: |
  动手实验：学习 AI 应用开发的四大核心支柱。
  通过交互式练习，实践 Chat Completions API、提示工程、工具调用和 RAG。
keywords: AI, Docker, Model Runner, prompt engineering, RAG, tool calling, lab, labspace
aliases:
  - /labs/docker-for-ai/ai-fundamentals/
params:
  tags: [labs]
  time: 45 minutes
---

动手实践 AI 应用开发的四大核心支柱：模型、
提示工程、工具调用和 RAG。本实验使用 Docker Model Runner 完全在你的
本机上运行——无需 API 密钥或云账号。

## 启动实验

{{< labspace-launch image="dockersamples/labspace-ai-fundamentals" model-download="true" >}}

## 你将学到什么

完成本 Labspace 后，你将掌握以下内容：

- 理解 Chat Completions API 以及如何为模型组织消息结构
- 使用提示工程技巧，包括系统提示、少样本示例和结构化输出
- 在代码中实现工具调用和智能体循环
- 构建 RAG 流水线，让模型的回答基于你自己的数据

## 模块

| #   | 模块                                 | 说明                                                              |
| --- | ------------------------------------ | ----------------------------------------------------------------- |
| 1   | 欢迎与环境准备                       | 实验介绍与环境验证                                                |
| 2   | 与模型对话                           | Chat Completions API、消息角色与模型的无状态特性                  |
| 3   | 提示工程                             | 系统提示、少样本示例与结构化输出                                  |
| 4   | 工具调用                             | 工具定义、智能体循环以及在代码中执行工具                          |
| 5   | 检索增强生成（RAG）                  | 基于你自己的知识库进行检索、增强与生成                            |
| 6   | 总结                                 | 概念回顾与后续步骤                                                |
