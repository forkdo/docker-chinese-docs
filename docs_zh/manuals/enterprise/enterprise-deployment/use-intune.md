---
title: 使用 Intune 部署
description: 使用 Microsoft 基于云的设备管理工具 Intune 来部署 Docker Desktop
keywords: microsoft, windows, docker desktop, deploy, mdm, enterprise, administrator, mac, pkg, dmg
tags: [admin]
weight: 40
aliases:
 - /desktop/install/msi/use-intune/
 - /desktop/setup/install/msi/use-intune/
 - /desktop/setup/install/enterprise-deployment/use-intune/
---

{{< summary-bar feature_name="Intune" >}}

了解如何使用 Microsoft Intune 在 Windows 和 macOS 设备上部署 Docker Desktop。本指南涵盖应用创建、安装程序配置以及分配给用户或设备。

{{< tabs >}}
{{< tab name="Windows" >}}

1. 登录到您的 Intune 管理中心。
2. 添加新应用。选择 **Apps**（应用），然后 **Windows**，再选择 **Add**（添加）。
3. 对于应用类型，选择 **Windows app (Win32)**。
4. 选择 `intunewin` 包。
5. 填写所需详细信息，例如描述、发布者或应用版本，然后选择 **Next**（下一步）。
6. 可选：在 **Program**（程序）选项卡上，您可以更新 **Install command**（安装命令）字段以满足您的需求。该字段已预填充 `msiexec /i "DockerDesktop.msi" /qn`。有关您可以进行的更改示例，请参阅[常见安装场景](msi-install-and-configure.md)。

   > [!TIP]
   >
   > 建议您配置 Intune 部署，以便在成功安装后安排计算机重启。
   >
   > 这是因为 Docker Desktop 安装程序会根据您的引擎选择安装 Windows 功能，并且还会更新 `docker-users` 本地组的成员资格。
   >
   > 您可能还需要设置 Intune 以根据返回代码确定行为，并监视返回代码 `3010`。返回代码 3010 表示安装成功但需要重启。

7. 完成剩余的选项卡，然后检查并创建应用。

{{< /tab >}}
{{< tab name="Mac" >}}

首先，上传包：

1. 登录到您的 Intune 管理中心。
2. 添加新应用。选择 **Apps**（应用），然后 **macOS**，再选择 **Add**（添加）。
3. 选择 **Line-of-business app**（业务线应用），然后选择 **Select**（选择）。
4. 上传 `Docker.pkg` 文件并填写所需详细信息。

接下来，分配应用：

1. 应用添加后，在 Intune 中导航到 **Assignments**（分配）。
2. 选择 **Add group**（添加组）并选择您要将应用分配到的用户或设备组。
3. 选择 **Save**（保存）。

{{< /tab >}}
{{< /tabs >}}

## 其他资源

- [查看常见问题解答](faq.md)。
- 了解如何为您的用户[强制执行登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。