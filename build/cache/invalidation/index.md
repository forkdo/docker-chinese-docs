# 构建缓存失效


在构建镜像时，Docker 会按指定顺序逐步执行 Dockerfile 中的指令。对于每条指令，[builder](/manuals/build/builders/_index.md) 都会检查是否能够复用构建缓存中的该指令。

## 通用规则（General rules）

构建缓存失效的基本规则如下：

- builder 首先会检查基础镜像是否已被缓存。每条后续指令都会与缓存的层进行比较。如果没有任何缓存层与指令精确匹配，则缓存失效。

- 在大多数情况下，将 Dockerfile 指令与对应的缓存层进行比较就足够了。但是，有些指令需要额外的检查和解释。

- 对于 `ADD` 和 `COPY` 指令，以及带有绑定挂载的 `RUN` 指令（`RUN --mount=type=bind`），builder 会根据文件元数据计算一个缓存校验和，以确定缓存是否有效。在缓存查找期间，如果任何相关文件的文件元数据发生了变化，则缓存失效。

  文件的修改时间（`mtime`）在计算缓存校验和时不会被考虑。如果只有被复制文件的 `mtime` 发生了变化，缓存不会失效。

- 除了 `ADD` 和 `COPY` 命令外，缓存检查不会查看容器中的文件来确定缓存是否匹配。例如，在处理 `RUN apt-get -y update` 命令时，不会检查容器中更新的文件来确定是否存在缓存命中。在这种情况下，仅使用该命令字符串本身来查找匹配。

一旦缓存失效，所有后续的 Dockerfile 命令都会生成新的镜像，且不会使用缓存。

如果你的构建包含多个层，并且你希望确保构建缓存可复用，请在可能的情况下将指令按从较少变更到较频繁变更的顺序排列。

## WORKDIR 与 SOURCE_DATE_EPOCH

`WORKDIR` 指令在确定缓存有效性时会遵循 `SOURCE_DATE_EPOCH` 构建参数。在两次构建之间更改 `SOURCE_DATE_EPOCH` 会使 `WORKDIR` 及其所有后续指令的缓存失效。

`SOURCE_DATE_EPOCH` 设置构建期间创建文件的时间戳。如果你将其设置为动态值（如 Git 提交时间戳），则每次提交都会破坏缓存。在跟踪构建来源时，这是预期的行为。

要在不频繁造成缓存失效的情况下进行可复现构建，请使用固定的时间戳：

```console
$ docker build --build-arg SOURCE_DATE_EPOCH=0 .
```

## RUN 指令（RUN instructions）

`RUN` 指令的缓存在两次构建之间不会自动失效。假设你的 Dockerfile 中有一个安装 `curl` 的步骤：

```dockerfile
FROM alpine:3.23 AS install
RUN apk add curl
```

这并不意味着你镜像中的 `curl` 版本始终是最新的。一周后重新构建镜像，仍然会得到与之前相同的软件包。要强制重新执行 `RUN` 指令，你可以：

- 确保它之前的某一层已发生变化
- 在构建之前使用 [`docker builder prune`](/reference/cli/docker/builder/prune/) 清除构建缓存
- 使用 `--no-cache` 或 `--no-cache-filter` 选项

`--no-cache-filter` 选项让你指定要使其缓存失效的特定构建阶段：

```console
$ docker build --no-cache-filter install .
```

## 构建密钥（Build secrets）

构建密钥的内容不属于构建缓存。更改密钥的值不会导致缓存失效。

如果你希望在更改密钥值后强制缓存失效，你可以传递一个构建参数，并附带一个你在更改密钥时也会更改的任意值。构建参数确实会导致缓存失效。

```dockerfile
FROM alpine
ARG CACHEBUST
RUN --mount=type=secret,id=TOKEN,env=TOKEN \
    some-command ...
```

```console
$ TOKEN="tkn_pat123456" docker build --secret id=TOKEN --build-arg CACHEBUST=1 .
```

密钥的属性（如 ID 和挂载路径）会参与缓存校验和的计算，如果发生变化会导致缓存失效。

