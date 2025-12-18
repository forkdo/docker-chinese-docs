---
title: 测试
description: 测试您的 Docker 设置。
weight: 30
---

## SSO 和 SCIM 测试

通过使用与已验证域关联的 Docker 账户的电子邮件地址登录 Docker Desktop 或 Docker Hub 来测试 SSO 和 SCIM。使用 Docker 用户名登录的开发人员不受 SSO 和 SCIM 设置的影响。

> [!IMPORTANT]
>
> 某些用户可能需要通过 CLI 登录 Docker Hub，为此他们需要一个[个人访问令牌 (PAT)](/manuals/security/access-tokens.md)。

## 测试注册表访问管理 (RAM) 和镜像访问管理 (IAM)

> [!WARNING]
>
> 在继续之前请与您的用户沟通，因为此步骤将影响所有登录到您 Docker 组织的现有用户。

如果您计划使用[注册表访问管理 (RAM)](/manuals/enterprise/security/hardened-desktop/registry-access-management.md) 和/或[镜像访问管理 (IAM)](/manuals/enterprise/security/hardened-desktop/image-access-management.md)：

1. 确保您的测试开发人员使用其组织凭据登录 Docker Desktop
2. 让他们尝试通过 Docker CLI 拉取一个未授权的镜像或来自不允许的注册表的镜像
3. 验证他们收到错误消息，表明该注册表受到组织限制

## 部署设置并为测试组强制登录

通过 MDM 为一小部分测试用户部署 Docker 设置并强制登录。让该组测试用户在 Docker Desktop 和 Docker Hub 上测试他们的容器开发工作流，以确保所有设置和登录强制功能按预期工作。

## 测试 Docker Build Cloud 功能

让您的 Docker Desktop 测试人员[连接到您创建的云构建器并使用它进行构建](/manuals/build-cloud/usage.md)。

## 测试 Testcontainers Cloud

让测试开发人员[连接到 Testcontainers Cloud](https://testcontainers.com/cloud/docs/#getting-started) 并在云端运行一个容器，以验证设置是否正确工作。

## 验证 Docker Scout 监控仓库

检查[Docker Scout 仪表板](https://scout.docker.com/)，确认已启用 Docker Scout 的仓库正在正确接收数据。

## 验证对 Docker Hardened 镜像的访问

让测试开发人员尝试[拉取一个 Docker Hardened 镜像](/manuals/dhi/get-started.md)，以确认团队具有适当的访问权限，并能够将这些镜像集成到他们的工作流中。