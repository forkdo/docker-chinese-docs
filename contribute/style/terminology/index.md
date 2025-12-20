# Docker 术语

#### `compose.yaml`

Compose 文件的当前命名，因为它是一个文件，格式为代码。

#### Compose plugin

作为附加组件（用于 Docker CLI）的 Compose 插件，可以启用/禁用。

#### Digest

每次推送镜像时自动生成的长字符串。你可以通过 Digest 或 Tag 拉取镜像。

#### Docker Compose

当我们谈论该应用程序或与该应用程序相关的所有功能时使用。

#### `docker compose`

在文本和命令使用示例/代码示例中引用命令时使用代码格式。

#### Docker Compose CLI

指 Docker CLI 提供的 Compose 命令系列时使用。

#### K8s

请勿使用。请改用 `Kubernetes`。

#### Multi-platform

（广义）Mac 与 Linux 与 Microsoft，但也指平台架构对，例如 Linux/amd64 和 Linux/arm64；（狭义）Windows/Linux/macOS。

#### Multi-architecture / multi-arch

用于特指 CPU 架构或基于硬件架构的事物时使用。避免将其用作与 multi-platform 相同的含义。

#### Member

Docker Hub 的用户，是组织的一部分。

#### Namespace

组织或用户名。每个镜像都需要一个命名空间才能存在。

#### Node

节点是在 swarm 模式下运行 Docker Engine 实例的物理或虚拟机。
管理节点执行 swarm 管理和编排职责。默认情况下，管理节点也是工作节点。
工作节点调用任务。

#### Registry

Docker 镜像的在线存储。

#### Repository

允许用户与他们的团队、客户或 Docker 社区共享容器镜像。
