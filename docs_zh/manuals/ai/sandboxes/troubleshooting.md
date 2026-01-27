---
title: 故障排除
description: 解决在本地对代理进行沙盒化时的常见问题。
weight: 50
---

{{< summary-bar feature_name="Docker Sandboxes" >}}

本指南帮助您解决在本地对 Claude Code 进行沙盒化时的常见问题。

<!-- vale off -->

## 'sandbox' 不是 docker 命令

<!-- vale on -->

当您运行 `docker sandbox` 时，您会看到一条错误提示说该命令不存在。这意味着 CLI 插件未安装或未放置在正确的位置。

解决方法：

1. 验证插件是否存在：

```console
$ ls -la ~/.docker/cli-plugins/docker-sandbox
```

该文件应存在并且可执行。

2. 如果使用 Docker Desktop，请重启它以检测该插件。

## 需要由管理员启用"实验性功能"

当您尝试使用沙盒时，您会看到一条关于测试版功能被禁用的错误。这发生在您的 Docker Desktop 安装由管理员管理且设置被锁定的情况下。

如果您的组织使用了 [设置管理](/enterprise/security/hardened-desktop/settings-management/)，请要求您的管理员[允许测试版功能](/enterprise/security/hardened-desktop/settings-management/configure-json-file/#beta-features)：

```json
{
  "configurationFileVersion": 2,
  "allowBetaFeatures": {
    "locked": false,
    "value": true
  }
}
```

## 身份验证失败

Claude 无法进行身份验证，或者您看到 API 密钥错误。API 密钥可能无效、已过期或未正确配置。

## 工作区包含 API 密钥配置

启动沙盒时，您会看到一条关于凭据冲突的警告。这发生在您的工作区有一个包含 `primaryApiKey` 字段的 `.claude.json` 文件时。

选择以下方法之一：

- 从您的 `.claude.json` 中移除 `primaryApiKey` 字段：

```json
{
  "apiKeyHelper": "/path/to/script",
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.anthropic.com"
  }
}
```

- 或者继续并保留警告——工作区凭据将被忽略，优先使用沙盒凭据。

## 访问工作区文件时权限被拒绝

Claude 或命令在访问工作区中的文件时失败，并显示"Permission denied"（权限被拒绝）错误。这通常意味着 Docker 无法访问工作区路径，或者文件权限过于严格。

如果使用 Docker Desktop：

1. 在 Docker Desktop → **设置** → **资源** → **文件共享** 中检查文件共享设置。
2. 确保您的工作区路径（或父目录）列在虚拟文件共享下。
3. 如果缺失，请点击"+"添加包含您工作区的目录。
4. 重启 Docker Desktop。

对于所有平台，验证文件权限：

```console
$ ls -la <workspace>
```

确保文件可读。如果需要：

```console
$ chmod -R u+r <workspace>
```

还要验证工作区路径是否存在：

```console
$ cd <workspace>
$ pwd
```

## 在 Windows 上启动多个沙盒时发生崩溃

在 Windows 上，同时启动过多沙盒可能会导致崩溃。如果发生这种情况，请通过关闭 OpenVMM 进程来恢复：

1. 打开任务管理器（Ctrl+Shift+Esc）。
2. 查找所有 `docker.openvmm.exe` 进程。
3. 结束每个进程。
4. 如果需要，重启 Docker Desktop。

为避免此问题，请一次启动一个沙盒，而不是同时创建多个沙盒。