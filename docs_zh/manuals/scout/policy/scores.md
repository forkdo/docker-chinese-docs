---
title: Docker Scout 健康评分
description: |
  Docker Scout 健康评分提供对 Docker Hub 镜像的供应链评估，
  根据各种安全策略对其进行从 A 到 F 的评级。
keywords: scout, health scores, evaluation, checks, grades, docker hub
---

{{< summary-bar feature_name="Docker Scout health scores" >}}

Docker Scout 健康评分提供对 Docker Hub 上镜像的安全评估和整体供应链健康状况，帮助您确定镜像是否符合既定的安全最佳实践。评分范围为 A 到 F，其中 A 代表最高安全级别，F 代表最低安全级别，让您能够一目了然地了解镜像的安全状况。

只有作为拥有该仓库的组织成员，并且至少拥有仓库“读取”访问权限的用户才能查看健康评分。评分对于组织外部用户或没有“读取”访问权限的成员不可见。

## 查看健康评分

{{< tabs >}}
{{< tab name="Docker Hub" >}}

要查看 Docker Hub 中镜像的健康评分：

1. 访问 Docker Hub 并登录。
2. 导航到您的组织页面。

在仓库列表中，您可以看到每个仓库基于最新推送标签的健康评分。

![仓库健康评分](../images/score-badges-repolist.png)

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

要查看 Docker Desktop 中镜像的健康评分：

1. 打开 Docker Desktop 并登录到您的 Docker 账户。
2. 导航到**镜像**视图并选择 **Hub** 选项卡。

在仓库列表中，**健康**列显示已推送到 Docker Hub 的不同标签的评分。

![仓库健康评分](../images/score-badges-dd.png)

{{< /tab >}}
{{< /tabs >}}

健康评分徽章采用颜色编码来指示仓库的整体健康状况：

- **绿色**：A 或 B 评分。
- **黄色**：C 评分。
- **橙色**：D 评分。
- **红色**：E 或 F 评分。
- **灰色**：`N/A` 评分。

评分也显示在 Docker Hub 上特定仓库的页面上，以及每个影响评分的策略。

![Scout "A" 健康评分](../images/score-a-shiny.png?w=450px)

## 评分系统

健康评分通过根据 Docker Scout [策略](./_index.md)评估镜像来确定。这些策略与软件供应链的最佳实践保持一致。

如果您的镜像仓库已经注册了 Docker Scout，健康评分将根据为您的组织启用的策略自动计算。这还包括您配置的任何自定义策略。

如果您没有使用 Docker Scout，健康评分将显示您的镜像与默认策略的合规性，这是 Docker 推荐的作为镜像基础标准的一组供应链规则。您可以为您的组织启用 Docker Scout 并编辑策略配置，以根据您的特定策略获得更相关的健康评分。

### 评分过程

每个策略根据其[类型](/manuals/scout/policy/_index.md#policy-types)分配一个分值。如果镜像符合策略，则获得该策略类型的分值。镜像的健康评分基于相对于总可能分值的已获分值百分比计算。

1. 对镜像评估策略合规性。
2. 根据策略合规性授予分值。
3. 计算已获分值百分比：

   ```text
   百分比 = (分值 / 总分) * 100
   ```

4. 根据已获分值百分比分配最终评分，如下表所示：

   | 分值百分比（已获分值/总分） | 评分 |
   | ---------------------------------------- | ----- |
   | 超过 90%                            | A     |
   | 71% 到 90%                               | B     |
   | 51% 到 70%                               | C     |
   | 31% 到 50%                               | D     |
   | 11% 到 30%                               | E     |
   | 低于 10%                            | F     |

### N/A 评分

镜像也可能被分配 `N/A` 评分，这可能在以下情况下发生：

- 镜像大于 4GB（压缩大小）。
- 镜像架构不是 `linux/amd64` 或 `linux/arm64`。
- 镜像太旧，没有用于评估的新数据。

如果您看到 `N/A` 评分，请考虑以下事项：

- 如果镜像太大，请尝试减小镜像大小。
- 如果镜像具有不受支持的架构，请为支持的架构重新构建镜像。
- 如果镜像太旧，请推送新标签以触发新的评估。

### 策略权重

不同的策略类型具有不同的权重，这会影响在评估期间分配给镜像的评分，如下表所示。

| 策略类型                                                                                  | 分值 |
| -------------------------------------------------------------------------------------------- | ------ |
| [基于严重性的漏洞](/manuals/scout/policy/_index.md#severity-based-vulnerability) | 20     |
| [高关注度漏洞](/manuals/scout/policy/_index.md#high-profile-vulnerabilities) | 20     |
| [供应链证明](/manuals/scout/policy/_index.md#supply-chain-attestations)       | 15     |
| [批准的基准镜像](/manuals/scout/policy/_index.md#approved-base-images)                 | 15     |
| [最新的基准镜像](/manuals/scout/policy/_index.md#up-to-date-base-images)             | 10     |
| [SonarQube 质量门](/manuals/scout/policy/_index.md#sonarqube-quality-gates) \*        | 10     |
| [默认非 root 用户](/manuals/scout/policy/_index.md#default-non-root-user)               | 5      |
| [合规许可证](/manuals/scout/policy/_index.md#compliant-licenses)                     | 5      |

\* _此策略默认未启用，必须由用户配置。_

### 评估

健康评分在启用功能后推送到 Docker Hub 的新镜像上计算。健康评分帮助您维护高安全标准，并确保您的应用程序构建在安全可靠镜像之上。

### 仓库评分

除了单个镜像评分（每个标签或摘要）之外，每个仓库还根据最新推送的标签接收健康评分，提供仓库安全状况的整体视图。

### 示例

对于总可能评分为 100 分的镜像：

- 如果镜像仅偏离一个策略，价值 5 分，其评分为 100 分中的 95 分。由于此评分高于第 90 个百分位，镜像获得 A 健康评分。
- 如果镜像不符合更多策略，评分为 100 分中的 65 分，则获得 C 健康评分，反映其较低的合规性。

## 提高您的健康评分

要提高镜像的健康评分，请采取措施确保镜像符合 Docker Scout 推荐的[策略](./_index.md)。

1. 访问 [Docker Scout 仪表板](https://scout.docker.com/)。
2. 使用您的 Docker ID 登录。
3. 转到[仓库设置](https://scout.docker.com/settings/repos)并为您的 Docker Hub 镜像仓库启用 Docker Scout。
4. 分析您仓库的[策略合规性](./_index.md)，并采取措施确保您的镜像符合策略要求。

由于策略的权重不同，请优先考虑评分最高的策略，以对镜像的整体评分产生更大影响。