---
title: 获取 Docker 产品支持
linkTitle: 支持
description: 了解 Docker 产品的支持选项，包括付费订阅和社区资源
keywords: support, help, docker desktop, subscriptions, community, troubleshooting
weight: 5
params:
  sidebar:
    group: Platform
---

Docker 根据您的订阅级别和需求提供多种支持渠道。

## 付费订阅支持

所有 Docker Pro、Team 和 Business 订阅用户均可获得 Docker 产品的电子邮件支持。

### 支持响应时间

- Docker Pro：3 个工作日内响应
- Docker Team：2 个工作日内响应，24×5 可用性
- Docker Business：1 个工作日内响应，24×5 可用性

> [!NOTE]
>
> Docker Business 订阅用户可额外购买高级支持服务，享受更快的响应时间和 24×7 可用性。

有关详细的支持功能和响应时间，请参阅 [Docker 定价](https://www.docker.com/pricing/)。

### 支持严重性级别

| 级别 | 描述 |
| :--- | :--- |
| 严重 | 影响众多客户或单个组织内所有用户的广泛或全公司范围的服务中断。业务运营已停止，且无可用解决方案。 |
| 高 | 团队或部门级别的影响，阻止重要用户访问核心功能。存在严重的业务影响，且无可用解决方案。 |
| 中等 | 个人用户或小组影响，导致部分功能丧失。业务运营仍在继续，通常有可用解决方案，但生产力降低。 |

### 请求支持

> [!TIP]
>
> 在寻求支持之前，请查看您产品的故障排除文档。

如果您拥有付费 Docker 订阅，请[联系支持团队](https://hub.docker.com/support/contact/)。

## 社区支持

所有 Docker 用户均可通过社区资源寻求支持，Docker 或社区将尽最大努力回应：

- [Docker 社区论坛](https://forums.docker.com/)
- [Docker 社区 Slack](http://dockr.ly/comm-slack)

## Docker Desktop 支持

Docker Desktop 支持仅对付费订阅用户提供。

### 支持范围

{{< tabs >}}
{{< tab name="支持范围">}}

Docker Desktop 支持包括：

- 账户管理和计费
- 配置和安装问题
- 桌面更新
- 登录问题
- 推送或拉取问题，包括速率限制
- 应用程序崩溃或意外行为
- 自动构建
- 基本产品“如何使用”问题

**Windows 特定：**

- 在 BIOS 中启用虚拟化
- 启用 Windows 功能
- 在[某些 VM 或 VDI 环境](/manuals/desktop/setup/vm-vdi.md)中运行（仅限 Docker Business）

{{< /tab >}}
{{< tab name="不支持范围">}}

Docker Desktop 支持不包括：

- 不受支持的操作系统，包括测试版/预览版
- 使用仿真运行不同架构的容器
- Docker Engine、Docker CLI 或其他捆绑的 Linux 组件
- Kubernetes
- 标记为实验性的功能
- 系统/服务器管理活动
- 将桌面作为生产运行时
- 规模部署/多机安装
- 常规产品维护（数据备份、磁盘空间、日志轮换）
- 非 Docker 提供的第三方应用程序
- 修改或更改的 Docker 软件
- 硬件故障、滥用或不当使用
- 早于最新版本的版本（Docker Business 除外）
- 培训、定制和集成
- 在单台机器上运行多个实例

> [!NOTE]
>
> 仅在 [VM 或 VDI 环境中运行 Docker Desktop](/manuals/desktop/setup/vm-vdi.md) 的支持仅对 Docker Business 客户提供。

{{< /tab >}}
{{< /tabs >}}

### 支持的版本

- Docker Business：最新版本的六个月内的版本（仅对最新版本应用修复）
- Docker Pro 和 Team：仅最新版本

### 机器数量

- Docker Pro：一台机器
- Docker Team：等于订阅席位的机器数量
- Docker Business：无限机器

### 支持的操作系统

- [Mac 系统要求](/manuals/desktop/setup/install/mac-install.md#system-requirements)
- [Windows 系统要求](/manuals/desktop/setup/install/windows-install.md#system-requirements)
- [Linux 系统要求](/manuals/desktop/setup/install/linux/_index.md#system-requirements)

### 社区资源

- [Docker Desktop for Windows](https://github.com/docker/for-win)
- [Docker Desktop for Mac](https://github.com/docker/for-mac)
- [Docker Desktop for Linux](https://github.com/docker/desktop-linux)

### 诊断数据和隐私

上传诊断信息时，诊断包可能包含用户名和 IP 地址等个人数据。诊断包仅可由直接参与诊断问题的 Docker, Inc. 员工访问。

默认情况下，Docker, Inc. 会在 30 天后删除上传的诊断包。您可以通过指定诊断 ID 或您的 GitHub ID 请求删除诊断包。Docker, Inc. 仅使用数据调查特定用户问题，但可能会得出高级（非个人）指标。

有关更多信息，请参阅 [Docker 数据处理协议](https://www.docker.com/legal/data-processing-agreement)。