---
title: 自定义 Docker 加固镜像或 Helm chart <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>
url: /dhi/how-to/customize/
parent:
  title: 操作指南
  url: /dhi/how-to/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Hardened Images
    url: /dhi/
  - title: 操作指南
    url: /dhi/how-to/
  - title: 自定义 Docker 加固镜像或 Helm chart <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>
    url: /dhi/how-to/customize/
next:
  title: 镜像 Docker Hardened Image 仓库 <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>
  url: /dhi/how-to/mirror/
prev:
  title: 使用 Docker Hardened Image
  url: /dhi/how-to/use/
---




当您拥有 Docker 加固镜像订阅时，可以通过 Docker Hub 网页界面自定义 Docker 加固镜像（DHI）和 chart，以满足您的特定需求。对于镜像，您可以选择基础镜像、添加软件包、添加 OCI 制品（例如自定义证书或额外工具）以及配置设置。对于 chart，您可以自定义镜像引用。

您的自定义内容会自动保持安全。当基础 Docker 加固镜像或 chart 收到安全补丁，或您的 OCI 制品更新时，Docker 会在后台自动重建您的自定义内容。这确保了默认情况下持续合规和保护，无需手动操作。重建的制品会按照与基础镜像和 chart 相同的 SLSA Build Level 3 标准进行签名和验证，确保供应链安全可靠且可验证。

## 自定义 Docker 加固镜像

要向您的组织添加自定义的 Docker 加固镜像，组织所有者必须首先将 DHI 仓库[镜像](./mirror.md)到 Docker Hub 上的您的组织中。一旦仓库被镜像，任何有权访问镜像 DHI 仓库的用户都可以创建自定义镜像。

### 创建镜像自定义

要自定义 Docker 加固镜像，请按照以下步骤操作：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub**。
1. 在命名空间下拉菜单中，选择拥有镜像 DHI 仓库的组织。
1. 选择 **Hardened Images** > **Manage** > **Mirrored Images**。
1. 对于您要自定义的镜像 DHI 仓库，选择最右侧列中的菜单图标。
1. 选择 **Customize**。

   此时，屏幕上的说明将引导您完成自定义过程。您可以继续执行以下步骤以获取更多详细信息。

