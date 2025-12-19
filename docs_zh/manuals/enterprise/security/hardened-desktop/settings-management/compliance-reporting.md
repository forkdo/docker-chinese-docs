---
title: 桌面设置合规性报告
linkTitle: 桌面设置合规性报告
description: 使用合规性报告仪表板跟踪和监控用户对 Docker Desktop 设置策略的合规性
keywords: settings management, compliance reporting, admin console, policy enforcement, docker desktop
weight: 30
aliases:
 - /security/for-admins/hardened-desktop/settings-management/compliance-reporting/
---

{{< summary-bar feature_name="Compliance reporting" >}}

桌面设置合规性报告功能可跟踪用户对 Docker Desktop 设置策略的合规性。使用此功能监控整个组织的策略应用情况，并识别需要合规性协助的用户。

## 先决条件

在使用 Docker Desktop 设置合规性报告之前，请确保满足以下条件：

- 已在整个组织中安装 [Docker Desktop 4.37.1 或更高版本](/manuals/desktop/release-notes.md)
- [已验证的域名](/manuals/enterprise/security/single-sign-on/configure.md#step-one-add-and-verify-your-domain)
- 为您的组织[强制启用登录](/manuals/enterprise/security/enforce-sign-in/_index.md)
- Docker Business 订阅
- 至少配置了一个设置策略

> [!WARNING]
>
> 使用 Docker Desktop 4.40 以下版本的用户可能会显示为不合规，因为旧版本无法报告合规状态。为了获得准确的报告，请将用户更新至 Docker Desktop 4.40 或更高版本。

## 访问合规性报告仪表板

要查看合规性报告：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。
2. 选择 **Admin Console**（管理控制台），然后选择 **Desktop settings reporting**（桌面设置合规性报告）。

合规性报告仪表板提供以下工具：

- 搜索字段，可按用户名或电子邮件地址查找用户
- 筛选选项，可显示分配给特定策略的用户
- 切换选项，可隐藏或取消隐藏合规用户
- 合规状态指示器
- CSV 导出选项，可下载合规性数据

## 用户合规状态

Docker Desktop 评估三种类型的状态以确定整体合规性：

### 合规状态

这是仪表板中显示的主要状态：

| 合规状态 | 含义 |
|-------------------|---------------|
| 合规 | 用户已获取并应用最新分配的策略。 |
| 不合规 | 用户已获取正确的策略，但尚未应用。 |
| 过期 | 用户获取的是策略的早期版本。 |
| 未分配策略 | 用户未分配任何策略。 |
| 未受控域 | 用户的电子邮件域未经验证。 |

### 域状态

显示用户的电子邮件域与组织的关系：

| 域状态 | 含义 |
|---------------|---------------|
| 已验证 | 用户的电子邮件域已验证。 |
| 访客用户 | 用户的电子邮件域未验证。 |
| 无域 | 您的组织没有已验证的域，且用户的域未知。 |

### 设置状态

指示用户的策略分配情况：

| 设置状态 | 含义 |
|-----------------|---------------|
| 全局策略 | 用户已分配组织的默认策略。 |
| 用户策略 | 用户已分配特定的自定义策略。 |
| 未分配策略 | 用户未分配任何策略。 |

## 监控合规性

通过 **Desktop settings reporting**（桌面设置合规性报告）仪表板，您可以：

- 一目了然地查看整个组织的合规性
- 打开 **Hide compliant users**（隐藏合规用户）以专注于问题
- 按特定策略筛选以检查目标合规性
- 导出合规性数据
- 选择任何用户的名称以查看详细状态和解决步骤

选择用户名称后，您将看到其详细的合规信息，包括当前状态、域验证、分配的策略、上次获取策略的时间和 Docker Desktop 版本。

## 解决合规性问题

您可以在仪表板中选择不合规用户的名称，以获取推荐的状态解决步骤。以下部分针对不合规状态提供一般解决步骤：

### 不合规或过期的用户

- 要求用户完全退出并重新启动 Docker Desktop
- 验证用户是否已登录 Docker Desktop
- 确认用户使用的是 Docker Desktop 4.40 或更高版本

### 未受控域用户

- 在组织设置中验证用户的电子邮件域
- 如果该域应受控，请添加并验证它，然后等待验证完成
- 如果用户是访客且不应受控，则无需执行任何操作

### 未分配策略的用户

- 将用户分配给现有策略
- 为其创建新的用户特定策略
- 验证他们是否包含在组织的默认策略范围内

用户采取纠正措施后，请刷新合规性报告仪表板以验证状态变化。

## 策略更新时间

Docker Desktop 检查策略更新的时机：

- 启动时
- Docker Desktop 运行期间每 60 分钟
- 用户重新启动 Docker Desktop 时

管理控制台中对策略的更改会立即生效，但用户必须重新启动 Docker Desktop 才能应用这些更改。