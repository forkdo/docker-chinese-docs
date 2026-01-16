---
title: Docker 沙盒
url: /ai/sandboxes/
parent:
  title: 手册
  url: /manuals/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker 沙盒
    url: /ai/sandboxes/
children:
  - title: Docker Sandbox 快速入门
    url: /ai/sandboxes/get-started/
    description: 在隔离的沙箱环境中运行 Claude Code。包含先决条件和基本命令的快速设置指南。
  - title: 配置 Claude Code
    url: /ai/sandboxes/claude-code/
    description: 了解如何配置 Claude Code 身份验证、传递 CLI 选项，以及使用 Docker 自定义沙盒代理环境。
  - title: 高级配置
    url: /ai/sandboxes/advanced-config/
    description: Docker访问、卷挂载、环境变量、自定义模板和沙箱管理。
  - title: 故障排除
    url: /ai/sandboxes/troubleshooting/
    description: 解决在本地为代理创建沙箱时的常见问题。
---




Docker 沙盒可简化在本地机器上安全运行 AI 代理的过程。
该功能专为使用 Claude Code 等编码代理进行开发的开发者设计，
将代理与您的本地机器隔离，同时保留熟悉的开发体验。
通过 Docker 沙盒，代理可以在容器化的工作区中执行命令、
安装软件包和修改文件，该工作区会镜像您的本地目录。
这让您在获得完整代理自主权的同时，也能确保安全性。

## 工作原理

当您运行 `docker sandbox run <agent>` 时：

1. Docker 从模板镜像创建容器，并将您当前的工作目录以相同路径挂载到容器中。

2. Docker 会发现您的 Git `user.name` 和 `user.email` 配置，并将其注入容器，
   以便代理所做的提交归属于您。

3. 首次运行时，系统会提示您进行身份验证。凭据会存储在 Docker 卷中，
   并在后续的沙盒代理中重复使用。

4. 代理在容器内启动，并启用了绕过权限。

### 工作区挂载

您的工作区目录会以相同的绝对路径（在 macOS 和 Linux 上）挂载到容器中。
例如，主机上的 `/Users/alice/projects/myapp` 在容器中也是
`/Users/alice/projects/myapp`。这意味着：

- 错误消息中的文件路径与主机匹配
- 硬编码路径的脚本能按预期工作
- 对工作区文件的更改在主机和容器上都立即可见

### 每个工作区一个沙盒

Docker 强制每个工作区只能有一个沙盒。当您在同一目录下运行
`docker sandbox run <agent>` 时，Docker 会复用现有的容器。
这意味着状态（已安装的软件包、临时文件）会在该工作区的
多次代理会话中持续保留。

> [!NOTE]
> 要更改沙盒的配置（环境变量、挂载卷等），
> 您需要先移除再重新创建它。详情请参见
> [管理沙盒](advanced-config.md#managing-sandboxes)。

## 发布状态

Docker 沙盒是一项实验性功能。功能和设置可能会发生变化。

请在 GitHub 上报告问题：
- [Docker Desktop for Mac](https://github.com/docker/for-mac)
- [Docker Desktop for Windows](https://github.com/docker/for-win)
- [Docker Desktop for Linux](https://github.com/docker/desktop-linux)

## 开始使用

前往[入门指南](get-started.md)运行您的第一个沙盒代理。
