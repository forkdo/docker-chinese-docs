---
description: 了解在 Docker 仪表板的卷视图中可以执行哪些操作
keywords: Docker Desktop Dashboard, manage, containers, gui, dashboard, volumes, user manual
title: 在 Docker Desktop 中探索卷视图
linkTitle: Volumes
weight: 30
---

Docker Desktop 中的 **Volumes**（卷）视图允许您创建、检查、删除、克隆、清空、导出和导入 [Docker 卷](/manuals/engine/storage/volumes.md)。您还可以浏览卷中的文件和文件夹，并查看哪些容器正在使用它们。

## 查看您的卷

您可以查看有关卷的以下信息：

- **名称 (Name)**：卷的名称。
- **状态 (Status)**：卷是否正在被容器使用。
- **创建时间 (Created)**：卷创建于多久之前。
- **大小 (Size)**：卷的大小。
- **计划导出 (Scheduled exports)**：计划导出是否处于活动状态。

默认情况下，**Volumes** 视图会显示所有卷的列表。

您可以通过以下方式筛选和排序卷，以及修改显示的列：

- **按名称筛选卷**：使用 **搜索 (Search)** 字段。
- **按状态筛选卷**：在搜索栏右侧，按 **正在使用 (In use)** 或 **未使用 (Unused)** 筛选卷。
- **排序卷**：选择列名对卷进行排序。
- **自定义列**：在搜索栏右侧，选择要显示的卷信息。

## 创建卷

