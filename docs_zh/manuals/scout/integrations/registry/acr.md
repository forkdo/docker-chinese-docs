---
description: 将 Azure Container Registry 与 Docker Scout 集成
keywords: docker scout, acr, azure, integration, image analysis, security, cves
title: 将 Docker Scout 与 Azure Container Registry 集成
linkTitle: Azure Container Registry
---

将 Docker Scout 与 Azure Container Registry (ACR) 集成后，您可以查看托管在 ACR 仓库中的镜像的洞察信息。在将 Docker Scout 与 ACR 集成并为仓库激活 Docker Scout 后，向仓库推送镜像将自动触发镜像分析。您可以使用 Docker Scout Dashboard 或 `docker scout` CLI 命令查看镜像洞察信息。

## 工作原理

为帮助您实现 Azure Container Registry 与 Docker Scout 的集成，您可以使用一个自定义的 Azure Resource Manager (ARM) 模板，该模板会自动为您在 Azure 中创建必要的基础设施：

- 用于镜像推送和删除事件的 EventGrid 主题和订阅。
- 用于注册表的只读授权令牌，用于列出仓库并提取镜像。

当资源已在 Azure 中创建后，您可以在集成的 ACR 实例中为镜像仓库启用集成。一旦您启用了一个仓库，推送新镜像将自动触发镜像分析。分析结果将显示在 Docker Scout Dashboard 中。

如果您在已包含镜像的仓库上启用集成，Docker Scout 会自动拉取并分析最新的镜像版本。

### ARM 模板

下表描述了配置资源。

> [!NOTE]
>
> 创建这些资源会在 Azure 账户上产生少量持续费用。
> 表中的 **费用** 列表示当集成每天推送 100 个镜像的 ACR 注册表时，这些资源的估计月费用。
>
> 出口费用根据使用情况而变化，但大约为每 GB 0.1 美元，前 100 GB 免费。

| Azure                   | 资源                                                                                   | 费用                                              |
| ----------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| Event Grid 系统主题 | 订阅 Azure Container Registry 事件（镜像推送和镜像删除）                 | 免费                                              |
| 事件订阅      | 通过 Webhook 订阅将 Event Grid 事件发送到 Scout                                 | 每 100 万条消息 0.60 美元。前 10 万条免费。 |
| 注册表令牌          | 用于 Scout 列出仓库并从注册表拉取镜像的只读令牌 | 免费                                              |

以下 JSON 文档显示了 Docker Scout 用于创建 Azure 资源的 ARM 模板。

{{< accordion title="JSON 模板" >}}

{{< acr-template.inline >}}
{{ with resources.GetRemote "https://prod-scout-integration-templates.s3.amazonaws.com/latest/acr_token_template.json" }}
{{ $data := .Content | transform.Unmarshal }}

```json
{{ transform.Remarshal "json" $data }}
```

{{ end }}
{{< /acr-template.inline >}}

{{< /accordion >}}

## 集成注册表

1. 转到 Docker Scout Dashboard 上的 [ACR 集成页面](https://scout.docker.com/settings/integrations/azure/)。
2. 在 **如何集成** 部分，输入您要集成的注册表的 **注册表主机名**。
3. 选择 **下一步**。
4. 选择 **部署到 Azure** 以在 Azure 中打开模板部署向导。

   如果您尚未登录 Azure 账户，可能会提示您登录。

5. 在模板向导中，配置您的部署：

   - **资源组**：输入与容器注册表使用的相同资源组。Docker Scout 资源必须部署到与注册表相同的资源组中。

   - **注册表名称**：该字段已预填充注册表主机名的子域名。

6. 选择 **查看 + 创建**，然后选择 **创建** 以部署模板。

7. 等待部署完成。
8. 在 **部署详细信息** 部分，点击新创建的 **容器注册表令牌** 类型的资源。为此令牌生成一个新密码。
    
    或者，使用 Azure 中的搜索功能导航到您希望集成的 **容器注册表** 资源，并为创建的访问令牌生成新密码。

9. 复制生成的密码，然后返回 Docker Scout Dashboard 以完成集成。
10. 将生成的密码粘贴到 **注册表令牌** 字段中。
11. 选择 **启用集成**。

选择 **启用集成** 后，Docker Scout 将执行连接测试以验证集成。如果验证成功，您将被重定向到 Azure 注册表摘要页面，该页面显示当前组织的所有 Azure 集成。

接下来，在 [仓库设置](https://scout.docker.com/settings/repos/) 中为您希望分析的仓库激活 Docker Scout。

激活仓库后，您推送的镜像将由 Docker Scout 分析。分析结果将显示在 Docker Scout Dashboard 中。如果您的仓库已包含镜像，Docker Scout 会自动拉取并分析最新的镜像版本。

## 移除集成

> [!IMPORTANT]
>
> 在 Docker Scout Dashboard 中移除集成不会自动移除在 Azure 中创建的资源。

要移除 ACR 集成：

1. 转到 Docker Scout Dashboard 上的 [ACR 集成页面](https://scout.docker.com/settings/integrations/azure/)。
2. 找到您要移除的 ACR 集成，然后选择 **移除** 按钮。
3. 在打开的对话框中，通过选择 **移除** 进行确认。
4. 在 Docker Scout Dashboard 中移除集成后，还需移除与集成相关的 Azure 资源：

   - 容器注册表的 `docker-scout-readonly-token` 令牌。
   - `docker-scout-repository` Event Grid 系统主题。