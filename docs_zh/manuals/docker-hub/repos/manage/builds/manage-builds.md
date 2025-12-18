---
title: 管理自动构建
description: 如何在 Docker Hub 中管理自动构建
keywords: 自动构建, 自动化, docker hub, 仓库
aliases:
- /docker-hub/builds/manage-builds/
---

> [!NOTE]
>
> 自动化构建需要 Docker Pro、Team 或 Business 订阅。


## 取消或重试构建

在构建排队或运行期间，其构建报告链接旁边会显示一个 **Cancel** 图标，位置在 **General** 选项卡和 **Builds** 选项卡上。您也可以在 **Build report** 页面上或从 **Timeline** 选项卡的日志显示中选择 **Cancel**。

![显示取消图标的构建列表](images/build-cancelicon.png)

## 查看您的活跃构建

仓库构建的摘要会同时显示在仓库的 **General** 选项卡和 **Builds** 选项卡上。**Builds** 选项卡还显示了构建队列时间和持续时间的彩色条形图。这两种视图都会显示仓库任何标签的待处理、进行中、成功和失败的构建。

![活跃构建](images/index-active.png)

从任一位置，您都可以选择一个构建任务来查看其构建报告。构建报告显示有关构建任务的信息，包括源仓库和分支或标签、构建日志、构建持续时间、创建时间和位置，以及发生构建的用户账户。

> [!NOTE]
>
> 现在，当您刷新 **Builds** 页面时，可以每 30 秒查看一次构建的进度。借助进行中的构建日志，您可以在构建完成之前调试构建。

![构建报告](./images/index-report.png)

## 禁用自动化构建

自动化构建按分支或标签启用，可以禁用和重新启用。例如，当您想暂时只进行手动构建时（比如正在对代码进行重大重构），可能会这样做。禁用自动构建不会禁用 [autotests](automated-testing.md)。

要禁用自动化构建：

1. 在 [Docker Hub](https://hub.docker.com) 中，转到 **My Hub** > **Repositories**，选择一个仓库，然后选择 **Builds** 选项卡。

2. 选择 **Configure automated builds** 以编辑仓库的构建设置。

3. 在 **Build Rules** 部分，找到您不再希望自动构建的分支或标签。

4. 选择配置行旁边的 **Autobuild** 切换按钮。禁用后，切换按钮会变为灰色。

5. 选择 **Save**。