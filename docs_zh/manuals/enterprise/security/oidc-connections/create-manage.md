---
title: 创建和管理 OIDC 连接
linkTitle: 创建和管理连接
description: 为您的组织创建、更新和删除 OIDC 连接
keywords: oidc connections, create oidc connection, github actions, docker/oidc-action, openid connect, enterprise security, admin
tags: [admin]
weight: 10
---

{{< summary-bar feature_name="OIDC connections" >}}

组织所有者和编辑者可以在 Docker Home 的 **OIDC 连接** 中创建 OIDC 连接或管理现有连接。建立 OIDC 连接分为两个阶段。首先，您在 Docker Home 中创建 OIDC 连接，然后配置您的 GitHub Actions 工作流 YAML 文件。

> [!NOTE]
> OIDC 连接仅支持 GitHub 作为受信任的第三方。

## 设置 GitHub Actions 身份验证

### 第 1 步：创建 OIDC 连接

1. 登录 [Docker Home](https://app.docker.com/)，选择您的组织，然后进入 **Identity & auth**。
1. 选择 **OIDC connections**。
1. 选择 **Create OIDC connection** 并填写 OIDC 连接表单。
   - 您必须提供规则集（rulesets）和主题声明（subject claims）。其他值为可选。
   - 有关规则集、主题声明和资源，请参阅 [OIDC 连接规则集和主题声明](/manuals/enterprise/security/oidc-connections/rulesets-claims.md)。
1. 选择 **Create connection**。
1. 复制您的 OIDC 连接 ID。

### 第 2 步：定义 GitHub Actions 工作流

1. 添加一个顶级的 `permissions` 键以请求 GitHub OIDC ID 令牌：

   ```yaml
   permissions:
     id-token: write
   ```

1. 定义一个触发 OIDC 交换的作业。将 `connection_id` 更新为您从 Docker 复制的连接 ID：

   ```yaml
   jobs:
     login:
       runs-on: ubuntu-latest
       steps:
         - name: OIDC connections
           id: docker_oidc
           uses: docker/oidc-action@v1
           with:
             connection_id: <YOUR_CONNECTION_ID>
   ```

1. 添加一个步骤，一旦 ID 令牌通过验证，就使用访问令牌登录 Docker：

   ```yaml
   - name: Sign in to Docker Hub
     uses: docker/login-action@{{% param "login_action_version" %}}
     with:
       username: <DOCKER_ORGANIZATION_NAME>
       password: ${{ steps.docker_oidc.outputs.token }}
   ```

   `username` 的值必须是组织名称。不支持个人账户。

   更新后的工作流 YAML 应如下所示：

   ```yaml
   permissions:
     id-token: write

   jobs:
     login:
       runs-on: ubuntu-latest
       steps:
         - name: OIDC connections
           id: docker_oidc
           uses: docker/oidc-action@v1
           with:
             connection_id: <YOUR_CONNECTION_ID>

         - name: Sign in to Docker Hub
           uses: docker/login-action@{{% param "login_action_version" %}}
           with:
             username: <YOUR_ORGANIZATION_NAME>
             password: ${{ steps.docker_oidc.outputs.token }}
   ```

1. 运行您的 GitHub Action 并验证工作流可以登录 Docker。

## 管理 OIDC 连接

您可以从 **OIDC connections** 页面查看、编辑、停用或删除连接。

1. 从 **Identity & auth** 进入 **OIDC connections**。
1. 在 **OIDC connections** 页面，找到目标连接 ID 所在的行。
1. 选择操作菜单图标以获取选项。
   - **Edit** 打开 **Edit OIDC connection** 页面，您可以在其中复制连接 ID、更新规则集或查看 **Failures** 表。
   - **Deactivate** 临时禁用对您 GitHub 工作流的访问。
   - **Activate** 恢复对您 GitHub 工作流的访问。
   - **Delete** 永久删除一个连接。

## 停用和删除

您可以停用 OIDC 连接，以在不删除连接的情况下暂停 GitHub 工作流对您 Docker 资源的访问。当连接处于停用状态时：

- 它无法签发 Docker 访问令牌。
- 没有 Docker 访问令牌，`docker/oidc-action` 会在令牌交换步骤失败，直到您激活该连接。

与停用不同，删除 OIDC 连接是永久性的。任何其 `docker/oidc-action` 步骤仍引用已删除 `connection_id` 的工作流都会在令牌交换步骤失败。在受影响的每个工作流再次运行之前，使用该替换连接的 ID 更新该输入。

## 后续步骤

- [OIDC 连接规则集和主题声明](/manuals/enterprise/security/oidc-connections/rulesets-claims.md)
