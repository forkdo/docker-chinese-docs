---
title: 概述
linkTitle: 订阅
description: 了解 Docker 的各种套餐，例如如何订阅基于产品的套餐，以及它们如何应用于个人和组织账户。
keywords:
  docker subscription, pricing, billing, subscription types, subscription
  plans, docker hardened images, gordon, cloud sandboxes, subscription
  management
weight: 20
params:
  sidebar:
    group: Platform
grid_subscriptions:
  - title: 比较 Docker 套餐
    description: 访问定价页面，查看不同 Docker 套餐包含的内容。
    link: "https://www.docker.com/pricing?ref=Docs&refAction=DocsSubscription"
    icon: magnifying-glass
  - title: 管理套餐
    description: 添加新套餐、升级活动套餐，或取消自动续费。
    link: /subscription/manage/
    icon: shopping-cart
  - title: 浏览套餐
    description: 浏览适用于个人、团队和组织的可用 Docker 套餐及附加组件。
    link: /subscription/plans/
    icon: chart-bar
  - title: Docker Desktop 许可协议
    description: 查看 Docker 订阅服务协议的条款。
    link: /subscription/desktop-license/
    icon: document-text
  - title: 套餐常见问题
    description: 找到您需要的答案，探索常见问题。
    link: /subscription/faq/
    icon: question-mark-circle
aliases:
  - /docker-hub/billing/
  - /docker-hub/billing/faq/
---

您可以订阅从免费到付费的多种 Docker 套餐。当您升级套餐时，会扩展您对 Docker 产品的使用权益和功能集。您还可以为某些套餐追加用量，在不更改套餐类型的情况下将使用权限扩展到更多用户。

## Docker 套餐

您可以为个人账户或组织账户订阅套餐，也可以为特定产品订阅套餐。下表总结了可用的套餐。

| 套餐                                                              | 计费模式                                             | 类型                                                     |
| ------------------------------------------------------------------ | --------------------------------------------------------- | --------------------------------------------------------- |
| [Docker](/manuals/subscription/plans/docker.md)                    | 适用于个人和组织账户的固定费率套餐    | Docker Personal、Docker Pro、Docker Team、Docker Business |
| [Docker Hardened Images (DHI)](/manuals/subscription/plans/dhi.md) | 面向加固容器镜像的阶梯式安全特性 | DHI Community、DHI Select、DHI Enterprise                 |
| [Gordon](/manuals/subscription/plans/gordon.md)                    | Gordon AI 代理的预付费用量 | Gordon Plus、Gordon Max、Gordon Ultra                     |
| [AI Governance](/manuals/subscription/plans/ai-governance.md)      | 购买设定数量的许可证                           | AI Governance                                             |

升级账户的 Docker 套餐（Docker Pro 或 Docker Team 和 Business）可以为大多数用例提供基础。某些产品套餐可能需要升级的 Docker 账户，而其他产品套餐允许您在未升级账户的情况下订阅。了解更多，请参阅 [Docker 套餐](/manuals/subscription/plans/_index.md)。

## 追加套餐用量

套餐附带使用权益，可以在不升级到不同套餐的情况下进行扩展。

| 单位         | 说明                                                                           | 示例                      |
| ------------ | ------------------------------------------------------------------------------------- | ----------------------------- |
| 席位        | 每个席位将使用权益扩展到另外一名成员。                                    | Docker Team、Docker Business  |
| 许可证     | 访问特定产品或功能。                                              | AI Governance、Docker Offload |
| 分钟      | 云构建容量，按块出售并在计费周期内消耗。          | Docker Build Cloud            |
| 仓库       | 受安全扫描和分析功能覆盖的额外容器仓库。 | DHI                           |

## 管理您的套餐

要订阅新套餐，您可以通过 [Docker Home](https://app.docker.com) 中的 **Billing（计费）** 自助办理，或通过 <a href="https://www.docker.com/pricing/contact-sales/" id="dkr_docs_index_sales" class="link" rel="noopener">联系销售</a>。

要了解有关添加新套餐或升级活动套餐的更多信息，请参阅 [管理套餐](/manuals/subscription/manage.md)。

## 后续步骤

{{< grid items="grid_subscriptions" >}}
