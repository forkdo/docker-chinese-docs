---
title: 如何备份和恢复 Docker Desktop 数据
linkTitle: 备份和恢复数据
keywords: Docker Desktop, backup, restore, migration, reinstall, containers, images,
  volumes
weight: 20
aliases:
 - /desktop/backup-and-restore/
---

使用此流程可以备份和恢复您的镜像和容器数据。这在您需要重置虚拟机磁盘、将 Docker 环境迁移到新计算机，或从 Docker Desktop 更新或安装失败中恢复时非常有用。

> [!IMPORTANT]
>
> 如果您使用卷或绑定挂载来存储容器数据，可能不需要备份容器，但请务必记住创建容器时使用的选项，或使用 [Docker Compose 文件](/reference/compose-file/_index.md)以便在重新安装后以相同配置重新创建容器。

## 如果 Docker Desktop 运行正常

### 保存数据

1. 使用 [`docker container commit`](/reference/cli/docker/container/commit.md) 将容器提交为镜像。

   提交容器会将文件系统更改和某些容器配置（如标签和环境变量）存储为本地镜像。请注意，环境变量可能包含敏感信息（如密码或代理认证），因此在将结果镜像推送到注册表时需谨慎。

   另外请注意，附加到容器的卷中的文件系统更改不会包含在镜像中，必须单独备份。

   如果您使用了[命名卷](/manuals/engine/storage/_index.md#more-details-about-mount-types)来存储容器数据（如数据库），请参考存储部分的[备份、恢复或迁移数据卷](/manuals/engine/storage/volumes.md#back-up-restore-or-migrate-data-volumes)页面。

2. 使用 [`docker push`](/reference/cli/docker/image/push.md) 将您在本地构建并希望保留的任何镜像推送到 [Docker Hub 注册表](/manuals/docker-hub/_index.md)。
   
   > [!TIP]
   >
   > 如果您的镜像包含敏感内容，[将仓库可见性设置为私有](/manuals/docker-hub/repos/_index.md)。

   或者，使用 [`docker image save -o images.tar image1 [image2 ...]`](/reference/cli/docker/image/save.md) 将您希望保留的任何镜像保存到本地 `.tar` 文件中。

备份数据后，您可以卸载当前版本的 Docker Desktop 并[安装不同版本](/manuals/desktop/release-notes.md)或重置 Docker Desktop 为出厂默认设置。

### 恢复数据

1. 加载您的镜像。

   - 如果您推送到 Docker Hub：
   
      ```console
      $ docker pull <my-backup-image>
      ```
   
   - 如果您保存了 `.tar` 文件：
   
      ```console
      $ docker image load -i images.tar
      ```

2. 如有必要，使用 [`docker run`](/reference/cli/docker/container/run.md) 或 [Docker Compose](/manuals/compose/_index.md) 重新创建容器。

要恢复卷数据，请参考[备份、恢复或迁移数据卷](/manuals/engine/storage/volumes.md#back-up-restore-or-migrate-data-volumes)。 

## 如果 Docker Desktop 无法启动

如果 Docker Desktop 无法启动且必须重新安装，您可以直接从磁盘备份其 VM 磁盘和镜像数据。在备份这些文件之前，Docker Desktop 必须完全停止。

{{< tabs >}}
{{< tab name="Windows" >}}

1. 备份 Docker 容器/镜像。

   备份以下文件：

   ```console
   %LOCALAPPDATA%\Docker\wsl\data\docker_data.vhdx
   ```

   将其复制到安全位置。

1. 备份 WSL 发行版。

   如果您运行任何 WSL Linux 发行版（Ubuntu、Alpine 等），请使用 [Microsoft 指南](https://learn.microsoft.com/en-us/windows/wsl/faq#how-can-i-back-up-my-wsl-distributions-) 备份它们。

1. 恢复。

   重新安装 Docker Desktop 后，将 `docker_data.vhdx` 恢复到相同位置，并在需要时重新导入您的 WSL 发行版。

{{< /tab >}}
{{< tab name="Mac" >}}

1. 备份 Docker 容器/镜像。

   备份以下文件：

   ```console
   ~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw
   ```

   将其复制到安全位置。

1. 恢复。

   重新安装 Docker Desktop 后，将 `Docker.raw` 恢复到相同位置。

{{< /tab >}}
{{< tab name="Linux" >}}

1. 备份 Docker 容器/镜像：

   备份以下文件：

   ```console
   ~/.docker/desktop/vms/0/data/Docker.raw
   ```

   将其复制到安全位置。

1. 恢复。

   重新安装 Docker Desktop 后，将 `Docker.raw` 恢复到相同位置。

{{< /tab >}}
{{< /tabs >}}