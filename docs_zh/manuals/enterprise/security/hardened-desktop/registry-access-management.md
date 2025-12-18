---
title: Registry Access Management
description: 使用 Registry Access Management 控制对已批准容器注册表的访问，确保 Docker Desktop 安全使用
keywords: registry access management, container registry, security controls, docker business, admin controls
tags: [admin]
aliases:
 - /desktop/hardened-desktop/registry-access-management/
 - /admin/organization/registry-access/
 - /docker-hub/registry-access-management/
 - /security/for-admins/registry-access-management/
 - /security/for-admins/hardened-desktop/registry-access-management/
weight: 30
---

{{< summary-bar feature_name="Registry access management" >}}

Registry Access Management (RAM) 允许管理员控制开发者通过 Docker Desktop 可以访问哪些容器注册表。这种基于 DNS 的过滤机制确保开发者只能从已批准的注册表拉取和推送镜像，从而提升供应链安全性。

RAM 支持所有类型的注册表，包括云服务、本地注册表和注册表镜像。您可以允许任何主机名或域名，但必须在允许列表中包含重定向域名（例如某些注册表使用的 `s3.amazonaws.com`）。

## 支持的注册表

Registry Access Management 支持任何容器注册表，包括：

 - Docker Hub（默认允许）
- 云注册表：Amazon ECR、Google Container Registry、Azure Container Registry
- 基于 Git 的注册表：GitHub Container Registry、GitLab Container Registry
- 本地解决方案：Nexus、Artifactory、Harbor
- 注册表镜像：包括 Docker Hub 镜像

## 前置条件

配置 Registry Access Management 之前，您必须：

- [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md) 以确保用户使用组织凭据进行身份验证
- 使用 [个人访问令牌 (PATs)](/manuals/security/access-tokens.md) 进行身份验证（不支持组织访问令牌）
- 拥有 Docker Business 订阅

> [!IMPORTANT]
>
> Registry Access Management 仅在用户使用组织凭据登录 Docker Desktop 时生效。

## 配置注册表权限

要配置注册表权限：

1. 登录到 [Docker Home](https://app.docker.com) 并从左上角的账户下拉菜单中选择您的组织。
1. 选择 **Admin Console**，然后选择 **Registry access**。
1. 使用 **toggle** 启用注册表访问。默认情况下，Docker Hub 已在注册表列表中启用。
1. 要添加其他注册表，选择 **Add registry** 并提供 **Registry address** 和 **Registry nickname**。
1. 选择 **Create**。您可以添加最多 100 个注册表。
1. 验证您的注册表出现在注册表列表中，然后选择 **Save changes**。

更改可能需要最多 24 小时才能生效。要更快应用更改，请让开发者从 Docker Desktop 登出并重新登录。

> [!IMPORTANT]
>
> 从 Docker Desktop 4.36 开始，如果开发者属于多个具有不同 RAM 策略的组织，则仅执行配置文件中第一个组织的策略。

> [!TIP]
>
> RAM 限制也适用于 Dockerfile 中通过 URL 获取内容的 `ADD` 指令。在使用带 URL 的 `ADD` 时，请在允许列表中包含受信任的注册表域名。
><br><br>
> RAM 专为容器注册表设计，不适用于一般用途的 URL（如包镜像或存储服务）。添加过多域名可能导致错误或达到系统限制。

## 验证限制是否生效

用户使用组织凭据登录 Docker Desktop 后，Registry Access Management 立即生效。

当用户尝试从被阻止的注册表拉取时：

```console
$ docker pull blocked-registry.com/image:tag
Error response from daemon: registry access to blocked-registry.com is not allowed
```

允许的注册表访问正常工作：

```console
$ docker pull allowed-registry.com/image:tag
# 拉取成功
```

注册表限制适用于所有 Docker 操作，包括拉取、推送和引用外部注册表的构建。

## 注册表限制和平台约束

Registry Access Management 具有以下限制和特定平台行为：

- 允许列表最大大小：每个组织最多 100 个注册表或域名
- 基于 DNS 的过滤：限制在主机名级别工作，而非 IP 地址
- 需要重定向域名：必须包含注册表重定向到的所有域名（CDN 端点、存储服务）
- Windows 容器：默认情况下，Windows 镜像操作不受限制。在 Docker Desktop 设置中启用 **Use proxy for Windows Docker daemon** 以应用限制
- WSL 2 要求：需要 Linux 内核 5.4 或更高版本，限制适用于所有 WSL 2 发行版

## 构建和部署限制

以下场景不受 Registry Access Management 限制：

- 使用 Kubernetes 驱动的 Docker buildx
- 使用自定义 docker-container 驱动的 Docker buildx
- 某些 Docker Debug 和 Kubernetes 镜像拉取（即使 Docker Hub 被阻止）
- 之前被注册表镜像缓存的镜像，如果源注册表受限，仍可能被阻止

## 安全绕过注意事项

用户可能通过以下方式绕过 Registry Access Management：

- 本地代理或 DNS 操纵
- 从 Docker Desktop 登出（除非强制登录）
- Docker Desktop 控制范围外的网络级修改

为最大化安全效果：

- [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md) 以防止通过登出绕过
- 实施额外的网络级控制以获得完整保护
- 将 Registry Access Management 作为更广泛安全策略的一部分使用

## 注册表允许列表最佳实践

- 包含所有注册表域名：某些注册表会重定向到多个域名。对于 AWS ECR，应包含：

    ```text
    your-account.dkr.ecr.us-west-2.amazonaws.com
    amazonaws.com
    s3.amazonaws.com
    ```

- 定期维护允许列表：
    - 定期移除未使用的注册表
    - 根据需要添加新批准的注册表
    - 更新可能已更改的域名
    - 通过 Docker Desktop 分析监控注册表使用情况
- 测试配置更改：
    - 在更新允许列表后验证注册表访问
    - 检查是否包含所有必要的重定向域名
    - 确保开发工作流程不受干扰
    - 与 [Enhanced Container Isolation](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md) 结合使用以获得全面保护