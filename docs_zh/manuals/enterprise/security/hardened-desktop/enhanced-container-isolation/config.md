---
title: 配置 Docker 套接字异常和高级设置
linkTitle: 配置高级设置
description: 为增强容器隔离配置 Docker 套接字异常和高级设置
keywords: 增强容器隔离, docker socket, 配置, testcontainers, 管理设置
aliases:
- /desktop/hardened-desktop/enhanced-container-isolation/config/
- /security/for-admins/hardened-desktop/enhanced-container-isolation/config/
weight: 20
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

本页介绍如何为增强容器隔离 (ECI) 配置 Docker 套接字异常和其他高级设置。这些配置使受信任的工具（如 Testcontainers）能够在 ECI 下工作，同时保持安全性。

## Docker 套接字挂载权限

默认情况下，增强容器隔离会阻止容器挂载 Docker 套接字，以防止对 Docker 引擎的恶意访问。但是，某些工具需要访问 Docker 套接字。

需要 Docker 套接字访问的常见场景包括：

- 测试框架：管理测试容器的 Testcontainers
- 构建工具：创建临时构建容器的 Paketo buildpacks
- CI/CD 工具：作为部署管道一部分管理容器的工具
- 开发实用程序：用于容器管理的 Docker CLI 容器

## 配置套接字异常

使用设置管理配置 Docker 套接字异常：

{{< tabs >}}
{{< tab name="Admin Console" >}}

