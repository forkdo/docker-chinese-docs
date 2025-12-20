# 洞察 (Insights)





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Subscription:</span>
        
          <span>Business</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M80-180v-600q0-24.75 17.63-42.38Q115.25-840 140-840h270q24.75 0 42.38 17.62Q470-804.75 470-780v105h350q24.75 0 42.38 17.62Q880-639.75 880-615v435q0 24.75-17.62 42.37Q844.75-120 820-120H140q-24.75 0-42.37-17.63Q80-155.25 80-180Zm60 0h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm165 495h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm165 495h350v-435H470v105h80v60h-80v105h80v60h-80v105Zm185-270v-60h60v60h-60Zm0 165v-60h60v60h-60Z"/></svg>
            
          </span>
        
      </div>
    

    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">For:</span>
        <span>Administrators</span>
        
          <span class="icon-svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M693-80q-78 0-133-55.5T505-267q0-78 55-133.5T693-456q77 0 132.5 55.5T881-267q0 76-55.5 131.5T693-80ZM160-522v-197q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v190q0 14-11 21.5t-24 2.5q-17-5-35.5-8t-36.5-3q-103 0-175.5 73T445-267q0 40 13.5 79t38.5 71q10 13 2.5 26T478-82q-69-20-122-51.5T251-237q-43-60-67-132.5T160-522Zm531 252q26 0 44-19t18-45q0-26-18-44t-44-18q-26 0-45 18t-19 44q0 26 19 45t45 19Zm-1 125q28 0 53-11t43-31q4-5 2.5-11t-6.5-8q-22-10-45-15.5t-47-5.5q-24 0-47 5t-45 16q-5 2-7 8t2 11q18 21 43.5 31.5T690-145Z"/></svg>
          </span>
        
      </div>
    
  </div>



Insights 帮助管理员可视化并了解 Docker 在其组织内的使用情况。通过 Insights，管理员可以确保其团队完全有能力充分利用 Docker，从而提高整个组织的生产力和效率。

主要优势包括：

- 统一的工作环境：在团队之间建立并维护标准化的配置。
- 最佳实践：推广并强制执行使用指南，以确保最佳性能。
- 提高可见性：监控并推动组织配置和策略的采用。
- 优化许可证使用：确保开发人员能够访问 Docker 订阅提供的高级功能。

## 先决条件

要使用 Insights，您必须满足以下要求：

