---
title: 内置函数
linkTitle: 内置函数
description: Buildx 包含内置辅助函数，使编写策略更轻松
keywords: build policies, built-in functions, rego functions, signature verification, policy helpers
weight: 90
---

除了 [Rego 内置函数](#rego-built-in-functions) 外，Buildx 还提供内置函数，用以通过 Docker 特定的操作（如加载本地文件、验证 Git 签名以及固定镜像摘要）来扩展 Rego 策略。

## Rego 内置函数（Rego built-in functions）

[本页记录的](#buildx-built-in-functions) 函数是 Buildx 特有的函数，不同于 [Rego 标准内置函数](https://www.openpolicyagent.org/docs/policy-language#built-in-functions)。

Buildx 也支持标准的 Rego 内置函数，但仅支持一个子集。要查看受支持函数的确切列表，请参阅 Buildx [源代码](https://github.com/docker/buildx/blob/master/policy/builtins.go)。

## Buildx 内置函数（Buildx built-in functions）

Buildx 为策略开发提供以下自定义内置函数：

- [`print`](#print)
- [`load_json`](#load_json)
- [`verify_git_signature`](#verify_git_signature)
- [`pin_image`](#pin_image)

### `print`

在策略评估期间输出调试信息。

参数：

- 任意数量的待打印值

返回：这些值（透传）

示例：

```rego
allow if {
    input.image.repo == "alpine"
    print("Allowing alpine image:", input.image.tag)
}
```

调试输出会在使用 `--progress=plain` 构建时出现。

### `load_json`

从构建上下文中的本地文件加载并解析 JSON 数据。

参数：

- `filename`（字符串）- 相对于策略目录的 JSON 文件路径

返回：解析后的 JSON 数据，作为 Rego 值

示例：

```rego
# 从外部文件加载已批准的版本
approved_versions = load_json("versions.json")

allow if {
    input.image.repo == "alpine"
    some version in approved_versions.alpine
    input.image.tag == version
}
```

文件结构：

```text
project/
├── Dockerfile
├── Dockerfile.rego
└── versions.json
```

versions.json：

```json
{
  "alpine": ["3.19", "3.20"],
  "golang": ["1.21", "1.22"]
}
```

JSON 文件必须与策略位于同一目录，或位于可从策略位置访问的子目录中。

### `verify_git_signature`

验证 Git 提交或标签上的 PGP 签名。

参数：

- `git_object`（对象）- 可以是 `input.git.commit` 或 `input.git.tag`
- `keyfile`（字符串）- PGP 公钥文件路径（相对于策略目录）

返回：布尔值 - 如果签名有效则为 `true`，否则为 `false`

示例：

```rego
# 要求已签名的 Git 标签
allow if {
    input.git.tagName != ""
    verify_git_signature(input.git.tag, "maintainer.asc")
}

# 要求已签名的提交
allow if {
    input.git.commit
    verify_git_signature(input.git.commit, "keys/team.asc")
}
```

目录结构：

```text
project/
├── Dockerfile.rego
└── maintainer.asc          # PGP 公钥
```

或者使用子目录：

```text
project/
├── Dockerfile.rego
└── keys/
    ├── maintainer.asc
    └── team.asc
```

获取公钥：

```console
$ gpg --export --armor user@example.com > maintainer.asc
```

### `pin_image`

将镜像固定到特定摘要，覆盖基于标签的引用。使用它来强制构建使用特定的镜像版本。

参数：

- `image_object`（对象）- 必须是 `input.image`（正在评估的当前镜像）
- `digest`（字符串）- 目标摘要，格式为 `sha256:...`

返回：布尔值 - 如果固定成功则为 `true`

示例：

```rego
# 将 alpine 3.19 固定到特定摘要
alpine_3_19_digest = "sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412"

allow if {
    input.image.repo == "alpine"
    input.image.tag == "3.19"
    pin_image(input.image, alpine_3_19_digest)
}
```

自动摘要替换：

```rego
# 将旧摘要替换为已修补的版本
replace_map = {
  "3.22.0": "3.22.2",
  "3.22.1": "3.22.2",
}

alpine_digests = {
  "3.22.0": "sha256:8a1f59ffb675680d47db6337b49d22281a139e9d709335b492be023728e11715",
  "3.22.2": "sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412",
}

allow if {
    input.image.repo == "alpine"
    some old_version, new_version in replace_map
    input.image.checksum == alpine_digests[old_version]
    print("Replacing", old_version, "with", new_version)
    pin_image(input.image, alpine_digests[new_version])
}
```

这种模式会自动将旧的镜像版本升级到已修补的发布版本。

## 下一步

- 浏览完整示例：[示例策略](./examples.md)
- 学习策略开发工作流：[使用构建策略](./usage.md)
- 参考输入字段：[输入参考](./inputs.md)
