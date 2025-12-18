---
title: 使用 JSON 文件配置设置管理
linkTitle: 使用 JSON 文件
description: 使用 admin-settings.json 文件配置和强制执行 Docker Desktop 设置
keywords: 管理员控制, 设置管理, 配置, 企业, docker desktop, json 文件
weight: 10
aliases:
 - /desktop/hardened-desktop/settings-management/configure/
 - /security/for-admins/hardened-desktop/settings-management/configure/
 - /security/for-admins/hardened-desktop/settings-management/configure-json-file/
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

设置管理允许您使用 `admin-settings.json` 文件配置并强制执行组织中所有 Docker Desktop 的设置。这可以标准化 Docker Desktop 环境，确保所有用户使用一致的配置。

## 前置条件

开始之前，请确保您已满足以下条件：

- [强制执行登录](/manuals/enterprise/security/enforce-sign-in/_index.md) 以加入您的组织
- 拥有 Docker Business 订阅

只有在身份验证和 Docker Business 许可证检查均成功时，Docker Desktop 才会应用 `admin-settings.json` 文件中的设置。

> [!IMPORTANT]
>
> 用户必须登录并属于 Docker Business 组织。如果任一条件不满足，设置文件将被忽略。

## 步骤一：创建设置文件

您可以通过两种方式创建 `admin-settings.json` 文件：

