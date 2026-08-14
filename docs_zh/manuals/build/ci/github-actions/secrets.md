---
title: 在 GitHub Actions 中使用密钥
linkTitle: 构建密钥
description: 在 GitHub Actions 中使用 secret 挂载的示例
keywords: ci, github actions, gha, buildkit, buildx, secret
tags: [Secrets]
---

构建密钥（build secret）是构建过程中使用的一类敏感信息，例如密码或 API 令牌。
Docker Build 支持两种形式的密钥：

- [Secret 挂载](#secret-mounts) 将密钥作为文件添加到构建容器中
  （默认位于 `/run/secrets` 下）。
- [SSH 挂载](#ssh-mounts) 将 SSH agent 套接字或密钥注入构建容器。

本页介绍如何在 GitHub Actions 中使用密钥。
如需了解密钥的整体概念，请参阅 [Build secrets](/manuals/build/building/secrets.md)。

## Secret mounts

下面的示例使用了 GitHub 在工作流中提供的 [`GITHUB_TOKEN` secret](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret)
并将其暴露给构建。

首先，创建一个使用该密钥的 `Dockerfile`：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=github_token,env=GITHUB_TOKEN ...
```

在本例中，密钥名称为 `github_token`。下面的工作流
通过 `secrets` 输入将该密钥暴露出来：

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@{{% param "setup_qemu_action_version" %}}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}

      - name: Build
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          platforms: linux/amd64,linux/arm64
          tags: user/app:latest
          secrets: |
            "github_token=${{ secrets.GITHUB_TOKEN }}"
```

> [!NOTE]
> 密钥以文件形式挂载到构建容器中。
> 默认情况下，它们位于 `/run/secrets/<id>`。
> 你也可以使用 `env` 选项将密钥加载到环境变量中，
> 或者使用 `target` 选项自定义挂载路径。
> 有关 secret 挂载的详细信息，请参阅 [Build secrets](/manuals/build/building/secrets.md)。

### Secret sources

`docker/build-push-action` 中用于 secret 挂载的输入项定义了密钥
值的来源。Dockerfile 中的 `RUN --mount=type=secret` 选项则定义了
构建步骤如何使用该密钥。

| Action 输入                            | 来源                                | 等效的 Buildx 选项                    |
| -------------------------------------- | ----------------------------------- | ------------------------------------- |
| `secrets: MY_SECRET=value`             | 工作流中的内联值                    | `--secret id=MY_SECRET,src=<temp-file>` |
| `secret-envs: MY_SECRET=MY_ENV_VAR`    | runner 上的环境变量                 | `--secret id=MY_SECRET,env=MY_ENV_VAR`  |
| `secret-files: MY_SECRET=./secret.txt` | runner 上的文件                     | `--secret id=MY_SECRET,src=./secret.txt` |

例如，`RUN --mount=type=secret,id=MY_SECRET` 将密钥作为文件
挂载到 `/run/secrets/MY_SECRET`。若要在 `RUN` 指令中将同一个密钥
暴露为环境变量，可在 Dockerfile 中使用 `env` 选项：
`RUN --mount=type=secret,id=MY_SECRET,env=MY_SECRET`。

### Using environment variables as secret sources

`secret-envs` 输入项会从 GitHub Actions runner 上的环境变量读取密钥。
当某个先前的步骤设置了环境变量，或者你想将 runner 的环境变量
映射为构建中不同的密钥 ID 时，可以使用它。

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@{{% param "checkout_action_version" %}}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}

      - name: Build
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        env:
          SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
        with:
          context: .
          secret-envs: |
            sentry_token=SENTRY_AUTH_TOKEN
          tags: user/app:latest
```

在 Dockerfile 中，挂载该密钥并将其暴露为需要它的命令所用的环境变量：

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN --mount=type=secret,id=sentry_token,env=SENTRY_AUTH_TOKEN \
    npm run build
```

### Using secret files

`secret-files` 输入项让你可以将已有文件作为密钥挂载到构建中。
当你需要使用工作流执行期间生成的凭据文件，
或需要挂载格式已符合要求（如 `.npmrc` 或 `.pypirc`）的配置文件时，这会很有用。

`secrets`、`secret-envs` 与 `secret-files` 之间的关键区别：

- `secrets`：从工作流中以字符串形式传入密钥值。
- `secret-envs`：从 runner 上的环境变量读取密钥值。
- `secret-files`：挂载 runner 文件系统中已有的文件。

#### Example: Using .npmrc for private npm packages

如果构建需要从私有 npm 注册表安装包，
你可以创建一个 `.npmrc` 文件并将其作为密钥挂载：

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@{{% param "checkout_action_version" %}}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}

      - name: Create .npmrc file
        run: |
          echo "//registry.npmjs.org/:_authToken=${{ secrets.NPM_TOKEN }}" > .npmrc

      - name: Build
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          context: .
          secret-files: |
            npmrc=./.npmrc
          tags: user/app:latest
