---
title: 部署你的 Docker 环境
description: 在你的公司内部署 Docker 环境。
weight: 40
---

> [!WARNING]
>
> 在执行以下操作前，请先与你的用户沟通，并确认你的 IT 和 MDM 团队已准备好处理任何意外问题，因为这些步骤将影响所有登录到你的 Docker 组织的现有用户。

## 强制执行 SSO

强制执行 SSO 意味着任何在 Docker 个人资料中使用与你已验证域名匹配的电子邮件地址的用户，都必须通过你的 SSO 连接登录。请确保与你的 SSO 连接关联的 Identity Provider 组涵盖所有你希望访问 Docker 订阅的开发者组。

有关如何强制执行 SSO 的说明，请参阅 [强制执行 SSO](/manuals/enterprise/security/single-sign-on/connect.md)。

## 向用户部署配置设置并强制登录

让 MDM 团队向所有用户部署 Docker 的配置文件。

## 下一步

恭喜！你已成功完成 Docker 管理员实施流程。

要继续优化你的 Docker 环境：

- 查看你的 [组织使用情况数据](/manuals/admin/organization/insights.md) 以跟踪采用情况
- 监控 [Docker Scout 检测结果](/manuals/scout/explore/analysis.md) 以获取安全洞察
- 探索 [更多安全功能](/manuals/enterprise/security/_index.md) 以增强你的配置