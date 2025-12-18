---
title: 使用 Intune 部署
description: 使用 Intune（微软的基于云的设备管理工具）部署 Docker Desktop
keywords: microsoft, windows, docker desktop, deploy, mdm, enterprise, administrator, mac, pkg, dmg
tags: [admin]
weight: 40
aliases:
 - /desktop/install/msi/use-intune/
 - /desktop/setup/install/msi/use-intune/
 - /desktop/setup/install/enterprise-deployment/use-intune/
---

{{< summary-bar feature_name="Intune" >}}

了解如何使用 Microsoft Intune 在 Windows 和 macOS 设备上部署 Docker Desktop。内容涵盖应用创建、安装程序配置，以及分配给用户或设备的步骤。

{{< tabs >}}
{{< tab name="Windows" >}}

1. 登录到你的 Intune 管理中心。
2. 添加新应用。选择 **Apps**，然后选择 **Windows**，再选择 **Add**。
3. 对于应用类型，选择 **Windows app (Win32)**。
4. 选择 `intunewin` 包。
5. 填写必要信息，例如描述、发布者或应用版本，然后选择 **Next**。
6. 可选：在 **Program** 选项卡中，你可以根据需要更新 **Install command** 字段。该字段默认填充为 `msiexec /i "DockerDesktop.msi" /qn`。有关可进行的更改示例，请参阅 [常见安装场景](msi-install-and-configure.md)。

   > [!TIP]
   >
   > 建议你配置 Intune 部署，在成功安装后安排机器重启。
   >
   > 这是因为 Docker Desktop 安装程序会根据你的引擎选择安装 Windows 功能，并更新 `docker-users` 本地组的成员资格。
   >
   > 你可能还希望设置 Intune 根据返回代码确定行为，并监控返回代码 `3010`。返回代码 3010 表示安装成功但需要重启。

7. 完成其余选项卡的配置，然后查看并创建应用。

{{< /tab >}}
{{< tab name="Mac" >}}

首先，上传包：

1. 登录到你的 Intune 管理中心。
2. 添加新应用。选择 **Apps**，然后选择 **macOS**，再选择 **Add**。
3. 选择 **Line-of-business app**，然后选择 **Select**。
4. 上传 `Docker.pkg` 文件并填写必要信息。

接下来，分配应用：

1. 应用添加后，在 Intune 中导航到 **Assignments**。
2. 选择 **Add group**，然后选择要分配应用的用户或设备组。
3. 选择 **Save**。

{{< /tab >}}
{{< /tabs >}}

## 附加资源

- [查看常见问题解答](faq.md)。
- 了解如何为你的用户 [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。