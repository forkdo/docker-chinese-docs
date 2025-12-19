---
title: 在 Marketplace 中发布
description: Docker 扩展分发
keywords: Docker, extensions, publish
aliases: 
 - /desktop/extensions-sdk/extensions/publish/
weight: 50
---

## 将您的扩展提交到 Marketplace

Docker Desktop 会在 [Docker Desktop](https://open.docker.com/extensions/marketplace) 和 [Docker Hub](https://hub.docker.com/search?q=&type=extension) 的扩展市场 (Extensions Marketplace) 中显示已发布的扩展。
扩展市场是一个空间，开发者可以在此发现扩展以改善其开发者体验，并提交自己的扩展供所有 Desktop 用户使用。

当您[准备好发布](DISTRIBUTION.md)您的扩展到 Marketplace 时，您可以[自行发布您的扩展](https://github.com/docker/extensions-submissions/issues/new?assignees=&labels=&template=1_automatic_review.yaml&title=%5BSubmission%5D%3A+)。

> [!NOTE]
>
> 随着扩展市场不断为扩展用户和发布者增加新功能，您需要长期维护您的扩展，以确保其在 Marketplace 中保持可用。

> [!IMPORTANT]
>
> 目前，Docker 对扩展的人工审核流程已暂停。请通过[自动化提交流程](https://github.com/docker/extensions-submissions/issues/new?assignees=&labels=&template=1_automatic_review.yaml&title=%5BSubmission%5D%3A+)提交您的扩展。

### 提交之前

在提交您的扩展之前，它必须通过[验证](validate.md)检查。

强烈建议您在提交扩展之前遵循本节概述的准则。如果您请求 Docker Extensions 团队进行审核但未遵循这些准则，审核过程可能会更长。

这些准则不能取代 Docker 的服务条款，也不能保证批准：
- 查阅[设计指南](../design/design-guidelines.md)
- 确保 [UI 样式](../design/_index.md) 符合 Docker Desktop 指南
- 确保您的扩展同时支持浅色和深色模式
- 考虑您的扩展的新用户和现有用户的需求
- 与潜在用户一起测试您的扩展
- 测试您的扩展是否存在崩溃、错误和性能问题
- 在各种平台（Mac、Windows、Linux）上测试您的扩展
- 阅读[服务条款](https://www.docker.com/legal/extensions_marketplace_developer_agreement/)

#### 验证流程

提交的扩展会经过自动化验证流程。如果所有验证检查均成功通过，该扩展将在几小时内发布到 Marketplace，并可供所有用户访问。
这是让开发者获得所需工具并从他们那里获得反馈的最快方式，以便您改进/完善您的扩展。

> [!IMPORTANT]
>
> Docker Desktop 会将 Marketplace 中可用扩展的列表缓存 12 小时。如果您在 Marketplace 中看不到您的扩展，可以重新启动 Docker Desktop 以强制刷新缓存。