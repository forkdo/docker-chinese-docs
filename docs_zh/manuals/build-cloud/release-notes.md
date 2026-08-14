---
description: 了解 Docker Build Cloud 的最新功能
keywords: docker build cloud, release notes, changelog, features, changes, delta, new, releases
title: Docker Build Cloud 发布说明
linkTitle: 发布说明
tags:
- release-notes
---

此页面包含有关 Docker Build Cloud 各版本中的新功能、改进、已知问题和错误修复的信息。

## 2026-08-03

### 增强功能

- 云构建器现在运行 BuildKit v0.32.1，从 v0.20.0 升级而来。本次升级跨越了十二个 BuildKit 次要版本的发布，带来了新的构建功能、性能改进和错误修复。完整的变更列表，请参阅 [BuildKit 发布说明](https://github.com/moby/buildkit/releases)。

  此范围包含以下默认行为的变更。其中每一项都是您通过 `--output` 传入的[导出器属性](/manuals/build/exporters/image-registry.md)，或通过 `--attest` 传入的[证明属性](/manuals/build/metadata/attestations/_index.md)：

  - 镜像结果现在默认使用 OCI 媒体类型。如果您的注册表不支持 OCI 媒体类型，请使用 `--output type=image,oci-mediatypes=false` 进行构建。在您的注册表支持 OCI 媒体类型之前，请将此视为一种临时措施。
  - 证明现在默认使用 OCI 制品描述符。如果您的注册表不支持 OCI 制品，请使用 `--output type=image,oci-artifact=false` 进行构建。请注意该属性是单数形式。
  - [来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)现在默认使用 SLSA v1 而非 v0.2，这同时改变了断言类型和架构。如果您在 CI 流水线中验证来源证明，请在下一次构建之前确认您的验证器支持 SLSA v1 断言。无法识别新断言类型的验证器可能会报告未找到任何证明，而不是直接失败，从而可能在不知不觉中削弱供应链检查。若要在更新工具期间保持原有格式，请使用 `--attest type=provenance,version=v0.2` 进行构建。

- Docker Build Cloud 已基于 Buildx v0.36.0 完成验证，较之前的 v0.21.0 有所提升。Buildx 是您用于构建的客户端，它随 Docker Desktop 和 Docker Engine 分发，而非随 Docker Build Cloud 分发，因此您的客户端版本取决于您安装 Docker 的方式。有关使用云构建器时可用的客户端功能，请参阅 [Buildx 发布说明](https://github.com/docker/buildx/releases)。

## 2025-12-19

### 错误修复

- 修复了使用云构建器构建 [Docker Hardened Images](/manuals/dhi/_index.md) 时出现的错误。
- 修复了在传输大量数据时因 gRPC 消息大小错误而导致构建失败的问题。
- 修复了在通过 OCI referrers 回退机制解析证明或签名时拉取镜像出现的 500 错误（注册表在不直接实现 referrers API 时会使用此回退机制）。

## 2025-06-04

### 增强功能

- 构建超时时间现在由您的订阅套餐决定，而非应用于所有构建的单一固定限制。

## 2025-04-29

### 增强功能

- 改进了构建错误消息。由您的 Dockerfile 或构建上下文导致的失败现在会报告为构建错误，而不是内部错误。这包括被拒绝的基础镜像拉取、无效的阶段名称，以及无效的 `chmod` 和 `mkdir` 目标。

## 2025-04-09

### 增强功能

- 新增了涵盖您组织内所有构建的合并云使用报告。

## 2025-03-05

### 增强功能

- 构建使用报告现在支持自定义日期范围。

## 2025-02-24

### 新增功能

新增了 **Build settings**（构建设置）页面，您可以在其中为组织中的云构建器配置磁盘分配、私有资源访问和防火墙设置。这些配置有助于优化存储、启用对私有注册表的访问以及保护出站网络流量。
