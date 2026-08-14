---
title: BuildKit
weight: 100
description: BuildKit 简介与概述
keywords: build, buildkit
---

[BuildKit](https://github.com/moby/buildkit) 是 Docker 使用的构建器后端。与早期 Docker 版本中使用的旧版构建器相比，BuildKit 提供了改进的功能，并提升了构建性能。它还新增了对更复杂场景的支持：

- 检测并跳过执行未使用的构建阶段
- 并行构建相互独立的构建阶段
- 在构建之间仅增量传输你 [构建上下文](../concepts/context.md) 中发生更改的文件
- 检测并跳过传输你 [构建上下文](../concepts/context.md) 中未使用的文件
- 使用具有许多额外功能的 [Dockerfile 前端](frontend.md) 实现
- 避免对 API 其余部分（中间镜像与容器）产生副作用
- 优先处理你的构建缓存以进行自动修剪

BuildKit 相比旧版构建器主要改进的领域是性能、存储管理和可扩展性。从性能方面来看，一个重要的更新是完全并发的构建图求解器。它可以在可能时并行运行构建步骤，并优化掉对最终结果没有影响的命令。对本地源文件的访问也得到了优化。通过仅在重复构建调用之间跟踪对这些文件所做的更新，无需在可以开始工作之前等待读取或上传本地文件。

## LLB

BuildKit 的核心是一种 [低级构建（LLB）](https://github.com/moby/buildkit#exploring-llb) 定义格式。LLB 是一种中间二进制格式，允许开发者扩展 BuildKit。LLB 定义了一个内容可寻址的依赖图，可用于组合复杂的构建定义。它还支持 Dockerfile 中未暴露的功能，例如直接数据挂载和嵌套调用。

{{< figure src="../images/buildkit-dag.svg" class="invertible" >}}

关于构建的执行和缓存的一切都在 LLB 中定义。与旧版构建器相比，缓存模型被完全重写。LLB 不再使用启发式方法来比较镜像，而是直接跟踪构建图 checksum 以及挂载到特定操作的内容。这使得它更快、更精确且可移植。构建缓存甚至可以导出到镜像仓库，供后续在任何主机上的调用按需拉取。

LLB 可以使用 [golang 客户端包](https://pkg.go.dev/github.com/moby/buildkit/client/llb) 直接生成，该包允许使用 Go 语言原语定义构建操作之间的关系。这赋予了你运行任何你能想到的东西的全部能力，但很可能不是大多数人定义其构建的方式。相反，大多数用户会使用前端组件或 LLB 嵌套调用来运行一组预先准备好的构建步骤。

## Frontend

前端（frontend）是一个组件，它接受人类可读的构建格式并将其转换为 LLB，以便 BuildKit 执行它。前端可以作为镜像分发，用户可以指定某个特定版本的前端，以保证对其定义所使用的功能有效。

例如，要使用 BuildKit 构建 [Dockerfile](/reference/dockerfile.md)，你需要 [使用外部 Dockerfile 前端](frontend.md)。

## Getting started

BuildKit 是 Docker Desktop 和 Docker Engine 用户的默认构建器。如果你正在构建 Windows 容器，则会改用旧版构建器。

## BuildKit on Windows

> [!WARNING]
>
> BuildKit 仅完全支持构建 Linux 容器。对 Windows 容器的支持是实验性的。

BuildKit 从 0.13 版本开始实验性地支持 Windows 容器（WCOW）。本节将引导你完成试用步骤。若要分享反馈，请 [在仓库中提交 issue](https://github.com/moby/buildkit/issues/new)，尤其是关于 `buildkitd.exe` 的反馈。

### Known limitations

有关 BuildKit on Windows 相关未解决 bug 和限制的信息，请参阅 [GitHub issues](https://github.com/moby/buildkit/issues?q=is%3Aissue%20state%3Aopen%20label%3Aarea%2Fwindows-wcow)。

### Prerequisites

- 架构：`amd64`、`arm64`（有二进制文件但官方尚未测试）。
- 受支持的 OS：Windows Server 2019、Windows Server 2022、Windows 11。
- 基础镜像：`ServerCore:ltsc2019`、`ServerCore:ltsc2022`、`NanoServer:ltsc2022`。
  请参阅 [兼容性对照表](https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility?tabs=windows-server-2019%2Cwindows-11#windows-server-host-os-compatibility)。
- Docker Desktop 4.29 或更高版本

### Steps

> [!NOTE]
>
> 以下命令需要在 PowerShell 终端中以管理员（提升后的）权限运行。

1. 启用 **Hyper-V** 和 **Containers** Windows 功能。

   ```console
   > Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V, Containers -All
   ```

   如果你看到的 `RestartNeeded` 为 `True`，请重启机器并以管理员身份重新打开 PowerShell 终端。否则，继续下一步。

2. 在 Docker Desktop 中切换到 Windows 容器。

   选择任务栏中的 Docker 图标，然后选择 **Switch to Windows containers...**。

3. 按照 [设置说明](https://github.com/containerd/containerd/blob/main/docs/getting-started.md#installing-containerd-on-windows) 安装 containerd 1.7.7 或更高版本。

4. 下载并解压最新的 BuildKit 发布版本。

   ```powershell
   $version = "v0.22.0" # 指定发布版本，v0.13+
   $arch = "amd64" # arm64 二进制文件也可用
   curl.exe -LO https://github.com/moby/buildkit/releases/download/$version/buildkit-$version.windows-$arch.tar.gz
   # containerd 说明可能会生成另一个 `.\bin` 目录
   # 你可以移动这些文件
   mv bin bin2
   tar.exe xvf .\buildkit-$version.windows-$arch.tar.gz
   ## x bin/
   ## x bin/buildctl.exe
   ## x bin/buildkitd.exe
   ```

5. 将 BuildKit 二进制文件安装到 `PATH` 中。

   ```powershell
   # 二进制文件解压到 bin 目录后
   # 将它们移动到 $Env:PATH 目录中的适当路径，或者：
   Copy-Item -Path ".\bin" -Destination "$Env:ProgramFiles\buildkit" -Recurse -Force
   # 将 `buildkitd.exe` 和 `buildctl.exe` 二进制文件加入 $Env:PATH
   $Path = [Environment]::GetEnvironmentVariable("PATH", "Machine") + `
       [IO.Path]::PathSeparator + "$Env:ProgramFiles\buildkit"
   [Environment]::SetEnvironmentVariable( "Path", $Path, "Machine")
   $Env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + `
       [System.Environment]::GetEnvironmentVariable("Path","User")
   ```

6. 启动 BuildKit 守护进程。

   ```console
   > buildkitd.exe
   ```

   > [!NOTE]
   > 如果你正在运行 *由 dockerd 管理的* `containerd` 进程，请改用该进程，通过提供地址：
   > `buildkitd.exe --containerd-worker-addr "npipe:////./pipe/docker-containerd"`

7. 在另一个具有管理员权限的终端中，创建一个使用本地 BuildKit 守护进程的远程构建器。

   > [!NOTE]
   >
   > 这需要 Docker Desktop 4.29 或更高版本。

   ```console
   > docker buildx create --name buildkit-exp --use --driver=remote npipe:////./pipe/buildkitd
   buildkit-exp
   ```

8. 通过运行 `docker buildx inspect` 验证构建器连接。

   ```console
   > docker buildx inspect
   ```

   输出应表明构建器平台为 Windows，且构建器端点是一个命名管道。

   ```text
   Name:          buildkit-exp
    Driver:        remote
    Last Activity: 2024-04-15 17:51:58 +0000 UTC
    Nodes:
    Name:             buildkit-exp0
    Endpoint:         npipe:////./pipe/buildkitd
    Status:           running
    BuildKit version: v0.13.1
    Platforms:        windows/amd64
   ...
   ```

9. 创建一个 Dockerfile 并构建 `hello-buildkit` 镜像。

   ```console
   > mkdir sample_dockerfile
   > cd sample_dockerfile
   > Set-Content Dockerfile @"
   FROM mcr.microsoft.com/windows/nanoserver:ltsc2022
   USER ContainerAdministrator
   COPY hello.txt C:/
   RUN echo "Goodbye!" >> hello.txt
   CMD ["cmd", "/C", "type C:\\hello.txt"]
   "@
   Set-Content hello.txt @"
   Hello from BuildKit!
   This message shows that your installation appears to be working correctly.
   "@
   ```

10. 构建并将镜像推送到镜像仓库。

    ```console
    > docker buildx build --push -t <username>/hello-buildkit .
    ```

11. 推送到镜像仓库后，使用 `docker run` 运行该镜像。

    ```console
    > docker run <username>/hello-buildkit
    ```
