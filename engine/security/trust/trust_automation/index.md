# 使用内容信任实现自动化

Docker 内容信任（Docker Content Trust）通常被集成到现有的自动化系统中。为了让工具能够封装 Docker 并推送受信任的内容，可以向客户端传递特定的环境变量。

本指南遵循[使用 Docker 内容信任签名镜像](index.md#signing-images-with-docker-content-trust)中描述的步骤。请确保您已理解并满足先决条件。

当直接使用 Notary 客户端时，它使用[自己的一套环境变量](https://github.com/theupdateframework/notary/blob/master/docs/reference/client-config.md#environment-variables-optional)。

## 添加委派私钥

为了自动化将委派私钥导入本地 Docker 信任存储，我们需要传递新密钥的密码短语。每次使用该委派对标签进行签名时，都需要此密码短语。

```console
$ export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="mypassphrase123"

$ docker trust key load delegation.key --name jeff
Loading key from "delegation.key"...
Successfully imported key from delegation.key
```

## 添加委派公钥

如果您在添加委派公钥的同时初始化仓库，则需要使用本地 Notary 规范根密钥（Canonical Root Key）的密码短语来创建仓库的信任数据。如果仓库已经初始化，则只需要仓库的密码短语。

```console
# 如果需要，导出本地根密钥密码短语。
$ export DOCKER_CONTENT_TRUST_ROOT_PASSPHRASE="rootpassphrase123"

# 导出仓库密码短语
$ export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="repopassphrase123"

# 初始化仓库并推送委派
$ docker trust signer add --key delegation.crt jeff registry.example.com/admin/demo
Adding signer "jeff" to registry.example.com/admin/demo...
Initializing signed repository for registry.example.com/admin/demo...
Successfully initialized "registry.example.com/admin/demo"
Successfully added signer: registry.example.com/admin/demo
```

## 签名镜像

最后，在签名镜像时，我们需要导出签名密钥的密码短语。该密钥是在使用 `$ docker trust key load` 将密钥加载到本地 Docker 信任存储时创建的。

```console
$ export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="mypassphrase123"

$ docker trust sign registry.example.com/admin/demo:1
Signing and pushing trust data for local image registry.example.com/admin/demo:1, may overwrite remote trust data
The push refers to repository [registry.example.com/admin/demo]
428c97da766c: Layer already exists
2: digest: sha256:1a6fd470b9ce10849be79e99529a88371dff60c60aab424c077007f6979b4812 size: 524
Signing and pushing trust metadata
Successfully signed registry.example.com/admin/demo:1
```

## 使用内容信任进行构建

您也可以在构建时使用内容信任。在运行 `docker build` 命令之前，您应该手动或以脚本方式设置环境变量 `DOCKER_CONTENT_TRUST`。考虑下面的简单 Dockerfile。

```dockerfile
# syntax=docker/dockerfile:1
FROM docker/trusttest:latest
RUN echo
```

`FROM` 标签正在拉取一个已签名的镜像。您无法构建一个 `FROM` 镜像既不在本地存在也未签名的镜像。假设标签 `latest` 存在内容信任数据，以下构建应该会成功：

```console
$  docker build -t docker/trusttest:testing .
Using default tag: latest
latest: Pulling from docker/trusttest

b3dbab3810fc: Pull complete
a9539b34a6ab: Pull complete
Digest: sha256:d149ab53f871
```

如果启用了内容信任，构建依赖于没有信任数据的标签的 Dockerfile 会导致构建命令失败：

```console
$  docker build -t docker/trusttest:testing .
unable to process Dockerfile: No trust data for notrust
```

## 相关信息

* [内容信任的委派](trust_delegation.md)
* [Docker 中的内容信任](index.md)
* [管理内容信任的密钥](trust_key_mng.md)
* [在内容信任沙盒中体验](trust_sandbox.md)
