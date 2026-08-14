# 构建上下文


`docker build` 和 `docker buildx build` 命令从
[Dockerfile](/reference/dockerfile.md) 和上下文中构建 Docker 镜像。

## 什么是构建上下文？（What is a build context?）

构建上下文是你的构建可以访问的文件集合。
你传递给构建命令的位置参数指定了你要用于构建的上下文：

```console
$ docker build [OPTIONS] PATH | URL | -
                         ^^^^^^^^^^^^^^
```

你可以将以下任意输入作为构建的上下文：

- 本地目录的相对或绝对路径
- 远程 Git 仓库、tarball 或纯文本文件的 URL
- 通过标准输入管道传入 `docker build` 命令的纯文本文件或 tarball

### 文件系统上下文（Filesystem contexts）

当你的构建上下文是本地目录、远程 Git 仓库或 tar 文件时，它就成为 builder 在构建期间可以访问的文件集合。诸如 `COPY` 和 `ADD` 之类的构建指令可以引用上下文中的任何文件和目录。

文件系统构建上下文是递归处理的：

- 当你指定本地目录或 tarball 时，所有子目录都会包含在内
- 当你指定远程 Git 仓库时，该仓库及其所有子模块都会包含在内

有关你可以在构建中使用的不同类型的文件系统上下文的更多信息，请参阅：

