# 输入参考


当 Buildx 评估策略时，它通过 `input` 对象提供有关构建输入的信息。`input` 的结构取决于你的 Dockerfile 所引用资源的类型。

## 输入类型

构建输入对应于 Dockerfile 指令：

| Dockerfile 指令                         | 输入类型 | 访问模式          |
| --------------------------------------- | -------- | ----------------- |
| `FROM alpine:latest`                    | Image    | `input.image`     |
| `COPY --from=builder /app /app`         | Image    | `input.image`     |
| `ADD https://example.com/file.tar.gz /` | HTTP     | `input.http`      |
| `ADD git@github.com:user/repo.git /src` | Git      | `input.git`       |
| 构建上下文（`.`）                       | Local    | `input.local`     |

每种输入类型都有可供策略评估使用的特定字段。

## HTTP 输入

HTTP 输入表示使用 `ADD` 指令通过 HTTP 或 HTTPS 下载的文件。

### 示例 Dockerfile

```dockerfile
FROM alpine
ADD --checksum=sha256:abc123... https://example.com/app.tar.gz /app.tar.gz
```

### 可用字段

#### `input.http.url`

资源的完整 URL。

```rego
allow if {
    input.http.url == "https://example.com/app.tar.gz"
}
```

#### `input.http.schema`

URL 方案（`http` 或 `https`）。

```rego
# 要求所有下载使用 HTTPS
allow if {
    input.http.schema == "https"
}
```

#### `input.http.host`

来自 URL 的主机名。

```rego
# 允许来自已批准域名的下载
allow if {
    input.http.host == "cdn.example.com"
}
```

#### `input.http.path`

URL 的路径部分。

```rego
allow if {
    startswith(input.http.path, "/releases/")
}
```

#### `input.http.checksum`

使用 `ADD --checksum=...` 指定的校验和（如果存在）。如果未提供校验和，则为空字符串。

```rego
# 要求所有下载都有校验和
allow if {
    input.http.checksum != ""
}
```

#### `input.http.hasAuth`

布尔值，指示请求是否包含认证信息（HTTP 基本认证或 bearer token）。

```rego
# 要求内部服务器进行认证
allow if {
    input.http.host == "internal.company.com"
    input.http.hasAuth
}
```

## 镜像输入

镜像输入表示来自 `FROM` 指令或 `COPY --from` 引用的容器镜像。

### 示例 Dockerfile

```dockerfile
FROM alpine:3.19@sha256:abc123...
COPY --from=builder:latest /app /app
```

### 可用字段

#### `input.image.ref`

如 Dockerfile 中所写的完整镜像引用。

```rego
allow if {
    input.image.ref == "alpine:3.19@sha256:abc123..."
}
```

#### `input.image.host`

镜像仓库主机名。Docker Hub 镜像使用 `"docker.io"`。

```rego
# 仅允许 Docker Hub 镜像
allow if {
    input.image.host == "docker.io"
}

# 仅允许来自 GitHub 容器镜像仓库的镜像
allow if {
    input.image.host == "ghcr.io"
}
```

#### `input.image.repo`

不含镜像仓库主机的仓库名称。

```rego
allow if {
    input.image.repo == "library/alpine"
}
```

#### `input.image.fullRepo`

包含镜像仓库主机的完整仓库路径。

```rego
allow if {
    input.image.fullRepo == "docker.io/library/alpine"
}
```

#### `input.image.tag`

引用中的标签部分。如果使用摘要引用，则为空。

```rego
# 仅允许特定标签
allow if {
    input.image.tag == "3.19"
}
```

#### `input.image.isCanonical`

布尔值，指示引用是否使用摘要（`@sha256:...`）。

```rego
# 要求摘要引用
allow if {
    input.image.isCanonical
}
```

#### `input.image.checksum`

镜像清单的 SHA256 摘要。

```rego
allow if {
    input.image.checksum == "sha256:abc123..."
}
```

#### `input.image.platform`

多平台镜像的目标平台。

```rego
allow if {
    input.image.platform == "linux/amd64"
}
```

#### `input.image.os`

来自镜像配置的操作系统。

```rego
allow if {
    input.image.os == "linux"
}
```

#### `input.image.arch`

来自镜像配置的 CPU 架构。

```rego
allow if {
    input.image.arch == "amd64"
}
```

#### `input.image.hasProvenance`

布尔值，指示镜像是否具有来源证明（provenance attestations）。

```rego
# 要求生产镜像具有来源证明
allow if {
    input.image.hasProvenance
}
```

#### `input.image.labels`

来自镜像配置的镜像标签映射。

```rego
# 检查特定标签
allow if {
    input.image.labels["org.opencontainers.image.vendor"] == "Example Corp"
}
```

#### `input.image.signatures`

证明签名（attestation signatures）数组。数组中的每个签名具有以下字段：

- `kind`：签名种类（例如 `"docker-github-builder"`、`"self-signed"`）
- `type`：签名类型（例如 `"bundle-v0.3"`、`"simplesigning-v1"`）
- `timestamps`：来自透明度日志的受信任时间戳
- `dockerReference`：Docker 镜像引用
- `isDHI`：布尔值，指示这是否为 Docker Hardened Image
- `signer`：Sigstore 证书详细信息

```rego
# 要求至少一个签名
allow if {
    count(input.image.signatures) > 0
}
```

对于 Sigstore 签名，`signer` 对象提供来自签名工作流的详细证书信息：

