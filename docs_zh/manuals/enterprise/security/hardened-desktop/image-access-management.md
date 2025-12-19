---
title: 镜像访问管理
description: 使用镜像访问管理控制开发者可访问的 Docker Hub 镜像，以增强供应链安全
keywords: 镜像访问管理, Docker 官方镜像, 验证发布者, 供应链安全, Docker Business
tags: [admin]
aliases:
 - /docker-hub/image-access-management/
 - /desktop/hardened-desktop/image-access-management/
 - /admin/organization/image-access/
 - /security/for-admins/image-access-management/
 - /security/for-admins/hardened-desktop/image-access-management/
weight: 40
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

镜像访问管理让管理员能够控制开发者可以从 Docker Hub 拉取哪些类型的镜像。这可以防止开发者意外使用不受信任的社区镜像，这些镜像可能给您的组织带来安全风险。

通过镜像访问管理，您可以限制对以下内容的访问：

- **Docker 官方镜像**：由 Docker 维护的精选镜像
- **Docker 验证发布者镜像**：来自受信任商业发布者的镜像
- **组织镜像**：您组织的私有仓库
- **社区镜像**：来自个人开发者的公共镜像

## 谁应该使用镜像访问管理？

镜像访问管理通过确保开发者仅使用受信任的容器镜像，帮助防止供应链攻击。例如，构建新应用程序的开发者可能会意外使用恶意社区镜像作为组件。镜像访问管理通过限制仅访问批准的镜像类型来防止这种情况。

常见的安全场景包括：

- 防止使用无人维护或恶意的社区镜像
- 确保开发者仅使用经过审查的官方基础镜像
- 控制对商业第三方镜像的访问
- 在开发团队中保持一致的安全标准

## 先决条件

在配置镜像访问管理之前，您必须：

- [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)以确保用户使用您的组织进行身份验证
- 使用[个人访问令牌 (PAT)](/manuals/security/access-tokens.md) 进行身份验证（不支持组织访问令牌）
- 拥有 Docker Business 订阅

> [!IMPORTANT]
>
> 仅当用户使用组织凭据登录 Docker Desktop 时，镜像访问管理才会生效。

## 配置镜像访问

要配置镜像访问管理：

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角帐户下拉菜单中选择您的组织。
2. 选择 **Admin Console**，然后选择 **Image access**。
3. 使用**切换开关**启用镜像访问。
4. 选择要允许的镜像类型：
    - **组织镜像**：来自您组织的镜像（默认始终允许）。这些可以是组织内成员创建的公共或私有镜像。
    - **社区镜像**：由不同用户贡献的镜像，可能构成安全风险。此类别包括 Docker 赞助的开源镜像，默认关闭。
    - **Docker 验证发布者镜像**：来自 Docker 验证发布者计划中合作伙伴的镜像，符合安全供应链要求。
    - **Docker 官方镜像**：精选的 Docker 仓库，提供 OS 仓库、Dockerfile 最佳实践、即插即用解决方案和及时的安全更新。

应用限制后，组织成员可以以只读格式查看权限页面。

> [!NOTE]
>
> 镜像访问管理默认关闭。无论策略设置如何，组织所有者都可以访问所有镜像。

## 验证访问限制

配置镜像访问管理后，测试限制是否正常工作。

当开发者拉取允许的镜像类型时：

```console
$ docker pull nginx  # Docker 官方镜像
# 如果允许 Docker 官方镜像，拉取成功
```

当开发者拉取被阻止的镜像类型时：

```console
$ docker pull someuser/custom-image  # 社区镜像
Error response from daemon: image access denied: community images not allowed
```

镜像访问限制适用于所有 Docker Hub 操作，包括拉取、使用 `FROM` 指令的构建以及 Docker Compose 服务。

## 安全实施

从限制性最强的策略开始，并根据合法的业务需求逐步扩展：

1. 从以下开始：Docker 官方镜像和组织镜像
2. 如果需要，添加：Docker 验证发布者镜像用于商业工具
3. 仔细评估：社区镜像仅用于特定、经过审查的用例

其他安全建议包括：

- **监控使用模式**：审查开发者尝试拉取的镜像，识别对其他镜像类型的合法请求，定期审核批准的镜像类别以确保持续相关性，并使用 Docker Desktop 分析来监控使用模式。
- **分层安全控制**：镜像访问管理与以下功能配合使用效果最佳：
    - [Registry Access Management](/manuals/enterprise/security/hardened-desktop/registry-access-management.md) 控制开发者可以访问哪些仓库
    - [Enhanced Container Isolation](/manuals/desktop/hardened-desktop/enhanced-container-isolation.md) 在运行时保护容器安全
    - [Settings Management](/manuals/desktop/hardened-desktop/settings-management.md) 控制 Docker Desktop 配置

## 范围和绕过注意事项

- 镜像访问管理仅控制对 Docker Hub 镜像的访问。来自其他仓库的镜像不受这些策略的影响。使用 [Registry Access Management](/manuals/enterprise/security/hardened-desktop/registry-access-management.md) 来控制对其他仓库的访问。
- 用户可能通过以下方式绕过镜像访问管理：退出 Docker Desktop（除非强制登录）、使用来自其他未受限制仓库的镜像，或使用仓库镜像或代理。强制登录并结合 Registry Access Management 以实现全面控制。
- 镜像限制适用于 Dockerfile `FROM` 指令，使用受限镜像的 Docker Compose 服务将失败，如果中间镜像受限，多阶段构建可能会受到影响，使用多样化镜像类型的 CI/CD 管道可能会受到影响。