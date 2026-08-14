---
title: 构建密钥
linkTitle: 密钥
weight: 30
description: 安全管理凭据及其他密钥
keywords: build, secrets, credentials, passwords, tokens, ssh, git, auth, http
tags: [Secrets]
---

构建密钥（build secret）是指构建过程中消费的任意敏感信息，例如密码或 API
令牌。

构建参数（build arguments）和环境变量不适合用来向构建传递密钥，因为它们会
持久化到最终镜像中。相反，你应该使用 secret 挂载或 SSH 挂载，它们能安全地将
密钥暴露给构建过程。

## 构建密钥的类型（Types of build secrets）

- [Secret 挂载](#secret-mounts) 是一种通用挂载，用于向构建传递密钥。Secret 挂载
  从构建客户端获取一个密钥，并在构建指令执行期间，临时将其提供给构建容器内部。
  例如，当你的构建需要与一个私有制品服务器或 API 通信时，这会很有用。
- [SSH 挂载](#ssh-mounts) 是一种特殊用途挂载，用于将 SSH 套接字或密钥提供给
  构建内部使用。当你需要在构建中获取私有 Git 仓库时，通常会用到它们。
- [远程上下文的 Git 认证](#git-authentication-for-remote-contexts)
  是一组预定义的密钥，用于当你使用一个同样是私有仓库的远程 Git 上下文进行构建时。
  这些密钥属于「起飞前（pre-flight）」密钥：它们不会被构建指令消费，而是用于
  为构建器提供必要的凭据以获取上下文。

## 使用构建密钥（Using build secrets）

对于 secret 挂载和 SSH 挂载，使用构建密钥是一个两步过程。首先，你需要将密钥
传入 `docker build` 命令；然后，你需要在 Dockerfile 中消费该密钥。

要将密钥传递给构建，请使用 [`docker build --secret`
flag](/reference/cli/docker/buildx/build/#secret)，或
[Bake](../bake/reference.md#targetsecret) 的等效选项。

{{< tabs >}}
{{< tab name="CLI" >}}

```console
$ docker build --secret id=aws,src=$HOME/.aws/credentials .
```

{{< /tab >}}
{{< tab name="Bake" >}}

```hcl
variable "HOME" {
  default = null
}

target "default" {
  secret = [
    "id=aws,src=${HOME}/.aws/credentials"
  ]
}
```

{{< /tab >}}
{{< /tabs >}}

要在构建中消费密钥并使其对 `RUN` 指令可访问，请在 Dockerfile 中使用
[`--mount=type=secret`](/reference/dockerfile.md#run---mounttypesecret) 标志。

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

## Secret 挂载（Secret mounts）

Secret 挂载以文件或环境变量的形式将密钥暴露给构建容器。你可以使用 secret 挂载
向构建传递敏感信息，例如 API 令牌、密码或 SSH 密钥。

### 来源（Sources）

密钥的来源可以是
[文件](/reference/cli/docker/buildx/build/#file) 或
[环境变量](/reference/cli/docker/buildx/build/#typeenv)。
当你使用 CLI 或 Bake 时，类型可被自动检测。你也可以显式指定 `type=file` 或
`type=env`。

以下示例将环境变量 `KUBECONFIG` 挂载为 secret ID `kube`，作为构建容器内的一个
文件，路径为 `/run/secrets/kube`。

```console
$ docker build --secret id=kube,env=KUBECONFIG .
```

当使用来自环境变量的密钥时，可以省略 `env` 参数，从而将密钥绑定到与变量同名的
文件。在以下示例中，`API_TOKEN` 变量的值被挂载到构建容器的
`/run/secrets/API_TOKEN`。

```console
$ docker build --secret id=API_TOKEN .
```

### 目标（Target）

在 Dockerfile 中消费密钥时，默认情况下密钥会被挂载为一个文件。在构建容器内，
密钥的默认文件路径是 `/run/secrets/<id>`。你可以使用 Dockerfile 中
`RUN --mount` 标志的 `target` 和 `env` 选项来自定义密钥在构建容器中的挂载方式。

以下示例获取 secret ID `aws`，并将其挂载为构建容器内 `/run/secrets/aws` 处的一个文件。

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

要将密钥挂载为具有不同名称的文件，请在 `--mount` 标志中使用 `target` 选项。

```dockerfile
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws s3 cp ...
```

要将密钥挂载为环境变量而非文件，请在 `--mount` 标志中使用 `env` 选项。

```dockerfile
RUN --mount=type=secret,id=aws-key-id,env=AWS_ACCESS_KEY_ID \
    --mount=type=secret,id=aws-secret-key,env=AWS_SECRET_ACCESS_KEY \
    --mount=type=secret,id=aws-session-token,env=AWS_SESSION_TOKEN \
    aws s3 cp ...
```

可以同时使用 `target` 和 `env` 选项，将密钥既挂载为文件又挂载为环境变量。

## SSH 挂载（SSH mounts）

如果你要在构建中使用的凭据是一个 SSH agent 套接字或密钥，可以使用 SSH 挂载
而非 secret 挂载。克隆私有 Git 仓库是 SSH 挂载的常见用例。

以下示例使用 [Dockerfile
SSH 挂载](/reference/dockerfile.md#run---mounttypessh) 克隆一个私有 GitHub 仓库。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ADD git@github.com:me/myprivaterepo.git /src/
```

要向构建传递 SSH 套接字，请使用 [`docker build --ssh`
flag](/reference/cli/docker/buildx/build/#ssh)，或
[Bake](../bake/reference.md#targetssh) 的等效选项。

```console
$ docker buildx build --ssh default .
```

## 远程上下文的 Git 认证（Git authentication for remote contexts）

BuildKit 支持两个预定义的构建密钥：`GIT_AUTH_TOKEN` 和 `GIT_AUTH_HEADER`。当你
使用远程私有 Git 仓库进行构建时，用它们来指定 HTTP 认证参数，包括：

- 使用私有 Git 仓库作为构建上下文进行构建
- 在构建中使用 `ADD` 获取私有 Git 仓库

例如，假设你有一个位于 `https://github.com/example/todo-app.git` 的私有 GitHub
仓库，并希望以该仓库作为构建上下文来运行构建。未经认证的 `docker build` 命令会
失败，因为构建器未被授权拉取该仓库：

```console
$ docker build https://github.com/example/todo-app.git
[+] Building 0.4s (1/1) FINISHED
 => ERROR [internal] load git source https://github.com/example/todo-app.git
------
 > [internal] load git source https://github.com/example/todo-app.git:
0.313 fatal: could not read Username for 'https://github.com': terminal prompts disabled
------
```

要让构建器向 GitHub 进行认证，请将 `GIT_AUTH_TOKEN` 环境变量设置为一个有效的
GitHub 访问令牌，并将其作为密钥传递给构建：

```console
$ GIT_AUTH_TOKEN=$(gh auth token) docker build \
  --secret id=GIT_AUTH_TOKEN \
  https://github.com/example/todo-app.git
```

`GIT_AUTH_TOKEN` 也可配合 `ADD` 使用，在你的构建中获取私有 Git 仓库：

```dockerfile
FROM alpine
ADD https://github.com/example/todo-app.git /src
```

### HTTP 认证方案（HTTP authentication scheme）

BuildKit 支持两种 Git 认证密钥：

- **`GIT_AUTH_TOKEN`**：使用 Basic 认证，固定用户名为 `x-access-token`（GitHub 风格的默认值）
- **`GIT_AUTH_HEADER`**：使用你提供的原始授权头（authorization header）值（适用于任何 Git 提供商）

#### 使用 GIT_AUTH_TOKEN（例如 GitHub）

当你使用 `GIT_AUTH_TOKEN` 时，BuildKit 使用 `x-access-token` 作为用户构造一个
Basic 认证头：

```http
Authorization: Basic <base64("x-access-token:<GIT_AUTH_TOKEN>")>
```

此方法适用于接受 `x-access-token` Basic 认证模式的提供商，例如 GitHub。示例用法：

```console
$ export GIT_AUTH_TOKEN=$(gh auth token)
$ docker build \
  --secret id=GIT_AUTH_TOKEN \
  https://github.com/example/todo-app.git
```

#### 使用 GIT_AUTH_HEADER（自定义授权头）

当你使用 `GIT_AUTH_HEADER` 时，BuildKit 将你提供的确切值作为 `Authorization` 头：

```http
Authorization: <GIT_AUTH_HEADER>
```

配合 GitLab CI/CD 令牌的示例用法：

```console
$ export GIT_AUTH_HEADER="Basic $(echo -n "gitlab-ci-token:${CI_JOB_TOKEN}" | base64)"
$ docker build \
  --secret id=GIT_AUTH_HEADER \
  https://gitlab.com/example/todo-app.git
```

### 多个主机（Multiple hosts）

你可以基于每个主机设置 `GIT_AUTH_TOKEN` 和 `GIT_AUTH_HEADER` 密钥，从而针对不同的
主机名使用不同的认证参数。要指定主机名，请将主机名作为后缀附加到密钥 ID：

```console
$ export GITHUB_TOKEN=$(gh auth token)
$ export GITLAB_AUTH_HEADER="Basic $(echo -n "gitlab-ci-token:${CI_JOB_TOKEN}" | base64)"
$ docker build \
  --secret id=GIT_AUTH_TOKEN.github.com,env=GITHUB_TOKEN \
  --secret id=GIT_AUTH_HEADER.gitlab.com,env=GITLAB_AUTH_HEADER \
  https://github.com/example/todo-app.git
```

## `COPY` 和 `ADD` 的 HTTP 认证（HTTP authentication for `COPY` and `ADD`）

要在 `COPY` 或 `ADD` 命令中使用密钥，你可以创建 `HTTP_AUTH_TOKEN_<host>` 或
`HTTP_AUTH_HEADER_<host>` 密钥，用于访问指定主机时。例如 `HTTP_AUTH_TOKEN_127.0.0.1=token`
会让对 `127.0.0.1` 的请求添加一个头 `Authorization: Bearer token`。

这些变量遵循与 [Git HTTP 认证方案](#http-authentication-scheme) 处理相同的约定。
