# Docker Sandbox 快速入门





  
  
  
  


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



本指南将帮助你首次在隔离环境中运行 Claude Code。

## 先决条件

开始之前，请确保你已具备以下条件：

- Docker Desktop 4.50 或更高版本
- Claude Code 订阅

## 运行沙箱代理

按照以下步骤在沙箱环境中运行 Claude Code：

1. 导航到你的项目

   ```console
   $ cd ~/my-project
   ```

2. 启动沙箱中的 Claude

   ```console
   $ docker sandbox run claude
   ```

3. 身份验证：首次运行时，Claude 会提示你进行身份验证。

   身份验证后，凭据将存储在持久化的 Docker 卷中，并在后续会话中重复使用。

4. Claude Code 在容器内启动。

## 刚才发生了什么？

当你运行 `docker sandbox run claude` 时：

- Docker 从模板镜像创建了一个容器
- 你的当前目录被挂载到容器内的相同路径
- 你的 Git 用户名和邮箱被注入到容器中
- 你的 API 密钥被存储在 Docker 卷中（`docker-claude-sandbox-data`）
- Claude Code 以启用绕过权限的方式启动

容器在后台继续运行。在同一目录中再次运行 `docker sandbox run claude` 会复用现有的容器，使代理能够在会话之间保持状态（已安装的包、临时文件等）。

## 基本命令

以下是一些管理沙箱的基本命令：

### 列出你的沙箱

```console
$ docker sandbox ls
```

显示所有沙箱的 ID、名称、状态和创建时间。

### 删除沙箱

```console
$ docker sandbox rm <sandbox-id>
```

完成工作后删除沙箱。沙箱 ID 可通过 `docker sandbox ls` 获取。

### 查看沙箱详细信息

```console
$ docker sandbox inspect <sandbox-id>
```

以 JSON 格式显示特定沙箱的详细信息。

有关所有命令和选项的完整列表，请参阅 [CLI 参考文档](/reference/cli/docker/sandbox/)。

## 后续步骤

现在你已经成功在沙箱环境中运行了 Claude，可以进一步了解：

- [身份验证策略](claude-code.md#authentication)
- [配置选项](claude-code.md#configuration)
- [高级配置](advanced-config.md)
- [故障排除指南](troubleshooting.md)
