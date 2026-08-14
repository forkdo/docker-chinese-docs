# 验证 Docker Hardened 镜像或图表


Docker Hardened 镜像 (DHI) 和图表包含签名证明，用于验证构建过程、内容和安全态势。

Docker 用于 DHI 镜像和图表的公钥发布在以下位置：

- https://registry.scout.docker.com/keyring/dhi/latest.pub
- https://github.com/docker-hardened-images/keyring

Docker 推荐使用 [Docker Scout](/scout/)，但你也可以使用 [`regctl`](https://github.com/regclient/regclient) 和 [`cosign`](https://docs.sigstore.dev/) 来检索和验证证明。Docker Scout 具有几个关键优势：它理解 DHI 证明结构，自动解析平台，提供人类可读的摘要，通过 `--verify` 一步完成验证，并与 Docker 的证明基础设施紧密集成。

> [!IMPORTANT]
>
> 您必须对 Docker Hardened 镜像注册表 (`dhi.io`) 进行身份验证才能拉取镜像。登录时请使用您的 Docker ID 凭据（与您用于 Docker Hub 的用户名和密码相同）。如果您没有 Docker 账户，请免费[创建一个](../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

## 验证镜像证明

> [!NOTE]
>
> 在运行 `docker scout attest` 命令之前，请确保您本地拉取的任何镜像都与远程镜像保持同步。您可以通过运行 `docker pull` 来实现这一点。如果您不这样做，可能会看到 `No attestation found`。

### 列出可用证明

要列出镜像的 DHI 镜像的证明：

**Docker Scout**



> [!NOTE]
>
> 如果镜像在您的设备上本地存在，您必须在镜像名称前加上 `registry://`。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

```console
$ docker scout attest list dhi.io/<image>:<tag>
```

此命令显示所有可用的证明，包括 SBOM、来源、漏洞报告等。

**regctl**



首先，对两个注册表进行身份验证。本示例使用[组织访问令牌 (OAT)](../../enterprise/security/access-tokens.md) 以您的 Docker 组织身份进行身份验证。OAT 必须对您要验证的 DHI 仓库至少具有 pull 访问权限。只有令牌范围内的仓库才可访问。或者，您可以使用具有 `read only` 访问权限的[个人访问令牌 (PAT)](../../security/access-tokens.md) 以 Docker Hub 用户身份进行身份验证。

> [!WARNING]
>
> 以下示例为了演示目的在命令行上直接导出凭据。这会在您的 shell 历史记录和进程列表中暴露敏感令牌。在生产环境中，请使用安全的方法，例如从受限权限的文件中读取、在运行时加载的环境文件，或密钥管理工具。

```console
$ export DOCKER_ORG="YOUR_DOCKER_ORG"
$ export DOCKER_OAT="YOUR_DOCKER_OAT"
$ echo $DOCKER_OAT | regctl registry login -u "$DOCKER_ORG" --pass-stdin docker.io
$ echo $DOCKER_OAT | regctl registry login -u "$DOCKER_ORG" --pass-stdin registry.scout.docker.com
```

然后使用 `--external` 标志列出证明。DHI 仓库将镜像层存储在 `dhi.io`（或镜像镜像的 `docker.io`）上，并将签名证明存储在 `registry.scout.docker.com` 中：

```console
$ regctl artifact list docker.io/${DOCKER_ORG}/<image>:<tag> \
  --external registry.scout.docker.com/${DOCKER_ORG}/<image> \
  --platform linux/amd64
```

例如：

```console
$ regctl artifact list docker.io/${DOCKER_ORG}/dhi-node:22 \
  --external registry.scout.docker.com/${DOCKER_ORG}/dhi-node \
  --platform linux/amd64
```



### 检索特定证明

**Docker Scout**



要检索特定证明，请使用 `--predicate-type` 标志和完整的谓词类型 URI：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/<image>:<tag>
```

> [!NOTE]
>
> 如果镜像在您的设备上本地存在，您必须在镜像名称前加上 `registry://`。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

例如：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/python:3.13
```

要仅检索谓词主体：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --predicate \
  dhi.io/<image>:<tag>
```

例如：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --predicate \
  dhi.io/python:3.13
```

**regctl**



列出证明后，使用 `Name` 字段中的摘要下载完整的证明制品：

```console
$ regctl artifact get <attestation-digest> > attestation.json
```

例如，要保存 SLSA 来源证明：

```console
$ regctl artifact get registry.scout.docker.com/${DOCKER_ORG}/dhi-node@sha256:6cbf803796e281e535f2681de7cd33a1012202610322a50ee745d1bb02ac3c18 > slsa_provenance.json
```



### 验证证明

**Docker Scout**



要使用 Docker Scout 验证证明，您可以使用 `--verify` 标志：

```console
$ docker scout attest get dhi.io/<image>:<tag> \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

> [!NOTE]
>
> 如果镜像在您的设备上本地存在，您必须在镜像名称前加上 `registry://`。例如，使用 `registry://dhi.io/node:20.19-debian12` 而不是 `dhi.io/node:20.19-debian12`。

例如，要验证 `dhi.io/node:20.19-debian12` 镜像的 SBOM 证明：

```console
$ docker scout attest get dhi.io/node:20.19-debian12 \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

**cosign**



列出证明并从 `Name` 字段获取摘要后，使用 cosign 进行验证：

```console
$ cosign verify \
  <attestation-digest-from-name-field> \
  --key https://registry.scout.docker.com/keyring/dhi/latest.pub \
  --insecure-ignore-tlog=true
```

例如：

```console
$ cosign verify \
  registry.scout.docker.com/${DOCKER_ORG}/dhi-node@sha256:6cbf803796e281e535f2681de7cd33a1012202610322a50ee745d1bb02ac3c18 \
  --key https://registry.scout.docker.com/keyring/dhi/latest.pub \
  --insecure-ignore-tlog=true
```

> [!NOTE]
>
> 需要使用 `--insecure-ignore-tlog=true` 标志，因为 DHI 证明可能不会记录在公共 Rekor 透明日志中以保护私有客户信息。证明签名仍会针对 Docker 的公钥进行验证。



#### 处理缺少的透明日志条目

在 Docker Scout 中使用 `--verify` 或 `cosign verify` 时，有时可能会看到如下错误：

```text
ERROR no matching signatures: signature not found in transparency log
```

这是因为 Docker Hardened 镜像并不总是将证明记录在公共的 [Rekor](https://docs.sigstore.dev/logging/overview/) 透明日志中。在证明可能包含私有用户信息的情况下（例如，镜像引用中您组织的命名空间），将其写入 Rekor 会公开该信息。

即使缺少 Rekor 条目，证明仍然使用 Docker 的公钥签名，并且可以通过跳过 Rekor 透明日志检查进行离线验证。

要跳过透明日志检查并根据 Docker 的密钥进行验证，请使用 `--skip-tlog` 标志：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/<image>:<tag> \
  --verify --skip-tlog
```

> [!NOTE]
>
> `--skip-tlog` 标志仅在 Docker Scout CLI 1.18.2 及更高版本中可用。
>
> 如果镜像在您的设备上本地存在，您必须在镜像名称前加上 `registry://`。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

这相当于使用带有 `--insecure-ignore-tlog=true` 标志的 `cosign`，该标志根据 Docker 发布的公钥验证签名，但忽略透明日志检查。

### 显示等效的 cosign 命令

使用 `--verify` 标志时，它还会打印相应的 [cosign](https://docs.sigstore.dev/) 命令来验证镜像签名：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --verify \
  dhi.io/<image>:<tag>
```

> [!NOTE]
>
> 如果镜像在您的设备上本地存在，您必须在镜像名称前加上 `registry://`。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

例如：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --verify \
  dhi.io/python:3.13
```

如果验证成功，Docker Scout 会打印完整的 `cosign verify` 命令。

示例输出：

```console
    v SBOM obtained from attestation, 101 packages found
    v Provenance obtained from attestation
    v cosign verify ...
```

> [!IMPORTANT]
>
> 使用 cosign 时，您必须首先对 DHI 注册表和 Docker Scout 注册表进行身份验证。
>
> 例如：
>
> ```console
> $ docker login dhi.io
> $ docker login registry.scout.docker.com
> $ cosign verify ...
> ```

## 验证包证明

除了镜像证明之外，单个加固包也有自己的证明。这些包级别的证明允许您验证镜像中特定包的溯源和构建信息。

有关如何从镜像证明中提取包信息并检索包级别证明的说明，请参阅[包证明](./hardened-packages.md#package-attestations)。

## 使用 Docker Scout 验证 Helm 图表证明

Docker Hardened 镜像 Helm 图表包含与容器镜像相同的全面证明。图表的验证过程与镜像相同，使用相同的 Docker Scout CLI 命令。

### 列出可用的图表证明

要列出 DHI Helm 图表的证明：

```console
$ docker scout attest list dhi.io/<chart>:<version>
```

例如，要列出 external-dns 图表的证明：

```console
$ docker scout attest list dhi.io/external-dns-chart:1.20.0
```

此命令显示所有可用的图表证明，包括 SBOM、来源、漏洞报告等。

### 检索特定的图表证明

要从 Helm 图表中检索特定证明，请使用 `--predicate-type` 标志和完整的谓词类型 URI：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/<chart>:<version>
```

例如：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  dhi.io/external-dns-chart:1.20.0
```

要仅检索谓词主体：

```console
$ docker scout attest get \
  --predicate-type https://cyclonedx.org/bom/v1.6 \
  --predicate \
  dhi.io/<chart>:<version>
```

### 使用 Docker Scout 验证图表证明

要使用 Docker Scout 验证图表证明，请使用 `--verify` 标志：

```console
$ docker scout attest get dhi.io/<chart>:<version> \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

例如，要验证 external-dns 图表的 SBOM 证明：

```console
$ docker scout attest get dhi.io/external-dns-chart:1.20.0 \
   --predicate-type https://scout.docker.com/sbom/v0.1 --verify
```

在[处理缺少的透明日志条目](#handle-missing-transparency-log-entries)中描述的相同 `--skip-tlog` 标志也可以在需要时用于图表证明。

## 可用的 DHI 证明

有关每个 DHI 镜像可用的证明列表，请参阅[可用证明](../explore/security-concepts/attestations.md#image-attestations)和[Helm 图表证明](../explore/security-concepts/attestations.md#helm-chart-attestations)。

## 在 Docker Hub 上探索证明

您还可以在[探索镜像变体](./search-evaluate.md#image-variant-details)时以可视化方式浏览证明。**证明**部分列出了每个可用的证明及其：

- 类型（例如 SBOM、VEX）
- 谓词类型 URI
- 用于 `cosign` 的摘要引用

这些证明是在 Docker Hardened 镜像或图表构建过程中自动生成并签名的。

