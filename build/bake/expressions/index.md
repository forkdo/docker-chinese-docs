# Bake 中的表达式求值


HCL 格式的 Bake 文件支持表达式求值，让你可以执行算术运算、有条件地设置值等。

## 算术运算

你可以在表达式中执行算术运算。以下示例展示了如何将两个数相乘。

```hcl {title=docker-bake.hcl}
sum = 7*6

target "default" {
  args = {
    answer = sum
  }
}
```

使用 `--print` 标志打印 Bake 文件，会显示 `answer` 构建参数的求值结果。

```console
$ docker buildx bake --print
```

```json
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "answer": "42"
      }
    }
  }
}
```

## 三元运算符

你可以使用三元运算符有条件地注册一个值。

以下示例使用内置的 `notequal` [函数](./funcs.md)，仅在变量不为空时添加一个 tag。

```hcl {title=docker-bake.hcl}
variable "TAG" {}

target "default" {
  context="."
  dockerfile="Dockerfile"
  tags = [
    "my-image:latest",
    notequal("",TAG) ? "my-image:${TAG}": ""
  ]
}
```

在这种情况下，`TAG` 是一个空字符串，因此生成的构建配置只包含硬编码的 `my-image:latest` tag。

```console
$ docker buildx bake --print
```

```json
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["my-image:latest"]
    }
  }
}
```

## 带变量的表达式

你可以使用 [变量](./variables.md) 配合表达式来有条件地设置值，或执行算术运算。

以下示例使用表达式根据变量的值设置值。`v1` 构建参数在变量 `FOO` 大于 5 时设为 "higher"，否则设为
"lower"。`v2` 构建参数在 `IS_FOO` 变量为 true 时设为 "yes"，否则设为 "no"。

```hcl {title=docker-bake.hcl}
variable "FOO" {
  default = 3
}

variable "IS_FOO" {
  default = true
}

target "app" {
  args = {
    v1 = FOO > 5 ? "higher" : "lower"
    v2 = IS_FOO ? "yes" : "no"
  }
}
```

使用 `--print` 标志打印 Bake 文件，会显示 `v1` 和 `v2` 构建参数的求值结果。

```console
$ docker buildx bake --print app
```

```json
{
  "group": {
    "default": {
      "targets": ["app"]
    }
  },
  "target": {
    "app": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "v1": "lower",
        "v2": "yes"
      }
    }
  }
}
```

