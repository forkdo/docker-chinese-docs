---
title: Docker Scout
weight: 40
keywords: scout, supply chain, vulnerabilities, packages, cves, scan, analysis, analyze
description:
  了解 Docker Scout 的概述，以主动增强您的软件供应链安全
aliases:
  - /engine/scan/
params:
  sidebar:
    group: Products
grid:
  - title: 快速开始
    link: /scout/quickstart/
    description: 了解 Docker Scout 的功能以及如何开始使用。
    icon: explore
  - title: 镜像分析
    link: /scout/image-analysis/
    description: 揭示并深入分析您的镜像组成。
    icon: radar
  - title: 咨询数据库
    link: /scout/advisory-db-sources/
    description: 了解 Docker Scout 使用的信息来源。
    icon: database
  - title: 集成
    description: 将 Docker Scout 与您的 CI、注册表和其他第三方服务连接。
    link: /scout/integrations/
    icon: multiple_stop
  - title: 仪表板
    link: /scout/dashboard/
    description: Docker Scout 的 Web 界面。
    icon: dashboard
  - title: 策略
    link: /scout/policy/
    description: 确保您的制品符合供应链最佳实践。
    icon: policy
  - title: 升级
    link: /subscription/change/
    description: 个人订阅包含最多 1 个仓库。升级以获得更多功能。
    icon: upgrade
---

容器镜像由多层和软件包组成，这些组件容易受到漏洞的影响。
这些漏洞可能会危及容器和应用程序的安全。

Docker Scout 是一个用于主动增强软件供应链安全的解决方案。
通过分析您的镜像，Docker Scout 会编译出组件清单，也称为软件物料清单（SBOM）。
SBOM 会与持续更新的漏洞数据库进行匹配，以识别安全弱点。

Docker Scout 是一个独立的服务和平台，您可以通过 Docker Desktop、Docker Hub、Docker CLI 和 Docker Scout 仪表板与之交互。
Docker Scout 还支持与第三方系统（如容器注册表和 CI 平台）的集成。

{{< grid >}}