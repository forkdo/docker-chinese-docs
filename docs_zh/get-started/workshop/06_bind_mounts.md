---
title: 使用绑定挂载
weight: 60
linkTitle: "Part 5: Use bind mounts"
keywords: 'get started, setup, orientation, quickstart, intro, concepts, containers, docker desktop'
description: 在我们的应用程序中使用绑定挂载
aliases:
 - /guides/walkthroughs/access-local-folder/
 - /get-started/06_bind_mounts/
 - /guides/workshop/06_bind_mounts/
---

在[第四部分](./05_persisting_data.md)中，你使用了卷挂载（volume mount）来持久化
数据库中的数据。当你需要一个持久的地方来存储应用程序数据时，卷挂载是一个很好的选择。

绑定挂载（bind mount）是另一种挂载类型，它允许你将主机文件系统中的目录
共享到容器中。在开发应用程序时，你可以使用绑定挂载将源代码挂载到容器中。容器会立即看到你对代码所做的更改，一旦你保存文件即可。这意味着
你可以在容器中运行监听文件系统变化并做出响应的进程。

在本章中，你将看到如何使用绑定挂载和一个名为
[nodemon](https://npmjs.com/package/nodemon) 的工具来监听文件变化，然后自动重启应用程序。
大多数其他语言和框架中都有类似的工具。

## 快速比较卷类型

以下是使用 `--mount` 的命名卷和绑定挂载的示例：

- 命名卷：`type=volume,src=my-volume,target=/usr/local/data`
- 绑定挂载：`type=bind,src=/path/to/data,target=/usr/local/data`

下表概述了卷挂载和绑定挂载之间的主要区别。

|                                              | 命名卷                                      | 绑定挂载                                          |
| -------------------------------------------- | ------------------------------------------- | ------------------------------------------------- |
| 主机位置                                     | Docker 自动选择                             | 你自行决定                                          |
| 用容器内容填充新卷                           | 是                                          | 否                                                |
| 支持卷驱动                                   | 是                                          | 否                                                |

## 尝试使用绑定挂载

在查看如何使用绑定挂载来开发你的应用程序之前，你可以运行一个快速实验来实际理解绑定挂载的工作原理。

1. 确认你的 `getting-started-app` 目录位于 Docker Desktop 文件共享设置中定义的目录中。此设置定义了你可以与容器共享的文件系统部分。有关访问该设置的详细信息，请参阅 [文件共享](/manuals/desktop/settings-and-maintenance/settings.md#file-sharing)。

    > [!NOTE]
    > **文件共享**选项卡仅在 Hyper-V 模式下可用，因为在 WSL 2 模式和 Windows 容器模式下文件会自动共享。

2. 打开终端并将目录更改为 `getting-started-app` 目录。

3. 运行以下命令，在 `ubuntu` 容器中启动 `bash`，并使用绑定挂载。

   {{< tabs >}}
   {{< tab name="Mac / Linux" >}}

   ```console
   $ docker run -it --mount type=bind,src="$(pwd)",target=/src ubuntu bash
   ```
   
   {{< /tab >}}
   {{< tab name="Command Prompt" >}}

   ```console
   $ docker run -it --mount "type=bind,src=%cd%,target=/src" ubuntu bash
   ```
   
   {{< /tab >}}
   {{< tab name="Git Bash" >}}

   ```console
   $ docker run -it --mount type=bind,src="/$(pwd)",target=/src ubuntu bash
   ```
   
   {{< /tab >}}
   {{< tab name="PowerShell" >}}

   ```console
   $ docker run -it --mount "type=bind,src=$($pwd),target=/src" ubuntu bash
   ```
   
   {{< /tab >}}
   {{< /tabs >}}
   
   `--mount type=bind` 选项告诉 Docker 创建一个绑定挂载，其中 `src` 是你主机上的当前工作目录（`getting-started-app`），`target` 是该目录在容器内应出现的位置（`/src`）。

4. 运行命令后，Docker 在容器文件系统的根目录启动一个交互式 `bash` 会话。

   ```console
   root@ac1237fad8db:/# pwd
   /
   root@ac1237fad8db:/# ls
   bin   dev  home  media  opt   root  sbin  srv  tmp  var
   boot  etc  lib   mnt    proc  run   src   sys  usr
   ```

5. 将目录更改为 `src` 目录。

   这是你启动容器时挂载的目录。列出此目录的内容会显示与主机上 `getting-started-app` 目录相同的文件。

   ```console
   root@ac1237fad8db:/# cd src
   root@ac1237fad8db:/src# ls
   Dockerfile  node_modules  package.json  spec  src  yarn.lock
   ```

6. 创建一个名为 `myfile.txt` 的新文件。

   ```console
   root@ac1237fad8db:/src# touch myfile.txt
   root@ac1237fad8db:/src# ls
   Dockerfile  myfile.txt  node_modules  package.json  spec  src  yarn.lock
   ```

7. 打开主机上的 `getting-started-app` 目录，观察 `myfile.txt` 文件就在目录中。

   ```text
   ├── getting-started-app/
   │ ├── Dockerfile
   │ ├── myfile.txt
   │ ├── node_modules/
   │ ├── package.json
   │ ├── spec/
   │ ├── src/
   │ └── yarn.lock
   ```

8. 从主机上删除 `myfile.txt` 文件。
9. 在容器中，再次列出 `app` 目录的内容。观察到文件现在消失了。

   ```console
   root@ac1237fad8db:/src# ls
   Dockerfile  node_modules  package.json  spec  src  yarn.lock
   ```

10. 使用 `Ctrl` + `D` 停止交互式容器会话。

以上就是对绑定挂载的简要介绍。此过程演示了文件如何在主机和容器之间共享，以及更改如何立即反映在两边。现在你可以使用绑定挂载来开发软件。

## 开发容器

使用绑定挂载在本地开发设置中很常见。优点是开发机器不需要安装所有构建工具和环境。通过单个 docker run 命令，Docker 就会拉取依赖项和工具。

### 在开发容器中运行你的应用

以下步骤描述了如何使用绑定挂载运行开发容器，该容器执行以下操作：

- 将你的源代码挂载到容器中
- 安装所有依赖项
- 启动 `nodemon` 以监听文件系统变化

你可以使用 CLI 或 Docker Desktop 在容器中运行绑定挂载。

{{< tabs >}}
{{< tab name="Mac / Linux CLI" >}}

1. 确保当前没有运行任何 `getting-started` 容器。

2. 从 `getting-started-app` 目录运行以下命令。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 \
       -w /app --mount type=bind,src="$(pwd)",target=/app \
       node:lts-alpine \
       sh -c "yarn install && yarn run dev"
   ```

   以下是命令的详细说明：
   - `-dp 127.0.0.1:3000:3000` - 与之前相同。在分离（后台）模式下运行并创建端口映射
   - `-w /app` - 设置“工作目录”或命令将从其运行的当前目录
   - `--mount type=bind,src="$(pwd)",target=/app` - 将主机上的当前目录绑定挂载到容器中的 `/app` 目录
   - `node:lts-alpine` - 要使用的镜像。注意这是你的应用的基镜像，来自 Dockerfile
   - `sh -c "yarn install && yarn run dev"` - 命令。你正在使用 `sh`（alpine 没有 `bash`）启动一个 shell，运行 `yarn install` 安装包，然后运行 `yarn run dev` 启动开发服务器。如果你查看 `package.json`，你会看到 `dev` 脚本启动 `nodemon`。

3. 你可以使用 `docker logs <container-id>` 观察日志。当你看到以下内容时，你就准备好了：

   ```console
   $ docker logs -f <container-id>
   nodemon -L src/index.js
   [nodemon] 2.0.20
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching path(s): *.*
   [nodemon] watching extensions: js,mjs,json
   [nodemon] starting `node src/index.js`
   Using sqlite database at /etc/todos/todo.db
   Listening on port 3000
   ```

   当你完成观察日志后，按 `Ctrl`+`C` 退出。

{{< /tab >}}
{{< tab name="PowerShell CLI" >}}

1. 确保当前没有运行任何 `getting-started` 容器。

2. 从 `getting-started-app` 目录运行以下命令。

   ```powershell
   $ docker run -dp 127.0.0.1:3000:3000 `
       -w /app --mount "type=bind,src=$pwd,target=/app" `
       node:lts-alpine `
       sh -c "yarn install && yarn run dev"
   ```

   以下是命令的详细说明：
   - `-dp 127.0.0.1:3000:3000` - 与之前相同。在分离（后台）模式下运行并创建端口映射
   - `-w /app` - 设置“工作目录”或命令将从其运行的当前目录
   - `--mount "type=bind,src=$pwd,target=/app"` - 将主机上的当前目录绑定挂载到容器中的 `/app` 目录
   - `node:lts-alpine` - 要使用的镜像。注意这是你的应用的基镜像，来自 Dockerfile
   - `sh -c "yarn install && yarn run dev"` - 命令。你正在使用 `sh`（alpine 没有 `bash`）启动一个 shell，运行 `yarn install` 安装包，然后运行 `yarn run dev` 启动开发服务器。如果你查看 `package.json`，你会看到 `dev` 脚本启动 `nodemon`。

3. 你可以使用 `docker logs <container-id>` 观察日志。当你看到以下内容时，你就准备好了：

   ```console
   $ docker logs -f <container-id>
   nodemon -L src/index.js
   [nodemon] 2.0.20
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching path(s): *.*
   [nodemon] watching extensions: js,mjs,json
   [nodemon] starting `node src/index.js`
   Using sqlite database at /etc/todos/todo.db
   Listening on port 3000
   ```

   当你完成观察日志后，按 `Ctrl`+`C` 退出。

{{< /tab >}}
{{< tab name="Command Prompt CLI" >}}

1. 确保当前没有运行任何 `getting-started` 容器。

2. 从 `getting-started-app` 目录运行以下命令。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 ^
       -w /app --mount "type=bind,src=%cd%,target=/app" ^
       node:lts-alpine ^
       sh -c "yarn install && yarn run dev"
   ```

   以下是命令的详细说明：
   - `-dp 127.0.0.1:3000:3000` - 与之前相同。在分离（后台）模式下运行并创建端口映射
   - `-w /app` - 设置“工作目录”或命令将从其运行的当前目录
   - `--mount "type=bind,src=%cd%,target=/app"` - 将主机上的当前目录绑定挂载到容器中的 `/app` 目录
   - `node:lts-alpine` - 要使用的镜像。注意这是你的应用的基镜像，来自 Dockerfile
   - `sh -c "yarn install && yarn run dev"` - 命令。你正在使用 `sh`（alpine 没有 `bash`）启动一个 shell，运行 `yarn install` 安装包，然后运行 `yarn run dev` 启动开发服务器。如果你查看 `package.json`，你会看到 `dev` 脚本启动 `nodemon`。

3. 你可以使用 `docker logs <container-id>` 观察日志。当你看到以下内容时，你就准备好了：

   ```console
   $ docker logs -f <container-id>
   nodemon -L src/index.js
   [nodemon] 2.0.20
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching path(s): *.*
   [nodemon] watching extensions: js,mjs,json
   [nodemon] starting `node src/index.js`
   Using sqlite database at /etc/todos/todo.db
   Listening on port 3000
   ```

   当你完成观察日志后，按 `Ctrl`+`C` 退出。

{{< /tab >}}
{{< tab name="Git Bash CLI" >}}

1. 确保当前没有运行任何 `getting-started` 容器。

2. 从 `getting-started-app` 目录运行以下命令。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 \
       -w //app --mount type=bind,src="/$(pwd)",target=/app \
       node:lts-alpine \
       sh -c "yarn install && yarn run dev"
   ```

   以下是命令的详细说明：
   - `-dp 127.0.0.1:3000:3000` - 与之前相同。在分离（后台）模式下运行并创建端口映射
   - `-w //app` - 设置“工作目录”或命令将从其运行的当前目录
   - `--mount type=bind,src="/$(pwd)",target=/app` - 将主机上的当前目录绑定挂载到容器中的 `/app` 目录
   - `node:lts-alpine` - 要使用的镜像。注意这是你的应用的基镜像，来自 Dockerfile
   - `sh -c "yarn install && yarn run dev"` - 命令。你正在使用 `sh`（alpine 没有 `bash`）启动一个 shell，运行 `yarn install` 安装包，然后运行 `yarn run dev` 启动开发服务器。如果你查看 `package.json`，你会看到 `dev` 脚本启动 `nodemon`。

3. 你可以使用 `docker logs <container-id>` 观察日志。当你看到以下内容时，你就准备好了：

   ```console
   $ docker logs -f <container-id>
   nodemon -L src/index.js
   [nodemon] 2.0.20
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching path(s): *.*
   [nodemon] watching extensions: js,mjs,json
   [nodemon] starting `node src/index.js`
   Using sqlite database at /etc/todos/todo.db
   Listening on port 3000
   ```

   当你完成观察日志后，按 `Ctrl`+`C` 退出。

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

确保当前没有运行任何 `getting-started` 容器。

使用绑定挂载运行镜像。

1. 在 Docker Desktop 顶部选择搜索框。
2. 在搜索窗口中，选择 **Images** 选项卡。
3. 在搜索框中，指定容器名称 `getting-started`。

   > [!TIP]
   >
   > 使用搜索过滤器过滤镜像，仅显示 **Local images**。

4. 选择你的镜像，然后选择 **Run**。
5. 选择 **Optional settings**。
6. 在 **Host path** 中，指定主机上 `getting-started-app` 目录的路径。
7. 在 **Container path** 中，指定 `/app`。
8. 选择 **Run**。

你可以使用 Docker Desktop 观察容器日志。

1. 在 Docker Desktop 中选择 **Containers**。
2. 选择你的容器名称。

当你看到以下内容时，你就准备好了：

```console
nodemon -L src/index.js
[nodemon] 2.0.20
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `node src/index.js`
Using sqlite database at /etc/todos/todo.db
Listening on port 3000
```

{{< /tab >}}
{{< /tabs >}}

### 使用开发容器开发你的应用

在主机上更新你的应用，观察更改在容器中的反映。

1. 在 `src/static/js/app.js` 文件中，第 109 行，将“Add Item”按钮更改为仅显示“Add”：

   ```diff
   - {submitting ? 'Adding...' : 'Add Item'}
   + {submitting ? 'Adding...' : 'Add'}
   ```

   保存文件。

2. 刷新浏览器中的页面，你应该几乎立即看到更改，这是因为绑定挂载。Nodemon 检测到更改并重启服务器。Node 服务器重启可能需要几秒钟。如果你遇到错误，请在几秒钟后尝试刷新。

   ![Screenshot of updated