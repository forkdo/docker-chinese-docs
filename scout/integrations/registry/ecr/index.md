# 将 Docker Scout 与 Amazon ECR 集成

将 Docker Scout 与 Amazon Elastic Container Registry (ECR) 集成后，您可以查看托管在 ECR 仓库中的镜像洞察。在将 Docker Scout 与 ECR 集成并为仓库激活 Docker Scout 后，将镜像推送到该仓库会自动触发镜像分析。您可以使用 Docker Scout 仪表盘或 `docker scout` CLI 命令来查看镜像洞察。

## 工作原理

为了帮助您将 Docker Scout 与 ECR 集成，您可以使用一个 CloudFormation 堆栈模板来创建和配置必要的 AWS 资源，从而将 Docker Scout 与您的 ECR 注册表集成起来。有关 AWS 资源的更多详细信息，请参阅 [CloudFormation 堆栈模板](#cloudformation-stack-template)。

下图展示了 Docker Scout ECR 集成的工作原理。

![How the ECR integration works](../../images/Scout-ECR.png)

集成后，Docker Scout 会自动拉取并分析您推送到 ECR 注册表的镜像。有关您镜像的元数据存储在 Docker Scout 平台上，但 Docker Scout 本身不存储容器镜像。有关 Docker Scout 如何处理镜像数据的更多信息，请参阅 [数据处理](/manuals/scout/deep-dive/data-handling.md)。

### CloudFormation 堆栈模板

下表描述了配置资源。

> [!NOTE]
>
> 创建这些资源会在您的 AWS 账户上产生少量周期性费用。
> 表中的 **成本** 列代表了在集成一个每天接收 100 次镜像推送的 ECR 注册表时，这些资源的预估月度成本。
>
> 此外，当 Docker Scout 从 ECR 拉取镜像时，还会产生出口流量费用。出口流量费用约为每 GB 0.09 美元。

| Resource type                 | Resource name                 | Description                                                                                | Cost  |
| ----------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------ | ----- |
| `AWS::SNSTopic::Topic`        | `SNSTopic`                    | 用于在 AWS 资源创建后通知 Docker Scout 的 SNS 主题。                                        | 免费  |
| `AWS::SNS::TopicPolicy`       | `TopicPolicy`                 | 定义用于初始设置通知的主题。                                                                | 免费  |
| `AWS::SecretsManager::Secret` | `ScoutAPICredentials`         | 存储 EventBridge 用于向 Scout 触发事件的凭证。                                              | $0.42 |
| `AWS::Events::ApiDestination` | `ApiDestination`              | 设置 EventBridge 到 Docker Scout 的连接，用于发送 ECR 推送和删除事件。                      | $0.01 |
| `AWS::Events::Connection`     | `Connection`                  | EventBridge 到 Scout 的连接凭证。                                                           | 免费  |
| `AWS::Events::Rule`           | `DockerScoutEcrRule`          | 定义将 ECR 推送和删除事件发送到 Scout 的规则。                                              | 免费  |
| `AWS::Events::Rule`           | `DockerScoutRepoDeletedRule`  | 定义将 ECR 仓库删除事件发送到 Scout 的规则。                                                | 免费  |
| `AWS::IAM::Role`              | `InvokeApiRole`               | 用于授予事件访问 `ApiDestination` 权限的内部角色。                                          | 免费  |
| `AWS::IAM::Role`              | `AssumeRoleEcrAccess`         | 此角色有权访问 `ScoutAPICredentials`，用于设置 Docker Scout 集成。                          | 免费  |

## 集成您的第一个注册表

在您的 AWS 账户中创建 CloudFormation 堆栈以启用 Docker Scout 集成。

前提条件：

- 您必须有权访问一个具有创建资源权限的 AWS 账户。
- 您必须是 Docker 组织的所有者。

创建堆栈的步骤：

1. 前往 Docker Scout 仪表盘上的 [ECR 集成页面](https://scout.docker.com/settings/integrations/ecr/)。
2. 选择 **在 AWS 上创建** 按钮。

   这会在新的浏览器标签页中打开 AWS CloudFormation 控制台中的 **创建堆栈** 向导。如果您尚未登录 AWS，系统会首先将您重定向到登录页面。

   如果该按钮为灰色，则表示您在 Docker 组织中缺少必要的权限。

3. 按照 **创建堆栈** 向导中的步骤操作直至结束。选择您要集成的 AWS 区域。通过创建资源来完成该过程。

   向导中的字段已由 CloudFormation 模板预填充，因此您无需编辑任何字段。

4. 当资源创建完成（CloudFormation 状态在 AWS 控制台中显示为 `CREATE_COMPLETE`）后，返回 Docker Scout 仪表盘中的 ECR 集成页面。

   **已集成的注册表** 列表会显示您刚刚集成的 ECR 注册表的账户 ID 和区域。如果成功，集成状态将为 **已连接**。

ECR 集成现已激活。要让 Docker Scout 开始分析注册表中的镜像，您需要在 [仓库设置](https://scout.docker.com/settings/repos/) 中为每个仓库激活它。

激活仓库后，您推送的镜像将由 Docker Scout 进行分析。分析结果会显示在 Docker Scout 仪表盘中。
如果您的仓库中已包含镜像，Docker Scout 会自动拉取并分析最新的镜像版本。

## 集成其他注册表

添加其他注册表的步骤：

1. 前往 Docker Scout 仪表盘上的 [ECR 集成页面](https://scout.docker.com/settings/integrations/ecr/)。
2. 选择列表顶部的 **添加** 按钮。
3. 完成创建 AWS 资源的步骤。
4. 资源创建完成后，返回 Docker Scout 仪表盘中的 ECR 集成页面。

   **已集成的注册表** 列表会显示您刚刚集成的 ECR 注册表的账户 ID 和区域。如果成功，集成状态将为 **已连接**。

接下来，在 [仓库设置](https://scout.docker.com/settings/repos/) 中为您想要分析的仓库激活 Docker Scout。

## 移除集成

要移除已集成的 ECR 注册表，您必须是 Docker 组织的所有者。

1. 前往 Docker Scout 仪表盘上的 [ECR 集成页面](https://scout.docker.com/settings/integrations/ecr/)。
2. 在已集成注册表列表中找到您想要移除的注册表，然后选择 **操作** 列中的移除图标。

   如果移除图标被禁用，则表示您在 Docker 组织中缺少必要的权限。

3. 在打开的对话框中，选择 **移除** 进行确认。

> [!IMPORTANT]
>
> 从 Docker Scout 仪表盘中移除集成并不会删除您账户中的 AWS 资源。
>
> 在 Docker Scout 中移除集成后，请前往 AWS 控制台并删除您想要移除的集成对应的 **DockerScoutECRIntegration** CloudFormation 堆栈。

## 故障排除

### 无法集成注册表

在 Docker Scout 仪表盘的 [ECR 集成页面](https://scout.docker.com/settings/integrations/ecr/) 上检查集成的 **状态**。

- 如果状态长时间为 **待处理**，这表明集成尚未在 AWS 端完成。选择 **待处理** 链接以打开 CloudFormation 向导，并完成所有步骤。

- **错误** 状态表示后端出现了问题。您可以尝试 [移除集成](#remove-integration) 并重新创建。

### ECR 镜像未显示在仪表盘中

如果您的 ECR 镜像的分析结果未显示在 Docker Scout 仪表盘中：

- 确保您已为该仓库激活了 Docker Scout。您可以在 [仓库设置](https://scout.docker.com/settings/repos/) 中查看和管理活动仓库。

- 确保您注册表的 AWS 账户 ID 和区域已列在 ECR 集成页面上。

  账户 ID 和区域包含在注册表主机名中：
  `<aws_account_id>.dkr.ecr.<region>.amazonaws.com/<image>`
