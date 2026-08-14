---
title: "实验：容器镜像证明"
linkTitle: "实验：镜像证明"
description: |
  学习为容器镜像附加 SBOM、构建来源、镜像签名和 VEX
  声明，打造可验证的软件供应链。
summary: |
  动手实验：为容器镜像添加供应链元数据。使用 BuildKit 生成
  SBOM 和 SLSA 来源证明，使用 Cosign 为镜像签名，并附加
  OpenVEX 声明以说明漏洞的可利用状态。
keywords: Docker, supply chain, SBOM, provenance, SLSA, Cosign, VEX, attestations, security, lab, labspace
params:
  tags: [labs]
  time: 45 minutes
---

证明你的容器镜像来自何处，以及它们未被
篡改。本实验将带你使用 BuildKit 生成 SBOM 和 SLSA 构建
来源证明，使用 Cosign 为镜像签名，并编写 VEX
声明来说明哪些 CVE 会影响你的镜像——这些正是用于
满足 NIST SSDF 和 EO 14028 等供应链安全要求的技术。

## 启动实验

{{< labspace-launch image="dockersamples/labspace-attestation-basics" >}}

## 你将学到什么

完成本 Labspace 后，你将掌握以下内容：

- 使用 `--sbom=true` 生成并检查附加到容器镜像上的 SPDX SBOM
- 使用 `--provenance=mode=max` 生成 SLSA 构建来源证明，并理解多阶段构建是如何被完整记录的
- 安装 Cosign 并使用基于密钥的签名方式为容器镜像签名和验签
- 编写 OpenVEX 声明来说明 CVE 的可利用状态，并将其作为签名证明附加到镜像
- 理解 SBOM、来源证明、签名和 VEX 如何在完整的供应链叙事中相辅相成

## 模块

| #   | 模块                              | 说明                                                                                   |
| --- | --------------------------------- | -------------------------------------------------------------------------------------- |
| 1   | 引言                              | 供应链证明概览与示例 Go 应用介绍                                                       |
| 2   | 软件物料清单（SBOM）              | 使用 `--sbom=true` 构建、检查 SPDX 内容，并理解与扫描器的集成                          |
| 3   | 构建来源证明                      | 生成 SLSA 来源证明，并探究多阶段构建是如何被记录的                                     |
| 4   | 使用 Cosign 为镜像签名            | 生成密钥对、为镜像签名、验证签名，并了解无密钥签名                                     |
| 5   | VEX 声明                          | 扫描 CVE、编写 OpenVEX 文档，并将其作为签名证明附加                                    |
| 6   | 融会贯通                          | 运行完整的构建—签名—证明工作流，纵览完整的供应链全貌                                   |
| 7   | 回顾                              | 技能总结，以及策略强制执行和更高 SLSA 等级的后续步骤                                   |
