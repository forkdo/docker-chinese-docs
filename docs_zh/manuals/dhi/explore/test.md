---
title: Docker Hardened Images 的测试方式
linktitle: 镜像测试
description: 了解 Docker Hardened Images 如何通过自动化的标准合规性、功能性和安全性测试。
keywords: docker scout, test attestation, cosign verify, image testing, vulnerability scan
weight: 45
---

Docker Hardened Images（DHI）旨在提供安全、精简且可直接用于生产环境的镜像。为了确保其可靠性和安全性，Docker 采用了一套全面的测试策略，您也可以使用已签名的证明文件和开源工具独立验证。

每个镜像都会经过标准合规性、功能性和安全性的测试。测试结果以签名证明的形式嵌入镜像中，您可以通过 Docker Scout CLI 程序化地[查看和验证](#view-and-verify-the-test-attestation)这些证明。

## 测试策略概述

DHI 的测试流程主要关注两个方面：

- 镜像标准合规性：确保每个镜像符合严格的安全性、体积和兼容性标准。
- 应用功能性：验证镜像中的应用程序能够正常运行。

## 镜像标准合规性

每个 DHI 都会经过严格的检查，以满足以下标准：

- 最小攻击面：镜像被构建得尽可能小，移除不必要的组件以减少潜在漏洞。
- 接近零已知 CVE：使用 Docker Scout 等工具扫描镜像，确保其不包含已知的通用漏洞与暴露（CVE）。
- 多架构支持：DHI 支持多种架构（`linux/amd64` 和 `linux/arm64`），确保广泛的兼容性。
- Kubernetes 兼容性：镜像经过测试，确保能够在 Kubernetes 集群中无缝运行，满足容器编排环境的要求。

## 应用功能性测试

Docker 会测试 Docker Hardened Images，确保其在典型使用场景中表现正常。包括验证：

- 应用程序能够在容器化环境中成功启动和运行。
- 运行时行为与上游预期一致。
- 构建变体（如 `-dev` 镜像）支持常见的开发和构建任务。

目标是确保 DHI 在保持精简、强化设计的同时，能够开箱即用地满足最常见的使用场景。

## 自动化测试与 CI/CD 集成

Docker 将自动化测试集成到其持续集成/持续部署（CI/CD）流水线中：

- 自动扫描：每次镜像构建都会触发自动漏洞扫描和合规性检查。
- 可重现构建：构建过程设计为可重现的，确保不同环境之间的一致性。
- 持续监控：Docker 持续监控新漏洞，并相应更新镜像以维持安全标准。

## 测试证明

Docker 提供测试证明，详细说明每个 DHI 经历的测试和验证过程。

### 查看和验证测试证明

您可以使用 Docker Scout CLI 查看和验证此证明。

1. 使用 `docker scout attest get` 命令和测试谓词类型：

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --predicate \
     dhi.io/<image>:<tag>
   ```

   > [!NOTE]
   >
   > 如果镜像存在于本地设备上，您必须在镜像名称前加上 `registry://` 前缀。例如，使用
   > `registry://dhi.io/python` 而不是 `dhi.io/python`。

   示例：

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --predicate \
     dhi.io/python:3.13
   ```

   这将返回测试列表及其结果。

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

2. 验证测试证明签名。为确保证明真实且由 Docker 签名，请运行：

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

要查看其他证明，如 SBOM 或漏洞报告，请参阅 [验证镜像](../how-to/verify.md)。