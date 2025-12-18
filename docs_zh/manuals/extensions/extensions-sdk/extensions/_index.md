---
title: "第二部分：发布"
description: 如何发布扩展的一般步骤
keywords: Docker, Extensions, sdk, publish
aliases:
 - /desktop/extensions-sdk/extensions/
weight: 40
---

本节介绍如何让你的扩展可用并提高其可见性，以便用户可以发现并一键安装使用。

## 发布你的扩展

在开发并完成本地测试后，你就可以发布扩展，让其他人安装和使用（可以是团队内部，也可以是更广泛的公开场景）。

发布扩展包括：

- 提供扩展的相关信息：描述、截图等，帮助用户决定是否安装你的扩展
- [验证](validate.md) 扩展是否符合正确的格式要求，并包含必要信息
- 将扩展镜像发布到 [Docker Hub](https://hub.docker.com/)

更多发布流程详情，请参阅 [打包和发布你的扩展](DISTRIBUTION.md)。

## 推广你的扩展

扩展发布到 Docker Hub 后，拥有该镜像访问权限的用户即可通过 Docker CLI 安装使用。

### 使用共享扩展链接

你也可以[生成一个共享 URL](share.md)，在团队内部分享，或在互联网上推广你的扩展。共享链接允许用户查看扩展的描述和截图。

### 在 Marketplace 中发布扩展

你可以将扩展发布到 Extensions Marketplace，以提高其可发现性。如果希望扩展出现在 Marketplace 中，必须[提交你的扩展](publish.md)。

## 后续事项

### 新版本发布

扩展发布后，只需推送带有递增标签（仍遵循 `semver` 规范）的新版本镜像，即可发布新版本。
发布在 Marketplace 的扩展支持更新通知，所有已安装该扩展的 Desktop 用户将收到提示。更多详情请参阅 [新版本和更新](DISTRIBUTION.md#new-releases-and-updates)。

### 扩展支持和用户反馈

除了提供扩展功能描述和截图外，还应使用[扩展标签](labels.md)指定额外的 URL，引导用户前往你的网站报告问题、提交反馈，以及获取文档和支持。

{{% include "extensions-form.md" %}}