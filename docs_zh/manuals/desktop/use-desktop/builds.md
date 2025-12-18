---
title: 探索 Docker Desktop 中的 Builds 视图
linkTitle: Builds
description: 了解如何在 Docker Desktop 中使用 Builds 视图
keywords: Docker Dashboard, 管理, gui, dashboard, builders, builds
weight: 40
---

**Builds** 视图为检查构建历史、监控活跃构建以及直接在 Docker Desktop 中管理构建器提供了一个交互式界面。

默认情况下，**Build history** 选项卡会显示已完成构建的列表，按日期排序（最新的在前）。切换到 **Active builds** 选项卡可以查看正在进行的构建。

如果您通过 [Docker Build Cloud](../../build-cloud/_index.md) 连接到云构建器，
Builds 视图还会列出其他连接到同一云构建器的团队成员的任何活跃或已完成的云构建。

> [!NOTE]
>
> 使用 `docker build` 命令构建 Windows 容器镜像时，使用的是旧版构建器，它不会填充 **Builds** 视图。要切换到 BuildKit，您可以：
> - 在构建命令中设置 `DOCKER_BUILDKIT=1`，例如 `DOCKER_BUILDKIT=1 docker build .`，或者
> - 使用 `docker buildx build` 命令

## 显示构建列表

从 Docker Dashboard 打开 **Builds** 视图，可以访问：

- **Build history**：已完成的构建，可查看日志、依赖项、追踪等
- **Active builds**：当前正在进行的构建

仅列出活跃、运行中构建器的构建。已删除或已停止构建器的构建不会显示。

### 构建器设置