1. 登录 [Docker Home](https://app.docker.com)，从左上角的帐户下拉菜单中选择您的组织。
2. 转到 **Admin Console** > **Desktop Settings Management**。
3. [创建或编辑设置策略](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md)。
4. 找到 **Enhanced Container Isolation** 设置。
5. 使用受信任的镜像和命令限制配置 **Docker socket access control**。

{{< /tab >}}
{{< tab name="JSON file" >}}

创建一个 [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 并添加：

```json
{
  "configurationFileVersion": 2,
  "enhancedContainerIsolation": {
    "locked": true,
    "value": true,
    "dockerSocketMount": {
      "imageList": {
        "images": [
          "docker.io/localstack/localstack:*",
          "docker.io/testcontainers/ryuk:*",
          "docker:cli"
        ],
        "allowDerivedImages": true
      },
      "commandList": {
        "type": "deny",
        "commands": ["push", "build"]
      }
    }
  }
}
```

{{< /tab >}}
{{< /tabs >}}

## 镜像允许列表配置

`imageList` 定义了哪些容器镜像可以挂载 Docker 套接字。

### 镜像引用格式

| 格式 | 描述 |
| :---------------------- | :---------- |
| `<image_name>[:<tag>]` | 镜像名称，带有可选标签。如果省略标签，则使用 `:latest` 标签。如果标签是通配符 `*`，则表示“该镜像的任何标签”。 |
| `<image_name>@<digest>` | 镜像名称，带有特定的存储库摘要（例如，由 `docker buildx imagetools inspect <image>` 报告）。这意味着只允许匹配该名称和摘要的镜像。 |

### 配置示例

测试工具的基本允许列表：

```json
"imageList": {
  "images": [
    "docker.io/testcontainers/ryuk:*",
    "docker:cli",
    "alpine:latest"
  ]
}
```

通配符允许列表（Docker Desktop 4.36 及更高版本）：

```json
"imageList": {
  "images": ["*"]
}
```

> [!WARNING]
>
> 使用 `"*"` 允许所有容器挂载 Docker 套接字，这会降低安全性。仅在明确列出允许的镜像不可行时才使用此选项。

### 安全验证

Docker Desktop 通过以下方式验证允许的镜像：

1. 从注册表下载允许镜像的镜像摘要
2. 在容器启动时将容器镜像摘要与允许列表进行比较
3. 阻止摘要与允许镜像不匹配的容器

这可以防止通过重新标记未经授权的镜像来绕过限制：

```console
$ docker tag malicious-image docker:cli
$ docker run -v /var/run/docker.sock:/var/run/docker.sock docker:cli
# 此操作失败，因为摘要与真实的 docker:cli 镜像不匹配
```

## 派生镜像支持

对于像 Paketo buildpacks 这样创建临时本地镜像的工具，您可以允许从受信任的基础镜像派生的镜像。

### 启用派生镜像

```json
"imageList": {
  "images": [
    "paketobuildpacks/builder:base"
  ],
  "allowDerivedImages": true
}
```

当 `allowDerivedImages` 为 true 时，从允许的基础镜像构建的本地镜像（使用 Dockerfile 中的 `FROM`）也将获得 Docker 套接字访问权限。

### 派生镜像要求

- 仅限本地镜像：派生镜像不得存在于远程注册表中
- 基础镜像可用：父镜像必须首先拉取到本地
- 性能影响：验证会使容器启动时间增加最多 1 秒
- 版本兼容性：完全通配符支持需要 Docker Desktop 4.36+

## 命令限制

### 拒绝列表（推荐）

阻止指定的命令，同时允许所有其他命令：

```json
"commandList": {
  "type": "deny",
  "commands": ["push", "build", "image*"]
}
```

### 允许列表

仅允许指定的命令，同时阻止所有其他命令：

```json
"commandList": {
  "type": "allow",
  "commands": ["ps", "container*", "volume*"]
}
```

### 命令通配符

| 通配符 | 阻止/允许 |
| :---------------- | :---------- |
| `"container\*"` | 所有 "docker container ..." 命令 |
| `"image\*"` | 所有 "docker image ..." 命令 |
| `"volume\*"` | 所有 "docker volume ..." 命令 |
| `"network\*"` | 所有 "docker network ..." 命令 |
| `"build\*"` | 所有 "docker build ..." 命令 |
| `"system\*"` | 所有 "docker system ..." 命令 |

### 命令阻止示例

当执行被阻止的命令时：

```console
/ # docker push myimage
Error response from daemon: enhanced container isolation: docker command "/v1.43/images/myimage/push?tag=latest" is blocked; if you wish to allow it, configure the docker socket command list in the Docker Desktop settings.
```

## 常见配置示例

### Testcontainers 设置

用于 Java/Python 测试的 Testcontainers：

```json
"dockerSocketMount": {
  "imageList": {
    "images": [
      "docker.io/testcontainers/ryuk:*",
      "testcontainers/*:*"
    ]
  },
  "commandList": {
    "type": "deny",
    "commands": ["push", "build"]
  }
}
```

### CI/CD 管道工具

用于受控的 CI/CD 容器管理：

```json
"dockerSocketMount": {
  "imageList": {
    "images": [
      "docker:cli",
      "your-registry.com/ci-tools/*:*"
    ]
  },
  "commandList": {
    "type": "allow",
    "commands": ["ps", "container*", "image*"]
  }
}
```

### 开发环境

用于本地开发的 Docker-in-Docker：

```json
"dockerSocketMount": {
  "imageList": {
    "images": [
      "docker:dind",
      "docker:cli"
    ]
  },
  "commandList": {
    "type": "deny",
    "commands": ["system*"]
  }
}
```

## 安全建议

### 镜像允许列表最佳实践

- 严格限制：只允许您绝对信任和需要的镜像
- 谨慎使用通配符：标签通配符 (`*`) 很方便，但不如特定标签安全
- 定期审查：定期审查和更新您的允许列表
- 摘要固定：在关键环境中使用摘要引用以获得最大安全性

### 命令限制

- 默认拒绝：从拒绝列表开始，阻止危险命令，如 `push` 和 `build`
- 最小权限原则：只允许您的工具实际需要的命令
- 监控使用情况：跟踪哪些命令被阻止以优化您的配置

### 监控和维护

- 定期验证：Docker Desktop 更新后测试您的配置，因为镜像摘要可能会更改。
- 处理摘要不匹配：如果允许的镜像被意外阻止：
    ```console
    $ docker image rm <image>
    $ docker pull <image>
    ```

当上游镜像更新时，这可以解决摘要不匹配的问题。

## 下一步

- 查看 [增强容器隔离限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations.md)。
- 查看 [增强容器隔离常见问题解答](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/faq.md)。