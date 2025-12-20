# 使用 LocalStack 和 Docker 开发与测试 AWS Cloud 应用程序

在现代应用程序开发中，在将云应用程序部署到生产环境之前进行本地测试，有助于您更快速、更自信地交付产品。这种方法涉及在本地模拟服务、尽早发现并修复问题，以及快速迭代，而无需承担成本或面对完整云环境的复杂性。像 [LocalStack](https://www.localstack.cloud/) 这样的工具在此过程中变得非常宝贵，它使您能够模拟 AWS 服务并将应用程序容器化，以获得一致且隔离的测试环境。

在本指南中，您将学习如何：

- 使用 Docker 启动 LocalStack 容器
- 从未容器化的应用程序连接到 LocalStack
- 从容器化的应用程序连接到 LocalStack

## 什么是 LocalStack？

LocalStack 是一个云服务模拟器，它在您的笔记本电脑上的单个容器中运行。它提供了一种强大、灵活且经济高效的方式来在本地测试和开发基于 AWS 的应用程序。

## 为什么要使用 LocalStack？

在本地模拟 AWS 服务允许您测试您的应用程序如何与 S3、Lambda 和 DynamoDB 等服务交互，而无需连接到真实的 AWS 云。您可以快速迭代开发，避免在此阶段部署到云所产生的成本和复杂性。

通过在本地模仿这些服务的行为，LocalStack 能够实现更快的反馈循环。您的应用程序可以与外部 API 交互，但所有操作都在本地运行，无需处理云配置或网络延迟。

这使得验证集成和测试基于云的场景变得更加容易，而无需在生产环境中配置 IAM 角色或策略。您可以在本地模拟复杂的云架构，并仅在准备好时才将更改推送到 AWS。

## 将 LocalStack 与 Docker 结合使用

[LocalStack 的官方 Docker 镜像](https://hub.docker.com/r/localstack/localstack) 提供了一种在开发机器上运行 LocalStack 的便捷方式。它是免费使用的，不需要任何 API 密钥即可运行。您甚至可以使用 [LocalStack Docker Extension](https://www.docker.com/blog/develop-your-cloud-app-locally-with-the-localstack-extension/) 通过图形用户界面使用 LocalStack。

## 先决条件

要遵循本操作指南，需要满足以下先决条件：

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js](https://nodejs.org/en/download/package-manager)
- [Python 和 pip](https://www.python.org/downloads/)
- Docker 的基本知识

## 启动 LocalStack

通过以下步骤启动 LocalStack 的快速演示：

1. 首先[克隆一个示例应用程序](https://github.com/dockersamples/todo-list-localstack-docker)。打开终端并运行以下命令：

   ```console
   $ git clone https://github.com/dockersamples/todo-list-localstack-docker
   $ cd todo-list-localstack-docker
   ```

2. 启动 LocalStack

   运行以下命令以启动 LocalStack。

   ```console
   $ docker compose -f compose-native.yml up -d
   ```

   此 Compose 文件还包含所需 Mongo 数据库的规范。您可以通过访问 Docker Desktop 仪表板来验证服务是否已启动并正在运行。

   ![显示 LocalStack 和 Mongo 容器在 Docker Desktop 上运行的图示](./images/launch-localstack.webp)

3. 通过选择容器并检查日志来验证 LocalStack 是否已启动并正在运行。

   ![显示 LocalStack 容器日志的图示](./images/localstack-logs.webp)

4. 创建本地 Amazon S3 存储桶

   当您使用 LocalStack 创建本地 S3 存储桶时，您实际上是在模拟在 AWS 上创建 S3 存储桶。这使您可以测试和开发与 S3 交互的应用程序，而无需实际的 AWS 账户。

   要创建本地 Amazon S3 存储桶，请在您的系统上安装 [`awscli-local` CLI](https://github.com/localstack/awscli-local)。`awslocal` 命令是 AWS 命令行界面的一个薄包装，用于与 LocalStack 一起使用。它允许您针对本地机器上的模拟环境进行测试和开发，而无需访问真实的 AWS 服务。

    ```console
    $ pip install awscli-local
    ```

    在 LocalStack 环境中使用以下命令创建一个新的 S3 存储桶：

    ```console
    $ awslocal s3 mb s3://mysamplebucket
    ```

    命令 `s3 mb s3://mysamplebucket` 告诉 AWS CLI 创建一个名为 `mysamplebucket` 的新 S3 存储桶（mb 代表 `make bucket`）。

    您可以通过在 Docker Desktop 仪表板上选择 LocalStack 容器并查看日志来验证 S3 存储桶是否已创建。日志表明您的 LocalStack 环境配置正确，您现在可以使用 `mysamplebucket` 来存储和检索对象。

    ![显示 LocalStack 日志的图示，突出显示 S3 存储桶已成功创建](./images/localstack-s3put.webp)

## 在开发中使用 LocalStack

现在您已经熟悉了 LocalStack，是时候看看它的实际应用了。在本演示中，您将使用一个包含 React 前端和 Node.js 后端的示例应用程序。此应用程序堆栈利用以下组件：

- React：用于访问待办事项列表应用程序的用户友好前端
- Node：负责处理 HTTP 请求的后端
- MongoDB：用于存储所有待办事项列表数据的数据库
- LocalStack：模拟 Amazon S3 服务并存储和检索图像

![显示示例待办事项列表应用程序技术堆栈的图示，包括 LocalStack、前端和后端服务](images/localstack-arch.webp)

## 从未容器化的应用程序连接到 LocalStack

现在是将您的应用程序连接到 LocalStack 的时候了。位于 `backend/` 目录中的 `index.js` 文件是后端应用程序的主要入口点。

该代码与 LocalStack 的 S3 服务交互，该服务通过 `S3_ENDPOINT_URL` 环境变量定义的端点访问，对于本地开发通常设置为 `http://localhost:4556`。

来自 AWS SDK 的 `S3Client` 被配置为使用此 LocalStack 端点，以及同样来自环境变量的测试凭证（`AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY`）。这种设置让应用程序能够在本地模拟的 S3 服务上执行操作，就像与真实的 AWS S3 交互一样，使代码能够灵活适应不同的环境。

该代码使用 `multer` 和 `multer-s3` 来处理文件上传。当用户通过 `/upload` 路径上传图像时，文件直接存储在 LocalStack 模拟的 S3 存储桶中。存储桶名称从环境变量 `S3_BUCKET_NAME` 中检索。每个上传的文件都会通过将当前时间戳附加到原始文件名来获得一个唯一的名称。然后，该路由返回上传文件在本地 S3 服务中的 URL，使其可访问，就像托管在真实的 AWS S3 存储桶上一样。

让我们看看它的实际操作。首先启动 Node.js 后端服务。

1. 切换到 `backend/` 目录

   ```console
   $ cd backend/
   ```

2. 安装所需的依赖项：

   ```console
   $ npm install
   ```

3. 设置 AWS 环境变量

   位于 `backend/` 目录中的 `.env` 文件已经包含 LocalStack 用于模拟 AWS 服务的占位符凭证和配置值。`AWS_ACCESS_KEY_ID` 和 `AWS_SECRET_ACCESS_KEY` 是占位符凭证，而 `S3_BUCKET_NAME` 和 `S3_ENDPOINT_URL` 是配置设置。无需更改，因为这些值已经为 LocalStack 正确设置。

   > [!TIP]
   >
   > 鉴于您在 Docker 容器中运行 Mongo，而后端 Node 应用在您的主机上原生运行，请确保在您的 `.env` 文件中设置了 `MONGODB_URI=mongodb://localhost:27017/todos`。

   ```plaintext
   MONGODB_URI=mongodb://localhost:27017/todos
   AWS_ACCESS_KEY_ID=test
   AWS_SECRET_ACCESS_KEY=test
   S3_BUCKET_NAME=mysamplebucket
   S3_ENDPOINT_URL=http://localhost:4566
   AWS_REGION=us-east-1
   ```

   虽然 AWS SDK 通常使用以 `AWS_` 开头的环境变量，但此特定应用程序直接在 `index.js` 文件（位于 `backend/` 目录下）中引用以下 `S3_*` 变量来配置 S3Client。

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

    您将看到后端服务已成功在端口 5000 启动的消息。

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

   此时，您应该看到以下消息：

   ```console
   VITE v5.4.2  ready in 110 ms
   ➜  Local: http://localhost:5173/
   ➜  Network: use --host to expose
   ➜  press h + enter to show help
   ```

   您现在可以通过 [http://localhost:5173](http://localhost:5173) 访问该应用程序。继续操作，选择一个图像文件并点击 **Upload** 按钮上传图像。

   ![显示正在工作的待办事项列表应用程序的图示](images/localstack-todolist.webp)

   您可以通过检查 LocalStack 容器日志来验证图像是否已上传到 S3 存储桶：

   ![显示 LocalStack 日志的图示，突出显示图像已上传到模拟的 S3 存储桶](images/localstack-todolist-s3put.webp)

   `200` 状态码表示 `putObject` 操作（涉及将对象上传到 S3 存储桶）已在 LocalStack 环境中成功执行。LocalStack 记录此条目以提供对正在执行的操作的可见性。它有助于调试和确认您的应用程序是否与模拟的 AWS 服务正确交互。

   由于 LocalStack 旨在本地模拟 AWS 服务，此日志条目表明您的应用程序在本地沙盒环境中执行云操作时按预期运行。

## 从容器化的 Node 应用程序连接到 LocalStack

现在您已经了解了如何将非容器化的 Node.js 应用程序连接到 LocalStack，是时候探索在容器化环境中运行完整应用程序堆栈所需的更改了。为此，您将创建一个 Compose 文件，指定所有必需的服务 - 前端、后端、数据库和 LocalStack。

1. 检查 Docker Compose 文件。

   以下 Docker Compose 文件定义了四个服务：`backend`、`frontend`、`mongodb` 和 `localstack`。`backend` 和 `frontend` 服务是您的 Node.js 应用程序，而 `mongodb` 提供数据库，`localstack` 模拟 AWS 服务（如 S3）。

   `backend` 服务依赖于 `localstack` 和 `mongodb` 服务，确保它们在启动之前正在运行。它还使用 `.env` 文件进行环境变量设置。前端服务依赖于后端并设置 API URL。`mongodb` 服务使用持久卷进行数据存储，`localstack` 配置为运行 S3 服务。此设置让您可以使用类似 AWS 的服务在本地开发和测试您的应用程序。

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

2. 修改 `backend/` 目录下的 `.env` 文件，使资源使用内部网络名称进行连接。

   > [!TIP]
   > 根据前面的 Compose 文件，应用程序将使用主机名 `localstack` 连接到 LocalStack，而 Mongo 将使用主机名 `mongodb` 连接。

   ```plaintext
   MONGODB_URI=mongodb://mongodb:27017/todos
   AWS_ACCESS_KEY_ID=test
   AWS_SECRET_ACCESS_KEY=test
   S3_BUCKET_NAME=mysamplebucket
   S3_ENDPOINT_URL=http://localstack:4566
   AWS_REGION=us-east-1
   ```

3. 停止正在运行的服务

   确保通过按终端中的“Ctrl+C”停止上一步中的 Node 前端和后端服务。此外，您需要通过在 Docker Desktop 仪表板中选择它们并选择“Delete”按钮来停止 LocalStack 和 Mongo 容器。

4. 在克隆的项目目录根目录下执行以下命令以启动应用程序堆栈：

   ```console
   $ docker compose -f compose.yml up -d --build
   ```

   稍等片刻，应用程序将启动并运行。

5. 手动创建 S3 存储桶

   AWS S3 存储桶不会由 Compose 文件预先创建。运行以下命令在 LocalStack 环境中创建一个新存储桶：

   ```console
   $ awslocal s3 mb s3://mysamplebucket
   ```

   该命令创建一个名为 `mysamplebucket` 的 S3 存储桶。

   打开 [http://localhost:5173](http://localhost:5173) 访问完整的待办事项列表应用程序，并开始将图像上传到 Amazon S3 存储桶。

   > [!TIP]
   > 为了优化性能并减少开发期间的上传时间，建议上传较小的图像文件。较大的图像可能需要更长的处理时间，并可能影响应用程序的整体响应能力。

## 回顾

本指南引导您完成了使用 LocalStack 和 Docker 设置本地开发环境的过程。您已经学习了如何在本地测试基于 AWS 的应用程序，从而降低成本并提高开发工作流程的效率。
