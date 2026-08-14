---
aliases:
  - /dhi/core-concepts/glibc-musl/
title: glibc and musl support in Docker Hardened Images（DHI 中的 glibc 与 musl 支持）
linktitle: glibc and musl
description: 比较 DHI 的 glibc 和 musl 变体，为应用程序的兼容性、大小和性能需求选择正确的基础镜像。
keywords: glibc vs musl, alpine musl image, debian glibc container, docker hardened images compatibility, c library in containers
---

Docker Hardened Images（DHI）的构建优先考虑安全性，同时不牺牲与更广泛的开源和企业软件生态系统的兼容性。这种兼容性的一个关键方面是对常见 Linux 标准库的支持：`glibc` 和 `musl`。

## What are glibc and musl?（什么是 glibc 和 musl？）

当你运行基于 Linux 的容器时，镜像的 C 库在应用程序与操作系统交互的方式中扮演着关键角色。大多数现代 Linux 发行版依赖于以下标准 C 库之一：

- `glibc`（GNU C Library）：主流发行版（如 Debian、Ubuntu 和 Red Hat Enterprise Linux）上的标准 C 库。它受到广泛支持，通常被认为是跨语言、框架和企业软件最具兼容性的选项。

- `musl`：一种轻量级的 `glibc` 替代方案，常用于 Alpine Linux 等精简发行版。虽然它提供了更小的镜像体积和性能优势，但 `musl` 并不总是与期望 `glibc` 的软件完全兼容。

## DHI compatibility（DHI 兼容性）

DHI 镜像同时提供基于 `glibc`（例如 Debian）和基于 `musl`（例如 Alpine）的变体。对于企业应用程序和兼容性至关重要的语言运行时，我们建议使用基于 glibc 的 DHI 镜像。

## What to choose, glibc or musl?（如何选择，glibc 还是 musl？）

Docker Hardened Images 同时提供基于 glibc（Debian）和基于 musl（Alpine）的变体，让你可以为工作负载选择最合适的方案。

如果满足以下条件，请选择基于 Debian（`glibc`）的镜像：

- 你需要与企业工作负载、语言运行时或专有软件的广泛兼容性。
- 你正在使用依赖 `glibc` 的生态系统，如带有原生扩展的 .NET、Java 或 Python。
- 你希望最小化因库不兼容导致的运行时错误风险。

如果满足以下条件，请选择基于 Alpine（`musl`）的镜像：

- 你需要具有更小镜像体积和缩小表面面积的最小占用空间。
- 你正在构建一个依赖项已知且经过测试的自定义或严格受控的应用程序栈。
- 你优先考虑启动速度和精简部署，而非最大兼容性。

如果不确定，请从基于 Debian 的镜像开始以确保兼容性，并在确认应用程序的依赖项后评估 Alpine。
