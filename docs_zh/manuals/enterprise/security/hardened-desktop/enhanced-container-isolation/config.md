---
title: 配置 Docker 套接字例外和高级设置
linkTitle: 配置高级设置
description: 为增强容器隔离配置 Docker 套接字例外和高级设置
keywords: 增强容器隔离, docker 套接字, 配置, testcontainers, 管理员设置
aliases:
 - /desktop/hardened-desktop/enhanced-container-isolation/config/
 - /security/for-admins/hardened-desktop/enhanced-container-isolation/config/
weight: 20
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

本页面展示了如何为增强容器隔离（ECI）配置 Docker 套接字例外和其他高级设置。这些配置使 Testcontainers 等受信任的工具能够在保持安全的同时与 ECI 协同工作。

## Docker 套接字挂载权限

默认情况下，增强容器隔离会阻止容器挂载 Docker 套接字，以防止对 Docker Engine 的恶意访问。但是，某些工具需要 Docker 套接字访问。

需要 Docker 套接字访问的常见场景包括：

- 测试框架：管理测试容器的 Testcontainers
- 构建工具：创建临时构建容器的 Paketo buildpacks
- CI/CD 工具：作为部署流水线一部分管理容器的工具
- 开发工具：用于容器管理的 Docker CLI 容器

## 配置套接字例外

使用设置管理配置 Docker 套接字例外：

{{< tabs >}}
{{< tab name="Admin Console" >}}

1. 登录 [Docker Home](https://app.docker.com)，从左上角账户下拉菜单中选择您的组织。
1. 转到 **Admin Console** > **Desktop Settings Management**。
1. [创建或编辑设置策略](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md)。
1. 找到 **Enhanced Container Isolation** 设置。
1. 使用您的受信任镜像和命令限制配置 **Docker socket access control**。

{{< /tab >}}
{{< tab name="JSON file" >}}

创建 [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 并添加：

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

## 镜像白名单配置

`imageList` 定义了哪些容器镜像可以挂载 Docker 套接字。

### 镜像引用格式

| 格式  | 描述 |
| :---------------------- | :---------- |
| `<image_name>[:<tag>]`  | 镜像名称，可选标签。如果省略标签，则使用 `:latest` 标签。如果标签是通配符 `*`，则表示"该镜像的任何标签"。 |
| `<image_name>@<digest>` | 镜像名称，带有特定仓库摘要（例如，由 `docker buildx imagetools inspect <image>` 报告）。这意味着只有匹配该名称和摘要的镜像才被允许。 |

### 配置示例

测试工具的基本白名单：

```json
"imageList": {
  "images": [
    "docker.io/testcontainers/ryuk:*",
    "docker:cli",
    "alpine:latest"
  ]
}
```

通配符白名单（Docker Desktop 4.36 及以后版本）：

```json
"imageList": {
  "images": ["*"]
}
```

> [!WARNING]
>
> 使用 `"*"` 允许所有容器挂载 Docker 套接字，这会降低安全性。仅在无法明确列出允许镜像时使用此配置。

### 安全验证

Docker Desktop 通过以下方式验证允许的镜像：

1. 从注册表下载允许镜像的摘要
1. 容器启动时将容器镜像摘要与白名单进行比较
1. 阻止摘要不匹配允许镜像的容器

这防止了通过重新标记未授权镜像来绕过限制：

```console
$ docker tag malicious-image docker:cli
$ docker run -v /var/run/docker.sock:/var/run/docker.sock docker:cli
# 这会失败，因为摘要不匹配真实的 docker:cli 镜像
```

## 衍生镜像支持

对于 Paketo buildpacks 等创建临时本地镜像的工具，您可以允许从受信任基础镜像派生的镜像。

### 启用衍生镜像

```json
"imageList": {
  "images": [
    "paketobuildpacks/builder:base"
  ],
  "allowDerivedImages": true
}
```

当 `allowDerivedImages` 为 true 时，从允许的基础镜像（在 Dockerfile 中使用 `FROM`）构建的本地镜像也能获得 Docker 套接字访问权限。

### 衍生镜像要求

- 仅限本地镜像：衍生镜像不能存在于远程注册表中
- 基础镜像可用：父镜像必须首先在本地拉取
- 性能影响：容器启动验证最多增加 1 秒
- 版本兼容性：完整通配符支持需要 Docker Desktop 4.36+

## 命令限制

### 拒绝列表（推荐）

阻止指定命令，同时允许所有其他命令：

```json
"commandList": {
  "type": "deny",
  "commands": ["push", "build", "image*"]
}
```

### 允许列表

仅允许指定命令，同时阻止所有其他命令：

```json
"commandList": {
  "type": "allow",
  "commands": ["ps", "container*", "volume*"]
}
```

### 命令通配符

| 通配符 | 阻止/允许 |
| :---------------- | :---------- |
| `"container\*"`     | 所有 "docker container ..." 命令 |
| `"image\*"`         | 所有 "docker image ..." 命令 |
| `"volume\*"`        | 所有 "docker volume ..." 命令 |
| `"network\*"`       | 所有 "docker network ..." 命令 |
| `"build\*"`         | 所有 "docker build ..." 命令 |
| `"system\*"`        | 所有 "docker system ..." 命令 |

### 命令阻止示例

执行被阻止的命令时：

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

用于受控 CI/CD 容器管理：

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

用于带 Docker-in-Docker 的本地开发：

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

### 镜像白名单最佳实践

- 限制严格：仅允许您绝对信任和需要的镜像
- 谨慎使用通配符：标签通配符（`*`）很方便，但不如特定标签安全
- 定期审查：定期审查和更新您的白名单
- 摘要固定：在关键环境中使用摘要引用以获得最大安全性

### 命令限制

- 默认拒绝：从拒绝列表开始，阻止 `push` 和 `build` 等危险命令
- 最小权限原则：仅允许您的工具实际需要的命令
- 监控使用情况：跟踪被阻止的命令以优化您的配置

### 监控和维护

- 定期验证：在 Docker Desktop 更新后测试您的配置，因为镜像摘要可能已更改
- 处理摘要不匹配：如果允许的镜像意外被阻止：
    ```console
    $ docker image rm <image>
    $ docker pull <image>
    ```

这解决了上游镜像更新时的摘要不匹配问题。

## 下一步

- 查看 [增强容器隔离限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations.md)。
- 查看 [增强容器隔离常见问题](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/faq.md)。