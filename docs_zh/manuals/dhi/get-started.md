---
linktitle: 快速开始
title: Docker Hardened Images 快速开始
description: 通过快速开始指南探索并运行 Docker Hardened Image。
weight: 2
keywords: docker hardened images quickstart, run secure image
---

本指南将通过一个真实示例，向你展示如何从零开始运行 Docker Hardened Image（DHI）。最后，你将对比 DHI 与标准 Docker 镜像的差异，从而更好地理解它们的区别。虽然示例使用了特定镜像，但这些步骤适用于任何 DHI。

> [!NOTE]
>
> Docker Hardened Images 对所有人免费提供，无需订阅，无使用限制，无厂商锁定。当你需要企业级功能（如 FIPS 或 STIG 合规变体、自定义能力或 SLA 支持）时，可升级至 DHI Enterprise 订阅。

## 步骤 1：查找要使用的镜像

1. 访问 [Docker Hub](https://hub.docker.com/hardened-images/catalog) 中的 Hardened Images 目录并登录。
2. 在左侧边栏中，选择 **Hardened Images**。如果你有 DHI Enterprise，请选择 **Hardened Images** > **Catalog**。
3. 使用搜索框或筛选器查找镜像（例如 `python`、`node`、`golang`）。本指南以 Python 镜像为例。
4. 选择 Python 仓库以查看其详细信息。

继续下一步以拉取并运行镜像。如需深入了解镜像探索，请参阅 [探索 Docker Hardened Images](./how-to/explore.md)。

## 步骤 2：拉取并运行镜像

你可以像拉取和运行任何其他 Docker 镜像一样拉取和运行 DHI。注意，Docker Hardened Images 旨在最小化和安全，因此它们可能不包含你期望在典型镜像中的所有工具或库。你可以在 [采用 DHIs 时的注意事项](./how-to/use.md#considerations-when-adopting-dhis) 中查看典型差异。

> [!TIP]
>
> 在 DHI 目录的每个仓库页面上，选择 **Use this image** 即可找到拉取和扫描镜像的说明。

以下示例演示了你可以运行 Python 镜像并执行简单的 Python 命令，就像使用任何其他 Docker 镜像一样：

1. 打开终端，使用你的 Docker ID 凭据登录到 Docker Hardened Images 注册表。

   ```console
   $ docker login dhi.io
   ```

2. 拉取镜像：

   ```console
   $ docker pull dhi.io/python:3.13
   ```

3. 运行镜像以确认一切正常：

    ```console
    $ docker run --rm dhi.io/python:3.13 python -c "print('Hello from DHI')"
    ```

    此命令从 `python:3.13` 镜像启动一个容器，并运行一个简单的 Python 脚本，打印 `Hello from DHI`。

如需深入了解镜像使用，请参阅：

- [使用 Docker Hardened Image](./how-to/use.md) 了解一般用法
- [在 Kubernetes 中使用](./how-to/k8s.md) 了解 Kubernetes 部署
- [使用 Helm Chart](./how-to/helm.md) 了解使用 Helm 部署

## 步骤 3：与其他镜像对比

你可以快速对比 DHIs 与其他镜像，以查看安全改进和差异。这种对比有助于你理解使用加固镜像的价值。

运行以下命令，查看 Docker Hardened Image for Python 与 Docker Hub 上非加固的 Docker Official Image for Python 的摘要对比：

```console
$ docker scout compare dhi.io/python:3.13 \
    --to python:3.13 \
    --platform linux/amd64 \
    --ignore-unchanged \
    2>/dev/null | sed -n '/## Overview/,/^  ## /p' | head -n -1
```

示例输出：

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
> 这是示例输出。你的结果可能因新发现的 CVE 和镜像更新而异。
>
> Docker 在 Docker Hardened Images 中保持接近零的 CVE。对于 DHI Enterprise 订阅，当发现新 CVE 时，将在行业领先的 SLA 时间范围内修复。了解有关 [SLA 支持的安全功能](./features.md#sla-backed-security) 的更多信息。

此对比显示 Docker Hardened Image：

- 消除漏洞：移除了 1 个高危、5 个中危、141 个低危和 2 个未指定严重性的 CVE
- 减小体积：从 412 MB 减少到 35 MB（减少 91%）
- 减少包数量：从 610 个包减少到 80 个（减少 87%）

如需深入了解镜像对比，请参阅 [对比 Docker Hardened Images](./how-to/compare.md)。

## 下一步

你已成功拉取并运行了第一个 Docker Hardened Image。以下是继续探索的几种方式：

- [将现有应用迁移到 DHIs](./migration/migrate-with-ai.md)：使用 Docker 的 AI 助手更新你的 Dockerfile，以使用 Docker Hardened Images 作为基础。

- [开始试用](https://hub.docker.com/hardened-images/start-free-trial)：探索 DHI Enterprise 订阅的优势，例如访问 FIPS 和 STIG 变体、自定义镜像以及 SLA 支持的更新。

- [镜像仓库](./how-to/mirror.md)：订阅 DHI Enterprise 或开始试用后，学习如何镜像 DHI 仓库以启用自定义、访问合规变体并获得 SLA 支持的更新。

- [验证 DHIs](./how-to/verify.md)：使用 Docker Scout 或 Cosign 等工具检查和验证签名证明（如 SBOM 和来源）。

- [扫描 DHIs](./how-to/scan.md)：使用 Docker Scout 或其他扫描器分析镜像以识别已知 CVE。