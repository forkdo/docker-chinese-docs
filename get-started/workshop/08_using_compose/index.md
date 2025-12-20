# 使用 Docker Compose

[Docker Compose](/manuals/compose/_index.md) 是一个帮助你定义和共享多容器应用的工具。使用 Compose，你可以创建一个 YAML 文件来定义服务，然后通过单条命令启动或停止所有服务。

使用 Compose 的最大优势是，你可以将应用栈定义在一个文件中，放在项目仓库的根目录（现在受版本控制），并轻松地让其他人参与你的项目开发。其他人只需克隆你的仓库，然后使用 Compose 启动应用即可。事实上，你可能会在 GitHub/GitLab 上看到许多项目现在正是这样做的。

## 创建 Compose 文件

在 `getting-started-app` 目录中，创建一个名为 `compose.yaml` 的文件。

```text
├── getting-started-app/
│ ├── Dockerfile
│ ├── compose.yaml
│ ├── node_modules/
│ ├── package.json
│ ├── spec/
│ ├── src/
│ └── yarn.lock
```

## 定义应用服务

在 [第 6 部分](./07_multi_container.md) 中，你使用了以下命令启动应用服务。

```console
$ docker run -dp 127.0.0.1:3000:3000 \
  -w /app -v "$(pwd):/app" \
  --network todo-app \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=secret \
  -e MYSQL_DB=todos \
  node:lts-alpine \
  sh -c "yarn install && yarn run dev"
```

现在你将在 `compose.yaml` 文件中定义此服务。

1. 在文本或代码编辑器中打开 `compose.yaml`，首先定义你想要作为应用一部分运行的第一个服务（或容器）的名称和镜像。名称会自动成为网络别名，这在定义 MySQL 服务时会很有用。

   ```yaml
   services:
     app:
       image: node:lts-alpine
   ```

2. 通常你会看到 `command` 紧邻 `image` 定义（尽管没有顺序要求）。将 `command` 添加到你的 `compose.yaml` 文件中。

   ```yaml
   services:
     app:
       image: node:lts-alpine
       command: sh -c "yarn install && yarn run dev"
   ```

3. 现在通过为服务定义 `ports` 来迁移命令中的 `-p 127.0.0.1:3000:3000` 部分。

   ```yaml
   services:
     app:
       image: node:lts-alpine
       command: sh -c "yarn install && yarn run dev"
       ports:
         - 127.0.0.1:3000:3000
   ```

4. 接下来，通过使用 `working_dir` 和 `volumes` 定义，迁移工作目录 (`-w /app`) 和卷映射 (`-v "$(pwd):/app"`)。
   Docker Compose 卷定义的一个优势是你可以使用当前目录的相对路径。

   ```yaml
   services:
     app:
       image: node:lts-alpine
       command: sh -c "yarn install && yarn run dev"
       ports:
         - 127.0.0.1:3000:3000
       working_dir: /app
       volumes:
         - ./:/app
   ```

5. 最后，你需要使用 `environment` 键迁移环境变量定义。

   ```yaml
   services:
     app:
       image: node:lts-alpine
       command: sh -c "yarn install && yarn run dev"
       ports:
         - 127.0.0.1:3000:3000
       working_dir: /app
       volumes:
         - ./:/app
       environment:
         MYSQL_HOST: mysql
         MYSQL_USER: root
         MYSQL_PASSWORD: secret
         MYSQL_DB: todos
   ```

### 定义 MySQL 服务

现在，是时候定义 MySQL 服务了。你为该容器使用的命令如下：

```console
$ docker run -d \
  --network todo-app --network-alias mysql \
  -v todo-mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=todos \
  mysql:8.0
```

1. 首先定义新服务并将其命名为 `mysql`，这样它会自动获得网络别名。同时指定要使用的镜像。

   ```yaml

   services:
     app:
       # The app service definition
     mysql:
       image: mysql:8.0
   ```

2. 接下来，定义卷映射。当你使用 `docker run` 运行容器时，Docker 会自动创建命名卷。但在使用 Compose 运行时不会发生这种情况。你需要在顶级 `volumes:` 部分定义卷，然后在服务配置中指定挂载点。仅提供卷名称时，将使用默认选项。

   ```yaml
   services:
     app:
       # The app service definition
     mysql:
       image: mysql:8.0
       volumes:
         - todo-mysql-data:/var/lib/mysql

   volumes:
     todo-mysql-data:
   ```

