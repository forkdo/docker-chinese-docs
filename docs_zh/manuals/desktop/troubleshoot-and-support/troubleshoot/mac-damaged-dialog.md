---
description: 修复 macOS 上出现的“Docker.app 已损坏，无法打开。您应该将它移到废纸篓”对话框问题
title: 修复 macOS 上“Docker.app 已损坏，无法打开”的问题
linkTitle: macOS 应用损坏对话框
weight: 30
tags:
- Troubleshooting
keywords: docker desktop mac, damaged app, move to trash, gatekeeper, installation
  issues, troubleshooting
---
## 错误信息

当您尝试打开 Docker Desktop 时，macOS 会显示以下对话框：

```text
Docker.app is damaged and can't be opened. You should move it to the Trash.
```

此错误会阻止 Docker Desktop 启动，可能发生在安装期间或更新之后。

## 可能的原因

此问题是由于拖放安装过程中的非原子性复制引起的。当您从 DMG 文件中将 `Docker.app` 拖放到 Applications 文件夹时，如果另一个应用程序（如 VS Code）正在通过符号链接调用 Docker CLI，复制操作可能会被中断，导致应用程序处于部分复制的状态，从而被 Gatekeeper 标记为“已损坏”。

## 解决方案

请按照以下步骤解决此问题：

### 步骤一：退出第三方软件

关闭任何可能在后台调用 Docker 的应用程序：

- Visual Studio Code 及其他 IDE
- 终端应用程序
- 代理应用或开发工具
- 任何使用 Docker CLI 的脚本或进程

### 步骤二：移除任何不完整的安装

1. 将 `/Applications/Docker.app` 移至废纸篓并清空废纸篓。
2. 如果您使用了 DMG 安装器，请先推出并重新装载 Docker 的 DMG 文件。

### 步骤三：重新安装 Docker Desktop

按照 [macOS 安装指南](/manuals/desktop/setup/install/mac-install.md) 中的说明重新安装 Docker Desktop。

### 如果对话框仍然出现

如果在执行恢复步骤后，您仍然看到“已损坏”的对话框：

1. 使用终端收集诊断信息。请按照 [从终端进行诊断](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md#diagnose-from-the-terminal) 中的说明操作。

   - 运行诊断后，请记下终端中显示的诊断 ID。

2. 获取帮助：
   - 如果您拥有付费的 Docker 订阅，请[联系支持团队](/manuals/support/_index.md) 并附上您的诊断 ID。
   - 对于社区用户，请在 [GitHub 上创建 issue](https://github.com/docker/for-mac/issues) 并附上您的诊断 ID。

## 预防措施

为避免将来再次出现此问题：

- 如果您的组织允许，请通过应用内更新流程来更新 Docker Desktop。
- 在使用 DMG 安装器进行拖放安装之前，务必先退出所有使用 Docker 的应用程序。
- 在托管环境中，请优先使用 PKG 安装包，而不是 DMG 拖放安装。
- 在安装完成之前，请保持安装器宗卷的挂载状态。

## 相关信息

- [在 Mac 上安装 Docker Desktop](/manuals/desktop/setup/install/mac-install.md)
- [PKG 安装器文档](/manuals/enterprise/enterprise-deployment/pkg-install-and-configure.md)
- [Docker Desktop 故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md)
- [已知问题](/manuals/desktop/troubleshoot-and-support/troubleshoot/known-issues.md)