- `certificateIssuer`：证书颁发者
- `subjectAlternativeName`：来自证书的 subject alternative name
- `buildSignerURI`：构建签名者的 URI
- `buildSignerDigest`：构建签名者的摘要
- `runnerEnvironment`：CI/CD runner 环境
- `sourceRepositoryURI`：源仓库 URL
- `sourceRepositoryDigest`：源仓库摘要
- `sourceRepositoryRef`：源仓库引用（分支/标签）
- `sourceRepositoryIdentifier`：源仓库标识符
- `sourceRepositoryOwnerURI`：仓库所有者 URI
- `buildConfigURI`：构建配置 URI
- `buildTrigger`：触发构建的原因
- `runInvocationURI`：CI/CD 运行调用 URI

```rego
# 要求来自 GitHub Actions 的签名
allow if {
    some sig in input.image.signatures
    sig.signer.runnerEnvironment == "github-hosted"
    startswith(sig.signer.sourceRepositoryURI, "https://github.com/myorg/")
}
```

## Git 输入

Git 输入表示在 `ADD` 指令中引用或用作构建上下文的 Git 仓库。

### 示例 Dockerfile

```dockerfile
ADD git@github.com:moby/buildkit.git#v0.12.0 /src
```

### 可用字段

#### `input.git.schema`

URL 方案（`https`、`http`、`git` 或 `ssh`）。

```rego
# 要求 Git 克隆使用 HTTPS
allow if {
    input.git.schema == "https"
}
```

#### `input.git.host`

Git 主机（例如 `github.com`、`gitlab.com`）。

```rego
allow if {
    input.git.host == "github.com"
}
```

#### `input.git.remote`

完整的 Git URL。

```rego
allow if {
    input.git.remote == "https://github.com/moby/buildkit.git"
}
```

#### `input.git.ref`

Git 引用。

```rego
allow if {
    input.git.ref == "refs/heads/master"
}
```

#### `input.git.tagName`

如果引用是标签，则为标签名称。

```rego
# 仅允许版本标签
allow if {
    regex.match(`^v[0-9]+\.[0-9]+\.[0-9]+$`, input.git.tagName)
}
```

#### `input.git.branch`

如果引用是分支，则为分支名称。

```rego
allow if {
    input.git.branch == "main"
}
```

#### `input.git.subDir`

仓库内的子目录路径（如果指定）。

```rego
# 确保克隆来自根目录
allow if {
    input.git.subDir == ""
}
```

#### `input.git.isCommitRef`

布尔值，指示引用是否为提交 SHA（而不是分支或标签名称）。

```rego
# 要求生产环境使用提交 SHA
allow if {
    input.env.target == "production"
    input.git.isCommitRef
}
```

#### `input.git.checksum`

Git 引用的校验和。对于提交引用和分支，这是提交哈希。对于带注释的标签，这是标签对象哈希。

```rego
allow if {
    input.git.checksum == "abc123..."
}
```

#### `input.git.commitChecksum`

引用所指向的提交哈希。对于带注释的标签，这不同于 `checksum`（即标签对象哈希）。对于提交引用和分支，这与 `checksum` 相同。

```rego
allow if {
    input.git.commitChecksum == "abc123..."
}
```

#### `input.git.isAnnotatedTag`

布尔值，指示引用是否为带注释的标签（而不是轻量级标签）。

```rego
# 要求带注释的标签
allow if {
    input.git.tagName != ""
    input.git.isAnnotatedTag
}
```

#### `input.git.commit`

包含提交元数据的对象：

- `author`：作者姓名、邮箱、时间
- `committer`：提交者姓名、邮箱、时间
- `message`：提交信息
- `pgpSignature`：如果已签名，则为 PGP 签名详情
- `sshSignature`：如果已签名，则为 SSH 签名详情

```rego
# 检查提交作者
allow if {
    input.git.commit.author.email == "maintainer@example.com"
}
```

#### `input.git.tag`

包含带注释标签的标签元数据的对象：

- `tagger`：打标签者姓名、邮箱、时间
- `message`：标签信息
- `pgpSignature`：如果已签名，则为 PGP 签名详情
- `sshSignature`：如果已签名，则为 SSH 签名详情

```rego
# 要求已签名的标签
allow if {
    input.git.tag.pgpSignature != null
}
```

## 本地输入

本地输入表示构建上下文目录。

### 可用字段

#### `input.local.name`

本地上下文的名称或路径。

```rego
allow if {
    input.local.name == "."
}
```

本地输入通常比远程输入限制更少，但你仍然可以编写策略来强制执行上下文要求。

## 环境字段

`input.env` 对象提供由用户在调用构建时设置的构建配置信息，与特定资源类型无关。

### 可用字段

#### `input.env.filename`

正在构建的 Dockerfile 的名称。

```rego
# 对生产 Dockerfile 使用更严格的规则
allow if {
    input.env.filename == "Dockerfile"
    input.image.isCanonical
}

# 对开发环境使用宽松规则
allow if {
    input.env.filename == "Dockerfile.dev"
}
```

#### `input.env.target`

来自多阶段构建的构建目标。

```rego
# 仅对发布构建要求签名
allow if {
    input.env.target == "release"
    input.git.tagName != ""
    verify_git_signature(input.git.tag, "maintainer.asc")
}
```

#### `input.env.args`

使用 `--build-arg` 传递的构建参数。按键访问特定参数。

```rego
# 检查构建参数值
allow if {
    input.env.args.ENVIRONMENT == "production"
    input.image.hasProvenance
}
```

## 下一步

- 请参阅 [内置函数](./built-ins.md) 了解用于检查和验证输入属性的内置辅助函数
- 浏览 [示例策略](./examples.md) 获取常见模式
- 阅读有关 [Rego](https://www.openpolicyagent.org/docs/latest/policy-language/) 的内容以了解进阶策略逻辑

