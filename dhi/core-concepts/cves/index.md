# 常见漏洞和暴露 (CVE)

## 什么是 CVE？

CVE 是指软件或硬件中公开披露的网络安全漏洞。每个 CVE 都被分配一个唯一的标识符（例如 CVE-2024-12345），并包含标准化的描述，使组织能够一致地跟踪和处理漏洞。

在 Docker 的背景下，CVE 通常涉及基础镜像或应用程序依赖项中的问题。这些漏洞的范围从轻微错误到严重的安全风险，例如远程代码执行或权限提升。

## 为什么 CVE 很重要？

定期扫描和更新 Docker 镜像以缓解 CVE 对于维护安全和合规的环境至关重要。忽略 CVE 可能会导致严重的安全漏洞，包括：

- **未经授权的访问**：漏洞利用可能使攻击者获得对系统的未经授权访问。
- **数据泄露**：敏感信息可能被暴露或窃取。
- **服务中断**：漏洞可能被利用来中断服务或导致停机。
- **合规性违规**：未能处理已知漏洞可能导致不符合行业法规和标准。

## Docker Hardened Images 如何帮助缓解 CVE

Docker Hardened Images (DHIs) 的设计旨在从一开始就最大限度地降低 CVE 风险。通过采用安全优先的方法，DHIs 在 CVE 缓解方面提供了几个优势：

- **减少攻击面**：DHIs 使用无发行版 (distroless) 方法构建，剥离了不必要的组件和软件包。镜像大小减少了高达 95%，限制了潜在漏洞的数量，使攻击者更难利用不需要的软件。
- **更快的 CVE 修复**：DHIs 由 Docker 以企业级 SLA 维护，持续更新以解决已知漏洞。关键和高严重性的 CVE 会迅速修补，确保您的容器在无需手动干预的情况下保持安全。
- **主动漏洞管理**：通过使用 DHIs，组织可以主动管理漏洞。这些镜像附带 CVE 和漏洞暴露 (VEX) 源，使团队能够及时了解潜在威胁并采取必要的行动。

## 扫描镜像以查找 CVE

定期扫描 Docker 镜像中的 CVE 对于维护安全的容器化环境至关重要。虽然 Docker Scout 集成在 Docker Desktop 和 Docker CLI 中，但 Grype 和 Trivy 等工具提供了替代的扫描功能。以下是使用每个工具扫描 Docker 镜像以查找 CVE 的说明。

### Docker Scout

Docker Scout 集成在 Docker Desktop 和 Docker CLI 中。它提供漏洞洞察、CVE 摘要以及指向修复指南的直接链接。

#### 使用 Docker Scout 扫描 DHI

要使用 Docker Scout 扫描 Docker Hardened Image，请运行以下命令：

```console
$ docker scout cves dhi.io/<image>:<tag> --platform <platform>
```

示例输出：

```plaintext
    v SBOM obtained from attestation, 101 packages found
    v Provenance obtained from attestation
    v VEX statements obtained from attestation
    v No vulnerable package detected
    ...
```

有关更详细的过滤和 JSON 输出，请参阅 [Docker Scout CLI 参考](../../../reference/cli/docker/scout/_index.md)。

### Grype

[Grype](https://github.com/anchore/grype) 是一个开源扫描器，可根据漏洞数据库（如 NVD 和发行版公告）检查容器镜像。

#### 使用 Grype 扫描 DHI

安装 Grype 后，您可以拉取镜像并运行扫描命令来扫描 Docker Hardened Image。Grype 要求您首先将 VEX 证明导出到文件：

```console
$ docker pull dhi.io/<image>:<tag>
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
$ grype dhi.io/<image>:<tag> --vex vex.json
```

示例输出：

```plaintext
NAME               INSTALLED              FIXED-IN     TYPE  VULNERABILITY     SEVERITY    EPSS%  RISK
libperl5.36        5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
perl               5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
perl-base          5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
...
```

### Trivy

[Trivy](https://github.com/aquasecurity/trivy) 是一个用于容器和其他工件的开源漏洞扫描器。它可以检测操作系统软件包和应用程序依赖项中的漏洞。

#### 使用 Trivy 扫描 DHI

安装 Trivy 后，您可以拉取镜像并运行扫描命令来扫描 Docker Hardened Image：

```console
$ docker pull dhi.io/<image>:<tag>
$ trivy image --scanners vuln --vex repo dhi.io/<image>:<tag>
```

示例输出：

```plaintext
Report Summary

┌──────────────────────────────────────────────────────────────────────────────┬────────────┬─────────────────┬─────────┐
│                                    Target                                    │    Type    │ Vulnerabilities │ Secrets │
├──────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ dhi.io/<image>:<tag> (debian 12.11)                                          │   debian   │       66        │    -    │
├──────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ opt/python-3.13.4/lib/python3.13/site-packages/pip-25.1.1.dist-info/METADATA │ python-pkg │        0        │    -    │
└──────────────────────────────────────────────────────────────────────────────┴────────────┴─────────────────┴─────────┘
```

## 使用 VEX 过滤已知的不可利用 CVE

Docker Hardened Images 包含签名的 [VEX (Vulnerability Exploitability eXchange，漏洞可利用性交换)](./vex.md) 证明，用于识别与镜像运行时行为无关的漏洞。

使用 Docker Scout 或 Trivy 时，这些 VEX 语句会自动应用，如前面的示例所示，无需手动配置。

要手动检索支持该功能的工具的 VEX 证明：

```console
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
```

> [!NOTE]
>
> `docker scout vex get` 命令需要 [Docker Scout CLI](https://github.com/docker/scout-cli/) 1.18.3 或更高版本。
>
> 如果镜像在您的设备上本地存在，您必须在镜像名称前加上 `registry://` 前缀。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

例如：

```console
$ docker scout vex get dhi.io/python:3.13 --output vex.json
```

这将创建一个包含指定镜像的 VEX 语句的 `vex.json` 文件。然后，您可以将此文件与支持 VEX 的工具一起使用，以过滤掉已知的不可利用的 CVE。
