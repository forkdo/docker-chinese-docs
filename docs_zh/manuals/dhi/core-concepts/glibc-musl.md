---
title: Docker Hardened Images 中的 glibc 和 musl 支持
linktitle: glibc 和 musl
description: 比较 DHI 的 glibc 和 musl 变体，为您的应用程序在兼容性、大小和性能方面的需求选择合适的基镜像。
keywords: glibc 与 musl, alpine musl 镜像, debian glibc 容器, docker 硬化镜像兼容性, 容器中的 C 库
---

Docker Hardened Images (DHI) 在不牺牲与更广泛的开源和企业软件生态系统兼容性的情况下，优先考虑安全性。这种兼容性的一个关键方面是对常见 Linux 标准库的支持：`glibc` 和 `musl`。

## 什么是 glibc 和 musl？

当您运行基于 Linux 的容器时，镜像的 C 库在应用程序与操作系统交互方面起着关键作用。大多数现代 Linux 发行版依赖以下标准 C 库之一：

- `glibc`（GNU C 库）：主流发行版（如 Debian、Ubuntu 和 Red Hat Enterprise Linux）上的标准 C 库。它得到广泛支持，通常被认为是跨语言、框架和企业软件的最兼容选项。

- `musl`：`glibc` 的轻量级替代品，通常用于 Alpine Linux 等最小化发行版。虽然它提供更小的镜像大小和性能优势，但 `musl` 并不总是与期望 `glibc` 的软件完全兼容。

## DHI 兼容性

DHI 镜像同时提供基于 `glibc`（例如 Debian）和基于 `musl`（例如 Alpine）的变体。对于兼容性至关重要的企业应用程序和语言运行时，我们建议使用基于 glibc 的 DHI 镜像。

## 选择 glibc 还是 musl？

Docker Hardened Images 同时提供基于 glibc（Debian）和基于 musl（Alpine）的变体，允许您为工作负载选择最合适的选项。

如果符合以下情况，请选择基于 Debian（`glibc`）的镜像：

- 您需要与企业工作负载、语言运行时或专有软件广泛兼容。
- 您正在使用依赖 `glibc` 的生态系统，如 .NET、Java 或带有原生扩展的 Python。
- 您希望最大限度地降低因库不兼容导致运行时错误的风险。

如果符合以下情况，请选择基于 Alpine（`musl`）的镜像：

- 您希望获得更小的占用空间，包括更小的镜像大小和更小的攻击面。
- 您正在构建自定义或严格控制的应用程序栈，其中依赖项已知且经过测试。
- 与最大兼容性相比，您更重视启动速度和精简部署。

如果您不确定，请先使用基于 Debian 的镜像以确保兼容性，然后在您对应用程序的依赖项有信心后再评估 Alpine。