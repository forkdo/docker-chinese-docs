# 策略模板与示例


本页提供完整的、可运行的策略示例，你可以复制并改编。这些示例分为两部分：用于快速采用的入门策略，以及用于全面安全性的生产模板。

如果你不熟悉策略，请从教程开始：[简介](./intro.md)、[镜像验证](./validate-images.md) 和 [Git 验证](./validate-git.md)。这些页面讲授了各个技术。本页展示组合了这些技术的完整策略。

## 如何使用这些示例

1. 将策略代码复制到你的 Dockerfile 旁边的 `Dockerfile.rego` 文件中
2. 用你的特定值自定义任何 todo 注释
3. 通过运行 `docker build .` 并验证策略按预期工作来进行测试
4. 根据你的团队需求进行完善

### 与 bake 一起使用

这些策略同时适用于 `docker buildx build` 和 `docker buildx bake`。对于 bake，将策略放在你的 Dockerfile 旁边，它会自动加载。要使用额外的策略：

```hcl
target "default" {
  dockerfile = "Dockerfile"
  policy = ["extra.rego"]
}
```

有关完整的 bake 集成详细信息，请参阅 [用法指南](./usage.md)。

## 入门

这些策略只需极少或无需自定义即可立即使用。使用它们来快速采用策略并向你的团队展示价值。

### 对开发友好的基线

一个宽松的策略，允许典型的开发工作流，同时阻止明显的安全问题。

```rego
package docker

default allow := false

allow if input.local
allow if input.git

# 允许常见的公共镜像仓库
allow if {
  input.image.host == "docker.io"  # Docker Hub
}

allow if {
  input.image.host == "ghcr.io"  # GitHub Container Registry
}

allow if {
  input.image.host == "dhi.io"  # Docker Hardened Images
}

# 要求所有下载使用 HTTPS
allow if {
  input.http.schema == "https"
}

decision := {"allow": allow}
```

此策略允许本地和 Git 上下文、来自 Docker Hub、GitHub Container Registry 和 [Docker Hardened Images](/dhi/) 的镜像，以及通过 HTTPS 进行的 `ADD` 下载。它会阻止 HTTP 下载和非标准镜像仓库。

何时使用：对于刚接触策略的团队作为起点。在不干扰开发工作流的情况下提供基本安全性。

### 镜像仓库允许列表

控制你的构建可以从哪些镜像仓库拉取镜像。

```rego
package docker

default allow := false

allow if input.local

# TODO: 添加你的内部镜像仓库主机名
allowed_registries := ["docker.io", "ghcr.io", "dhi.io", "registry.company.com"]

allow if {
  input.image.host in allowed_registries
}

# 允许从 Docker Hub 镜像的 DHI 镜像（DHI Enterprise 用户）
# TODO: 替换为你的组织命名空间
allow if {
  input.image.host == "docker.io"
  startswith(input.image.repo, "myorg/dhi-")
}

deny_msg contains msg if {
  not allow
  input.image
  msg := sprintf("registry %s is not in the allowlist", [input.image.host])
}

decision := {"allow": allow, "deny_msg": deny_msg}
```

此策略将镜像拉取限制为已批准的镜像仓库。根据你的内部镜像仓库自定义并将其添加到列表中。如果你拥有 DHI Enterprise 订阅并将 Docker Hardened Images 镜像到了 Docker Hub，请添加一条规则以允许来自你组织命名空间的镜像。

何时使用：执行关于已批准镜像来源的公司策略。防止开发者使用任意公共镜像仓库。

### 将基础镜像固定到摘要

要求使用摘要引用以实现可复现的构建。

```rego
package docker

default allow := false

allow if input.local

# 要求所有镜像使用摘要引用
allow if {
  input.image.isCanonical
}

deny_msg contains msg if {
  not allow
  input.image
  msg := sprintf("image %s must use digest reference (e.g., @sha256:...)", [input.image.ref])
}

decision := {"allow": allow, "deny_msg": deny_msg}
```

此策略要求镜像使用像 `alpine@sha256:abc123...` 这样的摘要引用，而不是像 `alpine:3.19` 这样的标签。摘要是不可变的——相同的摘要始终解析为相同的镜像内容。

何时使用：确保构建可复现性。防止在上游标签更新时构建中断。在某些环境中合规要求必须如此。

### 控制外部依赖

固定构建期间下载的依赖项的特定版本。

```rego
package docker

default allow := false

allow if input.local

# 允许任何镜像（根据需要添加限制）
allow if input.image

# TODO: 添加你允许的 Git 仓库和标签
allowed_repos := {
  "https://github.com/moby/buildkit.git": ["v0.26.1", "v0.27.0"],
}
# 仅允许来自 allowed_repos 的 Git 输入
allow if {
  some repo, versions in allowed_repos
  input.git.remote == repo
  input.git.tagName in versions
}

# TODO: 添加你允许的下载
allow if {
  input.http.url == "https://example.com/app-v1.0.tar.gz"
}

decision := {"allow": allow}
```

