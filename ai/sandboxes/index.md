# Docker 沙盒





  
  
  
  


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
    
  
  <a class="link" href="https://docs.docker.com/desktop/release-notes/#4500">4.50</a> or later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



Docker 沙盒可简化在本地机器上安全运行 AI 代理的过程。
该功能专为使用 Claude Code 等编码代理进行开发的开发者设计，
将代理与您的本地机器隔离，同时保留熟悉的开发体验。
通过 Docker 沙盒，代理可以在容器化的工作区中执行命令、
安装软件包和修改文件，该工作区会镜像您的本地目录。
这让您在获得完整代理自主权的同时，也能确保安全性。

## 工作原理

当您运行 `docker sandbox run <agent>` 时：

1. Docker 从模板镜像创建容器，并将您当前的工作目录以相同路径挂载到容器中。

2. Docker 会发现您的 Git `user.name` 和 `user.email` 配置，并将其注入容器，
   以便代理所做的提交归属于您。

3. 首次运行时，系统会提示您进行身份验证。凭据会存储在 Docker 卷中，
   并在后续的沙盒代理中重复使用。

4. 代理在容器内启动，并启用了绕过权限。

### 工作区挂载

您的工作区目录会以相同的绝对路径（在 macOS 和 Linux 上）挂载到容器中。
例如，主机上的 `/Users/alice/projects/myapp` 在容器中也是
`/Users/alice/projects/myapp`。这意味着：

- 错误消息中的文件路径与主机匹配
- 硬编码路径的脚本能按预期工作
- 对工作区文件的更改在主机和容器上都立即可见

### 每个工作区一个沙盒

Docker 强制每个工作区只能有一个沙盒。当您在同一目录下运行
`docker sandbox run <agent>` 时，Docker 会复用现有的容器。
这意味着状态（已安装的软件包、临时文件）会在该工作区的
多次代理会话中持续保留。

> [!NOTE]
> 要更改沙盒的配置（环境变量、挂载卷等），
> 您需要先移除再重新创建它。详情请参见
> [管理沙盒](advanced-config.md#managing-sandboxes)。

## 发布状态

Docker 沙盒是一项实验性功能。功能和设置可能会发生变化。

请在 GitHub 上报告问题：
- [Docker Desktop for Mac](https://github.com/docker/for-mac)
- [Docker Desktop for Windows](https://github.com/docker/for-win)
- [Docker Desktop for Linux](https://github.com/docker/desktop-linux)

## 开始使用

前往[入门指南](get-started.md)运行您的第一个沙盒代理。

- [Docker Sandbox 快速入门](https://docs.docker.com/ai/sandboxes/get-started/)

- [配置 Claude Code](https://docs.docker.com/ai/sandboxes/claude-code/)

- [高级配置](https://docs.docker.com/ai/sandboxes/advanced-config/)

- [故障排除](https://docs.docker.com/ai/sandboxes/troubleshooting/)

