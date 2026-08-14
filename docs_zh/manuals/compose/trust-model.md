---
title: Compose 文件的信任模型
weight: 70
description: 了解 Docker Compose 如何将 Compose 文件视为受信任的输入，以及在使用非你编写的文件时这意味着什么。
keywords: compose, security, trust model, oci, remote, registry, include, extends, supply chain, trust, best practices
---

Docker Compose 将每个 Compose 文件都视为受信任的输入。当某个 Compose 文件请求提升的权限、主机文件系统访问权限或任何其他配置时，Compose 会按照所写内容应用它。这与直接向 `docker run` 传递标志的行为相同。

这意味着你运行的任何 Compose 文件，无论它位于你的本地文件系统、Git 仓库中，还是 OCI 注册表中，都完全控制着容器与你的主机的交互方式。安全边界不在于文件来自哪里，而在于你是否信任其作者。

评估信任意味着要问：谁编写了这个文件？自你上次审查以来它是否发生了变化？你是否理解它请求的每一项权限？

## 依赖链

一个 Compose 应用程序可以由多个来源组装而成。[`include`](/reference/compose-file/include.md) 指令会导入整个 Compose 文件，而 [`extends`](/reference/compose-file/services.md#extends) 则从另一个文件中的特定服务继承配置。两者都支持远程引用，并且可以链式嵌套：

```text
你的命令
  └─ compose.yaml                                    （本地或远程）
       ├─ services, volumes, networks                （直接配置）
       ├─ include:
       │    └─ oci://registry.example.com/base:v2   （远程依赖）
       │         └─ services, volumes, networks      （间接配置）
       └─ services:
            └─ app:
                 └─ extends:
                      └─ file: oci://registry.example.com/templates:v1
                           └─ service: webapp        （继承的配置）
```

每一层都具有相同的能力。你检查的顶部文件可能看起来是安全的，而嵌套的 `include` 或 `extends` 却引入了具有提升权限、主机绑定挂载或不可信镜像的服务。这些依赖项也可以独立变更。除非你检查完全解析后的输出，否则你永远看不到的嵌套依赖项可能会引入有风险的设置。

> [!IMPORTANT]
>
> 当配置引用远程源时，Compose 会向你发出警告。在理解链中的每一个引用之前，不要接受它。

## 最佳实践

### 检查完整配置

要确切查看 Compose 应用了什么，包括所有已解析的 `includes`、`extends`、合并的覆盖项以及插值变量，请使用：

```console
$ docker compose config
```

对于远程引用：

```console
$ docker compose -f oci://registry.example.com/myapp:latest config
```

在运行 `up` 或 `create` 之前审查此输出，尤其是当配置来自你尚未审计的来源时。

#### 需要留意的字段

Compose 配置对容器与主机的交互方式有着广泛的控制权。以下并非详尽列表，列出了由不可信作者设置时带有安全影响的字段：

| 字段 | 效果 |
|-------|--------|
| `privileged` | 授予容器对主机的完全访问权限 |
| `cap_add` | 添加 Linux 能力，如 `SYS_ADMIN` 或 `NET_RAW` |
| `security_opt` | 配置安全配置文件，包括 seccomp 和 AppArmor |
| `volumes` / 绑定挂载 | 将主机目录挂载到容器中 |
| `network_mode: host` | 共享主机网络栈 |
| `pid: host` | 共享主机 PID 命名空间 |
| `devices` | 将主机设备暴露给容器 |
| `image` | 拉取并运行任意容器镜像 |
| `env_file`、`label_file`、`secrets`/`configs`（`file:`）、`include`、`extends` | 从主机读取文件，可直接读取，也可通过从远程检出解析的符号链接读取，并且在配置加载期间可能暴露其内容 |
| `provider` | 在运行 `up`、`down` 或 `stop` 时，在主机上、任何容器之外运行由 `provider.type` 命名的二进制文件 |

如有疑问，在运行配置之前，先查阅任何不熟悉字段的效果。

与 `volumes` 类似，文件引用字段会读取运行 Compose 的用户可以访问的任何文件，包括通过从远程检出解析的符号链接，并且它们的内容可能在任何容器启动之前就出现在 `docker compose config` 的输出中。Compose 不会将读取限制在项目目录内。请将 Compose 项目视为你运行的代码，而不是你检查的数据。

### CI/CD 环境

自动化流水线尤其敏感，因为它们通常可以访问凭据、云提供商令牌或 Docker 套接字。

- 避免在自动化流水线中引用公共或未经验证的 Compose 配置。
- 将更新置于你正常的代码审查流程之后。
- 尽可能使用只读的 Docker 套接字挂载以降低风险。

### 将远程引用固定到摘要

标签是可变的，这意味着任何具有注册表推送权限的人都可以悄无声息地覆盖一个标签，因此你上周审查过的引用今天可能指向不同的内容。

摘要是不可变的。不要按标签引用，而是固定到摘要。

```yaml
include:
  - oci://registry.example.com/base@sha256:a1b2c3d4...
```

将任何对已固定摘要的更新视为代码变更。在更新引用之前，请确保你已审查新内容。

### 其他

- 使用私有注册表：将 OCI 工件托管在你的组织控制的注册表上。限制谁可以向其推送。
- 审计传递依赖项：检查链中的每一个远程 `include` 和 `extends` 引用，而不仅仅是顶部文件。
- 审查所有 Compose 确认提示：加载远程 Compose 文件时，Compose 会显示插值变量、环境变量值和远程 include 的确认提示。在接受之前请审查这些内容。

## 延伸阅读

- [OCI 工件应用程序](/manuals/compose/how-tos/oci-artifact.md)
- [在生产环境中使用 Compose](/manuals/compose/how-tos/production.md)
- [`include` 参考](/reference/compose-file/include.md)
- [`extends` 参考](/reference/compose-file/services.md#extends)
- [在 Compose 中管理机密信息](/manuals/compose/how-tos/use-secrets.md)
