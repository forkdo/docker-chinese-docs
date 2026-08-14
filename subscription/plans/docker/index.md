# Docker 套餐


Docker 套餐是指将您的账户类型从基础免费套餐升级为付费套餐的套餐。付费 Docker 套餐提供更高的用量限制、商业
许可和扩展的功能集。

- Docker Personal 对个人开发者免费。Docker Pro 增加了无限私有仓库、Docker Build Cloud 和 Docker Desktop 的商业使用。
- Docker Team 和 Docker Business 是面向组织的套餐，其中 Team 增加了审计日志和基于角色的访问控制，Business 增加了 SSO、SCIM、加固版 Docker Desktop 和镜像访问管理。

要在计费门户中升级您的免费 Docker 套餐，请参阅 [管理套餐](../manage.md)。

## 用量

Docker Personal 和 Docker Pro 是面向个人账户类型的 Docker 套餐，而 Docker Team 和 Docker Business 是面向组织账户类型的 Docker 套餐。完整的功能和定价明细，请参阅
<a href="https://www.docker.com/pricing/" id="dkr_docs_index_pricing_docker_plans" class="link" rel="noopener">Docker 定价页面</a>。

> [!TIP]
> 如果您要从 Personal 套餐升级到 Team 套餐
> 并希望保留您的用户名，
> 请参阅[将您的用户账户转换为组织](/manuals/admin/organization/setup/convert-account.md)。

## 计费行为

Docker 个人和组织套餐按每用户每月的固定费率计费，提供按月或
按年计费选项。
升级套餐会立即扩展对所有功能和权益的访问。

### 组织席位

对于 Docker Team 和 Docker Business，您可以为新成员购买更多席位，以扩展对付费 Docker 套餐的访问。要为您的 Docker 套餐添加或移除席位：

1. 登录 [Docker Home](https://app.docker.com/)，然后选择您的组织账户。
1. 转到 **Billing（计费）** 查看 Overview 页面，然后转到 **Active plans（活动套餐）**。
1. 在 Docker Team 或 Docker Business 卡片中，选择操作菜单。
   - 从下拉菜单中选择 **Add seats（添加席位）** 或 **Remove seats（移除席位）**。
   - 添加或移除席位时，请根据新的总席位数审视您当前的席位。
   - 移除席位时，必须从组织中移除成员。
1. 核实您的账单信息，继续付款，并完成结账。

要了解如何在 Docker Home 中管理席位，请参阅
[管理席位](/manuals/admin/organization/manage/manage-seats.md)。

### Docker Offload 许可证

[Docker Offload](/manuals/offload/_index.md) 许可证适用于 Docker Team 和 Docker Business 套餐。分配给您的账户后，组织所有者可以在 Docker Home 中[管理许可证分配](/manuals/admin/organization/manage/manage-licenses.md)。

要添加 Docker Offload 许可证，您必须<a href="https://www.docker.com/pricing/contact-sales/" id="dkr_docs_cs_plans_docker_offload" class="link" rel="noopener">联系销售</a>。

### Docker Build Cloud 分钟数

每个套餐包含每月一定基数的 [Docker Build Cloud](/manuals/build-cloud/_index.md) 构建分钟数。基准分钟数按年度或月度周期重置，且不累积。额外购买的
分钟数在您的计费周期结束时过期。

要购买额外分钟数：

1. 从 [Docker Home](https://app.docker.com/) 中，选择您的组织。
1. 选择 Build Cloud，然后选择 Build minutes。
1. 在 **Minute breakdown（分钟明细）** 表中，选择 **Add minutes（添加分钟数）**。
1. 选择您要添加的额外分钟数量。
1. 核实您的账单信息，继续付款，并完成结账。

您额外购买的分钟数会立即显示在 Build minutes 页面上。

### Testcontainers Cloud 分钟数

每个套餐包含每月一定基数的 Testcontainers Cloud 运行时分钟数。基准分钟数按月重置且不累积。

您可以通过两种方式添加 Testcontainers Cloud 运行时分钟数：

- <a href="https://www.docker.com/pricing/contact-sales/" id="dkr_docs_cs_plans_docker_testcontainers" class="link" rel="noopener">联系销售</a> 以每 100 分钟 3 美元的价格
  预购运行时分钟数。预购的分钟数在您的计费周期结束时过期。
- 使用按需运行时分钟数，每 100 分钟 4 美元，在每个月度周期结束时计费。

## 取消 Docker 套餐

> [!NOTE]
> 如果您的 Docker Business 套餐是通过销售协助的，
> 您必须联系您的客户经理才能取消。

您可以在续费日期之前的任何时间取消，但无法暂停或延迟套餐。如果发票未在到期日之前支付，将有从到期日起 15 天的宽限期。虽然未使用的部分不可退款，但您仍保留对付费功能的访问权限，直到当前计费周期结束。

> [!NOTE]
>
> 计费周期以 UTC（协调世界时）计算。如果您所在的时区晚于 UTC，例如美国太平洋时间为 UTC−7/−8，在您当地一天的晚些时候取消或进行更改可能会落入 UTC 的下一个计费日。

取消付费套餐可能会影响协作者或组织成员：

- Docker Pro 私有仓库协作者将被移除，额外的私有仓库将被锁定。
- 通过 SCIM 配置且未设置密码的 Docker Team 或 Docker Business 成员将被锁定。如果您的组织使用单点登录，请移除 SSO 连接和已验证域名。
- 对于付费个人和组织套餐，您必须将私有仓库转换为符合新套餐限制的数量。

取消付费套餐会将您的账户恢复为 Docker Personal 或基础组织账户。
要取消套餐：

1. 登录 [Docker Home](https://app.docker.com/) 并转到 **Billing（计费）**。
2. 在 **Active plans（活动套餐）** 中，选择您的 Docker 套餐旁边的操作菜单。
3. 选择 **Cancel plan（取消套餐）** 并完成反馈调查。

