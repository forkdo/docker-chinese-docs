---
description: 将 Amazon Elastic Container Registry 与 Docker Scout 集成
keywords: docker scout, ecr, 集成, 镜像分析, 安全, cves
title: 将 Docker Scout 与 Amazon ECR 集成
linkTitle: Amazon ECR
---

将 Docker Scout 与 Amazon Elastic Container Registry (ECR) 集成后，您可以查看托管在 ECR 仓库中的镜像的洞察信息。完成 Docker Scout 与 ECR 的集成并为仓库启用 Docker Scout 后，向仓库推送镜像会自动触发镜像分析。您可以使用 Docker Scout 仪表板或 `docker scout` CLI 命令查看镜像洞察。

## 工作原理

为了帮助您集成 Docker Scout 与 ECR，您可以使用 CloudFormation 堆栈模板创建和配置必要的 AWS 资源，以将 Docker Scout 与您的 ECR 注册表集成。有关 AWS 资源的更多详细信息，请参阅[CloudFormation 堆栈模板](#cloudformation-stack-template)。

下图展示了 Docker Scout ECR 集成的工作原理。

![ECR 集成工作原理](../../images/Scout-ECR.png)

集成后，Docker Scout 会自动拉取并分析您推送到 ECR 注册表的镜像。镜像的元数据存储在 Docker Scout 平台上，但 Docker Scout 不存储容器镜像本身。有关 Docker Scout 如何处理镜像数据的更多信息，请参阅[数据处理](/manuals/scout/deep-dive/data-handling.md)。

### CloudFormation 堆栈模板

下表描述了配置资源。

> [!NOTE]
>
> 创建这些资源会在 AWS 账户上产生少量重复费用。表中的 **Cost** 列表示在集成每天接收 100 个镜像推送的 ECR 注册表时，资源的估计月费用。
>
> 此外，当 Docker Scout 从 ECR 拉取镜像时，还会产生出口流量费用。出口流量费用约为每 GB $0.09。

| 资源类型                      | 资源名称                      | 描述                                                                                       | 费用  |
| ----------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------ | ----- |
| `AWS::SNSTopic::Topic`        | `SNSTopic`                    | 用于在 AWS 资源创建完成后通知 Docker Scout 的 SNS 主题。                                   | 免费  |
| `AWS::SNS::TopicPolicy`       | `TopicPolicy`                 | 定义初始设置通知的主题。                                                                     | 免费  |
| `AWS::SecretsManager::Secret` | `ScoutAPICredentials`         | 存储 EventBridge 用于向 Scout 发送事件的凭据。                                             | $0.42 |
| `AWS::Events::ApiDestination` | `ApiDestination`              | 设置 EventBridge 连接，将 ECR 推送和删除事件发送到 Docker Scout。                          | $0.01 |
| `AWS::Events::Connection`     | `Connection`                  | EventBridge 到 Scout 的连接凭据。                                                          | 免费  |
| `AWS::Events::Rule`           | `DockerScoutEcrRule`          | 定义将 ECR 推送和删除发送到 Scout 的规则。                                                 | 免费  |
| `AWS::Events::Rule`           | `DockerScoutRepoDeletedRule`  | 定义将 ECR 仓库删除发送到 Scout 的规则。                                                   | 免费  |
| `AWS::IAM::Role`              | `InvokeApiRole`               | 授予事件访问 `ApiDestination` 的内部角色。                                                  | 免费  |
| `AWS::IAM::Role`              | `AssumeRoleEcrAccess`         | 此角色可访问 `ScoutAPICredentials` 以设置 Docker Scout 集成。                              | 免费  |

## 集成您的第一个注册表

在 AWS 账户中创建 CloudFormation 堆栈以启用 Docker Scout 集成。

先决条件：

- 您必须拥有可创建资源的 AWS 账户访问权限。
- 您必须是 Docker 组织的所有者。

创建堆栈步骤：

1. 转到 Docker Scout 仪表板上的 [ECR 集成页面](https://scout.docker.com/settings/integrations/ecr/)。
2. 选择 **Create on AWS** 按钮。

   这将在 AWS CloudFormation 控制台中打开 **Create stack** 向导，新浏览器标签页。如果您尚未登录 AWS，将首先重定向到登录页面。

   如果按钮为灰色，表示您在 Docker 组织中缺少必要的权限。

3. 按照 **Create stack** 向导中的步骤操作，直到完成。选择您要集成的 AWS 区域。通过创建资源完成该过程。

   向导中的字段由 CloudFormation 模板预填充，因此您无需编辑任何字段。

4. 资源创建完成后（AWS 控制台中的 CloudFormation 状态显示 `CREATE_COMPLETE`），返回 Docker Scout 仪表板上的 ECR 集成页面。

   **Integrated registries** 列表显示您刚刚集成的 ECR 注册表的账户 ID 和区域。如果成功，集成状态为 **Connected**。

ECR 集成现已激活。为了让 Docker Scout 开始分析注册表中的镜像，您需要在 [Repository settings](https://scout.docker.com/settings/repos/) 中为每个仓库启用它。

启用仓库后，您推送的镜像将由 Docker Scout 进行分析。分析结果将显示在 Docker Scout 仪表板中。如果您的仓库已包含镜像，Docker Scout 会自动拉取并分析最新镜像版本。

## 集成额外的注册表

要添加额外的注册表：

1. 转到 Docker Scout 仪表板上的 [ECR 集成页面](https://scout.docker.com/settings/integrations/ecr/)。
2. 选择列表顶部的 **Add** 按钮。
3. 完成创建 AWS 资源的步骤。
4. 资源创建完成后，返回 Docker Scout 仪表板上的 ECR 集成页面。

   **Integrated registries** 列表显示您刚刚集成的 ECR 注册表的账户 ID 和区域。如果成功，集成状态为 **Connected**。

接下来，在 [Repository settings](https://scout.docker.com/settings/repos/) 中为要分析的仓库启用 Docker Scout。

## 移除集成

要移除集成的 ECR 注册表，您必须是 Docker 组织的所有者。

1. 转到 Docker Scout 仪表板上的 [ECR 集成页面](https://scout.docker.com/settings/integrations/ecr/)。
2. 在集成注册表列表中找到您要移除的注册表，选择 **Actions** 列中的移除图标。

   如果移除图标被禁用，表示您在 Docker 组织中缺少必要的权限。

3. 在打开的对话框中，选择 **Remove** 确认。

> [!IMPORTANT]
>
> 从 Docker Scout 仪表板移除集成不会移除您账户中的 AWS 资源。
>
> 从 Docker Scout 移除集成后，请转到 AWS 控制台，删除您要移除的集成的 **DockerScoutECRIntegration** CloudFormation 堆栈。

## 故障排除

### 无法集成注册表

在 Docker Scout 仪表板的 [ECR 集成页面](https://scout.docker.com/settings/integrations/ecr/) 上检查集成的 **Status**。

- 如果状态长时间为 **Pending**，表明 AWS 侧的集成尚未完成。选择 **Pending** 链接打开 CloudFormation 向导，完成所有步骤。

- **Error** 状态表示后端出现问题。您可以尝试[移除集成](#remove-integration) 并重新创建。

### ECR 镜像未在仪表板中显示

如果您的 ECR 镜像分析结果未在 Docker Scout 仪表板中显示：

- 确保您已为仓库启用 Docker Scout。在 [Repository settings](https://scout.docker.com/settings/repos/) 中查看和管理活动仓库。

- 确保您的注册表的 AWS 账户 ID 和区域列在 ECR 集成页面上。

  账户 ID 和区域包含在注册表主机名中：
  `<aws_account_id>.dkr.ecr.<region>.amazonaws.com/<image>`