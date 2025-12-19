---
title: 使用 Admin Console 配置设置管理
linkTitle: 使用 Admin Console
description: 使用 Docker Admin Console 在整个组织内配置和强制执行 Docker Desktop 设置
keywords: admin console, settings management, policy configuration, enterprise controls, docker desktop
weight: 20
aliases:
 - /security/for-admins/hardened-desktop/settings-management/configure-admin-console/
---

{{< summary-bar feature_name="Admin Console" >}}

使用 Docker Admin Console 为整个组织的 Docker Desktop 创建和管理设置策略。设置策略可让您标准化配置、强制执行安全要求并保持一致的 Docker Desktop 环境。

## 先决条件

在开始之前，请确保您已具备：

- 已安装 [Docker Desktop 4.37.1 或更高版本](/manuals/desktop/release-notes.md)
- [已验证的域名](/manuals/enterprise/security/single-sign-on/configure.md#step-one-add-and-verify-your-domain)
- 为您的组织[强制执行登录](/manuals/enterprise/security/enforce-sign-in/_index.md)
- Docker Business 订阅

> [!IMPORTANT]
>
> 您必须将用户添加到已验证的域名，设置才能生效。

## 创建设置策略

要创建新的设置策略：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Admin Console**，然后选择 **Desktop Settings Management**。
3. 选择 **Create a settings policy**。
4. 提供名称和可选描述。

      > [!TIP]
      >
      > 您可以上传现有的 `admin-settings.json` 文件来预填充表单。
      Admin Console 策略会覆盖本地的 `admin-settings.json` 文件。

5. 选择策略适用对象：
   - 所有用户
   - 特定用户

      > [!NOTE]
      >
      > 针对特定用户的策略会覆盖全局默认策略。在全组织范围应用策略之前，请先用小范围群体测试您的策略。

6. 使用以下状态配置每个设置：
   - **User-defined**：用户可以更改该设置。
   - **Always enabled**：设置开启并锁定。
   - **Enabled**：设置开启但可以更改。
   - **Always disabled**：设置关闭并锁定。
   - **Disabled**：设置关闭但可以更改。

      > [!TIP]
      >
      > 有关可配置设置、支持平台和配置方法的完整列表，请参阅[设置参考](settings-reference.md)。

7. 选择 **Create** 以保存您的策略。

## 应用策略

设置策略在 Docker Desktop 重启且用户重新登录后生效。

对于新安装：

1. 启动 Docker Desktop。
2. 使用您的 Docker 账户登录。

对于现有安装：

1. 完全退出 Docker Desktop。
2. 重新启动 Docker Desktop。

> [!IMPORTANT]
>
> 用户必须完全退出并重新打开 Docker Desktop。从 Docker Desktop 菜单中重启是不够的。

Docker Desktop 在启动时以及运行期间每 60 分钟检查一次策略更新。

## 验证应用的设置

应用策略后：

- Docker Desktop 将大多数设置显示为灰色（不可更改）
- 某些设置，特别是增强型容器隔离配置，可能不会出现在 GUI 中
- 您可以通过检查系统上的 [`settings-store.json` 文件](/manuals/desktop/settings-and-maintenance/settings.md) 来验证所有应用的设置

## 管理现有策略

在 Admin Console 的 **Desktop Settings Management** 页面中，使用 **Actions** 菜单可以：

- 编辑或删除现有的设置策略
- 将设置策略导出为 `admin-settings.json` 文件
- 将特定用户策略提升为新的全局默认策略

## 回滚策略

要回滚设置策略：

- 完全回滚：删除整个策略。
- 部分回滚：将特定设置设置为 **User-defined**。

当您回滚设置时，用户将重新获得对这些设置配置的控制权。