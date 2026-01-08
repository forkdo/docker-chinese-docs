---
---
title: How Docker Hardened Images are tested
linktitle: Image testing
description: "See how Docker Hardened Images are automatically tested for standards compliance, functionality, and security."
weight: 45
keywords: "docker scout, test attestation, cosign verify, image testing, vulnerability scan"
aliases:
  - /dhi/about/test/---
title: Docker 加固镜像的测试方式
linktitle: 镜像测试
description: "了解 Docker 加固镜像如何自动进行标准合规性、功能性和安全性测试。"
weight: 45---
Docker 加固镜像（Docker Hardened Images，简称 DHI）旨在实现安全、精简并可用于生产环境。为确保其可靠性和安全性，Docker 采用了一套全面的测试策略，您可以使用经过签名的证明和可公开访问的工具独立验证这些测试结果。

每个镜像都会接受标准合规性、功能性和安全性测试。这些测试结果会以经过签名的证明形式嵌入镜像中，您可以使用 Docker Scout CLI 以编程方式[查看和验证这些测试证明](#view-and-verify-the-test-attestation)。

## 测试策略概览

DHI 的测试流程主要关注以下两个方面：

- 镜像标准合规性：确保每个镜像都符合严格的体积、安全性和兼容性标准。
- 应用程序功能性：验证镜像中的应用程序能否正常运行。

## 镜像标准合规性

每个 DHI 都会经过严格检查，以满足以下标准：

- 最小化攻击面：镜像构建时尽可能精简，移除不必要的组件以降低潜在漏洞风险。
- 近乎零已知 CVE：使用 Docker Scout 等工具扫描镜像，确保其不包含任何已知的通用漏洞披露（Common Vulnerabilities and Exposures，简称 CVE）。
- 多架构支持：DHI 支持多种架构（`linux/amd64` 和 `linux/arm64`），以确保广泛的兼容性。
- Kubernetes 兼容性：镜像经过测试，可在 Kubernetes 集群中无缝运行，满足容器编排环境的要求。

## 应用程序功能性测试

Docker 会对 Docker 加固镜像进行测试，确保其在典型使用场景下表现符合预期。具体包括验证以下内容：

- 应用程序能否在容器化环境中成功启动并运行。
- 运行时行为是否与上游预期一致。
- 构建变体（如 `-dev` 镜像）是否支持常见的开发和构建任务。

目标是确保 DHI 在保持加固和精简设计的同时，开箱即用，满足最常见用例的需求。

## 自动化测试与 CI/CD 集成

Docker 将自动化测试集成到其持续集成/持续部署（CI/CD）流水线中：

- 自动化扫描：每次镜像构建都会触发自动化漏洞扫描和合规性检查。
- 可重现构建：构建流程设计为可重现，确保在不同环境中的一致性。
- 持续监控：Docker 持续监控新出现的漏洞，并相应更新镜像以维持安全标准。

## 测试证明

Docker 提供测试证明，详细说明每个 DHI 所经历的测试和验证流程。

### 查看和验证测试证明

您可以使用 Docker Scout CLI 查看和验证此证明。

1. 使用 `docker scout attest get` 命令并指定测试谓词类型：

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --predicate \
     dhi.io/<image>:<tag>
   ```

   > [!NOTE]
   >
   > 如果镜像已存在于您的设备上，则必须在镜像名称前添加 `registry://` 前缀。例如，使用 `registry://dhi.io/python` 而不是 `dhi.io/python`。

   例如：

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --predicate \
     dhi.io/python:3.13
   ```

   此命令会返回测试列表及其结果。

   示例输出：

    ```console
        v SBOM obtained from attestation, 101 packages found
        v Provenance obtained from attestation
        {
          "reportFormat": "CTRF",
          "results": {
            "summary": {
              "failed": 0,
              "passed": 1,
              "skipped": 0,
              "start": 1749216533,
              "stop": 1749216574,
              "tests": 1
            },
            "tests": [
              {
                ...
   ```

2. 验证测试证明签名。为确保证明真实有效且由 Docker 签名，请运行：

   ```console
   docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --verify \
     dhi.io/<image>:<tag> --platform <platform>
   ```

   示例输出：
   
   ```console
    v SBOM obtained from attestation, 101 packages found
    v Provenance obtained from attestation
    v cosign verify registry.scout.docker.com/docker/dhi-python@sha256:70c8299c4d3cb4d5432734773c45ae58d8acc2f2f07803435c65515f662136d5 \
        --key https://registry.scout.docker.com/keyring/dhi/latest.pub --experimental-oci11

      Verification for registry.scout.docker.com/docker/dhi-python@sha256:70c8299c4d3cb4d5432734773c45ae58d8acc2f2f07803435c65515f662136d5 --
      The following checks were performed on each of these signatures:
        - The cosign claims were validated
        - Existence of the claims in the transparency log was verified offline
        - The signatures were verified against the specified public key

    i Signature payload
    ...
    ```

如果证明有效，Docker Scout 将确认签名并显示匹配的 `cosign verify` 命令。

如需查看其他证明（如 SBOM 或漏洞报告），请参阅[验证镜像](../how-to/verify.md)。