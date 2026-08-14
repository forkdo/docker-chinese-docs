# 搜索和评估 Docker 安全加固镜像


## 搜索目录

您可以在 [Docker Hub 目录](https://hub.docker.com/hardened-images/catalog) 中按类别浏览、搜索或筛选镜像。有关目录界面的详细信息，请参阅 [Docker Hub](/dhi/tools/hub/)。

或者，您可以使用 [DHI MCP server](/dhi/tools/mcp/) 直接从您的 AI 助手搜索和检查目录，或者使用 [DHI CLI](/dhi/tools/cli/) 从命令行浏览目录：

```console
$ docker dhi catalog list
```

按镜像类型、名称或合规要求进行筛选：

```console
$ docker dhi catalog list --type image
$ docker dhi catalog list --filter python
$ docker dhi catalog list --fips
$ docker dhi catalog list --stig
```

要查看仓库详细信息，包括可用标签和 CVE 数量：

```console
$ docker dhi catalog get python
```

## 比较和评估镜像

Docker Scout 允许您分析两个镜像之间的差异。将 DHI 与标准镜像进行比较，有助于您了解采用加固镜像所带来的安全改进、软件包差异以及整体优势。

比较适用于：

- 评估从标准镜像迁移到 DHI 时的安全改进
- 了解镜像变体之间的软件包和漏洞差异
- 评估自定义或更新的影响

### 先决条件

在比较镜像之前：

- 安装 [Docker Desktop](/desktop/) 以使用 Docker Scout 比较功能。
- 登录 `dhi.io` 以获取 Docker 安全加固镜像：

  ```console
  $ docker login dhi.io
  ```

### 基本比较

要将 Docker 安全加固镜像与另一个镜像进行比较，请使用 [`docker scout compare`](/reference/cli/docker/scout/compare/) 命令：

```console
$ docker scout compare dhi.io/<image>:<tag> \
    --to <comparison-image>:<tag> \
    --platform <platform>
```

例如，要将 DHI Node.js 镜像与官方 Node.js 镜像进行比较：

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to node:22 \
    --platform linux/amd64
```

输出在顶部显示包含关键比较指标的概览，随后是详细的软件包和漏洞信息。概览示例：

```console
  ## Overview

                      │                    Analyzed Image                     │              Comparison Image
  ────────────────────┼───────────────────────────────────────────────────────┼─────────────────────────────────────────────
    Target            │  dhi.io/node:22-debian13                              │  node:22
      digest          │  55d471f61608                                         │  9ee3220f602f
      platform        │ linux/amd64                                           │ linux/amd64
      vulnerabilities │    0C     0H     0M     0L                            │    0C     1H     3M   153L     4?
                      │           -1     -3   -153     -4                     │
      size            │ 41 MB (-367 MB)                                       │ 408 MB
      packages        │ 19 (-726)                                             │ 745
```

### 筛选未更改的软件包

要仅关注差异并忽略未更改的软件包，请使用 `--ignore-unchanged` 标志：

```console
$ docker scout compare dhi.io/node:22-debian13 \
    --to node:22 \
    --platform linux/amd64 \
    --ignore-unchanged
```

此输出仅突出显示两个镜像之间不同的软件包和漏洞。

