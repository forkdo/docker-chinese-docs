# 验证 Git 仓库


Git 仓库经常作为源代码输入出现在 Docker 构建中。`ADD` 指令可以克隆仓库，构建上下文也可以引用 Git URL。验证这些输入可确保你是从受信任的源和经过验证的版本构建的。

本指南将教你编写验证 Git 输入的策略，从基本的版本固定到验证已签名的提交和标签。

## 先决条件

你应该已从 [简介](./intro.md) 了解了策略基础知识：创建策略文件、基本的 Rego 语法，以及策略在构建期间如何评估。

## 什么是 Git 输入？

Git 输入来自引用 Git 仓库的 `ADD` 指令：

```dockerfile
# 克隆特定标签
ADD https://github.com/moby/buildkit.git#v0.26.1 /buildkit

# 克隆分支
ADD https://github.com/user/repo.git#main /src

# 克隆提交
ADD https://github.com/user/repo.git#abcde123 /src
```

当你使用以下方式构建时，构建上下文也可以是 Git 仓库：

```console
$ docker build https://github.com/user/repo.git#main
```

每个 Git 引用都会触发一次策略评估。你的策略可以检查仓库 URL、验证版本、检查提交元数据并验证签名。

## 匹配特定仓库

最简单的 Git 策略是限制可以使用哪些仓库：

```rego {title="Dockerfile.rego"}
package docker

default allow := false

allow if input.local

allow if {
  input.git.host == "github.com"
  input.git.remote == "https://github.com/moby/buildkit.git"
}

decision := {"allow": allow}
```

此策略：

- 默认拒绝所有输入
- 允许本地构建上下文
- 仅允许来自 GitHub 的 BuildKit 仓库

`host` 字段包含 Git 服务器主机名，`remote` 包含完整的仓库 URL。测试它：

```dockerfile {title="Dockerfile"}
FROM scratch
ADD https://github.com/moby/buildkit.git#v0.26.1 /
```

```console
$ docker build .
```

构建成功。尝试一个不同的仓库，它会失败。

你可以使用额外的规则匹配多个仓库：

```rego
allow if {
  input.git.host == "github.com"
  input.git.remote == "https://github.com/moby/buildkit.git"
}

allow if {
  input.git.host == "github.com"
  input.git.remote == "https://github.com/docker/cli.git"
}

decision := {"allow": allow}
```

## 固定到特定版本

标签和分支会随时间变化。固定到特定版本以确保可复现的构建：

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  input.git.tagName == "v0.26.1"
}

decision := {"allow": allow}
```

当 Git 引用指向标签时，`tagName` 字段包含标签名称。对分支使用 `branch`：

```rego
allow if {
  input.git.remote == "https://github.com/user/repo.git"
  input.git.branch == "main"
}
```

或者对任何类型的引用（分支、标签或提交 SHA）使用 `ref`：

```rego
allow if {
  input.git.ref == "v0.26.1"
}
```

## 使用版本允许列表

对于你信任但想控制版本的仓库，维护一个允许列表：

```rego
package docker

default allow := false

allowed_versions = [
    {"tag": "v0.26.1", "annotated": true, "sha": "abc123"},
]

is_buildkit if {
    input.git.remote == "https://github.com/moby/buildkit.git"
}

allow if {
    not is_buildkit
}

allow if {
    is_buildkit
    some version in allowed_versions
    input.git.tagName == version.tag
    input.git.isAnnotatedTag == version.annotated
    startswith(input.git.commitChecksum, version.sha)
}

decision := {"allow": allow}
```

此策略：

- 定义一个带有元数据的已批准版本允许列表
- 使用一个辅助规则（`is_buildkit`）以提高可读性
- 允许所有非 BuildKit 的输入
- 对于 BuildKit，根据允许列表检查标签名称、它是否为带注释标签以及提交 SHA

辅助规则使复杂策略更易于维护。随着新版本被批准，你可以扩展允许列表：

```rego
allowed_versions = [
    {"tag": "v0.26.1", "annotated": true, "sha": "abc123"},
    {"tag": "v0.27.0", "annotated": true, "sha": "def456"},
    {"tag": "v0.27.1", "annotated": true, "sha": "789abc"},
]
```

## 使用正则表达式模式验证

使用模式匹配来实现语义化版本：

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  regex.match(`^v[0-9]+\.[0-9]+\.[0-9]+$`, input.git.tagName)
}

decision := {"allow": allow}
```

