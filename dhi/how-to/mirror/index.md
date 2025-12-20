# 镜像 Docker Hardened Image 仓库 <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Subscription:</span>
        
          <span>Docker Hardened Images Enterprise</span>
          <span class="icon-svg">
            
            
              <svg 
  class="w-5 h-5 text-gray-800 dark:text-white"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
  xmlns="http://www.w3.org/2000/svg"
  focusable="false"
  aria-hidden="true"
>
<path d="M18.1639 21.6147V18.6147M18.1639 18.6147V15.6147M18.1639 18.6147H15.1639M18.1639 18.6147H21.1639M19.8692 13.3281C19.9541 12.8974 20 12.4544 20 11.9999V7.21747C20 6.41796 20 6.0182 19.8692 5.67457C19.7537 5.37101 19.566 5.10015 19.3223 4.8854C19.0465 4.64231 18.6722 4.50195 17.9236 4.22122L12.5618 2.21054C12.3539 2.13258 12.25 2.0936 12.143 2.07815C12.0482 2.06444 11.9518 2.06444 11.857 2.07815C11.75 2.0936 11.6461 2.13258 11.4382 2.21054L6.0764 4.22122C5.3278 4.50195 4.9535 4.64231 4.67766 4.8854C4.43398 5.10015 4.24627 5.37101 4.13076 5.67457C4 6.0182 4 6.41796 4 7.21747V11.9999C4 16.9083 9.35396 20.4783 11.302 21.6147C11.5234 21.7439 11.6341 21.8085 11.7903 21.842C11.9116 21.868 12.0884 21.868 12.2097 21.842C12.3659 21.8085 12.4766 21.7439 12.698 21.6147C12.986 21.4467 13.3484 21.2255 13.757 20.9547M14.517 9.70865C14.517 10.4365 14.2081 11.0922 13.7143 11.5517C13.5354 11.7181 13.446 11.8013 13.4126 11.8658C13.3774 11.9337 13.3672 11.9737 13.3656 12.0501C13.364 12.1227 13.3936 12.2115 13.4528 12.3891L14.2225 14.6983C14.322 14.9966 14.3717 15.1458 14.3419 15.2645C14.3158 15.3684 14.2509 15.4584 14.1606 15.516C14.0574 15.5818 13.9002 15.5818 13.5858 15.5818H10.4142C10.0998 15.5818 9.94255 15.5818 9.83936 15.516C9.74903 15.4584 9.68416 15.3684 9.65807 15.2645C9.62826 15.1458 9.67797 14.9966 9.7774 14.6983L10.5472 12.3891C10.6063 12.2115 10.6359 12.1227 10.6344 12.0501C10.6328 11.9737 10.6226 11.9337 10.5874 11.8658C10.5539 11.8013 10.4645 11.7181 10.2857 11.5517C9.79182 11.0922 9.48291 10.4365 9.48291 9.70865C9.48291 8.31852 10.6098 7.19159 12 7.19159C13.3901 7.19159 14.517 8.31852 14.517 9.70865Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
            
          </span>
        
      </div>
    

    

    

    
  </div>



镜像需要 DHI Enterprise 订阅。如果没有 DHI Enterprise 订阅，您可以直接从 `dhi.io` 拉取 Docker Hardened Images，无需镜像。拥有 DHI Enterprise 订阅后，您必须进行镜像才能获得：

- 合规变体（启用 FIPS 或准备 STIG 的镜像）
- 扩展生命周期支持 (ELS) 变体（需要附加组件）
- 镜像或 Helm chart 自定义
- 气隙或受限网络环境
- 支持 SLA 的安全更新

## 如何镜像

本主题涵盖 Docker Hardened Image (DHI) 仓库的两种镜像类型：

