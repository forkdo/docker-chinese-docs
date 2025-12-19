---
title: 注册表访问管理
description: 使用注册表访问管理控制对已批准容器注册表的访问，确保 Docker Desktop 安全使用
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

注册表访问管理 (RAM) 让管理员能够控制开发者可以通过 Docker Desktop 访问哪些容器注册表。这种 DNS 级别的过滤确保开发者只能从批准的注册表拉取和推送镜像，从而提高供应链安全性。

RAM 适用于所有注册表类型，包括云服务、本地注册表和注册表镜像。您可以允许任何主机名或域名，但必须在允许列表中包含重定向域名（例如某些注册表使用的 `s3.amazonaws.com`）。

## 支持的注册表

注册表访问管理适用于任何容器注册表，包括：

 - Docker Hub（默认允许）
- 云注册表：Amazon ECR、Google Container Registry、Azure Container Registry
- 基于 Git 的注册表：GitHub Container Registry、GitLab Container Registry
- 本地解决方案：Nexus、Artifactory、Harbor
- 注册表镜像：包括 Docker Hub 镜像

## 先决条件

在配置注册表访问管理之前，您必须：

- [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md) 以确保用户使用您的组织进行身份验证
- 使用[个人访问令牌 (PAT)](/manuals/security/access-tokens.md) 进行身份验证（不支持组织访问令牌）
- 拥有 Docker Business 订阅

> [!IMPORTANT]
>
> 注册表访问管理仅在用户使用组织凭据登录 Docker Desktop 时生效。

## 配置注册表权限

要配置注册表权限：

1. 登录 [Docker Home](https://app.docker.com)，从左上角帐户下拉菜单中选择您的组织。
1. 选择 **Admin Console**，然后选择 **Registry access**。
1. 使用**切换开关**启用注册表访问。默认情况下，Docker Hub 在注册表列表中已启用。
1. 要添加其他注册表，选择 **Add registry** 并提供**注册表地址**和**注册表昵称**。
1. 选择 **Create**。最多可以添加 100 个注册表。
1. 确认您的注册表出现在注册表列表中，然后选择 **Save changes**。

更改最多需要 24 小时才能生效。要更快应用更改，请让开发者注销并重新登录 Docker Desktop。

> [!IMPORTANT]
>
> 从 Docker Desktop 4.36 开始，如果开发者属于具有不同 RAM 策略的多个组织，则仅强制执行配置文件中第一个组织的策略。

> [!TIP]
>
> RAM 限制也适用于通过 URL 获取内容的 Dockerfile `ADD` 指令。当使用带有 URL 的 `ADD` 时，请将受信任的注册表域名包含在您的允许列表中。
><br><br>
> RAM 专为容器注册表设计，不适用于通用 URL（如软件包镜像或存储服务）。添加过多域名可能导致错误或达到系统限制。

## 验证限制是否生效

用户使用其组织凭据登录 Docker Desktop 后，注册表访问管理会立即生效。

当用户尝试从受阻止的注册表拉取时：

```console
$ docker pull blocked-registry.com/image:tag
Error response from daemon: registry access to blocked-registry.com is not allowed
```

允许的注册表访问正常工作：

```console
$ docker pull allowed-registry.com/image:tag
# Pull succeeds
```

注册表限制适用于所有 Docker 操作，包括拉取、推送和引用外部注册表的构建。

## 注册表限制和平台约束

注册表访问管理具有以下限制和特定于平台的行为：

- 最大允许列表大小：每个组织 100 个注册表或域名
- 基于 DNS 的过滤：限制在主机名级别工作，而非 IP 地址
- 需要重定向域名：必须包含注册表重定向到的所有域名（CDN 端点、存储服务）
- Windows 容器：默认情况下，Windows 镜像操作不受限制。在 Docker Desktop 设置中打开 **Use proxy for Windows Docker daemon** 以应用限制
- WSL 2 要求：需要 Linux 内核 5.4 或更高版本，限制适用于所有 WSL 2 发行版

## 构建和部署限制

以下场景不受注册表访问管理限制：

- 使用 Kubernetes 驱动程序的 Docker buildx
- 使用自定义 docker-container 驱动程序的 Docker buildx
- 某些 Docker Debug 和 Kubernetes 镜像拉取（即使 Docker Hub 被阻止）
- 如果源注册表受到限制，先前由注册表镜像缓存的镜像可能仍被阻止

## 安全绕过注意事项

用户可能通过以下方式绕过注册表访问管理：

- 本地代理或 DNS 操作
- 注销 Docker Desktop（除非强制登录）
- Docker Desktop 控制范围之外的网络级别修改

为了最大限度地提高安全性效果：

- [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md) 以防止通过注销绕过
- 实施额外的网络级别控制以实现全面保护
- 将注册表访问管理作为更广泛安全策略的一部分

## 注册表允许列表最佳实践

- 包含所有注册表域名：某些注册表会重定向到多个域名。对于 AWS ECR，请包含：

    ```text
    your-account.dkr.ecr.us-west-2.amazonaws.com
    amazonaws.com
    s3.amazonaws.com
    ```

- 定期维护允许列表：
    - 定期删除未使用的注册表
    - 根据需要添加新批准的注册表
    - 更新可能已更改的域名
    - 通过 Docker Desktop 分析监控注册表使用情况
- 测试配置更改：
    - 更新允许列表后验证注册表访问
    - 检查是否包含所有必要的重定向域名
    - 确保开发工作流程不会中断
    - 与[增强容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)结合使用以实现全面保护