# 过滤命令

您可以使用 `--filter` 标志来限定命令的作用范围。使用过滤时，命令仅包含与指定模式匹配的条目。

## 使用过滤器

`--filter` 标志需要以键值对的形式提供，并由操作符分隔。

```console
$ docker COMMAND --filter "KEY=VALUE"
```

键表示您要过滤的字段。
值是指定字段必须匹配的模式。
操作符可以是等于（`=`）或不等于（`!=`）。

例如，命令 `docker images --filter reference=alpine` 会过滤 `docker images` 命令的输出，仅打印 `alpine` 镜像。

```console
$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
ubuntu       24.04     33a5cc25d22c   36 minutes ago   101MB
ubuntu       22.04     152dc042452c   36 minutes ago   88.1MB
alpine       3.21      a8cbb8c69ee7   40 minutes ago   8.67MB
alpine       latest    7144f7bab3d4   40 minutes ago   11.7MB
busybox      uclibc    3e516f71d880   48 minutes ago   2.4MB
busybox      glibc     7338d0c72c65   48 minutes ago   6.09MB
$ docker images --filter reference=alpine
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
alpine       3.21      a8cbb8c69ee7   40 minutes ago   8.67MB
alpine       latest    7144f7bab3d4   40 minutes ago   11.7MB
```

可用字段（本例中为 `reference`）取决于您运行的命令。某些过滤器需要完全匹配，其他过滤器处理部分匹配，有些过滤器允许您使用正则表达式。

请参考每个命令的 [CLI 参考说明](#reference)，了解每个命令支持的过滤功能。

## 组合过滤器

您可以通过传递多个 `--filter` 标志来组合多个过滤器。以下示例显示了如何打印所有匹配 `alpine:latest` 或 `busybox` 的镜像——逻辑上的 `OR`。

```console
$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       24.04     33a5cc25d22c   2 hours ago   101MB
ubuntu       22.04     152dc042452c   2 hours ago   88.1MB
alpine       3.21      a8cbb8c69ee7   2 hours ago   8.67MB
alpine       latest    7144f7bab3d4   2 hours ago   11.7MB
busybox      uclibc    3e516f71d880   2 hours ago   2.4MB
busybox      glibc     7338d0c72c65   2 hours ago   6.09MB
$ docker images --filter reference=alpine:latest --filter=reference=busybox
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
alpine       latest    7144f7bab3d4   2 hours ago   11.7MB
busybox      uclibc    3e516f71d880   2 hours ago   2.4MB
busybox      glibc     7338d0c72c65   2 hours ago   6.09MB
```

### 多个否定过滤器

某些命令支持对 [标签](/manuals/engine/manage-resources/labels.md) 的否定过滤器。否定过滤器只考虑与指定模式不匹配的结果。以下命令会清理所有未标记为 `foo` 的容器。

```console
$ docker container prune --filter "label!=foo"
```

在组合多个否定标签过滤器时有一个需要注意的地方。多个否定过滤器会创建一个单一的否定约束——逻辑上的 `AND`。以下命令会清理所有未同时标记为 `foo` 和 `bar` 的容器。标记为 `foo` 或 `bar` 但不是同时标记两者的容器将被清理。

```console
$ docker container prune --filter "label!=foo" --filter "label!=bar"
```

## 参考

有关过滤命令的更多信息，请参考支持 `--filter` 标志的命令的 CLI 参考说明：

- [`docker config ls`](/reference/cli/docker/config/ls.md)
- [`docker container prune`](/reference/cli/docker/container/prune.md)
- [`docker image prune`](/reference/cli/docker/image/prune.md)
- [`docker image ls`](/reference/cli/docker/image/ls.md)
- [`docker network ls`](/reference/cli/docker/network/ls.md)
- [`docker network prune`](/reference/cli/docker/network/prune.md)
- [`docker node ls`](/reference/cli/docker/node/ls.md)
- [`docker node ps`](/reference/cli/docker/node/ps.md)
- [`docker plugin ls`](/reference/cli/docker/plugin/ls.md)
- [`docker container ls`](/reference/cli/docker/container/ls.md)
- [`docker search`](/reference/cli/docker/search.md)
- [`docker secret ls`](/reference/cli/docker/secret/ls.md)
- [`docker service ls`](/reference/cli/docker/service/ls.md)
- [`docker service ps`](/reference/cli/docker/service/ps.md)
- [`docker stack ps`](/reference/cli/docker/stack/ps.md)
- [`docker system prune`](/reference/cli/docker/system/prune.md)
- [`docker volume ls`](/reference/cli/docker/volume/ls.md)
- [`docker volume prune`](/reference/cli/docker/volume/prune.md)
