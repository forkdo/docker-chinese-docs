---
title: 通过 Microsoft Store 在 Windows 上安装 Docker Desktop
linkTitle: MS Store
description: 通过 Microsoft Store 安装 Windows 版 Docker Desktop。了解其更新行为和限制。
keywords: microsoft store, windows, docker desktop, install, deploy, configure, admin, mdm, intune, winget
tags: [admin]
weight: 30
aliases: 
 - /desktop/setup/install/enterprise-deployment/ms-store/
---

你可以通过 [Microsoft 应用商店](https://apps.microsoft.com/detail/xp8cbj40xlbwkx?hl=en-GB&gl=GB) 部署 Windows 版 Docker Desktop。

Microsoft Store 版本的 Docker Desktop 提供与标准安装程序相同的功能，但根据开发者是自行安装还是通过 Intune 等 MDM 工具管理安装，其更新行为有所不同。以下部分将详细说明。

请根据你的环境需求和管理实践选择合适的安装方式。

## 更新行为

### 开发者自主安装

对于直接安装 Docker Desktop 的开发者：

- Microsoft Store 不会自动更新大多数用户的 Win32 应用（如 Docker Desktop）。
- 只有部分用户（约 20%）可能在 Microsoft Store 页面收到更新通知。
- 大多数用户必须在商店中手动检查并应用更新。

### Intune 管理的安装

在使用 Intune 管理的环境中：
- Intune 约每 8 小时检查一次更新。
- 检测到新版本后，Intune 触发 `winget` 升级。
- 如果配置了适当的策略，更新可以自动进行，无需用户干预。
- 更新由 Intune 的管理基础架构处理，而非 Microsoft Store 本身。

## WSL 考虑事项

Windows 版 Docker Desktop 与 WSL 紧密集成。更新从 Microsoft Store 安装的 Docker Desktop 时：
- 确保已退出 Docker Desktop 并且不再运行，以便更新能够成功完成。
- 在某些环境中，虚拟硬盘 (VHDX) 文件锁可能会阻止更新完成。

## Intune 管理建议

如果使用 Intune 管理 Windows 版 Docker Desktop：
- 确保 Intune 策略已配置为处理应用程序更新。
- 请注意，更新过程使用 WinGet API 而非直接的 Store 机制。
- 考虑在受控环境中测试更新过程，以验证其正常功能。