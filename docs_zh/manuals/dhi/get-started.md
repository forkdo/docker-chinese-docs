---
linktitle: 快速入门
title: Docker 加固镜像快速入门
description: 按照快速入门指南探索并运行 Docker 加固镜像。
weight: 2
keywords: docker hardened images quickstart, run secure image
---

本指南通过一个真实示例，向您展示如何从零开始运行 Docker 加固镜像 (DHI)。最后，您将 DHI 与标准 Docker 镜像进行比较，以更好地理解两者之间的差异。虽然这些步骤以特定镜像为例，但它们适用于任何 DHI。

本快速入门使用来自 `dhi.io` 的 DHI Community 镜像。您使用 Docker 账户登录，拉取并运行镜像，然后将其与 Docker 官方镜像进行比较。

> [!NOTE]
>
> 如果您拥有 DHI Select 或 Enterprise 订阅，请改为参阅[开始使用 DHI Select 和 Enterprise](./how-to/select-enterprise.md)。Select 和 Enterprise 在 Docker Hub 上的组织命名空间中使用镜像仓库，以启用定制、SLA 支持的安全更新以及合规变体的访问。

## 步骤 1：查找要使用的镜像

1. 前往 [Docker Hub](https://hub.docker.com/hardened-images/catalog) 中的加固镜像目录。
2. 使用搜索栏或筛选器查找镜像（例如 `python`、`node` 或 `golang`）。本示例搜索 `python`。
3. 选择 Python 仓库以查看其详细信息。

继续下一步以拉取并运行镜像。要深入了解镜像搜索与评估，请参阅[搜索和评估 Docker 加固镜像](./how-to/search-evaluate.md)。

## 步骤 2：拉取并运行镜像

您可以像使用其他 Docker 镜像一样拉取并运行 DHI。请注意，Docker 加固镜像设计为最小且安全，因此可能不包含典型镜像中您所期望的所有工具或库。您可以在[采用 DHI 时的注意事项](./how-to/use.md#considerations-when-adopting-dhis)中查看典型差异。

以下示例演示您可以运行 Python 镜像并执行简单的 Python 命令，就像使用任何其他 Docker 镜像一样：

1. 打开终端并使用您的 Docker 账户凭据登录 Docker 加固镜像注册表。

   ```console
   $ docker login dhi.io
   ```

   > [!TIP]
   >
   > 如果您还没有 Docker 账户，请[创建一个免费账户](https://hub.docker.com/signup)以开始使用。

2. 拉取镜像：

   ```console
   $ docker pull dhi.io/python:3.13
   ```

3. 运行镜像以确认一切正常：

    ```console
    $ docker run --rm dhi.io/python:3.13 python -c "print('Hello from DHI')"
    ```

    这将从 `python:3.13` 镜像启动一个容器，并运行一个简单的 Python 脚本，打印 `Hello from DHI`。

要深入了解镜像使用，请参阅：

- [使用 Docker 加固镜像](./how-to/use.md)：了解一般用法
- [使用 Helm chart](./how-to/helm.md)：了解使用 Helm 部署

## 步骤 3：与其他镜像比较

您可以快速将 DHI 与其他镜像进行比较，以了解安全改进和差异。这种比较有助于您理解使用加固镜像的价值。

运行以下命令，将 Docker 加固 Python 镜像与 Docker Hub 上的非加固 Docker 官方 Python 镜像进行比较。在输出中查找 `## Overview` 部分以查看摘要比较：

```console
$ docker scout compare dhi.io/python:3.13 \
    --to python:3.13 \
    --platform linux/amd64 \
    --ignore-unchanged
```

输出的 `## Overview` 部分类似于以下内容：

```plaintext
  ## Overview

                      │                    Analyzed Image                     │               Comparison Image
  ────────────────────┼───────────────────────────────────────────────────────┼───────────────────────────────────────────────
    Target            │  dhi.io/python:3.13                                   │  python:3.13
      digest          │  c215e9da9f84                                         │  7f48e892134c
      tag             │  3.13                                                 │  3.13
      platform        │ linux/amd64                                           │ linux/amd64
      provenance      │ https://github.com/docker-hardened-images/definitions │ https://github.com/docker-library/python.git
                      │  77a629b3d0db035700206c2a4e7ed904e5902ea8             │  3f2d7e4c339ab883455b81a873519f1d0f2cd80a
      vulnerabilities │    0C     0H     0M     0L                            │    0C     1H     5M   141L     2?
                      │           -1     -5   -141     -2                     │
      size            │ 35 MB (-377 MB)                                       │ 412 MB
      packages        │ 80 (-530)                                             │ 610
                      │                                                       │
```

> [!NOTE]
>
> 这是示例输出。您的结果可能因新发现的 CVE 和镜像更新而异。

Docker 在 Docker 加固镜像中保持接近零 CVE。对于 DHI Select 和 Enterprise 订阅，当发现新的 CVE 时，会在行业领先的 SLA 时间范围内修复这些 CVE。了解有关 [SLA 支持的安全功能](./_index.md#sla-backed-security) 的更多信息。

此比较显示 Docker 加固镜像：

- 移除漏洞：1 个高危、5 个中危、141 个低危和 2 个未指定严重程度的 CVE 被移除
- 减小体积：从 412 MB 减少到 35 MB（减少 91%）
- 最小化软件包：从 610 个软件包减少到 80 个（减少 87%）

要深入了解镜像比较，请参阅[搜索和评估 Docker 加固镜像](./how-to/search-evaluate.md#compare-and-evaluate-images)。

## 下一步

您已拉取并运行了第一个 Docker 加固镜像。以下是继续操作的几种方式：

- [将现有应用程序迁移到 DHI](./migration/migrate-with-ai.md)：使用 Gordon 更新您的 Dockerfile，以使用 Docker 加固镜像作为基础镜像。

- [开始试用](https://hub.docker.com/hardened-images/start-free-trial)：探索 DHI 订阅的优势，例如访问 FIPS 和 STIG 变体、定制镜像以及 SLA 支持的更新。

- [开始使用 DHI Select 和 Enterprise](./how-to/select-enterprise.md)：在订阅 DHI 订阅或开始试用后，了解如何镜像仓库、定制镜像并访问合规变体。

- [验证 DHI](./how-to/verify.md)：使用 [Docker Scout](/scout/) 或 Cosign 等工具检查和验证签名证明，例如 SBOM 和来源。

- [扫描 DHI](./how-to/scan.md)：使用 Docker Scout 或其他扫描器分析镜像以识别已知 CVE。
