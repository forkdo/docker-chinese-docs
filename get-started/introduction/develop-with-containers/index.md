# 使用容器进行开发

<div id="youtube-player-D0SDBrS3t9I" data-video-id="D0SDBrS3t9I" class="youtube-video aspect-video h-fit w-full py-2">
</div>


## 解释

既然您已经安装了 Docker Desktop，就可以开始进行一些应用开发了。具体来说，您将执行以下操作：

1. 克隆并启动一个开发项目
2. 对后端和前端进行更改
3. 立即查看更改结果

## 动手尝试

在本实践指南中，您将学习如何使用容器进行开发。

## 启动项目

1. 首先，克隆项目或[将项目作为 ZIP 文件下载](https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip)到您的本地机器。

    ```console
    $ git clone https://github.com/docker/getting-started-todo-app
    ```

    项目克隆完成后，导航到克隆创建的新目录：

    ```console
    $ cd getting-started-todo-app
    ```

2. 获得项目后，使用 Docker Compose 启动开发环境。

    要使用 CLI 启动项目，请运行以下命令：

   ```console
   $ docker compose watch
   ```

   您将看到输出，显示正在拉取容器镜像、容器正在启动等等。如果此时您还不完全理解也不用担心。但过一会儿，一切就会稳定下来并完成。

3. 打开浏览器访问 [http://localhost](http://localhost) 以查看应用程序已启动并运行。应用程序可能需要几分钟才能运行。这是一个简单的待办事项应用程序，您可以随意添加一两项、标记某些项为已完成，甚至删除某项。

    ![首次启动后待办事项应用的截图](images/develop-getting-started-app-first-launch.webp)

### 环境中包含什么？

现在环境已经启动并运行，其中实际包含什么？从高层次来看，有几个容器（或进程）各自为应用程序提供特定需求：

- React 前端 - 一个运行 React 开发服务器的 Node 容器，使用 [Vite](https://vitejs.dev/)。
- Node 后端 - 后端提供一个 API，用于检索、创建和删除待办事项。
- MySQL 数据库 - 用于存储事项列表的数据库。
- phpMyAdmin - 一个基于 Web 的界面，用于与数据库交互，可通过 [http://db.localhost](http://db.localhost) 访问。
- Traefik 代理 - [Traefik](https://traefik.io/traefik/) 是一个应用程序代理，将请求路由到正确的服务。它将所有对 `localhost/api/*` 的请求发送到后端，对 `localhost/*` 的请求发送到前端，然后对 `db.localhost` 的请求发送到 phpMyAdmin。这提供了使用端口 80 访问所有应用程序的能力（而不是为每个服务使用不同的端口）。

有了这个环境，您作为开发人员无需安装或配置任何服务、填充数据库模式、配置数据库凭据或做任何其他事情。您只需要 Docker Desktop。其余的一切都能正常工作。

## 更改应用程序

环境启动并运行后，您就可以对应用程序进行一些更改，并查看 Docker 如何帮助提供快速的反馈循环。

### 更改问候语

页面顶部的问候语由 `/api/greeting` 的 API 调用填充。目前，它总是返回 "Hello world!"。现在您将修改它以返回三个随机消息之一（您可以选择）。

1. 在文本编辑器中打开 `backend/src/routes/getGreeting.js` 文件。此文件提供 API 端点的处理程序。

2. 将顶部的变量修改为一个问候语数组。您可以使用以下修改，也可以根据自己的喜好进行自定义。此外，更新端点以从此列表中发送随机问候语。

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

3. 如果您还没有保存文件，请保存。如果您刷新浏览器，您应该会看到一个新的问候语。如果您不断刷新，您应该会看到所有消息出现。

    ![带有新问候语的待办事项应用截图](images/develop-app-with-greetings.webp)

### 更改占位符文本

当您查看应用程序时，您会看到占位符文本只是 "New Item"。您现在要让它更具描述性和趣味性。您还将对应用程序的样式进行一些更改。

1. 打开 `client/src/components/AddNewItemForm.jsx` 文件。此文件提供向待办事项列表添加新项的组件。

2. 将 `Form.Control` 元素的 `placeholder` 属性修改为您想要显示的任何内容。

    ```js {linenos=table,hl_lines=[5],linenostart=33}
    <Form.Control
        value={newItem}
        onChange={(e) => setNewItem(e.target.value)}
        type="text"
        placeholder="What do you need to do?"
        aria-label="New item"
    />
    ```

3. 保存文件并返回浏览器。您应该会看到更改已经热重载到您的浏览器中。如果您不喜欢，可以随意调整直到看起来刚刚好。

![在添加项文本字段中更新了占位符的待办事项应用截图"](images/develop-app-with-updated-placeholder.webp)

### 更改背景颜色

在您认为应用程序最终确定之前，您需要让颜色变得更好。

1. 打开 `client/src/index.scss` 文件。

2. 将 `background-color` 属性调整为您喜欢的任何颜色。提供的代码片段是柔和的蓝色，与 Docker 的航海主题相得益彰。

    如果您使用的是 IDE，可以使用集成的颜料选择器选择颜色。否则，可以随意使用在线的[颜色选择器](https://www.w3schools.com/colors/colors_picker.asp)。

    ```css {linenos=table,hl_lines=2,linenostart=3}
    body {
        background-color: #99bbff;
        margin-top: 50px;
        font-family: 'Lato';
    }
    ```

    每次保存都应让您在浏览器中立即看到更改。不断调整，直到它是您完美的设置。

    ![带有新占位符和背景颜色的待办事项应用截图"](images/develop-app-with-updated-client.webp)

就这样，您完成了。恭喜您更新了您的网站。

## 回顾

在继续之前，花点时间反思一下这里发生了什么。在短短的时间内，您能够：

- 以零安装工作量启动一个完整的开发项目。容器化环境提供了开发环境，确保您拥有所需的一切。您无需在机器上直接安装 Node、MySQL 或任何其他依赖项。您只需要 Docker Desktop 和一个代码编辑器。

- 进行更改并立即看到它们。这是通过以下方式实现的：1) 在每个容器中运行的进程正在监视并响应文件更改，2) 文件与容器化环境共享。

Docker Desktop 实现了这一切以及更多功能。一旦您开始用容器思考，您就可以创建几乎任何环境，并轻松地与您的团队共享。

## 下一步

应用程序更新后，您就可以学习如何将其打包为容器镜像并推送到注册表，特别是 Docker Hub。


<a class="button not-prose" href="https://docs.docker.com/get-started/introduction/build-and-push-first-image/">构建并推送您的第一个镜像</a>