- 使用 `--admin-settings` 安装程序标志自动生成文件：
    - [macOS](/manuals/desktop/setup/install/mac-install.md#install-from-the-command-line) 安装指南
    - [Windows](/manuals/desktop/setup/install/windows-install.md#install-from-the-command-line) 安装指南
- 手动创建文件并放置在以下位置：
    - Mac: `/Library/Application\ Support/com.docker.docker/admin-settings.json`
    - Windows: `C:\ProgramData\DockerDesktop\admin-settings.json`
    - Linux: `/usr/share/docker-desktop/admin-settings.json`

> [!IMPORTANT]
>
> 将文件放置在受保护的目录中，以防止未经授权的更改。使用移动设备管理（MDM）工具（如 Jamf）在组织范围内分发文件。

## 步骤二：配置设置

> [!TIP]
>
> 有关所有可用设置、支持的平台以及适用的配置方法的完整列表，请参阅 [设置参考](settings-reference.md)。

`admin-settings.json` 文件使用结构化键来定义可配置的设置以及值是否被强制执行。

每个设置都支持一个 `locked` 字段来控制用户权限：

- 当 `locked` 设置为 `true` 时，用户无法在 Docker Desktop、CLI 或配置文件中更改该值。
- 当 `locked` 设置为 `false` 时，该值仅作为默认建议，用户仍可以更新。

如果用户已在 `settings-store.json`、`settings.json` 或 `daemon.json` 中自定义了某个值，则该值在现有安装上会被忽略（当 `locked` 设置为 `false` 时）。

### 分组设置

Docker Desktop 将某些设置组合在一起，通过单个切换来控制整个部分。这些设置包括：

- 增强容器隔离（ECI）：使用主切换（`enhancedContainerIsolation`）启用/禁用整个功能，子设置用于特定配置
- Kubernetes：使用主切换（`kubernetes.enabled`）和子设置配置集群
- Docker Scout：在 `scout` 对象下分组设置

配置分组设置时：

1. 设置主切换以启用功能
1. 配置该组内的子设置
1. 当锁定主切换时，用户无法修改该组中的任何设置

`enhancedContainerIsolation` 的示例：

```json
"enhancedContainerIsolation": {
  "locked": true,  // 这将锁定整个 ECI 部分
  "value": true,   // 这将启用 ECI
  "dockerSocketMount": {  // 这些是子设置
    "imageList": {
      "images": ["docker.io/testcontainers/ryuk:*"]
    }
  }
}
```

### 示例 `admin-settings.json` 文件

以下是一个配置了常见企业设置的 `admin-settings.json` 文件示例。您可以使用此示例作为模板，结合 [`admin-settings.json` 配置](#admin-settingsjson-configurations)：

```json {collapse=true}
{
  "configurationFileVersion": 2,
  "exposeDockerAPIOnTCP2375": {
    "locked": true,
    "value": false
  },
  "proxy": {
    "locked": true,
    "mode": "system",
    "http": "",
    "https": "",
    "exclude": [],
    "windowsDockerdPort": 65000,
    "enableKerberosNtlm": false,
    "pac": "",
    "embeddedPac": ""
  },
  "containersProxy": {
    "locked": true,
    "mode": "manual",
    "http": "",
    "https": "",
    "exclude": [],
    "pac":"",
    "embeddedPac": "",
    "transparentPorts": ""
  },
  "enhancedContainerIsolation": {
    "locked": true,
    "value": true,
    "dockerSocketMount": {
      "imageList": {
        "images": [
          "docker.io/localstack/localstack:*",
          "docker.io/testcontainers/ryuk:*"
        ]
      },
      "commandList": {
        "type": "deny",
        "commands": ["push"]
      }
    }
  },
  "linuxVM": {
    "wslEngineEnabled": {
      "locked": false,
      "value": false
    },
    "dockerDaemonOptions": {
      "locked": false,
      "value":"{\"debug\": false}"
    },
    "vpnkitCIDR": {
      "locked": false,
      "value":"192.168.65.0/24"
    }
  },
  "kubernetes": {
     "locked": false,
     "enabled": false,
     "showSystemContainers": false,
     "imagesRepository": ""
  },
  "windowsContainers": {
    "dockerDaemonOptions": {
      "locked": false,
      "value":"{\"debug\": false}"
    }
  },
  "disableUpdate": {
    "locked": false,
    "value": false
  },
  "analyticsEnabled": {
    "locked": false,
    "value": true
  },
  "extensionsEnabled": {
    "locked": true,
    "value": false
  },
  "scout": {
    "locked": false,
    "sbomIndexing": true,
    "useBackgroundIndexing": true
  },
  "allowBetaFeatures": {
    "locked": false,
    "value": false
  },
  "blockDockerLoad": {
    "locked": false,
    "value": true
  },
  "filesharingAllowedDirectories": [
    {
      "path": "$HOME",
      "sharedByDefault": true
    },
    {
      "path":"$TMP",
      "sharedByDefault": false
    }
  ],
  "useVirtualizationFrameworkVirtioFS": {
    "locked": true,
    "value": true
  },
  "useVirtualizationFrameworkRosetta": {
    "locked": true,
    "value": true
  },
  "useGrpcfuse": {
    "locked": true,
    "value": true
  },
  "displayedOnboarding": {
    "locked": true,
    "value": true
  },
  "desktopTerminalEnabled": {
    "locked": false,
    "value": false
  },
  "enableInference": {
    "locked": false,
    "value": true
  },
  "enableInferenceTCP": {
    "locked": false,
    "value": true
  },
  "enableInferenceTCPPort": {
    "locked": true,
    "value": 12434
  },
  "enableInferenceCORS": {
    "locked": true,
    "value": ""
  },
  "enableInferenceGPUVariant": {
    "locked": true,
    "value": true
  },
  "portBindingBehavior": {
    "locked": true,
    "value": "default-port-binding"
  }
}
```

## 步骤三：应用设置

设置在 Docker Desktop 重启并登录后生效。

对于新安装：

1. 启动 Docker Desktop。
1. 使用您的 Docker 账户登录。

对于现有安装：

1. 完全退出 Docker Desktop。
1. 重新启动 Docker Desktop。

> [!IMPORTANT]
>
> 您必须完全退出并重新打开 Docker Desktop。从菜单重启是不够的。

## `admin-settings.json` 配置

下表描述了 `admin-settings.json` 文件中所有可用的设置。

> [!NOTE]
>
> 某些设置是特定于平台的，或需要最低 Docker Desktop 版本。请查看版本列以了解要求。

### 通用设置

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`configurationFileVersion`|   |指定配置文件格式的版本。|   |
|`analyticsEnabled`|  |如果 `value` 设置为 false，Docker Desktop 不会向 Docker 发送使用统计信息。 |  |
|`disableUpdate`|  |如果 `value` 设置为 true，则禁用 Docker Desktop 更新的检查和通知。|  |
|`extensionsEnabled`|  |如果 `value` 设置为 false，则禁用 Docker 扩展。 |  |
| `blockDockerLoad` | | 如果 `value` 设置为 `true`，用户将无法运行 [`docker load`](