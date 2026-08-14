# 镜像 Docker Hardened Image 仓库




镜像需要 DHI Select 或 Enterprise 订阅。如果没有订阅，您可以直接从 `dhi.io` 拉取 Docker Hardened Images，无需镜像。拥有 DHI Select 或 Enterprise 订阅后，您必须将仓库镜像到您的组织中才能获得：

- 合规变体（启用 FIPS 或准备 STIG 的镜像）
- 扩展生命周期支持 (ELS) 变体（需要附加组件）
- 镜像或 Helm chart 自定义
- 气隙或受限网络环境
- [SLA 支持的安全更新](https://docs.docker.com/go/dhi-sla/)

## 如何镜像

本主题涵盖 Docker Hardened Image (DHI) 仓库的两种镜像类型：

- [镜像到您的组织](#mirror-a-dhi-repository-to-your-organization)：将 DHI 仓库镜像到您在 Docker Hub 上的组织命名空间。

- [镜像到第三方注册中心](#mirror-a-dhi-repository-to-a-third-party-registry)：将仓库镜像到另一个容器注册中心，例如 Amazon ECR、Google Artifact Registry 或私有 Harbor 实例。

## 将 DHI 仓库镜像到您的组织

要镜像仓库，您必须是组织所有者或编辑者，或者使用个人访问令牌 (PAT) 或组织访问令牌 (OAT)。有关所需权限范围，请参阅以下各节中的 CLI 和 Terraform 选项卡。

- **镜像仓库**：镜像允许您通过添加软件包、OCI 工件（例如自定义证书或附加工具）、环境变量、标签和其他配置设置来自定义镜像。更多详情，请参阅[自定义 Docker Hardened Image](./customize.md#customize-a-docker-hardened-image)。

- **Chart 仓库**：镜像允许您自定义 chart 中的镜像引用。这在使用自定义镜像或将镜像镜像到第三方注册中心并需要 chart 引用这些自定义位置时特别有用。更多详情，请参阅[自定义 Docker Hardened Helm chart](./customize.md#customize-a-docker-hardened-helm-chart)。

**Docker Hub**



1. 访问 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Hardened Images** > **Catalog**。
5. 选择一个 DHI 仓库以查看其详细信息。
6. 镜像仓库：
    - 要镜像镜像仓库，请选择 **Use this image** > **Mirror repository**，然后按照屏幕上的说明操作。如果您有 ELS 附加组件，还可以选择 **Enable support for end-of-life versions**。
    - 要镜像 Helm chart 仓库，请选择 **Get Helm chart**，然后按照屏幕上的说明操作。

所有标签完成镜像可能需要几分钟时间。

**CLI**



使用您的 Docker 凭据、具有 **Read & Write** 权限的[个人访问令牌 (PAT)](../../security/access-tokens.md)，或[组织访问令牌 (OAT)](../../enterprise/security/access-tokens.md) 通过 `docker login` 进行身份验证。使用 OAT 时，可用操作取决于令牌的权限范围：

- 要列出已镜像的仓库，OAT 必须对相关仓库具有读取（pull）访问权限。结果限定在 OAT 可访问的仓库范围内。
- 要创建到现有目标仓库的镜像，OAT 必须对该仓库具有推送访问权限。要创建到尚不存在的新目标仓库的镜像，OAT 必须具有组织范围的仓库访问权限（例如，具有 pull 或 push 权限的 `<org>/*`）。对未来仓库名称的仓库范围访问是不够的。
- 要停止镜像，OAT 必须对相关仓库具有推送访问权限。
- 具有公共仓库只读访问权限的 OAT 无法列出或管理已镜像的仓库。

使用 [`docker dhi mirror`](/reference/cli/docker/dhi/mirror/) 命令：

```console
$ docker dhi mirror start --org my-org \
  dhi/golang,my-org/dhi-golang \
  dhi/nginx,my-org/dhi-nginx \
  dhi/prometheus-chart,my-org/dhi-prometheus-chart
```

带依赖项镜像：

```console
$ docker dhi mirror start --org my-org dhi/golang,my-org/dhi-golang --dependencies
```

列出您组织中的已镜像镜像：

```console
$ docker dhi mirror list --org my-org
```

按名称或类型筛选已镜像镜像：

```console
$ docker dhi mirror list --org my-org --filter python
$ docker dhi mirror list --org my-org --type image
$ docker dhi mirror list --org my-org --type helm-chart
```

**Terraform**



您可以使用 [DHI Terraform provider](/dhi/tools/terraform/) 将 DHI 镜像作为基础设施即代码进行管理。

为您要镜像的每个仓库定义一个 `dhi_mirror` 资源：

```hcl
resource "dhi_mirror" "golang" {
  source_namespace = "dhi"
  source_name      = "golang"
  destination_name = "dhi-golang"
}

resource "dhi_mirror" "nginx" {
  source_namespace = "dhi"
  source_name      = "nginx"
  destination_name = "dhi-nginx"
}
```

要启用扩展生命周期支持 (ELS) 变体，请设置 `els` 属性：

```hcl
resource "dhi_mirror" "golang" {
  source_namespace = "dhi"
  source_name      = "golang"
  destination_name = "dhi-golang"
  els              = true
}
```

运行 `terraform apply` 以创建镜像。

有关资源属性的完整列表，请参阅 [Terraform Registry 文档](https://registry.terraform.io/providers/docker-hardened-images/dhi/latest/docs/resources/mirror)。



镜像后，该仓库将出现在您组织的仓库列表中，前缀为 `dhi-`，并继续接收更新的镜像。它的行为类似于任何其他 Docker Hub 仓库，因此您可以管理访问和权限、配置 webhook 以及使用其他标准 Hub 功能。有关详细信息，请参阅 [Docker Hub 仓库](/manuals/docker-hub/repos/_index.md)。

### 停止镜像仓库

停止镜像后，仓库仍然存在，但不再接收更新。您仍然可以使用最后镜像的镜像或 chart。

> [!NOTE]
>
> 如果您只想停止镜像 ELS 版本，可以在镜像仓库的 **Settings** 选项卡中清除 ELS 选项。

**Docker Hub**



1. 访问 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择有权访问 DHI 的组织。
4. 选择 **Hardened Images** > **Manage**。
5. 选择 **Mirrored Images** 或 **Mirrored Helm charts** 选项卡。
6. 在要停止镜像的仓库的最右侧列中，选择菜单图标。
7. 选择 **Stop mirroring**。

**CLI**



使用您的 Docker 凭据、具有 **Read & Write** 权限的[个人访问令牌 (PAT)](../../security/access-tokens.md)，或对相关仓库具有推送访问权限的[组织访问令牌 (OAT)](../../enterprise/security/access-tokens.md)，通过 `docker login` 进行身份验证。

使用 [`docker dhi mirror`](/reference/cli/docker/dhi/mirror/) 命令：

```console
$ docker dhi mirror stop --org my-org dhi-golang
```

**Terraform**



要停止镜像，请从您的 Terraform 配置中移除 `dhi_mirror` 资源并运行 `terraform apply`。该仓库仍保留在您的组织中，但不再接收更新。



## 将 DHI 仓库镜像到第三方注册中心

在将 DHI 仓库镜像到您在 Docker Hub 上的组织之后，您可以选择将其镜像到另一个容器注册中心，例如 Amazon ECR、Google Artifact Registry、GitHub Container Registry 或私有 Harbor 实例。

您可以使用任何标准工作流来镜像镜像，例如 [Docker CLI](/reference/cli/docker/)、[Docker Hub Registry API](/reference/api/registry/latest/)、第三方注册中心工具或 CI/CD 自动化。

但是，为了保留完整的安全上下文（包括证明），您还必须镜像其关联的 OCI 工件。DHI 仓库将镜像层存储在 `dhi.io`（或自定义镜像的 `docker.io`）上，并将签名的证明存储在单独的注册中心 (`registry.scout.docker.com`) 中。

要复制两者，您可以使用 [`regctl`](https://regclient.org/cli/regctl/)，这是一个支持镜像镜像以及附加工件（如 SBOM、漏洞报告和 SLSA 证明）的 OCI 感知 CLI。对于持续同步，您可以使用 [`regsync`](https://regclient.org/cli/regsync/)。

### 使用 webhook 自动同步

为了使外部注册中心或系统与您镜像的 Docker Hardened Images 保持同步，并在更新发生时接收通知，您可以在 Docker Hub 中的镜像仓库上配置 [webhook](/docker-hub/repos/manage/webhooks/)。Webhook 会在推送或更新新的镜像标签时向您定义的 URL 发送 `POST` 请求。

例如，您可以配置一个 webhook，在镜像新标签时调用 `https://ci.example.com/hooks/dhi-sync` 处的 CI/CD 系统。此 webhook 触发的自动化可以从 Docker Hub 拉取更新的镜像，并将其推送到内部注册中心，例如 Amazon ECR、Google Artifact Registry 或 GitHub Container Registry。

其他常见的 webhook 用例包括：

- 触发验证或漏洞扫描工作流
- 签名或提升镜像
- 向下游系统发送通知

#### Webhook 有效负载示例

当 webhook 被触发时，Docker Hub 会发送如下所示的 JSON 有效负载：

```json{collapse=true}
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

### 使用 `regctl` 进行镜像的示例

以下示例展示了如何使用 `regctl` 将 Docker Hardened Image 的特定标签从 Docker Hub 镜像到另一个注册中心，并附带其关联的证明。您必须首先[安装 `regctl`](https://github.com/regclient/regclient)。

该示例假设您已如前一节所述，将 DHI 仓库镜像到您在 Docker Hub 上的组织命名空间。您可以通过相应地更新 `SRC_ATT_REPO` 和 `SRC_REPO` 变量，将相同的步骤应用于非镜像镜像。

1. 为您的特定环境设置环境变量。将占位符替换为您的实际值。

   在此示例中，您使用[组织访问令牌 (OAT)](../../enterprise/security/access-tokens.md) 以您的 Docker 组织身份进行身份验证。OAT 必须对您要镜像的每个 DHI 仓库至少具有 pull 访问权限。只有在令牌范围内的仓库才可访问。或者，您可以使用具有 `read only` 访问权限的[个人访问令牌 (PAT)](../../security/access-tokens.md) 以 Docker Hub 用户身份进行身份验证。

   > [!WARNING]
   >
   > 以下示例为了演示目的在命令行上直接导出凭据。这会在您的 shell 历史记录和进程列表中暴露敏感令牌。在生产环境中，请使用安全的方法，例如从受限权限的文件中读取、在运行时加载的环境文件，或密钥管理工具。

   ```console
   $ export DOCKER_ORG="YOUR_DOCKER_ORG"
   $ export DOCKER_OAT="YOUR_DOCKER_OAT"
   $ export DEST_REG="registry.example.com"
   $ export DEST_REPO="mirror/dhi-python"
   $ export DEST_REG_USERNAME="YOUR_DESTINATION_REGISTRY_USERNAME"
   $ export DEST_REG_TOKEN="YOUR_DESTINATION_REGISTRY_TOKEN"
   $ export SRC_REPO="docker.io/${DOCKER_ORG}/dhi-python"
   $ export SRC_ATT_REPO="registry.scout.docker.com/${DOCKER_ORG}/dhi-python"
   $ export TAG="3.13-alpine3.21"
   ```

2. 通过 `regctl` 登录到 Docker Hub、包含证明的 Scout 注册中心以及您的目标注册中心。

   ```console
   $ echo $DOCKER_OAT | regctl registry login -u "$DOCKER_ORG" --pass-stdin docker.io
   $ echo $DOCKER_OAT | regctl registry login -u "$DOCKER_ORG" --pass-stdin registry.scout.docker.com
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

   列出附加的工件（SBOM、证明、VEX、漏洞报告）。

   ```console
   $ regctl artifact list "${DEST_REG}/${DEST_REPO}@${DIGEST}"
   ```

   或者，使用 `docker scout` 列出附加的工件。

   ```console
   $ docker scout attest list "registry://${DEST_REG}/${DEST_REPO}@${DIGEST}"
   ```

### 使用 `regsync` 进行持续镜像的示例

`regsync` 可自动从您在 Docker Hub 上的组织镜像的 DHI 仓库拉取，并推送到您的外部注册中心，包括证明。它读取 YAML 配置文件并可以过滤标签。

以下示例使用 `regsync.yaml` 文件同步 Node 24 和 Python 3.12 Debian 13 变体，排除 Alpine 和 Debian 12。

```yaml{title="regsync.yaml",collapse=true}
version: 1
# 可选：如果不依赖先前的 CLI 登录，可以内联凭证
# creds:
#   - registry: docker.io
#     user: <your-docker-org>
#     pass: "{{file \"/run/secrets/docker_oat\"}}"
#   - registry: registry.scout.docker.com
#     user: <your-docker-org>
#     pass: "{{file \"/run/secrets/docker_oat\"}}"
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

要使用配置文件进行试运行，您可以运行以下命令。您必须首先[安装 `regsync`](https://github.com/regclient/regclient)。

```console
$ regsync check -c regsync.yaml
```

要使用配置文件运行同步：

```console
$ regsync once -c regsync.yaml
```

## 下一步

镜像后，请参阅[拉取 DHI](./use.md#pull-a-dhi) 以了解如何拉取和使用镜像镜像。

