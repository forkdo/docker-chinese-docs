---
description: 修复 macOS 上“Docker.app 已损坏，无法打开。您应该将其移到废纸篓”对话框
keywords: docker desktop mac, damaged app, move to trash, gatekeeper, installation issues, troubleshooting
title: 修复 macOS 上“Docker.app 已损坏，无法打开”问题
linkTitle: macOS 应用已损坏对话框
tags: [Troubleshooting]
weight: 30
---

## 错误信息

在 macOS 上尝试打开 Docker Desktop 时，系统会显示以下对话框：

```text
Docker.app 已损坏，无法打开。您应该将其移到废纸篓。
```

此错误会阻止 Docker Desktop 启动，可能出现在安装过程中或更新后。

## 可能的原因

此问题是由于在拖放安装过程中进行了非原子复制操作导致的。当您在另一个应用程序（如 VS Code）通过符号链接调用 Docker CLI 的同时，从 DMG 文件中拖放 `Docker.app` 时，复制操作可能会被中断，导致应用程序处于部分复制状态，Gatekeeper 会将其标记为“已损坏”。

## 解决方案

请按照以下步骤解决问题：

### 第一步：退出第三方软件

关闭任何可能在后台调用 Docker 的应用程序：

- Visual Studio Code 和其他 IDE
- 终端应用程序
- 代理应用或开发工具
- 任何使用 Docker CLI 的脚本或进程

### 第二步：移除任何部分安装

1. 将 `/Applications/Docker.app` 移到废纸篓并清空废纸篓。
2. 如果您使用的是 DMG 安装程序，请弹出并重新挂载 Docker DMG。

### 第三步：重新安装 Docker Desktop

按照 [macOS 安装指南](/manuals/desktop/setup/install/mac-install.md) 中的说明重新安装 Docker Desktop。

### 如果对话框仍然存在

如果在执行恢复步骤后仍然看到“已损坏”对话框：

1. 使用终端收集诊断信息。按照 [从终端诊断](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md#diagnose-from-the-terminal) 中的说明操作。

   - 记录运行诊断后在终端中显示的诊断 ID。

2. 获取帮助：
   - 如果您有付费 Docker 订阅，请 [联系支持](/manuals/support/_index.md) 并包含您的诊断 ID
   - 对于社区用户，请在 [GitHub 上打开问题](https://github.com/docker/desktop-feedback) 并包含您的诊断 ID

## 预防措施

为避免将来出现此问题：

- 如果您的组织允许，请通过应用内更新流程更新 Docker Desktop
- 在使用 DMG 安装程序进行拖放安装之前，始终退出使用 Docker 的应用程序
- 在受管理的环境中，优先使用 PKG 安装而不是 DMG 拖放安装
- 保持安装卷挂载状态，直到安装完成

## 相关信息

- [在 Mac 上安装 Docker Desktop](/manuals/desktop/setup/install/mac-install.md)
- [PKG 安装程序文档](/manuals/enterprise/enterprise-deployment/pkg-install-and-configure.md)
- [Docker Desktop 故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md)
- [已知问题](/manuals/desktop/troubleshoot-and-support/troubleshoot/known-issues.md)