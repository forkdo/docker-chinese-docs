---
title: 使用策略验证构建输入
linkTitle: 验证构建
description: 通过使用构建策略验证镜像、Git 仓库和依赖项来保障你的 Docker 构建安全
keywords: build policies, opa, rego, docker security, supply chain, attestations
weight: 70
params:
  sidebar:
    badge:
      color: blue
      text: Experimental
---

使用 Docker 进行构建通常涉及下载远程资源。这些外部依赖（例如 Docker 镜像、Git 仓库、远程文件以及其他制品）被称为构建输入（build inputs）。

例如：

- 从镜像仓库拉取镜像
- 克隆源代码仓库
- 通过 HTTPS 从服务器获取文件

在消费构建输入时，验证内容是否符合预期是一个好主意。一种方法是为 `ADD` Dockerfile 指令使用 `--checksum` 选项。这让你可以在将远程资源拉入构建时验证其 SHA256 校验和：

```dockerfile
ADD --checksum=sha256:c0ff3312345… https://example.com/archive.tar.gz /
```

如果远程的 `archive.tar.gz` 文件与 Dockerfile 期望的校验和不匹配，构建将失败。

校验和可以验证内容是否符合预期，但仅限于 `ADD` 指令。它们无法告诉你内容的来源或生成方式。你无法使用校验和来强制执行"镜像必须已签名"或"依赖项必须来自已批准的来源"之类的约束。

构建策略（build policies）解决了这个问题。它们让你能够定义规则，用于验证所有的构建输入，并在整个构建过程中强制执行诸如来源证明（provenance attestations）、已批准的镜像仓库以及已签名的 Git 标签等要求。

## 先决条件

构建策略目前是一项实验性功能。要试用它，你需要：

- Buildx 0.31.0 或更高版本 - 检查你的版本：`docker buildx version`
- BuildKit 0.27.0 或更高版本 - 通过以下命令验证：`docker buildx inspect --bootstrap`

如果你使用的是 Docker Desktop，请确保你使用的版本包含这些更新。

## 构建策略（Build policies）

Buildx 0.31.0 版本新增了对构建策略的支持。构建策略是用于保障 Docker 构建供应链安全的规则，有助于防范上游被入侵、恶意依赖项以及构建输入被未授权篡改。

构建策略让你能够在用于构建项目的输入上强制执行扩展验证，例如：

- Docker 镜像必须使用摘要引用（不能仅使用标签）
- 镜像必须具有来源证明和 cosign 签名
- Git 标签由维护者使用 PGP 公钥签名
- 所有远程制品必须使用 HTTPS 并包含用于验证的校验和

构建策略使用一种声明式策略语言（称为 Rego）定义，该语言为 [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) 而创建。以下示例展示了一个最小的 Rego 构建策略。

```rego {title="Dockerfile.rego"}
package docker

default allow := false

# 允许此构建的任何本地输入
# 例如：本地构建上下文，或本地 Dockerfile
allow if input.local

# 允许镜像，但仅当它们具有来源证明时
allow if {
    input.image.hasProvenance
}

decision := {"allow": allow}
```

如果与此策略关联的 Dockerfile 在 `FROM` 指令中引用了没有来源证明的镜像，该策略就会被违反，构建将失败。

## 策略工作原理（How policies work）

当你运行 `docker buildx build` 时，Buildx 会：

1. 解析所有构建输入（镜像、Git 仓库、HTTP 下载）
2. 查找与你的 Dockerfile 名称匹配的策略文件（例如 `Dockerfile.rego`）
3. 在构建开始之前，针对策略对每个输入进行评估
4. 仅当所有输入都通过策略时才允许构建继续

策略使用 Rego（Open Policy Agent 的策略语言）编写。你不需要是 Rego 专家——[简介](./intro.md) 教程会教你所需的一切。

策略文件与你的 Dockerfile 放在一起：

```text
project/
├── Dockerfile
├── Dockerfile.rego
└── src/
```

无需额外配置——Buildx 在构建时会自动查找并加载策略。

## 使用场景（Use cases）

构建策略可帮助你针对 Docker 构建强制执行安全和合规要求。策略能提供价值的常见场景：

### 强制执行基础镜像标准

要求所有生产 Dockerfile 使用特定的、已批准的基础镜像（带摘要引用）。防止开发者使用未经安全团队审查的任意镜像。

### 验证第三方依赖项

当你的构建从互联网下载文件、库或工具时，验证它们来自受信任的来源，并与预期的校验和或签名相匹配。这可以防止上游依赖项被入侵的供应链攻击。

### 确保签名的发布版本

要求所有依赖项具有来自受信任方的有效签名。

- 检查你在构建中克隆的 Git 仓库的 GPG 签名
- 使用 Sigstore 验证来源证明签名

### 满足合规要求

某些监管框架要求提供你验证构建输入的证明。构建策略为你提供了一种可审计的、声明式的方式来证明你正在根据安全标准检查依赖项。

### 区分开发与生产规则

对生产构建应用更严格的验证，同时在开发期间允许更大的灵活性。同一个策略文件可以根据构建上下文或目标包含条件规则。

## 开始使用（Get started）

准备好开始编写策略了吗？[简介](./intro.md) 教程将引导你创建第一个策略，并教授你所需的 Rego 基础知识。

有关实际使用指南，请参阅 [使用构建策略](./usage.md)。

有关可供复制和改编的实用示例，请参阅 [示例策略](./examples.md) 库。