这允许任何匹配模式 `vX.Y.Z` 的 BuildKit 标签，其中 X、Y 和 Z 是数字。该正则确保你使用的是发布版本，而不是像 `v0.26.0-rc1` 这样的预发布标签。

匹配主版本：

```rego
# 仅允许 v0.x 发布版本
allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  regex.match(`^v0\.[0-9]+\.[0-9]+$`, input.git.tagName)
}
```

## 检查提交元数据

`commit` 对象提供有关提交的详细信息：

```rego
package docker

default allow := false

allow if input.local

# 检查提交作者
allow if {
  input.git.remote == "https://github.com/user/repo.git"
  input.git.commit.author.email == "trusted@example.com"
}

decision := {"allow": allow}
```

`commit` 对象包括：

- `author.name`：作者姓名
- `author.email`：作者邮箱
- `author.when`：提交创作时间
- `committer.name`：提交者姓名
- `committer.email`：提交者邮箱
- `committer.when`：提交时间
- `message`：提交信息

验证提交信息：

```rego
allow if {
  input.git.commit
  contains(input.git.commit.message, "Signed-off-by:")
}
```

固定到特定提交 SHA：

```rego
allow if {
  input.git.commitChecksum == "abc123def456..."
}
```

## 要求已签名的提交

GPG 签名的提交可证明真实性。检查提交签名：

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  input.git.commit.pgpSignature != null
}

decision := {"allow": allow}
```

对于未签名的提交，`pgpSignature` 字段为 `null`。对于已签名的提交，它包含签名详情。

SSH 签名的工作方式类似：

```rego
allow if {
  input.git.commit.sshSignature != null
}
```

## 要求已签名的标签

带注释的标签可以被签名，从而提供对发布的密码学保证：

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  input.git.tag.pgpSignature != null
}

decision := {"allow": allow}
```

`tag` 对象仅对带注释的标签可用。它包括：

- `tagger.name`：谁创建了该标签
- `tagger.email`：打标签者的邮箱
- `tagger.when`：标签创建时间
- `message`：标签信息
- `pgpSignature`：GPG 签名（如果已签名）
- `sshSignature`：SSH 签名（如果已签名）

轻量级标签没有 `tag` 对象，因此此策略实际上要求带注释的、已签名的标签。

## 使用公钥验证签名

使用 `verify_git_signature()` 函数针对受信任的公钥对 Git 签名进行密码学验证：

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  input.git.tagName != ""
  verify_git_signature(input.git.tag, "keys.asc")
}

decision := {"allow": allow}
```

这会验证 Git 标签是否由 `keys.asc` 公钥文件中的密钥签名。要设置它：

1. 导出维护者公钥：
   ```console
   $ curl https://github.com/user.gpg > keys.asc
   ```
2. 将 `keys.asc` 放在你的策略文件旁边

该函数验证提交或标签上的 PGP 签名。有关更多详细信息，请参阅 [内置函数](./built-ins.md)。

## 应用条件规则

对不同上下文使用不同的规则。在开发期间允许未签名的引用，但对生产要求签名：

```rego
package docker

default allow := false

allow if input.local

is_buildkit if {
    input.git.remote == "https://github.com/moby/buildkit.git"
}

is_version_tag if {
    is_buildkit
    regex.match(`^v[0-9]+\.[0-9]+\.[0-9]+$`, input.git.tagName)
}

# 版本标签必须已签名
allow if {
    is_version_tag
    input.git.tagName != ""
    verify_git_signature(input.git.tag, "keys.asc")
}

# 在开发中允许未签名的引用
allow if {
    is_buildkit
    not is_version_tag
    input.env.target != "release"
}

decision := {"allow": allow}
```

此策略：

- 定义辅助规则以提高可读性
- 要求来自维护者的已签名版本标签
- 允许未签名的引用（分支、提交），除非构建 release 目标
- 使用 `input.env.target` 检测构建目标

构建一个没有签名开发目标：

```console
$ docker buildx build --target=dev .
```

构建 release 目标，签名将被强制执行：

```console
$ docker buildx build --target=release .
```

## 下一步

你现在理解了如何在构建策略中验证 Git 仓库。要继续学习：

- 浏览 [示例策略](./examples.md) 获取完整的策略模式
- 阅读 [内置函数](./built-ins.md) 了解 Git 签名验证函数
- 查看 [输入参考](./inputs.md) 了解所有可用的 Git 字段