- [Docker Business 订阅](https://www.docker.com/pricing/)
- 管理员必须[强制用户登录](/security/for-admins/enforce-sign-in/)
- 您的客户经理 (Account Executive) 必须为您的组织开启 Insights

## 查看组织用户的洞察数据

要访问 Insights，请联系您的客户经理 (Account Executive) 以开启该功能。功能开启后，请按照以下步骤访问 Insights：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Insights**，然后选择数据的时间段。

> [!NOTE]
>
> Insights 数据不是实时的，而是每日更新。在 Insights 页面的右上角，查看**最后更新**日期以了解数据的最后更新时间。

Insights 数据显示在以下图表中：

 - [Docker Desktop 用户](#docker-desktop-users)
 - [构建 (Builds)](#builds)
 - [容器 (Containers)](#containers)
 - [Docker Desktop 使用情况](#docker-desktop-usage)
 - [Docker Hub 镜像](#docker-hub-images)
 - [扩展 (Extensions)](#extensions)

### Docker Desktop 用户

跟踪您域中的活跃 Docker Desktop 用户，按许可证状态区分。此图表帮助您了解组织内的参与度，提供有关有多少用户正在积极使用 Docker Desktop 的洞察。请注意，选择退出分析的用户不包含在活跃计数中。

该图表包含以下数据：

| 数据 | 描述 |
|:-----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 活跃用户 (Active user) | 曾积极使用过 Docker Desktop 的用户数量，这些用户使用您组织内拥有许可证的 Docker 账户登录，或者使用与您组织关联的域中的电子邮件地址登录的 Docker 账户。<br><br>未登录与您组织关联的账户的用户不会显示在数据中。为确保用户使用与您组织关联的账户登录，您可以[强制登录](/security/for-admins/enforce-sign-in/)。 |
| 组织成员总数 (Total organization members) | 使用过 Docker Desktop 的用户数量，无论其 Insights 活动如何。 |
| 选择退出分析的用户 (Users opted out of analytics) | 属于您组织成员但选择退出发送分析的用户数量。<br><br>当用户选择退出发送分析时，您将不会在 Insights 中看到他们的任何数据。为确保数据包含所有用户，您可以使用[设置管理](/desktop/hardened-desktop/settings-management/)为所有用户设置 `analyticsEnabled`。 |
| 活跃用户（图表） (Active users (graph)) | 总活跃用户随时间变化的视图。 |

### 构建 (Builds)

通过此图表监控开发效率和团队在构建上投入的时间。它提供了构建活动的清晰视图，帮助您识别模式、优化构建时间并提高整体开发生产力。

该图表包含以下数据：

| 数据 | 描述 |
|:-----------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 每用户平均构建次数 (Average build per user) | 每个活跃用户的平均构建次数。构建包括用户运行以下任一命令的任何时间：<ul><li>`docker build`</li><li>`docker buildx b`</li><li>`docker buildx bake`</li><li>`docker buildx build`</li><li>`docker buildx f`</li><li>`docker builder b`</li><li>`docker builder bake`</li><li>`docker builder build`</li><li>`docker builder f`</li><li>`docker compose build`</li><li>`docker compose up --build`</li><li>`docker image build`</li></ul> |
| 平均构建时间 (Average build time) | 每次构建的平均构建时间。 |
| 构建成功率 (Build success rate) | 成功构建占总构建次数的百分比。成功构建包括任何正常退出的构建。 |
| 总构建次数（图表） (Total builds (graph)) | 总构建次数，分为成功构建和失败构建。成功构建包括任何正常退出的构建。失败构建包括任何异常退出的构建。 |

### 容器 (Containers)

通过此图表查看用户运行的容器总数和平均数。它让您可以衡量整个组织的容器使用情况，帮助您了解使用趋势并有效管理资源。

该图表包含以下数据：

| 数据 | 描述 |
|:---------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 运行的容器总数 (Total containers run) | 活跃用户运行的容器总数。运行的容器包括使用 Docker Desktop 图形用户界面、`docker run` 或 `docker compose` 运行的容器。 |
| 平均运行容器数 (Average number of containers run) | 每个活跃用户运行的平均容器数。 |
| 活跃用户运行的容器数（图表） (Containers run by active users (graph)) | 活跃用户随时间运行的容器数量。 |

### Docker Desktop 使用情况

通过此图表探索 Docker Desktop 的使用模式，以优化团队的工作流程并确保兼容性。它提供了有关 Docker Desktop 如何被利用的宝贵见解，使您能够简化流程并提高效率。

该图表包含以下数据：

| 数据 | 描述 |
|:----------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 最常用版本 (Most used version) | 您组织中用户最常用的 Docker Desktop 版本。 |
| 最常用操作系统 (Most used OS) | 用户最常用的操作系统。 |
| 按活跃用户划分的版本（图表） (Versions by active users (graph)) | 使用每个 Docker Desktop 版本的活跃用户数量。<br><br>要了解每个版本和发布日期的更多信息，请参阅 [Docker Desktop 发行说明](/desktop/release-notes/)。 |
| 按活跃用户划分的界面（图表） (Interface by active users (graph)) | 按用于与 Docker Desktop 交互的界面类型分组的活跃用户数量。<br><br>CLI 用户是指运行过 `docker` 命令的任何活跃用户。GUI 用户是指与 Docker Desktop 图形用户界面交互过的任何活跃用户。 |

### Docker Hub 镜像

通过此图表分析镜像分发活动，并查看您域中最常用的 Docker Hub 镜像。此信息帮助您管理镜像使用情况，确保最关键的资源随时可用并被高效使用。

> [!NOTE]
>
> 镜像数据仅适用于 Docker Hub。不包含第三方注册表和镜像的数据。

该图表包含以下数据：

| 数据 | 描述 |
|:---------------------|:----------------------------------------------------------------------------------------------------------------|
| 拉取的镜像总数 (Total pulled images) | 用户从 Docker Hub 拉取的镜像总数。 |
| 推送的镜像总数 (Total pushed images) | 用户推送到 Docker Hub 的镜像总数。 |
| 拉取次数排名前 10 的镜像 (Top 10 pulled images) | 用户从 Docker Hub 拉取次数排名前 10 的镜像列表，以及每个镜像被拉取的次数。 |

### 扩展 (Extensions)

通过此图表监控扩展安装活动。它提供了对团队正在使用的 Docker Desktop 扩展的可见性，让您能够跟踪采用情况并识别提高生产力的流行工具。

该图表包含以下数据：

| 数据 | 描述 |
|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| 安装了扩展的组织百分比 (Percentage of org with extensions installed) | 您组织中至少安装了一个 Docker Desktop 扩展的用户百分比。 |
| 组织中安装次数排名前 5 的扩展 (Top 5 extensions installed in the organization) | 您组织中用户安装次数排名前 5 的 Docker Desktop 扩展列表，以及安装了每个扩展的用户数量。 |

## 导出 Docker Desktop 用户数据

您可以将 Docker Desktop 用户数据导出为 CSV 文件：

1. 打开 [Docker Home](https://app.docker.com) 并从左上角的账户下拉菜单中选择您的组织。
2. 在左侧导航菜单中选择 **Admin Console**。
3. 选择 **Desktop insights**。
4. 为您的洞察数据选择一个时间段：**1 周**、**1 个月**或**3 个月**。
5. 选择 **Export**，然后从下拉菜单中选择 **Docker Desktop users**。

您的导出将自动下载。打开文件以查看导出数据。

### 理解导出数据

Docker Desktop 用户导出文件包含以下数据点：

- Name：用户姓名
- Username：用户的 Docker ID
- Email：与用户 Docker ID 关联的电子邮件地址
- Type：用户类型
- Role：用户[角色](/manuals/enterprise/security/roles-and-permissions.md)
- Teams：用户所属的您组织内的团队
- Date Joined：用户加入您组织的日期
- Last Logged-In Date：用户上次使用其 Web 浏览器登录 Docker 的日期（这包括 Docker Hub 和 Docker Home）
- Docker Desktop Version：用户已安装的 Docker Desktop 版本
- Last Seen Date：用户上次使用 Docker Desktop 应用程序的日期
- Opted Out Analytics：用户是否在 Docker Desktop 中选择退出[发送使用统计信息](/manuals/enterprise/security/hardened-desktop/settings-management/settings-reference.md#send-usage-statistics)设置

## 故障排除 Insights

如果您在 Insights 中遇到数据问题，请考虑以下解决方案来解决常见问题：

- 将用户更新到最新版本的 Docker Desktop。

   使用 4.16 或更低版本 Docker Desktop 的用户不会显示数据。此外，旧版本可能无法提供所有数据。确保所有用户都已安装最新版本的 Docker Desktop。

- 为所有用户在 Docker Desktop 中开启**发送使用统计信息**。

   如果用户选择退出发送 Docker Desktop 的使用统计信息，那么他们的使用数据将不会成为 Insights 的一部分。要为所有用户大规模管理此设置，您可以使用[设置管理](/desktop/hardened-desktop/settings-management/)并开启 `analyticsEnabled` 设置。

- 确保用户使用 Docker Desktop，而不是使用独立版本的 Docker Engine。

   只有 Docker Desktop 才能为 Insights 提供数据。如果用户在 Docker Desktop 之外安装了 Docker Engine，Docker Engine 将不会为该用户提供数据。

- 确保用户登录到与您组织关联的账户。

   未登录与您组织关联的账户的用户不会显示在数据中。为确保用户使用与您组织关联的账户登录，您可以[强制登录](/security/for-admins/enforce-sign-in/)。
