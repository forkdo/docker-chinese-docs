# 在 Compose 中使用生命周期钩子





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="https://docs.docker.com/compose/releases/release-notes/#2300">2.30.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



## 服务生命周期钩子

当 Docker Compose 运行一个容器时，它使用两个元素——
[ENTRYPOINT and COMMAND](/manuals/engine/containers/run.md#default-command-and-options)——
来管理容器启动和停止时发生的行为。

然而，有时使用生命周期钩子单独处理这些任务会更方便——
生命周期钩子是在容器启动后立即或停止前运行的命令。

生命周期钩子之所以特别有用，是因为即使容器本身为了安全而以较低的权限运行，
这些钩子也可以拥有特殊权限（例如以 root 用户身份运行）。
这意味着，某些需要更高权限的任务可以在不损害容器整体安全性的情况下完成。

### 启动后钩子

启动后钩子是在容器启动后运行的命令，但并没有固定的执行时间。
在容器 entrypoint 执行期间，钩子的执行时机无法保证。

在提供的示例中：

- 该钩子用于将一个卷的所有权更改为一个非 root 用户（因为卷默认以 root 用户的所有权创建）。
- 容器启动后，`chown` 命令将 `/data` 目录的所有权更改为用户 `1001`。

```yaml
services:
  app:
    image: backend
    user: 1001
    volumes:
      - data:/data    
    post_start:
      - command: chown -R /data 1001:1001
        user: root

volumes:
  data: {} # a Docker volume is created with root ownership
```

### 停止前钩子

停止前钩子是在容器被特定命令（如 `docker compose down` 或使用 `Ctrl+C` 手动停止）停止之前运行的命令。
如果容器自行停止或被突然终止，这些钩子将不会运行。

在下面的示例中，在容器停止之前，会运行 `./data_flush.sh` 脚本来执行任何必要的清理工作。

```yaml
services:
  app:
    image: backend
    pre_stop:
      - command: ./data_flush.sh
```

## 参考资料

- [`post_start`](/reference/compose-file/services.md#post_start)
- [`pre_stop`](/reference/compose-file/services.md#pre_stop)
