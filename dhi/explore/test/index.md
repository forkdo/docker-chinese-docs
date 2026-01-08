# Docker 强化镜像如何进行测试

Docker 强化镜像（DHI）旨在安全、精简并可用于生产环境。为了确保其可靠性和安全性，Docker 采用了全面的测试策略，您可以使用签名证明和开源工具独立验证这些策略。

每个镜像都会针对标准合规性、功能性和安全性进行测试。测试结果以签名证明的形式嵌入，您可以使用 Docker Scout CLI 以[编程方式查看和验证](#view-and-verify-the-test-attestation)这些结果。

## 测试策略概览

DHI 的测试过程主要集中在两个领域：

- 镜像标准合规性：确保每个镜像都严格遵守大小、安全性和兼容性标准。
- 应用程序功能性：验证镜像内的应用程序是否正常运行。

## 镜像标准合规性

每个 DHI 都经过严格检查以满足以下标准：

- 最小攻击面：镜像构建得尽可能小，移除不必要的组件以减少潜在漏洞。
- 近零已知 CVE：使用 Docker Scout 等工具扫描镜像，确保它们没有已知的通用漏洞披露（CVE）。
- 多架构支持：DHI 为多种架构（`linux/amd64` 和 `linux/arm64`）构建，以确保广泛的兼容性。
- Kubernetes 兼容性：对镜像进行测试以确保其在 Kubernetes 集群中无缝运行，满足容器编排环境的要求。

## 应用程序功能测试

Docker 对 Docker 强化镜像进行测试，以确保它们在典型使用场景下的行为符合预期。这包括验证：

- 应用程序在容器化环境中成功启动并运行。
- 运行时行为与上游预期一致。
- 构建变体（如 `-dev` 镜像）支持常见的开发和构建任务。

目标是确保 DHI 在最常见的用例中开箱即用，同时保持强化和精简的设计。

## 自动化测试和 CI/CD 集成

Docker 将自动化测试集成到其持续集成/持续部署（CI/CD）流水线中：

- 自动化扫描：每次镜像构建都会触发漏洞扫描和合规性检查。
- 可重现构建：构建过程设计为可重现，确保在不同环境中的一致性。
- 持续监控：Docker 持续监控新漏洞，并相应地更新镜像以维护安全标准。

## 测试证明

Docker 提供测试证明，详细说明每个 DHI 经过的测试和验证流程。

### 查看和验证测试证明

您可以使用 Docker Scout CLI 查看和验证此证明。

1. 使用带有测试谓词类型的 `docker scout attest get` 命令：

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --predicate \
     dhi.io/<image>:<tag>
   ```

   > [!NOTE]
   >
   > 如果镜像存在于您的本地设备上，则必须在镜像名称前加上 `registry://` 前缀。例如，使用
   > `registry://dhi.io/python` 而不是 `dhi.io/python`。

   例如：

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --predicate \
     dhi.io/python:3.13
   ```

   这包含测试列表及其结果。

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

2. 验证测试证明签名。为了确保证明是真实的并由 Docker 签名，请运行：

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

要查看其他证明（如 SBOM 或漏洞报告），请参阅[验证镜像](../how-to/verify.md)。
