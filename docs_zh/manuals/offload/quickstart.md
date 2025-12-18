---
title: Docker Offload 快速开始
linktitle: 快速开始
weight: 10
description: 了解如何使用 Docker Offload 更快地构建和运行容器镜像，无论是在本地还是 CI 环境中。
keywords: cloud, quickstart, Docker Desktop, offload
---

{{< summary-bar feature_name="Docker Offload" >}}

[Docker Offload](./about.md) 允许你在云端构建和运行容器，同时使用你本地的 Docker Desktop 工具和工作流。这意味着更快的构建速度、访问强大的云资源，以及无缝的开发体验。

本快速开始指南涵盖开发者开始使用 Docker Offload 所需的步骤。

> [!NOTE]
>
> 如果你是组织所有者，要开始使用，必须先[注册](https://www.docker.com/products/docker-offload/)并为你的组织订阅 Docker Offload。订阅后，请参阅以下内容：
>
> - [管理 Docker 产品](../admin/organization/manage-products.md) 了解如何为组织中的开发者管理访问权限。
> - [用量和计费](./usage.md) 了解如何设置计费和监控用量。

## 前置条件

- 你必须已安装 [Docker Desktop](/desktop/)。Docker Offload 适用于 Docker Desktop 4.50 或更高版本。
- 你必须有访问 Docker Offload 的权限。你的组织所有者必须已为你的组织[注册](https://www.docker.com/products/docker-offload/)。
- 你的组织必须有可用的承诺用量或已启用按需用量。这由你的组织所有者设置。更多详情，请参阅 [Docker Offload 用量和计费](/offload/usage/)。

## 步骤 1：验证 Docker Offload 访问权限

要访问 Docker Offload，你必须是已订阅 Docker Offload 的组织成员。作为开发者，你可以通过检查 Docker Desktop 仪表板标题中是否出现 Docker Offload 切换开关来验证这一点。

1. 启动 Docker Desktop 并登录。
2. 在 Docker Desktop 仪表板标题中，查找 Docker Offload 切换开关。

![Offload 切换开关](./images/offload-toggle.png)

如果你看到 Docker Offload 切换开关，说明你有访问权限，可以继续下一步。如果你没有看到 Docker Offload 切换开关，请检查 Docker Offload 是否在你的 [Docker Desktop 设置](./configuration.md) 中被禁用，然后联系你的管理员确认你的组织已订阅 Docker Offload，并且已为你的组织启用访问权限。

## 步骤 2：启动 Docker Offload

你可以从 CLI 或 Docker Desktop 仪表板标题中启动 Docker Offload。以下步骤描述如何使用 CLI 启动 Docker Offload。

1. 启动 Docker Desktop 并登录。
2. 打开终端并运行以下命令启动 Docker Offload：

   ```console
   $ docker offload start
   ```

   > [!TIP]
   >
   > 要了解有关 Docker Offload CLI 命令的更多信息，请参阅 [Docker Offload CLI 参考](/reference/cli/docker/offload/)。

3. 如果你是多个有 Docker Offload 访问权限的组织成员，你可以选择一个配置文件。所选组织将负责任何用量。

启动 Docker Offload 后，你会在 Docker Desktop 仪表板标题中看到一个云图标
({{< inline-image src="./images/cloud-mode.png" alt="Offload 模式图标" >}})
，Docker Desktop 仪表板会显示紫色。你可以在终端中运行 `docker offload status` 来检查 Docker Offload 的状态。

## 步骤 3：使用 Docker Offload 运行容器

启动 Docker Offload 后，Docker Desktop 会连接到一个安全的云环境，该环境与你的本地体验相匹配。当你运行构建或容器时，它们会在远程执行，但行为与本地运行完全相同。

要验证 Docker Offload 是否正常工作，请运行一个容器：

```console
$ docker run --rm hello-world
```

如果 Docker Offload 正常工作，你会在终端输出中看到 `Hello from Docker!`。

## 步骤 4：监控你的 Offload 用量

当 Docker Offload 启动并且你已开始会话（例如，你已运行容器）时，你可以在 Docker Desktop 仪表板页脚中沙漏图标
({{< inline-image src="./images/hourglass-icon.png" alt="Offload 会话时长" >}})
旁边看到当前会话时长估算。

此外，当 Docker Offload 启动时，你可以通过在 Docker Desktop 仪表板左侧导航中选择 **Offload** > **Insights** 来查看详细的会话信息。

## 步骤 5：停止 Docker Offload

Docker Offload 在一段时间不活动后会自动[idle](./configuration.md#understand-active-and-idle-states)。你可以随时停止它。要停止 Docker Offload：

```console
$ docker offload stop
```

当你停止 Docker Offload 时，云环境会被终止，所有运行中的容器和镜像都会被删除。当 Docker Offload 空闲约 5 分钟后，环境也会被终止，所有运行中的容器和镜像都会被删除。

要再次启动 Docker Offload，运行 `docker offload start` 命令。

## 接下来

在 Docker Desktop 中配置你的空闲超时。更多信息，请参阅 [配置 Docker Offload](./configuration.md)。