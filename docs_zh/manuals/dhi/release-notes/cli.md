---
title: DHI CLI release notes
linkTitle: CLI release notes
description: DHI CLI 中的新功能、错误修复和变更
keywords: docker hardened images, dhi, dhictl, cli, release notes, changelog
toc_min: 1
toc_max: 2
tags:
  - Release notes
---

本页面列出了 DHI CLI（`docker dhi`）近期稳定版本的变更。
有关包括预发布版本和下载在内的完整发布历史，请参阅 GitHub 上的
[dhictl releases](https://github.com/docker-hardened-images/dhictl/releases)。

<!-- BEGIN GENERATED RELEASES -->

## 0.0.7

{{< release-date date="2026-07-21" >}}

[GitHub release](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.7)

### 错误修复

- 修复 JSON 输出错误地将 `&` 转义为 `\u0026` 的问题 —— 包含 `&` 的目录分类等取值现在会原样显示

## 0.0.6

{{< release-date date="2026-07-13" >}}

[GitHub release](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.6)

此版本修复了导致无法通过 CLI 创建自定义配置的问题。

### 错误修复

- 修复当 GraphQL 因 OCI 制品数据中错误地包含了仅供输出的 `__typename` 字段而拒绝 mutation 输入时，`dhictl customization create` 失败的问题

## 0.0.5

{{< release-date date="2026-06-29" >}}

[GitHub release](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.5)

包含依赖项更新的维护版本。

## 0.0.4

{{< release-date date="2026-05-25" >}}

[GitHub release](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.4)

### 新增功能

- 为 DHI DEB 仓库新增 `deb` 子命令，用于生成针对 DHI DEB 仓库进行身份验证的 netrc 风格凭据

## 0.0.3

{{< release-date date="2026-04-22" >}}

[GitHub release](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.3)

### 新增功能

- 新增用于管理证明的 attestation list 和 get 命令
- 为软件物料清单证明新增 SBOM 子命令
- 为自定义配置的 prepare 命令新增批量支持
- 为自定义配置新增 compression 字段支持
- 在 catalog get 输出中新增 tag-definition-id 列

### 破坏性变更

我们移除了少数几个带有 `--output` 标志的命令（`customization prepare` 和 `customization get`）中的该标志，改用标准输出重定向。
```console
# 之前
dhictl customization prepare --org my-org golang 1.25 --output my-customization.yaml

# 之后 
dhictl customization prepare --org my-org golang 1.25 > my-customization.yaml
```

## 0.0.2

{{< release-date date="2026-03-19" >}}

[GitHub release](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.2)

这是一个侧重于构建系统改进的维护版本。

### 技术变更

- 全局禁用 CGO 以修复 macOS 16 的 dyld 崩溃问题并简化构建流程

## 0.0.1

{{< release-date date="2026-03-12" >}}

[GitHub release](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.1)

此版本通过允许传入命令参数改进了 dhictl 中的镜像功能。

### 改进

- Mirror start 命令现在接受参数，以支持更灵活的镜像操作

<!-- END GENERATED RELEASES -->

## 早期版本

有关更旧的版本，请参阅 GitHub 上的
[dhictl releases](https://github.com/docker-hardened-images/dhictl/releases)。
