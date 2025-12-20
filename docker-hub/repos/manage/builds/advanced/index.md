# 自动化构建和自动化测试的高级选项

> [!NOTE]
>
> 自动化构建需要 Docker Pro、Team 或 Business 订阅。

以下选项允许您自定义自动化构建和自动化测试流程。

## 用于构建和测试的环境变量

构建过程会设置多个实用环境变量，在自动化构建、自动化测试和执行钩子时可用。

> [!NOTE]
>
> 这些环境变量仅对构建和测试过程可用，不会影响您的服务运行环境。

* `SOURCE_BRANCH`：当前正在测试的分支或标签的名称。
* `SOURCE_COMMIT`：正在测试的提交的 SHA1 哈希值。
* `COMMIT_MSG`：正在测试和构建的提交消息。
* `DOCKER_REPO`：正在构建的 Docker 仓库的名称。
* `DOCKERFILE_PATH`：当前正在构建的 Dockerfile。
* `DOCKER_TAG`：正在构建的 Docker 仓库标签。
* `IMAGE_NAME`：正在构建的 Docker 仓库的名称和标签（此变量是 `DOCKER_REPO`:`DOCKER_TAG` 的组合）。

如果您在 `docker-compose.test.yml` 文件中使用这些构建环境变量进行自动化测试，请在您的 `sut` 服务的环境变量中声明它们，如下所示：

```yaml
services:
  sut:
    build: .
    command: run_tests.sh
    environment:
      - SOURCE_BRANCH
```


## 覆盖构建、测试或推送命令

Docker Hub 允许您使用钩子自定义和覆盖自动化构建和测试流程中的 `build`、`test` 和 `push` 命令。例如，您可能使用构建钩子设置仅在构建过程中使用的构建参数。您还可以设置[自定义构建阶段钩子](#custom-build-phase-hooks) 在这些命令之间执行操作。

> [!IMPORTANT]
>
> 请谨慎使用这些钩子。这些钩子文件的内容会替换基本的 `docker` 命令，因此您必须在钩子中包含类似的构建、测试或推送命令，否则您的自动化流程无法完成。

要覆盖这些阶段，请在源代码仓库中与 Dockerfile 相同的目录级别创建一个名为 `hooks` 的文件夹。创建名为 `hooks/build`、`hooks/test` 或 `hooks/push` 的文件，并包含构建器可以执行的命令，例如 `docker` 和 `bash` 命令（适当前缀 `#!/bin/bash`）。

这些钩子在 [Ubuntu](https://releases.ubuntu.com/) 实例上运行，其中包含解释器（如 Perl 或 Python）和实用程序（如 `git` 或 `curl`）。请参考 [Ubuntu 文档](https://ubuntu.com/) 获取可用解释器和实用程序的完整列表。

## 自定义构建阶段钩子

您可以通过创建钩子在构建流程的各个阶段之间运行自定义命令。钩子允许您向自动化构建和自动化测试流程提供额外的指令。

在源代码仓库中与 Dockerfile 相同的目录级别创建一个名为 `hooks` 的文件夹。将定义钩子的文件放在该文件夹中。钩子文件可以包含 `docker` 命令和 `bash` 命令，只要它们适当前缀 `#!/bin/bash`。构建器在每个步骤之前和之后执行文件中的命令。

以下钩子可用：

* `hooks/post_checkout`
* `hooks/pre_build`
* `hooks/post_build`
* `hooks/pre_test`
* `hooks/post_test`
* `hooks/pre_push`（仅在执行构建规则或[自动化构建](index.md)时使用）
* `hooks/post_push`（仅在执行构建规则或[自动化构建](index.md)时使用）

### 构建钩子示例

#### 覆盖"构建"阶段以设置变量

Docker Hub 允许您在钩子文件中或从自动化构建界面定义构建环境变量，然后您可以在钩子中引用这些变量。

以下示例定义了一个构建钩子，使用 `docker build` 参数根据使用 Docker Hub 构建设置定义的变量值设置变量 `CUSTOM`。`$DOCKERFILE_PATH` 是您提供的 Dockerfile 名称变量，`$IMAGE_NAME` 是正在构建的镜像名称。

```console
$ docker build --build-arg CUSTOM=$VAR -f $DOCKERFILE_PATH -t $IMAGE_NAME .
```

> [!IMPORTANT]
>
> `hooks/build` 文件会覆盖构建器使用的基本 `docker build` 命令，因此您必须在钩子中包含类似的构建命令，否则自动化构建会失败。

请参考 [docker build 文档](/reference/cli/docker/buildx/build.md#build-arg) 了解 Docker 构建时变量的更多信息。

#### 推送到多个仓库

默认情况下，构建流程仅将镜像推送到配置构建设置的仓库。如果您需要将同一镜像推送到多个仓库，可以设置 `post_push` 钩子添加额外标签并推送到更多仓库。

```console
$ docker tag $IMAGE_NAME $DOCKER_REPO:$SOURCE_COMMIT
$ docker push $DOCKER_REPO:$SOURCE_COMMIT
```

## 源仓库或分支克隆

当 Docker Hub 从源代码仓库拉取分支时，它执行浅克隆，仅克隆指定分支的最新提交。这具有最小化仓库必要数据传输量并加速构建的优势，因为它只拉取最少的必要代码。

因此，如果您需要执行依赖于不同分支的自定义操作（例如 `post_push` 钩子），除非您执行以下操作之一，否则无法检出该分支：

* 您可以通过以下方式获得目标分支的浅检出：

    ```console
    $ git fetch origin branch:mytargetbranch --depth 1
    ```

* 您也可以"取消浅克隆"，这会获取整个 Git 历史记录（可能耗时较长 / 传输大量数据），方法是在 fetch 时使用 `--unshallow` 标志：

    ```console
    $ git fetch --unshallow origin
    ```
