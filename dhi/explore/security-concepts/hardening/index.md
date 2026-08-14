# Base image hardening（基础镜像加固）


## What is base image hardening?（什么是基础镜像加固？）

基础镜像加固是通过最小化容器镜像的基础层所包含的内容，并为其配置以安全为先的默认值，来保护其基础层的过程。加固后的基础镜像会移除不必要的组件，如 shell、编译器和包管理器，从而限制可用的攻击面，使攻击者更难在容器内获得控制权或提升权限。

加固还涉及应用最佳实践，例如以非 root 用户运行、减少可写表面，以及通过不可变性确保一致性。虽然 [Docker Official Images](../../../docker-hub/image-library/trusted-content.md#docker-official-images) 和 [Docker Verified Publisher Images](../../../docker-hub/image-library/trusted-content.md#verified-publisher-images) 遵循安全最佳实践，但它们可能不如 Docker Hardened Images 那样加固，因为它们旨在支持更广泛的使用场景。

## Why is it important?（为何很重要？）

大多数容器从其所使用的基础镜像继承其安全态势。如果基础镜像包含不必要的工具或以提升的权限运行，那么在其之上构建的每个容器都会暴露这些风险。

加固基础镜像：

- 通过移除可能被利用的工具和库来减少攻击面
- 通过放弃 root 访问并限制容器可以执行的操作来强制执行最小权限
- 通过避免运行时变更和配置漂移来提高可靠性和一致性
- 与安全的软件供应链实践保持一致，并有助于满足合规标准

使用加固的基础镜像是保护你在容器中构建和运行的软件的关键第一步。

## What's removed and why（移除了什么及其原因）

加固镜像通常会排除在安全的生产环境中存在风险或不必要的常见组件：

| 移除的组件                                | 原因                                                                           |
|--------------------------------------------------|----------------------------------------------------------------------------------|
| Shell（例如 `sh`、`bash`）                      | 防止用户或攻击者在容器内执行任意命令  |
| 包管理器（例如 `apt`、`apk`）            | 禁用构建后安装软件的能力，减少漂移和暴露 |
| 编译器和解释器                       | 避免引入可用于运行或注入恶意代码的工具      |
| 调试工具（例如 `strace`、`curl`、`wget`） | 降低被利用或信息泄露的风险                              |
| 未使用的库或区域设置（locales）                      | 缩小镜像体积并最小化攻击向量                                  |

## How Docker Hardened Images apply base image hardening（Docker Hardened Images 如何应用基础镜像加固）

Docker Hardened Images（DHI）在设计时即应用基础镜像加固原则。每个镜像都经过构建，仅包含其特定用途所需的内容，无论是构建应用程序（使用 `-dev` 或 `-sdk` 标签）还是在生产中运行它们。

### Docker Hardened Image traits（Docker Hardened Image 特性）

Docker Hardened Images 的构建目标是：

- 最小化（Minimal）：仅包含必要的库和二进制文件
- 不可变（Immutable）：镜像在构建时固定——无运行时安装
- 默认非 root（Non-root by default）：除非另行配置，容器以非特权用户运行
- 用途限定（Purpose-scoped）：提供不同的标签用于开发（`-dev`）、基于 SDK 的构建（`-sdk`）和生产运行时

这些特性有助于在开发、测试和生产环境中强制执行一致、安全的行为。

### Docker Hardened Image compatibility considerations（Docker Hardened Image 兼容性注意事项）

由于 Docker Hardened Images 去掉了许多常用工具，它们可能无法开箱即用地适用于所有用例。你可能需要：

- 使用多阶段构建在 `-dev` 镜像中编译代码或安装依赖项，并将输出复制到加固的运行时镜像
- 用等效的入口点（entrypoint）二进制文件替换 shell 脚本，或如有需要显式包含一个 shell
- 使用 [Docker Debug](/reference/cli/docker/debug/) 临时检查或排查容器问题，而无需更改基础镜像

这些权衡是有意为之的，有助于支持构建安全、可复现且可用于生产的容器的最佳实践。

