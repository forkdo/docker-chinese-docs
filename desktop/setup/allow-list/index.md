---
title: Docker Desktop 允许列表
url: /desktop/setup/allow-list/
parent:
  title: Docker Desktop
  url: /desktop/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Desktop
    url: /desktop/
  - title: Docker Desktop 允许列表
    url: /desktop/setup/allow-list/
next:
  title: 登录 Docker Desktop
  url: /desktop/setup/sign-in/
---




此页面包含您需要添加到防火墙允许列表中的域名 URL，以确保 Docker Desktop 在您的组织内正常工作。

## 需要允许的域名 URL

| 域名                                                                              | 描述                                  |
| ------------------------------------------------------------------------------------ | -------------------------------------------- |
| https://api.segment.io                                                               | 分析                                    |
| https://cdn.segment.com                                                              | 分析                                    |
| https://notify.bugsnag.com                                                           | 错误报告                                |
| https://sessions.bugsnag.com                                                         | 错误报告                                |
| https://auth.docker.io                                                               | 认证                               |
| https://cdn.auth0.com                                                                | 认证                               |
| https://login.docker.com                                                             | 认证                               |
| https://auth.docker.com                                                              | 认证                               |
| https://desktop.docker.com                                                           | 更新                                       |
| https://hub.docker.com                                                               | Docker Hub                                   |
| https://registry-1.docker.io                                                         | Docker 拉取/推送                             |
| https://production.cloudflare.docker.com                                             | Docker 拉取/推送（付费计划）                |
| https://docker-images-prod.6aa30f8b08e16409b46e0173d6de2f56.r2.cloudflarestorage.com | Docker 拉取/推送（个人计划/匿名） |
| https://docker-pinata-support.s3.amazonaws.com                                       | 故障排除                              |
| https://api.dso.docker.com                                                           | Docker Scout 服务                         |
| https://api.docker.com                                                               | 新 API                                      |
