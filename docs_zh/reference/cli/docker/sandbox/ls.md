---
datafolder: sandbox-cli
datafile: docker_sandbox_ls
title: docker sandbox ls
layout: cli
---

# docker sandbox ls

## 描述

列出所有可用的沙盒。

## 使用

```
docker sandbox ls [OPTIONS]
```

## 选项

| 名称        | 简写 | 类型    | 默认值 | 描述                                                                 |
|-------------|------|---------|--------|----------------------------------------------------------------------|
| --format    | -f   | string  |        | 使用自定义输出格式打印输出：<br>`--format '{{.Name}}'`               |
| --no-trunc  |      | bool    | false  | 不截断输出                                                            |
| --quiet     | -q   | bool    | false  | 仅显示沙盒 ID                                                         |

## 示例

### 使用自定义格式列出所有沙盒

```
$ docker sandbox ls --format '{{.Name}}'
```

### 列出所有沙盒的 ID

```
$ docker sandbox ls -q
```

### 列出所有沙盒（不截断输出）

```
$ docker sandbox ls --no-trunc
```