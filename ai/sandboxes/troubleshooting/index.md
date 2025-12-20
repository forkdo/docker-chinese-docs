# 故障排除





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    
      
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Availability:</span>
        <span>
          Experimental
          
            
          
            
          
            
              <span class="icon-svg"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M172-120q-41.78 0-59.39-39T124-230l248-280v-270h-52q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h320q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-52v270l248 280q29 32 11.39 71T788-120H172Z"/></svg></span>
            
          
            
          
            
          
        </span>
      </div>
    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 
    
  
  <a class="link" href="/desktop/release-notes/#4500">4.50</a> or later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



本指南帮助您解决在本地为 Claude Code 创建沙箱时的常见问题。

<!-- vale off -->

## 'sandbox' 不是一个 docker 命令

<!-- vale on -->

当您运行 `docker sandbox` 时，会看到一条提示该命令不存在的错误。

这意味着 CLI 插件未安装或未位于正确的位置。要解决此问题：

1. 验证插件是否存在：

   ```console
   $ ls -la ~/.docker/cli-plugins/docker-sandbox
   ```

   该文件应该存在并且是可执行的。

2. 如果使用 Docker Desktop，请重启它以检测该插件。

## 需要由您的管理员启用“实验性功能”

在尝试使用沙箱时，您看到一条关于 Beta 功能被禁用的错误。

当您的 Docker Desktop 安装由锁定了设置的管理员管理时，会发生这种情况。如果您的组织使用了[设置管理](/enterprise/security/hardened-desktop/settings-management/)，请要求您的管理员[允许 Beta 功能](/enterprise/security/hardened-desktop/settings-management/configure-json-file/#beta-features)：

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

Claude 无法进行身份验证，或者您看到 API 密钥错误。

API 密钥可能无效、已过期或未正确配置。解决方法取决于您的凭证模式：

如果使用 `--credentials=sandbox`（默认模式）：

1. 移除已存储的凭证：

   ```console
   $ docker volume rm docker-claude-sandbox-data
   ```

2. 启动一个新的沙箱并完成身份验证工作流：

   ```console
   $ docker sandbox run claude
   ```

## 工作区包含 API 密钥配置

启动沙箱时，您会看到一条关于凭证冲突的警告。

当您的工作区中包含一个带有 `primaryApiKey` 字段的 `.claude.json` 文件时，会发生这种情况。请选择以下方法之一：

- 从您的 `.claude.json` 中移除 `primaryApiKey` 字段：

  ```json
  {
    "apiKeyHelper": "/path/to/script",
    "env": {
      "ANTHROPIC_BASE_URL": "https://api.anthropic.com"
    }
  }
  ```

- 或者在出现警告的情况下继续 - 工作区凭证将被忽略，优先使用沙箱凭证。

## 访问工作区文件时权限被拒绝

当访问工作区中的文件时，Claude 或命令因“权限被拒绝”错误而失败。

这通常意味着工作区路径无法被 Docker 访问，或者文件权限过于严格。

如果使用 Docker Desktop：

1. 在 Docker Desktop → **设置** → **资源** → **文件共享** 中检查文件共享设置。

2. 确保您的工作区路径（或其父目录）已列在虚拟文件共享下。

3. 如果缺失，点击“+”添加包含您工作区的目录。

4. 重启 Docker Desktop。

对于所有平台，请验证文件权限：

```console
$ ls -la <workspace>
```

确保文件是可读的。如果需要：

```console
$ chmod -R u+r <workspace>
```

同时验证工作区路径是否存在：

```console
$ cd <workspace>
$ pwd
```