您可以使用以下步骤创建一个空卷。或者，如果您[启动一个带有卷的容器](/manuals/engine/storage/volumes.md#start-a-container-with-a-volume)而该卷尚不存在，Docker 会为您创建该卷。

创建卷的步骤：

1. 在 **Volumes** 视图中，选择 **Create**（创建）按钮。
2. 在 **New Volume**（新卷）模态框中，指定卷名称，然后选择 **Create**（创建）。

要将卷与容器一起使用，请参阅[使用卷](/manuals/engine/storage/volumes.md#start-a-container-with-a-volume)。

## 检查卷

要探索特定卷的详细信息，请从列表中选择一个卷。这将打开详细视图。

**Container in-use**（正在使用的容器）选项卡显示使用该卷的容器名称、镜像名称、容器使用的端口号以及目标路径。目标路径是容器内部的路径，用于访问卷中的文件。

**Stored data**（存储的数据）选项卡显示卷中的文件和文件夹以及文件大小。要保存文件或文件夹，请右键单击文件或文件夹以显示选项菜单，选择 **Save as...**（另存为...），然后指定位置以下载文件。

要从卷中删除文件或文件夹，请右键单击文件或文件夹以显示选项菜单，选择 **Delete**（删除），然后再次选择 **Delete**（删除）以确认。

**Exports**（导出）选项卡允许您[导出卷](#export-a-volume)。

## 克隆卷

克隆卷会创建一个包含克隆卷所有数据副本的新卷。当克隆一个或多个正在运行的容器正在使用的卷时，容器会在 Docker 克隆数据时暂时停止，并在克隆过程完成后重新启动。

克隆卷的步骤：

1. 登录 Docker Desktop。您必须登录才能克隆卷。
2. 在 **Volumes** 视图中，找到要克隆的卷，在 **Actions**（操作）列中选择 **Clone**（克隆）图标。
3. 在 **Clone a volume**（克隆卷）模态框中，指定 **Volume name**（卷名称），然后选择 **Clone**（克隆）。

## 删除一个或多个卷

删除卷会删除该卷及其所有数据。当容器正在使用某个卷时，即使容器已停止，您也无法删除该卷。您必须先停止并移除使用该卷的所有容器，然后才能删除该卷。

删除卷的步骤：

1. 在 **Volumes** 视图中，找到要删除的卷，在 **Actions**（操作）列中选择 **Delete**（删除）图标。
2. 在 **Delete volume?**（删除卷？）模态框中，选择 **Delete forever**（永久删除）。

删除多个卷的步骤：

1. 在 **Volumes** 视图中，选中要删除的所有卷旁边的复选框。
2. 选择 **Delete**（删除）。
3. 在 **Delete volumes?**（删除卷？）模态框中，选择 **Delete forever**（永久删除）。

## 清空卷

清空卷会删除卷的所有数据，但不会删除卷本身。当清空一个或多个正在运行的容器正在使用的卷时，容器会在 Docker 清空数据时暂时停止，并在清空过程完成后重新启动。

清空卷的步骤：

1. 登录 Docker Desktop。您必须登录才能清空卷。
2. 在 **Volumes** 视图中，选择要清空的卷。
3. 在 **Import**（导入）旁边，选择 **More volume actions**（更多卷操作）图标，然后选择 **Empty volume**（清空卷）。
4. 在 **Empty a volume?**（清空卷？）模态框中，选择 **Empty**（清空）。

## 导出卷

您可以将卷的内容导出到本地文件、本地镜像、Docker Hub 中的镜像或受支持的云提供商。当导出一个或多个正在运行的容器正在使用的卷的内容时，容器会在 Docker 导出内容时暂时停止，并在导出过程完成后重新启动。

您可以选择[立即导出卷](#export-a-volume-now)或[计划定期导出](#schedule-a-volume-export)。

### 立即导出卷

1. 登录 Docker Desktop。您必须登录才能导出卷。
2. 在 **Volumes** 视图中，选择要导出的卷。
3. 选择 **Exports**（导出）选项卡。
4. 选择 **Quick export**（快速导出）。
5. 选择是将卷导出到 **Local or Hub storage**（本地或 Hub 存储）还是 **External cloud storage**（外部云存储），然后根据您的选择指定以下附加详细信息。

   {{< tabs >}}
   {{< tab name="Local or Hub storage" >}}
   
   - **Local file**（本地文件）：指定文件名并选择文件夹。
   - **Local image**（本地镜像）：选择要将内容导出到的本地镜像。镜像中的任何现有数据都将被导出的内容替换。
   - **New image**（新镜像）：指定新镜像的名称。
   - **Registry**（注册表）：指定 Docker Hub 仓库。

   {{< /tab >}}
   {{< tab name="External cloud storage" >}}

   您必须拥有 [Docker Business 订阅](https://www.docker.com/pricing/)才能导出到外部云提供商。

   选择您的云提供商，然后指定上传到存储的 URL。请参阅以下针对您的云提供商的文档以了解如何获取 URL。

   - Amazon Web Services: [使用 AWS SDK 创建 Amazon S3 的预签名 URL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_Scenario_PresignedUrl_section.html)
   - Microsoft Azure: [生成 SAS 令牌和 URL](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/api/connection-strings/generate-sas-token)
   - Google Cloud: [创建用于上传对象的签名 URL](https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers#upload-object)

   {{< /tab >}}
   {{< /tabs >}}

6. 选择 **Save**（保存）。

### 计划卷导出

1. 登录 Docker Desktop。您必须登录并拥有付费的 [Docker 订阅](https://www.docker.com/pricing/)才能计划卷导出。
2. 在 **Volumes** 视图中，选择要导出的卷。
3. 选择 **Exports**（导出）选项卡。
4. 选择 **Schedule export**（计划导出）。
5. 在 **Recurrence**（重复频率）中，选择导出发生的频率，然后根据您的选择指定以下附加详细信息。

   - **Daily**（每天）：指定每天进行备份的时间。
   - **Weekly**（每周）：指定一周中的一个或多个日期以及进行备份的时间。
   - **Monthly**（每月）：指定月份中的哪一天以及进行备份的时间。

6. 选择是将卷导出到 **Local or Hub storage**（本地或 Hub 存储）还是 **External cloud storage**（外部云存储），然后根据您的选择指定以下附加详细信息。
   
   {{< tabs >}}
   {{< tab name="Local or Hub storage" >}}
   
   - **Local file**（本地文件）：指定文件名并选择文件夹。
   - **Local image**（本地镜像）：选择要将内容导出到的本地镜像。镜像中的任何现有数据都将被导出的内容替换。
   - **New image**（新镜像）：指定新镜像的名称。
   - **Registry**（注册表）：指定 Docker Hub 仓库。

   {{< /tab >}}
   {{< tab name="External cloud storage" >}}

   您必须拥有 [Docker Business 订阅](https://www.docker.com/pricing/)才能导出到外部云提供商。

   选择您的云提供商，然后指定上传到存储的 URL。请参阅以下针对您的云提供商的文档以了解如何获取 URL。

   - Amazon Web Services: [使用 AWS SDK 创建 Amazon S3 的预签名 URL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_Scenario_PresignedUrl_section.html)
   - Microsoft Azure: [生成 SAS 令牌和 URL](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/api/connection-strings/generate-sas-token)
   - Google Cloud: [创建用于上传对象的签名 URL](https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers#upload-object)

   {{< /tab >}}
   {{< /tabs >}}

7. 选择 **Save**（保存）。

## 导入卷

您可以导入本地文件、本地镜像或来自 Docker Hub 的镜像。卷中的任何现有数据都将被导入的内容替换。当将内容导入到一个或多个正在运行的容器正在使用的卷时，容器会在 Docker 导入内容时暂时停止，并在导入过程完成后重新启动。

导入卷的步骤：

1. 登录 Docker Desktop。您必须登录才能导入卷。
2. （可选）[创建](#create-a-volume)一个新的卷来导入内容。
3. 选择要将内容导入到的卷。
4. 选择 **Import**（导入）。
5. 选择内容的来源，然后根据您的选择指定以下附加详细信息：

   - **Local file**（本地文件）：选择包含内容的文件。
   - **Local image**（本地镜像）：选择包含内容的本地镜像。
   - **Registry**（注册表）：指定来自 Docker Hub 的包含内容的镜像。

6. 选择 **Import**（导入）。

## 其他资源

- [持久化容器数据](/get-started/docker-concepts/running-containers/persisting-container-data.md)
- [使用卷](/manuals/engine/storage/volumes.md)