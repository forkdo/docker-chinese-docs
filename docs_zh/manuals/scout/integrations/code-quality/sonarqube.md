---
title: 将 Docker Scout 与 SonarQube 集成
linkTitle: SonarQube
description: 使用项目中定义的 SonarQube 质量门禁评估镜像
keywords: scout, supply chain, integration, code quality
---

SonarQube 集成功能使 Docker Scout 能够通过策略评估展示 SonarQube 质量门禁检查，具体位于新的 [SonarQube 质量门禁策略](/manuals/scout/policy/_index.md#sonarqube-quality-gates-policy) 下。

## 工作原理

此集成使用 [SonarQube Webhook](https://docs.sonarsource.com/sonarqube/latest/project-administration/webhooks/) 在 SonarQube 项目分析完成时通知 Docker Scout。当 Webhook 被调用时，Docker Scout 会接收分析结果并将其存储在数据库中。

当您向仓库推送新镜像时，Docker Scout 会评估与该镜像对应的 SonarQube 分析记录结果。Docker Scout 利用镜像上的 Git 来源元数据（来自来源证明或 OCI 注解）将镜像仓库与 SonarQube 分析结果相关联。

> [!NOTE]
>
> Docker Scout 无法访问历史 SonarQube 分析记录。只有在集成启用后记录的分析结果才会对 Docker Scout 可用。

支持自托管 SonarQube 实例和 SonarCloud。

## 先决条件

要将 Docker Scout 与 SonarQube 集成，请确保：

- 您的镜像仓库已与 [Docker Scout 集成](../_index.md#container-registries)。
- 您的镜像在构建时包含 [来源证明](/manuals/build/metadata/attestations/slsa-provenance.md) 或 `org.opencontainers.image.revision` 注解，其中包含有关 Git 仓库的信息。

## 启用 SonarQube 集成

1. 前往 Docker Scout 仪表板上的 [SonarQube 集成页面](https://scout.docker.com/settings/integrations/sonarqube/)。
2. 在 **如何集成** 部分，为此集成输入一个配置名称。Docker Scout 使用此标签作为集成的显示名称，并用于命名 Webhook。
3. 选择 **下一步**。
4. 输入您的 SonarQube 实例的配置详细信息。Docker Scout 使用此信息创建 SonarQube Webhook。

   在 SonarQube 中，[生成一个新的 **用户令牌**](https://docs.sonarsource.com/sonarqube/latest/user-guide/user-account/generating-and-using-tokens/#generating-a-token)。该令牌需要对指定项目具有“管理”权限，或全局“管理”权限。

   输入令牌、您的 SonarQube URL 以及 SonarQube 组织的 ID。如果您使用的是 SonarCloud，则必须提供 SonarQube 组织 ID。

5. 选择 **启用配置**。

   Docker Scout 会执行连接测试，以验证所提供的详细信息是否正确，以及令牌是否具有必要的权限。

6. 连接测试成功后，您将被重定向到 SonarQube 集成概览页面，其中列出了所有 SonarQube 集成及其状态。

在集成概览页面中，您可以直接进入 **SonarQube 质量门禁策略**。
此策略最初不会有任何结果。要开始查看此策略的评估结果，请触发项目的新 SonarQube 分析，并将相应镜像推送到仓库。有关更多信息，请参阅 [策略描述](../../policy/_index.md#sonarqube-quality-gates)。