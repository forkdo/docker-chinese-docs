# Insights（洞察）




Insights 帮助管理员可视化并了解 Docker 在其组织内的使用情况。借助 Insights，管理员可以确保团队充分具备发挥 Docker 最大潜力的条件，从而提升整个组织的生产力和效率。

主要优势包括：

- 统一的工作环境：在各团队间建立并维护标准化的配置。
- 最佳实践：推广并强制执行使用指南，以确保最佳性能。
- 提升可见性：监控并推动组织配置和策略的采用。
- 优化许可证使用：确保开发人员能够访问 Docker 订阅提供的进阶功能。

## Prerequisites（先决条件）

要使用 Insights，你必须满足以下要求：

- [Docker Business 订阅](https://www.docker.com/pricing?ref=Docs&refAction=DocsAdminInsights)
- 管理员必须为用户[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)
- 你的客户主管（Account Executive）必须为你的组织开启 Insights

## View Insights for organization users（查看组织用户的 Insights）

要访问 Insights，请联系你的客户主管开启该功能。启用后，使用以下步骤访问 Insights：

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的组织。
2. 选择 **Insights**，然后选择你要查看数据的时间段。

> [!NOTE]
>
> Insights 数据不是实时的，每日更新。在 Insights 页面右上角，查看 **Last updated（最后更新）** 日期以了解数据最后更新的时间。

### Docker Desktop users（Docker Desktop 用户）

跟踪你域名内的活跃 Docker Desktop 用户，按许可证状态区分。此图表帮助你了解组织内的参与度，提供有多少用户正在活跃使用 Docker Desktop 的洞察。请注意，选择退出分析（analytics）的用户不计入活跃用户数。

该图表包含以下数据：

| 数据                         | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Active user（活跃用户）                  | 已活跃使用 Docker Desktop 且使用组织中拥有许可证的 Docker 账户登录，或使用与你的组织关联的域名中的电子邮件地址登录 Docker 账户的用户的用户数。 <br><br>未使用与你的组织关联的账户登录的用户不会体现在数据中。为确保用户使用与你的组织关联的账户登录，你可以[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。 |
| Total organization members（组织成员总数）   | 已使用 Docker Desktop 的用户数，无论其 Insights 活动如何。                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Users opted out of analytics（退出分析的用户数） | 作为你组织成员并选择退出发送分析数据的用户数。 <br><br>当用户选择退出发送分析数据时，你不会在 Insights 中看到他们的任何数据。为确保数据包含所有用户，你可以使用 [Settings Management](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 为所有用户设置 `analyticsEnabled`。                                                                                                                           |
| Active users (graph)（活跃用户（图表））         | 总活跃用户随时间的视图。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

### Builds（构建）

通过此图表监控开发效率以及你的团队在构建上投入的时间。它清晰地展示了构建活动，帮助你识别模式、优化构建时间并提升整体开发生产力。

该图表包含以下数据：

| 数据                   | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Average build per user（每用户平均构建数） | 每个活跃用户的平均构建数。构建包括用户运行以下任一命令的情况： <ul><li>`docker build`</li><li>`docker buildx b`</li><li>`docker buildx bake`</li><li>`docker buildx build`</li><li>`docker buildx f`</li><li>`docker builder b`</li><li>`docker builder bake`</li><li>`docker builder build`</li><li>`docker builder f`</li><li>`docker compose build`</li><li>`docker compose up --build`</li><li>`docker image build`</li></ul> |
| Average build time（平均构建时间）     | 每次构建的平均构建时间。                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Build success rate（构建成功率）     | 成功构建数占总构建数的百分比。成功的构建包括任何正常退出的构建。                                                                                                                                                                                                                                                                                                                                           |
| Total builds (graph)（总构建数（图表））   | 总构建数，分为成功构建和失败构建。成功的构建包括任何正常退出的构建。失败的构建包括任何异常退出的构建。                                                                                                                                                                                                                                                                                    |

### Containers（容器）

通过此图表查看用户运行容器的总数和平均数。它让你能够衡量组织内的容器使用情况，帮助你了解使用趋势并有效管理资源。

该图表包含以下数据：

| 数据                                   | 描述                                                                                                                                                                |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Total containers run（运行容器总数）                   | 活跃用户运行的容器总数。运行的容器包括使用 Docker Desktop 图形用户界面、`docker run` 或 `docker compose` 运行的容器。 |
| Average number of containers run（平均运行容器数）       | 每个活跃用户运行的平均容器数。                                                                                                                      |
| Containers run by active users (graph)（活跃用户运行的容器数（图表）） | 活跃用户随时间运行的容器数。                                                                                                                    |

### Docker Desktop usage（Docker Desktop 使用情况）

通过此图表探索 Docker Desktop 使用模式，以优化团队的工作流并确保兼容性。它提供关于 Docker Desktop 如何被使用的宝贵洞察，使你能够简化流程并提高效率。

该图表包含以下数据：

| 数据                              | 描述                                                                                                                                                                                                                                                                       |
| :-------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Most used version（最常用的版本）                 | 组织内用户使用最多的 Docker Desktop 版本。                                                                                                                                                                                                            |
| Most used OS（最常用的操作系统）                      | 用户使用最多的操作系统。                                                                                                                                                                                                                                          |
| Versions by active users (graph)（按活跃用户的版本（图表））  | 使用每个 Docker Desktop 版本的活跃用户数。 <br><br>要了解每个版本和发布日期的更多信息，请参阅 [Docker Desktop 发布说明](/manuals/desktop/release-notes.md)。                                                                           |
| Interface by active users (graph)（按活跃用户的界面（图表）） | 按用于与 Docker Desktop 交互的界面类型分组的活跃用户数。 <br><br>CLI 用户是任何运行过 `docker` 命令的活跃用户。GUI 用户是任何与 Docker Desktop 图形用户界面交互过的活跃用户。 |

### Docker Hub images（Docker Hub 镜像）

通过此图表分析镜像分发活动，并查看你域名内使用最多的 Docker Hub 镜像。这些信息帮助你管理镜像使用，确保最关键资源随时可用并被高效使用。

> [!NOTE]
>
> 镜像数据仅针对 Docker Hub。第三方注册表和镜像的数据不包含在内。

该图表包含以下数据：

| 数据                 | 描述                                                                                                     |
| :------------------- | :-------------------------------------------------------------------------------------------------------------- |
| Total pulled images（拉取镜像总数）  | 用户从 Docker Hub 拉取的镜像总数。                                                     |
| Total pushed images（推送镜像总数）  | 用户推送到 Docker Hub 的镜像总数。                                                       |
| Top 10 pulled images（拉取最多的前 10 个镜像） | 用户从 Docker Hub 拉取次数最多的前 10 个镜像列表，以及每个镜像被拉取的次数。 |

### Extensions（扩展）

通过此图表监控扩展安装活动。它提供对团队正在使用的 Docker Desktop 扩展的可见性，让你能够跟踪采用情况并识别提升生产力的热门工具。

该图表包含以下数据：

| 数据                                           | 描述                                                                                                                                      |
| :--------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| Percentage of org with extensions installed（已安装扩展的组织占比）    | 组织中至少安装了一个 Docker Desktop 扩展的用户百分比。                                               |
| Top 5 extensions installed in the organization（组织中安装最多的前 5 个扩展） | 组织中用户安装最多的前 5 个 Docker Desktop 扩展列表，以及安装每个扩展的用户数。 |

## Export Docker Desktop user data（导出 Docker Desktop 用户数据）

你可以将 Docker Desktop 用户数据导出为 CSV 文件：

1. 打开 [Docker Home](https://app.docker.com) 并从左上角账户下拉菜单中选择你的组织。
1. 选择 **Docker Desktop**，然后选择 **Desktop insights**。
1. 为你的洞察数据选择时间范围：**1 Week（1 周）**、**1 Month（1 个月）** 或 **3 Months（3 个月）**。
1. 选择 **Export（导出）** 并从下拉菜单中选择 **Docker Desktop users（Docker Desktop 用户）**。

你的导出文件将自动下载。打开文件查看导出数据。

### Understanding export data（理解导出数据）

Docker Desktop 用户导出文件包含以下数据点：

- Name（姓名）：用户的姓名
- Username（用户名）：用户的 Docker ID
- Email（电子邮件）：与用户 Docker ID 关联的电子邮件地址
- Type（类型）：用户类型
- Role（角色）：用户 [role](/manuals/enterprise/security/roles-and-permissions.md)（角色）
- Teams（团队）：用户所属的组织内的团队
- Date Joined（加入日期）：用户加入你组织的日期
- Last Logged-In Date（最后登录日期）：用户最后使用其 Web 浏览器登录 Docker 的日期（包括 Docker Hub 和 Docker Home）
- Docker Desktop Version（Docker Desktop 版本）：用户安装的 Docker Desktop 版本
- Last Seen Date（最后出现日期）：用户最后使用 Docker Desktop 应用程序的日期
- Opted Out Analytics（是否退出分析）：用户是否退出了 Docker Desktop 中的 [Send usage statistics（发送使用统计）](/manuals/enterprise/security/hardened-desktop/settings-management/settings-reference.md#send-usage-statistics) 设置

## Troubleshoot Insights（排查 Insights 问题）

如果你在 Insights 的数据方面遇到问题，可考虑以下解决方案来解决常见问题：

- 将用户更新到最新版本的 Docker Desktop。

  对于使用 4.16 或更低版本 Docker Desktop 的用户，不显示数据。此外，较旧版本可能无法提供所有数据。确保所有用户都已安装最新版本的 Docker Desktop。

- 为所有用户开启 Docker Desktop 中的 **Send usage statistics（发送使用统计）**。

  如果用户选择退出发送 Docker Desktop 使用统计，则他们的使用数据将不会成为 Insights 的一部分。要为你所有用户大规模管理该设置，你可以使用 [Settings Management](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 并开启 `analyticsEnabled` 设置。

- 确保用户使用 Docker Desktop，而不是使用独立版本的 Docker Engine。

  只有 Docker Desktop 才能为 Insights 提供数据。如果用户安装在 Docker Desktop 之外安装 Docker Engine，Docker Engine 将不会为该用户提供数据。

- 确保用户登录到与你的组织关联的账户。

  未登录到与你的组织关联的账户的用户不会体现在数据中。为确保用户使用与你的组织关联的账户登录，你可以[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。

