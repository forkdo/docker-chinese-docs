---
title: Docker Scout
url: /scout/
parent:
  title: 手册
  url: /manuals/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Scout
    url: /scout/
children:
  - title: 安装 Docker Scout
    url: /scout/install/
    description: Docker Scout CLI 插件的安装说明
  - title: Docker Scout 快速入门
    url: /scout/quickstart/
    description: 了解如何开始使用 Docker Scout 分析镜像并修复漏洞
  - title: Docker Scout 中的策略评估入门
    url: /scout/policy/
    description: Docker Scout 中的策略让您能够为制品定义供应链规则和阈值，
并跟踪您的制品随时间推移相对于这些要求的表现
  - title: 将 Docker Scout 与其他系统集成
    url: /scout/integrations/
    description: 如何将 Docker Scout 与其他系统进行设置。
---


容器镜像由层（layers）和软件包组成，这些都可能存在漏洞。
这些漏洞可能会危及容器和应用程序的安全性。

Docker Scout 是一种主动增强软件供应链安全性的解决方案。
通过分析您的镜像，Docker Scout 会生成一个组件清单，也称为软件物料清单（SBOM）。
该 SBOM 会与一个持续更新的漏洞数据库进行比对，以识别安全弱点。

Docker Scout 是一个独立的服务和平台，您可以通过 Docker Desktop、Docker Hub、Docker CLI 和 Docker Scout Dashboard 与其交互。
Docker Scout 还支持与第三方系统（如容器注册表和 CI 平台）集成。


