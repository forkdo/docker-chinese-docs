# 扩展 SDK 概览


> [!IMPORTANT]
>
> 在 Docker 审查 Marketplace 安全性期间，暂停向 Docker 扩展 Marketplace 提交新扩展。您仍然可以更新现有扩展，私有 Marketplace 扩展不受影响。如果您有其他疑问，请联系 extensions@docker.com。

本节中的资源可帮助您创建自己的 Docker 扩展。

Docker CLI 工具提供了一组命令来帮助您构建和发布扩展，这些扩展被打包为特殊格式的 Docker 镜像。

镜像文件系统的根目录下有一个 `metadata.json` 文件，用于描述扩展的内容。这是 Docker 扩展的基本要素。

扩展可以包含 UI 部分和在主机或 Desktop 虚拟机中运行的后端部分。更多信息请参阅 [架构](architecture/_index.md)。

您可以通过 Docker Hub 分发扩展。不过，您也可以在本地开发扩展，而无需将扩展推送到 Docker Hub。详情请参阅 [扩展分发](extensions/DISTRIBUTION.md)。





> 已经构建了一个扩展？
>
> 请通过 [反馈表单](https://survey.alchemer.com/s3/7184948/Publishers-Feedback-Form) 告诉我们您的使用体验。




