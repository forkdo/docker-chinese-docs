---
title: 故障排除
description: 解决在本地沙箱化智能体时的常见问题
weight: 50
---

{{< summary-bar feature_name="Docker Sandboxes" >}}

本指南帮助您解决在本地沙箱化 Claude Code 时遇到的常见问题。

<!-- vale off -->

## 'sandbox' 不是 docker 命令

<!-- vale on -->

当您运行 `docker sandbox` 时，看到错误提示该命令不存在。

这表示 CLI 插件未安装或未放置在正确位置。解决方法：

1. 验证插件是否存在：

   ```console
   $ ls -la ~/.docker/cli-plugins/docker-sandbox
   ```

   文件应存在且可执行。

2. 如果使用 Docker Desktop，请重启以检测插件。

## "实验性功能"需要管理员启用

尝试使用沙箱时，看到关于 beta 功能被禁用的错误。

这通常发生在 Docker Desktop 安装由管理员管理且锁定设置的情况下。如果组织使用 [Settings Management](/enterprise/security/hardened-desktop/settings-management/)，
请要求管理员 [允许 beta 功能](/enterprise/security/hardened-desktop/settings-management/configure-json-file/#beta-features)：

```json
{
  "configurationFileVersion": 2,
  "allowBetaFeatures": {
    "locked": false,
    "value": true
  }
}
```

## 认证失败

Claude 无法认证，或看到 API 密钥错误。

API 密钥可能无效、过期或配置不正确。修复方法取决于您的凭据模式：

如果使用 `--credentials=sandbox`（默认）：

1. 删除存储的凭据：

   ```console
   $ docker volume rm docker-claude-sandbox-data
   ```

2. 启动新沙箱并完成认证流程：

   ```console
   $ docker sandbox run claude
   ```

## 工作区包含 API 密钥配置

启动沙箱时看到关于凭据冲突的警告。

这通常发生在工作区的 `.claude.json` 文件包含 `primaryApiKey` 字段时。选择以下方法之一：

- 从 `.claude.json` 中移除 `primaryApiKey` 字段：

  ```json
  {
    "apiKeyHelper": "/path/to/script",
    "env": {
      "ANTHROPIC_BASE_URL": "https://api.anthropic.com"
    }
  }
  ```

- 或继续忽略警告 - 工作区凭据将被忽略，优先使用沙箱凭据。

## 访问工作区文件时权限被拒绝

Claude 或命令访问工作区文件时失败，出现"权限被拒绝"错误。

这通常表示工作区路径对 Docker 不可访问，或文件权限过于严格。

如果使用 Docker Desktop：

1. 检查文件共享设置：Docker Desktop → **Settings** → **Resources** → **File Sharing**。

2. 确保工作区路径（或父目录）列在虚拟文件共享下。

3. 如果缺失，点击"+"添加包含工作区的目录。

4. 重启 Docker Desktop。

对于所有平台，验证文件权限：

```console
$ ls -la <workspace>
```

确保文件可读。如有需要：

```console
$ chmod -R u+r <workspace>
```

同时验证工作区路径存在：

```console
$ cd <workspace>
$ pwd
```