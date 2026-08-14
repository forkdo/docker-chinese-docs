---
title: 调试构建策略
linkTitle: 调试
description: 使用检查和测试工具在开发期间调试策略
keywords: build policies, debugging, policy troubleshooting, log-level, policy eval, rego debugging
weight: 70
---

当策略未按预期工作时，请使用可用的工具来检查策略评估并了解正在发生的情况。本指南涵盖了调试技术和常见陷阱。

## 快速参考

基本的调试命令：

```console
# 在构建期间查看完整的输入数据（推荐）
$ docker buildx build --progress=plain --policy log-level=debug .

# 查看策略检查和决策
$ docker buildx build --progress=plain .

# 探索不同源的输入结构
$ docker buildx policy eval --print .
$ docker buildx policy eval --print https://github.com/org/repo.git
$ docker buildx policy eval --print docker-image://alpine:3.19

# 测试策略是否允许某个源
$ docker buildx policy eval .
```

## 使用 `--progress=plain` 的策略输出

要在构建期间查看策略评估，请使用 `--progress=plain`：

```console
$ docker buildx build --progress=plain .
```

这会显示所有策略检查、决策和 `print()` 输出。如果没有 `--progress=plain`，除非出错，否则策略评估是静默的。

```plaintext
#1 loading policies Dockerfile.rego
#1 0.010 checking policy for source docker-image://alpine:3.19 (linux/arm64)
#1 0.011 Dockerfile.rego:8: image: {"ref":"alpine:3.19","repo":"alpine","tag":"3.19"}
#1 0.012 policy decision for source docker-image://alpine:3.19: ALLOW
```

如果策略拒绝某个源，你会看到：

```text
#1 0.012 policy decision for source docker-image://nginx:latest: DENY
ERROR: source "docker-image://nginx:latest" not allowed by policy
```

## 调试日志

要进行详细调试，请添加 `--policy log-level=debug` 以查看完整的输入 JSON、未解析字段和策略响应：

```console
$ docker buildx build --progress=plain --policy log-level=debug .
```

这会显示比默认级别多得多的信息，包括每个源的完整输入结构，而无需在你的策略中编写 `print()` 语句。

完整的输入 JSON：

```text
#1 0.007 policy input: {
#1 0.007   "env": {
#1 0.007     "filename": "."
#1 0.007   },
#1 0.007   "image": {
#1 0.007     "ref": "docker.io/library/alpine:3.19",
#1 0.007     "host": "docker.io",
#1 0.007     "repo": "alpine",
#1 0.007     "fullRepo": "docker.io/library/alpine",
#1 0.007     "tag": "3.19",
#1 0.007     "platform": "linux/arm64",
#1 0.007     "os": "linux",
#1 0.007     "arch": "arm64"
#1 0.007   }
#1 0.007 }
```

未解析字段：

```text
#1 0.007 unknowns for policy evaluation: [input.image.checksum input.image.labels input.image.user input.image.volumes input.image.workingDir input.image.env input.image.hasProvenance input.image.signatures]
```

策略响应：

```text
#1 0.008 policy response: map[allow:true]
```

这种详细的输出对于准确了解你的策略接收了哪些数据以及哪些字段尚未解析是非常宝贵的。在开发策略时使用调试日志，可以避免需要大量的 `print()` 语句。

## 使用 print() 进行条件调试

虽然 `--policy log-level=debug` 会自动显示所有输入数据，但 `print()` 函数对于调试特定规则逻辑和条件流很有用：

```rego
allow if {
    input.image
    print("Checking image:", input.image.repo, "isCanonical:", input.image.isCanonical)
    input.image.repo == "alpine"
    input.image.isCanonical
}
```

使用 `print()` 来调试规则内的条件逻辑或跟踪哪些规则正在评估。对于开发期间的一般输入检查，请改用 `--policy log-level=debug`——它不需要修改策略。

> [!NOTE]
> 打印语句仅在其包含的规则被评估时才会执行。像 `allow if { input.image; print(...) }` 这样的规则只对镜像输入打印，而不是对 Git 仓库、HTTP 下载或本地文件打印。

## 常见问题

### 完整仓库路径还是仓库名

症状：检查仓库名的策略没有按预期匹配。

原因：Docker Hub 镜像对短名称（`"alpine"`）使用 `input.image.repo`，但 `input.image.fullRepo` 包含完整路径（`"docker.io/library/alpine"`）。

解决方案：

```rego
# 只匹配仓库名（适用于 Docker Hub 和其他镜像仓库）
allow if {
    input.image
    input.image.repo == "alpine"
}

# 或匹配完整的仓库路径
allow if {
    input.image
    input.image.fullRepo == "docker.io/library/alpine"
}
```

### 策略评估执行多次

症状：构建输出显示同一源被评估多次。

原因：BuildKit 可能在不同的阶段（引用解析、实际拉取）或针对不同的平台评估策略。

这是正常行为。策略应该是幂等的（对于相同的输入每次都产生相同的结果）。

### 使用 `policy eval --print` 时字段缺失

症状：`docker buildx policy eval --print` 没有显示预期的字段，如 `hasProvenance`、`labels` 或 `checksum`。

原因：`--print` 默认只显示引用信息，而不从镜像仓库获取。

解决方案：使用 `--fields` 获取特定的元数据字段：

```console
$ docker buildx policy eval --print --fields image.labels docker-image://alpine:3.19
```

有关详细信息，请参阅 [使用构建策略](./usage.md#testing-policies-with-policy-eval)。

## 下一步

- 查看完整字段参考：[输入参考](./inputs.md)
- 查看示例策略：[示例](./examples.md)
- 学习策略使用模式：[使用构建策略](./usage.md)