- [镜像到 Docker Hub](#mirror-a-dhi-repository-to-docker-hub)：将 DHI 仓库镜像到您在 Docker Hub 上的组织命名空间。这需要 DHI Enterprise 订阅，用于[自定义镜像或 chart](./customize.md) 以及访问合规变体和 ELS 变体（需要附加组件）。这必须通过 Docker Hub Web 界面完成。

- [镜像到第三方注册中心](#mirror-a-dhi-repository-to-a-third-party-registry)：将仓库镜像到另一个容器注册中心，例如 Amazon ECR、Google Artifact Registry 或私有 Harbor 实例。

## 将 DHI 仓库镜像到 Docker Hub

将仓库镜像到 Docker Hub 需要 DHI Enterprise 订阅，并支持访问合规变体、扩展生命周期支持 (ELS) 变体（需要附加组件）以及自定义功能：

- **镜像仓库**：镜像允许您通过添加软件包、OCI 工件（例如自定义证书或附加工具）、环境变量、标签和其他配置设置来自定义镜像。更多详情，请参阅[自定义 Docker Hardened Image](./customize.md#customize-a-docker-hardened-image)。

- **Chart 仓库**：镜像允许您自定义 chart 中的镜像引用。这在使用自定义镜像或将镜像镜像到第三方注册中心并需要 chart 引用这些自定义位置时特别有用。更多详情，请参阅[自定义 Docker Hardened Helm chart](./customize.md#customize-a-docker-hardened-helm-chart)。

只有组织所有者可以执行镜像。镜像完成后，仓库将出现在您组织的命名空间中，您可以根据需要对其进行自定义。

要镜像 Docker Hardened Image 仓库：

1. 访问 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Hardened Images** > **Catalog**。
5. 选择一个 DHI 仓库以查看其详细信息。
6. 镜像仓库：
    - 要镜像镜像仓库，请选择 **Use this image** > **Mirror repository**，然后按照屏幕上的说明操作。如果您有 ELS 附加组件，还可以选择 **Enable support for end-of-life versions**。
    - 要镜像 Helm chart 仓库，请选择 **Get Helm chart**，然后按照屏幕上的说明操作。

所有标签完成镜像可能需要几分钟时间。

镜像仓库后，该仓库将出现在您组织的仓库列表中，前缀为 `dhi-`。它将继续接收更新的镜像。

镜像后，该仓库的工作方式与 Docker Hub 上的任何其他私有仓库相同，您现在可以对其进行自定义。要了解有关自定义的更多信息，请参阅[自定义 Docker Hardened Image 或 chart](./customize.md)。

### 用于同步和警报的 Webhook 集成

为了使外部注册中心或系统与您镜像的 Docker Hardened Images 保持同步，并在更新发生时接收通知，您可以在 Docker Hub 中的镜像仓库上配置 [webhook](/docker-hub/repos/manage/webhooks/)。Webhook 会在推送或更新新的镜像标签时向您定义的 URL 发送 `POST` 请求。

例如，您可以配置一个 webhook，在镜像新标签时调用 `https://ci.example.com/hooks/dhi-sync` 处的 CI/CD 系统。此 webhook 触发的自动化可以从 Docker Hub 拉取更新的镜像，并将其推送到内部注册中心，例如 Amazon ECR、Google Artifact Registry 或 GitHub Container Registry。

其他常见的 webhook 用例包括：

- 触发验证或漏洞扫描工作流
- 签名或提升镜像
- 向下游系统发送通知

#### Webhook 有效负载示例

当 webhook 被触发时，Docker Hub 会发送如下所示的 JSON 有效负载：

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

只有组织所有者可以停止镜像仓库。停止镜像后，仓库仍然存在，但将不再接收更新。您仍然可以使用最后镜像的镜像或 chart，但该仓库将不会从原始仓库接收新的标签或更新。

> [!NOTE]
>
> 如果您只想停止镜像 ELS 版本，可以在镜像仓库的 **Settings** 选项卡中取消选中 ELS 选项。更多详情，请参阅[为仓库禁用 ELS](./els.md#disable-els-for-a-repository)。

要停止镜像仓库：

1. 访问 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择有权访问 DHI 的组织。
4. 选择 **Hardened Images** > **Manage**。
5. 选择 **Mirrored Images** 或 **Mirrored Helm charts** 选项卡。
6. 在要停止镜像的仓库的最右侧列中，选择菜单图标。
7. 选择 **Stop mirroring**。

## 将 DHI 仓库镜像到第三方注册中心

您可以选择将 DHI 仓库镜像到另一个容器注册中心，例如 Amazon ECR、Google Artifact Registry、GitHub Container Registry 或私有 Harbor 实例。

您可以使用任何标准工作流来镜像镜像，例如 [Docker CLI](/reference/cli/docker/_index.md)、[Docker Hub Registry API](/reference/api/registry/latest/)、第三方注册中心工具或 CI/CD 自动化。

但是，为了保留完整的安全上下文（包括证明），您还必须镜像其关联的 OCI 工件。DHI 仓库将镜像层存储在 `dhi.io`（或自定义镜像的 `docker.io`）上，并将签名的证明存储在单独的注册中心 (`registry.scout.docker.com`) 中。

要复制两者，您可以使用 [`regctl`](https://regclient.org/cli/regctl/)，这是一个支持镜像镜像以及附加工件（如 SBOM、漏洞报告和 SLSA 证明）的 OCI 感知 CLI。对于持续同步，您可以使用 [`regsync`](https://regclient/regcli/regsync/)。

### 使用 `regctl` 进行镜像的示例

以下示例展示了如何使用 `regctl` 将 Docker Hardened Image 的特定标签从 Docker Hub 镜像到另一个注册中心，并附带其关联的证明。您必须首先[安装 `regctl`](https://github.com/regclient/regclient)。

该示例假设您已如前一节所述，将 DHI 仓库镜像到您在 Docker Hub 上的组织命名空间。您可以通过相应地更新 `SRC_ATT_REPO` 和 `SRC_REPO` 变量，将相同的步骤应用于非镜像镜像。

1. 为您的特定环境设置环境变量。将占位符替换为您的实际值。

   在此示例中，您使用 Docker 用户名来表示镜像 DHI 仓库的 Docker Hub 组织的成员。准备一个具有 `read only` 访问权限的[个人访问令牌 (PAT)](../../security/access-tokens.md)。或者，您可以使用组织命名空间和[组织访问令牌 (OAT)](../../enterprise/security/access-tokens.md) 登录 Docker Hub，但 OAT 尚未支持 `registry.scout.docker.com`。

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

2. 通过 `regctl` 登录到 Docker Hub、包含证明的 Scout 注册中心以及您的目标注册中心。

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

```yaml{title="regsync.yaml"}
version: 1
# 可选：如果不依赖先前的 CLI 登录，可以内联凭证
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