- [Local files](#local-context)
- [Git repositories](#git-repositories)
- [Remote tarballs](#remote-tarballs)

### 文本文件上下文（Text file contexts）

当你的构建上下文是纯文本文件时，builder 会将该文件解释为 Dockerfile。采用这种方式时，构建不使用文件系统上下文。

有关更多信息，请参阅 [empty build context](#empty-context)。

## 本地上下文（Local context）

要使用本地构建上下文，你可以为 `docker build` 命令指定相对或绝对的文件路径。以下示例展示了一个使用当前目录（`.`）作为构建上下文的构建命令：

```console
$ docker build .
...
#16 [internal] load build context
#16 sha256:23ca2f94460dcbaf5b3c3edbaaa933281a4e0ea3d92fe295193e4df44dc68f85
#16 transferring context: 13.16MB 2.2s done
...
```

这使得当前工作目录中的文件和目录可供 builder 使用。builder 会在需要时从构建上下文加载它所需的文件。

你也可以使用本地 tarball 作为构建上下文，方法是将 tarball 内容管道传入 `docker build` 命令。参见 [Tarballs](#local-tarballs)。

### 本地目录（Local directories）

考虑以下目录结构：

```text
.
├── index.ts
├── src/
├── Dockerfile
├── package.json
└── package-lock.json
```

如果你将此目录作为上下文传入，Dockerfile 指令可以引用并将这些文件包含在构建中。

```dockerfile
# syntax=docker/dockerfile:1
FROM node:latest
WORKDIR /src
COPY package.json package-lock.json .
RUN npm ci
COPY index.ts src .
```

```console
$ docker build .
```

### 从 stdin 提供 Dockerfile 的本地上下文（Local context with Dockerfile from stdin）

使用以下语法，可以在使用本地文件系统上的文件的同时，使用来自 stdin 的 Dockerfile 构建镜像。

```console
$ docker build -f- <PATH>
```

该语法使用 -f（或 --file）选项指定要使用的 Dockerfile，并使用连字符（-）作为文件名来指示 Docker 从 stdin 读取 Dockerfile。

以下示例将当前目录（.）用作构建上下文，并通过 heredoc（here-document）传入 Dockerfile 来构建镜像。

```bash
# create a directory to work in
mkdir example
cd example

# create an example file
touch somefile.txt

# build an image using the current directory as context
# and a Dockerfile passed through stdin
docker build -t myimage:latest -f- . <<EOF
FROM busybox
COPY somefile.txt ./
RUN cat /somefile.txt
EOF
```

### 本地 tarball（Local tarballs）

当你将 tarball 管道传入构建命令时，构建会使用 tarball 的内容作为文件系统上下文。

例如，给定以下项目目录：

```text
.
├── Dockerfile
├── Makefile
├── README.md
├── main.c
├── scripts
├── src
└── test.Dockerfile
```

你可以创建该目录的 tarball 并将其管道传入构建中以用作上下文：

```console
$ tar czf foo.tar.gz *
$ docker build - < foo.tar.gz
```

构建会从 tarball 上下文中解析 Dockerfile。你可以使用 `--file` 标志指定 Dockerfile 相对于 tarball 根目录的名称和位置。以下命令使用 tarball 中的 `test.Dockerfile` 进行构建：

```console
$ docker build --file test.Dockerfile - < foo.tar.gz
```

## 远程上下文（Remote context）

你可以指定远程 Git 仓库、tarball 或纯文本文件的地址作为构建上下文。

- 对于 Git 仓库，builder 会自动克隆该仓库。参见 [Git repositories](#git-repositories)。
- 对于 tarball，builder 会下载并解压 tarball 的内容。参见 [Tarballs](#remote-tarballs)。

如果远程 tarball 是文本文件，builder 不会收到任何[文件系统上下文](#filesystem-contexts)，而是假定远程文件是 Dockerfile。参见 [Empty build context](#empty-context)。

### Git 仓库（Git repositories）

当你将指向 Git 仓库位置的 URL 作为 `docker build` 的参数传入时，builder 会使用该仓库作为构建上下文。

builder 会执行该仓库的浅克隆（shallow clone），只下载 HEAD 提交，而不是整个历史记录。

builder 会递归克隆该仓库及其包含的任何子模块。

```console
$ docker build https://github.com/user/myrepo.git
```

默认情况下，builder 会克隆你所指定仓库默认分支上的最新提交。

#### URL 片段（URL fragments）

你可以向 Git 仓库地址追加 URL 片段，使 builder 克隆该仓库的特定分支、标签和子目录。URL 片段的格式为 `#ref:dir`，其中：

- `ref` 是分支、标签或提交哈希的名称
- `dir` 是仓库内的子目录

例如，以下命令使用 `container` 分支以及该分支中的 `docker` 子目录作为构建上下文：

```console
$ docker build https://github.com/user/myrepo.git#container:docker
```

下表表示了所有有效后缀及其对应的构建上下文：

| Build Syntax Suffix            | Commit Used                   | Build Context Used |
| ------------------------------ | ----------------------------- | ------------------ |
| `myrepo.git`                   | `refs/heads/<default branch>` | `/`                |
| `myrepo.git#mytag`             | `refs/tags/mytag`             | `/`                |
| `myrepo.git#mybranch`          | `refs/heads/mybranch`         | `/`                |
| `myrepo.git#pull/42/head`      | `refs/pull/42/head`           | `/`                |
| `myrepo.git#:myfolder`         | `refs/heads/<default branch>` | `/myfolder`        |
| `myrepo.git#master:myfolder`   | `refs/heads/master`           | `/myfolder`        |
| `myrepo.git#mytag:myfolder`    | `refs/tags/mytag`             | `/myfolder`        |
| `myrepo.git#mybranch:myfolder` | `refs/heads/mybranch`         | `/myfolder`        |

当你在 URL 片段中使用提交哈希作为 `ref` 时，请使用完整的、40 字符的 SHA-1 哈希字符串。不支持短哈希，例如截断为 7 个字符的哈希。

```bash
# ✅ The following works:
docker build github.com/docker/buildx#d4f088e689b41353d74f1a0bfcd6d7c0b213aed2
# ❌ The following doesn't work because the commit hash is truncated:
docker build github.com/docker/buildx#d4f088e
```

#### URL 查询（URL queries）



URL 查询比 [URL 片段](#url-fragments) 结构更清晰，推荐使用：

```console
$ docker buildx build 'https://github.com/user/myrepo.git?branch=container&subdir=docker'
```

| Build syntax suffix                          | Commit used                   | Build context used |
| -------------------------------------------- | ----------------------------- | ------------------ |
| `myrepo.git`                                 | `refs/heads/<default branch>` | `/`                |
| `myrepo.git?tag=mytag`                       | `refs/tags/mytag`             | `/`                |
| `myrepo.git?branch=mybranch`                 | `refs/heads/mybranch`         | `/`                |
| `myrepo.git?ref=pull/42/head`                | `refs/pull/42/head`           | `/`                |
| `myrepo.git?subdir=myfolder`                 | `refs/heads/<default branch>` | `/myfolder`        |
| `myrepo.git?branch=master&subdir=myfolder`   | `refs/heads/master`           | `/myfolder`        |
| `myrepo.git?tag=mytag&subdir=myfolder`       | `refs/tags/mytag`             | `/myfolder`        |
| `myrepo.git?branch=mybranch&subdir=myfolder` | `refs/heads/mybranch`         | `/myfolder`        |

提交哈希可以指定为 `checksum`（别名为 `commit`）查询，配合 `tag`、`branch` 或 `ref` 查询一起使用，以验证该引用是否解析为预期的提交：

```console
$ docker buildx build 'https://github.com/moby/buildkit.git?tag=v0.21.1&checksum=66735c67'
```

如果不匹配，构建会失败：

```console
$ docker buildx build 'https://github.com/user/myrepo.git?tag=v0.1.0&commit=deadbeef'
...
#3 [internal] load git source https://github.com/user/myrepo.git?tag=v0.1.0-rc1&commit=deadbeef
#3 0.484 bb41e835b6c3523c7c45b248cf4b45e7f862bc42       refs/tags/v0.1.0
#3 ERROR: expected checksum to match deadbeef, got bb41e835b6c3523c7c45b248cf4b45e7f862bc42
```

> [!NOTE]
>
> `checksum`（别名为 `commit`）查询支持短提交哈希，但对于 `ref`，只支持完整的提交哈希。

#### 保留 `.git` 目录（Keep `.git` directory）

默认情况下，BuildKit 在使用 Git 上下文时不会保留 `.git` 目录。你可以通过设置
[`BUILDKIT_CONTEXT_KEEP_GIT_DIR` 构建参数](/reference/dockerfile.md#buildkit-built-in-build-args)
将 BuildKit 配置为保留该目录。如果你希望在构建期间检索 Git 信息，这会很有用：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
WORKDIR /src
RUN --mount=target=. \
  make REVISION=$(git rev-parse HEAD) build
```

```console
$ docker build \
  --build-arg BUILDKIT_CONTEXT_KEEP_GIT_DIR=1
  https://github.com/user/myrepo.git#main
```

#### 私有仓库（Private repositories）

当你指定的 Git 上下文同时也是私有仓库时，builder 需要你提供必要的身份验证凭据。你可以使用 SSH 或基于令牌的身份验证。

如果你指定的 Git 上下文是 SSH 或 Git 地址，Buildx 会自动检测并使用 SSH 凭据。默认情况下，它使用 `$SSH_AUTH_SOCK`。
你可以使用 [`--ssh` 标志](/reference/cli/docker/buildx/build/#ssh) 配置要使用的 SSH 凭据。

```console
$ docker buildx build --ssh default git@github.com:user/private.git
```

如果你想改用基于令牌的身份验证，可以使用
[`--secret` 标志](/reference/cli/docker/buildx/build/#secret) 传递令牌。

```console
$ GIT_AUTH_TOKEN=<token> docker buildx build \
  --secret id=GIT_AUTH_TOKEN \
  https://github.com/user/private.git
```

> [!NOTE]
>
> 不要对密钥使用 `--build-arg`。

### 从 stdin 提供 Dockerfile 的远程上下文（Remote context with Dockerfile from stdin）

使用以下语法，可以在使用本地文件系统上的文件的同时，使用来自 stdin 的 Dockerfile 构建镜像。

```console
$ docker build -f- <URL>
```

该语法使用 -f（或 --file）选项指定要使用的 Dockerfile，并使用连字符（-）作为文件名来指示 Docker 从 stdin 读取 Dockerfile。

当你想要从不包含 Dockerfile 的仓库构建镜像时，这可能很有用。或者，如果你想使用自定义 Dockerfile 进行构建，而无需维护该仓库自己的分支。

以下示例通过 stdin 中的 Dockerfile 构建镜像，并添加来自 GitHub 上 [hello-world](https://github.com/docker-library/hello-world) 仓库的 `hello.c` 文件。

```bash
docker build -t myimage:latest -f- https://github.com/docker-library/hello-world.git <<EOF
FROM busybox
COPY hello.c ./
EOF
```

### 远程 tarball（Remote tarballs）

如果你传入远程 tarball 的 URL，URL 本身会被发送给 builder。

```console
$ docker build http://server/context.tar.gz
#1 [internal] load remote build context
#1 DONE 0.2s

#2 copy /context /
#2 DONE 0.1s
...
```

下载操作会在运行 BuildKit 守护进程的主机上执行。请注意，如果你使用的是远程 Docker 上下文或远程 builder，那不一定是发出构建命令的同一台机器。BuildKit 会获取 `context.tar.gz` 并将其用作构建上下文。Tarball 上下文必须是符合标准 `tar` Unix 格式的 tar 归档，并且可以使用 `xz`、`bzip2`、`gzip` 或 `identity`（无压缩）中的任意一种格式进行压缩。

## 空上下文（Empty context）

当你使用文本文件作为构建上下文时，builder 会将该文件解释为 Dockerfile。使用文本文件作为上下文意味着构建没有文件系统上下文。

当你的 Dockerfile 不依赖于任何本地文件时，你可以构建空构建上下文。

### 如何在没有上下文的情况下构建（How to build without a context）

你可以通过标准输入流传递文本文件，或者指向远程文本文件的 URL。

**Unix pipe**



```console
$ docker build - < Dockerfile
```

**PowerShell**



```powershell
Get-Content Dockerfile | docker build -
```

**Heredocs**



```bash
docker build -t myimage:latest - <<EOF
FROM busybox
RUN echo "hello world"
EOF
```

**Remote file**



```console
$ docker build https://raw.githubusercontent.com/dvdksn/clockbox/main/Dockerfile
```



当你在没有文件系统上下文的情况下构建时，诸如 `COPY` 之类的 Dockerfile 指令无法引用本地文件：

```console
$ ls
main.c
$ docker build -<<< $'FROM scratch\nCOPY main.c .'
[+] Building 0.0s (4/4) FINISHED
 => [internal] load build definition from Dockerfile       0.0s
 => => transferring dockerfile: 64B                        0.0s
 => [internal] load .dockerignore                          0.0s
 => => transferring context: 2B                            0.0s
 => [internal] load build context                          0.0s
 => => transferring context: 2B                            0.0s
 => ERROR [1/1] COPY main.c .                              0.0s
------
 > [1/1] COPY main.c .:
------
Dockerfile:2
--------------------
   1 |     FROM scratch
   2 | >>> COPY main.c .
   3 |
--------------------
ERROR: failed to solve: failed to compute cache key: failed to calculate checksum of ref 7ab2bb61-0c28-432e-abf5-a4c3440bc6b6::4lgfpdf54n5uqxnv9v6ymg7ih: "/main.c": not found
```

## .dockerignore 文件（.dockerignore files）

你可以使用 `.dockerignore` 文件将文件或目录从构建上下文中排除。

```text
# .dockerignore
node_modules
bar
```

这有助于避免将不必要的文件和目录发送给 builder，从而提升构建速度，尤其是在使用远程 builder 时。

### 文件名与位置（Filename and location）

当你运行构建命令时，构建客户端会在上下文的根目录中查找名为 `.dockerignore` 的文件。如果该文件存在，则在发送给 builder 之前，与文件中模式匹配的文件和目录会从构建上下文中移除。

如果你使用多个 Dockerfile，可以为每个 Dockerfile 使用不同的忽略文件。你可以通过对忽略文件使用特殊的命名约定来实现。将你的忽略文件放在与 Dockerfile 相同的目录中，并用 Dockerfile 的名称作为忽略文件的前缀，如下例所示。

```text
.
├── index.ts
├── src/
├── docker
│   ├── build.Dockerfile
│   ├── build.Dockerfile.dockerignore
│   ├── lint.Dockerfile
│   ├── lint.Dockerfile.dockerignore
│   ├── test.Dockerfile
│   └── test.Dockerfile.dockerignore
├── package.json
└── package-lock.json
```

如果两者都存在，特定于 Dockerfile 的忽略文件优先于构建上下文根目录下的 `.dockerignore` 文件。

### 语法（Syntax）

`.dockerignore` 文件是一个以换行分隔的模式列表，类似于 Unix shell 的文件 glob。忽略模式中的前导和尾随斜杠会被忽略。以下模式都会排除位于构建上下文根目录下 `foo` 子目录中名为 `bar` 的文件或目录：

- `/foo/bar/`
- `/foo/bar`
- `foo/bar/`
- `foo/bar`

如果 `.dockerignore` 文件中的某一行在第 1 列以 `#` 开头，则该行被视为注释，在 CLI 解释之前会被忽略。

```gitignore
#/this/is/a/comment
```

如果你有兴趣了解 `.dockerignore` 模式匹配的精确细节，请查看 GitHub 上的
[moby/patternmatcher 仓库](https://github.com/moby/patternmatcher/tree/main/ignorefile)，
其中包含源代码。

#### 匹配（Matching）

以下代码片段展示了一个 `.dockerignore` 文件的示例。

```text
# comment
*/temp*
*/*/temp*
temp?
```
<!-- vale off -->

此文件会导致以下构建行为：

| Rule        | Behavior                                                                                                                                                                                                      |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `# comment` | 被忽略。                                                                                                                                                                                                      |
| `*/temp*`   | 排除根目录下任意直接子目录中名称以 `temp` 开头的文件和目录。例如，普通文件 `/somedir/temporary.txt` 会被排除，目录 `/somedir/temp` 也会被排除。                                 |
| `*/*/temp*` | 排除根目录下两级子目录中名称以 `temp` 开头的文件和目录。例如，`/somedir/subdir/temporary.txt` 会被排除。                                                                                                      |
| `temp?`     | 排除根目录中名称为 `temp` 加一个字符扩展名的文件和目录。例如，`/tempa` 和 `/tempb` 会被排除。                                                                                                                  |

<!-- vale on -->

匹配使用 Go 的
[`filepath.Match` 函数](https://golang.org/pkg/path/filepath#Match) 规则进行。
预处理步骤使用 Go 的
[`filepath.Clean` 函数](https://golang.org/pkg/path/filepath/#Clean)
来去除空白并移除 `.` 和 `..`。预处理后为空的行会被忽略。

> [!NOTE]
>
> 由于历史原因，模式 `.` 会被忽略。

除 Go 的 `filepath.Match` 规则外，Docker 还支持特殊的通配符字符串 `**`，它可以匹配任意数量的目录（包括零个）。例如，`**/*.go` 排除构建上下文中任何位置的、以 `.go` 结尾的所有文件。

你可以使用 `.dockerignore` 文件排除 `Dockerfile` 和 `.dockerignore` 文件。这些文件仍会被发送给 builder，因为它们是运行构建所必需的。但你不能使用 `ADD`、`COPY` 或绑定挂载将这些文件复制到镜像中。

#### 否定匹配（Negating matches）

你可以在行前加 `!`（感叹号）来作为排除的例外。以下是一个使用此机制的 `.dockerignore` 文件示例：

```text
*.md
!README.md
```

除了 `README.md` 之外的所有位于上下文目录正下方的 markdown 文件都会被排除在上下文之外。请注意，子目录下的 markdown 文件仍会被包含。

`!` 例外规则的放置位置会影响行为：`.dockerignore` 中最后一条匹配特定文件的行决定了它是被包含还是被排除。考虑以下示例：

```text
*.md
!README*.md
README-secret.md
```

除 `README-secret.md` 外的所有 README 文件都不会包含在上下文中。

现在考虑这个示例：

```text
*.md
README-secret.md
!README*.md
```

所有 README 文件都会被包含。中间那行没有效果，因为 `!README*.md` 匹配了 `README-secret.md` 且排在最后。

## 命名上下文（Named contexts）

除了默认构建上下文（即 `docker build` 命令的位置参数）外，你还可以向构建传递额外的命名上下文。

命名上下文使用 `--build-context` 标志指定，后跟一个名值对。这让你可以在构建期间从多个来源包含文件和目录，同时让它们在逻辑上保持分离。

```console
$ docker build --build-context docs=./docs .
```

在此示例中：

- 命名上下文 `docs` 指向 `./docs` 目录。
- 默认上下文（`.`）指向当前工作目录。

### 在 Dockerfile 中使用命名上下文（Using named contexts in a Dockerfile）

Dockerfile 指令可以将命名上下文引用为好像它们是多阶段构建中的阶段一样。

例如，以下 Dockerfile：

1. 使用 `COPY` 指令将文件从默认上下文复制到当前构建阶段。
2. 绑定挂载命名上下文中的文件，以在构建过程中处理这些文件。

```dockerfile
# syntax=docker/dockerfile:1
FROM buildbase
WORKDIR /app

# Copy all files from the default context into /app/src in the build container
COPY . /app/src
RUN make bin

# Mount the files from the named "docs" context to build the documentation
RUN --mount=from=docs,target=/app/docs \
    make manpages
```

### 命名上下文的用例（Use cases for named contexts）

使用命名上下文可以在构建 Docker 镜像时获得更大的灵活性和有效性。以下是一些使用命名上下文会很有用的场景：

#### 示例：结合本地与远程来源（Example: combine local and remote sources）

你可以为不同类型的来源定义独立的命名上下文。例如，考虑一个项目，其应用源代码在本地，但部署脚本存储在 Git 仓库中：

```console
$ docker build --build-context scripts=https://github.com/user/deployment-scripts.git .
```

在 Dockerfile 中，你可以独立使用这些上下文：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine:latest

# Copy application code from the main context
COPY . /opt/app

# Run deployment scripts using the remote "scripts" context
RUN --mount=from=scripts,target=/scripts /scripts/main.sh
```

#### 示例：使用自定义依赖进行动态构建（Example: dynamic builds with custom dependencies）

在某些场景中，你可能需要从外部来源动态注入配置文件或依赖到构建中。命名上下文可以通过让你挂载不同的配置而无需修改默认构建上下文，从而简化这一过程。

```console
$ docker build --build-context config=./configs/prod .
```

示例 Dockerfile：

```dockerfile
# syntax=docker/dockerfile:1
FROM nginx:alpine

# Use the "config" context for environment-specific configurations
COPY --from=config nginx.conf /etc/nginx/nginx.conf
```

#### 示例：固定或覆盖镜像（Example: pin or override images）

你可以像引用镜像一样在 Dockerfile 中引用命名上下文。这意味着你可以通过使用命名上下文覆盖它，来更改 Dockerfile 中的镜像引用。例如，给定以下 Dockerfile：

```dockerfile
FROM alpine:3.23
```

如果你想在不更改 Dockerfile 的情况下强制镜像引用解析为不同的版本，你可以将具有相同名称的上下文传递给构建。例如：

```console
docker buildx build --build-context alpine:3.23=docker-image://alpine:edge .
```

`docker-image://` 前缀将该上下文标记为镜像引用。该引用可以是本地镜像，也可以是你的注册表中的镜像。

### 与 Bake 一起使用命名上下文（Named contexts with Bake）

[Bake](/manuals/build/bake/_index.md) 是内置于 `docker build` 的工具，让你可以通过配置文件管理构建配置。Bake 完全支持命名上下文。

要在 Bake 文件中定义命名上下文：

```hcl {title=docker-bake.hcl}
target "app" {
  contexts = {
    docs = "./docs"
  }
}
```

这等同于以下 CLI 调用：

```console
$ docker build --build-context docs=./docs .
```

#### 通过命名上下文链接目标（Linking targets with named contexts）

除了让复杂构建更易于管理外，Bake 还提供了相对于 CLI 上 `docker build` 的额外功能。你可以使用命名上下文创建构建流水线，其中一个目标依赖另一个目标并在其基础上构建。例如，考虑一个 Docker 构建设置，其中你有两个 Dockerfile：

- `base.Dockerfile`：用于构建基础镜像
- `app.Dockerfile`：用于构建应用镜像

`app.Dockerfile` 使用由 `base.Dockerfile` 生成的基础镜像作为其基础镜像：

```dockerfile {title=app.Dockerfile}
FROM mybaseimage
```

通常，你必须先构建基础镜像，然后要么将其加载到 Docker Engine 的本地镜像存储，要么推送到注册表。使用 Bake，你可以直接引用其他目标，从而在 `app` 目标与 `base` 目标之间建立依赖关系。

```hcl {title=docker-bake.hcl}
target "base" {
  dockerfile = "base.Dockerfile"
}

target "app" {
  dockerfile = "app.Dockerfile"
  contexts = {
    # the target: prefix indicates that 'base' is a Bake target
    mybaseimage = "target:base"
  }
}
```

通过此配置，`app.Dockerfile` 中对 `mybaseimage` 的引用会使用构建 `base` 目标的结果。必要时，构建 `app` 目标也会触发对 `mybaseimage` 的重新构建：

```console
$ docker buildx bake app
```

### 延伸阅读（Further reading）

有关使用命名上下文的更多信息，请参阅：

- [`--build-context` CLI 参考](/reference/cli/docker/buildx/build/#build-context)
- [将 Bake 与附加上下文配合使用](/manuals/build/bake/contexts.md)

