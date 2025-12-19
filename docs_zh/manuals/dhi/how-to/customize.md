---
title: '自定义 Docker 强化镜像或图表 <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>'
linkTitle: 自定义镜像或图表
weight: 25
keywords: hardened images, DHI, customize, certificate, artifact, helm chart
description: 了解如何自定义 Docker 强化镜像 (DHI) 和图表。
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

当您拥有 Docker 强化镜像 (Docker Hardened Images) 订阅时，您可以使用 Docker Hub Web 界面自定义 Docker 强化镜像 (DHI) 和图表以满足您的特定需求。对于镜像，这允许您选择基础镜像、添加软件包、添加 OCI 工件（如自定义证书或附加工具）以及配置设置。对于图表，这允许您自定义镜像引用。

您的自定义会自动保持安全。当基础 Docker 强化镜像或图表收到安全补丁，或者您的 OCI 工件更新时，Docker 会在后台自动重新构建您的自定义内容。这确保了默认情况下的持续合规性和保护，无需手动操作。重新构建的工件经过签名和证明，符合与基础镜像和图表相同的 SLSA 构建级别 3 标准，确保了安全且可验证的供应链。

## 自定义 Docker 强化镜像

要将自定义的 Docker 强化镜像添加到您的组织，组织所有者必须首先将 DHI 仓库[镜像](./mirror.md)到您在 Docker Hub 上的组织。仓库镜像完成后，任何有权访问镜像 DHI 仓库的用户都可以创建自定义镜像。

### 创建镜像自定义

要自定义 Docker 强化镜像，请按照以下步骤操作：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择拥有镜像 DHI 仓库的组织。
4. 选择 **Hardened Images** > **Manage** > **Mirrored Images**。
5. 对于您要自定义的镜像 DHI 仓库，选择最右侧列中的菜单图标。
6. 选择 **Customize**。

   此时，屏幕上的说明将引导您完成自定义过程。您可以继续执行以下步骤以获取更多详细信息。

