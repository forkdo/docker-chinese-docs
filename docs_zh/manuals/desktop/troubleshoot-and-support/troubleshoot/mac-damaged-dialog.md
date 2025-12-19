---
description: 修复 macOS 上出现的 "Docker.app 已损坏，无法打开。您应该将其移到废纸篓" 对话框
keywords: docker desktop mac, damaged app, move to trash, gatekeeper, installation issues, troubleshooting
title: 在 macOS 上修复 "Docker.app 已损坏，无法打开" 问题
linkTitle: MacOS 应用程序损坏对话框
tags: [故障排除]
weight: 30
---

## 错误信息

当您尝试打开 Docker Desktop 时，macOS 会显示以下对话框：

```text
Docker.app 已损坏，无法打开。您应该将其移到废纸篓。
```

此错误会阻止 Docker Desktop 启动，可能在安装期间或更新后发生。

## 可能的原因

此问题是由于拖拽安装过程中的非原子复制操作导致的。当您从 DMG 文件中拖放 `Docker.app` 时，如果有其他应用程序（如 VS Code）正在通过符号链接调用 Docker CLI，复制操作可能会被中断，导致应用程序处于部分复制状态，从而被 Gatekeeper 标记为“已损坏”。

## 解决方案

请按照以下步骤解决问题：

### 第一步：退出第三方软件

关闭任何可能在后台调用 Docker 的应用程序：

- Visual Studio Code 和其他 IDE
- 终端应用程序
- 代理应用程序或开发工具
- 任何使用 Docker CLI 的脚本或进程

### 第二步：移除任何部分安装

1. 将 `/Applications/Docker.app` 移到废纸篓并清空废纸篓。
2. 如果您使用了 DMG 安装程序，请推出并重新挂载 Docker DMG。

### 第三步：重新安装 Docker Desktop

按照 [macOS 安装指南](/manuals/desktop/setup/install/mac-install.md) 中的说明重新安装 Docker Desktop。

### 如果对话框仍然出现

如果在执行恢复步骤后仍然看到“已损坏”对话框：

1. 使用终端收集诊断信息。按照 [从终端诊断](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md#diagnose-from-the-terminal) 中的说明操作。

   - 记下运行诊断后在终端中显示的诊断 ID。

2. 寻求帮助：
   - 如果您拥有付费的 Docker 订阅，请 [联系支持](/manuals/support/_index.md) 并附上您的诊断 ID
   - 对于社区用户，请 [在 GitHub 上提交 issue](https://github.com/docker/for-mac/issues) 并附上您的诊断 ID

## 预防措施

为避免将来出现此问题：

- 如果您的组织允许，请通过应用内更新流程更新 Docker Desktop
- 在通过 DMG 安装程序拖放方式安装 Docker Desktop 之前，始终退出使用 Docker 的应用程序
- 在受管环境中，使用 PKG 安装而不是 DMG 拖放
- 保持安装程序卷挂载，直到安装完成

## 相关信息

- [在 Mac 上安装 Docker Desktop](/manuals/desktop/setup/install/mac-install.md)
- [PKG 安装程序文档](/manuals/enterprise/enterprise-deployment/pkg-install-and-configure.md)
- [排查 Docker Desktop 问题](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md)
- [已知问题](/manuals/desktop/troubleshoot-and-support/troubleshoot/known-issues.md)