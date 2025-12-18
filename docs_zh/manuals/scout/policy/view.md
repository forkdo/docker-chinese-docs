---
title: 查看 Docker Scout 策略状态
description: |
  Docker Scout 仪表板和 `docker scout policy` 命令可让您查看镜像的策略状态。
keywords: scout, policy, status, vulnerabilities, supply chain, cves, licenses
---

您可以通过 [Docker Scout 仪表板](#dashboard) 或使用 [CLI](#cli) 来跟踪制品的策略状态。

## 仪表板

[Docker Scout Dashboard](https://scout.docker.com/) 的 **概览** 选项卡会显示您仓库最近策略变化的摘要。
此摘要展示了在最新镜像与前一个镜像之间，策略评估变化最大的那些镜像。

![策略概览](../images/policy-overview.webp)

### 仓库的策略状态

**镜像** 选项卡会显示所选环境中所有镜像的当前策略状态以及最近的策略趋势。列表中的 **策略状态** 列显示：

- 已满足的策略数量与总策略数量
- 最近的策略趋势

![镜像列表中的策略状态](../images/policy-image-list.webp)

策略趋势用方向箭头表示，指示与同一环境中前一个镜像相比，当前镜像在策略方面是变好、变差还是没有变化。

- 向上的绿色箭头显示最新推送的镜像中变好的策略数量
- 向下的红色箭头显示最新推送的镜像中变差的策略数量
- 双向的灰色箭头显示最新版本镜像中未发生变化的策略数量

如果您选择一个仓库，可以打开 **策略** 选项卡，查看最近一次分析的镜像与其前一个镜像之间详细的策略差异。

### 详细结果与修复建议

要在仪表板中查看镜像的完整评估结果，请导航到镜像标签页面并打开 **策略** 选项卡。这会显示当前镜像所有策略违规的详细分解。

![详细的策略评估结果](../images/policy-detailed-results.webp)

此视图还提供如何改进违规策略状态的建议。

![标签视图中的策略详情](../images/policy-tag-view.webp)

对于与漏洞相关的策略，策略详情视图会显示能够消除该漏洞的修复版本（如果可用）。要解决此问题，请将软件包版本升级到修复版本。

对于与许可证相关的策略，列表会显示所有许可证不符合策略标准的软件包。要解决此问题，请找到移除违规软件包依赖的方法，例如寻找一个以更合适许可证分发的替代软件包。

## CLI

要从 CLI 查看镜像的策略状态，请使用 `docker scout policy` 命令。

```console
$ docker scout policy \
  --org dockerscoutpolicy \
  --platform linux/amd64 \
  dockerscoutpolicy/email-api-service:0.0.2

    ✓ Pulled
    ✓ Policy evaluation results found


​## 概览
​
​             │               Analyzed Image
​─────────────┼──────────────────────────────────────────────
​  Target     │  dockerscoutpolicy/email-api-service:0.0.2
​    digest   │  17b1fde0329c
​    platform │ linux/amd64
​
​
​## 策略
​
​策略状态  FAILED  (2/8 policies met, 3 missing data)
​
​  状态 │                  策略                             │           结果
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

有关该命令的更多信息，请参考 [CLI 参考文档](/reference/cli/docker/scout/policy.md)。