7. 选择您要自定义的镜像版本。
8. **可选**。添加软件包。

   1. 在 **Packages** 下拉菜单中，选择要添加到镜像中的软件包。

      下拉菜单中可用的软件包是所选镜像变体的 OS 系统软件包。例如，如果您正在自定义 Python DHI 的 Alpine 变体，该列表将包含所有 Alpine 系统软件包。

   2. 在 **OCI artifacts** 下拉菜单中，首先选择包含 OCI 工件镜像的仓库。然后，从该仓库中选择您要使用的标签。最后，指定您想从 OCI 工件镜像中包含的特定路径。

      OCI 工件是您之前构建并推送到与镜像 DHI 相同命名空间的仓库中的镜像。例如，您可以添加自定义根 CA 证书或包含您所需工具（如将 Python 添加到 Node.js 镜像中）的另一个镜像。有关如何创建 OCI 工件镜像的更多详细信息，请参阅[为镜像自定义创建 OCI 工件镜像](#create-an-oci-artifact-image-for-image-customization)。

      当组合包含相同路径的目录和文件的镜像时，列表中靠后的镜像将覆盖靠前镜像中的文件。为了管理这一点，您必须选择要包含的路径，并可选择性地从每个 OCI 工件镜像中排除某些路径。这允许您控制最终自定义镜像中包含哪些文件。

      默认情况下，不会包含 OCI 工件镜像中的任何文件。您必须显式包含您想要的路径。包含路径后，您可以显式排除其下的文件或目录。

      > [!NOTE]
      >
      > 当运行时所需的文件被 OCI 工件覆盖时，镜像构建仍会成功，但在运行镜像时可能会遇到问题。

   3. 在 **Scripts** 部分，您可以添加、编辑或删除脚本。

      脚本允许您将文件添加到容器镜像中，以便在运行时访问。它们在构建过程中不会执行。这对于需要启动前初始化的服务非常有用，例如设置脚本或写入 `/var/lock` 或 `/out` 等目录的文件。

      您必须指定以下内容：

      - 脚本将放置的路径
      - 脚本内容
      - 脚本的 UID 和 GID 所有权
      - 脚本的八进制文件权限

9. 选择 **Next: Configure** 以配置以下镜像设置：

   1. 指定镜像将包含的[环境变量](/reference/dockerfile/#env)及其值。
   2. 向镜像添加[标签](/reference/dockerfile/#label)。
   3. 向镜像添加[注解](/build/metadata/annotations/)。
   4. 指定要添加到镜像的用户。
   5. 指定要添加到镜像的用户组。
   6. 选择运行镜像时使用的[用户](/reference/dockerfile/#user)。
   7. 向镜像添加 [`ENTRYPOINT`](/reference/dockerfile/#entrypoint) 参数。这些参数会附加到基础镜像的 entrypoint。
   8. 向镜像添加 [`CMD`](/reference/dockerfile/#cmd) 参数。这些参数会附加到基础镜像的命令。
   9. 指定一个后缀，用于附加到自定义镜像的标签上。例如，如果您在自定义 `dhi-python:3.13` 镜像时指定 `custom`，则自定义镜像将被标记为 `dhi-python:3.13_custom`。
   10. 选择您要构建镜像的平台。您必须至少选择一个平台。

10. 选择 **Next: Review customization**。
11. 选择 **Create Customization**。

    将出现自定义的摘要。镜像构建可能需要一些时间。构建完成后，它将出现在仓库的 **Tags** 选项卡中，您的团队成员可以像拉取任何其他镜像一样拉取它。

### 为镜像自定义创建 OCI 工件镜像

OCI 工件镜像是一个 Docker 镜像，包含您想包含在自定义 Docker 强化镜像 (DHI) 中的文件或目录。这可以包括附加的工具、库或配置文件。

在创建用作 OCI 工件的镜像时，理想情况下应尽可能精简，并且只包含必要的文件。

例如，要分发自定义根 CA 证书作为受信任 CA 捆绑包的一部分，您可以使用多阶段构建。这种方法将您的证书注册到系统，并输出更新的 CA 捆绑包，该捆绑包可以提取到一个精简的最终镜像中：

```dockerfile
# syntax=docker/dockerfile:1

FROM dhi.io/bash:5-dev AS certs

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /usr/local/share/ca-certificates/my-rootca
COPY certs/rootCA.crt /usr/local/share/ca-certificates/my-rootca

RUN update-ca-certificates

FROM scratch
COPY --from=certs /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
```

您可以遵循此模式来创建其他 OCI 工件，例如包含您想包含在自定义 DHI 中的工具或库的镜像。在第一阶段安装必要的工具或库，然后将相关文件复制到使用 `FROM scratch` 的最终阶段。这确保了您的 OCI 工件是精简的，并且只包含必要的文件。

为了使 OCI 工件在 DHI 自定义中可用，必须将其构建并推送到与镜像 DHI 仓库相同命名空间的仓库中。

如果您正在为多个平台（如 `linux/amd64` 和 `linux/arm64`）自定义 DHI，请使用 `--platform` 标志为所有平台构建您的 OCI 工件：

```console
$ docker buildx build --platform linux/amd64,linux/arm64 \
  -t <your-namespace>/my-oci-artifact:latest \
  --push .
```

这会创建一个单一的镜像清单，您可以在每个平台上使用。自定义构建系统在构建每个自定义镜像时会自动选择正确的平台变体。

> [!IMPORTANT]
>
> 自定义 UI 只允许您选择在您添加的所有 OCI 工件中都可用的平台。如果任何 OCI 工件缺少某个平台，您将无法为您的自定义选择该平台。

一旦推送到您组织命名空间的仓库中，当您选择要添加到自定义 Docker 强化镜像的 OCI 工件时，OCI 工件会自动出现在自定义工作流程中。

#### OCI 工件的最佳实践

在为 DHI 自定义创建 OCI 工件时，请遵循以下最佳实践：

- **使用多阶段构建**：在构建阶段构建或安装依赖项，然后仅将必要的文件复制到 `FROM scratch` 的最终阶段。这使 OCI 工件保持精简，没有不必要的构建工具。
- **仅包含基本文件**：OCI 工件应仅包含您需要添加到自定义镜像中的文件。避免包含包管理器、shell 或其他在最终镜像中不会使用的实用程序。
- **匹配目标平台**：为您计划在自定义中使用的所有平台构建您的 OCI 工件。在需要时使用 `docker buildx build --platform` 来创建多平台镜像。
- **使用特定标签**：使用特定版本或日期（如 `v1.0` 或 `20250101`）标记您的 OCI 工件，而不是仅仅依赖 `latest`。这确保了可重现的构建，并使跟踪哪些工件用于哪些自定义变得更加容易。
- **启用不可变标签**：考虑为您的 OCI 工件仓库启用[不可变标签](../../docker-hub/repos/manage/hub-images/immutable-tags.md)。这可以防止意外覆盖，并确保您的 OCI 工件的每个版本保持不变，从而提高自定义的可重现性和可靠性。

## 自定义 DHI Helm 图表

您可以自定义 DHI Helm 图表以满足您组织的特定需求。通过 Docker Hub Web 界面，您可以修改镜像引用，以引用您创建的镜像或自定义镜像。这允许您创建一个自定义的、安全构建的图表，其中包含对存储在 Docker Hub 或其他私有注册表中的镜像的引用。DHI 默认会安全地打包自定义 Helm 图表，这些图表引用您的仓库，无论它们存储在哪里。

要自定义镜像引用，组织所有者必须将 DHI 图表仓库[镜像](./mirror.md)到您在 Docker Hub 上的组织。

您可以为每个 Helm 图表仓库创建一个图表自定义。这与镜像自定义不同，后者可以为每个仓库创建多个自定义。如果您需要进行更改，可以编辑现有的自定义。或者，您可以再次镜像相同的 Helm 图表仓库，并向新镜像添加新的自定义。

> [!NOTE]
>
> 您可以使用标准的 Helm 工具和实践（如 `values.yaml` 文件）在 Docker Hub 之外自定义 Docker 强化镜像图表，就像自定义任何其他 Helm 图表一样。以下说明描述了如何使用 Docker Hub Web 界面自定义图表的镜像引用。

镜像后自定义 Docker 强化镜像 Helm 图表：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择拥有镜像 DHI 仓库的组织。
4. 选择 **Hardened Images** > **Manage** > **Mirrored Helm charts**。
5. 对于您要自定义的镜像 DHI 仓库，选择 **Name**。
6. 选择 **Customizations** 选项卡。
7. 选择 **Create customization**。

   此时，屏幕上的说明将引导您完成自定义过程。

## 编辑或删除自定义

要编辑或删除 DHI 或图表自定义，请按照以下步骤操作：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择拥有镜像仓库的组织。
4. 选择 **Hardened Images** > **Manage**。
5. 选择 **Customizations**。
6. 对于您要管理的自定义 DHI 仓库，选择最右侧列中的菜单图标。
   从这里，您可以：
   - **Edit**：编辑自定义。
   - **Create new**：基于源仓库创建新的自定义。
   - **Delete**：删除自定义。
7. 按照屏幕上的说明完成编辑或删除。