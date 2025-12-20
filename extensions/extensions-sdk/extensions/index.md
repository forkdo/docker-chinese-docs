# 第二部分：发布

本节介绍如何让您的扩展更可用、更显眼，以便用户能够发现它并一键安装。

## 发布您的扩展

在开发完扩展并在本地测试后，您就可以发布该扩展，使其可供他人安装和使用（无论是团队内部使用还是更公开地使用）。

发布扩展包括以下步骤：

- 提供有关扩展的信息：描述、截图等，以便用户决定是否安装您的扩展
- [验证](validate.md) 扩展是否以正确的格式构建并包含所需的信息
- 使扩展镜像在 [Docker Hub](https://hub.docker.com/) 上可用

有关发布过程的更多详细信息，请参阅 [打包和发布您的扩展](DISTRIBUTION.md)。

## 推广您的扩展

一旦您的扩展在 Docker Hub 上可用，有权访问该扩展镜像的用户就可以使用 Docker CLI 安装它。

### 使用共享扩展链接

您还可以[生成共享 URL](share.md)，以便在团队内部共享您的扩展，或在互联网上推广您的扩展。共享链接允许用户查看扩展描述和截图。

### 在 Marketplace 中发布您的扩展

您可以在扩展 Marketplace 中发布您的扩展，以使其更容易被发现。如果您希望在 Marketplace 中发布您的扩展，则必须[提交您的扩展](publish.md)。

## 后续步骤

### 新版本发布

发布扩展后，只需推送带有递增标签（仍使用 `semver` 约定）的新版本扩展镜像即可推送新版本。在 Marketplace 中发布的扩展可以受益于更新通知，该通知会发送给所有已安装该扩展的 Desktop 用户。更多详情，请参阅 [新版本和更新](DISTRIBUTION.md#new-releases-and-updates)。

### 扩展支持和用户反馈

除了提供扩展功能描述和截图外，您还应该使用[扩展标签](labels.md)指定额外的 URL。这可以引导用户访问您的网站以报告错误和反馈，以及访问文档和支持。



> 已经构建了一个扩展？
>
> 请通过 [反馈表单](https://survey.alchemer.com/s3/7184948/Publishers-Feedback-Form) 告诉我们您的使用体验。

- [扩展镜像标签](https://docs.docker.com/extensions/extensions-sdk/extensions/labels/)

- [验证您的扩展](https://docs.docker.com/extensions/extensions-sdk/extensions/validate/)

- [打包并发布您的扩展](https://docs.docker.com/extensions/extensions-sdk/extensions/DISTRIBUTION/)

- [分享你的扩展](https://docs.docker.com/extensions/extensions-sdk/extensions/share/)

- [在 Marketplace 中发布](https://docs.docker.com/extensions/extensions-sdk/extensions/publish/)

- [构建多架构扩展](https://docs.docker.com/extensions/extensions-sdk/extensions/multi-arch/)

