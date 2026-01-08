---
title: 启用增强型容器隔离
linkTitle: 启用 ECI
description: 在 Docker Desktop 中启用增强型容器隔离以保护容器安全
keywords: enhanced container isolation, enable eci, container security, docker desktop setup
weight: 15
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

ECI 可在保持开发者完整生产力的同时，防止恶意容器破坏 Docker Desktop。

本页介绍如何开启增强型容器隔离（ECI）并验证其是否正常工作。

## 先决条件

开始前，您必须满足以下条件：

- Docker Business 订阅
- Docker Desktop 4.13 或更高版本
- [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)（仅适用于管理组织范围设置的 administrators）

## 启用增强型容器隔离

### 开发者操作

在 Docker Desktop 设置中开启 ECI：

1. 在 Docker Desktop 中登录您的组织。您的组织必须拥有
Docker Business 订阅。
1. 停止并删除所有现有容器：

    ```console
    $ docker stop $(docker ps -q)
    $ docker rm $(docker ps -aq)
    ```

1. 在 Docker Desktop 中，转到 **Settings** > **General**。
1. 勾选 **Use Enhanced Container Isolation** 复选框。
1. 选择 **Apply and restart**。

> [!IMPORTANT]
>
> ECI 无法保护在开启该功能前已创建的容器。开启 ECI 前请删除现有容器。

### 管理员操作

使用 Settings Management 在组织范围内配置增强型容器隔离：

{{< tabs >}}
{{< tab name="Admin Console" >}}

1. 登录 [Docker Home](https://app.docker.com) 并从左上角账户下拉菜单中选择您的组织。
1. 转到 **Admin Console** > **Desktop Settings Management**。
1. [创建或编辑设置策略](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md)。
1. 将 **Enhanced Container Isolation** 设置为 **Always enabled**。

{{< /tab >}}
{{< tab name="JSON file" >}}

1. 创建 [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 并添加：

      ```json
      {
        "configurationFileVersion": 2,
        "enhancedContainerIsolation": {
          "value": true,
          "locked": true
        }
      }
      ```

1. 根据需要配置以下选项：
    - `"value": true`：默认开启 ECI（必需）
    - `"locked": true`：防止开发者关闭 ECI
    - `"locked": false`：允许开发者控制该设置

{{< /tab >}}
{{< /tabs >}}

### 应用配置

ECI 设置生效需满足以下条件：

- 新安装：用户启动 Docker Desktop 并登录
- 现有安装：用户必须完全退出 Docker Desktop 并重新启动

> [!IMPORTANT]
>
> 仅从 Docker Desktop 菜单重启不够。用户必须完全退出并重新打开 Docker Desktop。

您还可以为需要 Docker API 访问的可信镜像配置 [Docker socket 挂载权限](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md)。

## 验证增强型容器隔离是否已激活

开启 ECI 后，请通过以下方法验证其是否正常工作。

### 检查用户命名空间映射

运行容器并检查用户命名空间映射：

```console
$ docker run --rm alpine cat /proc/self/uid_map
```

ECI 开启时：

```text
0     100000      65536
```

这表示容器 root 用户 (0) 映射到 Docker Desktop VM 中的非特权用户 (100000)，用户 ID 范围为 64K。每个容器获得专属用户 ID 范围以实现隔离。

ECI 关闭时：

```text
0          0 4294967295
```

这表示容器 root 用户 (0) 直接映射到 VM root 用户 (0)，隔离性较弱。

### 检查容器运行时

验证正在使用的容器运行时：

```console
$ docker inspect --format='{{.HostConfig.Runtime}}' <container_name>
```

ECI 开启时返回 `sysbox-runc`。ECI 关闭时返回
`runc`。

### 测试安全限制

验证 ECI 安全限制是否生效。

测试命名空间共享：

```console
$ docker run -it --rm --pid=host alpine
```

ECI 开启时，此命令会因 Sysbox 容器无法与主机共享命名空间而失败。

测试 Docker socket 访问：

```console
$ docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock alpine
```

ECI 开启时，此命令会失败，除非您已为可信镜像配置 Docker socket 例外。

## 强制 ECI 时用户看到的内容

当管理员通过 Settings Management 强制实施增强型容器隔离时：

- **Use Enhanced Container Isolation** 设置在 Docker Desktop 设置中显示为开启状态。
- 若设置为 `"locked": true`，该设置将被锁定并置灰。
- 所有新容器自动使用 Linux 用户命名空间。
- 现有开发工作流无需修改即可继续运行。
- 用户在 `docker inspect` 输出中看到 `sysbox-runc` 作为容器运行时。

## 后续步骤

- 查看 [配置 Docker socket 例外和高级设置](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md)。
- 查看 [增强型容器隔离限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations.md)。