右上角显示当前选定构建器的名称，
**Builder settings** 按钮允许您在 Docker Desktop 设置中[管理构建器](#manage-builders)。

### 导入构建

{{< summary-bar feature_name="Import builds" >}}

**Import builds** 按钮允许您导入其他人的构建记录，或 CI 环境中的构建记录。导入构建记录后，您可以直接在 Docker Desktop 中完全访问该构建的日志、追踪和其他数据。

`docker/build-push-action` 和 `docker/bake-action` GitHub Actions 的[构建摘要](/manuals/build/ci/github-actions/build-summary.md)包含下载构建记录的链接，用于使用 Docker Desktop 检查 CI 作业。

## 检查构建

要检查构建，请在列表中选择要查看的构建。
检查视图包含多个选项卡。

**Info** 选项卡显示构建的详细信息。

如果您正在检查多平台构建，此选项卡右上角的下拉菜单允许您将信息筛选到特定平台：

**Source details** 部分显示有关前端[frontend](/manuals/build/buildkit/frontend.md)的信息，如果可用，还包括用于构建的源代码仓库。

### 构建时间

Info 选项卡的 **Build timing** 部分包含图表，从各个角度展示构建执行的细分。

- **Real time** 指完成构建的挂钟时间。
- **Accumulated time** 显示所有步骤的总 CPU 时间。
- **Cache usage** 显示构建操作的缓存使用程度。
- **Parallel execution** 显示构建执行时间中有多少用于并行运行步骤。

图表颜色和图例键描述不同的构建操作。构建操作定义如下：

| 构建操作      | 描述                                                                                                                                                                     |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Local file transfers | 将本地文件从客户端传输到构建器所花费的时间。                                                                                                             |
| File operations      | 涉及在构建中创建和复制文件的任何操作。例如，Dockerfile 前端中的 `COPY`、`WORKDIR`、`ADD` 指令都会产生文件操作。 |
| Image pulls          | 拉取镜像所花费的时间。                                                                                                                                                      |
| Executions           | 容器执行，例如 Dockerfile 前端中定义为 `RUN` 指令的命令。                                                                              |
| HTTP                 | 使用 `ADD` 下载远程资源。                                                                                                                                          |
| Git                  | 与 **HTTP** 相同，但用于 Git URL。                                                                                                                                              |
| Result exports       | 导出构建结果所花费的时间。                                                                                                                                         |
| SBOM                 | 生成 [SBOM 证明](/manuals/build/metadata/attestations/sbom.md) 所花费的时间。                                                                                                 |
| Idle                 | 构建工作进程的空闲时间，如果您配置了 [最大并行度限制](/manuals/build/buildkit/configure.md#max-parallelism)，可能会发生这种情况。                              |

### 构建依赖项

**Dependencies** 部分显示构建期间使用的镜像和远程资源。
此处列出的资源包括：

- 构建期间使用的容器镜像
- 使用 Dockerfile 指令 `ADD` 包含的 Git 仓库
- 使用 Dockerfile 指令 `ADD` 包含的远程 HTTPS 资源

### 参数、机密和其他参数

Info 选项卡的 **Configuration** 部分显示传递给构建的参数：

- 构建参数，包括解析后的值
- 机密，包括它们的 ID（但不包括它们的值）
- SSH 套接字
- 标签
- [附加上下文](/reference/cli/docker/buildx/build/#build-context)

### 输出和构件

**Build results** 部分显示生成的构建构件摘要，包括镜像清单详细信息、证明和构建追踪。

证明是附加到容器镜像的元数据记录。
元数据描述了有关镜像的某些内容，例如它是如何构建的或包含哪些包。
有关证明的更多信息，请参阅 [Build attestations](/manuals/build/metadata/attestations/_index.md)。

构建追踪捕获 Buildx 和 BuildKit 中构建执行步骤的信息。
追踪以两种格式提供：OTLP 和 Jaeger。您可以通过打开操作菜单并选择要下载的格式，从 Docker Desktop 下载构建追踪。

#### 使用 Jaeger 检查构建追踪

使用 Jaeger 客户端，您可以从 Docker Desktop 导入和检查构建追踪。以下步骤展示如何从 Docker Desktop 导出追踪并在 [Jaeger](https://www.jaegertracing.io/) 中查看：

1. 启动 Jaeger UI：

   ```console
   $ docker run -d --name jaeger -p "16686:16686" jaegertracing/all-in-one
   ```

2. 在 Docker Desktop 中打开 Builds 视图，选择一个已完成的构建。

3. 导航到 **Build results** 部分，打开操作菜单并选择 **Download as Jaeger format**。

   <video controls>
     <source src="/assets/video/build-jaeger-export.mp4" type="video/mp4" />
   </video>

4. 在浏览器中访问 <http://localhost:16686> 打开 Jaeger UI。

5. 选择 **Upload** 选项卡并打开刚刚导出的 Jaeger 构建追踪。

现在您可以使用 Jaeger UI 分析构建追踪：

![Jaeger UI 截图](../images/build-ui-jaeger-screenshot.png "Jaeger UI 中构建追踪的截图")

### Dockerfile 源和错误

检查成功完成的构建或正在进行的活跃构建时，**Source** 选项卡显示用于创建构建的[前端](/manuals/build/buildkit/frontend.md)。

如果构建失败，会显示 **Error** 选项卡而不是 **Source** 选项卡。
错误消息内联在 Dockerfile 源中，
指示失败发生的位置和原因。

### 构建日志

**Logs** 选项卡显示构建日志。
对于活跃构建，日志会实时更新。

您可以在构建日志的 **List view** 和 **Plain-text view** 之间切换。

- **List view** 以可折叠格式呈现所有构建步骤，
  带有时间线以便沿时间轴导航日志。

- **Plain-text view** 将日志显示为纯文本。

**Copy** 按钮允许您将日志的纯文本版本复制到剪贴板。

### 构建历史

**History** 选项卡显示已完成构建的统计数据。

时间序列图表说明了相关构建在持续时间、构建步骤和缓存使用方面的趋势，
帮助您识别构建操作随时间的模式和变化。
例如，构建持续时间的显著峰值或大量缓存未命中
可能表明有机会优化 Dockerfile。

您可以通过在图表中选择相关构建，或使用图表下方的 **Past builds** 列表来导航和检查相关构建。