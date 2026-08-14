# 构建策略简介


构建策略让你能够在 Docker 构建运行之前验证其输入。本教程将引导你创建第一个策略，并在此过程中讲授你所需的 Rego 基础知识。

## 你将学到什么

到本教程结束时，你将理解：

- 如何创建和组织策略文件
- 基本的 Rego 语法和模式
- 如何编写验证 URL、校验和以及镜像的策略
- 策略在构建期间如何评估

## 先决条件

- Buildx 0.31 或更高版本
- 对 Dockerfile 和镜像构建有基本了解

## 策略工作原理（How policies work）

当你构建镜像时，Buildx 会解析你的 Dockerfile 引用的所有输入：来自 `FROM` 指令的基础镜像、来自 `ADD` 或 `COPY` 或构建上下文的文件，以及 Git 仓库。在运行构建之前，Buildx 会针对这些输入评估你的策略。如果有任何输入违反了策略，构建会在任何指令执行之前失败。

策略使用 Rego 编写，Rego 是一种为表达规则和约束而设计的声明式语言。你无需了解 Rego 即可开始——本教程会教你所需的内容。

## 创建你的第一个策略

为本教程创建一个新目录并添加一个 Dockerfile：

```console
$ mkdir policy-tutorial
$ cd policy-tutorial
```

创建一个使用 `ADD` 下载文件的 `Dockerfile`：

```dockerfile
FROM scratch
ADD https://example.com/index.html /index.html
```

现在创建一个策略文件。策略使用 `.rego` 扩展名，并与你的 Dockerfile 放在一起。创建 `Dockerfile.rego`：

```rego {title="Dockerfile.rego"}
package docker

default allow := false

allow if input.local
allow if {
  input.http.host == "example.com"
}

decision := {"allow": allow}
```

将此文件保存为 `Dockerfile.rego`，与你的 Dockerfile 位于同一目录中。

让我们拆解一下这个策略的作用：

- `package docker` - 所有构建策略都必须以此包声明开头
- `default allow := false` - 此示例使用默认拒绝规则：如果输入不匹配某个 `allow` 规则，策略检查就会失败
- `allow if input.local` - 第一条规则允许任何本地文件（你的构建上下文）
- `allow if { input.http.host == "example.com" }` - 第二条规则允许来自 `example.com` 的 HTTP 下载
- `decision := {"allow": allow}` - 最终的决策对象告诉 Buildx 是允许还是拒绝该输入

这条策略的意思是："只允许本地文件和来自 `example.com` 的 HTTP 下载"。Rego 会评估所有策略规则，以确定每个构建输入的 `decision` 变量返回值。评估是并行且按需进行的；策略规则的顺序无关紧要。

### 关于 `input.local`

你几乎会在每条策略中看到 `allow if input.local`。这条规则允许本地文件访问，包括你的构建上下文（通常是 `.` 目录），而且重要的是还包括 Dockerfile 本身。如果没有这条规则，Buildx 就无法读取你的 Dockerfile 来启动构建。

即使是不引用构建上下文中任何文件的构建，通常也需要 `input.local`，因为 Dockerfile 是一个本地文件。策略在构建开始之前评估，而拒绝本地访问就意味着拒绝访问 Dockerfile。

在极少数情况下，你可能想要更严格的本地文件策略——例如，在构建上下文直接使用 Git URL 作为上下文的 CI 构建中。在这些情况下，你可能想要拒绝本地来源，以防止未跟踪的文件或更改进入你的构建。

## 自动加载策略

Buildx 会自动加载与你的 Dockerfile 名称匹配的策略。当你使用 `Dockerfile` 构建时，Buildx 会在同一目录中查找 `Dockerfile.rego`。对于名为 `app.Dockerfile` 的文件，它会查找 `app.Dockerfile.rego`。

这种自动加载意味着在大多数情况下你不需要任何命令行标志——创建策略文件并构建即可。

策略文件必须与 Dockerfile 位于同一目录。如果 Buildx 找不到匹配的策略，构建将在不进行策略评估的情况下继续进行（除非你使用 `--policy strict=true`）。

要对策略加载进行更多控制，请参阅 [用法指南](./usage.md)。

## 使用你的策略运行构建

在启用策略评估的情况下构建镜像：

```console
$ docker build .
```

构建成功，因为你的 Dockerfile 中的 URL 与策略匹配。现在尝试将 Dockerfile 中的 URL 更改为其他内容：

```dockerfile
FROM scratch
ADD https://api.github.com/users/octocat /user.json
```

再次构建：

```console
$ docker build .
```

这次构建因策略违规而失败。`api.github.com` 主机名与你的策略中的规则不匹配，因此 Buildx 会在运行任何构建步骤之前拒绝它。

## 调试策略失败

如果你的构建因策略违规而失败，请使用 `--progress=plain` 来准确查看出了什么问题：

```console
$ docker buildx build --progress=plain .
```

这会显示所有策略检查、每个源的输入数据以及允许/拒绝决策。有关完整的调试指南，请参阅 [调试](./debugging.md)。

## 添加有用的错误消息

