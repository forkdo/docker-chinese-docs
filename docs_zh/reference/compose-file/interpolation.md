---
title: 插值
description: 使用插值语法在 Docker Compose 文件中替换环境变量。
keywords: compose, compose 规范, 插值, compose 文件参考
aliases: 
 - /compose/compose-file/12-interpolation/
weight: 90
---

{{% include "compose/interpolation.md" %}}

对于花括号表达式，支持以下格式：
- 直接替换
  - `${VAR}` -> `VAR` 的值
- 默认值
  - `${VAR:-default}` -> 如果 `VAR` 已设置且非空，则使用其值，否则使用 `default`
  - `${VAR-default}` -> 如果 `VAR` 已设置，则使用其值，否则使用 `default`
- 必需值
  - `${VAR:?error}` -> 如果 `VAR` 已设置且非空，则使用其值，否则退出并显示错误
  - `${VAR?error}` -> 如果 `VAR` 已设置，则使用其值，否则退出并显示错误
- 替代值
  - `${VAR:+replacement}` -> 如果 `VAR` 已设置且非空，则使用 `replacement`，否则为空
  - `${VAR+replacement}` -> 如果 `VAR` 已设置，则使用 `replacement`，否则为空

插值也可以嵌套使用：

- `${VARIABLE:-${FOO}}`
- `${VARIABLE?$FOO}`
- `${VARIABLE:-${FOO:-default}}`

Compose 不支持其他扩展的 shell 风格特性，例如 `${VARIABLE/foo/bar}`。

只要字符串在 `$` 符号后构成有效的变量定义（要么是字母数字名称 `[_a-zA-Z][_a-zA-Z0-9]*`，要么是以 `${` 开头的花括号字符串），Compose 就会处理该字符串。在其他情况下，字符串将被保留而不尝试插值。

当配置需要字面美元符号时，可以使用 `$$`（双美元符号）。这也防止了 Compose 插值处理，因此 `$$` 允许你引用不希望被 Compose 处理的环境变量。

```yml
web:
  build: .
  command: "$$VAR_NOT_INTERPOLATED_BY_COMPOSE"
```

如果 Compose 无法解析被替换的变量且未定义默认值，它会显示警告并用空字符串替换该变量。

由于 Compose 文件中的任何值（包括复杂元素的紧凑字符串表示法）都可以用变量替换进行插值，因此在合并之前会逐文件应用插值。

插值仅适用于 YAML 值，不适用于键。对于少数键实际上是用户自定义字符串的地方，如 [标签](services.md#labels) 或 [环境变量](services.md#environment)，必须使用等号语法才能应用插值。例如：

```yml
services:
  foo:
    labels:
      "$VAR_NOT_INTERPOLATED_BY_COMPOSE": "BAR"
```

```yml
services:
  foo:
    labels:
      - "$VAR_INTERPOLATED_BY_COMPOSE=BAR"
```