此策略为外部依赖创建允许列表。添加带有已批准版本标签和 URL 的 Git 仓库。

何时使用：控制可以在构建中使用的外部依赖。防止构建拉取任意版本或未经验证的下载。

## 生产模板

这些模板展示了全面的安全模式。它们需要自定义，但展示了生产环境的最佳实践。

### 镜像证明与来源

要求镜像具有来自受信任构建器的来源证明。

```rego
package docker

default allow := false

allow if input.local

# TODO: 添加你的仓库名称
allowed_repos := ["myorg/backend", "myorg/frontend", "myorg/worker"]

# 生产镜像需要完整的证明
allow if {
  some repo in allowed_repos
  input.image.repo == repo
  input.image.hasProvenance
  some sig in input.image.signatures
  trusted_github_builder(sig, repo)
}

# 验证来自 main 分支的 GitHub Actions 构建的辅助函数
trusted_github_builder(sig, repo) if {
  sig.signer.certificateIssuer == "CN=sigstore-intermediate,O=sigstore.dev"
  sig.signer.issuer == "https://token.actions.githubusercontent.com"
  startswith(sig.signer.buildSignerURI, sprintf("https://github.com/myorg/%s/.github/workflows/", [repo]))
  sig.signer.sourceRepositoryRef == "refs/heads/main"
  sig.signer.runnerEnvironment == "github-hosted"
}

# 允许带有内置证明的 Docker Hardened Images
allow if {
  input.image.host == "dhi.io"
  input.image.isCanonical
  input.image.hasProvenance
}

# 允许带有摘要的官方基础镜像
allow if {
  input.image.repo == "alpine"
  input.image.host == "docker.io"
  input.image.isCanonical
}

decision := {"allow": allow}
```

此模板验证你的应用镜像具有来源证明，并且是由你的 main 分支上的 GitHub Actions 构建的。当使用摘要时，Docker Hardened Images 被允许，因为它们默认包含全面的证明。其他基础镜像必须使用摘要。

自定义：

- 用你的镜像名称替换 `allowed_repos`
- 在 `trusted_github_builder()` 中更新组织名称
- 为你使用的其他基础镜像添加规则

何时使用：为生产部署执行供应链安全。确保镜像由具有可审计来源的受信任 CI/CD 管道构建。

### 已签名的 Git 发布版本

对来自受信任维护者的 Git 依赖强制执行已签名的标签。

```rego
package docker

default allow := false

allow if input.local

allow if input.image

# TODO: 用你的仓库 URL 替换
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
    verify_git_signature(input.git.tag, "maintainers.asc")
}

# 允许开发中未签名的引用
allow if {
    is_buildkit
    not is_version_tag
}

decision := {"allow": allow}
```

此模板要求生产发布标签由受信任的维护者签名。开发分支和提交可以未签名。

设置：

1. 将维护者 PGP 公钥导出到 `maintainers.asc`：
   ```console
   $ gpg --export --armor user1@example.com user2@example.com > maintainers.asc
   ```
2. 将 `maintainers.asc` 放在与你的策略文件相同的目录中

自定义：

- 在 `is_buildkit` 中替换仓库 URL
- 更新 PGP 密钥环文件中的维护者
- 根据需要调整版本标签正则模式

何时使用：验证生产依赖来自已签名的发布版本。防止被入侵的发布版本或未经授权的更新。

### 多镜像仓库策略

对内部和外部镜像仓库应用不同的验证规则。

```rego
package docker

default allow := false

allow if input.local

# TODO: 用你的内部镜像仓库主机名替换
internal_registry := "registry.company.com"

# 内部镜像仓库：基本验证
allow if {
  input.image.host == internal_registry
}

# 外部镜像仓库：严格验证
allow if {
  input.image.host != internal_registry
  input.image.host != ""
  input.image.isCanonical
  input.image.hasProvenance
}

# Docker Hub：允许列表特定镜像
allow if {
  input.image.host == "docker.io"
  # TODO: 添加你已批准的基础镜像
  input.image.repo in ["alpine", "golang", "node"]
  input.image.isCanonical
}

# Docker Hardened Images：默认受信任，带有内置证明
allow if {
  input.image.host == "dhi.io"
  input.image.isCanonical
}

decision := {"allow": allow}
```

此模板在内部和外部镜像源之间定义了一个信任边界。内部镜像需要最少的验证，而外部镜像需要摘要和来源证明。来自 `dhi.io` 的 Docker Hardened Images 被视为受信任的，因为它们包含全面的证明和安全保证。

自定义：

- 设置你的内部镜像仓库主机名
- 添加你已批准的 Docker Hub 基础镜像
- 根据你的安全策略调整验证要求

