---
description: 了解 Docker 赞助开源计划及其工作原理
title: Docker 赞助开源计划
keywords: docker hub, hub, insights, analytics, open source, Docker sponsored, program
aliases:
  - /docker-hub/dsos-program/
  - /trusted-content/dsos-program/
---

[Docker 赞助开源镜像](https://hub.docker.com/search?badges=open_source) 由 Docker 通过该计划赞助的开源项目发布和维护。

属于此计划的镜像在 Docker Hub 上具有特殊徽章，方便用户识别 Docker 已验证为可信、安全和活跃的开源项目。

![Docker 赞助开源徽章](../../../images/sponsored-badge-iso.png)

Docker 赞助开源（DSOS）计划为非商业开源开发者提供多项功能和优势。

该计划为符合条件的项目授予以下特权：

- 仓库徽标
- 已验证的 Docker 赞助开源徽章
- 洞察与分析
- 访问 [Docker Scout](#docker-scout) 以进行软件供应链管理
- 为开发者移除速率限制
- 在 Docker Hub 上提升可发现性

这些权益有效期为一年，如果项目仍符合计划要求，发布者可每年续期。计划成员以及所有从项目命名空间拉取公共镜像的用户可享受无限制拉取和无限制出站流量。

### 仓库徽标

DSOS 组织可以在 Docker Hub 上为各个仓库上传自定义图像。
这允许您逐仓库覆盖默认的组织级徽标。

只有组织中具有所有者或编辑者角色的用户才能更改仓库徽标。

#### 图像要求

- 支持的徽标图像文件类型为 JPEG 和 PNG。
- 允许的最小图像尺寸为 120×120 像素。
- 允许的最大图像尺寸为 1000×1000 像素。
- 允许的最大图像文件大小为 5MB。

#### 设置仓库徽标

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 转到要更改徽标的仓库页面。
3. 选择上传徽标按钮，该按钮由相机图标表示
   ({{< inline-image src="../../../images/upload_logo_sm.png" alt="camera icon" >}})
   覆盖在当前仓库徽标上。
4. 在打开的对话框中，选择要上传的 PNG 图像以设置为仓库徽标。

#### 移除徽标

选择 **清除** 按钮 ({{< inline-image src="../../../images/clear_logo_sm.png"
alt="clear button" >}}) 以移除徽标。

移除徽标后，仓库将默认使用组织徽标（如果已设置），否则使用以下默认徽标。

![默认徽标，一个 3D 灰色立方体](../../../images/default_logo_sm.png)

### 已验证的 Docker 赞助开源徽章

Docker 验证带有此徽章的镜像在 Docker Hub 上是活跃的开源项目，开发者可信任。

![带有 Docker 赞助开源徽章的 Fluent 组织](../../../images/sponsored-badge.png)

### 洞察与分析

[洞察与分析](/docker-hub/publish/insights-analytics) 服务提供社区如何使用 Docker 镜像的使用指标，让您深入了解用户行为。

使用指标显示按标签或摘要统计的镜像拉取次数，以及按地理位置、云提供商、客户端等的细分数据。

您可以选择要查看分析数据的时间范围。您还可以将数据导出为摘要或原始格式。

### 谁有资格参加 Docker 赞助开源计划？

要符合该计划的资格，发布者必须在公共仓库中共享项目命名空间，满足 [开放源代码促进会定义](https://opensource.org/docs/osd)，并且处于活跃开发状态，无商业化路径。

前往 [Docker 赞助开源计划](https://www.docker.com/community/open-source/application/) 申请页面了解更多信息。