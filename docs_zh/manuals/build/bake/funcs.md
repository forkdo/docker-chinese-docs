---
title: 函数（Functions）
weight: 60
description: 了解 Bake 中的内置函数和自定义 HCL 函数
keywords: build, buildx, bake, buildkit, hcl, functions, user-defined, built-in, custom, gocty
aliases:
  - /build/customize/bake/hcl-funcs/
  - /build/bake/hcl-funcs/
---

当你需要以比简单拼接或插值更复杂的方式操作构建配置中的值时，HCL 函数非常有用。

## 标准库

Bake 内置支持 [标准库函数](/manuals/build/bake/stdlib.md)。

以下示例展示了 `add` 函数：

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "latest"
}

group "default" {
  targets = ["webapp"]
}

target "webapp" {
  args = {
    buildno = "${add(123, 1)}"
  }
}
```

```console
$ docker buildx bake --print webapp
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
      "args": {
        "buildno": "124"
      }
    }
  }
}
```

## 用户自定义函数

如果内置的标准库函数不满足你的需求，你可以创建 [用户自定义函数](https://github.com/hashicorp/hcl/tree/main/ext/userfunc)
来做你恰好需要的事情。

以下示例定义了一个 `increment` 函数。

```hcl {title=docker-bake.hcl}
function "increment" {
  params = [number]
  result = number + 1
}

group "default" {
  targets = ["webapp"]
}

target "webapp" {
  args = {
    buildno = "${increment(123)}"
  }
}
```

```console
$ docker buildx bake --print webapp
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
      "args": {
        "buildno": "124"
      }
    }
  }
}
```

## 函数中的变量

你可以在函数内部引用 [variables](./variables) 和标准库函数。

以下示例在一个自定义函数中使用了全局变量（`REPO`）。

```hcl {title=docker-bake.hcl}
# docker-bake.hcl
variable "REPO" {
  default = "user/repo"
}

function "tag" {
  params = [tag]
  result = ["${REPO}:${tag}"]
}

target "webapp" {
  tags = tag("v1")
}
```

使用 `--print` 标志打印 Bake 文件，显示 `tag` 函数使用 `REPO` 的值来设置 tag 的前缀。

```console
$ docker buildx bake --print webapp
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
      "tags": ["user/repo:v1"]
    }
  }
}
```
