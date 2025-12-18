---
title: 在 Marketplace 中发布
description: Docker 扩展分发
keywords: Docker, extensions, publish
aliases: 
 - /desktop/extensions-sdk/extensions/publish/
weight: 50
---

## 向 Marketplace 提交你的扩展

Docker Desktop 在 [Docker Desktop](https://open.docker.com/extensions/marketplace) 和 [Docker Hub](https://hub.docker.com/search?q=&type=extension) 的扩展 Marketplace 中显示已发布的扩展。
扩展 Marketplace 是开发者发现扩展以改善开发体验，以及提交自己扩展供所有 Desktop 用户使用的平台。

当你[准备发布](DISTRIBUTION.md)扩展到 Marketplace 时，你可以通过[自助发布流程](https://github.com/docker/extensions-submissions/issues/new?assignees=&labels=&template=1_automatic_review.yaml&title=%5BSubmission%5D%3A+)提交扩展

> [!NOTE]
>
> 随着扩展 Marketplace 持续为扩展用户和发布者添加新功能，你有责任维护你的扩展，以确保它在 Marketplace 中保持可用。

> [!IMPORTANT]
>
> Docker 扩展的人工审核流程目前暂停。请通过[自动化提交流程](https://github.com/docker/extensions-submissions/issues/new?assignees=&labels=&template=1_automatic_review.yaml&title=%5BSubmission%5D%3A+)提交你的扩展

### 提交前准备

在提交扩展之前，它必须通过[验证](validate.md)检查。

在提交扩展之前，强烈建议你的扩展遵循本节中概述的指南。如果你请求 Docker Extensions 团队进行审核但未遵循这些指南，审核过程可能会更长。

这些指南不能替代 Docker 的服务条款，也不能保证审核通过：
- 查看[设计指南](../design/design-guidelines.md)
- 确保[UI 样式](../design/_index.md)符合 Docker Desktop 指南
- 确保你的扩展支持浅色和深色模式
- 考虑你的扩展新用户和老用户的需求
- 在潜在用户中测试你的扩展
- 测试扩展的崩溃、错误和性能问题
- 在各种平台（Mac、Windows、Linux）上测试扩展
- 阅读[服务条款](https://www.docker.com/legal/extensions_marketplace_developer_agreement/)

#### 验证流程

提交的扩展将经过自动化验证流程。如果所有验证检查成功通过，扩展将在几小时内发布到 Marketplace 并对所有用户可见。
这是让开发者快速获得所需工具并从他们那里获得反馈的最快方式，帮助你持续改进/完善扩展。

> [!IMPORTANT]
>
> Docker Desktop 会缓存 Marketplace 中可用扩展列表 12 小时。如果你在 Marketplace 中看不到你的扩展，可以重启 Docker Desktop 强制刷新缓存。