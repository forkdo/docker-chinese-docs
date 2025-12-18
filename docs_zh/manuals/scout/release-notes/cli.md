---
title: Docker Scout CLI 发布说明
linkTitle: CLI 发布说明
description: 了解 Docker Scout CLI 插件的最新功能
keywords: docker scout, 发布说明, 更新日志, cli, 功能, 变更, delta, 新版本, github actions
---

本文档包含 Docker Scout [CLI 插件](https://github.com/docker/scout-cli/) 和 `docker/scout-action` [GitHub Action](https://github.com/docker/scout-action/) 的最新功能、改进、已知问题和错误修复信息。

## 1.18.4

{{< release-date date="2025-10-02" >}}

### 错误修复

- VEX 和 SPDX 修复。

## 1.18.3

{{< release-date date="2025-08-13" >}}

### 新增

- 添加 `docker scout vex get` 命令，用于从所有 VEX 证明中检索合并的 VEX 文档。

### 错误修复

- Docker Hardened Images (DHI) 的小修复。

## 1.18.2

{{< release-date date="2025-07-21" >}}

### 新增

- 为 `docker scout attest get` 添加 `--skip-tlog` 标志，跳过对透明日志的签名验证。

### 增强

- 为 DHI FIPS 和 STIG 证明添加谓词类型的人类可读名称。

### 错误修复

- 不过滤被 VEX `under_investigation` 语句标记的 CVE。
- Docker Hardened Images (DHI) 的小修复。

## 1.18.1

{{< release-date date="2025-05-26" >}}

### 错误修复

- 修复 `docker scout attest list` 和 `docker scout attest get` 对本地镜像的问题。

## 1.18.0

{{< release-date date="2025-05-13" >}}

### 新增

- 添加 `docker scout attest list` 和 `docker scout attest get` 命令以列出证明。
- 添加对 Docker Hardened Images (DHI) VEX 文档的支持。

## 1.16.1

{{< release-date date="2024-12-13" >}}

### 错误修复

- 修复 `docker scout attestation add` 命令的 in-toto 主题摘要问题。

## 1.16.0

{{< release-date date="2024-12-12" >}}

### 新增

- 在 `docker scout sbom` 命令中添加秘密扫描功能。
- 添加对 Tanzu Application Catalog 镜像的证明支持。

### 增强

- 使用 SPDX 许可证列表规范化许可证。
- 使许可证唯一。
- 在 Markdown 输出中打印平台。
- 保留原始模式以查找嵌套匹配项。
- 更新以使 SPDX 输出符合规范。
- 更新 Go、crypto 模块和 Alpine 依赖项。

### 错误修复

- 修复 `docker scout attest` 命令中多个镜像的行为。
- 在创建临时文件之前检查目录是否存在。

## 1.15.0

{{< release-date date="2024-10-31" >}}

### 新增

- 为 `docker scout sbom` 命令添加新的 `--format=cyclonedx` 标志，以 CycloneDX 格式输出 SBOM。

### 增强

- 对 CVE 摘要使用从高到低的排序。
- 支持启用和禁用由 `docker scout push` 或 `docker scout watch` 启用的仓库。

### 错误修复

- 改进分析没有证明的 `oci` 目录时的消息。仅支持单平台镜像和带证明的多平台镜像。不支持没有证明的多平台镜像。
- 改进分类器和 SBOM 索引器：
  - 添加 Liquibase `lpm` 分类器。
  - 添加 Rakudo Star/MoarVM 二进制分类器。
  - 添加 silverpeas 工具的二进制分类器。
- 改进使用 containerd 镜像存储读取和缓存证明的功能。

## 1.14.0

{{< release-date date="2024-09-24" >}}

### 新增

- 在 `docker scout cves` 命令中添加 CVE 级别的抑制信息。

### 错误修复

- 修复列出悬空镜像的 CVE，例如：`local://sha256:...`
- 修复分析文件系统输入时的崩溃，例如使用 `docker scout cves fs://.`

## 1.13.0

{{< release-date date="2024-08-05" >}}

### 新增

- 为 `docker scout quickview`、`docker scout policy` 和 `docker scout compare` 命令添加 `--only-policy` 过滤选项。
- 为 `docker scout cves` 和 `docker scout quickview` 命令添加 `--ignore-suppressed` 过滤选项，以过滤受[异常](/scout/explore/exceptions/)影响的 CVE。

### 错误修复和增强

- 在检查中使用条件策略名称。
- 添加对检测使用链接器标志设置的 Go 项目版本的支持，例如：

  ```console
  $ go build -ldflags "-X main.Version=1.2.3"
  ```

## 1.12.0

{{< release-date date="2024-07-31" >}}

### 新增

- 仅显示来自基础镜像的漏洞：

  ```console {title="CLI"}
  $ docker scout cves --only-base IMAGE
  ```

  ```yaml {title="GitHub Action"}
  uses: docker/scout-action@v1
  with:
    command: cves
    image: [IMAGE]
    only-base: true
  ```

- 在 `quickview` 命令中考虑 VEX。

  ```console {title="CLI"}
  $ docker scout quickview IMAGE --only-vex-affected --vex-location ./path/to/my.vex.json
  ```

  ```yaml {title="GitHub Action"}
  uses: docker/scout-action@v1
  with:
    command: quickview
    image: [IMAGE]
    only-vex-affected: true
    vex-location: ./path/to/my.vex.json
  ```

- 在 `cves` 命令中考虑 VEX（GitHub Actions）。

  ```yaml {title="GitHub Action"}
  uses: docker/scout-action@v1
  with:
    command: cves
    image: [IMAGE]
    only-vex-affected: true
    vex-location: ./path/to/my.vex.json
  ```

### 错误修复和增强

- 更新 `github.com/docker/docker` 到 `v26.1.5+incompatible` 以修复 CVE-2024-41110。
- 更新 Syft 到 1.10.0。

## 1.11.0

{{< release-date date="2024-07-25" >}}

### 新增

- 过滤 CISA 已知被利用漏洞目录中的 CVE。

  ```console {title="CLI"}
  $ docker scout cves [IMAGE] --only-cisa-kev

  ... (cropped output) ...
  ## Packages and Vulnerabilities

  0C     1H     0M     0L  io.netty/netty-codec-http2 4.1.97.Final
  pkg:maven/io.netty/netty-codec-http2@4.1.97.Final

  ✗ HIGH CVE-2023-44487  CISA KEV  [OWASP Top Ten 2017 Category A9 - Using Components with Known Vulnerabilities]
    https://scout.docker.com/v/CVE-2023-44487
    Affected range  : <4.1.100
    Fixed version   : 4.1.100.Final
    CVSS Score      : 7.5
    CVSS Vector     : CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H
  ... (cropped output) ...
  ```

  ```yaml {title="GitHub Action"}
  uses: docker/scout-action@v1
  with:
    command: cves
    image: [IMAGE]
    only-cisa-kev: true
  ```

- 添加新分类器：
  - `spiped`
  - `swift`
  - `eclipse-mosquitto`
  - `znc`

### 错误修复和增强

- 允许在没有子组件时进行 VEX 匹配。
- 修复附加无效 VEX 文档时的崩溃。
- 修复 SPDX 文档根。
- 修复镜像使用 SCRATCH 作为基础镜像时的基础镜像检测。

## 1.10.0

{{< release-date date="2024-06-26" >}}

### 错误修复和增强

- 添加新分类器：
  - `irssi`
  - `Backdrop`
  - `CrateDB CLI (Crash)`
  - `monica`
  - `Openliberty`
  - `dumb-init`
  - `friendica`
  - `redmine`
- 修复包的空白字符发起者破坏 BuildKit 导出器的问题
- 修复带有摘要的镜像的 SPDX 语句中镜像引用的解析
- 支持图像比较的 `sbom://` 前缀：

  ```console {title="CLI"}
  $ docker scout compare sbom://image1.json --to sbom://image2.json
  ```

  ```yaml {title="GitHub Action"}
  uses: docker/scout-action@v1
  with:
    command: compare
    image: sbom://image1.json
    to: sbom://image2.json
  ```

## 1.9.3

{{< release-date date="2024-05-28" >}}

### 错误修复

- 修复检索缓存 SBOM 时的崩溃。

## 1.9.1

{{< release-date date="2024-05-27" >}}

### 新增

- 在 `docker scout cves` 命令中使用 `--format gitlab` 支持 [GitLab 容器扫描文件格式](https://docs.gitlab.com/ee/development/integrations/secure.html#container-scanning)。

  以下是一个示例流水线：

  ```yaml
     docker-build:
    # 使用官方 docker 镜像。
    image: docker:cli
    stage: build
    services:
      - docker:dind
    variables:
      DOCKER_IMAGE_NAME: $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG
    before_script:
      - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY

      # 安装 curl 和 Docker Scout CLI
      - |
        apk add --update curl
        curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
        apk del curl
        rm -rf /var/cache/apk/*
      # Docker Scout CLI 需要登录 Docker Hub
      - echo "$DOCKER_HUB_PAT" | docker login --username "$DOCKER_HUB_USER" --password-stdin

    # 所有分支都使用 $DOCKER_IMAGE_NAME 标记（默认为提交引用分支）
    # 默认分支也使用 `latest` 标记
    script:
      - docker buildx b --pull -t "$DOCKER_IMAGE_NAME" .
      - docker scout cves "$DOCKER_IMAGE_NAME" --format gitlab --output gl-container-scanning-report.json
      - docker push "$DOCKER_IMAGE_NAME"
      - |
        if [[ "$CI_COMMIT_BRANCH" == "$CI_DEFAULT_BRANCH" ]]; then
          docker tag "$DOCKER_IMAGE_NAME" "$CI_REGISTRY_IMAGE:latest"
          docker push "$CI_REGISTRY_IMAGE:latest"
        fi
    # 在存在 Dockerfile 的分支中运行此作业
    rules:
      - if: $CI_COMMIT_BRANCH
        exists:
          - Dockerfile
    artifacts:
      reports:
        container_scanning: gl-container-scanning-report.json
  ```

### 错误修复和增强

- 支持 `docker scout attest add` 命令的单架构镜像
- 在 `docker scout quickview` 和 `docker scout recommendations` 命令中指示镜像证明是否未使用 `mode=max` 创建。没有 `mode=max`，基础镜像可能被错误检测，导致结果准确性降低。

## 1.9.0

{{< release-date date="2024-05-24" >}}

已弃用，改用 [1.9.1](#191)。

## 1.8.0

{{< release-date date="2024-04-25" >}}

### 错误修复和增强

- 改进 EPSS 分数和百分位的格式。

  修改前：

  ```text
  EPSS Score      : 0.000440
  EPSS Percentile : 0.092510
  ```

  修改后：

  ```text
  EPSS Score      : 0.04%
  EPSS Percentile : 9th percentile
  ```

- 修复分析本地文件系统时 `docker scout cves` 命令的 Markdown 输出。[docker/scout-cli#113](https://github.com/docker/scout-cli/issues/113)

## 1.7.0

{{< release-date date="2024-04-15" >}}

### 新增

- [`docker scout push` 命令](/reference/cli/docker/scout/push/) 现在完全可用：在本地分析镜像并将 SBOM 推送到 Docker Scout。

### 错误修复和增强

- 修复向私有仓库中的镜像添加 `docker scout attestation add` 证明的问题
- 修复基于空 `scratch` 基础镜像的镜像处理
- Docker Scout CLI 命令的新 `sbom://` 协议允许您从标准输入读取 Docker Scout SBOM。

  ```console
  $ docker scout sbom IMAGE | docker scout qv sbom://
  ```

- 添加 Joomla 包的分类器

## 1.6.4

{{< release-date date="2024-03-26" >}}

### 错误修复和增强

- 修复基于 RPM 的 Linux 发行版的 epoch 处理

## 1.6.3

{{< release-date date="2024-03-22" >}}

### 错误修复和增强

- 改进包检测以忽略引用但未安装的包。

## 1.6.2

{{< release-date date="2024-03-22" >}}

### 错误修复和增强

- EPSS 数据现在通过后端获取，而不是通过 CLI 客户端。
- 修复使用 `sbom://` 前缀渲染 Markdown 输出时的问题。

### 已移除

- `docker scout cves --epss-date` 和 `docker scout cache prune --epss` 标志已被移除。

## 1.6.1

{{< release-date date="2024-03-20" >}}

> [!NOTE]
>
> 此版本仅影响 `docker/scout-action` GitHub Action。

### 新增

- 添加对传入 SDPX 或 in-toto SDPX 格式 SBOM 文件的支持

  ```yaml
  uses: docker/scout-action@v1
  with:
      command: cves
      image: sbom://alpine.spdx.json
  ```

- 添加对 `syft-json` 格式 SBOM 文件的支持

  ```yaml
  uses: docker/scout-action@v1
  with:
      command: cves
      image: sbom://alpine.syft.json
  ```

## 1.6.0

{{< release-date date="2024-03-19" >}}

> [!NOTE]
>
> 此版本仅影响 CLI 插件，不影响 GitHub Action

### 新增

- 添加对传入 SDPX 或 in-toto SDPX 格式 SBOM 文件的支持

  ```console
  $ docker scout cves sbom://path/to/sbom.spdx.json
  ```

- 添加对 `syft-json` 格式 SBOM 文件的支持

  ```console
  $ docker scout cves sbom://path/to/sbom.syft.json
  ```

- 从标准输入读取 SBOM 文件

  ```console
  $ syft -o json alpine | docker scout cves sbom://
  ```

- 按 EPSS 分数优先 CVE

  - `--epss` 显示并优先 CVE
  - `--epss-score` 和 `--epss-percentile` 按分数和百分位过滤
  - 使用 `docker scout cache prune --epss` 清理缓存的 EPSS 文件

### 错误修复和增强

- 在 WSL2 中使用 Windows 缓存

  当在 WSL2 中且 Docker Desktop 运行时，Docker Scout CLI 插件现在使用 Windows 的缓存。这样，如果镜像已被 Docker Desktop 索引，WSL2 端就无需重新索引。
- 如果使用[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 功能禁用了索引，CLI 中现在会阻止索引。

- 修复分析单镜像 `oci-dir` 输入时发生的崩溃
- 改进使用 containerd 镜像存储的本地证明支持

## 早期版本

Docker Scout CLI 插件早期版本的发布说明可在 [GitHub](https://github.com/docker/scout-cli/releases) 上找到。