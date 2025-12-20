# Docker 强化镜像的测试方式

Docker 强化镜像（DHIs）旨在实现安全、精简且可用于生产环境。为确保其可靠性和安全性，Docker 采用了一套全面的测试策略，您可以使用签名的证明（attestations）和开源工具独立进行验证。

每个镜像都会针对标准合规性、功能性和安全性进行测试。测试结果会作为签名证明嵌入其中，您可以使用 Docker Scout CLI 以编程方式[检查和验证](#view-and-verify-the-test-attestation)这些证明。

## 测试策略概览

DHI 的测试流程主要关注两个方面：

- **镜像标准合规性**：确保每个镜像都符合严格的大小、安全性和兼容性标准。
- **应用程序功能性**：验证镜像内的应用程序能够正常运行。

## 镜像标准合规性

每个 DHI 都会经过严格的检查，以满足以下标准：

- **最小攻击面**：镜像构建得尽可能小，移除了不必要的组件以减少潜在漏洞。
- **近乎为零的已知 CVE**：使用 Docker Scout 等工具扫描镜像，确保不存在已知的通用漏洞和暴露（CVE）。
- **多架构支持**：DHI 为多种架构（`linux/amd64` 和 `linux/arm64`）构建，确保广泛的兼容性。
- **Kubernetes 兼容性**：测试镜像能否在 Kubernetes 集群中无缝运行，确保其满足容器编排环境的要求。

## 应用程序功能性测试

Docker 会对 Docker 强化镜像进行测试，以确保它们在典型使用场景下表现符合预期。这包括验证：

- 应用程序在容器化环境中能够成功启动和运行。
- 运行时行为与上游预期保持一致。
- 构建变体（如 `-dev` 镜像）支持常见的开发和构建任务。

目标是确保 DHI 在最常见的用例中开箱即用，同时保持强化、精简的设计。

## 自动化测试与 CI/CD 集成

Docker 将自动化测试集成到其持续集成/持续部署（CI/CD）流程中：

- **自动化扫描**：每次镜像构建都会触发漏洞扫描和合规性检查。
- **可重现的构建**：构建流程设计为可重现的，确保在不同环境中的一致性。
- **持续监控**：Docker 持续监控新的漏洞，并相应地更新镜像以维持安全标准。

## 测试证明

Docker 提供一份测试证明，详细说明每个 DHI 所经历的测试和验证过程。

### 查看和验证测试证明

您可以使用 Docker Scout CLI 查看并验证此证明。

1. 使用 `docker scout attest get` 命令并指定测试谓词类型：

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --predicate \
     dhi.io/<image>:<tag>
   ```

   > [!NOTE]
   >
   > 如果镜像存在于本地设备上，必须在镜像名称前加上 `registry://` 前缀。例如，使用 `registry://dhi.io/python` 而不是 `dhi.io/python`。

   例如：

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --predicate \
     dhi.io/python:3.13
   ```

   这包含了测试列表及其结果。

   输出示例：

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

   输出示例：
   
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

如果证明有效，Docker Scout 会确认签名并显示匹配的 `cosign verify` 命令。

要查看其他证明，例如 SBOM 或漏洞报告，请参阅[验证镜像](../how-to/verify.md)。
