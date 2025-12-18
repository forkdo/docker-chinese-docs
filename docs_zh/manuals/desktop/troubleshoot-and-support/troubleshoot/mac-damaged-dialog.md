---
description: 修复在 macOS 上出现的“Docker.app 已损坏，无法打开。您应该将它移到废纸篓”的对话框
keywords: docker desktop mac, 已损坏的应用, 移到废纸篓, gatekeeper, 安装问题, 故障排除
title: 修复在 macOS 上出现的“Docker.app 已损坏，无法打开”错误
linkTitle: MacOS 应用损坏对话框
tags: [Troubleshooting]
weight: 30
---

## 错误消息

在 macOS 上尝试打开 Docker Desktop 时，系统会显示以下对话框：

```text
Docker.app 已损坏，无法打开。您应该将它移到废纸篓。
```

此错误会阻止 Docker Desktop 启动，可能在安装过程中或更新后出现。

## 可能的原因

此问题是由于拖放安装期间的非原子复制操作导致的。当您从 DMG 文件中拖放 `Docker.app` 时，如果其他应用程序（如 VS Code）通过符号链接调用 Docker CLI，复制操作可能被中断，导致应用处于部分复制状态，Gatekeeper 会将其标记为“已损坏”。

## 解决方案

按照以下步骤解决此问题：

### 步骤一：退出第三方软件

关闭任何可能在后台调用 Docker 的应用程序：

- Visual Studio Code 和其他 IDE
- 终端应用程序
- 代理应用或开发工具
- 任何使用 Docker CLI 的脚本或进程

### 步骤二：删除部分安装

1. 将 `/Applications/Docker.app` 移到废纸篓并清空废纸篓。
2. 如果您使用的是 DMG 安装程序，请弹出并重新挂载 Docker DMG。

### 步骤三：重新安装 Docker Desktop

按照 [macOS 安装指南](/manuals/desktop/setup/install/mac-install.md) 中的说明重新安装 Docker Desktop。

### 如果对话框仍然存在

如果按照上述恢复步骤后仍然看到“已损坏”对话框：

1. 使用终端收集诊断信息。按照 [从终端诊断](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md#diagnose-from-the-terminal) 中的说明操作。

   - 记下运行诊断后终端中显示的诊断 ID。

2. 获取帮助：
   - 如果您有付费 Docker 订阅，请 [联系支持](/manuals/support/_index.md) 并包含您的诊断 ID
   - 对于社区用户，请 [在 GitHub 上提交问题](https://github.com/docker/for-mac/issues) 并包含您的诊断 ID

## 预防措施

为避免将来出现此问题：

- 如果您的组织允许，通过应用内更新流程更新 Docker Desktop
- 在通过 DMG 安装程序拖放方式安装 Docker Desktop 之前，始终退出使用 Docker 的应用程序
- 在受管理的环境中，使用 PKG 安装而非 DMG 拖放
- 保持安装程序卷挂载状态，直到安装完成

## 相关信息

- [在 Mac 上安装 Docker Desktop](/manuals/desktop/setup/install/mac-install.md)
- [PKG 安装程序文档](/manuals/enterprise/enterprise-deployment/pkg-install-and-configure.md)
- [故障排除 Docker Desktop](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md)
- [已知问题](/manuals/desktop/troubleshoot-and-support/troubleshoot/known-issues.md)