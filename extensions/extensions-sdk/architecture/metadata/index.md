# 扩展元数据

## metadata.json 文件

`metadata.json` 文件是您扩展的入口点。它包含扩展的元数据，例如名称、版本和描述。它还包含构建和运行扩展所需的信息。Docker 扩展的镜像必须在其文件系统的根目录包含一个 `metadata.json` 文件。

`metadata.json` 文件的格式必须是：

```json
{
    "icon": "extension-icon.svg",
    "ui": ...
    "vm": ...
    "host": ...
}
```

`ui`、`vm` 和 `host` 部分是可选的，取决于给定扩展提供的内容。它们描述了要安装的扩展内容。

### UI 部分

`ui` 部分定义了一个添加到 Docker Desktop 仪表板的新选项卡。其形式如下：

```json
"ui":{
    "dashboard-tab":
    {
        "title":"MyTitle",
        "root":"/ui",
        "src":"index.html"
    }
}
```

`root` 指定扩展镜像文件系统内 UI 代码所在的文件夹。
`src` 指定应在扩展选项卡中加载的入口点。

其他 UI 扩展点将在未来提供。

### VM 部分

`vm` 部分定义了在 Desktop VM 内部运行的后端服务。它必须定义一个 `image` 或一个 `compose.yaml` 文件，以指定要在 Desktop VM 中运行的服务。

```json
"vm": {
    "image":"${DESKTOP_PLUGIN_IMAGE}"
},
```

当您使用 `image` 时，会为扩展生成一个默认的 Compose 文件。

> `${DESKTOP_PLUGIN_IMAGE}` 是一个特定的关键词，它提供了一种引用打包扩展的镜像的简便方法。
> 这里也可以指定任何其他完整的镜像名称。但是，在许多情况下，使用相同的镜像会使扩展开发更容易。

```json
"vm": {
    "composefile": "compose.yaml"
},
```

Compose 文件（例如包含卷定义）如下所示：

```yaml
services:
  myExtension:
    image: ${DESKTOP_PLUGIN_IMAGE}
    volumes:
      - /host/path:/container/path
```

### Host 部分

`host` 部分定义了 Docker Desktop 复制到主机上的可执行文件。

```json
  "host": {
    "binaries": [
      {
        "darwin": [
          {
            "path": "/darwin/myBinary"
          },
        ],
        "windows": [
          {
            "path": "/windows/myBinary.exe"
          },
        ],
        "linux": [
          {
            "path": "/linux/myBinary"
          },
        ]
      }
    ]
  }
```

`binaries` 定义了一个列表，包含 Docker Desktop 从扩展镜像复制到主机的二进制文件。

`path` 指定镜像文件系统中的二进制文件路径。Docker Desktop 负责将这些文件复制到其自己的位置，JavaScript API 允许调用这些二进制文件。

了解如何[调用可执行文件](../guides/invoke-host-binaries.md)。
