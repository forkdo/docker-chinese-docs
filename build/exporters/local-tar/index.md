# 本地与 tar 导出器


`local` 和 `tar` 导出器将构建结果的根文件系统输出到本地目录。它们对于生成非容器镜像的制品很有用。

- `local` 导出文件和目录。
- `tar` 导出相同的内容，但将导出打包成 tar 包。

## 概要（Synopsis）

使用 `local` 导出器构建容器镜像：

```console
$ docker buildx build --output type=local[,parameters] .
$ docker buildx build --output type=tar[,parameters] .
```

下表描述了可用的参数：

| 参数             | 类型    | 默认值  | 描述                                                                         |
| ---------------- | ------- | ------- | ---------------------------------------------------------------------------- |
| `dest`           | String  |         | 要复制文件到的路径                                                           |
| `platform-split` | Boolean | `true`  | 仅 `local` 导出器。将多平台输出拆分到平台子目录中。                          |

## 使用 local 导出器的多平台构建

`platform-split` 参数控制多平台构建输出的组织方式。

考虑这个创建平台特定文件的 Dockerfile：

```dockerfile
FROM busybox AS build
ARG TARGETOS
ARG TARGETARCH
RUN mkdir /out && echo foo > /out/hello-$TARGETOS-$TARGETARCH

FROM scratch
COPY --from=build /out /
```

### 按平台拆分（默认）

默认情况下，local 导出器为每个平台创建一个单独的子目录：

```console
$ docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --output type=local,dest=./output \
  .
```

这会生成以下目录结构：

```text
output/
├── linux_amd64/
│   └── hello-linux-amd64
└── linux_arm64/
    └── hello-linux-arm64
```

### 合并所有平台

要将所有平台的文件合并到同一目录中，请设置 `platform-split=false`：

```console
$ docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --output type=local,dest=./output,platform-split=false \
  .
```

这会生成一个扁平的目录结构：

```text
output/
├── hello-linux-amd64
└── hello-linux-arm64
```

来自所有平台的文件合并到单个目录中。如果多个平台生成了名称相同的文件，导出将因错误而失败。

### 单平台构建

单平台构建直接导出到目标目录，不创建平台子目录：

```console
$ docker buildx build \
  --platform linux/amd64 \
  --output type=local,dest=./output \
  .
```

这会生成：

```text
output/
└── hello-linux-amd64
```

即使对于单平台构建，要包含平台子目录，请显式设置 `platform-split=true`：

```console
$ docker buildx build \
  --platform linux/amd64 \
  --output type=local,dest=./output,platform-split=true \
  .
```

这会生成：

```text
output/
└── linux_amd64/
    └── hello-linux-amd64
```

## 延伸阅读

有关 `local` 或 `tar` 导出器的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#local-directory)。

