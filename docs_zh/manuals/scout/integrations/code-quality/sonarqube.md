---
title: 将 Docker Scout 与 SonarQube 集成
linkTitle: SonarQube
description: 使用项目中定义的 SonarQube 质量门禁评估你的镜像
keywords: scout, 供应链, 集成, 代码质量
---

SonarQube 集成使 Docker Scout 能够通过策略评估展示 SonarQube 质量门禁检查，
这些检查位于新的 [SonarQube 质量门禁策略](/manuals/scout/policy/_index.md#sonarqube-quality-gates-policy) 下。

## 工作原理

此集成使用 [SonarQube
webhook](https://docs.sonarsource.com/sonarqube/latest/project-administration/webhooks/)
在 SonarQube 项目分析完成时通知 Docker Scout。当 webhook 被调用时，
Docker Scout 接收分析结果并将其存储在数据库中。

当你向仓库推送新镜像时，Docker Scout 会评估与该镜像对应的 SonarQube 分析记录。
Docker Scout 使用镜像上的 Git 来源元数据（来自来源证明声明或 OCI 注释），
将镜像仓库与 SonarQube 分析结果关联起来。

> [!NOTE]
>
> Docker Scout 无法访问历史 SonarQube 分析记录。只有在启用集成后记录的
> 分析结果才能被 Docker Scout 使用。

支持自托管的 SonarQube 实例和 SonarCloud。

## 前置条件

要将 Docker Scout 与 SonarQube 集成，请确保：

- 你的镜像仓库已[与 Docker Scout 集成](../_index.md#container-registries)。
- 你的镜像已使用[来源证明声明](/manuals/build/metadata/attestations/slsa-provenance.md)
  或包含 Git 仓库信息的 `org.opencontainers.image.revision` 注释构建。

## 启用 SonarQube 集成

1. 前往 Docker Scout 仪表板上的
   [SonarQube 集成页面](https://scout.docker.com/settings/integrations/sonarqube/)。
2. 在 **如何集成** 部分，输入此集成的配置名称。Docker Scout 使用此标签
   作为集成的显示名称，并用于命名 webhook。
3. 选择 **下一步**。
4. 输入你的 SonarQube 实例的配置详细信息。Docker Scout 使用这些信息
   创建 SonarQube webhook。

   在 SonarQube 中，[生成新的 **用户令牌**](https://docs.sonarsource.com/sonarqube/latest/user-guide/user-account/generating-and-using-tokens/#generating-a-token)。
   该令牌需要在指定项目上具有“管理”权限，或全局“管理”权限。

   输入令牌、你的 SonarQube URL 和 SonarQube 组织的 ID。
   如果你使用的是 SonarCloud，则需要 SonarQube 组织信息。

5. 选择 **启用配置**。

   Docker Scout 会执行连接测试，以验证提供的详细信息是否正确，
   以及令牌是否具有必要的权限。

6. 连接测试成功后，你将被重定向到 SonarQube 集成概览页面，
   该页面列出你所有的 SonarQube 集成及其状态。

从集成概览页面，你可以直接进入 **SonarQube 质量门禁策略**。
此策略最初将没有结果。要在此策略中看到评估结果，
请触发项目的新的 SonarQube 分析，并将相应的镜像推送到仓库。
更多信息，请参考[策略描述](../../policy/_index.md#sonarqube-quality-gates)。