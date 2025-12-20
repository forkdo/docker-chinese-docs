# 查看 Docker Scout 策略状态

您可以从 [Docker Scout 仪表板](#dashboard) 或使用 [CLI](#cli) 跟踪制品的策略状态。

## 仪表板

[Docker Scout 仪表板](https://scout.docker.com/) 的 **Overview** 选项卡显示了仓库策略的近期变更摘要。此摘要展示了在最新镜像与上一镜像之间，策略评估变化最大的镜像。

![策略概览](../images/policy-overview.webp)

### 每个仓库的策略状态

**Images** 选项卡显示所选环境中所有镜像的当前策略状态和近期策略趋势。列表中的 **Policy status** 列显示：

- 已满足的策略数量与策略总数之比
- 近期策略趋势

![镜像列表中的策略状态](../images/policy-image-list.webp)

策略趋势由方向箭头表示，指示与同一环境中的上一镜像相比，当前镜像的策略是变好、变差还是保持不变。

- 向上绿色箭头显示在最新推送的镜像中变好的策略数量。
- 向下红色箭头显示在最新推送的镜像中变差的策略数量。
- 双向灰色箭头显示在最新版本镜像中保持不变的策略数量。

如果选择某个仓库，可以打开 **Policy** 选项卡，查看最新分析镜像与其前一镜像的策略差异的详细描述。

### 详细结果和修复方法

要查看镜像的完整评估结果，请在 Docker Scout 仪表板中导航到镜像标签并打开 **Policy** 选项卡。这将显示当前镜像所有策略违规的细分。

![详细的策略评估结果](../images/policy-detailed-results.webp)

此视图还提供了如何改进违规策略状态的建议。

![标签视图中的策略详情](../images/policy-tag-view.webp)

对于与漏洞相关的策略，策略详情视图会在修复版本可用时显示消除漏洞的修复版本。要修复问题，请将软件包版本升级到修复版本。

对于与许可相关的策略，列表会显示所有许可证不符合策略标准的软件包。要修复问题，请设法移除对违规软件包的依赖，例如寻找在更合适许可下分发的替代软件包。

## CLI

要从 CLI 查看镜像的策略状态，请使用 `docker scout policy` 命令。

```console
$ docker scout policy \
  --org dockerscoutpolicy \
  --platform linux/amd64 \
  dockerscoutpolicy/email-api-service:0.0.2

    ✓ Pulled
    ✓ Policy evaluation results found


​## Overview
​
​             │               Analyzed Image
​─────────────┼──────────────────────────────────────────────
​  Target     │  dockerscoutpolicy/email-api-service:0.0.2
​    digest   │  17b1fde0329c
​    platform │ linux/amd64
​
​
​## Policies
​
​Policy status  FAILED  (2/8 policies met, 3 missing data)
​
​  Status │                  Policy                             │           Results
​─────────┼─────────────────────────────────────────────────────┼──────────────────────────────
​  ✓      │ No copyleft licenses                                │    0 packages
​  !      │ Default non-root user                               │
​  !      │ No fixable critical or high vulnerabilities         │    2C     1H     0M     0L
​  ✓      │ No high-profile vulnerabilities                     │    0C     0H     0M     0L
​  ?      │ No outdated base images                             │    No data
​         │                                                     │    Learn more ↗
​  ?      │ SonarQube quality gates passed                      │    No data
​         │                                                     │    Learn more ↗
​  !      │ Supply chain attestations                           │    2 deviations
​  ?      │ No unapproved base images                           │    No data

...
```

有关该命令的更多信息，请参阅 [CLI 参考](/reference/cli/docker/scout/policy.md)。
