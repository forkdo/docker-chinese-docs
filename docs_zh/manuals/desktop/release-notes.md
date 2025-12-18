---
description: 查找 Docker Desktop 的 Mac、Linux 和 Windows 版本发布说明。
keywords: Docker desktop, release notes, linux, mac, windows
title: Docker Desktop 发布说明
linkTitle: 发布说明
tags: [Release notes]
toc_max: 2
aliases:
- /docker-for-mac/release-notes/
- /docker-for-mac/edge-release-notes/
- /desktop/mac/release-notes/
- /docker-for-windows/edge-release-notes/
- /docker-for-windows/release-notes/
- /desktop/windows/release-notes/
- /desktop/linux/release-notes/
- /mackit/release-notes/
weight: 220
outputs: ["HTML", "markdown", "RSS"]
type: "desktop-release"
---
{{< rss-button feed="/desktop/release-notes/index.xml" text="订阅 Docker Desktop RSS 源" >}}

<!-- vale off -->

本文档包含 Docker Desktop 发布版本中新增功能、改进、已知问题和错误修复的信息。

发布版本会逐步推出，以确保质量控制。如果最新版本尚未对您可用，请耐心等待——更新通常在发布日期后一周内可用。

Docker Desktop 最新发布版本前 6 个月的旧版本无法下载。之前的发布说明可在我们的 [文档仓库](https://github.com/docker/docs/tree/main/content/manuals/desktop/previous-versions) 中找到。

有关更频繁的常见问题解答，请参阅 [FAQs](/manuals/desktop/troubleshoot-and-support/faqs/releases.md)。

## 4.55.0

{{< release-date date="2025-12-16" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.55.0" build_path="/213807/" >}}

### 更新

- [Docker Engine v29.1.3](https://docs.docker.com/engine/release-notes/29/#2913)
- [cagent v1.15.1](https://github.com/docker/cagent/releases/tag/v1.15.1)

### 错误修复和增强

#### 适用于所有平台

- 修复了导致 Docker Desktop 在启动期间卡住的问题。
- 改进了 `daemon.json` 无效时的错误消息。
- 修复了在长 Ask Gordon 会话中每次按键时的性能问题。

> [!IMPORTANT]
>
> Wasm 工作负载将在未来的 Docker Desktop 版本中被弃用并移除。

## 4.54.0

{{< release-date date="2025-12-04" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.54.0" build_path="/212467/" >}}

### 新增功能

- 在 Windows 上使用 WSL2 和 NVIDIA GPU 为 Docker Model Runner 添加了 vLLM 支持。

### 错误修复和增强

#### 适用于 Mac

- 修复了一个错误，即 `/dev/shm` 没有足够的权限供容器写入。修复 [docker/for-mac#7804](https://github.com/docker/for-mac/issues/7804)。

### 升级

- [Docker Buildx v0.30.1](https://github.com/docker/buildx/releases/tag/v0.30.1)
- [Docker Engine v29.1.2](https://docs.docker.com/engine/release-notes/29/#2912)
- [Runc v1.3.4](https://github.com/opencontainers/runc/releases/tag/v1.3.4)
- [Docker Model Runner CLI v1.0.2](https://github.com/docker/model-runner/releases/tag/cmd%2Fcli%2Fv1.0.2)

### 安全

- 添加了一个安全补丁以解决 [CVE-2025-13743](https://www.cve.org/cverecord?id=CVE-2025-13743)，该问题导致 Docker Desktop 诊断包因错误对象序列化而在日志输出中包含过期的 Hub PAT。

## 4.53.0

{{< release-date date="2025-11-27" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4.53.0" build_path="/211793/" >}}

### 错误修复和增强

#### 适用于所有平台

- 修复了支持诊断工具意外捕获过期 Docker Hub 授权承载令牌的问题。

### 安全

- 添加了安全补丁以解决 CVEs [2025-52565](https://github.com/opencontainers/runc/security/advisories/GHSA-9493-h29p-rfm2)、[2025-52881](https://github.com/opencontainers/runc/security/advisories/GHSA-cgrx-mc8f-2prm) 和 [2025-31133](https://github.com/opencontainers/runc/security/advisories/GHSA-qw9x-cqr3-wc7r)，这些在使用 [增强容器隔离](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation) 时出现。

## 4.52.0

{{< release-date date="2025-11-20" >}}

{{< desktop-install-v2 all=true win_arm_release="Early Access" version="4