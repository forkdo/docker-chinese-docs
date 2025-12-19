---
title: 更新应用程序
weight: 30
linkTitle: "第 2 部分：更新应用程序"
keywords: get started, setup, orientation, quickstart, intro, concepts, containers,
  docker desktop
description: 对应用程序进行更改
aliases:
 - /get-started/03_updating_app/
 - /guides/workshop/03_updating_app/
---

在[第 1 部分](./02_our_app.md)中，你已经将一个待办事项应用程序容器化。在本部分中，你将更新应用程序和镜像。你还将学习如何停止和移除容器。

## 更新源代码

在以下步骤中，你将更改当没有待办事项列表项时显示的"空文本"，将其改为"You have no todo items yet! Add one above!"。

1. 在 `src/static/js/app.js` 文件中，将第 56 行更新为使用新的空文本。

   ```diff
   - <p className="text-center">No items yet! Add one above!</p>
   + <p className="text-center">You have no todo items yet! Add one above!</p>
   ```

2. 使用 `docker build` 命令构建更新后的镜像版本。

   ```console
   $ docker build -t getting-started .
   ```

3. 使用更新后的代码启动一个新容器。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 getting-started
   ```

你可能会看到类似这样的错误：

```console
docker: Error response from daemon: driver failed programming external connectivity on endpoint laughing_burnell 
(bb242b2ca4d67eba76e79474fb36bb5125708ebdabd7f45c8eaf16caaabde9dd): Bind for 127.0.0.1:3000 failed: port is already allocated.
```

出现这个错误是因为在旧容器仍在运行时，你无法启动新容器。原因是旧容器已经在使用主机的 3000 端口，而机器上只能有一个进程（包括容器）监听特定端口。要解决这个问题，你需要移除旧容器。

## 移除旧容器

要移除容器，首先需要停止它。一旦停止，就可以将其移除。你可以使用 CLI 或 Docker Desktop 的图形界面来移除旧容器。选择你最习惯的方式。

{{< tabs >}}
{{< tab name="CLI" >}}

### 使用 CLI 移除容器

1. 使用 `docker ps` 命令获取容器的 ID。

   ```console
   $ docker ps
   ```

2. 使用 `docker stop` 命令停止容器。将 `<the-container-id>` 替换为 `docker ps` 中的 ID。

   ```console
   $ docker stop <the-container-id>
   ```

3. 容器停止后，可以使用 `docker rm` 命令将其移除。

   ```console
   $ docker rm <the-container-id>
   ```

> [!NOTE]
>
> 你可以通过在 `docker rm` 命令中添加 `force` 标志来一次性停止并移除容器。例如：`docker rm -f <the-container-id>`

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

### 使用 Docker Desktop 移除容器

1. 打开 Docker Desktop 并进入 **Containers** 视图。
2. 为要删除的容器选择 **Actions** 列下的垃圾桶图标。
3. 在确认对话框中，选择 **Delete forever**。

{{< /tab >}}
{{< /tabs >}}

### 启动更新后的应用容器

1. 现在，使用 `docker run` 命令启动更新后的应用。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 getting-started
   ```

2. 在浏览器中刷新 [http://localhost:3000](http://localhost:3000)，你应该能看到更新后的帮助文本。

## 总结

在本节中，你学习了如何更新和重新构建镜像，以及如何停止和移除容器。

相关信息：
 - [docker CLI 参考文档](/reference/cli/docker/)

## 下一步

接下来，你将学习如何与他人共享镜像。

{{< button text="共享应用程序" url="04_sharing_app.md" >}}