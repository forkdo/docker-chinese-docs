---
title: 管理许可分配
linkTitle: 许可分配
description: 为您的组织管理产品许可，包括分配、撤销和自动分配。
keywords: licenses, organization, members, Docker Core, Docker Offload, AI governance, license assignment, docker home
weight: 30
---

许可让您可以精心选择组织中的哪些成员能够访问受支持的 Docker 产品。组织所有者可以监督其团队中谁持有有效许可，或者配置在成员访问受支持的 Docker 产品时自动分配许可。与 Docker Core 席位一样，许可可以按成员逐一配置。

> [!TIP]
> 要了解有关产品许可、Docker Core 席位和其他 Docker 附加组件的更多信息，请参阅 [Docker 套餐](/manuals/subscription/plans/_index.md)，
> 或 <a href="https://www.docker.com/pricing/contact-sales/" id="dkr_docs_cs_admin_licenses" class="link" rel="noopener">联系销售</a> 购买许可。

## 管理许可

**Members**（成员）页面让您可以跟踪组织可用的许可数量以及当前持有许可的人员。您也可以在此页面上分配或撤销许可。

要管理组织的许可：

1. 登录 [Docker Home](https://app.docker.com)，然后选择您的组织。
1. 从左侧导航中选择 **Members**（成员）。
1. 选择行末的操作菜单以分配或撤销有效许可。
1. 可选。要批量分配或撤销许可，选择您要批量管理的成员，然后选择 **Bulk actions**（批量操作）菜单。
1. 可选。要管理自动许可分配，使用 **Automatically assign licenses**（自动分配许可）开关进行关闭或开启。

你必须手动分配许可，或者配置自动许可分配才能消耗许可。在 [邀请流程](/manuals/admin/organization/manage/members.md) 期间选择 **Licenses (optional)**（许可（可选））中的产品会消耗一个席位或许可，但默认不会自动分配产品许可。相反，购买一组许可不会触发向现有成员自动分配。

## 自动许可分配

自动许可分配会在成员首次使用受支持的产品时为其提供产品许可。自动许可分配适用于 AI Governance 许可。只有购买了 AI Governance 的组织才能为 Docker Core 设置自动分配。

- 当您购买 AI Governance 后，使用 `sbx` CLI 中的 `login` 命令（`sbx login`）登录 [Docker Sandboxes](https://docs.docker.com/ai/sandboxes/) 会按先到先得的方式自动配置 AI Governance 许可。
- 类似地，登录 Docker Desktop 会为购买了 AI Governance 且拥有可用 Docker Core 席位的组织自动配置 Docker Core。
- 许可会一直分配，直到耗尽为止。
  - 一旦可用许可耗尽，自动许可分配将停止，直到您购买更多许可或撤销已分配的许可。
  - 成员仍可使用 Docker Sandbox 或 Docker Desktop，但这些产品的组织策略不会影响他们的使用。

无论您的 Docker Core 订阅如何，AI Governance 许可都包含单点登录 (SSO) 和配置功能。自动许可分配需要 [设置 SSO](/manuals/enterprise/security/single-sign-on/connect.md)，然后通过跨域身份管理系统 (SCIM) 或即时 (JIT) 进行 [配置](/manuals/enterprise/security/provisioning/_index.md)。

## 后续步骤

请参阅以下文档探索 Docker Core 附加组件或需要许可的产品：

- [Docker 套餐](/manuals/subscription/plans/_index.md) 了解不同的附加组件
- [管理席位](/manuals/admin/organization/manage/manage-seats.md) 为您的 Docker Core 订阅添加更多席位
- [AI Governance 套餐](/manuals/subscription/plans/ai-governance.md) 了解 AI Governance 许可的使用和计费
- [Docker Offload](/manuals/offload/about.md) 让您的开发者将构建和运行容器卸载到云端
