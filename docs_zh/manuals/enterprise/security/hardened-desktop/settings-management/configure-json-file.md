---
title: 使用 JSON 文件配置设置管理
linkTitle: 使用 JSON 文件
description: 使用 admin-settings.json 文件配置和强制执行 Docker Desktop 设置
keywords: 管理控制, 设置管理, 配置, 企业, docker desktop, json 文件
weight: 10
aliases:
- /desktop/hardened-desktop/settings-management/configure/
- /security/for-admins/hardened-desktop/settings-management/configure/
- /security/for-admins/hardened-desktop/settings-management/configure-json-file/
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

设置管理 (Settings Management) 允许您使用 `admin-settings.json` 文件在整个组织内配置和强制执行 Docker Desktop 设置。这可以标准化 Docker Desktop 环境，并确保所有用户都有一致的配置。

## 先决条件

在开始之前，请确保您已：

- 为您的组织[强制执行登录](/manuals/enterprise/security/enforce-sign-in/_index.md)
- 拥有 Docker Business 订阅

只有当身份验证和 Docker Business 许可证检查都成功时，Docker Desktop 才会应用来自 `admin-settings.json` 文件的设置。

> [!IMPORTANT]
>
> 用户必须已登录并属于 Docker Business 组织。如果任一条件未满足，设置文件将被忽略。

## 第一步：创建设置文件

您可以通过两种方式创建 `admin-settings.json` 文件：

