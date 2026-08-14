<!-- FILE: manuals/compose/how-tos/lifecycle.md -->

---
title: 在 Compose 中使用生命周期钩子
linkTitle: 使用生命周期钩子
weight: 110
description: 了解如何使用 Docker Compose 的生命周期钩子（如 pre_start、post_start 和 pre_stop）来自定义容器行为。
keywords: docker compose lifecycle hooks, post_start, pre_stop, pre_start, docker compose entrypoint, docker container stop hooks, compose hook commands
---

{{< summary-bar feature_name="Compose lifecycle hooks" >}}

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

由于钩子与容器 entrypoint 之间没有执行顺序保证，
启动后钩子最适合用于那些不需要在应用开始运行前完成的任务，例如向外部系统注册容器。

在以下示例中，容器启动后，一个以 root 权限运行的钩子将服务注册到内部服务注册表中。应用并不依赖注册在其开始提供服务之前完成。

```yaml
services:
  app:
    image: backend
    user: 1001
    post_start:
      - command: /opt/scripts/register-service.sh
        user: root
```

### 停止前钩子

停止前钩子是在容器被特定命令（如 `docker compose down` 或使用 `Ctrl+C` 手动停止）停止之前运行的命令。
如果容器自行停止或被突然终止，这些钩子将不会运行。

由于停止前钩子会在停止信号发送给容器之前运行，它适用于那些必须在应用仍在完全运行时完成的操作。

在以下示例中，钩子在容器收到停止信号之前备份了一个数据文件。

```yaml
services:
  app:
    image: backend
    volumes:
      - data:/data
    pre_stop:
      - command: cp /data/app.db /data/app.db.bak

volumes:
  data: {} # a Docker volume is created with root ownership
```

## 参考资料

- [`post_start`](/reference/compose-file/services.md#post_start)
- [`pre_stop`](/reference/compose-file/services.md#pre_stop)
- [`pre_start`](/reference/compose-file/services.md#pre_start)
