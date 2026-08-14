---
title: Bake 中的变量
linkTitle: 变量（Variables）
weight: 40
description:
keywords: build, buildx, bake, buildkit, hcl, variables
---

你可以在 Bake 文件中定义和使用变量来设置属性值、将变量插值到其他值中，并执行算术运算。
变量可以定义默认值，并可以通过环境变量覆盖。

## 将变量用作属性值

使用 `variable` 块来定义变量。

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "docker.io/username/webapp:latest"
}
```

以下示例展示了如何在目标中使用 `TAG` 变量。

```hcl {title=docker-bake.hcl}
target "webapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = [ TAG ]
}
```

## 将变量插值到值中

Bake 支持将变量字符串插值到值中。你可以使用 `${}` 语法将变量插值到值中。以下示例定义了一个
值为 `latest` 的 `TAG` 变量。

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "latest"
}
```

要将 `TAG` 变量插值到属性的值中，使用 `${TAG}` 语法。

```hcl {title=docker-bake.hcl}
group "default" {
  targets = [ "webapp" ]
}

variable "TAG" {
  default = "latest"
}

target "webapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["docker.io/username/webapp:${TAG}"]
}
```

使用 `--print` 标志打印 Bake 文件，会在解析后的构建配置中显示插值后的值。

```console
$ docker buildx bake --print
```

```json
{
  "group": {
    "default": {
      "targets": ["webapp"]
    }
  },
  "target": {
    "webapp": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["docker.io/username/webapp:latest"]
    }
  }
}
```

## 验证变量

要验证变量的值是否符合预期的类型、值范围或其他条件，你可以使用 `validation` 块定义自定义
验证规则。

在以下示例中，验证用于强制对变量值进行数值约束；`PORT` 变量必须为 1024 或更大。

```hcl {title=docker-bake.hcl}
# Define a variable `PORT` with a default value and a validation rule
variable "PORT" {
  default = 3000  # Default value assigned to `PORT`

  # Validation block to ensure `PORT` is a valid number within the acceptable range
  validation {
    condition = PORT >= 1024  # Ensure `PORT` is at least 1024
    error_message = "The variable 'PORT' must be 1024 or greater."  # Error message for invalid values
  }
}
```

如果 `condition` 表达式求值为 `false`，则该变量值被视为无效，构建调用将失败并发出 `error_message`。
例如，如果 `PORT=443`，条件求值为 `false`，并引发错误。

在设置验证之前，值会被强制转换为预期类型。这确保了通过环境变量设置的任何覆盖都能按预期工作。

### 验证多个条件

要评估多个条件，请为该变量定义多个 `validation` 块。所有条件都必须为 `true`。

示例如下：

```hcl {title=docker-bake.hcl}
# Define a variable `VAR` with multiple validation rules
variable "VAR" {
  # First validation block: Ensure the variable is not empty
  validation {
    condition = VAR != ""
    error_message = "The variable 'VAR' must not be empty."
  }

  # Second validation block: Ensure the value contains only alphanumeric characters
  validation {
    # VAR and the regex match must be identical:
    condition = VAR == regex("[a-zA-Z0-9]+", VAR)
    error_message = "The variable 'VAR' can only contain letters and numbers."
  }
}
```

此示例强制要求：

- 变量不能为空。
- 变量必须匹配特定的字符集。

对于像 `VAR="hello@world"` 这样的无效输入，验证将失败。

### 验证变量依赖关系

你可以在条件表达式中引用其他 Bake 变量，从而强制执行变量间依赖关系的验证。这可确保
依赖变量在继续之前已正确设置。

示例如下：

```hcl {title=docker-bake.hcl}
# Define a variable `FOO`
variable "FOO" {}

# Define a variable `BAR` with a validation rule that references `FOO`
variable "BAR" {
  # Validation block to ensure `FOO` is set if `BAR` is used
  validation {
    condition = FOO != ""  # Check if `FOO` is not an empty string
    error_message = "The variable 'BAR' requires 'FOO' to be set."
  }
}
```

此配置确保只有在 `FOO` 已被赋予非空值时才能使用 `BAR` 变量。尝试在不设置 `FOO` 的情况下
构建将触发验证错误。

## 转义变量插值

如果你想在解析 Bake 定义时绕过变量插值，请使用双美元符号（`$${VARIABLE}`）。

```hcl {title=docker-bake.hcl}
target "webapp" {
  dockerfile-inline = <<EOF
  FROM alpine
  ARG TARGETARCH
  RUN echo "Building for $${TARGETARCH/amd64/x64}"
  EOF
  platforms = ["linux/amd64", "linux/arm64"]
}
```

```console
$ docker buildx bake --progress=plain
...
#8 [linux/arm64 2/2] RUN echo "Building for arm64"
#8 0.036 Building for arm64
#8 DONE 0.0s

#9 [linux/amd64 2/2] RUN echo "Building for x64"
#9 0.046 Building for x64
#9 DONE 0.1s
...
```

## 跨文件在变量中使用变量

当指定多个文件时，一个文件可以使用在另一个文件中定义的变量。在以下示例中，`vars.hcl` 文件
定义了一个默认值为 `docker.io/library/alpine` 的 `BASE_IMAGE` 变量。

```hcl {title=vars.hcl}
variable "BASE_IMAGE" {
  default = "docker.io/library/alpine"
}
```

以下 `docker-bake.hcl` 文件定义了一个 `BASE_LATEST` 变量，它引用了 `BASE_IMAGE` 变量。

```hcl {title=docker-bake.hcl}
variable "BASE_LATEST" {
  default = "${BASE_IMAGE}:latest"
}

target "webapp" {
  contexts = {
    base = BASE_LATEST
  }
}
```

当你使用 `-f` 标志指定 `vars.hcl` 和 `docker-bake.hcl` 文件打印解析后的构建配置时，你会看到
`BASE_LATEST` 变量被解析为 `docker.io/library/alpine:latest`。

```console
$ docker buildx bake -f vars.hcl -f docker-bake.hcl --print app
```

```json
{
  "target": {
    "webapp": {
      "context": ".",
      "contexts": {
        "base": "docker.io/library/alpine:latest"
      },
      "dockerfile": "Dockerfile"
    }
  }
}
```

## 其他资源

以下是一些展示如何在 Bake 中使用变量的额外资源：

- 你可以使用环境变量覆盖 `variable` 的值。详见
  [覆盖配置](./overrides.md#environment-variables)。
- 你可以在函数中引用和使用全局变量。详见 [HCL 函数](./funcs.md#variables-in-functions)
- 你可以在计算表达式时使用变量值。详见 [表达式求值](./expressions.md#expressions-with-variables)
