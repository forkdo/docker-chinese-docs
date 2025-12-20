# 借助容器支持的开发实现更快速的开发与测试

容器提供了一种一致的方式来跨不同环境构建、共享和运行应用。虽然容器通常用于将你的应用容器化，但它们也使得运行开发所需的关键服务变得异常简单。你可以轻松启动自己的数据库，而无需安装或连接到远程数据库。但这还只是冰山一角。

通过容器支持的开发，你可以使用容器来增强开发环境，方法是模拟或运行应用所需的各种服务的本地实例。这能够提供更快的反馈循环、降低与远程服务的耦合度，并增强测试错误状态的能力。

最重要的是，无论正在开发的主应用是否运行在容器中，你都可以享受这些好处。

## 你将学到什么

- 容器支持开发的含义
- 如何将非容器化应用连接到容器化服务
- 多个使用容器来模拟或运行服务本地实例的示例
- 如何使用容器为开发环境添加额外的故障排查和调试工具

## 适合谁？

- 希望减少对共享或已部署基础设施或远程 API 端点依赖的团队
- 希望在开发过程中减少直接使用云服务所带来的复杂性和成本的团队
- 希望更轻松地可视化数据库、队列等内部情况的开发者
- 希望在不影响应用本身开发的前提下，降低开发环境设置复杂性的团队

## 工具集成

与 Docker Compose 和 Testcontainers 配合使用效果良好。

## 模块

### 什么是容器支持的开发？

容器支持的开发是指使用容器来增强开发环境，方法是运行应用所依赖的各种服务的本地实例或模拟器。一旦开始使用容器，就可以轻松添加额外的服务来可视化或排查服务中的问题。

<div id="youtube-player-pNcrto_wGi0" data-video-id="pNcrto_wGi0" class="youtube-video aspect-video h-fit w-full py-2">
</div>


### 演示：在本地运行数据库

通过容器支持的开发，可以轻松在本地运行数据库。在本演示中，你将看到如何做到这一点，以及如何将非容器化应用连接到数据库。

<div id="youtube-player-VieWeXOwKLU" data-video-id="VieWeXOwKLU" class="youtube-video aspect-video h-fit w-full py-2">
</div>


> [!TIP]
>
> 在[使用容器化数据库](/guides/databases.md)指南中了解更多关于在容器中运行数据库的信息。

### 演示：模拟 API 端点

许多 API 需要来自其他数据端点的数据。在开发过程中，这会带来诸如凭据共享、可用性/正常运行时间以及速率限制等复杂性。与其直接依赖这些服务，你的应用可以与一个模拟 API 服务器进行交互。

本演示将展示如何使用 WireMock 轻松开发和测试应用，包括 API 的各种错误状态。

<div id="youtube-player-VXSmX6f8vo0" data-video-id="VXSmX6f8vo0" class="youtube-video aspect-video h-fit w-full py-2">
</div>


> [!TIP]
>
> 在[使用 WireMock 模拟 API 服务](/guides/wiremock.md)指南中了解更多关于使用 WireMock 模拟 API 的信息。

### 演示：在本地开发云应用

在开发应用时，通常更容易将应用的某些方面外包给云服务，例如 Amazon S3。然而，在本地开发中连接这些服务会引入 IAM 策略、网络限制和配置复杂性等问题。虽然这些要求在生产环境中很重要，但它们会显著增加开发环境的复杂性。

通过容器支持的开发，你可以在开发和测试期间运行这些服务的本地实例，从而无需复杂的设置。在本演示中，你将看到 LocalStack 如何让开发者能够完全在本地工作站上开发和测试应用。

<div id="youtube-player-JtwUMvR5xlY" data-video-id="JtwUMvR5xlY" class="youtube-video aspect-video h-fit w-full py-2">
</div>


> [!TIP]
>
> 在[使用 LocalStack 开发和测试 AWS 云应用](/guides/localstack.md)指南中了解更多关于使用 LocalStack 的信息。

### 演示：添加额外的调试和故障排查工具

一旦开始在开发环境中使用容器，就可以轻松添加额外的容器来可视化数据库或消息队列的内容、填充文档存储或事件发布者。在本演示中，你将看到其中的一些示例，以及如何将多个容器连接在一起，使测试变得更加容易。

<div id="youtube-player-TCZX15aKSu4" data-video-id="TCZX15aKSu4" class="youtube-video aspect-video h-fit w-full py-2">
</div>


<div id="lp-survey-anchor"></div>
