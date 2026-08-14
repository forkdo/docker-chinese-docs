---
title: Use the DHI CLI
linkTitle: CLI
weight: 20
keywords: docker dhi, CLI, command line, docker hardened images
description: 了解如何安装和使用 docker dhi，即用于管理 Docker Hardened Images 的命令行界面。
aliases:
  - /dhi/how-to/cli/
---

`docker dhi` 命令行界面 (CLI) 是用于管理 Docker Hardened Images 的工具：
- 浏览可用的 DHI 镜像及其元数据
- 查看 DHI 镜像的证明，包括 SBOM 和来源信息
- 将 DHI 镜像镜像到您的 Docker Hub 组织
- 创建和管理 DHI 镜像的自定义配置
- 为企业的包仓库生成身份验证凭据
- 监控自定义配置构建

## 安装

`docker dhi` CLI 在 [Docker Desktop](https://docs.docker.com/desktop/) 4.65 及更高版本中可用。
您也可以安装独立的 `dhictl` 二进制文件。

### Docker Desktop

`docker dhi` 命令已包含在 Docker Desktop 4.65 及更高版本中。无需额外安装。

### 独立二进制文件

1. 从 [releases](https://github.com/docker-hardened-images/dhictl/releases) 页面下载适用于您平台的 `dhictl` 二进制文件。
2. 将其移动到您 `PATH` 中的目录：
    - 在 _Linux_ 和 _macOS_ 上为 `mv dhictl /usr/local/bin/`
    - 在 _Windows_ 上将 `dhictl.exe` 移动到您 `PATH` 中的目录

## 用法

每个命令都内置可通过 `--help` 标志访问的帮助：

```console
$ docker dhi --help
$ docker dhi catalog list --help
```

### 浏览 DHI 目录

列出所有可用的 DHI 镜像：

```console
$ docker dhi catalog list
```

按类型、名称或合规性进行筛选：

```console
$ docker dhi catalog list --type image
$ docker dhi catalog list --filter golang
$ docker dhi catalog list --fips
$ docker dhi catalog list --stig
```

获取特定镜像的详细信息，包括可用标签和 CVE 数量：

```console
$ docker dhi catalog get <image-name>
```

### 查看证明

列出附加到 DHI 镜像的所有证明：

```console
$ docker dhi attestation list dhi/nginx:1.27
$ docker dhi attestation list dhi/nginx:1.27 --platform linux/amd64
$ docker dhi attestation list dhi/nginx:1.27 --predicate-type https://slsa.dev/provenance/v1
$ docker dhi attestation list dhi/nginx:1.27 --json
```

通过引用摘要获取特定的证明：

```console
$ docker dhi attestation get dhi/nginx:1.27 sha256:<digest>
$ docker dhi attestation get dhi/nginx:1.27 sha256:<digest> -o provenance.json
```

显示镜像的 SPDX SBOM：

```console
$ docker dhi attestation sbom dhi/nginx:1.27
$ docker dhi attestation sbom dhi/nginx:1.27 --platform linux/amd64
```

### 镜像 DHI 镜像

{{< summary-bar feature_name="Docker Hardened Images" >}}

开始将一个或多个 DHI 镜像镜像到您的 Docker Hub 组织：

```console
$ docker dhi mirror start --org my-org \
  dhi/golang,my-org/dhi-golang \
  dhi/nginx,my-org/dhi-nginx \
  dhi/prometheus-chart,my-org/dhi-prometheus-chart
```

镜像包含依赖项：

```console
$ docker dhi mirror start --org my-org dhi/golang,my-org/dhi-golang --dependencies
```

列出您组织中的已镜像镜像：

```console
$ docker dhi mirror list --org my-org
```

按名称或类型筛选已镜像镜像：

```console
$ docker dhi mirror list --org my-org --filter python
$ docker dhi mirror list --org my-org --type image
$ docker dhi mirror list --org my-org --type helm-chart
```

停止镜像一个或多个镜像：

```console
$ docker dhi mirror stop dhi-golang --org my-org
$ docker dhi mirror stop dhi-python dhi-golang --org my-org
```

停止镜像并删除仓库：

```console
$ docker dhi mirror stop dhi-golang --org my-org --delete
$ docker dhi mirror stop dhi-golang --org my-org --delete --force
```

### 自定义 DHI 镜像

{{< summary-bar feature_name="Docker Hardened Images" >}}

CLI 可用于创建和管理 DHI 镜像的自定义配置。有关使用 GUI 创建自定义配置的详细说明，请参阅[自定义 Docker 强化镜像](../how-to/customize.md)。

以下是 CLI 命令的快速参考。有关所有选项和标志的完整详细信息，请参阅 [CLI 参考](/reference/cli/docker/dhi/)。

```console
# 准备单个自定义配置脚手架
$ docker dhi customization prepare golang 1.25 \
  --org my-org \
  --destination my-org/dhi-golang \
  --name "golang with git" \
  > my-customization.yaml

# 准备批量自定义配置脚手架（通过 stdin 管道传输 JSON 数组）
$ echo '[{"destination":"my-org/dhi-golang","tag-definition-id":"golang/alpine-3.23/1.24-dev"}]' \
  | docker dhi customization prepare --name "golang with git" --org my-org \
  > my-customization.yaml

# 创建自定义配置
$ docker dhi customization create my-customization.yaml --org my-org

# 使用标志覆盖进行创建（标志优先于 YAML 文件）
$ docker dhi customization create my-customization.yaml --org my-org \
  --destination my-org/dhi-golang \
  --name "golang with git"

# 列出自定义配置
$ docker dhi customization list --org my-org

# 按名称、仓库或来源筛选自定义配置
$ docker dhi customization list --org my-org --filter git
$ docker dhi customization list --org my-org --repo dhi-golang
$ docker dhi customization list --org my-org --source golang

# 通过 ID 获取自定义配置
$ docker dhi customization get <id> --org my-org

# 更新自定义配置
# YAML 文件必须包含 'id' 字段以标识要更新的自定义配置
$ docker dhi customization edit my-customization.yaml --org my-org

# 通过 ID 删除自定义配置
$ docker dhi customization delete <id> --org my-org

# 删除多个自定义配置
$ docker dhi customization delete <id1> <id2> --org my-org

# 无需确认提示即可删除
$ docker dhi customization delete <id> --org my-org --force
```

有关所有 YAML 字段的完整参考，请参阅
[镜像自定义 YAML 文件](/dhi/how-to/customize/#image-customization-yaml-file)。

### 企业包身份验证

{{< summary-bar feature_name="Docker Hardened Images Enterprise" >}}

生成用于访问企业加固包仓库的身份验证凭据。在您自己的镜像中配置包管理器以安装合规且安全修补的包时，会使用这些凭据。有关详细说明，请参阅[企业仓库](../how-to/hardened-packages.md#enterprise-repository)。

对于基于 Alpine 的镜像：

```console
$ docker dhi auth apk
```

对于基于 Debian 的镜像：

```console
$ docker dhi auth deb
```

### 监控自定义配置构建

{{< summary-bar feature_name="Docker Hardened Images" >}}

列出自定义配置的构建：

```console
$ docker dhi customization build list <customization-id> --org my-org
$ docker dhi customization build list <customization-id> --org my-org --json
```

获取特定构建的详细信息：

```console
$ docker dhi customization build get <customization-id> <build-id> --org my-org
$ docker dhi customization build get <customization-id> <build-id> --org my-org --json
```

查看构建日志：

```console
$ docker dhi customization build logs <customization-id> <build-id> --org my-org
$ docker dhi customization build logs <customization-id> <build-id> --org my-org --json
```

### JSON 输出

大多数 list 和 get 命令都支持 `--json` 标志以输出机器可读结果：

```console
$ docker dhi catalog list --json
$ docker dhi catalog get golang --json
$ docker dhi attestation list dhi/nginx:1.27 --json
$ docker dhi mirror list --org my-org --json
$ docker dhi mirror start --org my-org dhi/golang,my-org/dhi-golang --json
$ docker dhi customization list --org my-org --json
$ docker dhi customization build list <customization-id> --org my-org --json
```

## 配置

`docker dhi` CLI 可通过位于以下位置的 YAML 文件进行配置：
- 在 _Linux_ 和 _macOS_ 上为 `$HOME/.config/dhictl/config.yaml`
- 在 _Windows_ 上为 `%USERPROFILE%\.config\dhictl\config.yaml`

如果设置了 `$XDG_CONFIG_HOME`，则配置文件位于 `$XDG_CONFIG_HOME/dhictl/config.yaml`。

可用配置选项：

| 选项      | 环境变量 | 描述                                                                                                               |
|-------------|----------------------|---------------------------------------------------------------------------------------------------------------------------|
| `org`       | `DHI_ORG`            | 用于镜像和自定义配置命令的默认 Docker Hub 组织。                                                    |
| `api_token` | `DHI_API_TOKEN`      | 用于身份验证的 Docker 令牌。您可以在您的 [Docker Hub 账户设置](https://hub.docker.com/) 中生成令牌。 |

环境变量优先于配置文件中的值。
