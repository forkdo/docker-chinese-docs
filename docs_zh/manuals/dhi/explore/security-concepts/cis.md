---
aliases:
  - /dhi/core-concepts/cis/
title: CIS Benchmark（CIS 基准）
description: 了解 Docker Hardened Images 如何符合 CIS Docker Benchmark，帮助组织加固容器镜像以实现安全部署。
keywords: docker cis benchmark, cis docker compliance, cis docker images, docker hardened images, secure container images
---

## What is the CIS Docker Benchmark?（什么是 CIS Docker Benchmark？）

[CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker) 是全球公认的 CIS Benchmarks 的一部分，由 [Center for Internet Security（CIS，互联网安全中心）](https://www.cisecurity.org/) 制定。它定义了 Docker 容器生态系统各方面的推荐安全配置，包括容器宿主机、Docker 守护进程、容器镜像和容器运行时。

## Why CIS Benchmark compliance matters（为何 CIS Benchmark 合规很重要）

遵循 CIS Docker Benchmark 可以帮助组织：

- 借助广泛认可的加固指南降低安全风险。
- 满足引用 CIS 控制项的法规或合同要求。
- 跨团队标准化镜像和 Dockerfile 实践。
- 以基于公开标准的配置决策来证明审计准备度。

## How Docker Hardened Images comply with the CIS Benchmark（Docker Hardened Images 如何符合 CIS Benchmark）

Docker Hardened Images（DHI）在设计时即以安全为先，并经过验证符合适用于容器镜像和 Dockerfile 配置范围的 CIS Docker Benchmark 中的相关控制项。

符合 CIS 的 DHI 符合第 4 节中的所有控制项，唯一的例外是需要 Docker Content Trust（DCT）的控制项，[Docker 已正式弃用](https://www.docker.com/blog/retiring-docker-content-trust/)该功能。取而代之，DHI 使用 Cosign 进行[签名](/manuals/dhi/explore/security-concepts/signatures.md)，提供了更高级别的真实性和完整性。从符合 CIS 的 DHI 起步，团队可以更快、更有信心地采用该基准中的镜像级最佳实践。

> [!NOTE]
>
> CIS Docker Benchmark 还包含针对宿主机、守护进程和运行时的控制项。符合 CIS 的 DHI 仅处理镜像和 Dockerfile 范围（第 4 节）。整体合规性仍取决于你如何配置和运营更广阔的环境。

## Identify CIS-compliant images（识别符合 CIS 的镜像）

符合 CIS 的镜像在 Docker Hardened Images 目录中标记为 **CIS**。要查找它们，请[搜索目录](../../how-to/search-evaluate.md)并在单个列表中查找 **CIS** 标识。

## Get the benchmark（获取基准）

直接从 CIS 下载最新的 CIS Docker Benchmark：
https://www.cisecurity.org/benchmark/docker
