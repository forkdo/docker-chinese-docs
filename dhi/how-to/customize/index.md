# 自定义 Docker Hardened Image 或 chart




当您拥有 DHI Select 或 DHI Enterprise 订阅时，可以通过 Docker Hub 网页界面自定义 Docker 加固镜像（DHI）和 chart，以满足您的特定需求。对于镜像，您可以选择基础镜像、添加软件包、添加 OCI 制品（例如自定义证书或额外工具）以及配置设置。对于 chart，您可以自定义镜像引用。

您的自定义内容会自动保持安全。当基础 Docker 加固镜像或 chart 收到安全补丁，或您的 OCI 制品更新时，Docker 会在后台自动重建您的自定义内容。这确保了默认情况下持续合规和保护，无需手动操作。重建的制品会按照与基础镜像和 chart 相同的 SLSA Build Level 3 标准进行签名和验证，确保供应链安全可靠且可验证。

## 自定义 Docker 加固镜像

要向您的组织添加自定义的 Docker 加固镜像，组织所有者必须首先将 DHI 仓库[镜像](./mirror.md)到 Docker Hub 上的您的组织中。一旦仓库被镜像，任何有权访问镜像 DHI 仓库的用户都可以创建自定义镜像。

您可以使用 DHI CLI 或 Docker Hub 网页界面创建自定义。

**Docker Hub**



1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **My Hub**。
1. 在命名空间下拉菜单中，选择拥有镜像 DHI 仓库的组织。
1. 选择 **Hardened Images** > **Manage** > **Mirrored Images**。
1. 对于您要自定义的镜像 DHI 仓库，选择最右侧列中的菜单图标。
1. 选择 **Customize**。

   此时，屏幕上的说明将引导您完成自定义过程。您可以继续执行以下步骤以获取更多详细信息。

1. 选择一个或多个您要自定义的镜像或 Helm chart 及其版本。

   当选择多个镜像和版本时，所有选择必须共享相同的发行版和发行版版本。例如，您可以将 `dhi-node:22_alpine3.23` 和 `dhi-python:3.13_alpine3.23` 一起选择（均为 Alpine 3.23），但您不能将 `dhi-node:22_debian` 与 Alpine 镜像混用，也不能混用不同的 Alpine 版本（如 `alpine3.23` 与 `alpine3.22`）。

   或者，您可以选择多个 Helm chart 版本，以将相同的自定义应用到所有版本。您不能在同一个自定义中混用镜像和 Helm chart。

