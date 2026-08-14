---
title: 验证镜像输入
linkTitle: 镜像验证
description: 编写策略以验证构建中使用的容器镜像
keywords: build policies, image validation, docker images, provenance, attestations, signatures
weight: 30
---

容器镜像是构建输入中最常见的类型。每条 `FROM` 指令都会拉取一个镜像，而 `COPY --from` 引用会拉取额外的镜像。验证这些镜像可以保护你的构建供应链免受被入侵的镜像仓库、意外的更新以及未经授权的基础镜像的影响。

本指南将教你编写验证镜像输入的策略，从基本的允许列表（allowlisting）逐步深入到进阶的证明（attestation）检查。

## 先决条件

你应该已从 [简介](./intro.md) 了解了策略基础知识：创建策略文件、基本的 Rego 语法，以及策略在构建期间如何评估。

## 什么是镜像输入？

镜像输入来自两条 Dockerfile 指令：

```dockerfile
# FROM 指令
FROM alpine:3.22
FROM golang:1.25-alpine AS builder

# COPY --from 引用
COPY --from=builder /app /app
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

这些引用中的每一个都会触发一次策略评估。你的策略可以在构建继续之前检查镜像元数据、验证证明并强制执行约束。

## 允许列表特定仓库

最简单的镜像策略是限制可以使用哪些仓库。这可以防止开发者使用未经审查的任意镜像。

创建一个只允许 Alpine 的策略：

```rego {title="Dockerfile.rego"}
package docker

default allow := false

allow if input.local

allow if {
  input.image.repo == "alpine"
}

decision := {"allow": allow}
```

此策略：

- 默认拒绝所有输入
- 允许本地构建上下文
- 允许来自 `alpine` 仓库的任何镜像（任何标签或摘要）

用一个 Dockerfile 测试它：

```dockerfile {title="Dockerfile"}
FROM alpine
RUN echo "hello"
```

```console
$ docker build .
```

构建成功。尝试改为 `FROM ubuntu`：

```console
$ docker build .
```

构建失败，因为 `ubuntu` 与允许的仓库不匹配。

## 比较语义化版本

使用 Rego 的 `semver` 函数将镜像限制在特定版本范围内：

```rego
package docker

default allow := false

allow if input.local

# 允许 Go 1.21 或更新版本
allow if {
  input.image.repo == "golang"
  semver.is_valid(input.image.tag)
  semver.compare(input.image.tag, "1.21.0") >= 0
}

decision := {"allow": allow}
```

`semver.compare(a, b)` 函数比较语义化版本并返回：

- `-1` 如果版本 `a` 小于 `b`
- `0` 如果版本相等
- `1` 如果版本 `a` 大于 `b`

在比较之前，使用 `semver.is_valid()` 检查标签是否为有效的语义化版本。

限制为特定版本范围：

```rego
allow if {
  input.image.repo == "node"
  version := input.image.tag
  semver.is_valid(version)
  semver.compare(version, "20.0.0") >= 0  # 20.0.0 或更新
  semver.compare(version, "21.0.0") < 0   # 早于 21.0.0
}
```

这仅允许 Node.js 20.x 版本。该模式适用于任何使用语义化版本控制的镜像。

这些 `semver` 函数是标准的 Rego 内置函数，在 [OPA 策略参考](https://www.openpolicyagent.org/docs/latest/policy-reference/#semver) 中有文档说明。

## 要求摘要引用

像 `alpine:3.22` 这样的标签可能会变化——有人可能会用相同的标签推送一个新镜像。像 `alpine@sha256:abc123...` 这样的摘要是不可变的。

### 要求用户提供摘要

你可以要求用户在他们的 Dockerfile 中始终指定摘要：

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.image.isCanonical
}

decision := {"allow": allow}
```

当用户引用包含摘要时，`isCanonical` 字段为 `true`。此策略将允许：

```dockerfile
FROM alpine@sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412
```

但会拒绝仅使用标签的引用，如 `FROM alpine:3.22`。

### 固定到特定摘要

或者（或额外地），你可以验证镜像的实际摘要是否与特定值匹配，而不管用户如何编写引用：

```rego
allow if {
  input.image.repo == "alpine"
  input.image.checksum == "sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412"
}

decision := {"allow": allow}
```

这会检查所拉取镜像的实际内容摘要。它将允许：

```dockerfile
FROM alpine:3.22
FROM alpine@sha256:4b7ce...
```

只要解析出的镜像具有指定的摘要。这对于将关键基础镜像固定到已知良好的版本很有用。

## 限制镜像仓库

控制你的构建可以从哪些镜像仓库拉取。这有助于执行公司策略或限制为受信任的来源。

```rego
package docker

default allow := false

allow if input.local

# 允许 Docker Hub 镜像
allow if {
  input.image.host == "docker.io"  # Docker Hub
  input.image.repo == "alpine"
}

# 允许来自内部镜像仓库的镜像
allow if {
  input.image.host == "registry.company.com"
}

decision := {"allow": allow}
```

