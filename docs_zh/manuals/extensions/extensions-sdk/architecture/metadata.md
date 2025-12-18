---
title: 扩展元数据
linkTitle: 元数据
description: Docker 扩展元数据
keywords: Docker, extensions, sdk, metadata
aliases:
 - /desktop/extensions-sdk/extensions/METADATA
 - /desktop/extensions-sdk/architecture/metadata/
---

## metadata.json 文件

`metadata.json` 文件是扩展的入口点。它包含扩展的元数据，例如名称、版本和描述。它还包含构建和运行扩展所需的信息。Docker 扩展的镜像必须在其文件系统根目录包含一个 `metadata.json` 文件。

`metadata.json` 文件的格式必须如下：

```json
{
    "icon": "extension-icon.svg",
    "ui": ...
    "vm": ...
    "host": ...
}
```

`ui`、`vm` 和 `host` 部分是可选的，取决于特定扩展提供的内容。它们描述了要安装的扩展内容。

### UI 部分

`ui` 部分定义了一个新标签页，该标签页将添加到 Docker Desktop 的仪表板中。它遵循以下形式：

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

`root` 指定 UI 代码在扩展镜像文件系统中的文件夹位置。`src` 指定应该在扩展标签页中加载的入口点。

其他 UI 扩展点将在未来提供。

### VM 部分

`vm` 部分定义了一个在 Desktop VM 内运行的后端服务。它必须定义一个 `image` 或 `compose.yaml` 文件，以指定在 Desktop VM 中运行什么服务。

```json
"vm": {
    "image":"${DESKTOP_PLUGIN_IMAGE}"
},
```

当你使用 `image` 时，会为扩展生成一个默认的 Compose 文件。

> `${DESKTOP_PLUGIN_IMAGE}` 是一个特定关键字，提供了一种简便方式来引用打包扩展的镜像。
> 也可以在此处指定任何其他完整镜像名称。但在许多情况下，使用同一镜像会使扩展开发更加简单。

```json
"vm": {
    "composefile": "compose.yaml"
},
```

带有卷定义示例的 Compose 文件如下所示：

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

`binaries` 定义了 Docker Desktop 从扩展镜像复制到主机的可执行文件列表。

`path` 指定镜像文件系统中可执行文件的路径。Docker Desktop 负责将这些文件复制到自己的位置，JavaScript API 允许调用这些可执行文件。

了解如何 [调用主机可执行文件](../guides/invoke-host-binaries.md)。