何时使用：拥有内部镜像仓库、需要对内部和外部源采用不同规则的组织。在安全需求与实际工作流需求之间取得平衡。

### 多环境策略

根据构建目标或阶段应用不同的规则。例如：

```rego
package docker

default allow := false

allow if input.local

# TODO: 定义你的环境检测逻辑
is_production if {
  input.env.target == "production"
}

is_development if {
  input.env.target == "development"
}

# 生产：严格规则——仅允许带有来源的摘要镜像
allow if {
  is_production
  input.image.isCanonical
  input.image.hasProvenance
}

# 开发：宽松规则——任何镜像
allow if {
  is_development
  input.image
}

# 预发布环境继承生产规则（默认目标检测）
allow if {
  not is_production
  not is_development
  input.image.isCanonical
}

decision := {"allow": allow}
```

此模板使用构建目标来应用不同的验证级别。生产需要证明和摘要，开发是宽松的，预发布使用适度规则。

自定义：

- 更新环境检测逻辑（目标名称、构建参数等）
- 调整每个环境的验证要求
- 根据需要添加更多环境

何时使用：为不同部署阶段拥有独立构建配置的团队。在开发中允许灵活性的同时，对生产强制执行严格规则。

### 完整的依赖固定

将所有外部依赖跨所有输入类型固定到特定版本。

```rego
package docker

default allow := false

allow if input.local

# TODO: 添加带有确切摘要的已固定镜像
# Docker Hub 镜像使用 docker.io 作为主机
allowed_dockerhub := {
  "alpine": "sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412",
  "golang": "sha256:abc123...",
}

allow if {
  input.image.host == "docker.io"
  some repo, digest in allowed_dockerhub
  input.image.repo == repo
  input.image.checksum == digest
}

# TODO: 添加你已固定的 DHI 镜像
allowed_dhi := {
  "python": "sha256:def456...",
  "node": "sha256:ghi789...",
}

allow if {
  input.image.host == "dhi.io"
  some repo, digest in allowed_dhi
  input.image.repo == repo
  input.image.checksum == digest
}

# TODO: 添加你已固定的 Git 依赖
allowed_git := {
  "https://github.com/moby/buildkit.git": {
    "tag": "v0.26.1",
    "commit": "abc123...",
  },
}

allow if {
  some url, version in allowed_git
  input.git.remote == url
  input.git.tagName == version.tag
  input.git.commitChecksum == version.commit
}

# TODO: 添加你已固定的 HTTP 下载
allowed_downloads := {
  "https://releases.example.com/app-v1.0.tar.gz": "sha256:def456...",
}

allow if {
  some url, checksum in allowed_downloads
  input.http.url == url
  input.http.checksum == checksum
}

decision := {"allow": allow}
```

此模板通过密码学验证将每个外部依赖固定到确切版本。镜像使用摘要，Git 仓库使用提交 SHA，下载使用校验和。

自定义：

- 添加所有带有确切版本/校验和的依赖
- 更新依赖时维护此文件
- 考虑通过 CI/CD 自动化更新

何时使用：最大限度的可复现性和安全性。确保构建始终使用所有依赖的确切版本。高安全性或受监管环境所需。

### 手动签名验证

通过检查签名元数据字段来验证镜像签名。

```rego
package docker

default allow := false

allow if input.local

# 要求有效的 GitHub Actions 签名
allow if {
    input.image
    input.image.hasProvenance
    some sig in input.image.signatures
    valid_github_signature(sig)
}

# 验证 GitHub Actions 签名的辅助函数
valid_github_signature(sig) if {
    # Sigstore 无密钥签名
    sig.signer.certificateIssuer == "CN=sigstore-intermediate,O=sigstore.dev"
    sig.signer.issuer == "https://token.actions.githubusercontent.com"

    # TODO: 用你的组织替换
    startswith(sig.signer.buildSignerURI, "https://github.com/myorg/.github/workflows/")
    startswith(sig.signer.sourceRepositoryURI, "https://github.com/myorg/")

    # 要求时间戳
    count(sig.timestamps) > 0
}

decision := {"allow": allow}
```

此策略验证镜像是否由使用 Sigstore 无密钥签名的 GitHub Actions 构建。

自定义：

- 用你的 GitHub 组织替换 `myorg`
- 调整工作流路径限制
- 根据需要添加额外的签名字段检查

何时使用：强制执行镜像由具有可验证签名的 CI/CD 构建，而不是由开发者手动推送。

## 下一步

- 为你的策略编写单元测试：[测试构建策略](./testing.md)
- 查看 [内置函数](./built-ins.md) 了解签名验证和证明检查
- 查看 [输入参考](./inputs.md) 了解你可以验证的所有可用字段
- 阅读教程以获取详细解释：
  [简介](./intro.md)、[镜像验证](./validate-images.md)、[Git 验证](./validate-git.md)

