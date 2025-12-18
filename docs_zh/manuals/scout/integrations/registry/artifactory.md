---
description: 将 Artifactory 容器注册中心与 Docker Scout 集成
keywords: docker scout, artifactory, 集成, 镜像分析, 安全, cves
title: 将 Docker Scout 与 Artifactory 容器注册中心集成
linkTitle: Artifactory 容器注册中心
aliases:
  - /scout/artifactory/
---

{{% experimental %}}

`docker scout watch` 命令为实验性功能。

实验性功能旨在用于测试和反馈，其功能或设计可能在发布之间发生变更而不会发出警告，或者可能在未来的版本中完全移除。

{{% /experimental %}}

将 Docker Scout 与 JFrog Artifactory 集成，可让您对 Artifactory 中的镜像进行索引和分析。此集成由一个长期运行的 `docker scout watch` 进程驱动。它从您选择的仓库中拉取镜像（可选过滤），可以接收来自 Artifactory 的 webhook 回调，并将镜像数据推送到 Docker Scout。您可以在 Docker Scout 仪表板或使用 `docker scout` CLI 中查看结果。

## 工作原理

您在自己控制的主机上运行 [`docker scout watch`](/reference/cli/docker/scout/watch/)，并通过 `--registry "key=value,..."` 配置特定于 Artifactory 的注册中心字符串。watch 进程可以：

- 监视特定仓库或整个注册中心
- 可选地一次性摄取所有现有镜像
- 定期刷新仓库列表
- 在您选择的本地端口上接收来自 Artifactory 的 webhook 回调

集成后，Docker Scout 会自动拉取并分析您推送到 Artifactory 注册中心的镜像。镜像的元数据存储在 Docker Scout 平台上，但 Docker Scout 不存储容器镜像本身。有关 Docker Scout 如何处理镜像数据的更多信息，请参阅 [数据处理](/manuals/scout/deep-dive/data-handling.md)。

### Artifactory 特定注册中心字符串选项

这些 `type=artifactory` 选项覆盖 `--registry` 选项的通用注册中心处理：

| 键               | 是否必需 | 描述                                                                                 |
|------------------|:--------:|--------------------------------------------------------------------------------------|
| `type`           |   是     | 必须为 `artifactory`。                                                               |
| `registry`       |   是     | Docker/OCI 注册中心主机名（例如 `example.jfrog.io`）。                               |
| `api`            |   是     | Artifactory REST API 基础 URL（例如 `https://example.jfrog.io/artifactory`）。       |
| `repository`     |   是     | 要监视的仓库（替代 `--repository`）。                                                  |
| `includes`       |   否     | 要包含的 glob 模式（例如 `*/frontend*`）。                                             |
| `excludes`       |   否     | 要排除的 glob 模式（例如 `*/legacy/*`）。                                              |
| `port`           |   否     | 用于监听 webhook 回调的本地端口。                                                      |
| `subdomain-mode` |   否     | `true` 或 `false`；匹配 Artifactory 的 Docker 布局（子域名模式与仓库路径模式）。       |

## 集成 Artifactory 注册中心

请按照以下步骤将您的 Artifactory 注册中心与 Docker Scout 集成。

1. 选择运行 `docker scout watch` 的主机。

   该主机必须能够本地或通过网络访问您的私有注册中心，并能够通过互联网访问 Scout API（`https://api.scout.docker.com`）。如果您使用 webhook 回调，Artifactory 也必须能够访问 Scout 客户端主机上配置的端口。
   根据主机大小和预期工作负载，覆盖 `--workers` 选项（默认值：`3`）以获得最佳性能。

2. 确保您运行的是最新版本的 Scout。

   检查您的当前版本：

   ```console
   $ docker scout version
   ```

   如有必要，请[安装最新版本的 Scout](https://docs.docker.com/scout/install/)。

3. 设置 Artifactory 凭据。

   存储 Scout 客户端用于向 Artifactory 进行身份验证的凭据。以下是使用环境变量的示例。将 `<user>` 和 `<password-or-access-token>` 替换为您的实际值。

   ```console
   $ export DOCKER_SCOUT_ARTIFACTORY_API_USER=<user>
   $ export DOCKER_SCOUT_ARTIFACTORY_API_PASSWORD=<password-or-access-token>
   ```

   > [!TIP]
   >
   > 最佳实践是创建一个具有只读访问权限的专用用户，并使用访问令牌而不是密码。

   存储 Artifactory 用于验证 webhook 回调的凭据。以下是使用环境变量的示例。将 `<random-64-128-character-secret>` 替换为实际密钥。

   ```console
   $ export DOCKER_SCOUT_ARTIFACTORY_WEBHOOK_SECRET=<random-64-128-character-secret>
   ```

   > [!TIP]
   >
   > 最佳实践是生成一个 64-128 个字符的高熵随机字符串。

4. 设置您的 Scout 凭据。

   1. 为访问 Scout 生成组织访问令牌。更多详细信息，请参阅 [创建组织访问令牌](/enterprise/security/access-tokens/#create-an-organization-access-token)。
   2. 使用组织访问令牌登录 Docker。

       ```console
       $ docker login --username <your_organization_name>
       ```

       当提示输入密码时，粘贴您生成的组织访问令牌。

   3. 将您的本地 Docker 环境连接到组织的 Docker Scout 服务。

       ```console
       $ docker scout enroll <your_organization_name>
       ```

5. 索引现有镜像。您只需执行一次此操作。

    运行 `docker scout watch` 并使用 `--all-images` 选项索引指定 Artifactory 仓库中的所有镜像。以下是示例命令：

   ```console
   $ docker scout watch --registry \
   "type=artifactory,registry=example.jfrog.io,api=https://example.jfrog.io/artifactory,include=*/frontend*,exclude=*/dta/*,repository=docker-local,port=9000,subdomain-mode=true" \
   --all-images
   ```

6. 通过 [Scout 仪表板](https://scout.docker.com/) 确认镜像已被索引。

7. 配置 Artifactory 回调。

   在您的 Artifactory UI 中或通过 REST API，为镜像推送/更新事件配置 webhook。将端点设置为您的 `docker scout watch` 主机和端口，并包含 `DOCKER_SCOUT_ARTIFACTORY_WEBHOOK_SECRET` 用于身份验证。

   更多信息，请参阅 [JFrog Artifactory Webhooks 文档](https://jfrog.com/help/r/jfrog-platform-administration-documentation/webhooks) 或 [JFrog Artifactory REST API Webhooks 文档](https://jfrog.com/help/r/jfrog-rest-apis/webhooks)。

8. 持续监视新镜像或更新的镜像。

   运行 `docker scout watch` 并使用 `--refresh-registry` 选项监视要索引的新镜像。以下是示例命令：

   ```console
   $ docker scout watch --registry \
   "type=artifactory,registry=example.jfrog.io,api=https://example.jfrog.io/artifactory,include=*/frontend*,exclude=*/dta/*,repository=docker-local,port=9000,subdomain-mode=true" \
   --refresh-registry
   ```

9. 可选。设置 Scout 集成，以便从流行的协作平台接收实时通知。详情请参阅 [将 Docker Scout 与 Slack 集成](../team-collaboration/slack.md)。