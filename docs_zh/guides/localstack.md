---
description: 如何使用 LocalStack 和 Docker 开发和测试 AWS 云应用程序
keywords: LocalStack, 容器支持开发
title: 使用 LocalStack 和 Docker 开发和测试 AWS 云应用程序
linktitle: 使用 LocalStack 进行 AWS 开发
summary: |
  本指南解释了如何使用 Docker 启动 LocalStack 容器，LocalStack 是一个本地 AWS 云栈模拟器。
tags: [cloud-services]
languages: [js]
params:
  time: 20 分钟
---

在现代应用开发中，在部署到生产环境之前在本地测试云应用程序，可以帮助你更快、更自信地发布。这种方法包括在本地模拟服务，及早发现和修复问题，并快速迭代，而无需承担成本或面对完整云环境的复杂性。像 [LocalStack](https://www.localstack.cloud/) 这样的工具在这一过程中变得 invaluable，它使你能够在本地模拟 AWS 服务，并将应用程序容器化，以获得一致、隔离的测试环境。

在本指南中，你将学习如何：

- 使用 Docker 启动 LocalStack 容器
- 从非容器化应用程序连接到 LocalStack
- 从容器化应用程序连接到 LocalStack

## 什么是 LocalStack？

LocalStack 是一个云服务模拟器，它在你的笔记本电脑上的单个容器中运行。它提供了一种强大、灵活且经济高效的方式来在本地测试和开发基于 AWS 的应用程序。

## 为什么使用 LocalStack？

在本地模拟 AWS 服务可以让你测试应用程序如何与 S3、Lambda 和 DynamoDB 等服务交互，而无需连接到真实的 AWS 云。你可以快速迭代开发，避免在此阶段部署到云的成本和复杂性。

通过在本地模拟这些服务的行为，LocalStack 实现了更快的反馈循环。你的应用程序可以与外部 API 交互，但所有内容都在本地运行，无需处理云配置或网络延迟。

这使得验证集成和测试云场景变得更加容易，而无需在真实环境中配置 IAM 角色或策略。你可以在本地模拟复杂的云架构，并仅在准备就绪时将更改推送到 AWS。

## 将 LocalStack 与 Docker 一起使用

[LocalStack 的官方 Docker 镜像](https://hub.docker.com/r/localstack/localstack) 提供了一种方便的方式来在你的开发机器上运行 LocalStack。它免费使用，运行时不需要任何 API 密钥。你甚至可以使用 [LocalStack Docker 扩展](https://www.docker.com/blog/develop-your-cloud-app-locally-with-the-localstack-extension/) 来使用带有图形用户界面的 LocalStack。

## 先决条件

要遵循本指南，需要满足以下先决条件：

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js](https://nodejs.org/en/download/package-manager)
- [Python 和 pip](https://www.python.org/downloads/)
- Docker 基础知识

## 启动 LocalStack

通过以下步骤启动 LocalStack 的快速演示：

1. 首先 [克隆示例应用程序](https://github.com/dockersamples/todo-list-localstack-docker)。打开终端并运行以下命令：

   ```console
   $ git clone https://github.com/dockersamples/todo-list-localstack-docker
   $ cd todo-list-localstack-docker
   ```

2. 启动 LocalStack

   运行以下命令启动 LocalStack。

   ```console
   $ docker compose -f compose-native.yml up -d
   ```

   此 Compose 文件还包括必需的 Mongo 数据库的规范。你可以通过访问 Docker Desktop 仪表板来验证服务是否已启动并运行。

   ![图显示 LocalStack 和 Mongo 容器在 Docker Desktop 上启动并运行](./images/launch-localstack.webp)

3. 通过选择容器并检查日志来验证 LocalStack 是否已启动并运行。

   ![图显示 LocalStack 容器的日志](./images/localstack-logs.webp)

4. 创建本地 Amazon S3 存储桶

   当你使用 LocalStack 创建本地 S3 存储桶时，你实际上是在模拟在 AWS 上创建 S3 存储桶。这让你能够在不需要真实 AWS 账户的情况下测试和开发与 S3 交互的应用程序。

   要创建本地 Amazon S3 存储桶，请在你的系统上安装 [`awscli-local` CLI](https://github.com/localstack/awscli-local)。`awslocal` 命令是 AWS 命令行接口的轻量级包装器，用于与 LocalStack 配合使用。它让你能够在本地机器上的模拟环境中测试和开发，而无需访问真实的 AWS 服务。

    ```console
    $ pip install awscli-local
    ```

    使用以下命令在 LocalStack 环境中创建新的 S3 存储桶：

    ```console
    $ awslocal s3 mb s3://mysamplebucket
    ```

    命令 `s3 mb s3://mysamplebucket` 告诉 AWS CLI 创建一个名为 `mysamplebucket` 的新 S3 存储桶（mb 表示 `make bucket`）。

    你可以通过在 Docker Desktop 仪表板上选择 LocalStack 容器并查看日志来验证 S3 存储桶是否已创建。日志表明你的 LocalStack 环境已正确配置，现在你可以使用 `mysamplebucket` 来存储和检索对象。

    ![图显示 LocalStack 日志，突出显示 S3 存储桶成功创建](./images/localstack-s3put.webp)

## 在开发中使用 LocalStack

现在你已经熟悉了 LocalStack，是时候看看它在实际中的应用了。在本演示中，你将使用一个包含 React 前端和 Node.js 后端的示例应用程序。此应用程序栈使用以下组件：

- React：用于访问待办事项应用程序的用户友好前端
- Node：负责处理 HTTP 请求的后端
- MongoDB：用于存储所有待办事项数据的数据库
- LocalStack：模拟 Amazon S3 服务并存储和检索图像

![图显示示例待办事项应用程序的技术栈，包括 LocalStack、前端和后端服务](images/localstack-arch.webp)

## 从非容器化应用程序连接到 LocalStack

现在是时候让你的应用程序连接到 LocalStack 了。`index.js` 文件位于 backend/ 目录中，是后端应用程序的主要入口点。

代码与 LocalStack 的 S3 服务交互，该服务通过 `S3_ENDPOINT_URL` 环境变量定义的端点访问，通常设置为 `http://localhost:4556` 用于本地开发。

AWS SDK 中的 `S3Client` 配置为使用此 LocalStack 端点，以及来自环境变量的测试凭据（`AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY`）。此设置允许应用程序在本地模拟的 S3 服务上执行操作，就像与真实的 AWS S3 交互一样，使代码能够灵活适应不同的环境。

代码使用 `multer` 和 `multer-s3` 来处理文件上传。当用户通过 /upload 路由上传图像时，文件会直接存储在 LocalStack 模拟的 S3 存储桶中。存储桶名称从环境变量 `S3_BUCKET_NAME` 中检索。每个上传的文件都会通过在原始文件名后附加当前时间戳来获得唯一名称。然后路由返回上传文件在本地 S3 服务中的 URL，使其可以访问，就像托管在真实的 AWS S3 存储桶中一样。

让我们看看它的实际效果。首先启动 Node.js 后端服务。

1. 更改为 backend/ 目录

   ```console
   $ cd backend/
   ```

2. 安装所需的依赖项：

   ```console
   $ npm install
   ```

3. 设置 AWS 环境变量

   位于 backend/ 目录中的 `.env` 文件已经包含 LocalStack 用于模拟 AWS 服务的占位符凭据和配置值。`AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY` 是占位符凭据，而 `S3_BUCKET_NAME` 和 `S3_ENDPOINT_URL` 是配置设置。无需更改，因为这些值已经为 LocalStack 正确设置。

   > [!TIP]
   >
   > 鉴于你在 Docker 容器中运行 Mongo，而后端 Node 应用在主机上本地运行，请确保在你的 `.env` 文件中设置了 `MONGODB_URI=mongodb://localhost:27017/todos`。

   ```plaintext
   MONGODB_URI=mongodb://localhost:27017/todos
   AWS_ACCESS_KEY_ID=test
   AWS_SECRET_ACCESS_KEY=test
   S3_BUCKET_NAME=mysamplebucket
   S3_ENDPOINT_URL=http://localhost:4566
   AWS_REGION=us-east-1
   ```

   虽然 AWS SDK 可能通常使用以 `AWS_` 开头的环境变量，但此特定应用程序直接在 index.js 文件（位于 backend/ 目录下）中引用以下 `S3_*` 变量来配置 S3Client。

   ```js
   const s3 = new S3Client({
     endpoint: process.env.S3_ENDPOINT_URL, // 使用提供的端点或回退到默认值
     credentials: {
       accessKeyId: process.env.AWS_ACCESS_KEY_ID || 'default_access_key', // 开发的默认值
       secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || 'default_secret_key',  
     },
   });
   ```

4. 启动后端服务器：

   ```console
   $ node index.js
   ```

    你会看到后端服务已成功在端口 5000 上启动的消息。

## 启动前端服务

要启动前端服务，请打开一个新终端并按照以下步骤操作：

1. 导航到 `frontend` 目录：

   ```console
   $ cd frontend
   ```

2. 安装所需的依赖项

   ```console
   $ npm install
   ```

3. 启动前端服务

   ```console
   $ npm run dev
   ```

   此时，你应该看到以下消息：

   ```console
   VITE v5.4.2  ready in 110 ms
   ➜  Local: http://localhost:5173/
   ➜  Network: use --host to expose
   ➜  press h + enter to show help
   ```

   现在你可以通过 [http://localhost:5173](http://localhost:5173) 访问应用程序。继续操作，上传一张图片，选择一个图像文件并点击 **Upload** 按钮。

   ![图显示一个正在运行的待办事项应用程序](images/localstack-todolist.webp)

   你可以通过检查 LocalStack 容器日志来验证图像已上传到 S3 存储桶：

   ![图显示 LocalStack 的日志，突出显示图像已上传到模拟的 S3 存储桶](images/localstack-todolist-s3put.webp)

   `200` 状态码表示 `putObject` 操作（涉及将对象上传到 S3 存储桶）在 LocalStack 环境中成功执行。LocalStack 记录此条目以提供对正在执行的操作的可见性。它有助于调试并确认你的应用程序正在与模拟的 AWS 服务正确交互。

   由于 LocalStack 旨在在本地模拟 AWS 服务，此日志条目表明你的应用程序在本地沙箱环境中执行云操作时按预期运行。

## 从容器化 Node 应用连接到 LocalStack

现在你已经学会了如何将非容器化的 Node.js 应用程序连接到 LocalStack，是时候探索必要的更改，以便在容器化环境中运行完整的应用程序栈。为此，你将创建一个 Compose 文件，指定所有必需的服务——前端、后端、数据库和 LocalStack。

1. 检查 Docker Compose 文件。

   以下 Docker Compose 文件定义了四个服务：`backend`、`frontend`、`mongodb` 和 `localstack`。`backend` 和 `frontend` 服务是你的 Node.js 应用程序，而 `mongodb` 提供数据库，`localstack` 模拟 AWS 服务（如 S3）。

   `backend` 服务依赖于 `localstack` 和 `mongodb` 服务，确保它们在启动之前运行。它还使用 .env 文件作为环境变量。前端服务依赖于后端并设置 API URL。`mongodb` 服务使用持久卷进行数据存储，`localstack` 配置为运行 S3 服务。此设置让你能够在本地使用类似 AWS 的服务开发和测试你的应用程序。

   ```yaml
   services:
     backend:
       build:
         context: ./backend
         dockerfile: Dockerfile
       ports:
         - 5000:5000
       depends_on:
         - localstack
         - mongodb
       env_file:
         - backend/.env

     frontend:
       build:
         context: ./frontend
         dockerfile: Dockerfile
       ports:
         - 5173:5173
       depends_on:
         - backend
       environment:
         - REACT_APP_API_URL=http://backend:5000/api

     mongodb:
       image: mongo
       container_name: mongodb
       volumes:
         - mongodbdata:/data/db
       ports:
         - 27017:27017

     localstack:
       image: localstack/localstack
       container_name: localstack
       ports:
         - 4566:4566
       environment:
         - SERVICES=s3
         - GATEWAY_LISTEN=0.0.0.0:4566
       volumes:
         - ./localstack:/docker-entrypoint-initaws.d"

   volumes:
     mongodbdata:
   ```

2. 修改 backend/ 目录下的 `.env` 文件，使资源使用内部网络名称连接。

   > [!TIP]
   > 鉴于前面的 Compose 文件，应用程序将使用主机名 `localstack` 连接到 LocalStack，而 Mongo 将使用主机名 `mongodb` 连接。

   ```plaintext
   MONGODB_URI=mongodb://mongodb:27017/todos
   AWS_ACCESS_KEY_ID=test
   AWS_SECRET_ACCESS_KEY=test
   S3_BUCKET_NAME=mysamplebucket
   S3_ENDPOINT_URL=http://localstack:4566
   AWS_REGION=us-east-1
   ```

3. 停止正在运行的服务

   确保你通过在终端中按“Ctrl+C”来停止上一步中的 Node 前端和后端服务。此外，你还需要通过在 Docker Desktop 仪表板中选择它们并选择“Delete”按钮来停止 LocalStack 和 Mongo 容器。

4. 通过在克隆项目的根目录中执行以下命令来启动应用程序栈：

   ```console
   $ docker compose -f compose.yml up -d --build
   ```

   稍等片刻，应用程序将启动并运行。

5. 手动创建 S3 存储桶

   Compose 文件不会预先创建 AWS S3 存储桶。运行以下命令在 LocalStack 环境中创建新存储桶：

   ```console
   $ awslocal s3 mb s3://mysamplebucket
   ```

   该命令创建一个名为 `mysamplebucket` 的 S3 存储桶。

   打开 [http://localhost:5173](http://localhost:5173) 访问完整的待办事项应用程序并开始将图像上传到 Amazon S3 存储桶。

   > [!TIP]
   > 为了优化性能并减少开发期间的上传时间，请考虑上传较小的图像文件。较大的图像可能需要更长的处理时间，可能会影响应用程序的整体响应能力。

## 回顾

本指南已引导你完成使用 LocalStack 和 Docker 设置本地开发环境的过程。你已经学会了如何在本地测试基于 AWS 的应用程序，从而降低成本并提高开发工作流程的效率。