- 使用 `--admin-settings` 安装程序标志自动生成文件：
    - [macOS](/manuals/desktop/setup/install/mac-install.md#install-from-the-command-line) 安装指南
    - [Windows](/manuals/desktop/setup/install/windows-install.md#install-from-the-command-line) 安装指南
- 手动创建并将其放置在以下位置：
    - Mac: `/Library/Application\ Support/com.docker.docker/admin-settings.json`
    - Windows: `C:\ProgramData\DockerDesktop\admin-settings.json`
    - Linux: `/usr/share/docker-desktop/admin-settings.json`

> [!IMPORTANT]
>
> 将文件放在受保护的目录中以防止未经授权的更改。使用 Jamf 等移动设备管理 (MDM) 工具在您的整个组织中大规模分发该文件。

## 第二步：配置设置

> [!TIP]
>
> 有关可用设置的完整列表、其支持的平台以及它们与哪些配置方法配合使用，请参阅[设置参考](settings-reference.md)。

`admin-settings.json` 文件使用结构化键来定义可配置设置以及是否强制执行值。

每个设置都支持一个 `locked` 字段，用于控制用户权限：

- 当 `locked` 设置为 `true` 时，用户无法在 Docker Desktop、CLI 或配置文件中更改该值。
- 当 `locked` 设置为 `false` 时，该值充当默认建议，用户仍然可以更新它。

如果用户已经在 `settings-store.json`、`settings.json` 或 `daemon.json` 中自定义了该值，则在现有安装上会忽略 `locked` 设置为 `false` 的设置。

### 分组设置

Docker Desktop 将一些设置组合在一起，使用一个切换开关来控制整个部分。这些包括：

- 增强容器隔离 (ECI)：使用主开关 (`enhancedContainerIsolation`) 启用/禁用整个功能，并带有用于特定配置的子设置
- Kubernetes：使用主开关 (`kubernetes.enabled`) 和用于集群配置的子设置
- Docker Scout：将设置分组在 `scout` 对象下

配置分组设置时：

1. 设置主开关以启用该功能
2. 在该组内配置子设置
3. 当您锁定主开关时，用户无法修改该组中的任何设置

`enhancedContainerIsolation` 示例：

```json
"enhancedContainerIsolation": {
  "locked": true,  // 这会锁定整个 ECI 部分
  "value": true,   // 这会启用 ECI
  "dockerSocketMount": {  // 这些是子设置
    "imageList": {
      "images": ["docker.io/testcontainers/ryuk:*"]
    }
  }
}
```

### 示例 `admin-settings.json` 文件

以下示例是一个配置了常见企业设置的 `admin-settings.json` 文件。您可以使用此示例作为模板，并结合 [`admin-settings.json` 配置](#admin-settingsjson-configurations)：

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

## 第三步：应用设置

设置在 Docker Desktop 重启且用户登录后生效。

对于新安装：

1. 启动 Docker Desktop。
2. 使用您的 Docker 帐户登录。

对于现有安装：

1. 完全退出 Docker Desktop。
2. 重新启动 Docker Desktop。

> [!IMPORTANT]
>
> 您必须完全退出并重新打开 Docker Desktop。从菜单重启是不够的。

## `admin-settings.json` 配置

以下表格描述了 `admin-settings.json` 文件中的所有可用设置。

> [!NOTE]
>
> 某些设置是特定于平台的或需要最低 Docker Desktop 版本。请检查“版本”列以了解要求。

### 常规设置

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`configurationFileVersion`|   |指定配置文件格式的版本。|   |
|`analyticsEnabled`|  |如果 `value` 设置为 false，Docker Desktop 不会向 Docker 发送使用统计信息。 |  |
|`disableUpdate`|  |如果 `value` 设置为 true，则禁用检查 Docker Desktop 更新和相关通知。|  |
|`extensionsEnabled`|  |如果 `value` 设置为 false，则禁用 Docker 扩展。 |  |
| `blockDockerLoad` | | 如果 `value` 设置为 `true`，用户将无法再运行 [`docker load`](/reference/cli/docker/image/load/)，如果尝试运行，将会收到错误。|  |
| `displayedOnboarding` |  | 如果 `value` 设置为 `true`，新用户将不会看到入门调查。将 `value` 设置为 `false` 无效。 |  Docker Desktop 版本 4.30 及更高版本 |
| `desktopTerminalEnabled` |  | 如果 `value` 设置为 `false`，开发人员将无法使用 Docker 终端与主机交互，也无法直接从 Docker Desktop 执行命令。 |  |
|`exposeDockerAPIOnTCP2375`| 仅限 Windows| 在指定端口上公开 Docker API。如果 `value` 设置为 true，则 Docker API 在端口 2375 上公开。注意：这是未经身份验证的，只有在受适当防火墙规则保护的情况下才应启用。|  |
| `silentModulesUpdate` | | 如果 `value` 设置为 `true`，Docker Desktop 会自动更新不需要重启的组件。例如，Docker CLI 或 Docker Scout 组件。 | Docker Desktop 版本 4.46 及更高版本。 |

### 文件共享和仿真

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
| `filesharingAllowedDirectories` |  | 指定您的开发人员可以添加文件共享的路径。也接受 `$HOME`、`$TMP` 或 `$TEMP` 作为 `path` 变量。添加路径后，其子目录也被允许。如果 `sharedByDefault` 设置为 `true`，则该路径将在恢复出厂设置或 Docker Desktop 首次启动时添加。 |  |
| `useVirtualizationFrameworkVirtioFS`|  仅限 macOS | 如果 `value` 设置为 `true`，VirtioFS 将被设置为文件共享机制。注意：如果 `useVirtualizationFrameworkVirtioFS` 和 `useGrpcfuse` 的 `value` 都设置为 `true`，则 VirtioFS 优先。同样，如果两者的 `value` 都设置为 `false`，则 osxfs 被设置为文件共享机制。 |  |
| `useGrpcfuse` | 仅限 macOS | 如果 `value` 设置为 `true`，gRPC Fuse 将被设置为文件共享机制。 |  |
| `useVirtualizationFrameworkRosetta`|  仅限 macOS | 如果 `value` 设置为 `true`，Docker Desktop 会开启 Rosetta 以加速 Apple Silicon 上的 x86_64/amd64 二进制仿真。注意：这也会自动启用 `Use Virtualization framework`。 | Docker Desktop 版本 4.29 及更高版本。 |

### Docker Scout

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`scout`| | 将 `useBackgroundIndexing` 设置为 `false` 会禁用对加载到镜像存储中的镜像的自动索引。将 `sbomIndexing` 设置为 `false` 会阻止用户通过在 Docker Desktop 中检查镜像或使用 `docker scout` CLI 命令来索引镜像。 |  |

### 代理设置

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`proxy`|   |如果 `mode` 设置为 `system` 而不是 `manual`，Docker Desktop 会从系统获取代理值，并忽略为 `http`、`https` 和 `exclude` 设置的任何值。将 `mode` 更改为 `manual` 以手动配置代理服务器。如果代理端口是自定义的，请在 `http` 或 `https` 属性中指定，例如 `"https": "http://myotherproxy.com:4321"`。`exclude` 属性指定要绕过代理的主机和域的逗号分隔列表。 |  |
| `windowsDockerdPort`| 仅限 Windows | 在本地此端口上公开 Docker Desktop 的内部代理，以供 Windows Docker 守护进程连接。如果设置为 0，则选择一个随机的空闲端口。如果值大于 0，则使用该确切值作为端口。默认值为 -1，表示禁用该选项。 |  |
|`enableKerberosNtlm`|  |当设置为 `true` 时，启用 Kerberos 和 NTLM 身份验证。默认为 `false`。有关更多信息，请参阅设置文档。 | Docker Desktop 版本 4.32 及更高版本。 |
| `pac` | | 指定 PAC 文件 URL。例如，`"pac": "http://proxy/proxy.pac"`。 | |
| `embeddedPac`  | | 指定嵌入式 PAC（代理自动配置）脚本。例如，`"embeddedPac": "function FindProxyForURL(url, host) { return \"DIRECT\"; }"`。此设置优先于 HTTP、HTTPS、代理绕过和 PAC 服务器 URL。 |  Docker Desktop 版本 4.46 及更高版本。 |

### 容器代理

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`containersProxy` | | 创建隔离网络环境的容器。有关更多信息，请参阅[隔离网络环境容器](../air-gapped-containers.md)。| Docker Desktop 版本 4.29 及更高版本。 |
| `pac` | | 指定 PAC 文件 URL。例如，`"pac": "http://containerproxy/proxy.pac"`。 | |
| `embeddedPac`  | | 指定嵌入式 PAC（代理自动配置）脚本。例如，`"embeddedPac": "function FindProxyForURL(url, host) { return \"PROXY 192.168.92.1:2003\"; }"`。此设置优先于 HTTP、HTTPS、代理绕过和 PAC 服务器 URL。 |  Docker Desktop 版本 4.46 及更高版本。 |

### Linux VM 设置

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
| `linuxVM` |   |与 Linux VM 选项相关的参数和设置 - 为方便起见在此处分组。 |  |
| &nbsp; &nbsp; &nbsp; &nbsp;`wslEngineEnabled`  | 仅限 Windows | 如果 `value` 设置为 true，Docker Desktop 使用基于 WSL 2 的引擎。这会覆盖使用 `--backend=<backend name>` 标志在安装时设置的任何内容。 |  |
| &nbsp; &nbsp; &nbsp; &nbsp;`dockerDaemonOptions` |  |如果 `value` 设置为 true，它会覆盖 Docker 引擎配置文件中的选项。请参阅 [Docker 引擎参考](/reference/cli/dockerd/#daemon-configuration-file)。请注意，为了提高安全性，当启用增强容器隔离时，某些配置属性可能会被覆盖。 |  |
| &nbsp; &nbsp; &nbsp; &nbsp;`vpnkitCIDR` |  |覆盖用于 vpnkit DHCP/DNS 的 `*.docker.internal` 网络范围 |  |

### Windows 容器

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
| `windowsContainers` |  | 与 `windowsContainers` 选项相关的参数和设置 - 为方便起见在此处分组。  |  |
| &nbsp; &nbsp; &nbsp; &nbsp;`dockerDaemonOptions` |  | 覆盖 Linux 守护进程配置文件中的选项。请参阅 [Docker 引擎参考](/reference/cli/dockerd/#daemon-configuration-file)。|  |

> [!NOTE]
>
> 此设置无法通过 Docker 管理控制台进行配置。

### Kubernetes 设置

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`kubernetes`|  | 如果 `enabled` 设置为 true，则在 Docker Desktop 启动时启动 Kubernetes 单节点集群。如果 `showSystemContainers` 设置为 true，Kubernetes 容器将显示在 Docker Desktop 仪表板中，并且在运行 `docker ps` 时也会显示。[imagesRepository](/manuals/desktop/use-desktop/kubernetes.md#configuring-a-custom-image-registry-for-kubernetes-control-plane-images) 设置允许您指定 Docker Desktop 从中拉取 Kubernetes 控制平面镜像的仓库。 |  |

> [!NOTE]
>
> 当将 `imagesRepository` 与增强容器隔离 (ECI) 一起使用时，请将这些镜像添加到 [ECI Docker 套接字挂载镜像列表](#enhanced-container-isolation)：
>
> `[imagesRepository]/desktop-cloud-provider-kind:`
> `[imagesRepository]/desktop-containerd-registry-mirror:`
>
> 这些容器挂载了 Docker 套接字，因此您必须将它们添加到 ECI 镜像列表中。否则，ECI 会阻止挂载，Kubernetes 将无法启动。

### 网络设置

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
| `defaultNetworkingMode` | 仅限 Windows 和 Mac | 定义新 Docker 网络的默认 IP 协议：`dual-stack`（IPv4 + IPv6，默认）、`ipv4only` 或 `ipv6only`。 | Docker Desktop 版本 4.43 及更高版本。 |
| `dnsInhibition` | 仅限 Windows 和 Mac | 控制返回给容器的 DNS 记录过滤。选项：`auto`（推荐）、`ipv4`、`ipv6`、`none` | Docker Desktop 版本 4.43 及更高版本。 |
| `portBindingBehavior` | 仅限基于 Linux 的容器 | 定义端口绑定限制和默认行为，允许管理员控制用户如何从其容器暴露端口。选项：`default-port-binding`、`default-local-port-binding`、`local-only-port-binding` | Docker Desktop 版本 4.52 及更高版本。 |

有关更多信息，请参阅[网络](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

### AI 设置

| 参数                   | 操作系统            | 描述                                                                                                                                                                                                                         | 版本 |
|:----------------------------|---------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| `enableInference`           |               | 将 `enableInference` 设置为 `true` 会启用 [Docker Model Runner](/manuals/ai/model-runner/_index.md)。                                                                                                                                                                                              |         |
| `enableInferenceTCP`        |               | 启用主机端 TCP 支持。此设置需要先启用 Docker Model Runner 设置。                                                                                                                                                                                                |         |
| `enableInferenceTCPPort`    |               | 指定暴露的 TCP 端口。此设置需要先启用 Docker Model Runner 和启用主机端 TCP 支持设置。                                                                                                                                                                                                |         |
| `enableInferenceCORS`       |               | 指定允许的 CORS 源。空字符串表示拒绝所有，`*` 表示接受所有，或逗号分隔的值列表。此设置需要先启用 Docker Model Runner 和启用主机端 TCP 支持设置。                                                                                                                                                                                                |         |
| `enableInferenceGPUVariant` | 仅限 Windows  | 将 `enableInferenceGPUVariant` 设置为 `true` 会启用 GPU 支持的推理。此功能所需的额外组件不随 Docker Desktop 默认提供，因此它们将被下载到 `~/.docker/bin/inference`。  |         |

### Beta 功能

> [!IMPORTANT]
>
> 对于 Docker Desktop 版本 4.41 及更早版本，其中一些设置位于 **功能开发中** 页面的 **实验性功能** 选项卡下。

| 参数                                            | 操作系统 | 描述                                                                                                                                                                                                                                               | 版本                                 |
|:-----------------------------------------------------|----|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------|
| `allowBetaFeatures`                                  |    | 如果 `value` 设置为 `true`，则启用 Beta 功能。                                                                                                                                                                                                   |                                         |
| `enableDockerAI`                                     |    | 如果 `allowBetaFeatures` 为 true，将 `enableDockerAI` 设置为 `true` 会默认启用 [Docker AI (Ask Gordon)](/manuals/ai/gordon/_index.md)。您可以独立于 `allowBetaFeatures` 设置控制此设置。                            |                                         |
| `enableDockerMCPToolkit`                             |    | 如果 `allowBetaFeatures` 为 true，将 `enableDockerMCPToolkit` 设置为 `true` 会默认启用 [MCP Toolkit 功能](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md)。您可以独立于 `allowBetaFeatures` 设置控制此设置。 |                                         |
| `allowExperimentalFeatures`                          |    | 如果 `value` 设置为 `true`，则启用实验性功能。                                                                                                                                                                                           | Docker Desktop 版本 4.41 及更早版本 |

### 增强容器隔离

|参数|操作系统|描述|版本|
|:-------------------------------|---|:-------------------------------|---|
|`enhancedContainerIsolation`|  | 如果 `value` 设置为 true，Docker Desktop 通过 Linux 用户命名空间将所有容器作为非特权容器运行，防止它们修改 Docker Desktop VM 内部的敏感配置，并使用其他高级技术来隔离它们。有关更多信息，请参阅[增强容器隔离](../enhanced-container-isolation/_index.md)。|  |
| &nbsp; &nbsp; &nbsp; &nbsp;`dockerSocketMount` |  | 默认情况下，增强容器隔离会阻止将 Docker 引擎套接字绑定挂载到容器中（例如，`docker run -v /var/run/docker.sock:/var/run/docker.sock ...`）。这可以让您以受控方式放宽此限制。有关更多信息，请参阅 [ECI 配置](../enhanced-container-isolation/config.md)。 |  |
| &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; `imageList` |  | 指示哪些容器镜像允许绑定挂载 Docker 引擎套接字。 |  |
| &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; `commandList` |  | 限制容器可以通过绑定挂载的 Docker 引擎套接字发出的命令。 |  |