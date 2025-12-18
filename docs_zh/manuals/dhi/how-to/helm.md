---
title: 使用 Docker Hardened Image 图表
linktitle: 使用 Helm 图表
description: 了解如何使用 Docker Hardened Image 图表。
keywords: 使用加固镜像, helm, k8s, kubernetes, dhi 图表, 图表
weight: 32
---

Docker Hardened Image (DHI) 图表是 Docker 提供的 [Helm 图表](https://helm.sh/docs/)，基于上游源代码构建，专为与 Docker Hardened Images 兼容而设计。这些图表作为 OCI 工件存储在 Docker Hub 上的 DHI 目录中。更多详细信息，请参阅 [Docker Hardened Image 图表](/dhi/features/helm/)。

DHI 图表整合了多层供应链安全特性，这些特性在上游图表中并不存在：

- SLSA 3 级合规性：每个图表均按照 SLSA Build Level 3 标准构建，包含详细的构建来源信息
- 软件物料清单 (SBOM)：全面的 SBOM 详细列出图表中引用的所有组件
- 密码学签名：所有相关元数据均由 Docker 进行密码学签名，确保完整性和真实性
- 加固配置：图表自动引用 Docker Hardened Images 以实现安全部署
- 测试兼容性：图表经过充分测试，可与 Docker Hardened Images 开箱即用

您可以像使用任何存储在 OCI 注册表中的其他 Helm 图表一样使用 DHI 图表。当您拥有 Docker Hardened Images 订阅时，还可以自定义 DHI 图表以引用自定义镜像和镜像仓库。自定义图表构建流水线确保您的自定义内容能够安全构建，使用最新的基础图表，并包含证明信息。

## 查找 Docker Helm 图表

要在 DHI 中查找 Docker Helm 图表：

1. 访问 [Docker Hub](https://hub.docker.com/hardened-images/catalog) 中的 Hardened Images 目录并登录。
2. 在左侧边栏中，选择 **Hardened Images** > **Catalog**。
3. 选择 **Filter by** 中的 **Helm Charts**。
4. 选择一个 Helm 图表仓库以查看其详细信息。

## 将 Helm 图表和/或其镜像镜像到第三方注册表

如果您想将图表镜像到自己的第三方注册表，可以按照 [镜像 Docker Hardened Image 仓库](/dhi/how-to/mirror/) 中的说明，对图表、镜像或两者都进行镜像。

用于镜像容器镜像的相同 `regctl` 工具也可用于镜像 Helm 图表，因为 Helm 图表也是 OCI 工件。

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

## 为拉取镜像创建 Kubernetes 密钥

您需要创建一个 Kubernetes 密钥，以便从 `dhi.io`、Docker Hub 或您自己的注册表拉取镜像。这是必要的，因为 Docker Hardened Image 仓库需要身份验证。如果您将镜像镜像到自己的注册表，如果注册表需要身份验证，仍然需要创建此密钥。

1. 对于 `dhi.io` 或 Docker Hub，请使用您的 Docker 账户创建一个 [个人访问令牌 (PAT)](/security/access-tokens/)，或使用 [组织访问令牌 (OAT)](/enterprise/security/access-tokens/)。确保令牌至少对 Docker Hardened Image 仓库具有只读访问权限。
2. 使用以下命令在 Kubernetes 中创建密钥。将 `<your-secret-name>`、`<your-username>`、`<your-personal-access-token>` 和 `<your-email>` 替换为您自己的值。

   > [!NOTE]
   >
   > 您需要在使用 DHI 的每个 Kubernetes 命名空间中创建此密钥。如果您已将 DHI 镜像到另一个注册表，请将 `dhi.io` 替换为您的注册表主机名。将 `<your-username>`、`<your-access-token>` 和 `<your-email>` 替换为您自己的值。`<your-username>` 如果使用 PAT 则为 Docker ID，如果使用 OAT 则为您的组织名称。`<your-secret-name>` 是您为密钥选择的名称。

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

## 安装 Helm 图表

要从 Docker Hardened Images 安装 Helm 图表：

1. 使用 Helm 登录注册表：

   ```console
   $ echo $ACCESS_TOKEN | helm registry login dhi.io --username <your-username> --password-stdin
   ```

    将 `<your-username>` 替换为您的值，并设置 `$ACCESS_TOKEN`。

2. 使用 `helm install` 安装图表。您也可以选择使用 `--dry-run` 标志来测试安装，而不实际安装任何内容。

   ```console
   $ helm install <release-name> oci://dhi.io/<helm-chart-repository> --version <chart-version> \
     --set "imagePullSecrets[0].name=<your-secret-name>"
   ```

   相应地替换 `<helm-chart-repository>` 和 `<chart-version>`。如果图表在您自己的注册表或其他仓库中，请将 `dhi.io/<helm-chart-repository>` 替换为您自己的位置。将 `<your-secret-name>` 替换为从 [为拉取镜像创建 Kubernetes 密钥](#create-a-kubernetes-secret-for-pulling-images) 创建的镜像拉取密钥的名称。

## 自定义 Helm 图表

您可以自定义 Docker Hardened Image Helm 图表，以引用自定义镜像和镜像仓库。更多详细信息，请参阅 [自定义 Docker Hardened Images 和图表](./customize.md)。

## 验证 Helm 图表并查看其证明

您可以验证 Helm 图表。更多详细信息，请参阅 [验证 Helm 图表证明](./verify.md#verify-helm-chart-attestations-with-docker-scout)。