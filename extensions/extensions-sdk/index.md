---
title: 扩展 SDK 概览
url: /extensions/extensions-sdk/
parent:
  title: Docker 扩展
  url: /extensions/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker 扩展
    url: /extensions/
  - title: 扩展 SDK 概览
    url: /extensions/extensions-sdk/
children:
  - title: 构建和发布流程
    url: /extensions/extensions-sdk/process/
    description: 了解创建扩展的过程。
  - title: 快速入门
    url: /extensions/extensions-sdk/quickstart/
    description: 快速构建扩展的指南
  - title: 第二部分：发布
    url: /extensions/extensions-sdk/extensions/
    description: 发布扩展的一般步骤
  - title: 扩展架构
    url: /extensions/extensions-sdk/architecture/
    description: Docker 扩展架构
  - title: Docker 扩展的 UI 样式概览
    url: /extensions/extensions-sdk/design/
    description: Docker 扩展设计
  - title: 
    url: /extensions/extensions-sdk/dev/
---


本节中的资源可帮助您创建自己的 Docker 扩展。

Docker CLI 工具提供了一组命令来帮助您构建和发布扩展，这些扩展被打包为特殊格式的 Docker 镜像。

镜像文件系统的根目录下有一个 `metadata.json` 文件，用于描述扩展的内容。这是 Docker 扩展的基本要素。

扩展可以包含 UI 部分和在主机或 Desktop 虚拟机中运行的后端部分。更多信息请参阅 [架构](architecture/_index.md)。

您可以通过 Docker Hub 分发扩展。不过，您也可以在本地开发扩展，而无需将扩展推送到 Docker Hub。详情请参阅 [扩展分发](extensions/DISTRIBUTION.md)。



> 已经构建了一个扩展？
>
> 请通过 [反馈表单](https://survey.alchemer.com/s3/7184948/Publishers-Feedback-Form) 告诉我们您的使用体验。