1. 选择您要自定义的镜像版本。
1. 可选：添加软件包。

   1. 在 **Packages** 下拉菜单中，选择要添加到镜像中的软件包。

      下拉菜单中可用的软件包是所选镜像变体的操作系统系统软件包。例如，如果您正在自定义 Python DHI 的 Alpine 变体，列表将包括所有 Alpine 系统软件包。

   1. 在 **OCI artifacts** 下拉菜单中，首先选择包含 OCI 制品镜像的仓库。然后，从该仓库中选择要使用的标签。最后，指定要从 OCI 制品镜像中包含的具体路径。

      OCI 制品是您先前构建并推送到与镜像 DHI 相同命名空间仓库中的镜像。例如，您可以添加自定义根 CA 证书，或另一个包含您所需工具的镜像（例如向 Node.js 镜像添加 Python）。有关如何创建 OCI 制品镜像的更多详细信息，请参阅[为镜像自定义创建 OCI 制品镜像](#create-an-oci-artifact-image-for-image-customization)。

      当合并包含相同路径目录和文件的镜像时，列表中靠后的镜像将覆盖前面镜像中的文件。要管理此情况，您必须选择要从每个 OCI 制品镜像中包含和（可选）排除的路径。这使您可以控制在最终自定义镜像中包含哪些文件。

      默认情况下，不会从 OCI 制品镜像中包含任何文件。您必须明确包含所需的路径。包含路径后，您可以明确排除其下的文件或目录。

      > [!NOTE]
      >
      > 当运行时必需的文件被 OCI 制品覆盖时，镜像构建仍会成功，但在运行镜像时可能会遇到问题。

   1. 在 **Scripts** 部分，您可以添加、编辑或删除脚本。

      脚本允许您向容器镜像添加文件，这些文件可以在运行时访问。它们在构建过程中不会执行。这对于需要启动前初始化的服务非常有用，例如设置脚本或向 `/var/lock` 或 `/out` 等目录写入文件。

      您必须指定以下内容：

      - 脚本将被放置的路径
      - 脚本内容
      - 脚本的 UID 和 GID 所有权
      - 脚本的八进制文件权限

1. 选择 **Next: Configure** 以配置以下镜像设置：

   1. 指定镜像将包含的[环境变量](/reference/dockerfile/#env)及其值。
   1. 向镜像添加[标签](/reference/dockerfile/#label)。
   1. 向镜像添加[注解](/build/metadata/annotations/)。
   1. 指定要添加到镜像中的用户。
   1. 指定要添加到镜像中的用户组。
   1. 选择以哪个[用户](/reference/dockerfile/#user)身份运行镜像。
   1. 向镜像添加 [`ENTRYPOINT`](/reference/dockerfile/#entrypoint) 参数。这些参数会附加到基础镜像的入口点。
   1. 向镜像添加 [`CMD`](/reference/dockerfile/#cmd) 参数。这些参数会附加到基础镜像的命令。
   1. 覆盖镜像的默认（`/`）[工作目录](/reference/dockerfile/#workdir)。
   1. 为自定义名称指定一个后缀，该后缀会附加到自定义镜像的标签中。例如，如果您在自定义 `dhi-python:3.13` 镜像时指定 `custom`，则自定义镜像将被标记为 `dhi-python:3.13_custom`。
   1. 选择要为镜像构建的平台。您必须至少选择一个平台。

1. 选择 **Next: Review customization**。

1. 选择 **Create Customization**。

   将显示自定义摘要。镜像构建可能需要一些时间。构建完成后，它将出现在仓库的 **Tags** 选项卡中，您的团队成员可以像拉取任何其他镜像一样拉取它。

### 为镜像自定义创建 OCI 制品镜像

OCI 制品镜像是一个 Docker 镜像，其中包含您要包含在自定义 Docker 加固镜像（DHI）中的文件或目录。这可以包括额外的工具、库或配置文件。

创建用作 OCI 制品的镜像时，理想情况下应尽可能最小化，并且仅包含必要的文件。

例如，要将自定义根 CA 证书作为受信任 CA 捆绑包的一部分分发，您可以使用多阶段构建。这种方法会将您的证书注册到系统中并输出更新的 CA 捆绑包，可以将其提取到最小的最终镜像中：

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

您可以遵循此模式创建其他 OCI 制品，例如包含您要包含在自定义 DHI 中的工具或库的镜像。在第一阶段安装必要的工具或库，然后将相关文件复制到使用 `FROM scratch` 的最终阶段。这确保您的 OCI 制品最小化，并且仅包含必要的文件。

为了使 OCI 制品在 DHI 自定义中可用，必须将其构建并推送到与镜像 DHI 仓库相同命名空间中的仓库。

如果您正在为多个平台（例如 `linux/amd64` 和 `linux/arm64`）自定义 DHI，请使用 `--platform` 标志为所有平台构建 OCI 制品：

```console
$ docker buildx build --platform linux/amd64,linux/arm64 \
  -t <your-namespace>/my-oci-artifact:latest \
  --push .
```

这会创建一个单一镜像清单，您可以将其用于每个平台。自定义构建系统在构建每个自定义镜像时会自动选择正确的平台变体。

> [!IMPORTANT]
>
> 自定义 UI 仅允许您选择所有已添加 OCI 制品中可用的平台。如果任何 OCI 制品中缺少某个平台，您将无法为该自定义选择该平台。

一旦推送到您组织命名空间中的仓库，当您选择要添加到自定义 Docker 加固镜像的 OCI 制品时，OCI 制品会自动出现在自定义工作流中。

#### OCI 制品最佳实践

为 DHI 自定义创建 OCI 制品时，请遵循以下最佳实践：

- 使用多阶段构建：在构建器阶段构建或安装依赖项，然后仅将必要的文件复制到 `FROM scratch` 最终阶段。这可以保持 OCI 制品最小化，并且不包含不必要的构建工具。

- 仅包含必需文件：OCI 制品应仅包含您需要添加到自定义镜像中的文件。避免包含包管理器、shell 或其他在最终镜像中不会使用的实用程序。

- 匹配目标平台：为您计划在自定义中使用的所有平台构建 OCI 制品。在需要时使用 `docker buildx build --platform` 创建多平台镜像。

- 使用特定标签：使用特定版本或日期（如 `v1.0` 或 `20250101`）标记您的 OCI 制品，而不是仅依赖 `latest`。这可以确保可重现的构建，并使跟踪哪些制品用于哪些自定义更加容易。

- 启用不可变标签：考虑为您的 OCI 制品仓库启用[不可变标签](../../docker-hub/repos/manage/hub-images/immutable-tags.md)。这可以防止意外覆盖，并确保您的 OCI 制品每个版本保持不变，从而提高自定义的可重现性和可靠性。

## 自定义 DHI Helm chart

您可以自定义 DHI Helm chart 以满足您组织的特定需求。通过 Docker Hub 网页界面，您可以修改镜像引用以引用您创建的镜像镜像或自定义镜像。这使您可以创建一个自定义的、安全构建的 chart，其中包含对存储在 Docker Hub 或其他私有仓库中镜像的引用。默认情况下，DHI 会安全地打包引用您仓库的自定义 Helm chart，无论它们存储在哪里。

要自定义镜像引用，组织所有者必须将 DHI chart 仓库[镜像](./mirror.md)到 Docker Hub 上的您的组织中。

每个 Helm chart 仓库只能创建一个 chart 自定义。这与镜像自定义不同，后者每个仓库可以创建多个自定义。如果您需要进行更改，可以编辑现有自定义。或者，您可以再次镜像相同的 Helm chart 仓库，并向新镜像添加新的自定义。

> [!NOTE]
>
> 您可以使用标准 Helm 工具和做法（例如 `values.yaml` 文件）在 Docker Hub 外部自定义 Docker 加固镜像 chart，就像任何其他 Helm chart 一样。以下说明描述了如何使用 Docker Hub 网页界面自定义 chart 的镜像引用。

要在镜像后自定义 Docker 加固镜像 Helm chart：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub**。
1. 在命名空间下拉菜单中，选择拥有镜像 DHI 仓库的组织。
1. 选择 **Hardened Images** > **Manage** > **Mirrored Helm charts**。
1. 对于您要自定义的镜像 DHI 仓库，选择 **Name**。
1. 选择 **Customizations** 选项卡。
1. 选择 **Create customization**。

   此时，屏幕上的说明将引导您完成自定义过程。

## 编辑或删除自定义

要编辑或删除 DHI 或 chart 自定义，请按照以下步骤操作：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择拥有镜像仓库的组织。
4. 选择 **Hardened Images** > **Manage**。
5. 选择 **Customizations**。

6. 对于您要管理的自定义 DHI 仓库，选择最右侧列中的菜单图标。从这里，您可以：

   - **Edit**：编辑自定义。
   - **Create new**：基于源仓库创建新的自定义。
   - **Delete**：删除自定义。

7. 按照屏幕上的说明完成编辑或删除。