```

在 Dockerfile 中，将该密钥文件挂载到预期位置：

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci

COPY . .

RUN npm run build
```

如果 `RUN` 指令使用非 root 用户，则需要在 secret 挂载上设置 `uid`、`gid` 或 `mode`，
以便该用户能够读取挂载的文件：

```dockerfile
RUN --mount=type=secret,id=npmrc,target=/home/node/.npmrc,uid=1000,gid=1000 \
    npm ci
```

#### Example: Using dynamically generated credentials

你可以从多个密钥生成凭据文件并挂载它们：

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@{{% param "checkout_action_version" %}}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}

      - name: Create credentials file
        run: |
          cat <<EOF > aws-credentials
          [default]
          aws_access_key_id = ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws_secret_access_key = ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          EOF

      - name: Build
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          context: .
          secret-files: |
            aws=./aws-credentials
          tags: user/app:latest
```

在 Dockerfile 中：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine

RUN apk add --no-cache aws-cli

RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws s3 cp s3://my-private-bucket/data.tar.gz /tmp/
```

### Multi-line secrets

如果你正在使用 [GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
并且需要处理多行值，则需要将键值对放在引号之间：

```yaml
secrets: |
  "MYSECRET=${{ secrets.GPG_KEY }}"
  GIT_AUTH_TOKEN=abcdefghi,jklmno=0123456789
  "MYSECRET=aaaaaaaa
  bbbbbbb
  ccccccccc"
  FOO=bar
  "EMPTYLINE=aaaa

  bbbb
  ccc"
  "JSON_SECRET={""key1"":""value1"",""key2"":""value2""}"
```

| Key              | Value                               |
| ---------------- | ----------------------------------- |
| `MYSECRET`       | `***********************`           |
| `GIT_AUTH_TOKEN` | `abcdefghi,jklmno=0123456789`       |
| `MYSECRET`       | `aaaaaaaa\nbbbbbbb\nccccccccc`      |
| `FOO`            | `bar`                               |
| `EMPTYLINE`      | `aaaa\n\nbbbb\nccc`                 |
| `JSON_SECRET`    | `{"key1":"value1","key2":"value2"}` |

> [!NOTE]
>
> 引号需要双重转义。

## SSH mounts

SSH 挂载让你可以向 SSH 服务器进行身份验证。
例如执行 `git clone`，
或从私有仓库获取应用包。

下面的 Dockerfile 示例使用 SSH 挂载
从私有 GitHub 仓库获取 Go 模块。

```dockerfile {collapse=1}
# syntax=docker/dockerfile:1

ARG GO_VERSION="{{% param example_go_version %}}"

FROM golang:${GO_VERSION}-alpine AS base
ENV CGO_ENABLED=0
ENV GOPRIVATE="github.com/foo/*"
RUN apk add --no-cache file git rsync openssh-client
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
WORKDIR /src

FROM base AS vendor
# this step configure git and checks the ssh key is loaded
RUN --mount=type=ssh <<EOT
  set -e
  echo "Setting Git SSH protocol"
  git config --global url."git@github.com:".insteadOf "https://github.com/"
  (
    set +e
    ssh -T git@github.com
    if [ ! "$?" = "1" ]; then
      echo "No GitHub SSH key loaded exiting..."
      exit 1
    fi
  )
EOT
# this one download go modules
RUN --mount=type=bind,target=. \
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=ssh \
    go mod download -x

FROM vendor AS build
RUN --mount=type=bind,target=. \
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache \
    go build ...
```

要构建这个 Dockerfile，你必须在步骤中指定一个构建器可用于 `--mount=type=ssh` 的 SSH 挂载。

下面的 GitHub Action 工作流使用了第三方 action `MrSquaare/ssh-setup-action`
在 GitHub runner 上引导 SSH 配置。该 action 会创建一个由 GitHub Action secret `SSH_GITHUB_PPK`
定义的私钥，并将其添加到 `SSH_AUTH_SOCK` 处的 SSH agent 套接字文件。构建步骤中的 SSH 挂载
默认假定 `SSH_AUTH_SOCK`，因此无需显式指定 SSH agent 套接字的 ID 或路径。

{{< tabs >}}
{{< tab name="`docker/build-push-action`" >}}

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up SSH
        uses: MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a # v3.1.0
        with:
          host: github.com
          private-key: ${{ secrets.SSH_GITHUB_PPK }}
          private-key-name: github-ppk

      - name: Build and push
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          ssh: default
          push: true
          tags: user/app:latest
```

{{< /tab >}}
{{< tab name="`docker/bake-action`" >}}

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up SSH
        uses: MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a # v3.1.0
        with:
          host: github.com
          private-key: ${{ secrets.SSH_GITHUB_PPK }}
          private-key-name: github-ppk

      - name: Build
        uses: docker/bake-action@{{% param "bake_action_version" %}}
        with:
          set: |
            *.ssh=default
```

{{< /tab >}}
{{< /tabs >}}
