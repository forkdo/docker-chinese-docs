---
title: "实验：构建 AI 产品评论分析器"
linkTitle: "实验：AI 产品评论分析器"
description: |
  构建一条完整的 AI 驱动的反馈分析流水线——情感分析、
  基于嵌入向量的语义聚类以及回复生成——全部通过 Docker Model Runner 在
  本地运行。无需 API 密钥。
summary: |
  动手实验：构建一条 AI 流水线，按情感对产品评论进行分类、
  使用嵌入向量按主题聚类、提取可落地的功能点，
  并生成结合上下文的回复——全部在本地运行。
keywords: AI, Docker, Model Runner, sentiment analysis, embeddings, RAG, lab, labspace
aliases:
  - /labs/docker-for-ai/creating-ai-product-reviewer/
params:
  tags: [labs]
  time: 60 minutes
---

为一款名为 Jarvis 的虚构 AI 产品构建一条完整的反馈分析流水线。
你将编写 Node.js 代码，通过 Docker Model Runner 运行本地 LLM 和嵌入模型——
无需 API 密钥、无需云订阅，也没有任何数据离开你的
机器。

## 启动实验

{{< labspace-launch image="dockersamples/labspace-creating-ai-product-reviewer" >}}

## 你将学到什么

完成本 Labspace 后，你将掌握以下内容：

- 通过 Docker Model Runner 的 OpenAI 兼容 API 在本地运行 LLM
- 使用 OpenAI SDK 和 Compose 的 `models:` 集成，把 Node.js 应用连接到 Docker Model Runner
- 使用低温度的 LLM 分类完成情感分析
- 使用嵌入向量和余弦相似度对语义相关的反馈进行聚类
- 使用 `response_format: { type: 'json_object' }` 从 LLM 中提取结构化数据
- 基于提取出的产品功能点，生成结合上下文的评论回复

## 模块

| #   | 模块                                | 说明                                                                               |
| --- | ----------------------------------- | ---------------------------------------------------------------------------------- |
| 1   | 引言                                | 流水线概览与 Docker Model Runner 环境准备                                          |
| 2   | 项目搭建与 Docker Model Runner      | 浏览初始项目并接入 Compose 的模型集成                                              |
| 3   | 生成合成反馈                        | 使用 LLM 生成逼真的产品评论作为测试数据                                            |
| 4   | 情感分析                            | 使用低温度生成，将评论分类为正面、负面或中性                                       |
| 5   | 嵌入向量与语义聚类                  | 使用向量嵌入和余弦相似度对相关评论进行归类                                         |
| 6   | 功能点与回复                        | 提取可落地的功能点并生成结合上下文的评论回复                                       |
| 7   | 总结                                | 技术回顾与扩展流水线的思路                                                         |
