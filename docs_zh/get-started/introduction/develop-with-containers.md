---
title: 使用容器进行开发
keywords: 概念, build, 镜像, 容器, docker desktop
description: 本概念页面将教你如何使用容器进行开发
summary: |
  学习如何运行你的第一个容器，通过 Docker 强大的功能获得实践经验。我们将涵盖对容器化环境中后端和前端代码进行实时更改，确保无缝集成和测试。
weight: 2
aliases:
 - /guides/getting-started/develop-with-containers/
---

{{< youtube-embed D0SDBrS3t9I >}}

## 说明

现在你已经安装了 Docker Desktop，你已经准备好进行一些应用程序开发了。具体来说，你将完成以下内容：

1. 克隆并启动一个开发项目
2. 对后端和前端进行更改
3. 立即看到更改效果

## 动手尝试

在本实践指南中，你将学习如何使用容器进行开发。


## 启动项目

1. 首先，克隆或[将项目作为 ZIP 文件下载](https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip)到本地机器。

    ```console
    $ git clone https://github.com/docker/getting-started-todo-app
    ```

    项目克隆完成后，导航到克隆创建的新目录：

    ```console
    $ cd getting-started-todo-app
    ```

2. 获得项目后，使用 Docker Compose 启动开发环境。


    要通过 CLI 启动项目，请运行以下命令：

   ```console
   $ docker compose watch
   ```

   你将看到输出显示容器镜像正在被拉取，容器正在启动等。不用担心此时你可能不完全理解这些内容。但一两分钟后，一切应该会稳定并完成。


3. 在浏览器中打开 [http://localhost](http://localhost) 查看应用程序正在运行。应用程序启动可能需要几分钟。这是一个简单的待办事项应用程序，所以可以随意添加一些项目，标记为已完成，或删除一些项目。

    ![首次启动待办事项应用程序的截图](images/develop-getting-started-app-first-launch.webp)


### 环境中有什么？

现在环境已经启动并运行，其中实际包含什么？从高层次来看，有几个容器（或进程），每个都为应用程序提供特定的服务：

- React 前端 - 一个运行 React 开发服务器的 Node 容器，使用 [Vite](https://vitejs.dev/)。
- Node 后端 - 后端提供一个 API，用于检索、创建和删除待办事项。
- MySQL 数据库 - 用于存储项目列表的数据库。
- phpMyAdmin - 一个基于 Web 的数据库交互界面，可通过 [http://db.localhost](http://db.localhost) 访问。
- Traefik 代理 - [Traefik](https://traefik.io/traefik/) 是一个应用代理，将请求路由到正确的服务。它将所有 `localhost/api/*` 请求发送到后端，将 `localhost/*` 请求发送到前端，将 `db.localhost` 请求发送到 phpMyAdmin。这提供了使用端口 80 访问所有应用程序的能力（而不是为每个服务使用不同的端口）。

有了这个环境，作为开发者的你不需要安装或配置任何服务，填充数据库模式，配置数据库凭据，或做其他任何事情。你只需要 Docker Desktop。其余的都能正常工作。


## 对应用程序进行更改

环境启动并运行后，你就可以对应用程序进行一些更改，并看看 Docker 如何帮助提供快速的反馈循环。

### 更改问候语

页面顶部的问候语由 `/api/greeting` 的 API 调用填充。目前，它总是返回 "Hello world!"。现在你将修改它，使其返回三个随机消息之一（你可以选择）。

1. 在文本编辑器中打开 `backend/src/routes/getGreeting.js` 文件。此文件提供 API 端点的处理器。

2. 修改顶部的变量为问候语数组。可以使用以下修改或根据自己的喜好自定义。同时，更新端点以从此列表中发送随机问候语。

    ```js {linenos=table,hl_lines=["1-5",9],linenostart=1}
    const GREETINGS = [
        "Whalecome!",
        "All hands on deck!",
        "Charting the course ahead!",
    ];

    module.exports = async (req, res) => {
        res.send({
            greeting: GREETINGS[ Math.floor( Math.random() * GREETINGS.length )],
        });
    };
    ```

3. 如果还没有保存文件，请保存。刷新浏览器后，你应该看到新的问候语。继续刷新，你应该能看到所有消息出现。

    ![带有新问候语的待办事项应用程序截图](images/develop-app-with-greetings.webp)


### 更改占位符文本

查看应用程序时，你会看到占位符文本只是 "New Item"。现在你将让它更详细、更有趣。你还将对应用程序的样式进行一些更改。

1. 打开 `client/src/components/AddNewItemForm.jsx` 文件。这提供了向待办事项列表添加新项目的组件。

2. 修改 `Form.Control` 元素的 `placeholder` 属性为你想要显示的内容。

    ```js {linenos=table,hl_lines=[5],linenostart=33}
    <Form.Control
        value={newItem}
        onChange={(e) => setNewItem(e.target.value)}
        type="text"
        placeholder="What do you need to do?"
        aria-label="New item"
    />
    ```

3. 保存文件并回到浏览器。你应该看到更改已经热重载到浏览器中。如果不喜欢，可以随意调整，直到看起来完美。

![在添加项目文本字段中带有更新占位符的待办事项应用程序截图](images/develop-app-with-updated-placeholder.webp)


### 更改背景颜色

在你考虑完成应用程序之前，你需要让颜色更好看。

1. 打开 `client/src/index.scss` 文件。

2. 将 `background-color` 属性调整为你喜欢的任何颜色。提供的代码片段是一种柔和的蓝色，与 Docker 的航海主题相配。

    如果你使用的是 IDE，可以使用集成的颜色选择器选择颜色。否则，可以使用在线 [颜色选择器](https://www.w3schools.com/colors/colors_picker.asp)。

    ```css {linenos=table,hl_lines=2,linenostart=3}
    body {
        background-color: #99bbff;
        margin-top: 50px;
        font-family: 'Lato';
    }
    ```

    每次保存都应该让你立即在浏览器中看到更改。继续调整，直到它对你来说完美。

    ![带有新占位符和背景颜色的待办事项应用程序截图](images/develop-app-with-updated-client.webp)

这样，你就完成了。恭喜你更新了你的网站。


## 回顾

在继续之前，花点时间反思一下这里发生了什么。在几分钟内，你能够：

- 启动一个完整的开发项目，无需任何安装工作。容器化环境提供了开发环境，确保你拥有所需的一切。你不需要在机器上直接安装 Node、MySQL 或任何其他依赖项。你只需要 Docker Desktop 和一个代码编辑器。

- 进行更改并立即看到效果。这是可能的，因为 1) 每个容器中运行的进程正在监视并响应文件更改，以及 2) 文件与容器化环境共享。

Docker Desktop 实现了所有这些以及更多功能。一旦你开始用容器思考，你就可以创建几乎任何环境并轻松与团队共享。

## 下一步

现在应用程序已更新，你准备好学习如何将其打包为容器镜像并推送到注册表，特别是 Docker Hub。

{{< button text="构建并推送你的第一个镜像" url="build-and-push-first-image" >}}

