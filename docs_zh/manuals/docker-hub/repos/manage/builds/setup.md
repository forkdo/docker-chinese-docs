---
description: 设置自动化构建
keywords: automated, build, images, Docker Hub
title: 设置自动化构建
linkTitle: 设置
weight: 10
aliases:
- /docker-hub/builds/automated-build/
- /docker-hub/builds/classic/
- /docker-hub/builds/
---

> [!NOTE]
>
> 自动化构建需要 Docker Pro、Team 或 Business 订阅。

## 配置自动化构建

您可以配置 Docker Hub 中的仓库，以便在您向源代码提供程序推送新代码时自动构建镜像。如果您配置了[自动化测试](automated-testing.md)，则仅在测试成功时才会推送新镜像。

1. 在 [Docker Hub](https://hub.docker.com) 中，转到 **My Hub** > **Repositories**，然后选择一个仓库以查看其详细信息。

2. 选择 **Builds** 选项卡。

3. 选择 GitHub 或 Bitbucket 以连接存储镜像源代码的位置。

   > [!NOTE]
   >
   > 您可能会被重定向到设置页面以[链接代码仓库服务](link-source.md)。否则，如果您正在编辑现有自动化构建的构建设置，请选择 **Configure automated builds**。

4. 选择要从中构建 Docker 镜像的**源代码仓库 (source repository)**。

   > [!NOTE]
   >
   > 您可能需要指定源代码提供程序中的组织或用户。选择用户后，源代码仓库将出现在 **Select repository** 下拉列表中。

5. 可选。启用[自动化测试](automated-testing.md#enable-automated-tests-on-a-repository)。

6. 查看默认的 **Build Rules**。

    构建规则控制 Docker Hub 将源代码仓库的内容构建到镜像中的内容，以及生成的镜像在 Docker 仓库中的标记方式。

    系统会为您设置一个默认的构建规则，您可以编辑或删除该规则。此默认规则设置从源代码仓库中名为 `master` 或 `main` 的 `Branch` 进行构建，并创建一个标记为 `latest` 的 Docker 镜像。有关更多信息，请参阅[设置构建规则](#set-up-build-rules)。

7. 可选。选择**加号**图标以添加并[配置更多构建规则](#set-up-build-rules)。

8. 对于每个分支或标签，启用或禁用 **Autobuild** 切换开关。

    仅启用自动构建的分支或标签会被构建、测试，并将生成的镜像推送到仓库。禁用自动构建的分支会出于测试目的进行构建（如果在仓库级别启用了测试），但构建的 Docker 镜像不会推送到仓库。

9. 对于每个分支或标签，启用或禁用 **Build Caching** 切换开关。

    [构建缓存](/manuals/build/building/best-practices.md#leverage-build-cache)可以节省时间，如果您经常构建大型镜像或有许多依赖项。禁用构建缓存可确保所有依赖项都在构建时解析，或者如果您有一个在本地构建更快的大型层。

10. 选择 **Save** 保存设置，或选择 **Save and build** 保存并运行初始测试。

    > [!NOTE]
    >
    > 会自动向您的源代码仓库添加一个 Webhook，以便在每次推送时通知 Docker Hub。只有推送到列为一个或多个标签源的分支才会触发构建。

### 设置构建规则

默认情况下，当您设置自动化构建时，系统会为您创建一个基本的构建规则。此默认规则监视源代码仓库中 `master` 或 `main` 分支的更改，并将 `master` 或 `main` 分支构建为标记为 `latest` 的 Docker 镜像。

在 **Build Rules** 部分中，输入一个或要构建的源。

对于每个源：

* 选择要构建标签还是分支的 **Source type**。这告诉构建系统在源代码仓库中查找什么。

* 输入要构建的**源 (Source)** 分支或标签的名称。

  第一次配置自动化构建时，系统会为您设置一个默认的构建规则。此默认设置从源代码中名为 `master` 的 `Branch` 进行构建，并创建一个标记为 `latest` 的 Docker 镜像。

  您也可以使用正则表达式来选择要构建的源分支或标签。要了解更多信息，请参阅[正则表达式](#regexes-and-automated-builds)。

* 输入要应用于从此源构建的 Docker 镜像的标签。

  如果您配置了正则表达式来选择源，则可以引用捕获组并将其结果用作标签的一部分。要了解更多信息，请参阅[正则表达式](#regexes-and-automated-builds)。

* 将 **Dockerfile location** 指定为相对于源代码仓库根目录的路径。如果 Dockerfile 位于仓库根目录，请将此路径保留为 `/`。

> [!NOTE]
>
> 当 Docker Hub 从源代码仓库拉取分支时，它会执行浅克隆 - 仅克隆指定分支的提示。有关更多信息，请参阅[自动构建和自动测试的高级选项](advanced.md#source-repository-or-branch-clones)。

### 构建的环境变量

您可以在配置自动化构建时设置构建过程中使用的环境变量的值。通过选择 **Build environment variables** 部分旁边的**加号**图标添加构建环境变量，然后输入变量名称和值。

当您从 Docker Hub UI 设置变量值时，可以通过您在 `hooks` 文件中设置的命令使用它们。但是，它们的存储方式使得只有对 Docker Hub 仓库具有 `admin` 访问权限的用户才能看到其值。这意味着您可以使用它们来存储访问令牌或其他应保密的信息。

> [!NOTE]
>
> 在构建配置屏幕上设置的变量仅在构建过程中使用，不应与您的服务使用的环境值混淆，例如用于创建服务链接。

## 高级自动化构建选项

至少，您需要一个由源分支或标签以及目标 Docker 标签组成的构建规则来设置自动化构建。您还可以：

- 更改构建查找 Dockerfile 的位置
- 设置构建应使用的文件的路径（构建上下文）
- 设置多个静态标签或分支以从中构建
- 使用正则表达式（regexes）动态选择要构建的源代码并创建动态标签

所有这些选项都可从每个仓库的 **Build configuration** 屏幕中获得。在 [Docker Hub](https://hub.docker.com) 中，选择 **My Hub** > **Repositories**，然后选择要编辑的仓库名称。选择 **Builds** 选项卡，然后选择 **Configure Automated builds**。

### 标签和分支构建

您可以配置自动化构建，以便推送到特定分支或标签时触发构建。

1. 在 **Build Rules** 部分，选择**加号**图标以添加更多要构建的源。

2. 选择要构建标签还是分支的 **Source type**。

   > [!NOTE]
   >
   > 这告诉构建系统要在代码仓库中查找哪种类型的源。

3. 输入要构建的**源 (Source)** 分支或标签的名称。

   > [!NOTE]
   >
   > 您可以输入名称，或使用正则表达式来匹配要构建的源分支或标签名称。要了解更多信息，请参阅[正则表达式](index.md#regexes-and-automated-builds)。

4. 输入要应用于从此源构建的 Docker 镜像的标签。

   > [!NOTE]
   >
   > 如果您配置了正则表达式来选择源，则可以引用捕获组并将其结果用作标签的一部分。要了解更多信息，请参阅[正则表达式](index.md#regexes-and-automated-builds)。

5. 对于您设置的每个新构建规则，重复步骤 2 到 4。

### 设置构建上下文和 Dockerfile 位置

根据您在源代码仓库中排列文件的方式，构建镜像所需的文件可能不在仓库根目录。如果是这种情况，您可以指定构建查找文件的路径。

构建上下文是构建所需文件的路径，相对于仓库的根目录。在 **Build context** 字段中输入这些文件的路径。输入 `/` 将构建上下文设置为源代码仓库的根目录。

> [!NOTE]
>
> 如果您从 **Build context** 字段中删除默认路径 `/` 并将其留空，构建系统将使用 Dockerfile 的路径作为构建上下文。但是，为避免混淆，建议您指定完整路径。

您可以将 **Dockerfile location** 指定为相对于构建上下文的路径。如果 Dockerfile 位于构建上下文路径的根目录，请将 Dockerfile 路径保留为 `/`。如果构建上下文字段为空，请将 Dockerfile 的路径设置为从源代码仓库的根目录开始。

### 正则表达式和自动化构建

您可以指定正则表达式（regex），以便仅构建匹配的分支或标签。您还可以使用正则表达式的结果来创建应用于构建镜像的 Docker 标签。

您可以使用最多九个正则表达式捕获组（括在括号中的表达式）来选择要构建的源，并在 **Docker Tag** 字段中使用 `{\1}` 到 `{\9}` 引用它们。

<!-- Capture groups Not a priority
#### Regex example: build from version number branch and tag with version number

You could also use capture groups to build and label images that come from various
sources. For example, you might have

`/(alice|bob)-v([0-9.]+)/` -->

### 使用 BuildKit 构建镜像

自动构建默认使用 BuildKit 构建系统。如果您想使用旧版 Docker 构建系统，请添加[环境变量](index.md#environment-variables-for-builds) `DOCKER_BUILDKIT=0`。有关 BuildKit 的更多信息，请参阅 [BuildKit](/manuals/build/buildkit/_index.md) 页面。

## 团队的自动构建

当您在自己的用户帐户中创建自动化构建仓库时，您可以启动、取消和重试构建，以及编辑和删除自己的仓库。

如果您是所有者，这些相同的操作也可用于 Docker Hub 中的团队仓库。如果您是具有 `write` 权限的团队的成员，您可以启动、取消和重试团队仓库中的构建，但您无法编辑团队仓库设置或删除团队仓库。如果您的用户帐户具有 `read` 权限，或者您是具有 `read` 权限的团队的成员，您可以查看构建配置，包括任何测试设置。

| 操作/权限              | 读取 | 写入 | 管理员 | 所有者 |
| --------------------- | ---- | ----- | ----- | ----- |
| 查看构建详细信息      |  x   |   x   |   x   |   x   |
| 启动、取消、重试      |      |   x   |   x   |   x   |
| 编辑构建设置          |      |       |   x   |   x   |
| 删除构建              |      |       |       |   x   |

### 团队自动构建的服务用户

> [!NOTE]
>
> 只有所有者可以为团队设置自动化构建。

当您为团队设置自动化构建时，您需要使用链接到特定用户帐户的 OAuth 授权 Docker Hub 访问您的源代码仓库。这意味着 Docker Hub 可以访问链接的源代码提供程序帐户可以访问的所有内容。

对于组织和团队，建议您创建一个专用的服务帐户来授予对源代码提供程序的访问权限。这可以确保随着单个用户访问权限的更改，构建不会中断，并且单个用户的个人项目不会暴露给整个组织。

此服务帐户应有权访问要构建的任何仓库，并且必须具有对源代码仓库的管理访问权限，以便它可以管理部署密钥。如果需要，您可以将此帐户限制为仅特定构建所需的一组仓库。

如果您正在构建具有链接的私有子模块（私有依赖项）的仓库，您还需要向与该帐户关联的自动化构建添加一个覆盖 `SSH_PRIVATE` 环境变量。有关更多信息，请参阅[故障排除](troubleshoot.md#build-repositories-with-linked-private-submodules)

1. 在您的源代码提供程序上创建一个服务用户帐户，并为其生成 SSH 密钥。
2. 在您的组织中创建一个“build”团队。
3. 确保新的“build”团队有权访问您需要构建的每个仓库和子模块。

    1. 在 GitHub 或 Bitbucket 上，转到仓库的 **Settings** 页面。
    2. 将新的“build”团队添加到批准的用户列表中。

        - GitHub：在 **Collaborators and Teams** 中添加团队。
        - Bitbucket：在 **Access management** 中添加团队。

4. 将服务用户添加到源代码提供程序上的“build”团队中。

5. 以所有者身份登录 Docker Hub，切换到组织，然后按照说明使用服务帐户[链接到源代码仓库](link-source.md)。

   > [!NOTE]
   >
   > 您可能需要在源代码提供程序上注销您的个人帐户以创建到服务帐户的链接。

6. 可选。使用您生成的 SSH 密钥为具有私有子模块的任何构建进行设置，使用服务帐户和[之前的说明](troubleshoot.md#build-repositories-with-linked-private-submodules)。

## 下一步是什么？

- 使用环境变量、钩子等[自定义您的构建过程](advanced.md)
- [添加自动化测试](automated-testing.md)
- [管理您的构建](manage-builds.md)
- [故障排除](troubleshoot.md)