`host` 字段包含镜像仓库主机名。Docker Hub 镜像使用 `"docker.io"` 作为 host 值。用以下方式测试：

```dockerfile
FROM alpine                                    # 允许（Docker Hub）
FROM registry.company.com/myapp:latest         # 允许（公司镜像仓库）
FROM ghcr.io/someorg/image:latest              # 拒绝（错误的镜像仓库）
```

当你需要包含镜像仓库的完整路径时，使用 `fullRepo`：

```rego
allow if {
  input.image.fullRepo == "docker.io/library/alpine"
}
```

## 验证平台约束

多架构镜像支持不同的操作系统和 CPU 架构。你可以将构建限制在特定平台上：

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.image.os == "linux"
  input.image.arch in ["amd64", "arm64"]
}

decision := {"allow": allow}
```

此策略：

- 在列表中定义受支持的架构
- 检查 `input.image.os` 是否匹配 Linux
- 验证 `input.image.arch` 是否在受支持列表中

`os` 和 `arch` 字段来自镜像清单，反映了实际的镜像平台。这与 Docker 的自动平台选择配合工作——策略验证 Buildx 解析出的内容，而不是你指定的内容。

## 检查镜像元数据

镜像包含元数据，如环境变量、标签和工作目录。你可以验证这些元数据以确保镜像满足要求。

检查特定的环境变量：

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.image.repo == "golang"
  input.image.workingDir == "/go"
  some ver in input.image.env
  startswith(ver, "GOLANG_VERSION=")
  some toolchain in input.image.env
  toolchain == "GOTOOLCHAIN=local"
}

decision := {"allow": allow}
```

此策略通过检查以下内容来验证官方的 Go 镜像：

- 工作目录是 `/go`
- 环境中设置了 `GOLANG_VERSION`
- 环境包含 `GOTOOLCHAIN=local`

`input.image.env` 字段是 `KEY=VALUE` 格式的字符串数组。使用 Rego 的 `some` 迭代来搜索该数组。

检查镜像标签：

```rego
allow if {
  input.image.labels["org.opencontainers.image.vendor"] == "Example Corp"
  input.image.labels["org.opencontainers.image.version"] != ""
}
```

`labels` 字段是一个映射，因此你使用方括号表示法来访问值。

## 要求证明和来源

现代镜像包含 [证明](/build/metadata/attestations/)：关于镜像如何构建的机器可读元数据。[来源证明](/build/metadata/attestations/slsa-provenance/)（provenance）描述了构建过程，而 [SBOM](/build/metadata/attestations/sbom/) 列出了其中的软件。

要求来源证明：

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.image.hasProvenance
}

decision := {"allow": allow}
```

当镜像具有来源或 SBOM [证明](../metadata/attestations/_index.md) 时，`hasProvenance` 字段为 `true`。

## 验证 GitHub Actions 签名

对于使用 GitHub Actions 构建的镜像，通过检查签名元数据来验证它们来自受信任的工作流：

```rego
allow if {
  input.image.repo == "myapp"
  input.image.hasProvenance
  some sig in input.image.signatures
  valid_github_signature(sig)
}

# 验证 GitHub Actions 签名的辅助函数
valid_github_signature(sig) if {
  sig.signer.certificateIssuer == "CN=sigstore-intermediate,O=sigstore.dev"
  sig.signer.issuer == "https://token.actions.githubusercontent.com"
  startswith(sig.signer.buildSignerURI, "https://github.com/myorg/")
  sig.signer.runnerEnvironment == "github-hosted"
}

decision := {"allow": allow}
```

这种模式适用于任何使用 Sigstore 无密钥（keyless）签名的 GitHub Actions 工作流。签名元数据提供了构建来源密码学证明。有关完整的签名验证示例，请参阅 [示例策略](./examples.md)。

## 组合多个检查

真实的策略通常会组合多个检查。一条 `allow` 规则中的多个条件意味着 AND（与）——所有条件都必须为真：

```rego
package docker

default allow := false

allow if input.local

# 生产镜像需要所有条件
allow if {
  input.image.repo == "alpine"
  input.image.isCanonical
  input.image.hasProvenance
}

decision := {"allow": allow}
```

多条 `allow` 规则意味着 OR（或）——任何规则都可以匹配：

```rego
package docker

default allow := false

allow if input.local

# 对 Alpine 使用严格检查
allow if {
  input.image.repo == "alpine"
  input.image.isCanonical
}

# 对 Go 使用不同的检查
allow if {
  input.image.repo == "golang"
  input.image.workingDir == "/go"
}

decision := {"allow": allow}
```

使用这种模式对不同基础镜像应用不同的要求。

## 下一步

你现在理解了如何在构建策略中验证容器镜像。要继续学习：

- 学习用于源代码输入的 [Git 仓库验证](./validate-git.md)
- 浏览 [示例策略](./examples.md) 获取完整的策略模式
- 阅读 [内置函数](./built-ins.md) 了解签名验证和证明检查
- 查看 [输入参考](./inputs.md) 了解所有可用的镜像字段
