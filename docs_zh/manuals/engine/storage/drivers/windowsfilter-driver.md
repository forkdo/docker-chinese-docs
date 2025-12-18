---
description: 了解 windowsfilter 存储驱动
keywords: 容器, 存储, 驱动, Windows, windowsfilter
title: windowsfilter 存储驱动
---

windowsfilter 存储驱动是 Windows 上 Docker Engine 的默认存储驱动。windowsfilter 驱动使用 Windows 原生文件系统层在磁盘上存储 Docker 层和卷数据。windowsfilter 存储驱动仅在使用 NTFS 格式化的文件系统上工作。

## 配置 windowsfilter 存储驱动

对于大多数用例，无需配置 windowsfilter 存储驱动。

Docker Engine 在 Windows 上的默认存储限制为 127GB。要使用不同的存储大小，请设置 windowsfilter 存储驱动的 `size` 选项。请参阅 [windowsfilter 选项](/reference/cli/dockerd.md#windowsfilter-options)。

数据默认存储在 Docker 主机的 `C:\ProgramData\docker` 目录下的 `image` 和 `windowsfilter` 子目录中。您可以通过在 [守护进程配置文件](/reference/cli/dockerd.md#on-windows) 中配置 `data-root` 选项来更改存储位置：

```json
{
  "data-root": "d:\\docker"
}
```

配置更改后，您必须重启守护进程才能生效。

## 附加信息

有关 Windows 上容器存储工作原理的更多信息，请参阅 Microsoft 的 [Windows 容器文档](https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/container-storage)。