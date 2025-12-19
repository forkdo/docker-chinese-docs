---
description: 了解 Docker Verified Publisher Program 是什么以及其运作方式
title: Docker Verified Publisher Program
aliases:
- /docker-hub/publish/publish/
- /docker-hub/publish/customer_faq/
- /docker-hub/publish/publisher_faq/
- /docker-hub/publish/certify-images/
- /docker-hub/publish/certify-plugins-logging/
- /docker-hub/publish/trustchain/
- /docker-hub/publish/byol/
- /docker-hub/publish/publisher-center-migration/
- /docker-hub/publish/
- /docker-hub/publish/repository-logos/
- /docker-hub/dvp-program/
- /trusted-content/dvp-program/
toc_max: 2
---

[Docker Verified Publisher
Program](https://hub.docker.com/search?badges=verified_publisher) 提供由 Docker 验证的商业发布者发布的高质量镜像。

这些镜像帮助开发团队构建安全的软件供应链，在流程早期最大限度地减少接触恶意内容的风险，从而节省后续的时间和金钱。

## 谁有资格成为验证发布者？

任何在 Docker Hub 上分发软件的独立软件供应商 (ISV) 都可以加入 Verified Publisher Program。请访问 [Docker Verified Publisher
Program](https://www.docker.com/partners/programs) 页面了解更多信息。

> [!NOTE]
>
> DVP 权益按命名空间（组织）应用。如果您操作多个 Docker Hub 命名空间，每个命名空间都需要单独的 DVP 申请和验证过程。

## 计划权益

Docker Verified Publisher Program (DVP) 为 Docker Hub 发布者提供多项功能和权益。该计划根据参与级别授予以下特权：

- [企业级基础设施](#enterprise-grade-infrastructure)：具有 99.9% 正常运行时间的高可用性托管
- [验证发布者徽章](#verified-publisher-badge)：标识高质量商业发布者的特殊徽章
- [仓库徽标](#repository-logo)：为单个仓库上传自定义徽标
- [洞察与分析](#insights-and-analytics)：详细的使用指标和社区参与数据
- [漏洞分析](#vulnerability-analysis)：使用 Docker Scout 进行自动安全扫描
- [优先搜索排名](#priority-search-ranking)：在 Docker Hub 搜索结果中增强可发现性
- [移除速率限制](#removal-of-rate-limiting)：开发团队不受限制的拉取
- [联合营销机会](#co-marketing-opportunities)：与 Docker 的联合推广活动

### 企业级基础设施

Docker Verified Publisher Program 运行在 Docker Hub 的企业级基础设施上，服务于全球数百万开发者。您发布的内容受益于：

- **高可用性和正常运行时间**：Docker 的系统设计为跨多个可用区进行故障转移，具有负载均衡的自动扩展功能，可实现 99.9% 的正常运行时间。
- **全球交付和快速下载**：Docker 利用 Cloudflare 的 CDN 和缓存（配合 Cache Reserve），实现超过 99% 的缓存命中率，减少对源流量的依赖，确保全球各地的开发者都能快速访问。
- **持久性**：Docker 维护记录在案的备份策略，并对生产数据执行每日完整备份。

您只需像往常一样将镜像推送到 Docker Hub，Docker 就会处理其余的工作，将您的镜像提供给全球数百万开发者。

![Docker Hub 中的 DVP 流程](./images/dvp-hub-flow.svg)

要了解更多信息，请参阅 [Docker 的可用性](https://www.docker.com/trust/availability/)。

### 验证发布者徽章

属于该计划的镜像在 Docker Hub 上有一个特殊徽章，使用户更容易识别 Docker 已验证为高质量商业发布者的项目。

![Docker 赞助的开源徽章](../../../images/verified-publisher-badge.png)

### 仓库徽标

DVP 组织可以为 Docker Hub 上的单个仓库上传自定义图像。这允许您在每个仓库的基础上覆盖默认的组织级徽标。

要管理仓库徽标，请参阅 [管理仓库徽标](#manage-repository-logo)。

### 漏洞分析

[Docker Scout](/scout/) 为发布到 Docker Hub 的 DVP 镜像提供自动漏洞分析。
扫描镜像可确保发布的内容安全，并向开发人员证明他们可以信任该镜像。

您可以在每个仓库的基础上启用分析。有关使用此功能的更多信息，请参阅 [基本漏洞扫描](/docker-hub/repos/manage/vulnerability-scanning/)。

### 优先搜索排名

验证发布者镜像在 Docker Hub 搜索结果中获得增强的可见性，使开发人员更容易发现您的内容。这种改进的可发现性有助于推动您的镜像在开发人员社区中的采用。

### 移除速率限制

验证发布者镜像免于标准的 [Docker Hub 速率限制](../../../usage/_index.md)，确保开发人员可以不受限制地拉取您的镜像。**这适用于所有用户，包括未经身份验证的用户**，他们可以获得 DVP 镜像的无限拉取。这消除了潜在的采用障碍，并为您的内容用户提供了无缝体验。

DVP 合作伙伴可以通过在拉取其镜像时检查是否存在速率限制标头来验证这种无限访问。当拉取 DVP 镜像时，用户不会看到 `ratelimit-limit` 或 `ratelimit-remaining` 标头，这表示无限访问。有关检查速率限制的更多详细信息，请参阅 [查看拉取速率和限制](../../../usage/pulls.md#view-pull-rate-and-limit)。

### 联合营销机会

Docker 与验证发布者合作开展联合营销活动，包括博客文章、案例研究、网络研讨会和会议演示文稿。这些机会有助于在 Docker 生态系统中扩大您的品牌知名度。

### 洞察与分析

洞察与分析服务提供社区使用 Docker 镜像的使用指标，从而深入了解用户行为。

有一个 [Web 界面](./insights-analytics.md) 和一个 [API](/reference/api/dvp/latest/) 用于访问分析数据。

使用指标显示按标签或摘要、地理位置、云提供商、客户端等划分的镜像拉取次数。

## 管理仓库徽标

加入 Docker Verified Publisher Program 后，您可以为组织中的每个仓库设置自定义徽标。适用以下要求：

- 徽标图像支持的文件类型为 JPEG 和 PNG。
- 允许的最小图像尺寸（像素）为 120×120。
- 允许的最大图像尺寸（像素）为 1000×1000。
- 允许的最大图像文件大小为 5MB。

只有拥有组织所有者或编辑者角色的用户才能更改仓库徽标。

### 设置仓库徽标

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 转到您要更改徽标的仓库页面。
3. 选择上传徽标按钮，该按钮由一个相机图标 ({{< inline-image
   src="../../../images/upload_logo_sm.png" alt="camera icon" >}}) 表示，该图标覆盖在当前仓库徽标上。
4. 在打开的对话框中，选择您要上传的 PNG 图像，将其设置为仓库的徽标。

### 移除徽标

选择 **Clear** 按钮 ({{< inline-image src="../../../images/clear_logo_sm.png"
alt="clear button" >}}) 以移除徽标。

移除徽标后，仓库将默认使用组织徽标（如果已设置），或者使用以下默认徽标（如果未设置）。

![默认徽标是一个灰色的 3D 立方体](../../../images/default_logo_sm.png)