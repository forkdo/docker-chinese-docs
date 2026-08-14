---
title: 在仪表板中使用策略页面
linkTitle: 使用仪表板
description: 使用 Docker Scout 仪表板查看策略状态、配置策略并获取修复建议
keywords: scout, policy, dashboard, configure, remediation, status
params:
  sidebar:
    badge:
      color: gray
      text: 已弃用
aliases:
  - /scout/policy/ci/
  - /scout/policy/view/
  - /scout/policy/configure/
  - /scout/policy/remediation/
---

> [!IMPORTANT]
>
> 策略页面已弃用，将于 2026 年 9 月 1 日停用。
> `docker scout policy` 命令将取代该页面，并提供更多用于
> 评估策略的选项。您可以在本地、CI 中、针对自定义
> Rego 策略或使用 OCI 包进行评估。请参阅
> [评估策略](./local.md)。

## 查看策略状态

[Docker Scout 仪表板](https://scout.docker.com/) 的 **Overview（概览）** 标签页
显示了您的仓库中策略的最新变化摘要。
该摘要显示了在最近一次镜像和前一次镜像之间，策略
评估结果变化最大的镜像。

### 每个仓库的策略状态

**Images（镜像）** 标签页显示了所选环境中所有镜像的当前策略状态以及
最近的策略趋势。**Policy status（策略状态）** 列显示：

- 已满足的策略数量与策略总数
- 最近的策略趋势

策略趋势由方向箭头表示，指示某个镜像与其在同一环境中的
前一次镜像相比是变得更好、更差还是没有变化。

- 向上的绿色箭头显示改善的策略数量。
- 向下的红色箭头显示恶化的策略数量。
- 双向的灰色箭头显示未变化的策略数量。

### 详细结果

要查看某个镜像的完整评估结果，请导航到 Docker Scout 仪表板中的
镜像标签并打开 **Policy（策略）** 标签页。

对于与漏洞相关的策略，详情视图在可用时会显示修复版本。对于与许可证
相关的策略，列表显示所有不符合策略标准的软件包。

## 配置策略

某些策略类型是可配置的。您可以创建带有自定义参数的版本，
禁用某个策略，或删除它。

> [!NOTE]
> 如果您删除或自定义某个策略，默认策略配置的
> 历史评估结果将被删除。

### 添加策略

1. 转到 Docker Scout 仪表板中的 [策略页面](https://scout.docker.com/reports/policy)。
2. 选择 **Add policy（添加策略）**。
3. 找到您要配置的策略类型并选择 **Configure（配置）**。

   - 如果 **Configure** 是灰色的，说明该策略没有可配置的参数。
   - 如果按钮显示 **Integrate（集成）**，则启用该策略前需要先完成设置。

4. 更新策略参数。
5. 选择 **Save policy（保存策略）** 以启用，或 **Save and disable（保存并禁用）** 以保存但不启用。

### 编辑策略

1. 转到 [策略页面](https://scout.docker.com/reports/policy)。
2. 选择该策略，然后选择 **Edit（编辑）**。
3. 更新参数并保存。

### 禁用策略

禁用策略会隐藏其结果，但不会删除历史数据。

1. 转到 [策略页面](https://scout.docker.com/reports/policy)。
2. 选择该策略，然后选择 **Disable（禁用）**。

### 删除策略

删除策略会移除其评估结果。

1. 转到 [策略页面](https://scout.docker.com/reports/policy)。
2. 选择该策略，然后选择 **Delete（删除）**。

要重新创建已删除的策略，请遵循 [添加策略](#add-a-policy)，并在已删除的
策略类型上选择 **Configure**。

## 修复

Docker Scout 根据策略评估结果提供修复建议。以下策略类型
提供建议：

- [最新的基础镜像](#up-to-date-base-images)
- [供应链证明](#supply-chain-attestations)

要查看建议：

1. 转到 [策略页面](https://scout.docker.com/reports/policy)。
2. 选择一个策略。
3. 将鼠标悬停在列表中的某个镜像上并选择 **View fixes（查看修复）**。

如果有多个建议可用，主建议显示为 **Recommended fix（推荐修复）**。
其他建议列为 **Quick fixes（快速修复）**。

### 最新的基础镜像

如果没有来源证明，合规性无法确定。添加
[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)
以便 Docker Scout 能够检测您正在使用的基础镜像版本。

有了来源证明，推荐的操作会显示如何将您的基础镜像更新到最新版本，
并将其固定到特定的摘要。请参阅
[固定基础镜像版本](/manuals/build/building/best-practices.md#pin-base-image-versions)。

启用 GitHub 集成后，您可以直接从修复面板发起拉取请求，
以更新 Dockerfile 中的基础镜像版本。

### 供应链证明

**Supply Chain Attestations（供应链证明）** 策略需要 SBOM 和来源
证明。修复面板会显示缺少的内容。例如，如果您的镜像拥有来源证明
但信息不足，请使用
[`mode=max`](/manuals/build/metadata/attestations/slsa-provenance.md#max) 来源证明重新构建。

## 在 CI 中评估策略合规性

将策略评估添加到您的 CI 流水线有助于您检测并防止
变更会导致策略合规性相对于基线变差的情况。

推荐的策略涉及使用 [环境](../integrations/environment/_index.md) 评估本地镜像，
并将结果与该环境进行比较。如果新镜像的策略合规性比基线差，
CI 运行就会失败。如果合规性更好或没有变化，则运行成功。

以下 GitHub Actions 示例使用 [Docker Scout GitHub Action](https://github.com/marketplace/actions/docker-scout)
将拉取请求镜像与 `production` 环境进行比较。将 `exit-on` 输入
设置为 `policy`，因此只有在策略合规性恶化时该步骤才会失败。

> [!NOTE]
>
> 由于 Docker Engine 的限制，不支持将多平台镜像或带有证明的镜像
> 加载到镜像存储。请构建一个不带证明的单平台镜像并将其加载，
> 以使策略评估能够正常工作。

```yaml
name: Docker

on:
  push:
    tags: ["*"]
    branches:
      - "main"
  pull_request:
    branches: ["**"]

env:
  REGISTRY: docker.io
  IMAGE_NAME: <IMAGE_NAME>
  DOCKER_ORG: <ORG>

jobs:
  build:
    permissions:
      pull-requests: write

    runs-on: ubuntu-latest
    steps:
      - name: Log into registry ${{ env.REGISTRY }}
        uses: docker/login-action@{{% param "login_action_version" %}}
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_TOKEN }}

      - name: Setup Docker buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@{{% param "metadata_action_version" %}}
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build image
        id: build-and-push
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          sbom: ${{ github.event_name != 'pull_request' }}
          provenance: ${{ github.event_name != 'pull_request' }}
          push: ${{ github.event_name != 'pull_request' }}
          load: ${{ github.event_name == 'pull_request' }}

      - name: Authenticate with Docker
        uses: docker/login-action@{{% param "login_action_version" %}}
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PAT }}

      - name: Compare
        if: ${{ github.event_name == 'pull_request' }}
        uses: docker/scout-action@v1
        with:
          command: compare
          image: ${{ steps.meta.outputs.tags }}
          to-env: production
          platform: "linux/amd64"
          ignore-unchanged: true
          only-severities: critical,high
          organization: ${{ env.DOCKER_ORG }}
          exit-on: policy
```

对于其他 CI 平台，请参阅
[Docker Scout CI 集成](../integrations/_index.md#continuous-integration)。