1. 选择 **Next**。
1. 可选：添加软件包。

   1. 在 packages 下拉菜单中，选择要添加到镜像中的软件包。

      下拉菜单中可用的软件包是所选镜像变体的操作系统系统软件包。对于 3.23 及更高版本的 Alpine 基础镜像，这些是 Docker 从源代码构建、带有加密签名和完整供应链安全性的加固软件包。对于 3.22 版 Alpine 基础镜像和基于 Debian 的镜像，这些是标准系统软件包。

   1. 在 **OCI artifacts** 下拉菜单中，首先选择包含 OCI 制品镜像的仓库。然后，从该仓库中选择要使用的标签。最后，指定要从 OCI 制品镜像中包含的具体路径。

      OCI 制品是您先前构建并推送到与镜像 DHI 相同命名空间仓库中的镜像。例如，您可以添加自定义根 CA 证书，或另一个包含您所需工具的镜像（例如向 Node.js 镜像添加 Python）。

      您可以向单个自定义添加多个 OCI 制品镜像。当您添加多个时，它们按照您在 **OCI artifacts** 下拉菜单中添加的顺序应用。如果多个镜像包含相同路径的目录或文件，后添加的镜像会覆盖先添加镜像中的文件。要管理此情况，您必须选择要从每个 OCI 制品镜像中包含和（可选）排除的路径。这使您可以控制在最终自定义镜像中包含哪些文件。

      默认情况下，不会从 OCI 制品镜像中包含任何文件。您必须明确包含所需的路径。包含路径后，您可以明确排除其下的文件或目录。

      > [!NOTE]
      >
      > 当运行时必需的文件被 OCI 制品覆盖时，镜像构建仍会成功，但在运行镜像时可能会遇到问题。

      有关更多详细信息，请参阅 [OCI artifacts](#oci-artifacts)。

   1. 在 **Scripts** 部分，您可以添加、编辑或删除脚本。

      脚本允许您向容器镜像添加文件，这些文件可以在运行时访问。它们在构建过程中不会执行。这对于需要启动前初始化的服务非常有用，例如设置脚本或向 `/var/lock` 或 `/out` 等目录写入文件。

      您必须指定以下内容：

      - 脚本将被放置的路径
      - 脚本内容
      - 脚本的 UID 和 GID 所有权
      - 脚本的八进制文件权限

1. 选择 **Next: Configure** 以配置以下镜像设置：

   > [!NOTE]
   >
   > 当一次性自定义多个镜像时，其中许多配置选项默认受限，可能不可用。

   1. 指定镜像将包含的[环境变量](/reference/dockerfile/#env)及其值。
   1. 向镜像添加[标签](/reference/dockerfile/#label)。
   1. 向镜像添加[注解](/build/metadata/annotations/)。
   1. 指定要添加到镜像中的用户。当您添加用户时，会自动为该用户创建一个主目录，权限为 0755。
   1. 指定要添加到镜像中的用户组。
   1. 选择以哪个[用户](/reference/dockerfile/#user)身份运行镜像。
   1. 向镜像添加 [`ENTRYPOINT`](/reference/dockerfile/#entrypoint) 参数。这些参数会附加到基础镜像的入口点。
   1. 向镜像添加 [`CMD`](/reference/dockerfile/#cmd) 参数。这些参数会附加到基础镜像的命令。
   1. 覆盖镜像的默认（`/`）[工作目录](/reference/dockerfile/#workdir)。
   1. 为自定义名称指定一个后缀，该后缀会附加到自定义镜像的标签中。例如，如果您在自定义 `dhi-python:3.13` 镜像时指定 `custom`，则自定义镜像将被标记为 `dhi-python:3.13_custom`。
   1. 选择镜像层的压缩格式。您可以在 **ZSTD**（默认）或 **GZIP** 压缩之间选择。**ZSTD** 通常提供更快的镜像拉取和更好的压缩率，但可能与较旧的软件存在兼容性问题。如果您需要与较旧 Docker 版本的兼容性，请使用 **GZIP**。
   1. 选择要为镜像构建的平台。您必须至少选择一个平台。

1. 选择 **Next: Review customization**。

1. 选择 **Create Customization**。

   将显示自定义摘要。镜像构建可能需要一些时间。构建完成后，它将出现在仓库的 **Tags** 选项卡中，您的团队成员可以像拉取任何其他镜像一样拉取它。

**CLI**



使用您的 Docker 凭据或具有 **Read & Write** 权限的[个人访问令牌 (PAT)](../../security/access-tokens.md)，或[组织访问令牌 (OAT)](../../enterprise/security/access-tokens.md)，通过 `docker login` 进行身份验证。使用 OAT 时，可用操作取决于令牌的权限范围：

- 要列出或获取自定义、或查看构建日志，OAT 必须对目标仓库具有读取（pull）访问权限。结果限定在 OAT 可访问的仓库范围内。
- 要创建、更新或删除自定义，OAT 必须对目标仓库具有推送访问权限。批量操作需要对每个引用的目标仓库具有推送访问权限。

使用 [`docker dhi customization`](/reference/cli/docker/dhi/customization/) 命令：

```console
# 准备单个自定义脚手架
$ docker dhi customization prepare golang 1.25 \
  --org my-org \
  --destination my-org/dhi-golang \
  --name "golang with git" \
  > my-customization.yaml

# 准备批量自定义脚手架（通过 stdin 管道传入 JSON 数组）
$ echo '[{"destination":"my-org/dhi-golang","tag-definition-id":"golang/alpine-3.23/1.24-dev"}]' \
  | docker dhi customization prepare --name "golang with git" --org my-org \
  > my-customization.yaml

# 创建自定义
$ docker dhi customization create my-customization.yaml --org my-org

# 列出自定义
$ docker dhi customization list --org my-org

# 按名称、仓库或来源筛选自定义
$ docker dhi customization list --org my-org --filter git
$ docker dhi customization list --org my-org --repo dhi-golang
$ docker dhi customization list --org my-org --source golang

# 按 ID 获取自定义
$ docker dhi customization get <id> --org my-org

# 更新自定义
$ docker dhi customization edit my-customization.yaml --org my-org

# 按 ID 删除自定义
$ docker dhi customization delete <id> --org my-org

# 无需确认提示直接删除
$ docker dhi customization delete <id> --org my-org --force
```

有关所有 YAML 字段的完整参考，请参阅[镜像自定义 YAML 文件](#image-customization-yaml-file)。

**Terraform**



您可以使用 [DHI Terraform provider](/dhi/tools/terraform/) 将 DHI 自定义作为基础设施即代码进行管理。如果您尚未配置该 provider，请参阅 [DHI Terraform provider](/dhi/tools/terraform/) 获取设置说明。

为每个自定义定义一个 `dhi_customization` 资源：

```hcl
resource "dhi_customization" "golang_with_git" {
  repository = "dhi-golang"
  name       = "golang with git"

  contents {
    packages = ["git", "curl"]
  }

  platform {
    os           = "linux"
    architecture = "amd64"
  }
}
```

`dhi_customization` 资源还支持用于 `accounts`、`files`、`labels`、`annotations`、`environment`、`entrypoint`、`cmd`、`user`、`workdir` 和 `stop_signal` 的可选配置块。

运行 `terraform apply` 以创建自定义。

要编辑自定义，请更新资源配置并运行 `terraform apply`。要删除自定义，请移除该资源并运行 `terraform apply`。

有关资源属性的完整列表，请参阅 [Terraform Registry 文档](https://registry.terraform.io/providers/docker-hardened-images/dhi/latest/docs/resources/customization)。

> [!NOTE]
>
> 通过 Terraform provider 无法监控自定义构建。请使用 Docker Hub 网页界面或 DHI CLI 监控构建。



### 镜像自定义 YAML 文件

使用 CLI 时，自定义在 YAML 文件中定义。使用 `docker dhi customization prepare` 生成包含所有可用字段和注释示例的脚手架。编辑文件以描述您想要的内容，然后将其传递给 `docker dhi customization create`。

该文件有两部分：标识自定义及其目标的前言，以及指定要更改内容的配置节。

#### 关于 `id` 字段

`id` 字段在您运行 `docker dhi customization create` 时由 Docker Hub 自动分配。创建新自定义时，请完全省略 `id`。它是只读的。

要查找现有自定义的 ID，请运行：

```console
$ docker dhi customization list --org my-org
```

`id` 会显示在输出中，以及通过 `docker dhi customization get <id> --org my-org` 检索到的文件中。它使 `docker dhi customization edit` 能够识别要更新的自定义。`docker dhi customization prepare` 生成的脚手架不包含 `id`，这是预期的行为。

#### 设置目标

`name` 和 `targets` 字段在每个自定义文件中都是必填的。`targets` 数组指定自定义应用于哪些镜像版本。对单个镜像自定义使用单个条目，或对一次性将相同配置应用于多个镜像的批量自定义使用多个条目。

```yaml
name: golang with git

targets:
  - destination: my-org/dhi-golang
    tag_definition_id: golang/alpine-3.23/1.25
```

| 字段 | 描述 |
|:---|:---|
| `name` | 人类可读的名称。转换为小写并以连字符连接后，它会成为镜像标签后缀。例如，`golang with git` 生成的标签以 `_golang-with-git` 结尾。 |
| `targets[].destination` | Docker Hub 中的目标仓库，例如 `my-org/dhi-golang`。 |
| `targets[].tag_definition_id` | 要自定义的标签定义，例如 `golang/alpine-3.23/1.25`。使用带 tab 补全的 `docker dhi customization prepare` 查找有效值。 |

> [!NOTE]
>
> 当 `targets` 有多个条目时，不支持 `accounts`、`entrypoint` 和 `cmd` 字段。包含它们会导致 `docker dhi customization create` 返回错误。

#### 添加软件包

要在自定义镜像中安装额外的操作系统软件包，请在 `contents.packages` 下列出它们。可用的软件包取决于基础镜像变体。

```yaml
contents:
  packages:
    - git
    - curl
```

#### 添加 OCI 制品

要将额外文件（例如自定义证书、内部工具或配置文件）分层到自定义镜像中，请在 `contents.artifacts` 下列出 OCI 制品镜像。

```yaml
contents:
  artifacts:
    - name: my-org/my-certs:latest
      includes:
        - etc/ssl/certs
      excludes:
        - etc/ssl/certs/old
```

| 字段 | 描述 |
|:---|:---|
| `name` | OCI 制品的镜像引用。必须与镜像 DHI 位于同一 Docker Hub 命名空间中。 |
| `includes` | 要从制品复制的路径。默认不包含任何文件。您必须至少列出一个路径。 |
| `excludes` | 应用 `includes` 后要排除的路径。 |

要了解有关 OCI 制品的更多信息，包括如何创建它们、最佳实践以及环境变量的行为，请参阅 [OCI artifacts](#oci-artifacts)。

#### 向镜像注入文件

要在构建时添加静态文件（例如配置文件或启动脚本），请使用 `paths` 字段。文件作为静态内容添加，不会在构建期间执行。

```yaml
paths:
  - path: /etc/myconfig
    contents: |
      key=value
    mode: "0644"
    uid: 0
    gid: 0
```

| 字段 | 描述 |
|:---|:---|
| `path` | 文件将放置在镜像中的绝对路径。 |
| `contents` | 文件内容。对多行内容使用 YAML 块标量（`\|`）。 |
| `mode` | 八进制文件权限，例如 `"0644"`。将值加引号，以防止 YAML 将前导零视为八进制表示法。 |
| `uid` | 文件所有者的用户 ID。 |
| `gid` | 文件所有者的组 ID。 |

#### 配置用户账户

要向镜像添加用户或组，或更改容器以哪个用户运行，请使用 `accounts` 字段。

> [!NOTE]
>
> 批量自定义（多个 `targets`）不支持。

```yaml
accounts:
  root: true
  runs-as: nonroot
  users:
    - name: nonroot
      uid: 65532
      gid: 65532
  groups:
    - name: nonroot
      gid: 65532
      members:
        - nonroot
```

| 字段 | 描述 |
|:---|:---|
| `root` | 是否启用 root 用户。默认为 `false`。如果 `runs-as` 设置为 `root`，则必填。 |
| `runs-as` | 容器运行的默认用户。 |
| `users[].name` | 用户名。 |
| `users[].uid` | 用户 ID。 |
| `users[].gid` | 主组 ID。可选。 |
| `groups[].name` | 组名。 |
| `groups[].gid` | 组 ID。 |
| `groups[].members` | 要添加到此组的用户名。可选。 |

#### 设置环境变量

要向镜像添加或覆盖环境变量，请使用 `environment` 字段。这些变量会与基础镜像现有的环境变量合并，而不会替换它们。

```yaml
environment:
  MY_VAR: my_value
  DEBUG: "false"
```

对 YAML 解析器会解释为非字符串类型的值加引号，例如 `"false"`、`"0"` 和 `"null"`。

#### 设置标签和注解

要向镜像添加 OCI 元数据，请使用 `labels` 和 `annotations`。标签存储在镜像配置中；注解存储在镜像清单中。在适用的情况下使用 [OCI 标准键](https://specs.opencontainers.org/image-spec/annotations/)。

```yaml
labels:
  org.opencontainers.image.authors: your-email@example.com
  org.opencontainers.image.version: "1.0.0"

annotations:
  org.opencontainers.image.title: Custom hardened image
  org.opencontainers.image.description: Customized Docker Hardened Image
```

#### 覆盖入口点和命令

要更改容器的启动方式，请使用 `entrypoint` 和 `cmd`。这些参数会附加到基础镜像现有的入口点和命令。

> [!NOTE]
>
> 批量自定义（多个 `targets`）不支持。

```yaml
entrypoint:
  - /docker-entrypoint.sh

cmd:
  - /bin/bash
```

#### 设置平台和压缩

要为多个架构构建，请在 `platforms` 下列出它们。至少需要一个平台。

```yaml
platforms:
  - linux/amd64
  - linux/arm64
```

要控制层压缩，请设置 `compression`。`ZSTD`（默认）提供更好的压缩和更快的拉取。使用 `GZIP` 以兼容较旧的工具。

```yaml
compression: ZSTD
```

## OCI artifacts

在 DHI 自定义中，OCI 制品是包含您要分层到镜像中文件（例如自定义证书、内部工具或配置文件）的 Docker 镜像。

### 创建 OCI 制品镜像

使制品镜像尽可能最小化，仅包含必要的文件。

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

### 环境变量

当您在自定义中包含 OCI 制品时，这些制品中定义的环境变量会合并到最终镜像中。合并遵循以下规则：

- 您的自定义的 environment 设置优先。只有当相应键在您的自定义中缺失或为空时，才会应用制品的变量。
- `PATH` 是个例外。制品的 `PATH` 条目会添加到现有 `PATH` 的前面，使它们在运行时优先。

这与 Dockerfile 中的 `COPY --from` 不同，后者复制文件而不会从源镜像继承环境变量。要避免继承环境变量，请使用 `FROM scratch` 最终阶段构建制品。请参阅[创建 OCI 制品镜像](#create-an-oci-artifact-image)。

### 最佳实践

为 DHI 自定义创建 OCI 制品时，请遵循以下最佳实践：

- 使用多阶段构建：在构建器阶段构建或安装依赖项，然后仅将必要的文件复制到 `FROM scratch` 最终阶段。这保持 OCI 制品最小化，并避免从构建器镜像继承环境变量到您的自定义中。

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

### Helm chart 自定义 YAML 文件

使用 CLI 时，Helm chart 自定义使用与镜像自定义相同的 `prepare` / `create` 工作流，但配置节使用 `reference_mappings` 而非镜像字段。

使用 `reference_mappings` 替换 chart 中的镜像引用，例如将 chart 的镜像引用指向您镜像的 DHI。

```yaml
name: use mirrored images

targets:
  - destination: my-org/dhi-haproxy-chart
    tag_definition_id: haproxy/helm/1

reference_mappings:
  - from: dhi/haproxy
    to: my-org/dhi-haproxy
```

| 字段 | 描述 |
|:---|:---|
| `reference_mappings[].from` | 要替换的 chart 中的镜像引用。 |
| `reference_mappings[].to` | 替换后的镜像引用，通常是您组织中的镜像 DHI。 |

## 监控自定义构建

创建自定义后，您可以通过 Docker Hub 或 DHI CLI 跟踪构建状态并查看日志。

**Docker Hub**



1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Hardened Images** > **Manage**。
5. 选择 **Customizations** 选项卡。

**CLI**



列出自定义的构建：

```console
$ docker dhi customization build list <customization-id> --org my-org
```

获取特定构建的详细信息：

```console
$ docker dhi customization build get <customization-id> <build-id> --org my-org
```

查看构建日志：

```console
$ docker dhi customization build logs <customization-id> <build-id> --org my-org
```



## 编辑或删除自定义

**Docker Hub**



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

**CLI**



要编辑自定义，请更新您的 YAML 文件并运行：

```console
$ docker dhi customization edit my-customization.yaml --org my-org
```

YAML 文件必须包含 `id` 字段以识别要更新的自定义。要查找 ID，请运行 `docker dhi customization list --org my-org`。

要按 ID 删除自定义：

```console
$ docker dhi customization delete <id> --org my-org
$ docker dhi customization delete <id> --org my-org --force
```

`--force` 标志跳过确认提示。



