---
description: CLI 和日志输出格式化参考
keywords: format, formatting, output, templates, log
title: 格式化命令和日志输出
weight: 40
aliases:
  - /engine/admin/formatting/
  - /config/formatting/
---

Docker 支持 [Go 模板](https://golang.org/pkg/text/template/)，你可以使用它来操作某些命令和日志驱动的输出格式。

Docker 提供了一组基本函数来操作模板元素。
所有这些示例都使用 `docker inspect` 命令，但许多其他 CLI 命令都有 `--format` 标志，许多 CLI 命令参考文档中也包含自定义输出格式的示例。

> [!NOTE]
>
> 使用 `--format` 标志时，需要注意你的 shell 环境。
> 在 POSIX shell 中，你可以使用单引号运行以下命令：
>
> ```console
> $ docker inspect --format '{{join .Args " , "}}'
> ```
>
> 否则，在 Windows shell（例如 PowerShell）中，你需要使用单引号，但需要转义参数内的双引号，如下所示：
>
> ```console
> $ docker inspect --format '{{join .Args \" , \"}}'
> ```
>

## join

`join` 将字符串列表连接成单个字符串。
它在列表的每个元素之间放置一个分隔符。

```console
$ docker inspect --format '{{join .Args " , "}}' container
```

## table

`table` 指定你想要查看其输出的字段。

```console
$ docker image list --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

## json

`json` 将元素编码为 json 字符串。

```console
$ docker inspect --format '{{json .Mounts}}' container
```

## lower

`lower` 将字符串转换为其小写表示形式。

```console
$ docker inspect --format "{{lower .Name}}" container
```

## split

`split` 将字符串切片为由分隔符分隔的字符串列表。

```console
$ docker inspect --format '{{split .Image ":"}}' container
```

## title

`title` 将字符串的首字符大写。

```console
$ docker inspect --format "{{title .Name}}" container
```

## upper

`upper` 将字符串转换为其大写表示形式。

```console
$ docker inspect --format "{{upper .Name}}" container
```

## pad

`pad` 向字符串添加空白填充。你可以指定在字符串前后添加的空格数。

```console
$ docker image list --format '{{pad .Repository 5 10}}'
```

此示例在镜像仓库名称前添加 5 个空格，在其后添加 10 个空格。

## truncate

`truncate` 将字符串缩短到指定长度。如果字符串比指定长度短，则保持不变。

```console
$ docker image list --format '{{truncate .Repository 15}}'
```

此示例显示镜像仓库名称，如果超过 15 个字符则截断为前 15 个字符。

## println

`println` 在新行上打印每个值。

```console
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{println .IPAddress}}{{end}}' container
```

## 提示

要找出可以打印哪些数据，请以 json 格式显示所有内容：

```console
$ docker container ls --format='{{json .}}'
```