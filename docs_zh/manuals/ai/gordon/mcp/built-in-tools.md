---
title: Gordon 中的内置工具
description: 使用和配置 Gordon 的内置工具，用于 Docker、Kubernetes、安全性和开发工作流
keywords: ai, mcp, gordon, docker, kubernetes, security, developer tools, toolbox, configuration, usage
aliases:
 - /desktop/features/gordon/mcp/built-in-tools/
---

Gordon 包含一个集成的工具箱，可让您访问系统工具和功能。这些工具扩展了 Gordon 的功能，使您能够与 Docker Engine、Kubernetes、Docker Scout 安全扫描以及其他开发人员工具进行交互。本文档描述了可用的工具、如何配置它们以及使用模式。

## 配置工具

在工具箱中全局配置工具，使其在整个 Gordon 中可用，包括 Docker Desktop 和 CLI。

配置工具的步骤：

1. 在 Docker Desktop 的 **Ask Gordon** 视图中，选择输入区域左下角的 **Toolbox** 按钮。

   ![截图显示 Gordon 页面和工具箱按钮。](../images/gordon.png)

1. 要启用或禁用工具，请在左侧菜单中选择它，然后切换开关。

   ![截图显示 Gordon 的工具箱。](../images/toolbox.png)

   有关 Docker 工具的更多信息，请参阅 [参考](#reference)。

## 使用示例

本节展示您可以使用 Gordon 工具执行的常见任务。

### 管理 Docker 容器

#### 列出和监控容器

```console
# 列出所有正在运行的容器
$ docker ai "Show me all running containers"

# 列出使用特定资源的容器
$ docker ai "List all containers using more than 1GB of memory"

# 查看特定容器的日志
$ docker ai "Show me logs from my running api-container from the last hour"
```

#### 管理容器生命周期

```console
# 运行新容器
$ docker ai "Run a nginx container with port 80 exposed to localhost"

# 停止特定容器
$ docker ai "Stop my database container"

# 清理未使用的容器
$ docker ai "Remove all stopped containers"
```

### 使用 Docker 镜像

```console
# 列出可用镜像
$ docker ai "Show me all my local Docker images"

# 拉取特定镜像
$ docker ai "Pull the latest Ubuntu image"

# 从 Dockerfile 构建镜像
$ docker ai "Build an image from my current directory and tag it as myapp:latest"

# 清理未使用的镜像
$ docker ai "Remove all my unused images"
```

### 管理 Docker 卷

```console
# 列出卷
$ docker ai "List all my Docker volumes"

# 创建新卷
$ docker ai "Create a new volume called postgres-data"

# 将容器数据备份到卷
$ docker ai "Create a backup of my postgres container data to a new volume"
```

### 执行 Kubernetes 操作

```console
# 创建部署
$ docker ai "Create an nginx deployment and make sure it's exposed locally"

# 列出资源
$ docker ai "Show me all deployments in the default namespace"

# 获取日志
$ docker ai "Show me logs from the auth-service pod"
```

### 执行安全分析

```console
# 扫描 CVE
$ docker ai "Scan my application for security vulnerabilities"

# 获取安全建议
$ docker ai "Give me recommendations for improving the security of my nodejs-app image"
```

### 使用开发工作流

```console
# 分析并提交更改
$ docker ai "Look at my local changes, create multiple commits with sensible commit messages"

# 查看分支状态
$ docker ai "Show me the status of my current branch compared to main"
```

## 参考

本节列出了 Gordon 工具箱中的内置工具。

### Docker 工具

与 Docker 容器、镜像和卷进行交互。

#### 容器管理

<!-- vale off -->

| 名称          | 描述                      |
|---------------|----------------------------------|
| `docker`      | 访问 Docker CLI            |
| `list_builds` | 列出 Docker 守护进程中的构建 |
| `build_logs`  | 显示构建日志                  |

#### 卷管理

| 工具           | 描述                |
|----------------|---------------------------|
| `list_volumes` | 列出所有 Docker 卷   |
| `remove_volume`| 删除 Docker 卷    |
| `create_volume`| 创建新的 Docker 卷|

#### 镜像管理

| 工具           | 描述                    |
|----------------|-------------------------------|
| `list_images`  | 列出所有 Docker 镜像         |
| `remove_images`| 删除 Docker 镜像           |
| `pull_image`   | 从注册表拉取镜像  |
| `push_image`   | 推送镜像到注册表    |
| `build_image`  | 构建 Docker 镜像           |
| `tag_image`    | 为 Docker 镜像打标签             |
| `inspect`      | 检查 Docker 对象        |

### Kubernetes 工具

与您的 Kubernetes 集群进行交互。

#### Pod 管理

| 工具           | 描述                        |
|----------------|------------------------------------|
| `list_pods`    | 列出集群中的所有 Pod       |
| `get_pod_logs` | 从特定 Pod 获取日志       |

#### 部署管理

| 工具               | 描述                        |
|--------------------|------------------------------------|
| `list_deployments` | 列出所有部署               |
| `create_deployment`| 创建新部署            |
| `expose_deployment`| 将部署作为服务暴露   |
| `remove_deployment`| 删除部署                |

#### 服务管理

| 工具           | 描述                |
|----------------|---------------------------|
| `list_services`| 列出所有服务         |
| `remove_service`| 删除服务         |

#### 集群信息

| 工具             | 描述                  |
|------------------|-----------------------------|
| `list_namespaces`| 列出所有命名空间         |
| `list_nodes`     | 列出集群中的所有节点|

### Docker Scout 工具

由 Docker Scout 提供支持的安全分析。

| 工具                           | 描述                                                                                                             |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| `search_for_cves`              | 使用 Docker Scout CVE 分析 Docker 镜像、项目目录或其他工件中的漏洞。              |
| `get_security_recommendations` | 使用 Docker Scout 分析 Docker 镜像、项目目录或其他工件，获取基础镜像更新建议。 |

### 开发人员工具

通用开发实用工具。

| 工具              | 描述                      |
|-------------------|----------------------------------|
| `fetch`           | 从 URL 检索内容      |
| `get_command_help`| 获取 CLI 命令的帮助        |
| `run_command`     | 执行 shell 命令           |
| `filesystem`      | 执行文件系统操作    |
| `git`             | 执行 git 命令             |

### AI 模型工具

| 工具           | 描述                        |
|----------------|------------------------------------|
| `list_models`  | 列出所有可用的 Docker 模型   |
| `pull_model`   | 下载 Docker 模型            |
| `run_model`    | 使用提示查询模型        |
| `remove_model` | 删除 Docker 模型              |

### Docker MCP 目录

如果您启用了 [MCP Toolkit 功能](../../mcp-catalog-and-toolkit/_index.md)，
所有您已启用和配置的工具都可供 Gordon 使用。