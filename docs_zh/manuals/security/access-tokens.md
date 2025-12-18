---
title: 个人访问令牌
linkTitle: 个人访问令牌
description: 创建和管理个人 Docker 访问令牌，实现安全的 CLI 身份验证和自动化
keywords: 个人访问令牌, PAT, docker cli 身份验证, docker hub 安全, 程序化访问
weight: 10
aliases:
 - /docker-hub/access-tokens/
 - /security/for-developers/access-tokens/
---

个人访问令牌 (PAT) 为 Docker CLI 身份验证提供了比密码更安全的替代方案。使用 PAT 对自动化系统、CI/CD 流水线和开发工具进行身份验证，而无需暴露您的 Docker Hub 密码。

## 主要优势

PAT 相比密码身份验证具有显著的安全优势：

- 增强安全性：调查令牌使用情况，禁用可疑令牌，并防止可能危及您账户的管理操作（当您的系统被攻破时）。
- 更好的自动化：为不同的集成颁发多个令牌，每个令牌具有特定权限，并在不再需要时独立撤销它们。
- 双因素身份验证兼容性：当您启用了双因素身份验证时是必需的，提供安全的 CLI 访问，而不会绕过 2FA 保护。
- 使用情况跟踪：监控令牌的使用时间和方式，以识别潜在的安全问题或未使用的自动化。

## 谁应该使用个人访问令牌？

在以下常见场景中使用 PAT：

- 开发工作流：在本地开发期间对 Docker CLI 进行身份验证
- CI/CD 流水线：在持续集成系统中自动化镜像构建和部署
- 自动化脚本：在自动化部署或备份脚本中推送和拉取镜像
- 开发工具：将 Docker Hub 访问集成到 IDE、容器管理工具或监控系统中
- 双因素身份验证：启用 2FA 时，CLI 访问需要 PAT

> [!NOTE]
>
> 对于组织范围的自动化，请考虑使用[组织访问令牌](/manuals/enterprise/security/access-tokens.md)，它们不与单个用户账户绑定。

## 创建个人访问令牌

> [!IMPORTANT]
>
> 将访问令牌视为密码并保持其安全。将令牌存储在凭据管理器中，切勿将其提交到源代码仓库。

创建个人访问令牌的步骤：

1. 登录到 [Docker Home](https://app.docker.com/)。
1. 选择右上角的头像，从下拉菜单中选择 **Account settings**（账户设置）。
1. 选择 **Personal access tokens**（个人访问令牌）。
1. 选择 **Generate new token**（生成新令牌）。
1. 配置您的令牌：
   - **Description**（描述）：使用描述性名称表明令牌的用途
   - **Expiration date**（过期日期）：根据您的安全策略设置过期日期
   - **Access permissions**（访问权限）：**Read**（读取）、**Write**（写入）或 **Delete**（删除）。
1. 选择 **Generate**（生成）。复制屏幕上显示的令牌并保存。一旦退出屏幕，您将无法再次检索该令牌。

## 使用个人访问令牌

使用您的个人访问令牌登录 Docker CLI：

```console
$ docker login --username <YOUR_USERNAME>
Password: [在此粘贴您的 PAT]
```

当提示输入密码时，请输入您的个人访问令牌，而不是 Docker Hub 密码。

## 修改个人访问令牌

> [!NOTE]
>
> 您无法编辑现有个人访问令牌的过期日期。如果需要设置新的过期日期，必须创建新的 PAT。

您可以根据需要重命名、激活、停用或删除令牌。您可以在账户设置中管理您的令牌。

1. 登录到 [Docker Home](https://app.docker.com/login)。
1. 选择右上角的头像，从下拉菜单中选择 **Account settings**（账户设置）。
1. 选择 **Personal access tokens**（个人访问令牌）。
      - 此页面显示您所有令牌的概览，并列出令牌是手动生成的还是
   [自动生成](#auto-generated-tokens)（自动生成）的。您还可以查看令牌的作用域、哪些令牌处于激活和非激活状态、创建时间、最后使用时间及其过期日期。
1. 选择令牌行最右侧的操作菜单，然后选择 **Deactivate**（停用）或 **Activate**（激活）、**Edit**（编辑）或 **Delete**（删除）来修改令牌。
1. 编辑令牌后，选择 **Save token**（保存令牌）。

## 自动生成的令牌

Docker Desktop 在您登录时会自动创建身份验证令牌，具有以下特征：

- 自动创建：登录 Docker Desktop 时生成
- 完整权限：包含读取、写入和删除访问权限
- 基于会话：Docker Desktop 会话过期时自动删除
- 账户限制：每个账户最多 5 个自动生成的令牌
- 自动清理：创建新令牌时会删除旧令牌

如有需要，您可以手动删除自动生成的令牌，但当您使用 Docker Desktop 时，它们将被重新创建。

## 公平使用政策

使用个人访问令牌时，请注意过度创建令牌可能导致限流或额外收费。Docker 保留对过度使用 PAT 的账户实施限制的权利，以确保公平的资源分配并维护服务质量。

公平使用的最佳实践包括：

- 在相似的用例中重用令牌，而不是创建许多单一用途的令牌
- 定期删除未使用的令牌
- 对组织范围的自动化使用[组织访问令牌](/manuals/enterprise/security/access-tokens.md)
- 监控令牌使用情况以识别优化机会