---
title: Tools
description: 用于浏览、管理和自动化 Docker Hardened Images 的界面与工具。
weight: 25
params:
  grid_tools:
    - title: 使用 Docker Hub
      description: 在 Docker Hub 上浏览 DHI 目录，搜索仓库，检查镜像元数据，并查看 SBOM、CVE 和证明。
      icon: squares-2x2
      link: /dhi/tools/hub/
    - title: CLI
      description: 安装并使用 `docker dhi` 命令行界面，从终端浏览目录、检查镜像并管理镜像。
      icon: command-line
      link: /dhi/tools/cli/
    - title: MCP 服务器
      description: 将 AI 助手连接到 DHI 目录，使用自然语言搜索仓库、检查镜像、检索 SBOM 并检查 CVE。
      icon: cpu-chip
      link: /dhi/tools/mcp/
    - title: 使用 DHI Terraform 提供商
      description: 使用 DHI Terraform 提供商以基础设施即代码的方式管理镜像并自动化 DHI 配置。
      icon: wrench-screwdriver
      link: /dhi/tools/terraform/
---

可以通过多种界面访问和管理 Docker Hardened Images。
选择适合您工作流的工具。

{{< grid items="grid_tools" >}}
