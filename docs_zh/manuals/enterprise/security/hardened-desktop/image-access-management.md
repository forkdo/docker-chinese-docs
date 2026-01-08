---
title: 镜像访问管理
description: 通过镜像访问管理控制开发者可以访问哪些 Docker Hub 镜像，以增强供应链安全
keywords: 镜像访问管理, docker official images, verified publisher, 供应链安全, docker business
tags:
- admin
aliases:
- /docker-hub/image-access-management/
- /desktop/hardened-desktop/image-access-management/
- /admin/organization/image-access/
- /security/for-admins/image-access-management/
- /security/for-admins/hardened-desktop/image-access-management/
weight: 40
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

镜像访问管理允许管理员控制开发者可以从 Docker Hub 拉取哪些类型的镜像。这可以防止开发者意外使用不可信的社区镜像，从而给您的组织带来安全风险。

通过镜像访问管理，您可以限制访问以下类型的镜像：

- Docker Official Images：由 Docker 维护的精选镜像
- Docker Verified Publisher Images：来自可信商业发布者的镜像
- Organization images：您组织的私有仓库
- Community images：来自个人开发者的公共镜像

## 谁应该使用镜像访问管理？

镜像访问管理通过确保开发者仅使用可信的容器镜像来帮助防止供应链攻击。例如，开发者在构建新应用程序时，可能会意外地将恶意社区镜像用作组件。镜像访问管理通过限制仅允许使用已批准的镜像类型来防止这种情况发生。

常见的安全场景包括：

- 防止使用无人维护或恶意的社区镜像
- 确保开发者仅使用经过审查的官方基础镜像
- 控制对商业第三方镜像的访问
- 在开发团队间保持一致的安全标准

## 前提条件

在配置镜像访问管理之前，您必须：

- [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)以确保用户使用您的组织身份进行身份验证
- 使用[个人访问令牌 (PATs)](/manuals/security/access-tokens.md)进行身份验证（不支持组织访问令牌）
- 拥有 Docker Business 订阅

> [!IMPORTANT]
>
> 镜像访问管理仅在用户使用组织凭据登录 Docker Desktop 时生效。

## 配置镜像访问

要配置镜像访问管理：

1. 登录 [Docker Home](https://app.docker.com) 并从左上角的账户下拉菜单中选择您的组织。
1. 选择 **Admin Console**，然后选择 **Image access**。
1. 使用**切换开关**来启用镜像访问。
1. 选择允许的镜像类型：
    - **Organization images**：来自您组织的镜像（默认始终允许）。这些可以是由您组织内成员创建的公共或私有镜像。
    - **Community images**：由各种用户贡献的、可能存在安全风险的镜像。此类别包括 Docker 赞助的开源镜像，默认处于关闭状态。
    - **Docker Verified Publisher Images**：来自 Verified Publisher 计划中 Docker 合作伙伴的镜像，具备安全供应链资质。
    - **Docker Official Images**：精选的 Docker 仓库，提供操作系统仓库、Dockerfile 最佳实践、即用型解决方案以及及时的安全更新。

一旦应用限制，组织成员可以以只读格式查看权限页面。

> [!NOTE]
>
> 镜像访问管理默认关闭。组织所有者无论策略设置如何，都有权访问所有镜像。

## 验证访问限制

配置镜像访问管理后，请测试限制是否正常工作。

当开发者拉取允许的镜像类型时：

```console
$ docker pull nginx  # Docker Official Image
# 如果允许使用 Docker Official Images，则拉取成功
```

当开发者拉取被阻止的镜像类型时：

```console
$ docker pull someuser/custom-image  # Community image
Error response from daemon: image access denied: community images not allowed
```

镜像访问限制适用于所有 Docker Hub 操作，包括拉取、使用 `FROM` 指令的构建以及 Docker Compose 服务。

## 安全实施

从最严格的策略开始，然后根据合法的业务需求逐步放宽：

1. 从以下开始：Docker Official Images 和 Organization images
2. 根据需要添加：Docker Verified Publisher Images 用于商业工具
3. 谨慎评估：Community images 仅用于特定的、经过审查的用例

其他安全建议包括：

- 监控使用模式：审查开发者尝试拉取的镜像，识别对其他镜像类型的合法请求，定期审计已批准的镜像类别以确保其持续适用，并使用 Docker Desktop 分析来监控使用模式。
- 分层安全控制：镜像访问管理与注册表访问管理结合使用效果最佳，前者控制开发者可以访问哪些注册表，后者在运行时保护容器安全，而设置管理则用于控制 Docker Desktop 配置。

## 范围和绕过注意事项

- 镜像访问管理仅控制对 Docker Hub 镜像的访问。来自其他注册表的镜像不受这些策略的影响。请使用[注册表访问管理](/manuals/enterprise/security/hardened-desktop/registry-access-management.md)来控制对其他注册表的访问。
- 用户可能通过以下方式绕过镜像访问管理：退出 Docker Desktop 登录（如果未强制登录）、使用不受限制的其他注册表中的镜像，或使用注册表镜像或代理。请强制登录并结合注册表访问管理以实现全面控制。
- 镜像限制适用于 Dockerfile `FROM` 指令，使用受限镜像的 Docker Compose 服务将无法启动，如果中间镜像受限，多阶段构建可能会受到影响，使用多种镜像类型的 CI/CD 流水线也可能受到影响。