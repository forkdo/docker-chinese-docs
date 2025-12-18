---
title: Desktop 设置报告
linkTitle: Desktop 设置报告
description: 使用报告仪表板跟踪和监控用户对 Docker Desktop 设置策略的合规性
keywords: settings management, compliance reporting, admin console, policy enforcement, docker desktop
weight: 30
aliases:
 - /security/for-admins/hardened-desktop/settings-management/compliance-reporting/
---

{{< summary-bar feature_name="Compliance reporting" >}}

Desktop 设置报告用于跟踪用户对 Docker Desktop 设置策略的合规性。使用此功能可以监控组织内策略的应用情况，并识别需要协助以实现合规性的用户。

## 前提条件

在使用 Docker Desktop 设置报告之前，请确保您已具备以下条件：

- 在组织中安装了 [Docker Desktop 4.37.1 或更高版本](/manuals/desktop/release-notes.md)
- [已验证的域名](/manuals/enterprise/security/single-sign-on/configure.md#step-one-add-and-verify-your-domain)
- 为组织 [强制执行登录](/manuals/enterprise/security/enforce-sign-in/_index.md)
- Docker Business 订阅
- 至少配置了一个设置策略

> [!WARNING]
>
> 使用早于 4.40 版本的 Docker Desktop 的用户可能显示为不合规，因为旧版本无法报告合规状态。为获得准确的报告，请将用户更新至 Docker Desktop 4.40 或更高版本。

## 访问报告仪表板

要查看合规性报告：

1. 登录到 [Docker Home](https://app.docker.com) 并选择您的组织。
1. 选择 **Admin Console**，然后选择 **Desktop settings reporting**。

报告仪表板提供以下工具：

- 搜索字段，可通过用户名或电子邮件地址查找用户
- 筛选选项，显示分配到特定策略的用户
- 切换开关，隐藏或显示合规用户
- 合规状态指示器
- CSV 导出选项，用于下载合规数据

## 用户合规状态

Docker Desktop 评估三种类型的状态以确定整体合规性：

### 合规状态

这是仪表板中显示的主要状态：

| 合规状态 | 含义 |
|-------------------|---------------|
| 合规 | 用户获取并应用了最新的分配策略。 |
| 不合规 | 用户获取了正确的策略，但尚未应用。 |
| 过时 | 用户获取了策略的旧版本。 |
| 未分配策略 | 用户未分配到任何策略。 |
| 未受控域名 | 用户的电子邮件域名未验证。 |

### 域名状态

显示用户的电子邮件域名与您组织的关系：

| 域名状态 | 含义 |
|---------------|---------------|
| 已验证 | 用户的电子邮件域名已验证。 |
| 访客用户 | 用户的电子邮件域名未验证。 |
| 无域名 | 您的组织没有已验证的域名，且用户的域名未知。 |

### 设置状态

指示用户的策略分配：

| 设置状态 | 含义 |
|-----------------|---------------|
| 全局策略 | 用户分配到您组织的默认策略。 |
| 用户策略 | 用户分配到特定的自定义策略。 |
| 未分配策略 | 用户未分配到任何策略。 |

## 监控合规性

在 **Desktop settings reporting** 仪表板中，您可以：

- 快速查看组织范围的合规性
- 开启 **隐藏合规用户** 以专注于问题
- 按特定策略筛选以检查目标合规性
- 导出合规数据
- 选择任何用户的姓名以查看详细状态和解决步骤

选择用户姓名后，您将看到其详细的合规信息，包括当前状态、域名验证、分配的策略、上次策略获取时间和 Docker Desktop 版本。

## 解决合规问题

您可以在仪表板中选择不合规用户的姓名，以获取推荐的状态解决步骤。以下部分是针对不合规状态的一般解决步骤：

### 不合规或过时用户

- 要求用户完全退出并重新启动 Docker Desktop
- 验证用户已登录 Docker Desktop
- 确认用户使用的是 Docker Desktop 4.40 或更高版本

### 未受控域名用户

- 在组织设置中验证用户的电子邮件域名
- 如果域名应受控，请添加并验证它，然后等待验证
- 如果用户是访客且不应受控，则无需采取行动

### 未分配策略用户

- 将用户分配到现有策略
- 为他们创建新的用户特定策略
- 验证他们包含在组织的默认策略范围内

用户采取纠正措施后，刷新报告仪表板以验证状态变化。

## 策略更新时间

Docker Desktop 检查策略更新的频率：

- 启动时
- Docker Desktop 运行时每 60 分钟
- 用户重启 Docker Desktop 时

在 Admin Console 中对策略的更改立即生效，但用户必须重启 Docker Desktop 以应用更改。