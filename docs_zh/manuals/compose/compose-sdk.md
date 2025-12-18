---
description: 使用 Compose SDK 直接将 Docker Compose 集成到您的应用程序中。
keywords: docker compose sdk, compose api, Docker 开发者 SDK
title: 使用 Compose SDK
linkTitle: Compose SDK 
weight: 60
params:
  sidebar:
    badge:
      color: green
      text: 新功能
---

{{< summary-bar feature_name="Compose SDK" >}}

`docker/compose` 包可以作为 Go 库被第三方应用程序使用，通过编程方式管理在 Compose 文件中定义的容器化应用程序。该 SDK 提供了全面的 API，允许您将 Compose 功能直接集成到您的应用程序中，使您能够在不依赖 Compose CLI 的情况下加载、验证和管理多容器环境。

无论您需要作为部署流水线的一部分编排容器、构建自定义管理工具，还是将容器编排嵌入到您的应用程序中，Compose SDK 都提供了与 Docker Compose 命令行工具相同强大的功能。

## 设置 SDK

要开始使用，使用 `NewComposeService()` 函数创建一个 SDK 实例，该函数会使用必要的配置初始化服务，以便与 Docker 守护进程交互并管理 Compose 项目。此服务实例提供了所有核心 Compose 操作的方法，包括创建、启动、停止和删除容器，以及加载和验证 Compose 文件。该服务处理底层的 Docker API 交互和资源管理，让您能够专注于应用程序逻辑。

### 要求

在使用 SDK 之前，请确保您使用的是兼容版本的 Docker CLI。

```go
require (
    github.com/docker/cli v28.5.2+incompatible
)
```

Docker CLI 版本 29.0.0 及更高版本依赖新的 `github.com/moby/moby` 模块，而 Docker Compose v5 当前依赖 `github.com/docker/docker`。这意味着您需要固定 `docker/cli v28.5.2+incompatible` 以确保兼容性并避免构建错误。

### 使用示例

以下是一个基本示例，演示如何加载 Compose 项目并启动服务：

```go
package main

import (
    "context"
    "log"

	"github.com/docker/cli/cli/command"
	"github.com/docker/cli/cli/flags"
    "github.com/docker/compose/v5/pkg/api"
    "github.com/docker/compose/v5/pkg/compose"
)

func main() {
    ctx := context.Background()

	dockerCLI, err := command.NewDockerCli()
	if err != nil {
		log.Fatalf("Failed to create docker CLI: %v", err)
	}
	err = dockerCLI.Initialize(&flags.ClientOptions{})
	if err != nil {
		log.Fatalf("Failed to initialize docker CLI: %v", err)
	}
	
    // Create a new Compose service instance
    service, err := compose.NewComposeService(dockerCLI)
    if err != nil {
        log.Fatalf("Failed to create compose service: %v", err)
    }

    // Load the Compose project from a compose file
    project, err := service.LoadProject(ctx, api.ProjectLoadOptions{
        ConfigPaths: []string{"compose.yaml"},
        ProjectName: "my-app",
    })
    if err != nil {
        log.Fatalf("Failed to load project: %v", err)
    }

    // Start the services defined in the Compose file
    err = service.Up(ctx, project, api.UpOptions{
        Create: api.CreateOptions{},
        Start:  api.StartOptions{},
    })
    if err != nil {
        log.Fatalf("Failed to start services: %v", err)
    }

    log.Printf("Successfully started project: %s", project.Name)
}
```

此示例演示了核心工作流程——创建服务实例、从 Compose 文件加载项目以及启动服务。SDK 提供了许多额外的操作来管理容器化应用程序的生命周期。

## 自定义 SDK

`NewComposeService()` 函数接受可选的 `compose.Option` 参数来自定义 SDK 行为。这些选项允许您配置 I/O 流、并发限制、试运行模式和其他高级功能。

```go
    // Create a custom output buffer to capture logs
    var outputBuffer bytes.Buffer

    // Create a compose service with custom options
    service, err := compose.NewComposeService(dockerCLI,
        compose.WithOutputStream(&outputBuffer),          // Redirect output to custom writer
        compose.WithErrorStream(os.Stderr),               // Use stderr for errors
        compose.WithMaxConcurrency(4),                    // Limit concurrent operations
        compose.WithPrompt(compose.AlwaysOkPrompt()),     // Auto-confirm all prompts
    )
```

### 可用选项

- `WithOutputStream(io.Writer)`: 将标准输出重定向到自定义写入器
- `WithErrorStream(io.Writer)`: 将错误输出重定向到自定义写入器
- `WithInputStream(io.Reader)`: 为交互式提示提供自定义输入流
- `WithStreams(out, err, in)`: 一次性设置所有 I/O 流
- `WithMaxConcurrency(int)`: 限制对 Docker API 的并发操作数量
- `WithPrompt(Prompt)`: 自定义用户确认行为（使用 `AlwaysOkPrompt()` 进行非交互模式）
- `WithDryRun`: 以试运行模式运行操作，不实际应用更改
- `WithContextInfo(api.ContextInfo)`: 设置自定义 Docker 上下文信息
- `WithProxyConfig(map[string]string)`: 为构建配置 HTTP 代理设置
- `WithEventProcessor(progress.EventProcessor)`: 接收进度事件和操作通知

这些选项提供了对 SDK 行为的细粒度控制，使其适用于各种集成场景，包括 CLI 工具、Web 服务、自动化脚本和测试环境。

## 使用 `EventProcessor` 跟踪操作

`EventProcessor` 接口允许您通过接收有关 Docker 资源（如镜像、容器、卷和网络）更改的通知来实时监控 Compose 操作。这对于构建需要跟踪 Compose 操作进度的用户界面、日志系统或监控工具特别有用。

### 理解 `EventProcessor`

Compose 操作（如 `up`、`down`、`build`）对 Docker 资源执行一系列更改。`EventProcessor` 通过三个关键方法接收这些更改的通知：

- `Start(ctx, operation)`: 当 Compose 操作开始时调用，例如 `up`
- `On(events...)`: 使用单个资源更改的进度事件调用，例如容器启动、镜像拉取
- `Done(operation, success)`: 当操作完成时调用，指示成功或失败

每个事件都包含有关被修改资源的信息、其当前状态以及适用时的进度指示器（例如镜像拉取的下载进度）。

### 事件状态类型

事件报告资源更改时使用以下状态类型：

- Working: 操作正在进行中，例如创建、启动、拉取
- Done: 操作成功完成
- Warning: 操作完成但有警告
- Error: 操作失败

常见的状态文本值包括：`Creating`、`Created`、`Starting`、`Started`、`Running`、`Stopping`、`Stopped`、`Removing`、`Removed`、`Building`、`Built`、`Pulling`、`Pulled` 等。

### 内置 `EventProcessor` 实现

SDK 提供了三种现成可用的 `EventProcessor` 实现：

- `progress.NewTTYWriter(io.Writer)`: 渲染带有进度条和任务列表的交互式终端 UI（类似于 Docker Compose CLI 输出）
- `progress.NewPlainWriter(io.Writer)`: 输出简单的基于文本的进度消息，适用于非交互式环境或日志文件
- `progress.NewJSONWriter()`: 将事件渲染为 JSON 对象
- `progress.NewQuietWriter()`: （默认）静默处理事件，不产生任何输出

使用 `EventProcessor`，可以将自定义 UI 插入到 `docker/compose` 中。