---
description: 设置自动构建
keywords: 自动构建, 构建镜像, Docker Hub
title: 设置自动构建
linkTitle: 设置
weight: 10
aliases:
- /docker-hub/builds/automated-build/
- /docker-hub/builds/classic/
- /docker-hub/builds/
---

> [!NOTE]
>
> 自动构建需要 Docker Pro、Team 或 Business 订阅。

## 配置自动构建

您可以在 Docker Hub 中配置仓库，使其在每次向源代码提供商推送新代码时自动构建镜像。如果您配置了[自动测试](automated-testing.md)，只有在测试通过后才会推送新镜像。

1. 在 [Docker Hub](https://hub.docker.com) 中，进入 **My Hub** > **Repositories**，选择一个仓库查看其详细信息。

2. 选择 **Builds** 选项卡。

3. 选择 GitHub 或 Bitbucket 来连接镜像源代码存储的位置。

   > [!NOTE]
   >
   > 您可能被重定向到设置页面以[链接代码仓库服务](link-source.md)。否则，如果您正在编辑现有自动构建的构建设置，请选择 **Configure automated builds**。

4. 选择要从中构建 Docker 镜像的**源仓库**。

   > [!NOTE]
   >
   > 您可能需要在源代码提供商处指定一个组织或用户。选择用户后，源代码仓库将出现在 **Select repository** 下拉列表中。

5. 可选。启用[自动测试](automated-testing.md#enable-automated-tests-on-a-repository)。

6. 查看默认的**构建规则**。

    构建规则控制 Docker Hub 从源代码仓库内容中构建什么为镜像，以及生成的镜像如何在 Docker 仓库中标记标签。
    
    系统会为您设置一个默认构建规则，您可以编辑或删除它。此默认规则设置从源代码仓库中的 `Branch` 构建，名为 `master` 或 `main`，并创建一个标记为 `latest` 的 Docker 镜像。更多信息，请参阅[设置构建规则](#set-up-build-rules)。

7. 可选。选择 **plus** 图标添加并[配置更多构建规则](#set-up-build-rules)。

8. 对于每个分支或标签，启用或禁用 **Autobuild** 切换。

    只有启用了自动构建的分支或标签才会被构建、测试，并将生成的镜像推送到仓库。禁用自动构建的分支会被构建用于测试（如果在仓库级别启用），但构建的 Docker 镜像不会推送到仓库。

9. 对于每个分支或标签，启用或禁用 **Build Caching** 切换。

    [构建缓存](/manuals/build/building/best-practices.md#leverage-build-cache)
    可以节省时间，如果您频繁构建大型镜像或有许多依赖项。如果要在构建时确保所有依赖项都被解析，或者如果您有一个大型层在本地构建更快，请禁用构建缓存。

10. 选择 **Save** 保存设置，或选择 **Save and build** 保存并运行初始测试。

    > [!NOTE]
    >
    > 会自动将一个 webhook 添加到您的源代码仓库，以便在每次推送时通知 Docker Hub。只有推送到被列为一个或多个标签源的分支才会触发构建。

### 设置构建规则

默认情况下，当您设置自动构建时，会为您创建一个基本的构建规则。此默认规则监视源代码仓库中 `master` 或 `main` 分支的更改，并将 `master` 或 `main` 分支构建为标记为 `latest` 的 Docker 镜像。

在 **Build Rules** 部分，输入一个或多个要构建的源。

对于每个源：

* 选择要构建的**源类型**，分支或标签。这告诉构建系统在源代码仓库中查找什么。

* 输入要构建的**源**分支或标签的名称。

  首次配置自动构建时，会为您设置一个默认构建规则。此默认设置从源代码中称为 `master` 的 `Branch` 构建，并创建一个标记为 `latest` 的 Docker 镜像。

  您也可以使用正则表达式选择要构建的源分支或标签。要了解更多信息，请参阅[正则表达式](#regexes-and-automated-builds)。

* 输入应用于从此源构建的 Docker 镜像的标签。

  如果您配置了正则表达式选择源，可以引用捕获组并使用其结果作为标签的一部分。要了解更多信息，请参阅[正则表达式](#regexes-and-automated-builds)。

* 将 **Dockerfile location** 指定为相对于源代码仓库根目录的路径。如果 Dockerfile 在仓库根目录，请将此路径保留为 `/`。

> [!NOTE]
>
> 当 Docker Hub 从源代码仓库拉取分支时，它执行浅克隆 - 仅指定分支的顶端。请参阅[自动构建和自动测试的高级选项](advanced.md#source-repository-or-branch-clones)了解更多信息。

### 构建的环境变量

配置自动构建时，您可以设置构建过程中使用的环境变量值。通过选择 **Build environment variables** 部分旁边的 **plus** 图标，然后输入变量名和值来添加构建环境变量。

当您从 Docker Hub UI 设置变量值时，您的命令可以在 `hooks` 文件中使用它们。但是，它们被存储，只有对 Docker Hub 仓库具有 `admin` 访问权限的用户才能看到其值。这意味着您可以使用它们来存储访问令牌或其他应保持机密的信息。

> [!NOTE]
>
> 构建配置屏幕中设置的变量仅在构建过程中使用，不应与您的服务使用的环境值混淆，例如用于创建服务链接。

## 高级自动构建选项

最少您需要一个构建规则，由源分支或标签和目标 Docker 标签组成，以设置自动构建。您还可以：

- 更改构建查找 Dockerfile 的位置
- 设置构建应使用的文件路径（构建上下文）
- 设置多个静态标签或分支以从中构建
- 使用正则表达式（regexes）动态选择源代码以构建并创建动态标签

所有这些选项都可以从每个仓库的 **Build configuration** 屏幕中获得。在 [Docker Hub](https://hub.docker.com) 中，选择 **My Hub** > **Repositories**，然后选择要编辑的仓库名称。选择 **Builds** 选项卡，然后选择 **Configure Automated builds**。

### 标签和分支构建

您可以配置自动构建，使推送到特定分支或标签的操作触发构建。

1. 在 **Build Rules** 部分，选择 **plus** 图标添加更多要构建的源。

2. 选择要构建的**源类型**，分支或标签。

    > [!NOTE]
    >
    > 这告诉构建系统在代码仓库中查找什么类型的源。

3. 输入要构建的**源**分支或标签的名称。

    > [!NOTE]
    >
    > 您可以输入名称，或使用正则表达式匹配要构建的源分支或标签名称。要了解更多信息，请参阅[正则表达式](index.md#regexes-and-automated-builds)。

4. 输入应用于从此源构建的 Docker 镜像的标签。

   > [!NOTE]
   >
   > 如果您配置了正则表达式选择源，可以引用捕获组并使用其结果作为标签的一部分。要了解更多信息，请参阅[正则表达式](index.md#regexes-and-automated-builds)。

5. 对设置的每个新构建规则重复步骤 2 到 4。

### 设置构建上下文和 Dockerfile 位置

根据您在源代码仓库中安排文件的方式，构建镜像所需的文件可能不在仓库根目录。如果是这种情况，您可以指定构建查找文件的路径。

构建上下文是构建所需文件的路径，相对于仓库根目录。在 **Build context** 字段中输入这些文件的路径。输入 `/` 将构建上下文设置为源代码仓库的根目录。

> [!NOTE]
>
> 如果删除 **Build context** 字段中的默认路径 `/` 并留空，构建系统将使用 Dockerfile 的路径作为构建上下文。但是，为了避免混淆，建议您指定完整路径。

您可以将 **Dockerfile location** 指定为相对于构建上下文的路径。如果 Dockerfile 在构建上下文路径的根目录，请将 Dockerfile 路径保留为 `/`。如果构建上下文字段为空，请从源仓库根目录设置到 Dockerfile 的路径。

### 正则表达式和自动构建

您可以指定正则表达式（regex），以便只有匹配的分支或标签被构建。您还可以使用正则表达式的结果创建应用于构建镜像的 Docker 标签。

您可以使用最多九个正则表达式捕获组，或括在括号中的表达式，来选择要构建的源，并在 **Docker Tag** 字段中使用 `{\1}` 到 `{\9}` 引用它们。

<!-- Capture groups Not a priority
#### Regex example: build from version number branch and tag with version number

You could also use capture groups to build and label images that come from various
sources. For example, you might have

`/(alice|bob)-v([0-9.]+)/` -->

### 使用 BuildKit 构建镜像

自动构建默认使用 BuildKit 构建系统。如果您想使用传统的 Docker 构建系统，请添加[环境变量](index.md#environment-variables-for-builds) `DOCKER_BUILDKIT=0`。更多信息请参考 [BuildKit](/manuals/build/buildkit/_index.md) 页面。

## 团队自动构建

当您在自己的用户账户中创建自动构建仓库时，您可以启动、取消和重试构建，并编辑和删除自己的仓库。

如果您的身份是所有者，这些相同的操作也可以从 Docker Hub 对团队仓库执行。如果您是具有 `write` 权限的团队成员，您可以启动、取消和重试团队仓库中的构建，但不能编辑团队仓库设置或删除团队仓库。如果您的用户账户具有 `read` 权限，或者您是具有 `read` 权限的团队成员，您可以查看构建配置，包括任何测试设置。

| 操作/权限     | 读取 | 写入 | 管理员 | 所有者 |
| --------------------- | ---- | ----- | ----- | ----- |
| 查看构建详细信息    |  x   |   x   |   x   |   x   |
| 启动、取消、重试  |      |   x   |   x   |   x   |
| 编辑构建设置   |      |       |   x   |   x   |
| 删除构建          |      |       |       |   x   |

### 团队自动构建的服务用户

> [!NOTE]
>
> 只有所有者可以为团队设置自动构建。

当您为团队设置自动构建时，您使用与特定用户账户关联的 OAuth 授予 Docker Hub 访问源代码仓库的权限。这意味着 Docker Hub 可以访问链接的源提供商账户可以访问的所有内容。

对于组织和团队，建议您创建一个专用的服务账户来授予源提供商的访问权限。这确保了当个别用户的访问权限更改时不会破坏构建，并且个别用户个人项目不会暴露给整个组织。

此服务账户应具有访问要构建的任何仓库的权限，并且必须具有源代码仓库的管理访问权限，以便它可以管理部署密钥。如有需要，您可以将此账户限制为特定构建所需的特定仓库集合。

如果您正在构建带有链接私有子模块（私有依赖项）的仓库，您还需要为与该账户关联的自动构建添加覆盖 `SSH_PRIVATE` 环境变量。更多信息请参阅 [故障排除](troubleshoot.md#build-repositories-with-linked-private-submodules)

1. 在您的源提供商处创建一个服务用户账户，并为其生成 SSH 密钥。
2. 在您的组织中创建一个 "build" 团队。
3. 确保新的 "build" 团队可以访问每个仓库和子模块，这些是构建所需的。

    1. 在 GitHub 或 Bitbucket 上，进入仓库的 **Settings** 页面。
    2. 将新的 "build" 团队添加到已批准用户列表中。

        - GitHub：在 **Collaborators and Teams** 中添加团队。
        - Bitbucket：在 **Access management** 中添加团队。

4. 在源提供商处将服务用户添加到 "build" 团队。

5. 以所有者身份登录 Docker Hub，切换到组织，并按照说明使用服务账户[链接到源代码仓库](link-source.md)。

    > [!NOTE]
    >
    > 您可能需要从源代码提供商处退出您的个人账户，以创建与服务账户的链接。

6. 可选。使用您生成的 SSH 密钥设置任何带有私有子模块的构建，使用服务账户和[之前的说明](troubleshoot.md#build-repositories-with-linked-private-submodules)。

## 接下来做什么？

- 使用环境变量、hooks 等[自定义您的构建过程](advanced.md)
- [添加自动测试](automated-testing.md)
- [管理您的构建](manage-builds.md)
- [故障排除](troubleshoot.md)