当策略拒绝某个输入时，用户会看到一条通用错误消息。你可以提供自定义消息来解释构建被拒绝的原因：

```rego {title="Dockerfile.rego"}
package docker

default allow := false

allow if input.local
allow if {
  input.http.host == "example.com"
  input.http.schema == "https"
}

deny_msg contains msg if {
  not allow
  input.http
  msg := "only HTTPS downloads from example.com are allowed"
}

decision := {"allow": allow, "deny_msg": deny_msg}
```

现在，当构建被拒绝时，用户会看到你的自定义消息，解释出了什么问题：

```console
$ docker buildx build .
Policy: only HTTPS downloads from example.com are allowed
ERROR: failed to build: ... source not allowed by policy
```

`deny_msg` 规则使用 `contains` 将消息添加到一个集合中。你可以为不同的失败条件添加多个拒绝消息，以帮助用户准确理解需要更改什么。

## 理解 Rego 规则

Rego 策略由规则构成。规则定义了何时允许某件事。基本模式是：

```rego
allow if {
    condition_one
    condition_two
    condition_three
}
```

所有条件都必须为真，规则才能匹配。把它看作一个 AND（与）操作——URL 必须匹配 AND 校验和必须匹配 AND 你指定的任何其他条件。

你可以在一个策略中拥有多个 `allow` 规则。如果任何规则匹配，输入就被允许：

```rego
# 允许来自 example.com 的下载
allow if {
    input.http.host == "example.com"
}

# 也允许来自 api.github.com 的下载
allow if {
    input.http.host == "api.github.com"
}
```

这就像 OR（或）一样工作——输入可以匹配第一条规则 OR 第二条规则。

## 访问输入字段

`input` 对象让你可以访问有关构建输入的信息。其结构取决于输入类型：

- `input.http` - 使用 `ADD https://...` 下载的文件
- `input.image` - 来自 `FROM` 或 `COPY --from` 的容器镜像
- `input.git` - 来自 `ADD git://...` 或构建上下文的 Git 仓库
- `input.local` - 本地文件上下文

有关所有可用输入字段，请参阅 [输入参考](./inputs.md)。

对于 HTTP 下载，你可以访问：

| 键                   | 描述                       | 示例                             |
| ------------------- | -------------------------- | -------------------------------- |
| `input.http.url`    | 完整 URL                   | `https://example.com/index.html` |
| `input.http.schema` | 协议（HTTP/HTTPS）         | `https`                          |
| `input.http.host`   | 主机名                     | `example.com`                    |
| `input.http.path`   | URL 路径，包括参数         | `/index.html`                    |

更新你的策略以要求 HTTPS：

```rego
package docker

default allow := false

allow if {
    input.http.host == "example.com"
    input.http.schema == "https"
}

decision := {"allow": allow}
```

现在该策略要求主机名必须是 `example.com` 且协议必须是 HTTPS。HTTP URL（不带 TLS）将通过策略检查失败。

## 模式匹配与字符串

Rego 提供 [内置函数](https://www.openpolicyagent.org/docs/policy-language#built-in-functions) 用于模式匹配。使用 `startswith()` 匹配 URL 前缀：

[built-in functions]: https://www.openpolicyagent.org/docs/policy-language#built-in-functions

```rego
allow if {
    startswith(input.http.url, "https://example.com/")
}
```

这允许任何以 `https://example.com/` 开头的 URL。

使用 `regex.match()` 处理复杂模式：

```rego
allow if {
    regex.match(`^https://example\.com/.+\.json$`, input.http.url)
}
```

这会匹配满足以下条件的 URL：

- 以 `https://example.com/` 开头
- 以 `.json` 结尾
- 在域名和扩展名之间至少有一个字符

## 策略文件位置

策略文件位于它所验证的 Dockerfile 旁边，使用 `<dockerfile-name>.rego` 命名模式：

```text
project/
├── Dockerfile           # 主 Dockerfile
├── Dockerfile.rego      # Dockerfile 的策略
├── lint.Dockerfile      # 用于 lint 的 Dockerfile
└── lint.Dockerfile.rego # lint.Dockerfile 的策略
```

当你构建时，Buildx 会自动加载相应的策略文件：

```console
$ docker buildx build -f Dockerfile .        # 加载 Dockerfile.rego
$ docker buildx build -f lint.Dockerfile .   # 加载 lint.Dockerfile.rego
```

## 下一步

你现在理解了如何为 HTTP 资源编写基本的构建策略。要继续学习：

- 应用和测试策略：[使用构建策略](./usage.md)
- 学习 [镜像验证](./validate-images.md) 以验证来自 `FROM` 指令的容器镜像
- 学习 [Git 验证](./validate-git.md) 以验证构建中使用的 Git 仓库
- 请参阅 [示例策略](./examples.md) 获取可直接复制粘贴的常见场景策略
- 为你的策略编写单元测试：[测试构建策略](./testing.md)
- 调试策略失败：[调试](./debugging.md)
- 阅读 [输入参考](./inputs.md) 了解所有可用的输入字段
- 查看 [内置函数](./built-ins.md) 了解签名验证、证明以及其他安全检查

