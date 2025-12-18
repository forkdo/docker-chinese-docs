---
title: 自定义 Compose Bridge 
linkTitle: 自定义
weight: 20
description: 了解如何使用 Go 模板和 Compose 扩展自定义 Compose Bridge 转换
keywords: docker compose bridge, customize compose bridge, compose bridge templates, compose to kubernetes, compose bridge transformation, go templates docker
---

{{< summary-bar feature_name="Compose bridge" >}}

你可以自定义 Compose Bridge 如何将 Docker Compose 文件转换为特定平台的格式。

本文档解释了 Compose Bridge 如何使用模板生成 Kubernetes 清单，以及如何自定义这些模板以满足你的特定需求，或者如何构建自己的转换。

## 工作原理

Compose Bridge 使用转换（transformation）将 Compose 模型转换为另一种形式。

转换被打包为 Docker 镜像，接收完全解析的 Compose 模型作为 `/in/compose.yaml`，并可在 `/out` 下生成任意目标格式文件。

Compose Bridge 包含一个默认的 Kubernetes 转换，使用 Go 模板，你可以通过替换或扩展模板来自定义这些模板。

### 模板语法

Compose Bridge 使用模板将 Compose 配置文件转换为 Kubernetes 清单。模板是纯文本文件，使用 [Go 模板语法](https://pkg.go.dev/text/template)。这允许插入逻辑和数据，使模板根据 Compose 模型动态且可适应。

当模板执行时，它必须生成一个 YAML 文件，这是 Kubernetes 清单的标准格式。只要用 `---` 分隔，就可以生成多个文件。

每个 YAML 输出文件都以自定义头注释开始，例如：

```yaml
#! manifest.yaml
```

在以下示例中，模板遍历 `compose.yaml` 文件中定义的服务。为每个服务生成一个专用的 Kubernetes 清单文件，文件名根据服务命名，并包含指定的配置。

```yaml
{{ range $name, $service := .services }}
---
#! {{ $name }}-manifest.yaml
# Generated code, do not edit
key: value
## ...
{{ end }}
```

### 输入模型

你可以通过运行 `docker compose config` 生成输入模型。

这个规范的 YAML 输出作为 Compose Bridge 转换的输入。在模板中，使用点表示法访问 `compose.yaml` 中的数据，允许你遍历嵌套的数据结构。例如，要访问服务的部署模式，你可以使用 `service.deploy.mode`：

 ```yaml
# iterate over a yaml sequence
{{ range $name, $service := .services }}
  # access a nested attribute using dot notation
  {{ if eq $service.deploy.mode "global" }}
kind: DaemonSet
  {{ end }}
{{ end }}
```

你可以查看 [Compose Specification JSON schema](https://github.com/compose-spec/compose-go/blob/main/schema/compose-spec.json) 以获得 Compose 模型的完整概述。此 schema 概述了 Compose 模型中所有可能的配置及其数据类型。

### 辅助函数

作为 Go 模板语法的一部分，Compose Bridge 提供了一组 YAML 辅助函数，旨在模板中高效地操作数据：

| 函数        | 描述                                                                                                       |
| ----------- | ---------------------------------------------------------------------------------------------------------- |
| `seconds`   | 将 [持续时间](/reference/compose-file/extension.md#specifying-durations) 转换为整数（秒）。                 |
| `uppercase` | 将字符串转换为大写。                                                                                       |
| `title`     | 大写每个单词的首字母。                                                                                     |
| `safe`      | 将字符串转换为安全标识符（将非小写字符替换为 `-`）。                                                       |
| `truncate`  | 从列表中移除前 N 个元素。                                                                                  |
| `join`      | 使用分隔符将列表元素连接为单个字符串。                                                                     |
| `base64`    | 将字符串编码为 base64（用于 Kubernetes secrets）。                                                         |
| `map`       | 使用 `"value -> newValue"` 语法映射值。                                                                    |
| `indent`    | 将字符串内容缩进 N 个空格。                                                                                |
| `helmValue` | 输出 Helm 风格的模板值。                                                                                   |

在以下示例中，模板检查服务是否指定了健康检查间隔，应用 `seconds` 函数将此间隔转换为秒，并将值赋给 `periodSeconds` 属性。

```yaml
{{ if $service.healthcheck.interval }}
            periodSeconds: {{ $service.healthcheck.interval | seconds }}{{ end }}
{{ end }}
```

## 自定义默认模板

由于 Kubernetes 是一个多功能平台，有多种方式可以将 Compose 概念映射到 Kubernetes 资源定义。Compose Bridge 允许你自定义转换以匹配你自己的基础设施决策和偏好，灵活性和工作量各不相同。

### 修改默认模板

你可以从默认转换 `docker/compose-bridge-kubernetes` 中提取模板：

```console
$ docker compose bridge transformations create --from docker/compose-bridge-kubernetes my-template
``` 

模板被提取到一个以你的模板名称命名的目录中，在此情况下为 `my-template`。它包括：

- 一个 Dockerfile，允许你创建自己的镜像来分发你的模板
- 一个包含模板文件的目录

根据需要编辑、[添加](#add-your-own-templates) 或删除模板。

然后你可以使用生成的 Dockerfile 将你的更改打包到新的转换镜像中，然后在 Compose Bridge 中使用：

```console
$ docker build --tag mycompany/transform --push .
```

使用你的转换作为替代：

```console
$ docker compose bridge convert --transformations mycompany/transform 
```

#### Model Runner 模板

默认转换还包括用于使用 LLM 的应用程序的模板：

- `model-runner-deployment.tmpl`
- `model-runner-service.tmpl`
- `model-runner-pvc.tmpl`
- `/overlays/model-runner/kustomization.yaml`
- `/overlays/desktop/deployment.tmpl`

这些模板可以扩展或替换，以更改 Docker Model Runner 的部署或配置方式。

更多详情，请参阅 [使用 Model Runner](use-model-runner.md)。

### 添加你自己的模板

对于未由 Compose Bridge 默认转换管理的资源，你可以构建自己的模板。

`compose.yaml` 模型可能不提供填充目标清单所需的所有配置属性。在这种情况下，你可以依赖 Compose 自定义扩展来更好地描述应用程序，并提供与平台无关的转换。

例如，如果你在 `compose.yaml` 文件中的服务定义中添加 `x-virtual-host` 元数据，你可以使用以下自定义属性生成 Ingress 规则：

```yaml
{{ $project := .name }}
#! {{ $name }}-ingress.yaml
# Generated code, do not edit
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: virtual-host-ingress
  namespace: {{ $project }}
spec:
  rules:  
{{ range $name, $service := .services }}
{{ range index $service "x-virtual-host" }}
  - host: ${{ . }}
    http:
      paths:
      - path: "/"
        backend:
          service:
            name: ${{ name }}
            port:
              number: 80  
{{ end }}
{{ end }}
```

一旦打包到 Docker 镜像中，你可以在将 Compose 模型转换为 Kubernetes 时使用此自定义模板，与其他转换一起使用：

```console
$ docker compose bridge convert \
    --transformation docker/compose-bridge-kubernetes \
    --transformation mycompany/transform 
```

### 构建你自己的转换

虽然 Compose Bridge 模板可以轻松自定义且改动最小，你可能希望进行重大更改，或依赖现有的转换工具。

Compose Bridge 转换是一个 Docker 镜像，设计为从 `/in/compose.yaml` 获取 Compose 模型，并在 `/out` 下生成平台清单。这个简单的约定使得使用 [Kompose](https://kompose.io/) 打包替代转换变得简单：

```Dockerfile
FROM alpine

# Get kompose from github release page
RUN apk add --no-cache curl
ARG VERSION=1.32.0
RUN ARCH=$(uname -m | sed 's/armv7l/arm/g' | sed 's/aarch64/arm64/g' | sed 's/x86_64/amd64/g') && \
    curl -fsL \
    "https://github.com/kubernetes/kompose/releases/download/v${VERSION}/kompose-linux-${ARCH}" \
    -o /usr/bin/kompose
RUN chmod +x /usr/bin/kompose

CMD ["/usr/bin/kompose", "convert", "-f", "/in/compose.yaml", "--out", "/out"]
```

此 Dockerfile 打包了 Kompose 并根据 Compose Bridge 转换约定定义了运行此工具的命令。