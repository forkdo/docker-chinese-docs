# 使用 Docker Desktop CLI





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 
    
  
  <a class="link" href="/desktop/release-notes/#4370">4.37</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



Docker Desktop CLI 让您可以直接从命令行执行关键操作，例如启动、停止、重启和更新 Docker Desktop。

Docker Desktop CLI 提供：

- 简化的本地开发自动化：在脚本和测试中更高效地执行 Docker Desktop 操作。
- 改进的开发者体验：从命令行重启、退出或重置 Docker Desktop，减少对 Docker Desktop Dashboard 的依赖，提高灵活性和效率。

## 用法

```console
docker desktop COMMAND [OPTIONS]
```

## 命令

| 命令                 | 描述                                                             |
|:---------------------|:-----------------------------------------------------------------|
| `start`              | 启动 Docker Desktop                                              |
| `stop`               | 停止 Docker Desktop                                              |
| `restart`            | 重启 Docker Desktop                                              |
| `status`             | 显示 Docker Desktop 正在运行还是已停止。                         |
| `engine ls`          | 列出可用的引擎（仅限 Windows）                                   |
| `engine use`         | 在 Linux 和 Windows 容器之间切换（仅限 Windows）                 |
| `update`             | 管理 Docker Desktop 更新。在 Docker Desktop 4.38 版本中仅适用于 Mac，在 4.39 及更高版本中适用于所有操作系统。 |
| `logs`               | 打印日志条目                                                     |
| `disable`            | 禁用功能                                                         |
| `enable`             | 启用功能                                                         |
| `version`            | 显示 Docker Desktop CLI 插件版本信息                             |
| `kubernetes`         | 列出 Docker Desktop 使用的 Kubernetes 镜像或重启集群。在 Docker Desktop 4.44 及更高版本中可用。 |

有关每个命令的更多详细信息，请参阅 [Docker Desktop CLI 参考](/reference/cli/docker/desktop/_index.md)。
