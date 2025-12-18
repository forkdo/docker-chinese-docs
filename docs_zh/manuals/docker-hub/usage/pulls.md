---
description: 了解 Docker Hub 的拉取使用情况和限制。
keywords: Docker Hub, 拉取, 使用, 限制
title: Docker Hub 拉取使用情况和限制
linkTitle: 拉取
weight: 10
aliases:
  - /docker-hub/usage/storage/
  - /docker-hub/usage/repositories/
---

Docker Personal 用户和未认证用户在 Docker Hub 上会受到 6 小时拉取速率限制。
相比之下，Docker Pro、Team 和 Business 用户享有无限制的拉取速率。

根据您的订阅类型，适用以下拉取使用情况和限制，需遵守公平使用原则：

| 用户类型                | 每 6 小时拉取速率限制             |
|--------------------------|-----------------------------------------|
| Business（已认证） | 无限制                               |
| Team（已认证）     | 无限制                               |
| Pro（已认证）      | 无限制                               |
| Personal（已认证） | 200                                     |
| 未认证用户    | 每个 IPv4 地址或 IPv6 /64 子网 100 次 |

## 拉取定义

拉取定义如下：

 - 一次 Docker 拉取包括版本检查以及拉取过程中发生的任何下载。
   根据客户端的不同，`docker pull` 可以通过执行版本检查来验证镜像或标签的存在，而无需下载。
 - 版本检查不计入使用量计费。
 - 拉取普通镜像会为 [单个清单](https://github.com/opencontainers/image-spec/blob/main/manifest.md) 计为一次拉取。
 - 拉取多架构镜像将为每个不同架构计为一次拉取。

## 拉取归属

已认证用户的拉取可以归属到个人或 [组织命名空间](/manuals/accounts/general-faqs.md#whats-an-organization-name-or-namespace)。

归属基于以下规则：

- 私有拉取：私有仓库的拉取归属到仓库命名空间的所有者。
- 公共拉取：从公共仓库拉取镜像时，归属基于域名关联和组织成员身份确定。
- 已验证域名所有权：当从链接到已验证域名的账户拉取镜像时，归属设置为该
  [域名](/manuals/enterprise/security/single-sign-on/faqs/domain-faqs.md) 的所有者。
- 单个组织成员身份：
   - 如果已验证域名的所有者是公司，且用户在该
     [公司](../../admin/faqs/company-faqs.md#what-features-are-supported-at-the-company-level) 内仅属于一个组织，
     拉取归属到该特定组织。
   - 如果用户仅属于一个组织，拉取归属到该特定组织。
- 多个组织成员身份：如果用户在公司内属于多个组织，
  拉取归属到用户的个人命名空间。

### 认证

为确保拉取正确归属，您必须使用 Docker Hub 进行认证。以下部分提供有关如何登录 Docker Hub 以认证拉取的信息。

#### Docker Desktop

如果您使用 Docker Desktop，可以从 Docker Desktop 菜单登录 Docker Hub。

从 Docker Desktop 菜单中选择 **Sign in / Create Docker ID**，并按照屏幕说明完成登录过程。

#### Docker Engine

如果您使用独立版本的 Docker Engine，请从终端运行 `docker login` 命令以认证 Docker Hub。有关命令使用信息，请参阅 [docker login](/reference/cli/docker/login.md)。

#### Docker Swarm

如果您运行 Docker Swarm，必须使用 `--with-registry-auth` 标志认证 Docker Hub。更多信息请参阅 [创建服务](/reference/cli/docker/service/create.md#with-registry-auth)。如果您使用 Docker Compose 文件部署应用栈，请参阅 [docker stack deploy](/reference/cli/docker/stack/deploy.md)。

#### GitHub Actions

如果您使用 GitHub Actions 构建并推送 Docker 镜像到 Docker Hub，请参阅 [login action](https://github.com/docker/login-action#dockerhub)。如果您使用其他 Action，必须以类似方式添加用户名和访问令牌进行认证。

#### Kubernetes

如果您运行 Kubernetes，请按照 [从私有仓库拉取镜像](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/) 的说明进行认证。

#### 第三方平台

如果您使用任何第三方平台，请遵循提供商关于使用注册表认证的说明。

> [!NOTE]
>
> 通过第三方平台拉取镜像时，平台可能使用相同的
> IPv4 地址或 IPv6 /64 子网为多个用户拉取镜像。即使您已认证，归属到单个 IPv4 地址或 IPv6 /64 子网的拉取仍可能导致 [滥用速率限制](./_index.md#abuse-rate-limit)。

- [Artifactory](https://www.jfrog.com/confluence/display/JFROG/Advanced+Settings#AdvancedSettings-RemoteCredentials)
- [AWS CodeBuild](https://aws.amazon.com/blogs/devops/how-to-use-docker-images-from-a-private-registry-in-aws-codebuild-for-your-build-environment/)
- [AWS ECS/Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/private-auth.html)
- [Azure Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops&tabs=yaml#sep-docreg)
- [Chipper CI](https://docs.chipperci.com/builds/docker/#rate-limit-auth)
- [CircleCI](https://circleci.com/docs/2.0/private-images/)
- [Codefresh](https://codefresh.io/docs/docs/docker-registries/external-docker-registries/docker-hub/)
- [Drone.io](https://docs.drone.io/pipeline/docker/syntax/images/#pulling-private-images)
- [GitLab](https://docs.gitlab.com/ee/user/packages/container_registry/#authenticate-with-the-container-registry)
- [LayerCI](https://layerci.com/docs/advanced-workflows#logging-in-to-docker)
- [TeamCity](https://www.jetbrains.com/help/teamcity/integrating-teamcity-with-docker.html#Conforming+with+Docker+download+rate+limits)

## 查看月度拉取和包含的使用量

您可以在 Docker Hub 的 [使用量页面](https://hub.docker.com/usage/pulls) 查看月度拉取情况。

在该页面上，您还可以发送报告到您的邮箱，报告包含以下详细信息的逗号分隔文件。

| CSV 列           | 定义                                                                                                                                                                                                         | 使用指导                                                                                                                                                                      |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `datehour`           | 导致数据传输的拉取日期和小时（`yyyy/mm/dd/hh`）。                                                                                                                                                        | 这有助于识别高峰使用时间和模式。                                                                                                                            |
| `user_name`          | 拉取镜像的 Docker ID                                                                                                                                                                    | 这让组织所有者能够跟踪每个用户的消耗数据，有效管理资源。                                                                                     |
| `repository`         | 被拉取镜像的仓库名称。                                                                                                                                                           | 这让您识别哪些仓库最常被访问并消耗最多数据传输。                                                                       |
| `access_token_name`  | 用于与 Docker CLI 认证的访问令牌名称。`generated` 令牌由 Docker 客户端在用户登录时自动生成。                                               | 个人访问令牌通常用于认证自动化工具（Docker Desktop、CI/CD 工具等）。这对于识别哪个自动化系统发出的拉取很有用。 |
| `ips`                | 用于拉取镜像的 IP 地址。此字段已聚合，因此可能显示多个 IP 地址，代表同一日期和小时内用于拉取镜像的所有 IP 地址。                    | 这有助于您了解数据传输的来源，对诊断和识别自动化或手动拉取模式很有用。                                    |
| `repository_privacy` | 被拉取镜像仓库的隐私状态。可以是 `public` 或 `private`。                                                                                                               | 这区分了公共和私有仓库，以识别拉取影响哪个数据传输阈值。                                                              |
| `tag`                | 镜像的标签。仅当拉取包含标签时才提供此标签。                                                                                                                                       | 这有助于识别镜像。标签通常用于标识镜像的特定版本或变体。                                                                     |
| `digest`             | 镜像的唯一摘要。                                                                                                                                                                             | 这有助于识别镜像。                                                                                                                                                |
| `version_checks`     | 在每个镜像仓库的日期和小时内累积的版本检查次数。根据客户端的不同，拉取可以执行版本检查以验证镜像或标签的存在，而无需下载。 | 这有助于识别版本检查的频率，可用于分析使用趋势和潜在的意外行为。                                                  |
| `pulls`              | 在每个镜像仓库的日期和小时内累积的拉取次数。                                                                                                                                            | 这有助于识别仓库拉取的频率，可用于分析使用趋势和潜在的意外行为。                                                |

## 查看拉取速率和限制

拉取速率限制基于 6 小时计算。付费订阅用户或自动化系统在 Docker Hub 上没有拉取速率限制。未认证和 Docker Personal 用户在 Docker Hub 上拉取镜像时会遇到速率限制。

当您发出拉取请求且超过限制时，Docker Hub 在请求清单时返回 `429` 响应代码和以下正文：

```text
You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limits
```

此错误消息显示在 Docker CLI 或 Docker Engine 日志中。

要查看当前拉取速率和限制：

> [!NOTE]
>
> 要检查您的限制，您需要安装 `curl`、`grep` 和 `jq`。

1. 获取令牌。

   - 如果您匿名拉取，请匿名获取令牌：

      ```console
      $ TOKEN=$(curl "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
      ```

   - 如果您已认证，请在以下命令中插入您的用户名和密码：

      ```console
      $ TOKEN=$(curl --user 'username:password' "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
      ```

2. 获取包含您限制的头部。这些头部在 GET 和 HEAD 请求中都会返回。使用 GET 会模拟真实的拉取并计入限制。使用 HEAD 则不会。

   ```console
   $ curl --head -H "Authorization: Bearer $TOKEN" https://registry-1.docker.io/v2/ratelimitpreview/test/manifests/latest
   ```

3. 检查头部。您应该看到以下头部：

   ```text
   ratelimit-limit: 100;w=21600
   ratelimit-remaining: 20;w=21600
   docker-ratelimit-source: 192.0.2.1
   ```

   在前面的示例中，拉取限制是每 21600 秒（6 小时）100 次拉取，剩余 20 次拉取。

   如果您没有看到任何 `ratelimit` 头部，可能是因为镜像或您的 IP 与发布者、提供商或开源组织有合作关系，因此无限制。这也可能意味着您拉取的用户属于付费 Docker 订阅。如果您没有看到这些头部，拉取该镜像不会计入拉取速率限制。