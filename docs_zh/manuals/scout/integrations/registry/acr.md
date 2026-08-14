---
description: 将 Azure Container Registry 与 Docker Scout 集成
keywords: docker scout, acr, azure, integration, image analysis, security, cves
title: 将 Docker Scout 与 Azure Container Registry 集成
linkTitle: Azure Container Registry
params:
  sidebar:
    badge:
      color: gray
      text: Deprecated
---

> [!IMPORTANT]
>
> Docker Scout 的 Azure Container Registry 集成已弃用，并将于 2026 年 9 月 1 日停用。
> 请迁移到 [`docker scout watch`](/reference/cli/docker/scout/watch/) 以进行持续分析，或将 Scout 集成到您的 CI 流水线中。
> 请参阅 [从 ACR 集成迁移](#migrate-from-the-acr-integration)。

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

## 从 ACR 集成迁移

有两种可用的迁移路径。

### 持续轮询

最适合希望在不更改其构建流水线的情况下，进行持续的、覆盖整个注册表的分析的团队。`docker scout watch` 作为一个长期运行的进程运行，轮询您的 ACR 注册表并将结果推送到 Docker Scout，复现集成所提供的功能。

1. 选择用于运行 `docker scout watch` 的宿主。

   该宿主必须能够访问您的 ACR 注册表，并能够通过互联网访问 Scout API（`https://api.scout.docker.com`）。

2. 确保您运行的是最新版本的 Scout。

   ```console
   $ docker scout version
   ```

   如有必要，请[安装最新版本的 Scout](https://docs.docker.com/scout/install/)。

3. 将 Docker 身份验证到您的 ACR 注册表。

   ```console
   $ docker login <registry-name>.azurecr.io \
     --username <username> \
     --password <password-or-access-token>
   ```

   > [!TIP]
   >
   > 作为最佳实践，请创建一个对注册表具有只读（拉取）访问权限的专用服务主体或令牌。

4. 设置您的 Scout 凭据。

   1. 生成一个组织访问令牌。有关更多详细信息，请参阅[创建组织访问令牌](/enterprise/security/access-tokens/#create-an-organization-access-token)。
   2. 使用组织访问令牌登录 Docker。

      ```console
      $ docker login --username <your_organization_name>
      ```

      当提示输入密码时，粘贴组织访问令牌。

   3. 将您的本地 Docker 环境连接到您组织的 Docker Scout 服务。

      ```console
      $ docker scout enroll <your_organization_name>
      ```

5. 索引现有镜像。您只需执行一次此操作。

   使用 `--all-images` 标志运行 `docker scout watch`，以回填注册表中的所有现有镜像。

   ```console
   $ docker scout watch \
     --org <your-org> \
     --registry <registry-name>.azurecr.io \
     --all-images
   ```

6. 通过在 [Scout Dashboard](https://scout.docker.com/) 上查看镜像，确认镜像已被索引。

7. 持续监视新镜像。

   运行 `docker scout watch` 以轮询未来的新镜像。使用 `--interval`（默认 60 秒）来控制轮询频率，使用 `--repository` 和 `--tag` 来缩小范围。

   ```console
   $ docker scout watch \
     --org <your-org> \
     --registry <registry-name>.azurecr.io \
     --refresh-registry
   ```

   `docker scout watch` 是一个长期运行的进程。请将其作为系统服务（例如使用 `systemd` 或 `nohup`）运行，以确保它在后台持续运行。

参考：[`docker scout watch`](/reference/cli/docker/scout/watch/)

### 在 CI 中进行构建时分析

最适合已经拥有 CI 流水线、并希望将分析范围限定在其主动构建和推送的镜像上的团队。无需长期运行的进程。

在流水线中执行 `docker build` 之后，运行：

- `docker scout quickview` 或 `docker scout cves` 来分析镜像。
- `docker scout compare --to-env <env>` 用于针对策略的 PR 门禁。
- `docker scout environment` 用于将镜像记录到环境。

请参阅 [将 Docker Scout 与 CI 集成](../_index.md#continuous-integration)。
