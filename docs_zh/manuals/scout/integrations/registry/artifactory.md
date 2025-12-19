---
description: 将 Artifactory 容器注册表与 Docker Scout 集成
keywords: docker scout, artifactory, integration, image analysis, security, cves
title: 将 Docker Scout 与 Artifactory 容器注册表集成
linkTitle: Artifactory 容器注册表
aliases:
  - /scout/artifactory/
---

{{% experimental %}}

`docker scout watch` 命令是实验性功能。

实验性功能旨在用于测试和收集反馈，因为其功能或设计可能会在版本更新之间发生变更，恕不另行通知，或者可能会在未来的版本中完全移除。

{{% /experimental %}}

将 Docker Scout 与 JFrog Artifactory 集成，可让您对 Artifactory 中的镜像进行索引和分析。该集成由一个长期运行的 `docker scout watch` 进程提供支持。它会从您选择的仓库中提取镜像（可选择性过滤），接收来自 Artifactory 的 Webhook 回调，并将镜像数据推送到 Docker Scout。您可以在 Docker Scout 仪表板或通过 `docker scout` CLI 查看结果。

## 工作原理

您可以在您控制的宿主机上运行 [`docker scout watch`](/reference/cli/docker/scout/watch/)，并通过 `--registry "key=value,..."` 配置 Artifactory 特定的注册表字符串。watch 进程可以：

- 监视特定仓库或整个注册表
- 可选择一次性摄取所有现有镜像
- 定期刷新仓库列表
- 在您选择的本地端口上接收来自 Artifactory 的 Webhook 回调

集成完成后，Docker Scout 会自动拉取并分析您推送到 Artifactory 注册表的镜像。有关镜像的元数据会存储在 Docker Scout 平台上，但 Docker Scout 不会存储容器镜像本身。有关 Docker Scout 如何处理镜像数据的更多信息，请参阅[数据处理](/manuals/scout/deep-dive/data-handling.md)。

### Artifactory 特定的注册表字符串选项

这些 `type=artifactory` 选项会覆盖 `--registry` 选项的通用注册表处理逻辑：

| 键名             | 是否必需 | 描述                                                                                   |
|------------------|:--------:|----------------------------------------------------------------------------------------|
| `type`           |   是     | 必须为 `artifactory`。                                                                 |
| `registry`       |   是     | Docker/OCI 注册表主机名（例如：`example.jfrog.io`）。                                  |
| `api`            |   是     | Artifactory REST API 基础 URL（例如：`https://example.jfrog.io/artifactory`）。        |
| `repository`     |   是     | 要监视的仓库（替代 `--repository`）。                                                  |
| `includes`       |   否     | 包含的通配符（例如：`*/frontend*`）。                                                  |
| `excludes`       |   否     | 排除的通配符（例如：`*/legacy/*`）。                                                   |
| `port`           |   否     | 用于接收 Webhook 回调的本地端口。                                                      |
| `subdomain-mode` |   否     | `true` 或 `false`；匹配 Artifactory 的 Docker 布局（子域名 vs 仓库路径）。             |

## 集成 Artifactory 注册表

请按照以下步骤将您的 Artifactory 注册表与 Docker Scout 集成。

1. 选择运行 `docker scout watch` 的宿主机。

   该宿主机必须能够本地或通过网络访问您的私有注册表，并且能够通过互联网访问 Scout API（`https://api.scout.docker.com`）。如果您使用 Webhook 回调，Artifactory 还必须能够通过配置的端口访问 Scout 客户端宿主机。
   根据宿主机的大小和预期工作负载，覆盖 `--workers` 选项（默认值：`3`）以获得最佳性能。

2. 确保您运行的是最新版本的 Scout。

   检查您当前的版本：

   ```console
   $ docker scout version
   ```

   如有必要，请[安装最新版本的 Scout](https://docs.docker.com/scout/install/)。

3. 设置您的 Artifactory 凭据。

   存储 Scout 客户端用于向 Artifactory 进行身份验证的凭据。以下是使用环境变量的示例。将 `<user>` 和 `<password-or-access-token>` 替换为您的实际值。

   ```console
   $ export DOCKER_SCOUT_ARTIFACTORY_API_USER=<user>
   $ export DOCKER_SCOUT_ARTIFACTORY_API_PASSWORD=<password-or-access-token>
   ```

   > [!TIP]
   >
   > 最佳实践是创建一个具有只读访问权限的专用用户，并使用访问令牌而不是密码。

   存储 Artifactory 用于对 Webhook 回调进行身份验证的凭据。以下是使用环境变量的示例。将 `<random-64-128-character-secret>` 替换为实际密钥。

   ```console
   $ export DOCKER_SCOUT_ARTIFACTORY_WEBHOOK_SECRET=<random-64-128-character-secret>
   ```

   > [!TIP]
   >
   > 最佳实践是生成一个 64-128 个字符的高熵随机字符串。

4. 设置您的 Scout 凭据。

   1. 生成一个用于访问 Scout 的组织访问令牌。有关更多详细信息，请参阅[创建组织访问令牌](/enterprise/security/access-tokens/#create-an-organization-access-token)。
   2. 使用组织访问令牌登录 Docker。

       ```console
       $ docker login --username <your_organization_name>
       ```

       当提示输入密码时，粘贴您生成的组织访问令牌。

   3. 将您的本地 Docker 环境连接到您组织的 Docker Scout 服务。

       ```console
       $ docker scout enroll <your_organization_name>
       ```

5. 索引现有镜像。您只需执行一次此操作。

    使用 `--all-images` 选项运行 `docker scout watch`，以索引指定 Artifactory 仓库中的所有镜像。以下是示例命令：

   ```console
   $ docker scout watch --registry \
   "type=artifactory,registry=example.jfrog.io,api=https://example.jfrog.io/artifactory,include=*/frontend*,exclude=*/dta/*,repository=docker-local,port=9000,subdomain-mode=true" \
   --all-images
   ```

6. 通过在 [Scout 仪表板](https://scout.docker.com/)上查看镜像，确认镜像已被索引。

7. 配置 Artifactory 回调。

   在您的 Artifactory UI 或通过 REST API 中，为镜像推送/更新事件配置 Webhook。将端点设置为您 `docker scout watch` 宿主机和端口，并包含 `DOCKER_SCOUT_ARTIFACTORY_WEBHOOK_SECRET` 以进行身份验证。

   有关更多信息，请参阅 [JFrog Artifactory Webhooks 文档](https://jfrog.com/help/r/jfrog-platform-administration-documentation/webhooks) 或 [JFrog Artifactory REST API Webhooks 文档](https://jfrog.com/help/r/jfrog-rest-apis/webhooks)。

8. 持续监视新镜像或更新的镜像。

   使用 `--refresh-registry` 选项运行 `docker scout watch`，以监视需要索引的新镜像。以下是示例命令：

   ```console
   $ docker scout watch --registry \
   "type=artifactory,registry=example.jfrog.io,api=https://example.jfrog.io/artifactory,include=*/frontend*,exclude=*/dta/*,repository=docker-local,port=9000,subdomain-mode=true" \
   --refresh-registry
   ```

9. 可选。为来自流行协作平台的实时通知设置 Scout 集成。有关详细信息，请参阅[将 Docker Scout 与 Slack 集成](../team-collaboration/slack.md)。