# CIS 基准

## 什么是 CIS Docker 基准？

[CIS Docker 基准](https://www.cisecurity.org/benchmark/docker) 是全球公认的 CIS 基准的一部分，由 [互联网安全中心 (CIS)](https://www.cisecurity.org/) 开发。它定义了 Docker 容器生态系统所有方面的推荐安全配置，包括容器主机、Docker 守护进程、容器镜像和容器运行时。

## 为什么 CIS 基准合规性很重要

遵循 CIS Docker 基准可帮助组织：

- 通过广泛认可的加固指南降低安全风险。
- 满足引用 CIS 控制的法规或合同要求。
- 在团队间标准化镜像和 Dockerfile 实践。
- 通过基于公开标准的配置决策展示审计就绪性。

## Docker Hardened Images 如何符合 CIS 基准

Docker Hardened Images (DHIs) 从设计之初就注重安全，并经过验证，符合最新 CIS Docker 基准 (v1.8.0) 中适用于容器镜像和 Dockerfile 配置范围的相关控制项。

CIS 合规的 DHIs 符合第 4 节中的所有控制项，唯一例外是要求 Docker 内容信任 (DCT) 的控制项，该控制项已被 [Docker 正式弃用](https://www.docker.com/blog/retiring-docker-content-trust/)。取而代之的是，DHIs 使用 Cosign 进行[签名](/manuals/dhi/core-concepts/signatures.md)，提供更高水平的真实性和完整性。通过从 CIS 合规的 DHI 开始，团队可以更快、更自信地采用基准中的镜像级最佳实践。

> [!NOTE]
>
> CIS Docker 基准还包括针对主机、守护进程和运行时的控制项。CIS 合规的 DHIs 仅涵盖镜像和 Dockerfile 范围（第 4 节）。整体合规性仍取决于您如何配置和操作更广泛的环境。

## 识别 CIS 合规镜像

CIS 合规镜像在 Docker Hardened Images 目录中标记为 **CIS**。要找到它们，[浏览镜像](../how-to/explore.md) 并在各个列表上查找 **CIS** 标识。

## 获取基准

直接从 CIS 下载最新的 CIS Docker 基准：
https://www.cisecurity.org/benchmark/docker
