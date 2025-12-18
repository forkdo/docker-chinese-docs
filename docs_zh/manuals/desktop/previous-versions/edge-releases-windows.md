---
description: 每个边缘版本的更新日志/发布说明
keywords: Docker Desktop for Windows, 边缘版本, 发布说明
title: Docker Desktop for Windows 边缘版本发布说明
toc_min: 1
toc_max: 2
aliases:
- /desktop/windows/release-notes/edge-releases/
sitemap: false
---

此页面包含 Docker Desktop 边缘版本的信息。边缘版本为您提供对我们最新功能的早期访问。请注意，其中一些功能可能处于实验阶段，有些可能永远不会到达稳定版本。

有关 Docker Desktop 系统要求，请参阅
[安装前须知](/manuals/desktop/setup/install/windows-install.md#system-requirements)。

## Docker Desktop Community 2.5.4
2020-12-07


### 升级

- [Docker Engine 20.10.0-rc2](https://github.com/docker/docker-ce/blob/master/CHANGELOG.md#20100)
- [Go 1.15.6](https://github.com/golang/go/issues?q=milestone%3AGo1.15.6+label%3ACherryPickApproved+)

### 错误修复和小改动

- 修复了当前用户不是管理员时，后台更新失败的问题。
- 将内核降级到 [4.19.121](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.121-2a1dbedf3f998dac347c499808d7c7e029fbc4d3-amd64/images/sha256-4e7d94522be4f25f1fbb626d5a0142cbb6e785f37e437f6fd4285e64a199883a?context=repo) 以减少 hyperkit 的 CPU 使用率。修复 [docker/for-mac#5044](https://github.com/docker/for-mac/issues/5044)

## Docker Desktop Community 2.5.3
2020-11-30


### 升级

- [Compose CLI v1.0.3](https://github.com/docker/compose-cli/releases/tag/v1.0.3)

## Docker Desktop Community 2.5.2
2020-11-26


### 新增

- 使用三位数版本号。
- 从 Docker Desktop 2.5.2 开始，更新将使用增量补丁，因此会小得多。

### 错误修复和小改动

- 修复了尝试启动一个不存在的容器并使用 `-v /var/run/docker.sock:` 时出现意外 EOF 错误的问题。参见 [docker/for-mac#5025](https://github.com/docker/for-mac/issues/5025)。

## Docker Desktop Community 2.5.1.0
2020-11-18


此版本包含 Kubernetes 升级。注意，安装 Docker Desktop 后，您的本地 Kubernetes 集群将被重置。

### 升级

- [Docker Engine 20.10.0-rc1](https://github.com/docker/docker-ce/blob/master/CHANGELOG.md#20100)
- [Compose CLI v1.0.2](https://github.com/docker/compose-cli/releases/tag/v1.0.2)
- [Snyk v1.424.4](https://github.com/snyk/snyk/releases/tag/v1.424.4)
- [Kubernetes 1.19.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.3)

### 错误修复和小改动

- 将“运行诊断”重命名为“获取支持”。
- 修复了 WSL 2 后端中某些网络插件可能无法加载，导致 Docker 守护进程崩溃的问题。
- 修复了尝试启动一个不存在的容器时出现意外 EOF 错误的问题。参见 [docker/for-mac#5025](https://github.com/docker/for-mac/issues/5025)。

## Docker Desktop Community 2.4.2.0
2020-10-19


### 新增

- 如果您在 Docker Hub 中启用了[漏洞扫描](../../docker-hub/repos/manage/vulnerability-scanning.md)，扫描结果现在将显示在 Docker Desktop 中。

### 升级

- [Docker Engine 20.10.0 beta1](https://github.com/docker/docker-ce/blob/0fc7084265b3786a5867ec311d3f916af7bf7a23/CHANGELOG.md)
- [Docker Compose CLI - 0.1.22](https://github.com/docker/compose-cli/releases/tag/v0.1.22)
- [Linux kernel 5.4.39](https://hub.docker.com/layers/linuxkit/kernel/5.4.39-f39f83d0d475b274938c86eaa796022bfc7063d2/images/sha256-8614670219aca0bb276d4749e479591b60cd348abc770ac9ecd09ee4c1575405?context=explore)
- [Kubernetes 1.19.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.2)
- [Go 1.15.2](https://github.com/golang/go/issues?q=milestone:Go1.15.2+label:CherryPickApproved)

* 弃用
  - Docker Desktop 无法再安装在 Windows 1703（构建版本 15063）上。

### 错误修复和小改动

- 修复了 WSL 2 后端偶尔启动失败的问题。
- 修复了与 NFS 挂载相关的问题。参见 [docker/for-mac#4958](https://github.com/docker/for-mac/issues/4958)。
- 修复了 http 代理排除列表中包含 `localhost` 或 `127.0.0.1` 等条目时的问题。修复 [docker/for-win#8750](https://github.com/docker/for-win/issues/8750)。
- 当 WSL 集成进程意外停止时，现在会通知用户，用户可以决定是否重新启动，而不是循环尝试重新启动。修复 [docker/for-win#8968](https://github.com/docker/for-win/issues/8968)。
- 修复了容器日志在重负载下滞后的问题。修复 [docker/for-win#8216](https://github.com/docker/for-win/issues/8216)。
- 诊断：当 Kubernetes 处于损坏状态时避免挂起。
- 当将文件共享到容器中时（例如 `docker run -v ~/.gitconfig`），Docker Desktop 不会监视父目录。修复 [docker/for-mac#4981](https://github.com/docker/for-mac/issues/4981)。
- 在容器启动时始终同步刷新文件系统缓存。参见 [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943)。

## Docker Desktop Community 2.4.1.0
2020-10-01


### 升级

- [Docker Compose CLI - 0.1.18](https://github.com/docker/compose-cli)
- [Docker Compose 1.27.4](https://github.com/docker/compose/releases/tag/1.27.4)
- [Snyk v1.399.1](https://github.com/snyk/snyk/releases/tag/v1.399.1)
- [Docker Engine 19.03.13](https://github.com/docker/docker-ce/releases/tag/v19.03.13)

### 错误修复和小改动

- 修复了用户名包含空格时安装程序日志文件默认位置路径的问题。修复 [docker/for-win#7941](https://github.com/docker/for-win/issues/7941)。

## Docker Desktop Community 2.3.7.0
2020-09-17


### 新增

- [Amazon ECR Credential Helper](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.4.0)

### 升级

- [Docker ACI integration 0.1.15](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.15)
- [Snyk v0.393.0](https://github.com/snyk/snyk/releases/tag/v1.393.0)

### 错误修复和小改动

**WSL 2**

  - 修复了后端偶尔启动失败的问题。
  - 修复了 glibc 不兼容时代理崩溃的问题。参见 [docker/for-win#8183](https://github.com/docker/for-win/issues/8183)。
  - 修复了重启 Docker Desktop 可能删除容器中挂载文件的问题。
  - 修复了重启 Docker Desktop 时单个文件挂载到容器中会被截断的问题。参见 [docker/for-win#8439](https://github.com/docker/for-win/issues/8439)。

**其他修复**

- 修复了用于低级调试的 VM 调试 shell。
- 修复了与 Go 1.15 客户端的兼容性。参见 [docker/for-mac#4855](https://github.com/docker/for-mac/issues/4855)。
- 避免在 `docker container inspect` 和 `docker volume inspect` 中暴露 `/host_mnt` 路径。修复 [docker/for-mac#4859](https://github.com/docker/for-mac/issues/4859)。
- 修复了容器日志在重负载下滞后的问题。参见 [docker/for-win#8216](https://github.com/docker/for-win/issues/8216)。

### 已知问题

- `clock_gettime64` 系统调用在 i386 镜像中返回 `EPERM` 而不是 `ENOSYS`。要解决此问题，请使用 `--privileged` 标志禁用 `seccomp`。参见 [docker/for-win#8326](https://github.com/docker/for-win/issues/8326)。

## Docker Desktop Community 2.3.6.2
2020-09-09


### 升级

- [Docker Compose 1.27.0](https://github.com/docker/compose/releases/tag/1.27.0)

### 错误修复和小改动

- 修复了 WSL 2 中挂载阴影的问题。参见 [docker/for-win#8183](https://github.com/docker/for-win/issues/8183) 和 [docker/for-win#8316](https://github.com/docker/for-win/issues/8316)。

## Docker Desktop Community 2.3.6.0
2020-09-01


### 新增

- 与 Snyk 合作，Docker Desktop 现在推出本地镜像漏洞扫描功能。
- Docker ECS 插件已被 ECS 云集成取代
- Docker UI：
  - 镜像视图现在具有搜索和过滤选项。
  - 您现在可以使用远程仓库下拉菜单将镜像推送到 Docker Hub。

### 升级

- [Alpine 3.12](https://alpinelinux.org/posts/Alpine-3.12.0-released.html)
- [Kubernetes 1.18.8](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.8)

### 错误修复和小改动

- 修复了 Docker Desktop 与其他 WSL 2 发行版集成的问题。参见 [docker/for-win#6894](https://github.com/docker/for-win/issues/6894)
- 修复了短名称的 DNS 解析问题。参见 [docker/for-win#4425](https://github.com/docker/for-win/issues/4425)

## Docker Desktop Community 2.3.5.1
2020-08-25


### 错误修复和小改动

- 修复了当停止 Docker Desktop 时存在带有绑定挂载的容器会导致 WSL 2 集成中断的问题。参见 [docker/for-win#8164](https://github.com/docker/for-win/issues/8164)

## Docker Desktop Community 2.3.5.0
2020-08-20


### 新增

- Docker 菜单中的 **Images** 视图现在允许您与 Docker Hub 上的镜像交互。您现在可以从 Docker Hub 拉取具有特定标签的远程仓库，或查看 Docker Hub 页面上的仓库详细信息。要访问新的 Images 视图，请从 Docker 菜单中选择 **Dashboard** > **Images**。

- Docker Desktop 现在默认启用 BuildKit，重置为出厂设置后。要恢复到旧的 docker build 体验，请转到 **Preferences** > **Docker Engine**，然后禁用 BuildKit 功能。

- Docker Desktop 现在支持在 Windows 10 版本 1903 和 1909 的最新更新上运行 WSL 2（除了对版本 2004 的现有支持）。这意味着 Docker Desktop 可以安装在这些 Windows 10 Home 的构建版本上。

### 升级

- [Go 1.14.7](https://github.com/golang/go/issues?q=milestone:Go1.14.7+label:CherryPickApproved)
- [Docker ECS integration v1.0.0-beta.5](https://github.com/docker/ecs-plugin/releases/tag/v1.0.0-beta.5)
- [Docker Engine 19.03.13-beta2](https://github.com/docker/docker-ce/releases/tag/v19.03.13-beta2)
- [Docker ACI integration 0.1.12](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.12)

### 错误修复和小改动

- 将 **Dashboard** 移动到鲸鱼菜单的顶部。
- 系统托盘图标现在会响应深色或浅色模式。参见 [docker/for-win#4113](https://github.com/docker/for-win/issues/4113)
- 改进了 `dockerd` 崩溃时的错误处理。
- 修复了 **Images** 视图中的一些小错误。

## Docker Desktop Community 2.3.4.0
2020-07-28


### 新增

- Docker Desktop 在 Docker Dashboard 中引入了新的 **Images** 视图。Images 视图允许用户查看磁盘上的 Docker 镜像列表，将镜像作为容器运行，从 Docker Hub 拉取镜像的最新版本，检查镜像，并从磁盘中删除任何不需要的镜像。

  要访问新的 Images 视图，请从 Docker 菜单中选择 **Dashboard** > **Images**。

### 升级

- [Docker ECS integration v1.0.0-beta.4](https://github.com/docker/ecs-plugin/releases/tag/v1.0.0-beta.4)
- [Kubernetes 1.18.6](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.6)

### 错误修复和小改动

- UI 会根据 Windows 默认应用模式自动切换深色或浅色主题。
- 从仪表板复制容器日志时，不再将 ANSI 颜色代码复制到剪贴板。

## Docker Desktop Community 2.3.3.2
2020-07-21


### 升级

- [Docker ECS integration v1.0.0-beta.2](https://github.com/docker/ecs-plugin/releases/tag/v1.0.0-beta.2)
- [Docker ACI integration 0.1.10](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.10)

## Docker Desktop Community 2.3.3.1
2020-07-10


### 错误修复和小改动

- 修复了 WSL 2 中 ECS 插件不可见的错误。

## Docker Desktop Community 2.3.3.0
2020-07-09


### 升级

- Docker ECS 集成 v1.0.0-beta.1 的测试版发布。
- [Docker ACI integration v0.1.7](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.7)
- [Docker Compose 1.26.2](https://github.com/docker/compose/releases/tag/1.26.2)

### 错误修复和小改动

- Compose-on-Kubernetes 不再包含在 Docker Desktop 安装程序中。您可以从 compose-on-kubernetes [发布页面](https://github.com/docker/compose-on-kubernetes/releases)单独下载。

## Docker Desktop Community 2.3.2.1
2020-06-29


### 安全

- 修复了 Docker Desktop Edge 2.3.2.0 在 Windows 上的回归问题，默认情况下 Docker API 在所有接口上的随机端口上暴露。

## Docker Desktop Community 2.3.2.0
2020-06-25

### 升级

- [Docker 19.03.12](https://github.com/docker/docker-ce/releases/tag/v19.0