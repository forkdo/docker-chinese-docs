---
title: Resources and feedback
linktitle: Resources and feedback
description: Docker Hardened Images 的其他资源、社区链接、GitHub 仓库以及如何提交反馈。
keywords: docker hardened images resources, dhi feedback, dhi github, dhi community, report issue, dhi support
weight: 999
aliases:
  - /dhi/about/feedback/
  - /dhi/explore/feedback/
---

本页面提供与 Docker Hardened Images (DHI) 相关的其他资源、社区渠道以及反馈方式的链接。

有关产品信息和功能对比，请访问 [Docker Hardened
Images 产品页面](https://www.docker.com/products/hardened-images/)。

## 指南

有关在各种场景中演示如何使用 Docker Hardened Images 的指南，请参阅
[按 DHI 筛选的指南部分](/guides/?tags=dhi)。

## Docker Hub

Docker Hardened Images 可在 Docker Hub 上获得：

- [Docker Hardened Images 目录](https://dhi.io)：浏览并拉取官方目录中的 Docker Hardened Images
- [Docker Hub MCP 服务器](https://hub.docker.com/mcp/server/dockerhub/overview)：MCP 服务器，用于列出您的组织中可用的 Docker Hardened Images (DHI)

## GitHub 仓库和资源

Docker Hardened Images 仓库可在 GitHub 组织 [docker-hardened-images](https://github.com/docker-hardened-images) 中找到：

- [目录](https://github.com/docker-hardened-images/catalog)：DHI 定义文件和目录元数据
- [安全公告](https://github.com/docker-hardened-images/advisories)：随 DHI 分发的 OSS 包的 CVE 安全公告
  - [扫描器厂商集成指南](https://github.com/docker-hardened-images/advisories/tree/main/integration)：供扫描器厂商集成 DHI VEX 支持的参考文档
- [密钥环](https://github.com/docker-hardened-images/keyring)：公共签名密钥和验证工具
- [日志](https://github.com/docker-hardened-images/log)：Docker Hardened Images 的引用日志（标签 > 摘要）
- [策略](https://github.com/docker-hardened-images/policies)：用于强制执行 DHI 安全和合规标准的 Docker Scout 策略的 Rego 源文件
- [dhictl](https://github.com/docker-hardened-images/dhictl)：用于管理和交互 Docker Hardened Images 的命令行界面
- [Terraform Provider](https://github.com/docker-hardened-images/terraform-provider-dhi)：用于管理 DHI 资源的 Terraform 提供商
  （[Terraform Registry](https://registry.terraform.io/providers/docker-hardened-images/dhi/latest/docs)）

## 其他资源

- [开始免费试用](https://hub.docker.com/hardened-images/start-free-trial)：探索 DHI Select 和企业版功能，包括 FIPS/STIG 变体、自定义配置以及 SLA 支持
- [支持服务等级协议](https://docs.docker.com/go/dhi-sla/)：查看 DHI Select 和企业版订阅的 SLA 承诺
- [申请演示](https://www.docker.com/products/hardened-images/#getstarted)：获取个性化的演示以及有关 DHI Select 和企业版订阅的信息
- [申请镜像](https://github.com/docker-hardened-images/catalog/issues)：提交对特定 Docker 强化镜像的请求
- [Debian 包索引](https://dhi.io/deb/debian/main/index.html)：在 Docker 公共仓库中浏览加固的 Debian 包
- [Alpine 包索引](https://dhi.io/apk/alpine/v3.24/main/index.html)：在 Docker 公共仓库中浏览加固的 Alpine 包
- <a href="https://www.docker.com/pricing/contact-sales/" id="dkr_docs_cs_dhi_resources" class="link" rel="noopener">联系销售</a>：就企业咨询与 Docker 销售团队联系
- [Docker 支持](https://www.docker.com/support/)：DHI Select 和企业版客户获取支持资源

## 反馈与社区

使用 [GitHub Discussions 版块](https://github.com/orgs/docker-hardened-images/discussions)
就一般问题、最佳实践、安全提示和社区公告与 DHI 团队交流。

要报告错误、请求功能或提出文档改进建议，请在
目录仓库中[提交一个 issue](https://github.com/docker-hardened-images/catalog/issues)。

## 安全披露

在协调披露并解决之前，请勿发布漏洞详情。如果您发现了安全漏洞，请遵循 Docker 的
[安全披露政策](https://www.docker.com/trust/vulnerability-disclosure-policy/)负责任地报告。
