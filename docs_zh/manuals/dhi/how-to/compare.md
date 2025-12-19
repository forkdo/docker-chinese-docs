---
title: 对比 Docker Hardened 镜像
linktitle: 对比镜像
description: 了解如何对比 Docker Hardened 镜像与其他容器镜像，以评估安全性改进和差异。
keywords: compare docker images, docker scout compare, image comparison, vulnerability comparison, security comparison
weight: 40
---

Docker Hardened 镜像 (DHIs) 旨在为您的应用程序提供增强的安全性、最小化的攻击面以及可用于生产的可靠基础。将 DHI 与标准镜像进行对比，有助于您理解安全性改进、软件包差异以及采用强化镜像的整体优势。

本页介绍如何使用 Docker Scout 将 Docker Hardened 镜像与另一个镜像（例如 Docker 官方镜像 (DOI) 或自定义镜像）进行对比，以评估漏洞、软件包和配置方面的差异。

## 使用 Docker Scout 对比镜像

Docker Scout 提供了内置的对比功能，可用于分析两个镜像之间的差异。该功能适用于以下场景：

- 评估从标准镜像迁移到 DHI 时的安全性改进
- 理解不同镜像变体之间的软件包和漏洞差异
- 评估自定义或更新带来的影响

### 基本对比

要对比 Docker Hardened 镜像与另一个镜像，请使用 [`docker scout compare`](/reference/cli/docker/scout/compare/) 命令：

```console
$ docker scout compare dhi.io/<image>:<tag> \
    --to <comparison-image>:<tag> \
    --platform <platform>
```

例如，对比 DHI Node.js 镜像与官方 Node.js 镜像：

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to node:22 \
    --platform linux/amd64
```

该命令提供详细的对比结果，包括：

- 漏洞差异（新增、移除或变更的 CVE）
- 软件包差异（新增、移除或更新的软件包）
- 整体安全性改进

### 过滤未变更的软件包

若只想关注差异并忽略未变更的软件包，请使用 `--ignore-unchanged` 标志：

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to node:22 \
    --platform linux/amd64 \
    --ignore-unchanged
```

此输出仅突出显示两个镜像之间不同的软件包和漏洞，便于识别安全性改进和变更。

### 仅显示概览

如需获取简洁的对比结果概览，可使用标准 shell 工具仅提取概览部分：

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to node:22 \
    --platform linux/amd64 \
    --ignore-unchanged \
    2>/dev/null | sed -n '/## Overview/,/^  ## /p' | head -n -1
```

结果是一个清晰的摘要，显示两个镜像之间的关键差异。示例如下：

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

## 解读对比结果

对比输出包含以下部分。

### 概览

概览部分提供两个镜像的高级统计信息：

- 目标镜像和对比镜像的详细信息（摘要、标签、平台、来源）
- 每个镜像的漏洞数量
- 大小对比
- 软件包数量

重点关注：

- 漏洞减少（差值行中的负数）
- 大小减少，体现存储效率
- 软件包数量减少，表明攻击面更小

### 环境变量

环境变量部分显示两个镜像之间不同的环境变量，前缀 `+` 表示新增，`-` 表示移除。

重点关注：

- 移除的环境变量，这些变量可能对您特定的用例是必需的

### 标签

标签部分显示两个镜像之间不同的标签，前缀 `+` 表示新增，`-` 表示移除。

### 软件包和漏洞

软件包和漏洞部分列出所有软件包差异及其关联的安全漏洞。软件包前缀如下：

- `-` 表示从目标镜像中移除的软件包（对比镜像中不存在）
- `+` 表示添加到目标镜像中的软件包（基础镜像中不存在）
- `↑` 表示目标镜像中升级的软件包
- `↓` 表示目标镜像中降级的软件包

对于有关联漏洞的软件包，CVE 会列出其严重级别和标识符。

重点关注：

- 移除的软件包和漏洞：表明 DHI 的攻击面更小
- 新增的软件包：可能表示 DHI 特定的工具或依赖项
- 升级的软件包：显示可能包含安全修复的版本更新

## 何时对比镜像

### 评估迁移优势

在从 Docker 官方镜像迁移到 DHI 之前，先进行对比以了解安全性改进。例如：

```console
$ docker scout compare dhi.io/python:3.13 \
    --to python:3.13 \
    --platform linux/amd64 \
    --ignore-unchanged
```

这有助于通过展示具体的漏洞减少和软件包最小化来证明迁移的合理性。

### 评估自定义影响

自定义 DHI 后，将自定义版本与原始版本进行对比，以确保未引入新的漏洞。例如：

```console
$ docker scout compare <your-namespace>/dhi-python:3.13-custom \
    --to dhi.io/python:3.13 \
    --platform linux/amd64
```

### 跟踪版本更新

对比同一 DHI 的不同版本，以查看版本之间的变更。例如：

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to dhi.io/node:20-debian12 \
    --platform linux/amd64 \
    --ignore-unchanged
```