---
description: 了解 Docker 赞助的开源计划及其运作方式
title: Docker 赞助的开源计划
keywords: docker hub, hub, insights, analytics, open source, Docker sponsored, program
aliases:
- /docker-hub/dsos-program/
- /trusted-content/dsos-program/
---

[Docker 赞助的开源镜像](https://hub.docker.com/search?badges=open_source)由 Docker 通过该计划赞助的开源项目发布和维护。

该计划中的镜像在 Docker Hub 上带有特殊徽章，使用户更容易识别 Docker 已验证为可信、安全且活跃的开源项目。

![Docker 赞助的开源徽章](../../../images/sponsored-badge-iso.png)

Docker 赞助的开源（DSOS）计划为非商业开源开发者提供多项功能和福利。

该计划为符合条件的项目提供以下特权：

- 仓库 Logo
- 已验证的 Docker 赞助开源徽章
- 洞察与分析
- 访问 [Docker Scout](#docker-scout) 进行软件供应链治理
- 为开发者解除速率限制
- 在 Docker Hub 上提升可发现性

这些福利有效期为一年，如果项目仍符合计划要求，发布者可以每年续期。计划成员以及从项目命名空间拉取公共镜像的所有用户均可享受无限拉取和无限出口流量。

### 仓库 Logo

DSOS 组织可以在 Docker Hub 上为各个仓库上传自定义图片。
这使您可以按仓库覆盖默认的组织级 Logo。

只有组织的所有者或编辑角色用户才能更改仓库 Logo。

#### 图片要求

- Logo 图片支持的文件类型为 JPEG 和 PNG。
- 允许的最小图片尺寸为 120×120 像素。
- 允许的最大图片尺寸为 1000×1000 像素。
- 允许的最大图片文件大小为 5MB。

#### 设置仓库 Logo

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 转到您要更改 Logo 的仓库页面。
3. 选择上传 Logo 按钮，该按钮由覆盖在当前仓库 Logo 上的相机图标表示
   ({{< inline-image src="../../../images/upload_logo_sm.png" alt="相机图标" >}})。
4. 在打开的对话框中，选择要上传的 PNG 图片以将其设置为仓库 Logo。

#### 移除 Logo

选择 **清除** 按钮 ({{< inline-image src="../../../images/clear_logo_sm.png"
alt="清除按钮" >}}) 以移除 Logo。

移除 Logo 后，如果已设置组织 Logo，则仓库将默认使用该 Logo；如果未设置，则使用以下默认 Logo。

![默认 Logo，是一个 3D 灰色立方体](../../../images/default_logo_sm.png)

### 已验证的 Docker 赞助开源徽章

Docker 验证了带有此徽章的镜像在 Docker Hub 上是活跃的开源项目，开发者可信任这些镜像。

![带有 Docker 赞助开源徽章的 Fluent 组织](../../../images/sponsored-badge.png)

### 洞察与分析

[洞察与分析](/docker-hub/publish/insights-analytics) 服务提供社区如何使用 Docker 镜像的使用指标，深入了解用户行为。

使用指标显示按标签或摘要拉取镜像的次数，并按地理位置、云提供商、客户端等分类统计。

您可以选择要查看分析数据的时间范围。您还可以以摘要或原始格式导出数据。

### Docker Scout

DSOS 项目最多可免费在 100 个仓库上启用 Docker Scout。Docker
Scout 提供自动镜像分析、改进供应链治理的策略评估、与 CI 平台和源代码管理等第三方系统的集成等功能。

您可以按仓库启用 Docker Scout。有关如何使用此产品的信息，请参阅 [Docker Scout 文档](/scout/)。

### 谁有资格参加 Docker 赞助的开源计划？

要获得该计划资格，发布者必须在公共仓库中共享项目命名空间，符合[开源倡议定义](https://opensource.org/docs/osd)，并且处于活跃开发状态且无商业化途径。

前往
[Docker 赞助的开源计划](https://www.docker.com/community/open-source/application/) 申请页面了解更多信息。