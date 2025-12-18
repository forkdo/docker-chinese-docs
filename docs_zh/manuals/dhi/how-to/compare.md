---
title: 比较 Docker Hardened Images
linktitle: 比较镜像
description: 了解如何将 Docker Hardened Images 与其他容器镜像进行比较，以评估安全改进和差异。
keywords: 比较 docker 镜像, docker scout compare, 镜像比较, 漏洞比较, 安全比较
weight: 40
---

Docker Hardened Images (DHIs) 旨在为您的应用程序提供增强的安全性、最小化的攻击面和生产就绪的基础。将 DHI 与标准镜像进行比较有助于您了解采用强化镜像的安全改进、软件包差异和整体优势。

本文档说明如何使用 Docker Scout 将 Docker Hardened Image 与另一个镜像（如 Docker Official Image (DOI) 或自定义镜像）进行比较，以评估漏洞、软件包和配置的差异。

## 使用 Docker Scout 比较镜像

Docker Scout 提供了内置的比较功能，可让您分析两个镜像之间的差异。这对于以下场景很有用：

- 评估从标准镜像迁移到 DHI 时的安全改进
- 了解镜像变体之间的软件包和漏洞差异
- 评估自定义或更新的影响

### 基本比较

要将 Docker Hardened Image 与另一个镜像进行比较，请使用 [`docker scout
compare`](/reference/cli/docker/scout/compare/) 命令：

```console
$ docker scout compare dhi.io/<image>:<tag> \
    --to <comparison-image>:<tag> \
    --platform <platform>
```

例如，要将 DHI Node.js 镜像与官方 Node.js 镜像进行比较：

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to node:22 \
    --platform linux/amd64
```

此命令提供详细的比较，包括：

- 漏洞差异（新增、移除或更改的 CVE）
- 软件包差异（新增、移除或更新的软件包）
- 整体安全态势改进

### 过滤未更改的软件包

要仅关注差异并忽略未更改的软件包，请使用 `--ignore-unchanged` 标志：

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to node:22 \
    --platform linux/amd64 \
    --ignore-unchanged
```

此输出仅突出显示两个镜像之间不同的软件包和漏洞，使您更容易识别安全改进和更改。

### 仅显示概览

要简洁地查看比较结果，您可以使用标准 shell 工具提取概览部分：

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to node:22 \
    --platform linux/amd64 \
    --ignore-unchanged \
    2>/dev/null | sed -n '/## Overview/,/^  ## /p' | head -n -1
```

结果是显示两个镜像之间关键差异的简洁摘要。示例输出：

```console
  ## Overview
  
                      │                    Analyzed Image                     │              Comparison Image
  ────────────────────┼───────────────────────────────────────────────────────┼─────────────────────────────────────────────
    Target            │  dhi.io/node:22-debian13                              │  node:22
      digest          │  55d471f61608                                         │  9ee3220f602f
      tag             │  22-debian13                                          │  22
      platform        │ linux/amd64                                           │ linux/amd64
      provenance      │ https://github.com/docker-hardened-images/definitions │ https://github.com/nodejs/docker-node.git
                      │  9fe491f53122b84eebba81e13f20157c18c10de2             │  bf78d7603fbea92cd3652edb3b2edadd6f5a3fe8
      vulnerabilities │    0C     0H     0M     0L                            │    0C     1H     3M   153L     4?
                      │           -1     -3   -153     -4                     │
      size            │ 41 MB (-367 MB)                                       │ 408 MB
      packages        │ 19 (-726)                                             │ 745
                      │                                                       │
```

## 解释比较结果

比较输出包括以下部分。

### 概览

概览部分提供两个镜像的高级统计信息：

- 目标和比较镜像的详细信息（摘要、标签、平台、来源）
- 每个镜像的漏洞计数
- 大小比较
- 软件包计数

请关注：

- 漏洞减少（增量行中的负数）
- 大小减少显示存储效率
- 软件包计数减少表明最小攻击面

### 环境变量

环境变量部分显示两个镜像之间不同的环境变量，前面带有 `+` 表示新增或 `-` 表示移除。

请关注：

- 移除的环境变量，这些变量可能对您的特定用例是必需的

### 标签

标签部分显示两个镜像之间不同的标签，前面带有 `+` 表示新增或 `-` 表示移除。

### 软件包和漏洞

软件包和漏洞部分列出所有软件包差异及其相关的安全漏洞。软件包前面带有：

- `-` 表示从目标镜像中移除的软件包（在比较的镜像中不存在）
- `+` 表示添加到目标镜像中的软件包（在基础镜像中不存在）
- `↑` 表示在目标镜像中升级的软件包
- `↓` 表示在目标镜像中降级的软件包

对于有关联漏洞的软件包，CVE 会列出其严重性级别和标识符。

请关注：

- 移除的软件包和漏洞：表明 DHI 的攻击面减少
- 新增的软件包：可能表示 DHI 特定的工具或依赖项
- 升级的软件包：显示可能包含安全修复的版本更新

## 何时比较镜像

### 评估迁移优势

在从 Docker Official Image 迁移到 DHI 之前，比较它们以了解安全改进。例如：

```console
$ docker scout compare dhi.io/python:3.13 \
    --to python:3.13 \
    --platform linux/amd64 \
    --ignore-unchanged
```

这有助于通过显示具体的漏洞减少和软件包最小化来证明迁移的合理性。

### 评估自定义影响

自定义 DHI 后，将自定义版本与原始版本进行比较，以确保您没有引入新的漏洞。例如：

```console
$ docker scout compare <your-namespace>/dhi-python:3.13-custom \
    --to dhi.io/python:3.13 \
    --platform linux/amd64
```

### 跟踪随时间的变化

比较同一 DHI 的不同版本，以查看版本之间的变化。例如：

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to dhi.io/node:20-debian12 \
    --platform linux/amd64 \
    --ignore-unchanged
```