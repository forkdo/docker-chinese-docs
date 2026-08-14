---
description: 从自动构建迁移到 CI/CD 工作流
keywords: automated builds, autobuilds, migration, github actions, bitbucket pipelines
title: 从自动构建迁移
linkTitle: 迁移
weight: 80
---

> [!WARNING]
> Docker Hub 自动构建是一项已弃用的功能。
> 它将于 2027 年 4 月 1 日完全退役。

本指南介绍如何将您的 Docker Hub 自动构建设置迁移到持续集成 (CI) 工作流，重点介绍 GitHub Actions 和 Bitbucket Pipelines，因为它们是通过自动构建所支持的两个版本控制服务的内置 CI 服务。

## 步骤 1：创建访问令牌

要授予您的 CI 工作流向 Docker Hub 拉取和推送镜像的能力，您首先需要创建访问令牌：

- 对于个人仓库：创建一个具有 **读 & 写** 权限的[个人访问令牌](../../../../security/access-tokens.md)。

- 对于组织仓库：创建一个[组织访问令牌](../../../../enterprise/security/access-tokens.md)，并具有以下权限：
  - **读取公共仓库**
  - 对构建需要拉取的任何私有仓库的 **镜像拉取** 权限
  - 对将推送构建镜像的仓库的 **镜像推送** 权限

只要该令牌对账户命名空间下所有相关的 Docker Hub 仓库具有足够的权限，同一个令牌即可用于该命名空间下的所有 CI 工作流。

请将令牌安全地存储在密码管理器或您的 CI/CD 平台的密钥管理器中。切勿将令牌提交到源代码仓库。

## 步骤 2：提取您的自动构建配置

对于当前配置为使用自动构建的每个 Docker Hub 仓库，您需要提取其配置，以设置 CI 工作流来复制现有功能。提取配置的唯一方式是通过 Docker Hub Web 界面。

1. 登录 [Docker Hub](https://hub.docker.com)。

2. 通过 **我的 Hub** > ***您的命名空间*** > **仓库** > ***您的仓库*** 导航到您的仓库。

3. 转到 **构建** 选项卡并选择 **配置自动构建**。

   如果没有现有的构建配置，则该仓库未配置自动构建。

4. 记下以下配置详情：

   - **源仓库**：GitHub 或 Bitbucket 仓库。组织是命名空间，仓库是仓库名称。这是您需要添加工作流的位置。

   - **Autotest**：如果为拉取请求（仅内部或内部和外部）启用了 Autotest，则您的工作流中需要额外的步骤来运行 Autotest 步骤。

   - **仓库链接**：不支持，可以忽略。如果需要链式构建，请参阅您的 CI 服务文档了解如何将构建链接在一起。

   - **构建规则**：指定构建的触发器、标签和路径。忽略任何 **自动构建** 被关闭的条目。

   - **构建环境变量**：作为环境变量注入到构建中的用户定义变量。您需要将这些添加到您的工作流中。如果环境变量包含密钥，请将它们添加到您的 CI 服务的密钥管理器中。然后更新您的 Dockerfile 或构建脚本，使用您 CI 平台的语法来引用这些密钥。有关如何处理密钥，请参阅您的 CI 服务文档。

### 示例配置

下图显示了一个自动构建配置示例。

![自动构建配置示例](./images/autobuild-example.png)

基于图片中的示例，您将记录以下该自动构建配置项：

- 源代码仓库：GitHub 仓库 `docker/docker-rust-hello`
- Autotest：已禁用
- 构建规则 1：当检测到 `main` 分支有新提交时，构建并推送标签为 `latest` 的镜像。Dockerfile 位于 `./Dockerfile`，构建上下文为克隆代码的根目录。
- 构建规则 2：当检测到匹配正则表达式 `^v([0-9.]+)$` 的标签有新提交时，构建并推送标签为 `v{\1}` 的镜像。Dockerfile 位于 `./Dockerfile`，构建上下文为克隆代码的根目录。
- 环境变量：键 `ENV_KEY`，值 `ENV_VALUE`

## 步骤 3：迁移到您的 CI/CD 平台

选择与您的源代码仓库托管平台匹配的标签页。

{{< tabs >}}
{{< tab name="GitHub Actions" >}}

如果您的源代码仓库托管在 GitHub 上，请参阅 [Docker 自动构建示例仓库](https://github.com/docker/autobuilds-actions)。

除 `.github/workflows` 目录下的文件外，所有文件仅用于示例目的。

该仓库的 readme 详细说明了如何使用提供的两种工作流之一从自动构建迁移到 GitHub Actions：

- `simple-build` 工作流构建并将 Docker 镜像推送到您的 Docker Hub 仓库。
- `full-autobuilds` 工作流包含自动构建运行中常用的所有步骤，包括构建、打标签、运行 Docker Compose 测试以及运行可选的 bash 钩子文件。

### 迁移步骤

1. 按照 [示例仓库 readme](https://github.com/docker/autobuilds-actions) 中的说明，在您的 GitHub 仓库中配置 CI GitHub Action 工作流。

2. 工作流中包含有关每个步骤的作用以及应在何处进行更改的注释。需要做出的重要更改包括：

   - 将 `DOCKER_REPOSITORY_NAME` 环境变量设置为您的 Docker Hub 仓库的完整名称
   - 设置您的镜像标签策略
   - 设置工作流触发器

   readme 和工作流注释中提供了相关文档的链接。

3. 完成迁移到 GitHub Actions 后，从您的 Docker Hub 仓库中删除构建配置：

   1. 导航到仓库的 **构建** 选项卡。
   2. 选择 **配置自动构建**。
   3. 选择 **删除构建配置**。

{{< /tab >}}
{{< tab name="Bitbucket Pipelines" >}}

如果您的源代码仓库托管在 Bitbucket 上，请参阅 [Docker 自动构建 Bitbucket 示例仓库](https://bitbucket.org/docker-io/autobuilds-pipeline)。

除 `bitbucket-pipelines.yml` 文件外，所有文件仅用于示例目的。

该仓库的 readme 详细说明了如何使用提供的示例 `bitbucket-pipelines.yml` 配置文件从自动构建迁移到 Bitbucket Pipelines。

该 pipeline 示例包含三个独立的 pipeline：

- `branches/main`：展示如何在特定分支发生变更时构建、测试和推送镜像
- `tags/*`：展示如何在标签推送时构建、测试和推送镜像，包括将镜像标记为与 Git 标签相同
- `pull-requests/*`：展示如何从拉取请求构建和测试镜像，但不推送

### 迁移步骤

1. 按照 [示例仓库 readme](https://bitbucket.org/docker-io/autobuilds-pipeline) 中的说明，在您的 Bitbucket 仓库中配置 Bitbucket Pipeline。

2. pipeline 配置中的注释说明了每个部分的作用以及需要在何处进行更改。需要做出的重要更改包括：

   - 将 `DOCKER_REPOSITORY_NAME` 环境变量设置为您的 Docker Hub 仓库的完整名称
   - 设置您的镜像标签策略（参见每个 pipeline 中设置 `DOCKER_TAG` 变量的位置）
   - 为分支、标签和/或拉取请求设置 pipeline 触发器

   readme 和工作流注释中提供了相关文档的链接。

3. 完成迁移到 Bitbucket Pipelines 后，从您的 Docker Hub 仓库中删除构建配置：

   1. 导航到仓库的 **构建** 选项卡。
   2. 选择 **配置自动构建**。
   3. 选择 **删除构建配置**。

{{< /tab >}}
{{< /tabs >}}
