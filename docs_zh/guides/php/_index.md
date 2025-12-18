---
title: PHP 语言特定指南
linkTitle: PHP
description: 使用 Docker 容器化和开发 PHP 应用
keywords: 入门, php, composer
summary: |
  本指南介绍如何使用 Docker 容器化 PHP 应用。
toc_min: 1
toc_max: 2
aliases:
  - /language/php/
  - /guides/language/php/
languages: [php]
params:
  time: 20 分钟
---

PHP 语言特定指南教你如何使用 Docker 创建容器化的 PHP 应用。在本指南中，你将学习如何：

- 容器化并运行 PHP 应用
- 使用容器设置本地环境来开发 PHP 应用
- 在容器内运行 PHP 应用的测试
- 使用 GitHub Actions 为容器化的 PHP 应用配置 CI/CD 管道
- 将你的容器化应用本地部署到 Kubernetes 以测试和调试你的部署

完成 PHP 语言特定指南后，你应该能够根据本指南中提供的示例和说明容器化你自己的 PHP 应用。

首先从容器化一个现有的 PHP 应用开始。