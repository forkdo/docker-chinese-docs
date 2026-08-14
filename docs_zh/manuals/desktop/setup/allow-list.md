---
description: 组织内确保 Docker Desktop 正常运行所需的域名 URL 列表。
keywords: Docker Desktop, allowlist, allow list, 防火墙, 认证 URL, 分析
title: Docker Desktop 允许列表
tags:
- admin
linkTitle: 允许列表
weight: 100
aliases:
- /desktop/allow-list/
---

{{< summary-bar feature_name="Allow list" >}}

此页面包含您需要添加到防火墙允许列表中的域名 URL，以确保 Docker Desktop 在您的组织内正常工作。

## 需要允许的域名 URL

| 域名                                                                              | 描述                                  |
| ------------------------------------------------------------------------------------ | -------------------------------------------- |
| https://notify.bugsnag.com                                                           | 错误报告                                |
| https://sessions.bugsnag.com                                                         | 错误报告                                |
| https://auth.docker.io                                                               | 认证                               |
| https://cdn.auth0.com                                                                | 认证                               |
| https://login.docker.com                                                             | 认证                               |
| https://auth.docker.com                                                              | 认证                               |
| https://desktop.docker.com                                                           | 更新                                       |
| https://hub.docker.com                                                               | Docker Hub                                   |
| https://registry-1.docker.io                                                         | Docker 拉取/推送                             |
| https://production.cloudfront.docker.com                                             | Docker 拉取/推送                             |
| https://docker-pinata-support.s3.amazonaws.com                                       | 故障排除                              |
| https://api.dso.docker.com                                                           | Docker Scout 服务                         |
| https://api.docker.com                                                               | 新 API                                      |
| https://api.offload.docker.com                                                       | Docker Offload                               |
| https://dhi.io                                                                       | Docker Hardened Images                       |
| https://registry.scout.docker.com                                                    | 用于 DHI 证明的 Docker Scout 注册表   |
| https://ai-backend-service.docker.com                                                | [Gordon](/manuals/ai/gordon/_index.md)       |
