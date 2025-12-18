---
title: '镜像 Docker Hardened Image 仓库 <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>'
linktitle: 镜像仓库
description: 了解如何将镜像镜像到组织的命名空间，以及如何选择性地推送到另一个私有注册表。
weight: 20
keywords: 镜像 docker 镜像, 私有容器注册表, docker hub 自动化, webhook 镜像同步, 安全镜像分发, 内部注册表, jfrog artifactory, harbor 注册表, amazon ecr, google artifact registry, github 容器注册表
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

镜像功能需要 DHI Enterprise 订阅。没有 DHI Enterprise 订阅，你可以直接从 `dhi.io` 拉取 Docker Hardened Images，无需镜像。有了 DHI Enterprise 订阅，你必须通过镜像来获得：

- 合规变体（启用 FIPS 或准备 STIG 的镜像）
- 扩展生命周期支持（ELS）变体（需要附加组件）
- 镜像或 Helm 图表的自定义
- 离线或受限网络环境
- SLA 支持的安全更新

## 如何镜像

本主题涵盖 Docker Hardened Image (DHI) 仓库的两种镜像类型：

- [镜像到 Docker Hub](#mirror-a-dhi-repository-to-docker-hub)：将 DHI 仓库镜像到 Docker Hub 上组织的命名空间。这需要 DHI Enterprise 订阅，用于[自定义镜像或图表](./customize.md)，并访问合规变体和 ELS 变体（需要附加组件）。这必须通过 Docker Hub 网页界面完成。

- [镜像到第三方注册表](#mirror-a-dhi-repository-to-a-third-party-registry)：将仓库镜像到另一个容器注册表，例如 Amazon ECR、Google Artifact Registry 或私有的 Harbor 实例。

## 镜像 DHI 仓库到 Docker Hub

将仓库镜像到 Docker Hub 需要 DHI Enterprise 订阅，并启用对合规变体、扩展生命周期支持（ELS）变体（需要附加组件）和自定义功能的访问：

- 镜像仓库：镜像允许你通过添加包、OCI 工件（如自定义证书或其他工具）、环境变量、标签和其他配置设置来自定义镜像。更多详情，请参见[自定义 Docker Hardened Image](./customize.md#customize-a-docker-hardened-image)。

- 图表仓库：镜像允许你自定义图表内的镜像引用。当你使用自定义镜像或将镜像镜像到第三方注册表并需要图表引用这些自定义位置时，这特别有用。更多详情，请参见[自定义 Docker Hardened Helm 图表](./customize.md#customize-a-docker-hardened-helm-chart)。

只有组织所有者才能执行镜像。一旦镜像完成，仓库将出现在你组织的仓库列表中，前缀为 `dhi-`。它将继续接收更新的镜像。

要镜像 Docker Hardened Image 仓库：

1. 访问 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择你的组织。
4. 选择 **Hardened Images** > **Catalog**。
5. 选择一个 DHI 仓库查看其详细信息。
6. 镜像仓库：
    - 要镜像镜像仓库，选择 **Use this image** > **Mirror repository**，然后按照屏幕上的说明操作。如果你有 ELS 附加组件，还可以选择 **Enable support for end-of-life versions**。
    - 要镜像 Helm 图表仓库，选择 **Get Helm chart**，然后按照屏幕上的说明操作。

所有标签完成镜像可能需要几分钟时间。

镜像仓库后，仓库将出现在你组织的仓库列表中，前缀为 `dhi-`。它将继续接收更新的镜像。

镜像后，仓库在 Docker Hub 上像任何其他私有仓库一样工作，你现在可以自定义它。要了解有关自定义的更多信息，请参见[自定义 Docker Hardened Image 或图表](./customize.md)。

### 用于同步和警报的 Webhook 集成

为了保持外部注册表或系统与你镜像的 Docker Hardened Images 同步，并在更新发生时接收通知，你可以在 Docker Hub 上的镜像仓库上配置[webhook](/docker-hub/repos/manage/webhooks/)。每当推送或更新新镜像标签时，webhook 会向你定义的 URL 发送 `POST` 请求。

例如，你可能配置一个 webhook 调用 CI/CD 系统的 `https://ci.example.com/hooks/dhi-sync`，每当新标签被镜像时。此 webhook 触发的自动化可以从 Docker Hub 拉取更新的镜像并推送到内部注册表，如 Amazon ECR、Google Artifact Registry 或 GitHub Container Registry。

其他常见的 webhook 用例包括：

- 触发验证或漏洞扫描工作流
- 签名或提升镜像
- 向下游系统发送通知

#### 示例 webhook 载荷

当触发 webhook 时，Docker Hub 发送如下 JSON 载荷：

```json
{
  "callback_url": "https://registry.hub.docker.com/u/exampleorg/dhi-python/hook/abc123/",
  "push_data": {
    "pushed_at": 1712345678,
    "pusher": "trustedbuilder",
    "tag": "3.13-alpine3.21"
  },
  "repository": {
    "name": "dhi-python",
    "namespace": "exampleorg",
    "repo_name": "exampleorg/dhi-python",
    "repo_url": "https://hub.docker.com/r/exampleorg/dhi-python",
    "is_private": true,
    "status": "Active",
    ...
  }
}
```

### 停止镜像仓库

只有组织所有者才能停止镜像仓库。停止镜像后，仓库仍然存在，但将不再接收更新。你仍然可以使用最后镜像的镜像或图表，但仓库将不会从原始仓库接收新标签或更新。

> [!NOTE]
>
> 如果你只想停止镜像 ELS 版本，可以在镜像仓库的 **Settings** 选项卡中取消选中 ELS 选项。更多详情，请参见[为仓库禁用 ELS](./els.md#disable-els-for-a-repository)。

要停止镜像仓库：

1. 访问 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择你有 DHI 访问权限的组织。
4. 选择 **Hardened Images** > **Manage**。
5. 选择 **Mirrored Images** 或 **Mirrored Helm charts** 选项卡。
6. 在要停止镜像的仓库的最右侧列中，选择菜单图标。
7. 选择 **Stop mirroring**。

## 镜像 DHI 仓库到第三方注册表

你可以选择将 DHI 仓库镜像到另一个容器注册表，例如 Amazon ECR、Google Artifact Registry、GitHub Container Registry 或私有的 Harbor 实例。

你可以使用任何标准工作流来镜像镜像，例如 [Docker CLI](/reference/cli/docker/_index.md)、[Docker Hub Registry API](/reference/api/registry/latest/)、第三方注册表工具或 CI/CD 自动化。

但是，为了保留完整的安全上下文，包括证明，你必须同时镜像其关联的 OCI 工件。DHI 仓库将镜像层存储在 `dhi.io`（或自定义镜像的 `docker.io`）上，而签名的证明存储在单独的注册表中（`registry.scout.docker.com`）。

要复制两者，你可以使用 [`regctl`](https://regclient.org/cli/regctl/)，这是一个支持镜像镜像及其附加工件（如 SBOM、漏洞报告和 SLSA 来源）的 OCI 感知 CLI。对于持续同步，你可以使用 [`regsync`](https://regclient.org/cli/regsync/)。

### 使用 `regctl` 镜像示例

以下示例展示如何使用 `regctl` 将 Docker Hardened Image 的特定标签从 Docker Hub 镜像到另一个注册表，同时保留其关联的证明。你必须先[安装 `regctl`](https://github.com/regclient/regclient)。

示例假设你已将 DHI 仓库镜像到 Docker Hub 上组织的命名空间，如前一节所述。你可以通过更新 `SRC_ATT_REPO` 和 `SRC_REPO` 变量来对非镜像镜像应用相同步骤。

1. 为你的特定环境设置环境变量。将占位符替换为你的实际值。

   在此示例中，你使用 Docker 用户名来表示 DHI 仓库被镜像到的 Docker Hub 组织的成员。为具有 `read only` 访问权限的用户准备一个[个人访问令牌 (PAT)](../../security/access-tokens.md)。或者，你可以使用组织命名空间和[组织访问令牌 (OAT)](../../enterprise/security/access-tokens.md) 登录 Docker Hub，但 OAT 尚不支持 `registry.scout.docker.com`。

   ```console
   $ export DOCKER_USERNAME="YOUR_DOCKER_USERNAME"
   $ export DOCKER_PAT="YOUR_DOCKER_PAT"
   $ export DOCKER_ORG="YOUR_DOCKER_ORG"
   $ export DEST_REG="registry.example.com"
   $ export DEST_REPO="mirror/dhi-python"
   $ export DEST_REG_USERNAME="YOUR_DESTINATION_REGISTRY_USERNAME"
   $ export DEST_REG_TOKEN="YOUR_DESTINATION_REGISTRY_TOKEN"
   $ export SRC_REPO="docker.io/${DOCKER_ORG}/dhi-python"
   $ export SRC_ATT_REPO="registry.scout.docker.com/${DOCKER_ORG}/dhi-python"
   $ export TAG="3.13-alpine3.21"
   ```

2. 通过 `regctl` 登录 Docker Hub、包含证明的 Scout 注册表以及你的目标注册表。

   ```console
   $ echo $DOCKER_PAT | regctl registry login -u "$DOCKER_USERNAME" --pass-stdin docker.io
   $ echo $DOCKER_PAT | regctl registry login -u "$DOCKER_USERNAME" --pass-stdin registry.scout.docker.com
   $ echo $DEST_REG_TOKEN | regctl registry login -u "$DEST_REG_USERNAME" --pass-stdin "$DEST_REG"
   ```

3. 使用 `--referrers` 和引用端点镜像镜像和证明：

   ```console
   $ regctl image copy \
        "${SRC_REPO}:${TAG}" \
        "${DEST_REG}/${DEST_REPO}:${TAG}" \
        --referrers \
        --referrers-src "${SRC_ATT_REPO}" \
        --referrers-tgt "${DEST_REG}/${DEST_REPO}" \
        --force-recursive
   ```

4. 验证工件是否已保留。

   首先，获取特定标签和平台的摘要。例如，`linux/amd64`。

   ```console
   DIGEST="$(regctl manifest head "${DEST_REG}/${DEST_REPO}:${TAG}" --platform linux/amd64)"
   ```

   列出附加的工件（SBOM、来源、VEX、漏洞报告）。

   ```console
   $ regctl artifact list "${DEST_REG}/${DEST_REPO}@${DIGEST}"
   ```

   或者，使用 `docker scout` 列出附加的工件。

   ```console
   $ docker scout attest list "registry://${DEST_REG}/${DEST_REPO}@${DIGEST}"
   ```

### 使用 `regsync` 持续镜像示例

`regsync` 自动从 Docker Hub 上组织的镜像 DHI 仓库拉取并推送到外部注册表，包括证明。它读取 YAML 配置文件并可以过滤标签。

以下示例使用 `regsync.yaml` 文件同步 Node 24 和 Python 3.12 Debian 13 变体，排除 Alpine 和 Debian 12。

```yaml{title="regsync.yaml"}
version: 1
# 可选：如果不想依赖之前的 CLI 登录，可以内联凭据
# creds:
#   - registry: docker.io
#     user: <your-docker-username>
#     pass: "{{file \"/run/secrets/docker_token\"}}"
#   - registry: registry.scout.docker.com
#     user: <your-docker-username>
#     pass: "{{file \"/run/secrets/docker_token\"}}"
#   - registry: registry.example.com
#     user: <service-user>
#     pass: "{{file \"/run/secrets/dest_token\"}}"

sync:
  - source: docker.io/<your-org>/dhi-node
    target: registry.example.com/mirror/dhi-node
    type: repository
    fastCopy: true
    referrers: true
    referrerSource: registry.scout.docker.com/<your-org>/dhi-node
    referrerTarget: registry.example.com/mirror/dhi-node
    tags:
      allow: [ "24.*" ]
      deny: [ ".*alpine.*", ".*debian12.*" ]

  - source: docker.io/<your-org>/dhi-python
    target: registry.example.com/mirror/dhi-python
    type: repository
    fastCopy: true
    referrers: true
    referrerSource: registry.scout.docker.com/<your-org>/dhi-python
    referrerTarget: registry.example.com/mirror/dhi-python
    tags:
      allow: [ "3.12.*" ]
      deny: [ ".*alpine.*", ".*debian12.*" ]
```

要使用配置文件进行试运行，你可以运行以下命令。你必须先[安装 `regsync`](https://github.com/regclient/regclient)。

```console
$ regsync check -c regsync.yaml
```

要使用配置文件运行同步：

```console
$ regsync once -c regsync.yaml
```

## 接下来

镜像后，请参见[拉取 DHI](./use.md#pull-a-dhi)以了解如何拉取和使用镜像的镜像。