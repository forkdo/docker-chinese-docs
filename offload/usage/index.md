# Docker Offload 使用情况




[Docker Home](https://app.docker.com/) 中的 **Offload 活动 (Offload activity)** 页面提供了对 Docker Offload 用户活动和会话指标的可见性。

要监控您的使用情况：

1. 登录 [Docker Home](https://app.docker.com/)。
2. 如果您可以访问多个组织，请选择与您的 Docker Offload 订阅相关联的组织。
3. 选择 **Offload** > **Offload activity**。

### 概览指标

页面顶部的核心指标汇总了您的 Docker Offload 使用情况：

- **总时长 (Total duration)**：在 Offload 会话中花费的总时间
- **平均时长 (Average duration)**：每个 Offload 会话的平均时间
- **总会话数 (Total sessions)**：Offload 会话的总数
- **使用的唯一镜像数 (Unique images used)**：跨会话使用的不同容器镜像数量
- **唯一用户数 (Unique users)**：Docker Offload 会话中不同用户的数量

### 筛选和导出数据

您可以按以下方式筛选 Offload 活动数据：

- **时间段 (Period)**：选择预设时间段或自定义日期范围
- **用户 (Users)**：拥有分析权限的组织所有者和成员可以按特定用户筛选
- **附加筛选器 (Additional Filters)**：按活动会话和会话时长筛选

通过选择 **下载 CSV (Download CSV)** 按钮导出您的会话数据。导出的文件包含：

- 会话 ID (Session ID)
- 用户名 (Username)
- 镜像 (Image)
- 开始时间 (Started time)
- 结束时间 (Ended time)
- 时长（秒）(Duration (in seconds))
- 状态 (Status)
- 容器数量 (Container count)

CSV 导出包含您所选日期范围和用户筛选器的数据，让您下载到的正是您所查看的内容。

### 活动卡片

以下卡片提供了对您 Docker Offload 使用情况的洞察：

- **Offload 使用情况 (Offload usage)**：显示您随时间的用量趋势和云资源消耗模式。
- **热门镜像 (Popular images)**：显示在您的 Docker Offload 会话中最频繁使用的前 4 个容器镜像。选择该卡片可查看更多镜像。
- **Offload 活跃用户 (Top Offload users)**：按会话数和时长显示前 4 名用户。选择该卡片可查看更多用户。

### Offload 会话

活动卡片之后会显示 Offload 会话的详细列表。该列表：

- 以任何当前活动的会话开头
- 显示会话详细信息，包括开始时间、时长、使用的镜像和用户信息
- 可使用前面描述的日期和用户筛选器进行筛选
- 如果您拥有组织范围的分析权限，则显示 **Offload 会话 (Offload sessions)**；如果仅查看您自己的数据，则显示 **我的 Offload 会话 (My Offload sessions)**

选择任意会话可在侧面板中查看详细信息。

