# 格式化命令和日志输出

Docker 支持 [Go templates](https://golang.org/pkg/text/template/)，您可以用它来操作某些命令和日志驱动的输出格式。

Docker 提供了一套基本函数来操作模板元素。
所有这些示例都使用 `docker inspect` 命令，但许多其他 CLI 命令都有一个 `--format` 标志，并且许多 CLI 命令参考都包含了自定义输出格式的示例。

> [!NOTE]
>
> 使用 `--format` 标志时，您需要注意您的 shell 环境。
> 在 POSIX shell 中，您可以使用单引号运行以下命令：
>
> ```console
> $ docker inspect --format '{{join .Args " , "}}'
> ```
>
> 否则，在 Windows shell（例如 PowerShell）中，您需要使用单引号，并按如下方式对参数内的双引号进行转义：
>
> ```console
> $ docker inspect --format '{{join .Args \" , \"}}'
> ```
>

## join

`join` 连接一个字符串列表以创建单个字符串。
它会在列表中的每个元素之间放置一个分隔符。

```console
$ docker inspect --format '{{join .Args " , "}}' container
```

## table

`table` 指定您希望在其输出中看到的字段。

```console
$ docker image list --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

## json

`json` 将一个元素编码为 json 字符串。

```console
$ docker inspect --format '{{json .Mounts}}' container
```

## lower

`lower` 将字符串转换为小写形式。

```console
$ docker inspect --format "{{lower .Name}}" container
```

## split

`split` 使用分隔符将字符串切片成一个字符串列表。

```console
$ docker inspect --format '{{split .Image ":"}}' container
```

## title

`title` 将字符串的首字母大写。

```console
$ docker inspect --format "{{title .Name}}" container
```

## upper

`upper` 将字符串转换为大写形式。

```console
$ docker inspect --format "{{upper .Name}}" container
```

## pad

`pad` 为字符串添加空白填充。您可以指定要在字符串前后添加的空格数。

```console
$ docker image list --format '{{pad .Repository 5 10}}'
```

本示例在镜像仓库名称前添加 5 个空格，在名称后添加 10 个空格。

## truncate

`truncate` 将字符串缩短到指定长度。如果字符串短于指定长度，则保持不变。

```console
$ docker image list --format '{{truncate .Repository 15}}'
```

本示例显示镜像仓库名称，如果名称超过 15 个字符，则截断为前 15 个字符。

## println

`println` 将每个值打印在新的一行上。

```console
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{println .IPAddress}}{{end}}' container
```

## Hint

要找出可以打印哪些数据，请将所有内容以 json 格式显示：

```console
$ docker container ls --format='{{json .}}'
```
