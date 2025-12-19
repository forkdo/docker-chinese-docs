---
title: 部署您的 Docker 设置
description: 在整个公司范围内部署您的 Docker 设置。
weight: 40
---

> [!WARNING]
>
> 在继续操作之前，请与您的用户进行沟通，并确认您的 IT 和 MDM 团队已准备好处理任何意外问题，因为这些步骤将影响所有现有用户登录到您的 Docker 组织。

## 强制实施 SSO

强制实施 SSO 意味着任何拥有与您已验证域名匹配的电子邮件地址的 Docker 个人资料的用户都必须使用您的 SSO 连接进行登录。请确保与您的 SSO 连接关联的身份提供者组涵盖您希望访问 Docker 订阅的所有开发人员组。

有关如何强制实施 SSO 的说明，请参阅[强制实施 SSO](/manuals/enterprise/security/single-sign-on/connect.md)。

## 部署配置设置并强制用户登录

请让 MDM 团队将 Docker 的配置文件部署给所有用户。

## 下一步

恭喜您，您已成功完成 Docker 的管理员实施过程。

要继续优化您的 Docker 环境：

- 查看您的[组织使用数据](/manuals/admin/organization/insights.md)以跟踪采用情况
- 监控[Docker Scout 发现结果](/manuals/scout/explore/analysis.md)以获取安全洞察
- 探索[其他安全功能](/manuals/enterprise/security/_index.md)以增强您的配置