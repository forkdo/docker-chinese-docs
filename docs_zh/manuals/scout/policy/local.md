---
title: 评估策略
description: 使用 CLI 通过内置和自定义 Rego 策略评估 Docker Scout 策略
keywords: scout, policy, rego, opa, cli, custom policies, policy bundle
---

{{< summary-bar feature_name="Evaluate policies" >}}

`docker scout policy` 允许您使用 CLI 针对可配置的策略集评估镜像。您可以使用内置默认值，调整阈值以
匹配您的需求，或者使用
[Rego](https://www.openpolicyagent.org/docs/latest/policy-language/) 编写自定义策略。

## 工作原理

当您运行 `docker scout policy` 时，CLI 会将镜像索引为 SBOM，
用 CVE 和 VEX 数据丰富它，然后就地评估每个配置的策略。
不会向 Scout 服务发送任何数据，并且在大多数用例中
不需要组织。

策略来自三个可以组合的来源：

- 内置默认值：嵌入在 CLI 中的精选集合，在未提供其他来源时使用。
- OCI 策略包：Rego 打包为 OCI 制品，使用 `--policy-bundle`
  从注册表拉取。
- 本地 `.rego` 文件：使用 `--policy-file` 或 `--policy-dir`
  来编写和迭代自定义策略。

## 从仪表板中的策略评估迁移

如果您使用过 Docker Scout 仪表板中的策略页面，`docker scout
policy` 提供了与 CLI 中相同的功能。内置策略是同一组。要评估镜像：

```console
$ docker scout policy <image>
```

如果您在仪表板中自定义了策略，例如调整了严重性阈值
或禁用了某些策略，可以使用 `--policy-config` 文件
复制这些设置。请参阅 [配置内置策略](#configure-built-in-policies)。

### 在 CI 中使用

使用 [Docker Scout GitHub Action](https://github.com/marketplace/actions/docker-scout)
在工作流中将策略作为评估的一部分：

```yaml
- name: Evaluate policies
  uses: docker/scout-action@v1
  with:
    command: policy
    image: ${{ env.IMAGE_NAME }}
    organization: <ORG>
```

对于其他 CI 平台，请在您的 runner 上安装
[Docker Scout CLI 插件](/manuals/scout/install.md) 并运行
`docker scout policy <image> --exit-code`。

### 将 GitHub Action 从基于仪表板的策略评估迁移

Docker Scout GitHub Action 现在支持与 `docker scout policy`
相同的本地策略配置标志。如果您将 `compare --exit-on policy`
与基于仪表板的策略设置配合使用，请使用 `--policy-config`
在本地复制这些设置：

```yaml
- uses: docker/scout-action@v1.23.0
  with:
    command: compare
    image: ${{ env.IMAGE_NAME }}
    to-env: production
    exit-on: policy
    policy-config: policies.json
    organization: <ORG>
```

`policy-config` 文件格式请参阅
[配置内置策略](#configure-built-in-policies)。

## 示例

针对内置策略集评估镜像：

```console
$ docker scout policy myorg/app:latest
```

使用 `--exit-code` 在任意策略未满足时使流水线失败：

```console
$ docker scout policy myorg/app:latest --exit-code
```

要自定义运行哪些策略及其阈值，请传入策略配置文件：

```console
$ docker scout policy myorg/app:latest --policy-config policies.json
```

策略结果也会由 `docker scout quickview` 和
`docker scout compare` 显示，它们接受相同的 `--policy-file`、
`--policy-dir`、`--policy-bundle` 和 `--policy-config` 标志。

其他有用的标志：

```console
# 评估多平台镜像的特定平台
$ docker scout policy myorg/app:latest --platform linux/arm64

# 仅显示特定策略的结果
$ docker scout policy myorg/app:latest --only-policy "No copyleft licenses"

# 将报告写入文件
$ docker scout policy myorg/app:latest --output report.txt
```

## 内置策略

默认提供以下策略：

| 策略 | 检查内容 |
| --- | --- |
| No fixable critical or high vulnerabilities | 有修复可用的严重/高危 CVE |
| No high-profile vulnerabilities | 精选的知名 CVE 列表（Log4Shell、XZ 后门等） |
| No copyleft licenses | 使用 AGPL、GPL、LGPL、MPL 等类似许可证的软件包 |
| No outdated base images | 基础镜像落后于其标签的最新摘要 |
| Supply chain attestations | 附带来源和 SBOM 证明 |
| Default non-root user | 镜像配置为以非 root 用户身份运行 |
| No unapproved base images | 基础镜像与可配置的允许列表匹配 |

## 配置内置策略

JSON 策略配置文件控制运行哪些策略及其阈值。
使用 `--policy-config` 传入。

```json
{
  "policies": [
    {
      "name": "fixable-vulnerabilities",
      "config": {
        "severities": ["CRITICAL"],
        "grace_period_days": 14
      }
    },
    {
      "name": "no-stale-base-images",
      "enabled": false
    }
  ]
}
```

- `policies[].name`：策略的稳定 ID（见下表）。
- `policies[].enabled`：设为 `false` 可跳过该策略。未列出的策略默认启用。
- `policies[].config`：作为 `data.config` 传递给策略的对象。

### 配置参考

下表列出了每个内置策略的可配置键。

| 策略（稳定 ID） | config 键 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `fixable-vulnerabilities` | `severities` | `["CRITICAL","HIGH"]` | 计为违规的严重级别 |
| `fixable-vulnerabilities` | `fixable_only` | `true` | 为 `true` 时，仅统计有已知修复的漏洞 |
| `fixable-vulnerabilities` | `package_types` | `[]` | 考虑的白名单 PURL 软件包类型；为空表示全部 |
| `fixable-vulnerabilities` | `grace_period_days` | `0` | 新披露的 CVE 豁免天数 |
| `high-profile-vulnerabilities` | `cves` | [默认高调 CVE](#default-high-profile-cves) | 视为高调的 CVE ID |
| `high-profile-vulnerabilities` | `ignored_cves` | `[]` | 排除在导致失败之外的 CVE ID |
| `high-profile-vulnerabilities` | `include_cisa_kev` | `true` | 同时标记 CISA KEV 目录中的漏洞 |
| `copyleft-license` | `licenses` | AGPL/GPL/LGPL/MPL/… | 视为著佐权的 SPDX 许可证 ID |
| `copyleft-license` | `ignored_packages` | `[]` | 豁免检查的软件包 URL |
| `approved-base-images` | `allowed_base_images` | `["*"]` | 允许的基础镜像引用的 glob 模式 |
| `approved-base-images` | `allowed_distros_only` | `true` | 启用时，基础镜像必须使用允许的 OS 发行版 |
| `approved-base-images` | `allowed_distros` | 精选列表 | 视为允许的 OS 发行版 |
| `supply-chain-attestations` | `required_attestations` | 来源和 SBOM 谓词类型 | 必须存在的证明谓词类型 |

#### 默认高调 CVE

内置的 `cves` 列表包含以下 CVE。随着新的高调漏洞被披露，Docker 会更新此列表。

| CVE ID | 通用名 |
| --- | --- |
| CVE-2014-0160 | Heartbleed |
| CVE-2014-6271 | Shellshock |
| CVE-2021-44228 | Log4Shell |
| CVE-2021-45046 | Log4j 后续 |
| CVE-2022-22965 | Spring4Shell |
| CVE-2023-38545 | curl SOCKS5 堆溢出 |
| CVE-2023-44487 | HTTP/2 Rapid Reset |
| CVE-2024-3094 | XZ Utils 后门 |

要覆盖该列表，请在策略配置文件中设置 `cves`：

```json
{
  "policies": [
    {
      "name": "high-profile-vulnerabilities",
      "config": {
        "cves": ["CVE-2021-44228", "CVE-2024-3094"]
      }
    }
  ]
}
```

## 编写自定义策略

策略是 `docker.scout` 包中的 Rego 模块。策略声明一个
布尔 `pass` 规则和一个 `violation` 集合。对单个文件使用 `--policy-file`，
或使用 `--policy-dir` 递归加载目录。

```rego
# METADATA
# title: No packages from internal registry
# description: Flags packages sourced from registry.internal.example.com.
# custom:
#   name: no-internal-registry
#   result_type: generic
#   weight: 5
#   not_compliant_title: Packages from internal registry found
#   details_order:
#   - purl
#   - reason
package docker.scout

import rego.v1

default pass := false

pass if {
    count(violation) == 0
}

violation contains v if {
    att := oci.referrer("https://scout.docker.com/sbom/v0.1")
    some pkg in att.statement.predicate.artifacts
    contains(pkg.purl, "registry.internal.example.com")
    v := {
        "message": sprintf("Package %s sourced from internal registry", [pkg.purl]),
        "detail": {
            "purl": pkg.purl,
            "reason": "matches registry.internal.example.com",
        },
    }
}
```

```console
# 单个文件
$ docker scout policy myorg/app:latest --policy-file ./no-internal-registry.rego

# 策略目录
$ docker scout policy myorg/app:latest --policy-dir ./rego

# 自定义策略与配置文件结合
$ docker scout policy myorg/app:latest \
  --policy-dir ./rego \
  --policy-config ./policies.json
```

`--policy-file` 和 `--policy-dir` 都可重复使用。当提供其中任一选项时，
内置默认值不会自动加载。要同时运行内置和自定义策略，
请使用 `docker scout policy publish` 将内置集合发布到注册表，
然后使用 `--policy-bundle` 传入两个包：

```console
$ docker scout policy myorg/app:latest \
  --policy-bundle registry.example.com/default-policies:latest \
  --policy-bundle registry.example.com/dhi-policies:latest \
  --policy-file ./custom.rego
```

`--policy-bundle` 可重复使用，因此您可以根据需要组合任意数量的包，
以及本地策略文件。

### 元数据注解

CLI 读取 [OPA 元数据注解](https://www.openpolicyagent.org/docs/latest/annotations/)
以渲染结果。将其放在 `package` 声明正上方的 `# METADATA` 块中。

| 注解 | 用途 |
| --- | --- |
| `title` | 报告中显示的可读策略名称 |
| `description` | 更长的说明 |
| `custom.name` | 用于匹配 `--policy-config` 条目的稳定 ID。若省略则默认为包路径 |
| `custom.result_type` | 违规的渲染方式：`vulnerability`、`license`、`boolean` 或 `generic`（默认） |
| `custom.weight` | 权重越高，在报告中排序越靠前 |
| `custom.not_compliant_title` | 策略失败时显示的状态标签 |
| `custom.details_order` | 要作为列显示的 `detail` 键的有序列表 |

### 输出契约

- `pass`：策略满足时为 `true`。标准形式为 `pass if { count(violation) == 0 }`。
- `violation`：一个对象集合。每个对象应有一个 `message` 字符串和
  一个 `detail` 对象，其键与 `custom.details_order` 匹配。可选的
  `remediation` 字符串会作为修复指导显示。

### 输入和内置函数

评估输入是丰富后的 SBOM。关键入口点：

- `input.source.image`：镜像元数据，包括 `input.source.image.config.config.User`、
  `input.source.image.name` 和 `input.source.image.digest`。
- `data.config`：来自策略配置文件的每个策略的 `config` 对象。

策略 Rego 中提供以下内置函数：

| 函数 | 说明 |
| --- | --- |
| `oci.referrer(predicateType)` | 按谓词类型检索证明 |
| `oci.canonical_name(ref)` | 规范化镜像引用，例如 `"node:25"` 到 `"docker.io/library/node"` |
| `oci.image_digest(ref)` | 从注册表解析标签的当前摘要 |
| `oci.index(ref, digest)` | 获取镜像的 OCI 镜像索引 |
| `oci.referrer_index(ref, digest)` | 获取镜像的 OCI referrer 索引 |
| `oci.referrer_by_digest(ref, digest)` | 按摘要获取镜像的 referrer |
| `scout.parse_purl(purl)` | 将 PURL 解析为其组成部分 |
| `scout.package_provenance(purl)` | 来自 SBOM 的软件包来源 |
| `scout.vulnerabilities(purls)` | 给定 PURL 的漏洞 |
| `scout.package_recommendation(purl)` | 软件包的推荐（修复）版本 |
| `scout.base_image()` | SBOM 中记录的基础镜像匹配 |
| `cosign.verify_dsse(envelope, opts)` | 验证 in-toto DSSE 信封的 cosign 签名 |
| `cosign.verify_image(ref, opts)` | 验证镜像的 cosign 签名 |
| `gpg.verify_commit(...)` | 验证分离的提交签名 |

`oci.referrer` 的常用谓词类型：

| 谓词类型 | 内容 |
| --- | --- |
| `https://scout.docker.com/vulnerabilities/v0.1` | 每个软件包的 CVE |
| `https://scout.docker.com/sbom/v0.1` | SBOM 制品，包含 `purl` 和 `licenses` |
| `https://scout.docker.com/provenance/v0.1` | 构建来源，包括 `base_image` |
| `https://openvex.dev/ns/v0.2.0` | VEX 声明 |

## 调试策略

在 Rego 中添加 `print()` 语句，并通过在策略配置文件中设置
`"debug": true` 启用调试输出：

```rego
violation contains v if {
    att := oci.referrer("https://scout.docker.com/sbom/v0.1")
    some pkg in att.statement.predicate.artifacts
    print("checking", pkg.purl)
    contains(pkg.purl, blocked)
    # ...
}
```

```json
{
  "debug": true,
  "policies": [
    { "name": "no-internal-registry" }
  ]
}
```

输出以策略名称和源行作为前缀：

```text
no-internal-registry#28: checking pkg:deb/debian/curl@7.88.1
```

> [!NOTE]
>
> 策略配置中的 `debug` 字段控制来自您的 Rego 的 `print()` 输出。
> 全局 `--debug` 标志是分开的：它启用 CLI 级别的调试日志，
> 用于包加载、注册表解析以及类似的底层操作。

### 检查原始评估结果

使用 `--result-file` 将每个策略的完整评估结果写入
JSON 文件。这在迭代自定义策略以检查中间值时很有用。

```console
$ docker scout policy myorg/app:latest \
  --policy-file ./no-internal-registry.rego \
  --result-file result.json
```

输出中的每个条目包含：

- `pass`：策略的布尔结果。
- `violations`：每个报告的违规的 `detail` 对象。
- `bindings`：原始 `data.docker.scout` 文档，包括 `violation`
  集合和任何其他完整规则，用于检查中间值。
- `metrics`：OPA 评估指标（计时器和计数器）。

```json
{
  "no-internal-registry": {
    "pass": false,
    "violations": [
      { "purl": "pkg:deb/debian/curl@7.88.1", "reason": "matches \"registry.internal.example.com\"" }
    ],
    "bindings": {
      "blocked": "registry.internal.example.com",
      "violation": [
        {
          "message": "Package pkg:deb/debian/curl@7.88.1 sourced from internal registry",
          "detail": {
            "purl": "pkg:deb/debian/curl@7.88.1",
            "reason": "matches \"registry.internal.example.com\""
          }
        }
      ]
    },
    "metrics": {
      "timer_rego_query_eval_ns": 1234567
    }
  }
}
```

## 将策略作为 OCI 包共享

将 `.rego` 文件打包为 OCI 制品，并通过任何注册表分发。

### 发布包

```console
# 发布策略目录
$ docker scout policy publish \
  --policy-dir ./rego \
  registry.example.com/my-policies:latest

# 发布特定文件
$ docker scout policy publish \
  --policy-file fixable.rego \
  --policy-file licenses.rego \
  registry.example.com/my-policies:latest

# 发布内置默认集合
$ docker scout policy publish registry.example.com/my-policies:latest
```

每个模块的元数据在发布前进行验证。命令会打印
生成的摘要以及已打包的策略列表。

### 使用包

```console
$ docker scout policy myorg/app:latest \
  --policy-bundle registry.example.com/my-policies:latest

# 将包与本地文件和配置结合
$ docker scout policy myorg/app:latest \
  --policy-bundle registry.example.com/my-policies:latest \
  --policy-file ./extra.rego \
  --policy-config ./policies.json
```

`--policy-bundle` 可重复使用。认证使用您现有的 Docker
注册表凭据。包按摘要缓存，因此针对同一包重新运行不会
重新下载。新的摘要（例如，在重新发布 `:latest` 之后）会自动获取。
