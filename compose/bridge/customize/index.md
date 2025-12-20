# 自定义 Compose Bridge





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 4.43.0 and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



您可以自定义 Compose Bridge 将 Docker Compose 文件转换为特定平台格式的方式。

本页介绍 Compose Bridge 如何使用模板生成 Kubernetes 清单，以及如何根据您的特定需求和需求自定义这些模板，或者如何构建您自己的转换。

## 工作原理

Compose Bridge 使用转换来让您将 Compose 模型转换为另一种形式。

转换被打包为 Docker 镜像，该镜像接收完全解析的 Compose 模型作为 `/in/compose.yaml`，并可以在 `/out` 下生成任何目标格式文件。

Compose Bridge 包含一个使用 Go 模板的默认 Kubernetes 转换，您可以通过替换或扩展模板来自定义它。

### 模板语法

Compose Bridge 使用模板将 Compose 配置文件转换为 Kubernetes 清单。模板是纯文本文件，使用 [Go 模板语法](https://pkg.go.dev/text/template)。这使得可以插入逻辑和数据，使模板根据 Compose 模型动态且可适应。

当执行模板时，它必须生成一个 YAML 文件，这是 Kubernetes 清单的标准格式。只要用 `---` 分隔，就可以生成多个文件。

每个 YAML 输出文件都以自定义头部符号开头，例如：

```yaml
#! manifest.yaml
```

在以下示例中，模板遍历 `compose.yaml` 文件中定义的服务。对于每个服务，都会生成一个专用的 Kubernetes 清单文件，该文件根据服务命名并包含指定的配置。

```yaml
{{ range $name, $service := .services }}
---
#! {{ $name }}-manifest.yaml
# 生成的代码，请勿编辑
key: value
## ...
{{ end }}
```

### 输入模型

您可以通过运行 `docker compose config` 来生成输入模型。

这个规范的 YAML 输出用作 Compose Bridge 转换的输入。在模板中，使用点符号访问 `compose.yaml` 中的数据，使您可以浏览嵌套的数据结构。例如，要访问服务的部署模式，您可以使用 `service.deploy.mode`：

```yaml
# 遍历 yaml 序列
{{ range $name, $service := .services }}
  # 使用点符号访问嵌套属性
  {{ if eq $service.deploy.mode "global" }}
kind: DaemonSet
  {{ end }}
{{ end }}
```

您可以查看 [Compose 规范 JSON 架构](https://github.com/compose-spec/compose-go/blob/main/schema/compose-spec.json) 以全面了解 Compose 模型。此架构概述了 Compose 模型中所有可能的配置及其数据类型。

### 辅助函数

作为 Go 模板语法的一部分，Compose Bridge 提供了一组 YAML 辅助函数，旨在高效地操作模板中的数据：

| 函数 | 描述 |
| ----------- | ----------------------------------------------------------------------------------------------------------- |
| `seconds` | 将 [duration](/reference/compose-file/extension.md#specifying-durations) 转换为整数（秒）。 |
| `uppercase` | 将字符串转换为大写。 |
| `title` | 将每个单词的首字母大写。 |
| `safe` | 将字符串转换为安全标识符（将非小写字符替换为 `-`）。 |
| `truncate` | 从列表中删除前 N 个元素。 |
| `join` | 使用分隔符将列表元素连接成单个字符串。 |
| `base64` | 将字符串编码为 base64（用于 Kubernetes 密钥）。 |
| `map` | 使用 `“value -> newValue”` 语法映射值。 |
| `indent` | 将字符串内容缩进 N 个空格。 |
| `helmValue` | 输出 Helm 风格的模板值。 |

在以下示例中，模板检查是否为服务指定了健康检查间隔，应用 `seconds` 函数将此间隔转换为秒，并将值分配给 `periodSeconds` 属性。

```yaml
{{ if $service.healthcheck.interval }}
            periodSeconds: {{ $service.healthcheck.interval | seconds }}{{ end }}
{{ end }}
```

## 自定义默认模板

由于 Kubernetes 是一个多功能平台，因此有许多方法可以将 Compose 概念映射到 Kubernetes 资源定义。Compose Bridge 允许您自定义转换以匹配您自己的基础架构决策和偏好，具有不同程度的灵活性和工作量。

### 修改默认模板

您可以提取默认转换 `docker/compose-bridge-kubernetes` 使用的模板：

```console
$ docker compose bridge transformations create --from docker/compose-bridge-kubernetes my-template
```

模板被提取到以您的模板名称命名的目录中，在本例中为 `my-template`。它包括：

- 一个 Dockerfile，可让您创建自己的镜像来分发您的模板
- 一个包含模板文件的目录

根据需要编辑、[添加](#add-your-own-templates) 或删除模板。

然后，您可以使用生成的 Dockerfile 将您的更改打包到一个新的转换镜像中，然后您可以将其与 Compose Bridge 一起使用：

```console
$ docker build --tag mycompany/transform --push .
```

使用您的转换作为替换：

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

这些模板可以被扩展或替换，以更改 Docker Model Runner 的部署或配置方式。

有关更多详细信息，请参阅 [使用 Model Runner](use-model-runner.md)。

### 添加您自己的模板

对于 Compose Bridge 默认转换不管理的资源，您可以构建自己的模板。

`compose.yaml` 模型可能不提供填充目标清单所需的所有配置属性。如果是这种情况，您可以依赖 Compose 自定义扩展来更好地描述应用程序，并提供一个不可知的转换。

例如，如果您在 `compose.yaml` 文件中的服务定义中添加 `x-virtual-host` 元数据，您可以使用以下自定义属性来生成 Ingress 规则：

```yaml
{{ $project := .name }}
#! {{ $name }}-ingress.yaml
# 生成的代码，请勿编辑
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

一旦打包成 Docker 镜像，您可以在将 Compose 模型转换为 Kubernetes 时使用此自定义模板，以及其他转换：

```console
$ docker compose bridge convert \
    --transformation docker/compose-bridge-kubernetes \
    --transformation mycompany/transform
```

### 构建您自己的转换

虽然 Compose Bridge 模板使得只需少量更改即可轻松自定义，但您可能希望进行重大更改，或依赖现有的转换工具。

Compose Bridge 转换是一个 Docker 镜像，旨在从 `/in/compose.yaml` 获取 Compose 模型，并在 `/out` 下生成平台清单。这个简单的约定使得使用 [Kompose](https://kompose.io/) 捆绑替代转换变得容易：

```Dockerfile
FROM alpine

# 从 github 发布页面获取 kompose
RUN apk add --no-cache curl
ARG VERSION=1.32.0
RUN ARCH=$(uname -m | sed 's/armv7l/arm/g' | sed 's/aarch64/arm64/g' | sed 's/x86_64/amd64/g') && \
    curl -fsL \
    "https://github.com/kubernetes/kompose/releases/download/v${VERSION}/kompose-linux-${ARCH}" \
    -o /usr/bin/kompose
RUN chmod +x /usr/bin/kompose

CMD ["/usr/bin/kompose", "convert", "-f", "/in/compose.yaml", "--out", "/out"]
```

此 Dockerfile 捆绑了 Kompose 并定义了根据 Compose Bridge 转换约定运行此工具的命令。
