---
title: 使用 Docker 加固镜像（DHI）Helm chart
linktitle: 使用 Helm chart
description: 了解如何使用 Docker 加固镜像（DHI）Helm chart。
keywords: 使用加固镜像, helm, k8s, kubernetes, dhi chart, chart
weight: 32
---

Docker 加固镜像（Docker Hardened Image，简称 DHI）chart 是由 Docker 提供的 [Helm chart](https://helm.sh/docs/)，基于上游源码构建，专为与 Docker 加固镜像兼容而设计。这些 chart 以 OCI 制品的形式在 Docker Hub 上的 DHI 目录中提供。更多详情，请参阅 [Docker 加固镜像 chart](/dhi/features/helm/)。

DHI chart 集成了多层供应链安全保障，这些保障在上游 chart 中并不存在：

- **SLSA 3 级合规性**：每个 chart 均按照 SLSA Build Level 3 标准构建，包含详细的构建来源信息
- **软件物料清单（SBOM）**：全面的 SBOM 详细列出了 chart 中引用的所有组件
- **加密签名**：所有相关元数据均由 Docker 进行加密签名，确保完整性和真实性
- **加固配置**：Chart 自动引用 Docker 加固镜像，以实现安全部署
- **兼容性测试**：Chart 经过严格测试，可开箱即用，与 Docker 加固镜像完美配合

您可以像使用存储在 OCI 注册表中的其他 Helm chart 一样使用 DHI chart。当您拥有 Docker 加固镜像订阅时，还可以自定义 DHI chart，使其引用自定义镜像和镜像仓库。定制化的 chart 构建流水线可确保您的定制内容安全构建，使用最新的基础 chart，并包含证明信息。

## 查找 Docker Helm chart

要查找适用于 DHI 的 Docker Helm chart，请执行以下操作：

1. 访问 [Docker Hub](https://hub.docker.com/hardened-images/catalog) 中的“加固镜像”目录并登录。
2. 在左侧边栏中，选择 **Hardened Images** > **Catalog**。
3. 选择 **Filter by** 下的 **Helm Charts**。
4. 选择一个 Helm chart 仓库以查看其详细信息。

## 将 Helm chart 及其镜像镜像到第三方注册表

如果您希望将 chart 和/或其镜像镜像到您自己的第三方注册表，可以按照 [镜像 Docker 加固镜像仓库](/dhi/how-to/mirror/) 中的说明进行操作，镜像 chart、镜像或两者。

用于镜像容器镜像的 `regctl` 工具也可用于镜像 Helm chart，因为 Helm chart 是 OCI 制品。

例如：

```console
regctl image copy \
    "${SRC_CHART_REPO}:${TAG}" \
    "${DEST_REG}/${DEST_CHART_REPO}:${TAG}" \
    --referrers \
    --referrers-src "${SRC_ATT_REPO}" \
    --referrers-tgt "${DEST_REG}/${DEST_CHART_REPO}" \
    --force-recursive
```

## 创建用于拉取镜像的 Kubernetes secret

您需要创建一个 Kubernetes secret，用于从 `dhi.io`、Docker Hub 或您自己的注册表拉取镜像。这是必要的，因为 Docker 加固镜像仓库需要身份验证。即使您将镜像镜像到您自己的注册表，如果该注册表需要身份验证，您仍然需要创建此 secret。

1. 对于 `dhi.io` 或 Docker Hub，请使用您的 Docker 账户创建一个 [个人访问令牌（PAT）](/security/access-tokens/) 或 [组织访问令牌（OAT）](/enterprise/security/access-tokens/)。确保该令牌至少具有对 Docker 加固镜像仓库的只读访问权限。
2. 使用以下命令在 Kubernetes 中创建一个 secret。将 `<your-secret-name>`、`<your-username>`、`<your-personal-access-token>` 和 `<your-email>` 替换为您自己的值。

   > [!NOTE]
   >
   > 您需要在每个使用 DHI 的 Kubernetes 命名空间中创建此 secret。如果您已将 DHI 镜像到另一个注册表，请将 `dhi.io` 替换为您的注册表主机名。将 `<your-username>`、`<your-access-token>` 和 `<your-email>` 替换为您自己的值。如果使用 PAT，`<your-username>` 为 Docker ID；如果使用 OAT，则为您的组织名称。`<your-secret-name>` 是您为 secret 选择的名称。

   ```console
   $ kubectl create secret docker-registry <your-secret-name> \
       --docker-server=dhi.io \
       --docker-username=<your-username> \
       --docker-password=<your-access-token> \
       --docker-email=<your-email>
   ```

   例如：

    ```console
    $ kubectl create secret docker-registry dhi-pull-secret \
        --docker-server=dhi.io \
        --docker-username=docs \
        --docker-password=dckr_pat_12345 \
        --docker-email=moby@example.com
   ```

## 安装 Helm chart

要从 Docker 加固镜像安装 Helm chart，请执行以下操作：

1. 使用 Helm 登录到注册表：

   ```console
   $ echo $ACCESS_TOKEN | helm registry login dhi.io --username <your-username> --password-stdin
   ```

    替换 `<your-username>` 并设置 `$ACCESS_TOKEN`。

2. 使用 `helm install` 安装 chart。您也可以使用 `--dry-run` 标志来测试安装，而无需实际安装任何内容。

   ```console
   $ helm install <release-name> oci://dhi.io/<helm-chart-repository> --version <chart-version> \
     --set "imagePullSecrets[0].name=<your-secret-name>"
   ```

   相应地替换 `<helm-chart-repository>` 和 `<chart-version>`。如果 chart 位于您自己的注册表或其他仓库中，请将 `dhi.io/<helm-chart-repository>` 替换为您自己的位置。将 `<your-secret-name>` 替换为从 [创建用于拉取镜像的 Kubernetes secret](#create-a-kubernetes-secret-for-pulling-images) 创建的镜像拉取 secret 的名称。

## 自定义 Helm chart

您可以自定义 Docker 加固镜像 Helm chart，以引用自定义镜像和镜像仓库。更多详情，请参阅 [自定义 Docker 加固镜像和 chart](./customize.md)。

## 验证 Helm chart 并查看其证明

您可以验证 Helm chart。更多详情，请参阅 [验证 Helm chart 证明](./verify.md#verify-helm-chart-attestations-with-docker-scout)。