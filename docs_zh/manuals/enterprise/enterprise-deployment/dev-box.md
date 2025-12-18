---
Title: Microsoft Dev Box 中的 Docker Desktop
linkTitle: Microsoft Dev Box
description: 了解在 Microsoft Dev Box 中使用 Docker Desktop 的优势以及如何进行设置
keywords: desktop, docker, windows, microsoft dev box
weight: 60
aliases:
 - /desktop/features/dev-box/
 - /desktop/setup/install/enterprise-deployment/dev-box/
---

Docker Desktop 可作为 Microsoft Azure Marketplace 中的预配置镜像，用于 Microsoft Dev Box，允许开发人员快速在云端设置一致的开发环境。

Microsoft Dev Box 提供基于云的、预配置的开发者工作站，让您无需配置本地开发环境即可进行编码、构建和测试应用程序。Microsoft Dev Box 的 Docker Desktop 镜像已预安装并配置了 Docker Desktop 及其依赖项，为您提供即用即用的容器化开发环境。

## 主要优势

- 预配置环境：Docker Desktop、WSL2 和其他需求已预安装并配置
- 一致的开发体验：确保所有团队成员使用相同的 Docker 环境
- 强大资源：访问比本地机器可能更强大的计算能力和存储空间
- 状态持久化：Dev Box 在会话之间保持您的状态，类似于本地机器的休眠功能
- 无缝授权：使用现有的 Docker 订阅或直接通过 Azure Marketplace 购买新订阅

## 设置步骤

### 前置条件

- Azure 订阅
- Microsoft Dev Box 访问权限
- Docker 订阅（Pro、Team 或 Business）。您可以通过以下任一方式在 Microsoft Dev Box 中使用 Docker Desktop：
   - 现有的或新购买的 Docker 订阅
   - 通过 Azure Marketplace 直接购买的新 Docker 订阅
   - 为组织配置了 SSO 的 Docker Business 订阅

### 在 Dev Box 中设置 Docker Desktop

1. 导航至 Azure Marketplace 中的 [Docker Desktop for Microsoft Dev Box](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/dockerinc1694120899427.devbox_azuremachine?tab=Overview) 页面。
2. 选择 **Get It Now** 将虚拟机镜像添加到您的订阅中。
3. 按照 Azure 工作流程完成设置。
4. 使用该镜像创建虚拟机、分配到 Dev Center，或根据组织的设置创建 Dev Box 池。

### 激活 Docker Desktop

Dev Box 使用 Docker Desktop 镜像配置完成后：

1. 启动您的 Dev Box 实例。
2. 启动 Docker Desktop。
3. 使用您的 Docker ID 登录。

## 支持

如遇到以下问题：

- Docker Desktop 配置、使用或授权问题：通过 [Docker Support](https://hub.docker.com/support) 创建支持工单。
- Dev Box 创建、Azure 门户配置或网络问题：联系 Azure 支持。

## 限制

- Microsoft Dev Box 当前仅支持 Windows 10 和 11（不支持 Linux 虚拟机）。
- 性能可能因您的 Dev Box 配置和网络条件而异。