3. 最后，你需要指定环境变量。

   ```yaml
   services:
     app:
       # The app service definition
     mysql:
       image: mysql:8.0
       volumes:
         - todo-mysql-data:/var/lib/mysql
       environment:
         MYSQL_ROOT_PASSWORD: secret
         MYSQL_DATABASE: todos

   volumes:
     todo-mysql-data:
   ```

此时，你的完整 `compose.yaml` 应该如下所示：

```yaml
services:
  app:
    image: node:lts-alpine
    command: sh -c "yarn install && yarn run dev"
    ports:
      - 127.0.0.1:3000:3000
    working_dir: /app
    volumes:
      - ./:/app
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: secret
      MYSQL_DB: todos

  mysql:
    image: mysql:8.0
    volumes:
      - todo-mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: todos

volumes:
  todo-mysql-data:
```

## 运行应用栈

现在你有了 `compose.yaml` 文件，可以启动你的应用了。

1. 首先确保没有其他副本的容器正在运行。使用 `docker ps` 列出容器，并使用 `docker rm -f <ids>` 删除它们。

2. 使用 `docker compose up` 命令启动应用栈。添加 `-d` 标志在后台运行所有服务。

   ```console
   $ docker compose up -d
   ```

   当你运行前面的命令时，你应该看到如下输出：

   ```plaintext
   Creating network "app_default" with the default driver
   Creating volume "app_todo-mysql-data" with default driver
   Creating app_app_1   ... done
   Creating app_mysql_1 ... done
   ```

   你会注意到 Docker Compose 创建了卷以及一个网络。默认情况下，Docker Compose 会自动为应用栈创建一个专用网络（这就是为什么你没有在 Compose 文件中定义网络的原因）。

3. 使用 `docker compose logs -f` 命令查看日志。你会看到每个服务的日志交错在一个流中。这在你想观察与时间相关的问题时非常有用。`-f` 标志跟随日志输出，因此会为你提供实时输出。

   如果你已经运行了该命令，你会看到如下输出：

   ```plaintext
   mysql_1  | 2019-10-03T03:07:16.083639Z 0 [Note] mysqld: ready for connections.
   mysql_1  | Version: '8.0.31'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)
   app_1    | Connected to mysql db at host mysql
   app_1    | Listening on port 3000
   ```

   服务名称显示在每行的开头（通常带有颜色），以帮助区分消息。如果你想查看特定服务的日志，可以在日志命令末尾添加服务名称（例如，`docker compose logs -f app`）。

4. 此时，你应该能够在浏览器中打开 [http://localhost:3000](http://localhost:3000) 并看到应用正在运行。

## 在 Docker Desktop Dashboard 中查看应用栈

如果你查看 Docker Desktop Dashboard，你会看到有一个名为 **getting-started-app** 的组。这是来自 Docker Compose 的项目名称，用于将容器组合在一起。默认情况下，项目名称就是 `compose.yaml` 所在目录的名称。

如果你展开该栈，你会看到在 Compose 文件中定义的两个容器。名称也更具描述性，因为它们遵循 `<service-name>-<replica-number>` 的模式。因此，你可以很容易地快速识别哪个容器是你的应用，哪个容器是 mysql 数据库。

## 拆除所有服务

当你准备拆除所有服务时，只需运行 `docker compose down`，或在 Docker Desktop Dashboard 中点击整个应用的垃圾桶图标。容器将停止，网络将被移除。

> [!WARNING]
>
> 默认情况下，当你运行 `docker compose down` 时，Compose 文件中的命名卷不会被移除。如果你想移除卷，需要添加 `--volumes` 标志。
>
> Docker Desktop Dashboard 在删除应用栈时不会移除卷。

## 总结

在本节中，你了解了 Docker Compose 以及它如何帮助你简化定义和共享多服务应用的方式。

相关信息：
 - [Compose 概述](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)
 - [Compose CLI 参考](/reference/cli/docker/compose/_index.md)

## 下一步

接下来，你将学习一些可用于改进 Dockerfile 的最佳实践。


<a class="button not-prose" href="/get-started/workshop/09_image_best/">镜像构建最佳实践</a>

