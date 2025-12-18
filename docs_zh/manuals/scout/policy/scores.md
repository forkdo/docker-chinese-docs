---
title: Docker Scout 健康评分
description: |
  Docker Scout 健康评分为 Docker Hub 上的镜像提供供应链评估，根据多项安全策略对镜像进行 A 到 F 的评级。
keywords: scout, 健康评分, 评估, 检查, 评级, docker hub
---

{{< summary-bar feature_name="Docker Scout 健康评分" >}}

Docker Scout 健康评分为 Docker Hub 上的镜像提供安全评估和整体供应链健康状况，帮助您判断镜像是否符合既定的安全最佳实践。评分范围从 A 到 F，其中 A 代表最高安全级别，F 代表最低安全级别，让您一目了然地了解镜像的安全状况。

只有组织成员（且至少对仓库具有“读取”访问权限）才能查看健康评分。组织外部用户或没有“读取”权限的成员无法查看该评分。

## 查看健康评分

{{< tabs >}}
{{< tab name="Docker Hub" >}}

在 Docker Hub 中查看镜像健康评分的步骤：

1. 访问 Docker Hub 并登录。
2. 导航到您的组织页面。

在仓库列表中，您可以看到每个仓库的健康评分，该评分基于最新推送的标签。

![仓库健康评分](../images/score-badges-repolist.png)

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

在 Docker Desktop 中查看镜像健康评分的步骤：

1. 打开 Docker Desktop 并登录到您的 Docker 账户。
2. 导航到 **Images** 视图并选择 **Hub** 选项卡。

在仓库列表中，**Health** 列显示了已推送到 Docker Hub 的不同标签的评分。

![仓库健康评分](../images/score-badges-dd.png)

{{< /tab >}}
{{< /tabs >}}

健康评分徽章采用颜色编码，表示仓库的整体健康状况：

- **绿色**：评分为 A 或 B。
- **黄色**：评分为 C。
- **橙色**：评分为 D。
- **红色**：评分为 E 或 F。
- **灰色**：评分为 `N/A`。

评分也会显示在 Docker Hub 上特定仓库的页面上，同时列出影响评分的各个策略。

![Scout "A" 健康评分](../images/score-a-shiny.png?w=450px)

## 评分系统

健康评分通过评估镜像是否符合 Docker Scout [策略](./_index.md) 来确定。这些策略与软件供应链的最佳实践保持一致。

如果您的镜像仓库已注册 Docker Scout，健康评分将根据组织中启用的策略自动计算（包括您配置的任何自定义策略）。

如果您未使用 Docker Scout，健康评分将显示镜像与默认策略的合规性。默认策略是一组由 Docker 推荐的供应链规则，作为镜像的基础标准。您可以为组织启用 Docker Scout 并编辑策略配置，以根据特定策略获得更相关的健康评分。

### 评分流程

每个策略根据其 [类型](/manuals/scout/policy/_index.md#policy-types) 分配相应的分数值。如果镜像符合某策略，则授予该策略类型的分数值。镜像的健康评分基于获得的分数占总分的百分比计算：

1. 评估镜像的策略合规性。
2. 根据策略合规性授予分数。
3. 计算获得的分数百分比：

   ```text
   百分比 = (获得的分数 / 总分) * 100
   ```

4. 根据获得的分数百分比分配最终评分，如下表所示：

   | 分数百分比（获得分数占总分） | 评分 |
   | ---------------------------- | ---- |
   | 超过 90%                     | A    |
   | 71% 到 90%                   | B    |
   | 51% 到 70%                   | C    |
   | 31% 到 50%                   | D    |
   | 11% 到 30%                   | E    |
   | 低于 10%                     | F    |

### N/A 评分

镜像也可能被分配 `N/A` 评分，这可能发生在以下情况：

- 镜像大小超过 4GB（压缩后大小）。
- 镜像架构不是 `linux/amd64` 或 `linux/arm64`。
- 镜像过旧，没有新鲜数据用于评估。

如果您看到 `N/A` 评分，请考虑以下情况：

- 如果镜像过大，请尝试减小镜像大小。
- 如果镜像架构不受支持，请为支持的架构重新构建镜像。
- 如果镜像过旧，请推送新标签以触发新鲜评估。

### 策略权重

不同策略类型具有不同的权重，这会影响评估时分配给镜像的评分，如下表所示。

| 策略类型                                                                                         | 分数 |
| ------------------------------------------------------------------------------------------------ | ---- |
| [基于严重性的漏洞](/manuals/scout/policy/_index.md#severity-based-vulnerability)                | 20   |
| [高知名度漏洞](/manuals/scout/policy/_index.md#high-profile-vulnerabilities)                    | 20   |
| [供应链证明](/manuals/scout/policy/_index.md#supply-chain-attestations)                          | 15   |
| [已批准的基础镜像](/manuals/scout/policy/_index.md#approved-base-images)                         | 15   |
| [最新的基础镜像](/manuals/scout/policy/_index.md#up-to-date-base-images)                          | 10   |
| [SonarQube 质量门禁](/manuals/scout/policy/_index.md#sonarqube-quality-gates) \*                 | 10   |
| [默认非 root 用户](/manuals/scout/policy/_index.md#default-non-root-user)                        | 5    |
| [合规许可证](/manuals/scout/policy/_index.md#compliant-licenses)                                 | 5    |

\* _此策略默认未启用，必须由用户配置。_

### 评估

启用功能后，新推送到 Docker Hub 的镜像将计算健康评分。健康评分帮助您保持高标准的安全性，并确保您的应用程序构建在安全可靠的镜像之上。

### 仓库评分

除了单个镜像评分（按标签或摘要），每个仓库还会根据最新推送的标签获得健康评分，提供仓库安全状态的整体视图。

### 示例

对于总分可能为 100 分的镜像：

- 如果镜像仅偏离一个价值 5 分的策略，其评分为 95 分（满分 100 分）。由于此评分高于 90%，镜像获得 A 健康评分。
- 如果镜像不符合更多策略，评分为 65 分（满分 100 分），则获得 C 健康评分，反映其较低的合规性。

## 改善健康评分

要改善镜像的健康评分，请采取措施确保镜像符合 Docker Scout 推荐的 [策略](./_index.md)。

1. 访问 [Docker Scout 仪表板](https://scout.docker.com/)。
2. 使用您的 Docker ID 登录。
3. 进入 [仓库设置](https://scout.docker.com/settings/repos) 并为您的 Docker Hub 镜像仓库启用 Docker Scout。
4. 分析仓库的 [策略合规性](./_index.md)，并采取行动确保镜像符合策略。

由于策略权重不同，请优先处理分数最高的策略，以对镜像的整体评分产生更大影响。