# 探索 Docker Desktop 中的构建视图

**构建**视图提供了一个交互式界面，用于检查构建历史、监控活跃构建，以及直接在 Docker Desktop 中管理构建器。

默认情况下，**构建历史**选项卡会显示已完成构建的列表，按日期排序（最新的在前）。切换到**活跃构建**选项卡可以查看正在进行的构建。

如果您通过 [Docker Build Cloud](../../build-cloud/_index.md) 连接到云构建器，
构建视图还会列出其他连接到同一云构建器的团队成员的任何活跃或已完成的云构建。

> [!NOTE]
>
> 使用 `docker build` 命令构建 Windows 容器镜像时，使用的是传统构建器，不会填充 **构建**视图。要切换到使用 BuildKit，您可以：
> - 在构建命令中设置 `DOCKER_BUILDKIT=1`，例如 `DOCKER_BUILDKIT=1 docker build .`，或者
> - 使用 `docker buildx build` 命令

## 显示构建列表

从 Docker Dashboard 打开**构建**视图可以访问：

- **构建历史**：已完成的构建，可查看日志、依赖项、跟踪等
- **活跃构建**：当前正在进行的构建

仅列出活跃、运行中构建器的构建。已删除或已停止的构建器的构建不会显示。

### 构建器设置

右上角显示当前选中构建器的名称，
**构建器设置**按钮允许您在 Docker Desktop 设置中[管理构建器](#manage-builders)。

### 导入构建





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    
      
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Availability:</span>
        <span>
          Beta
          
            
              <span class="icon-svg"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M360-360H217q-18 0-26.5-16t2.5-31l338-488q8-11 20-15t24 1q12 5 19 16t5 24l-39 309h176q19 0 27 17t-4 32L388-66q-8 10-20.5 13T344-55q-11-5-17.5-16T322-95l38-265Z"/></svg></span>
            
          
            
          
            
          
            
          
            
          
        </span>
      </div>
    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 
    
  
  <a class="link" href="/desktop/release-notes/#4310">4.31</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



**导入构建**按钮允许您导入其他人或 CI 环境中的构建记录。导入构建记录后，您可以直接在 Docker Desktop 中查看该构建的完整日志、跟踪和其他数据。

`docker/build-push-action` 和 `docker/bake-action` GitHub Actions 的[构建摘要](/manuals/build/ci/github-actions/build-summary.md)包含一个下载构建记录的链接，用于使用 Docker Desktop 检查 CI 任务。

## 检查构建

要检查构建，请在列表中选择要查看的构建。
检查视图包含多个选项卡。

**信息**选项卡显示有关构建的详细信息。

如果您正在检查多平台构建，此选项卡右上角的下拉菜单允许您将信息筛选到特定平台：

**源代码详情**部分显示有关前端[前端](/manuals/build/buildkit/frontend.md)的信息，如果可用，还包括用于构建的源代码仓库。

### 构建时间

信息选项卡的**构建时间**部分包含图表，
从各个角度显示构建执行的细分。

- **实际时间**指完成构建所用的挂钟时间。
- **累计时间**显示所有步骤的总 CPU 时间。
- **缓存使用情况**显示构建操作被缓存的程度。
- **并行执行**显示构建执行时间中有多少用于并行运行步骤。

图表颜色和图例键描述不同的构建操作。构建操作定义如下：

| 构建操作      | 描述                                                                                                                                                                     |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 本地文件传输 | 将本地文件从客户端传输到构建器所花费的时间。                                                                                                             |
| 文件操作      | 涉及在构建中创建和复制文件的任何操作。例如，Dockerfile 前端中的 `COPY`、`WORKDIR`、`ADD` 指令都会产生文件操作。 |
| 镜像拉取          | 拉取镜像所花费的时间。                                                                                                                                                      |
| 执行           | 容器执行，例如 Dockerfile 前端中定义为 `RUN` 指令的命令。                                                                              |
| HTTP                 | 使用 `ADD` 下载远程资源。                                                                                                                                          |
| Git                  | 与 **HTTP** 相同，但用于 Git URL。                                                                                                                                              |
| 结果导出       | 导出构建结果所花费的时间。                                                                                                                                         |
| SBOM                 | 生成 [SBOM 证明](/manuals/build/metadata/attestations/sbom.md) 所花费的时间。                                                                                                 |
| 空闲                 | 构建工作进程的空闲时间，如果配置了 [最大并行度限制](/manuals/build/buildkit/configure.md#max-parallelism)，可能会发生这种情况。                              |

### 构建依赖项

**依赖项**部分显示构建期间使用的镜像和远程资源。
此处列出的资源包括：

- 构建期间使用的容器镜像
- 使用 `ADD` Dockerfile 指令包含的 Git 仓库
- 使用 `ADD` Dockerfile 指令包含的远程 HTTPS 资源

### 参数、密钥和其他参数

信息选项卡的**配置**部分显示传递给构建的参数：

- 构建参数，包括解析后的值
- 密钥，包括其 ID（但不包括其值）
- SSH 套接字
- 标签
- [其他上下文](/reference/cli/docker/buildx/build/#build-context)

### 输出和工件

**构建结果**部分显示生成的构建工件摘要，
包括镜像清单详情、证明和构建跟踪。

证明是附加到容器镜像的元数据记录。
元数据描述了有关镜像的某些内容，
例如它是如何构建的或包含哪些包。
有关证明的更多信息，请参阅 [构建证明](/manuals/build/metadata/attestations/_index.md)。

构建跟踪捕获 Buildx 和 BuildKit 中构建执行步骤的信息。
跟踪以两种格式提供：OTLP 和 Jaeger。您可以通过打开操作菜单并选择要下载的格式，从 Docker Desktop 下载构建跟踪。

#### 使用 Jaeger 检查构建跟踪

使用 Jaeger 客户端，您可以从 Docker Desktop 导入和检查构建跟踪。以下步骤展示如何从 Docker Desktop 导出跟踪并在 [Jaeger](https://www.jaegertracing.io/) 中查看：

1. 启动 Jaeger UI：

   ```console
   $ docker run -d --name jaeger -p "16686:16686" jaegertracing/all-in-one
   ```

2. 在 Docker Desktop 中打开构建视图，选择一个已完成的构建。

3. 导航到**构建结果**部分，打开操作菜单并选择**下载为 Jaeger 格式**。

   <video controls>
     <source src="/assets/video/build-jaeger-export.mp4" type="video/mp4" />
   </video>

4. 在浏览器中访问 <http://localhost:16686> 打开 Jaeger UI。

5. 选择**上传**选项卡，打开刚刚导出的 Jaeger 构建跟踪。

现在您可以使用 Jaeger UI 分析构建跟踪：

![Jaeger UI 截图](../images/build-ui-jaeger-screenshot.png "Jaeger UI 中构建跟踪的截图")

### Dockerfile 源代码和错误

检查成功的已完成构建或正在进行的活跃构建时，
**源代码**选项卡显示用于创建构建的[前端](/manuals/build/buildkit/frontend.md)。

如果构建失败，会显示**错误**选项卡而不是**源代码**选项卡。
错误消息内联在 Dockerfile 源代码中，
指示失败发生的位置和原因。

### 构建日志

**日志**选项卡显示构建日志。
对于活跃构建，日志会实时更新。

您可以在构建日志的**列表视图**和**纯文本视图**之间切换。

- **列表视图**以可折叠格式呈现所有构建步骤，
  并带有时间轴以便沿时间轴导航日志。

- **纯文本视图**将日志显示为纯文本。

**复制**按钮允许您将日志的纯文本版本复制到剪贴板。

### 构建历史

**历史**选项卡显示已完成构建的统计数据。

时间序列图表说明了相关构建的持续时间、构建步骤和缓存使用情况的趋势，
帮助您识别构建操作随时间的模式和变化。
例如，构建持续时间的显著峰值或大量缓存未命中
可能表明有机会优化 Dockerfile。

您可以通过在图表中选择相关构建或使用图表下方的**过去构建**列表来导航和检查相关构建。

## 管理构建器

**设置**中的**构建器**选项卡允许您：

- 检查活跃构建器的状态和配置
- 启动和停止构建器
- 删除构建历史
- 添加或删除构建器（或连接和断开云构建器）

有关管理构建器的更多信息，请参阅 [更改设置](/manuals/desktop/settings-and-maintenance/settings.md#builders)
