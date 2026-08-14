---
title: 使用构建策略
linkTitle: 用法
description: 将策略应用到构建中，并以迭代方式开发策略
keywords: build policies, policy eval, docker buildx, policy development, debugging
weight: 20
---

构建策略在构建执行之前验证输入。本指南介绍如何使用 `docker buildx build` 和 `docker buildx bake` 以迭代方式开发策略并将其应用到真实构建中。

## 先决条件

- Buildx 0.31.0 或更高版本 - 检查你的版本：`docker buildx version`
- BuildKit 0.26.0 或更高版本 - 通过以下命令验证：`docker buildx inspect --bootstrap`

如果你使用的是 Docker Desktop，请确保你使用的版本包含这些更新。

## 策略开发工作流

Buildx 会自动加载与你的 Dockerfile 名称匹配的策略。当你使用 `Dockerfile` 构建时，Buildx 会在同一目录中查找 `Dockerfile.rego`。对于名为 `app.Dockerfile` 的文件，它会查找 `app.Dockerfile.rego`。有关配置选项和手动策略加载，请参阅 [进阶：策略配置](#advanced-policy-configuration) 部分。

编写策略是一个迭代的过程：

1. 从基本的默认拒绝策略开始。
2. 使用调试日志构建，查看你的 Dockerfile 使用了哪些输入。
3. 根据调试输出添加规则以允许特定来源。
4. 测试并完善。

### 查看来自 Dockerfile 的输入

要查看你的 Dockerfile 引用的输入（镜像、Git 仓库、HTTP 下载），请使用调试日志构建：

```console
$ docker buildx build --progress=plain --policy log-level=debug .
```

镜像源的示例输出：

```text
#1 0.010 checking policy for source docker-image://alpine:3.19 (linux/arm64)
#1 0.011 policy input: {
#1 0.011   "env": {
#1 0.011     "filename": "."
#1 0.011   },
#1 0.011   "image": {
#1 0.011     "ref": "docker.io/library/alpine:3.19",
#1 0.011     "host": "docker.io",
#1 0.011     "repo": "alpine",
#1 0.011     "tag": "3.19",
#1 0.011     "platform": "linux/arm64"
#1 0.011   }
#1 0.011 }
#1 0.011 unknowns for policy evaluation: [input.image.checksum input.image.labels ...]
#1 0.012 policy decision for source docker-image://alpine:3.19: ALLOW
```

这显示了完整的输入结构、哪些字段未解析，以及每个源的策略决策。有关所有可用字段，请参阅 [输入参考](./inputs.md)。

### 使用 policy eval 测试策略

使用 [`docker buildx policy eval`](/reference/cli/docker/buildx/policy/eval/) 来测试你的策略是否允许某个特定源，而无需运行完整构建。

注意：`docker buildx policy eval` 测试作为参数指定的源。它不会解析你的 Dockerfile 来评估所有输入——要做到这一点，请 [使用 --progress=plain 构建](#viewing-inputs-from-your-dockerfile)。

测试你的策略是否允许本地上下文：

```console
$ docker buildx policy eval .
```

没有输出意味着策略允许了该源。如果被拒绝，你会看到：

```console
ERROR: policy denied
```

测试其他源：

```console
$ docker buildx policy eval https://example.com              # 测试 HTTP
$ docker buildx policy eval https://github.com/org/repo.git  # 测试 Git
```

默认情况下，`--print` 显示从源字符串解析出的引用信息（如 `repo`、`tag`、`host`），而不从镜像仓库获取。要检查需要获取源才能得到的元数据（如 `labels`、`checksum` 或 `hasProvenance`），请使用 `--fields` 指定要获取的字段：

```console
$ docker buildx policy eval --print --fields image.labels docker-image://alpine:3.19
```

多个字段可以指定为逗号分隔的列表。

### 迭代开发示例

以下是开发策略的实用工作流：

1. 从基本的默认拒绝策略开始：

   ```rego {title="Dockerfile.rego"}
   package docker

   default allow := false

   allow if input.local

   decision := {"allow": allow}
   ```

2. 使用调试日志构建，查看你的 Dockerfile 使用了哪些输入：

   ```console
   $ docker buildx build --progress=plain --policy log-level=debug .
   ```

   输出显示了被拒绝的镜像及其输入结构：

   ```text
   #1 0.026 checking policy for source docker-image://docker.io/library/alpine:3.19
   #1 0.027 policy input: {
   #1 0.027   "image": {
   #1 0.027     "repo": "alpine",
   #1 0.027     "tag": "3.19",
   #1 0.027     ...
   #1 0.027   }
   #1 0.027 }
   #1 0.028 policy decision for source docker-image://alpine:3.19: DENY
   #1 ERROR: source "docker-image://alpine:3.19" not allowed by policy
   ```

3. 添加一条允许 alpine 镜像的规则：

   ```rego
   allow if {
       input.image.repo == "alpine"
   }
   ```

4. 再次构建以验证策略是否有效：

   ```console
   $ docker buildx build .
   ```

如果失败，请参阅 [调试](./debugging.md) 获取故障排除指南。

## 将策略与 `docker build` 一起使用

一旦你开发并测试了策略，就将它应用到真实构建中。

### 基本用法

在你的 Dockerfile 旁边创建一个策略：

```dockerfile {title="Dockerfile"}
FROM alpine:3.19
RUN echo "hello"
```

```rego {title="Dockerfile.rego"}
package docker

default allow := false

allow if input.local

allow if {
    input.image.repo == "alpine"
}

decision := {"allow": allow}
```

正常构建：

```console
$ docker buildx build .
```

Buildx 会在构建前自动加载策略并验证 `alpine:3.19` 镜像。

### 使用不同的 Dockerfile 名称构建

使用 `-f` 指定 Dockerfile：

```console
$ docker buildx build -f app.Dockerfile .
```

Buildx 会在同一目录中查找 `app.Dockerfile.rego`。

### 使用手动策略构建

在自动策略之外添加一个额外策略：

```console
$ docker buildx build --policy filename=extra-checks.rego .
```

`Dockerfile.rego`（自动）和 `extra-checks.rego`（手动）都必须通过。

### 在没有自动策略的情况下构建

仅使用你指定的策略：

```console
$ docker buildx build --policy reset=true,filename=strict.rego .
```

## 将策略与 bake 一起使用

[Bake](/build/bake/) 支持与 `docker buildx build` 一样的自动策略加载。将 `Dockerfile.rego` 放在你的 Dockerfile 旁边并运行：

```console
$ docker buildx bake
```

### bake 文件中的手动策略

在你的 `docker-bake.hcl` 中指定额外的策略：

```hcl {title="docker-bake.hcl"}
target "default" {
  dockerfile = "Dockerfile"
  policy = ["extra.rego"]
}
```

`policy` 属性接受一个策略文件列表。Bake 会加载这些文件，外加自动的 `Dockerfile.rego`（如果存在）。

### bake 中的多个策略

```hcl {title="docker-bake.hcl"}
target "webapp" {
  dockerfile = "Dockerfile"
  policy = [
    "shared/base-policy.rego",
    "security/image-signing.rego"
  ]
}
```

所有策略都必须通过，目标才能成功构建。

### 每个目标使用不同的策略

对不同目标应用不同的验证规则：

```hcl {title="docker-bake.hcl"}
target "development" {
  dockerfile = "dev.Dockerfile"
  policy = ["policies/permissive.rego"]
}

target "production" {
  dockerfile = "prod.Dockerfile"
  policy = ["policies/strict.rego", "policies/signing-required.rego"]
}
```

使用适当的目标构建：

```console
$ docker buildx bake development  # 使用宽松策略
$ docker buildx bake production   # 使用严格策略
```

### 带策略选项的 bake

目前，bake 不支持在 HCL 文件中使用策略选项（reset、strict、disabled）。请改用命令行标志：

```console
$ docker buildx bake --policy disabled=true production
```

## 在 CI/CD 中测试

通过在构建时使用 `--policy` 标志运行构建，在持续集成中验证策略。有关在运行构建之前对策略进行单元测试，请参阅 [测试构建策略](./testing.md)。

在 CI 构建期间测试策略：

```yaml {title=".github/workflows/test-policies.yml"}
name: Test Build Policies
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@{{% param "checkout_action_version" %}}
      - uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
      - name: Test build with policy
        run: docker buildx build --policy strict=true .
```

这可确保策略更改不会破坏构建，并且新规则按预期工作。`strict=true` 标志会在策略未加载（例如，构建使用的 BuildKit 实例过旧且不支持策略）时使构建失败。

## 进阶：策略配置

本节介绍进阶的策略加载机制和配置选项。

### 自动策略加载

Buildx 会自动加载与你的 Dockerfile 名称匹配的策略。当你使用 `Dockerfile` 构建时，Buildx 会在同一目录中查找 `Dockerfile.rego`。对于名为 `app.Dockerfile` 的文件，它会查找 `app.Dockerfile.rego`。

```text
project/
├── Dockerfile
├── Dockerfile.rego          # 为 Dockerfile 自动加载
├── app.Dockerfile
├── app.Dockerfile.rego      # 为 app.Dockerfile 自动加载
└── src/
```

这种自动加载意味着在大多数情况下你不需要命令行标志。在你的 Dockerfile 旁边创建策略文件并构建：

```console
$ docker buildx build .
```

Buildx 会检测到 `Dockerfile.rego` 并在运行构建之前评估它。

> [!NOTE]
> 策略文件必须与它们所验证的 Dockerfile 位于同一目录。Buildx 不会搜索父目录或子目录。

### 当策略未加载时

如果 buildx 找不到匹配的 `.rego` 文件，构建将在不进行策略评估的情况下继续进行。要要求策略并在找不到任何策略时失败，请使用严格模式：

```console
$ docker buildx build --policy strict=true .
```

如果未加载任何策略，或者 BuildKit 守护进程不支持策略，这会使构建失败。

### 手动策略配置

`--policy` 标志让你指定额外的策略、覆盖自动加载，或控制策略行为。

基本语法：

```console
$ docker buildx build --policy filename=custom.rego .
```

这会加载 `custom.rego`，外加自动的 `Dockerfile.rego`（如果存在）。

多个策略：

```console
$ docker buildx build --policy filename=policy1.rego --policy filename=policy2.rego .
```

所有策略都必须通过，构建才能成功。用它来强制执行分层要求（基础策略 + 项目特定规则）。

可用选项：

| 选项                  | 描述                                                                           | 示例                          |
| --------------------- | ------------------------------------------------------------------------------ | ----------------------------- |
| `filename=<path>`     | 从指定文件加载策略                                                             | `filename=custom.rego`        |
| `reset=true`          | 忽略自动策略，仅使用指定的策略                                                 | `reset=true`                  |
| `disabled=true`       | 禁用所有策略评估                                                               | `disabled=true`               |
| `strict=true`         | 如果 BuildKit 不支持策略则失败                                                 | `strict=true`                 |
| `log-level=<level>`   | 控制策略日志（error、warn、info、debug、none）。使用 `debug` 可查看完整的输入 JSON 和未解析字段 | `log-level=debug`             |

用逗号组合选项：

```console
$ docker buildx build --policy filename=extra.rego,strict=true .
```

### 使用 policy eval 探索源

`docker buildx policy eval` 命令让你可以快速探索和测试源，而无需运行构建。

#### 使用 --print 检查输入结构

使用 `--print` 查看任何源的的输入结构，而无需运行策略评估：

```console
$ docker buildx policy eval --print https://github.com/moby/buildkit.git
```

```json
{
  "git": {
    "schema": "https",
    "host": "github.com",
    "remote": "https://github.com/moby/buildkit.git"
  }
}
```

测试不同的源类型：

```console
# HTTP 下载
$ docker buildx policy eval --print https://releases.hashicorp.com/terraform/1.5.0/terraform.zip

# 镜像（需要 docker-image:// 前缀）
$ docker buildx policy eval --print docker-image://alpine:3.19

# 本地上下文
$ docker buildx policy eval --print .
```

显示从源解析出的信息，而无需获取。使用 `--fields` 获取特定的元数据（请参阅 [上文](#testing-policies-with-policy-eval)）。

#### 使用特定策略文件测试

`--filename` 标志通过提供基础 Dockerfile 名称（不带 `.rego` 扩展名）来指定要加载哪个策略文件。这对于针对与不同 Dockerfile 关联的策略测试源很有用。

例如，要针对 `app.Dockerfile` 的策略测试一个源：

```console
$ docker buildx policy eval --filename app.Dockerfile .
```

这会加载 `app.Dockerfile.rego` 并测试它是否允许该源 `.`（本地目录）。如果未指定，该标志默认为 `Dockerfile`。

针对你的策略测试不同的源：

```console
$ docker buildx policy eval --filename app.Dockerfile https://github.com/org/repo.git
$ docker buildx policy eval --filename app.Dockerfile docker-image://alpine:3.19
```

### 重置自动加载

要仅使用你指定的策略并忽略自动的 `.rego` 文件：

```console
$ docker buildx build --policy reset=true,filename=custom.rego .
```

这会跳过 `Dockerfile.rego`，仅加载 `custom.rego`。

### 临时禁用策略

为测试或紧急情况禁用策略评估：

```console
$ docker buildx build --policy disabled=true .
```

构建将在没有任何策略检查的情况下继续进行。请谨慎使用——你正在绕过安全控制。

## 下一步

- 为你的策略编写单元测试：[测试构建策略](./testing.md)
- 调试策略失败：[调试](./debugging.md)
- 浏览可用的示例：[示例策略](./examples.md)
- 参考所有输入字段：[输入参考](./inputs.md)
