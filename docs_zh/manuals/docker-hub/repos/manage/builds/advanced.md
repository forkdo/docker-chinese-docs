---
description: 自动化构建
keywords: 自动化, 构建, 镜像
title: 自动化构建和自动化测试的高级选项
linkTitle: 高级选项
weight: 40
aliases:
- /docker-hub/builds/advanced/
---

> [!NOTE]
>
> 自动化构建需要
> Docker Pro、Team 或 Business 订阅。

以下选项允许您自定义自动化构建和自动化测试流程。

## 构建和测试的环境变量

构建过程会设置几个实用的环境变量，在自动化构建、自动化测试和执行
钩子（hooks）期间可用。

> [!NOTE]
>
> 这些环境变量仅对构建和测试过程可用，不会影响您的服务运行环境。

* `SOURCE_BRANCH`：当前正在测试的分支或标签的名称。
* `SOURCE_COMMIT`：正在测试的提交的 SHA1 哈希值。
* `COMMIT_MSG`：正在测试和构建的提交消息。
* `DOCKER_REPO`：正在构建的 Docker 仓库的名称。
* `DOCKERFILE_PATH`：当前正在构建的 Dockerfile。
* `DOCKER_TAG`：正在构建的 Docker 仓库标签。
* `IMAGE_NAME`：正在构建的 Docker 仓库的名称和标签。（此变量是 `DOCKER_REPO`:`DOCKER_TAG` 的组合。）

如果您在 `docker-compose.test.yml` 文件中使用这些构建环境变量进行自动化测试，请在您的 `sut` 服务的环境变量中声明它们，如下所示。

```yaml
services:
  sut:
    build: .
    command: run_tests.sh
    environment:
      - SOURCE_BRANCH
```


## 覆盖构建、测试或推送命令

Docker Hub 允许您使用钩子（hooks）在自动化构建和测试过程中覆盖和自定义 `build`、`test` 和 `push` 命令。例如，您可能使用构建钩子来设置仅在构建过程中使用的构建参数。您还可以设置 [自定义构建阶段钩子](#custom-build-phase-hooks) 来在这些命令之间执行操作。

> [!IMPORTANT]
>
> 请谨慎使用这些钩子。这些钩子文件的内容会替换构建器的基本 `docker` 命令，因此您必须在钩子中包含类似的构建、测试或推送命令，否则您的自动化流程将无法完成。

要覆盖这些阶段，请在您的源代码仓库中创建一个名为 `hooks` 的文件夹，位置与您的 Dockerfile 相同。创建名为 `hooks/build`、`hooks/test` 或 `hooks/push` 的文件，并包含构建器可以执行的命令，例如 `docker` 和 `bash` 命令（前面适当加上 `#!/bin/bash`）。

这些钩子在 [Ubuntu](https://releases.ubuntu.com/) 实例上运行，其中包含解释器（如 Perl 或 Python）和实用工具（如 `git` 或 `curl`）。请参考 [Ubuntu 文档](https://ubuntu.com/) 获取可用解释器和实用工具的完整列表。

## 自定义构建阶段钩子

您可以通过创建钩子在构建过程的各个阶段之间运行自定义命令。钩子允许您向自动化构建和自动化测试过程提供额外的指令。

在您的源代码仓库中创建一个名为 `hooks` 的文件夹，位置与您的 Dockerfile 相同。将定义钩子的文件放在该文件夹中。钩子文件可以包含 `docker` 命令和 `bash` 命令，只要它们前面适当加上 `#!/bin/bash`。构建器在每个步骤之前和之后执行文件中的命令。

以下钩子可用：

* `hooks/post_checkout`
* `hooks/pre_build`
* `hooks/post_build`
* `hooks/pre_test`
* `hooks/post_test`
* `hooks/pre_push`（仅在执行构建规则或 [自动化构建](index.md) 时使用）
* `hooks/post_push`（仅在执行构建规则或 [自动化构建](index.md) 时使用）

### 构建钩子示例

#### 覆盖“构建”阶段以设置变量

Docker Hub 允许您在钩子文件中或从自动化构建界面定义构建环境变量，然后您可以在钩子中引用这些变量。

以下示例定义了一个构建钩子，使用 `docker build` 参数根据使用 Docker Hub 构建设置定义的变量值设置变量 `CUSTOM`。`$DOCKERFILE_PATH` 是您提供的 Dockerfile 名称的变量，`$IMAGE_NAME` 是正在构建的镜像的名称。

```console
$ docker build --build-arg CUSTOM=$VAR -f $DOCKERFILE_PATH -t $IMAGE_NAME .
```

> [!IMPORTANT]
>
> `hooks/build` 文件会覆盖构建器使用的基本 `docker build` 命令，因此您必须在钩子中包含类似的构建命令，否则自动化构建将失败。

请参考 [docker build 文档](/reference/cli/docker/buildx/build.md#build-arg) 了解 Docker 构建时变量的更多信息。

#### 推送到多个仓库

默认情况下，构建过程仅将镜像推送到配置构建设置的仓库。如果您需要将同一镜像推送到多个仓库，可以设置 `post_push` 钩子以添加额外的标签并推送到更多仓库。

```console
$ docker tag $IMAGE_NAME $DOCKER_REPO:$SOURCE_COMMIT
$ docker push $DOCKER_REPO:$SOURCE_COMMIT
```

## 源仓库或分支克隆

当 Docker Hub 从源代码仓库拉取一个分支时，它执行浅克隆（shallow clone），即仅克隆指定分支的最新提交。这具有最小化从仓库传输的数据量和加速构建的优势，因为它只拉取必要的最少代码。

因此，如果您需要执行依赖于不同分支的自定义操作（例如 `post_push` 钩子），除非您执行以下操作之一，否则无法检出该分支：

* 您可以通过以下方式获取目标分支的浅检出：

    ```console
    $ git fetch origin branch:mytargetbranch --depth 1
    ```

* 您也可以“取消浅克隆”，这会获取整个 Git 历史记录（可能需要很长时间 / 传输大量数据），通过在 fetch 中使用 `--unshallow` 标志：

    ```console
    $ git fetch --unshallow origin
    ```