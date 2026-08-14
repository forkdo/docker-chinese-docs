---
title: "实验：将 Node 应用迁移到 Docker Hardened Images"
linkTitle: "实验：迁移到 DHI（Node）"
description: |
  将一个 Node.js 应用从标准基础镜像迁移到 Docker Hardened
  Images。使用 Docker Scout 分析 CVE、对比镜像，并查看
  供应链证明。
summary: |
  动手实验：把 Node.js 基础镜像替换为 Docker Hardened Image。
  使用 Docker Scout 分析 CVE，改写 Dockerfile 以采用基于 DHI 的多阶段
  构建，并探索 SBOM、VEX 和合规性证明。
keywords: Docker, Hardened Images, DHI, Node.js, Docker Scout, CVE, security, SBOM, lab, labspace
params:
  tags: [labs]
  time: 30 minutes
---

将一个 Node.js 应用从标准的 `node:24-trixie-slim` 基础镜像
迁移到 Docker Hardened Image。你将使用 Docker Scout 衡量迁移前后在 CVE
数量、镜像体积和策略合规性上的差异，然后探索
DHI 随每个镜像一同提供的供应链证明。

## 启动实验

{{< labspace-launch image="dockersamples/labspace-dhi-node" >}}

## 你将学到什么

完成本 Labspace 后，你将掌握以下内容：

- 使用 Docker Scout 分析 Node.js 容器镜像，找出 CVE 和策略未通过项
- 改写 Dockerfile，采用 DHI 的 dev 与 runtime 变体进行多阶段构建
- 对比迁移前后的镜像体积和漏洞数量
- 查看 Docker Hardened Images 附带的供应链证明（SBOM、SLSA、VEX）
- 导出 VEX 文档，以便与 Grype、Trivy 等外部扫描器集成

## 模块

| #   | 模块                                     | 说明                                                                            |
| --- | ---------------------------------------- | ------------------------------------------------------------------------------- |
| 1   | 引言                                     | Docker Hardened Images 概览及其安全收益                                         |
| 2   | 环境准备                                 | 完成本实验所需的准备工作。                                                      |
| 3   | 分析初始镜像                             | 构建应用、用 Docker Scout 扫描，并查看未通过的策略                              |
| 4   | 迁移到 DHI                               | 使用 DHI 多阶段构建改写 Dockerfile 并对比结果                                   |
| 5   | DHI 证明与扫描器集成                     | 查看 SBOM、FIPS 证明、STIG 扫描结果，并为外部工具导出 VEX                       |
