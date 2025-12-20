# Docker Compose 快速入门

本教程旨在通过引导您开发一个基本的 Python Web 应用程序，介绍 Docker Compose 的基本概念。

该应用程序使用 Flask 框架，具有 Redis 中的点击计数器功能，提供了一个关于如何在 Web 开发场景中应用 Docker Compose 的实际示例。

即使您不熟悉 Python，这里演示的概念也应该易于理解。

这是一个非规范性示例，用于演示 Compose 的核心功能。

## 先决条件

请确保您已：

- [安装最新版本的 Docker Compose](/manuals/compose/install/_index.md)
- 基本了解 Docker 概念及其工作原理

## 步骤 1：设置

1. 为项目创建一个目录：

   ```console
   $ mkdir composetest
   $ cd composetest
   ```

2. 在项目目录中创建一个名为 `app.py` 的文件，并粘贴以下代码：

   ```python
   import time

   import redis
   from flask import Flask

   app = Flask(__name__)
   cache = redis.Redis(host='redis', port=6379)

   def get_hit_count():
       retries = 5
       while True:
           try:
               return cache.incr('hits')
           except redis.exceptions.ConnectionError as exc:
               if retries == 0:
                   raise exc
               retries -= 1
               time.sleep(0.5)

   @app.route('/')
   def hello():
       count = get_hit_count()
       return f'Hello World! I have been seen {count} times.\n'
    ```

   在此示例中，`redis` 是应用程序网络上 Redis 容器的主机名，并使用默认端口 `6379`。

   > [!NOTE]
   >
   > 注意 `get_hit_count` 函数的编写方式。这个基本的重试循环会在 Redis 服务不可用时多次尝试请求。这在应用程序上线启动时很有用，而且即使在应用程序生命周期内需要随时重启 Redis 服务，也能使应用程序更具弹性。在集群中，这也有助于处理节点之间暂时的连接中断。

3. 在项目目录中创建另一个名为 `requirements.txt` 的文件，并粘贴以下代码：

   ```text
   flask
   redis
   ```

4. 创建一个 `Dockerfile` 并粘贴以下代码：

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM python:3.10-alpine
   WORKDIR /code
   ENV FLASK_APP=app.py
   ENV FLASK_RUN_HOST=0.0.0.0
   RUN apk add --no-cache gcc musl-dev linux-headers
   COPY requirements.txt requirements.txt
   RUN pip install -r requirements.txt
   EXPOSE 5000
   COPY . .
   CMD ["flask", "run", "--debug"]
   ```

   




<div
  id="理解-dockerfile"
  x-data="{ open: false }"
  class="my-6 rounded-sm border border-gray-200 bg-white py-2 dark:border-gray-700 dark:bg-gray-900"
>
  <button
    class="not-prose flex w-full justify-between px-4 py-2"
    x-on:click="open = ! open"
  >
    <div class=" flex items-center gap-2">
      理解 Dockerfile
    </div>
    <span :class="{ 'hidden' : !open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
    >
    <span :class="{ 'hidden' : open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
    >
  </button>
  <div x-show="open" x-collapse class="px-4">
    <p>这告诉 Docker：</p>
<ul>
<li>从 Python 3.10 镜像开始构建镜像。</li>
<li>将工作目录设置为 <code>/code</code>。</li>
<li>设置 <code>flask</code> 命令使用的环境变量。</li>
<li>安装 gcc 及其他依赖项。</li>
<li>复制 <code>requirements.txt</code> 并安装 Python 依赖项。</li>
<li>向镜像添加元数据，描述容器正在监听端口 5000。</li>
<li>将项目中的当前目录 <code>.</code> 复制到镜像中的工作目录 <code>.</code>。</li>
<li>将容器的默认命令设置为 <code>flask run --debug</code>。</li>
</ul>
  </div>
</div>



   > [!IMPORTANT]
   >
   > 确保 `Dockerfile` 没有像 `.txt` 这样的文件扩展名。某些编辑器可能会自动附加此文件扩展名，导致运行应用程序时出错。

   有关如何编写 Dockerfile 的更多信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

## 步骤 2：在 Compose 文件中定义服务

Compose 简化了对整个应用程序堆栈的控制，使得在单个易于理解的 YAML 配置文件中管理服务、网络和卷变得容易。

在项目目录中创建一个名为 `compose.yaml` 的文件，并粘贴以下内容：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:5000"
  redis:
    image: "redis:alpine"
```

此 Compose 文件定义了两个服务：`web` 和 `redis`。

`web` 服务使用从当前目录的 `Dockerfile` 构建的镜像。
然后，它将容器和主机绑定到暴露的端口 `8000`。此示例服务使用 Flask Web 服务器的默认端口 `5000`。

`redis` 服务使用从 Docker Hub 注册表拉取的公共 [Redis](https://registry.hub.docker.com/_/redis/) 镜像。

有关 `compose.yaml` 文件的更多信息，请参阅 [Compose 的工作原理](compose-application-model.md)。

## 步骤 3：使用 Compose 构建并运行您的应用

只需一个命令，您就可以从配置文件中创建并启动所有服务。

1. 从项目目录运行 `docker compose up` 启动应用程序。

   ```console
   $ docker compose up

   Creating network "composetest_default" with the default driver
   Creating composetest_web_1 ...
   Creating composetest_redis_1 ...
   Creating composetest_web_1
   Creating composetest_redis_1 ... done
   Attaching to composetest_web_1, composetest_redis_1
   web_1    |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
   redis_1  | 1:C 17 Aug 22:11:10.480 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
   redis_1  | 1:C 17 Aug 22:11:10.480 # Redis version=4.0.1, bits=64, commit=00000000, modified=0, pid=1, just started
   redis_1  | 1:C 17 Aug 22:11:10.480 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
   web_1    |  * Restarting with stat
   redis_1  | 1:M 17 Aug 22:11:10.483 * Running mode=standalone, port=6379.
   redis_1  | 1:M 17 Aug 22:11:10.483 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
   web_1    |  * Debugger is active!
   redis_1  | 1:M 17 Aug 22:11:10.483 # Server initialized
   redis_1  | 1:M 17 Aug 22:11:10.483 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
   web_1    |  * Debugger PIN: 330-787-903
   redis_1  | 1:M 17 Aug 22:11:10.483 * Ready to accept connections
   ```

   Compose 拉取 Redis 镜像，为您的代码构建镜像，并启动您定义的服务。在本例中，代码在构建时被静态复制到镜像中。

2. 在浏览器中输入 `http://localhost:8000/` 以查看正在运行的应用程序。

   如果无法解析，您也可以尝试 `http://127.0.0.1:8000`。

   您应该会在浏览器中看到一条消息：

   ```text
   Hello World! I have been seen 1 times.
   ```

   ![浏览器中的 hello world](images/quick-hello-world-1.png)

3. 刷新页面。

   数字应该会递增。

   ```text
   Hello World! I have been seen 2 times.
   ```

   ![浏览器中的 hello world](images/quick-hello-world-2.png)

4. 切换到另一个终端窗口，输入 `docker image ls` 列出本地镜像。

   此时列出镜像应返回 `redis` 和 `web`。

   ```console
   $ docker image ls

   REPOSITORY        TAG           IMAGE ID      CREATED        SIZE
   composetest_web   latest        e2c21aa48cc1  4 minutes ago  93.8MB
   python            3.4-alpine    84e6077c7ab6  7 days ago     82.5MB
   redis             alpine        9d8fa9aa0e5b  3 weeks ago    27.5MB
   ```

   您可以使用 `docker inspect <tag or id>` 检查镜像。

5. 停止应用程序，可以通过在第二个终端的项目目录中运行 `docker compose down`，或者在启动应用程序的原始终端中按 `CTRL+C`。

## 步骤 4：编辑 Compose 文件以使用 Compose Watch

编辑项目目录中的 `compose.yaml` 文件以使用 `watch`，这样您就可以预览正在运行的 Compose 服务，这些服务会在您编辑并保存代码时自动更新：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:5000"
    develop:
      watch:
        - action: sync
          path: .
          target: /code
  redis:
    image: "redis:alpine"
```

每当文件发生更改时，Compose 会将文件同步到容器内 `/code` 下的相应位置。复制完成后，捆绑器会更新正在运行的应用程序，无需重启。

有关 Compose Watch 工作原理的更多信息，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。或者，有关其他选项，请参阅[管理容器中的数据](/manuals/engine/storage/volumes.md)。

> [!NOTE]
>
   > 要使此示例正常工作，`--debug` 选项已添加到 `Dockerfile` 中。Flask 中的 `--debug` 选项启用自动代码重新加载，使得无需重启或重建容器即可处理后端 API。
> 更改 `.py` 文件后，后续 API 调用将使用新代码，但在此小示例中，浏览器 UI 不会自动刷新。大多数前端开发服务器都包含原生实时重新加载支持，可与 Compose 配合使用。

## 步骤 5：使用 Compose 重新构建并运行应用程序

从项目目录输入 `docker compose watch` 或 `docker compose up --watch` 以构建并启动应用程序，并启动文件监视模式。

```console
$ docker compose watch
[+] Running 2/2
 ✔ Container docs-redis-1 Created                                                                                                                                                                                                        0.0s
 ✔ Container docs-web-1    Recreated                                                                                                                                                                                                      0.1s
Attaching to redis-1, web-1
         ⦿ watch enabled
...
```

再次在 Web 浏览器中检查 `Hello World` 消息，并刷新以查看计数递增。

## 步骤 6：更新应用程序

要查看 Compose Watch 的实际效果：

1. 更改 `app.py` 中的问候语并保存。例如，将 `Hello World!` 消息更改为 `Hello from Docker!`：

   ```python
   return f'Hello from Docker! I have been seen {count} times.\n'
   ```

2. 在浏览器中刷新应用程序。问候语应已更新，且计数器应仍在递增。

   ![浏览器中的 hello world](images/quick-hello-world-3.png)

3. 完成后，运行 `docker compose down`。

## 步骤 7：拆分您的服务

使用多个 Compose 文件可以为不同的环境或工作流自定义 Compose 应用程序。这对于可能使用数十个容器、所有权分布在多个团队中的大型应用程序非常有用。

1. 在项目文件夹中，创建一个名为 `infra.yaml` 的新 Compose 文件。

2. 将 Redis 服务从 `compose.yaml` 文件剪切并粘贴到新的 `infra.yaml` 文件中。确保在文件顶部添加 `services` 顶级属性。您的 `infra.yaml` 文件现在应如下所示：

   ```yaml
   services:
     redis:
       image: "redis:alpine"
   ```

3. 在 `compose.yaml` 文件中，添加 `include` 顶级属性以及 `infra.yaml` 文件的路径。

   ```yaml
   include:
      - infra.yaml
   services:
     web:
       build: .
       ports:
         - "8000:5000"
       develop:
         watch:
           - action: sync
             path: .
             target: /code
   ```

4. 运行 `docker compose up` 以使用更新的 Compose 文件构建应用程序并运行它。您应该会在浏览器中看到 `Hello world` 消息。

这是一个简化的示例，但它演示了 `include` 的基本原理以及它如何使将复杂应用程序模块化为子 Compose 文件变得更加容易。有关 `include` 和使用多个 Compose 文件的更多信息，请参阅[使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)。

## 步骤 8：尝试其他命令

- 如果您想在后台运行服务，可以将 `-d` 标志（表示“分离”模式）传递给 `docker compose up`，并使用 `docker compose ps` 查看当前正在运行的内容：

   ```console
   $ docker compose up -d

   Starting composetest_redis_1...
   Starting composetest_web_1...

   $ docker compose ps

          Name                      Command               State           Ports         
   -------------------------------------------------------------------------------------
   composetest_redis_1   docker-entrypoint.sh redis ...   Up      6379/tcp              
   composetest_web_1     flask run                        Up      0.0.0.0:8000->5000/tcp
   ```

- 运行 `docker compose --help` 以查看其他可用命令。

- 如果您使用 `docker compose up -d` 启动了 Compose，完成后请停止服务：

   ```console
   $ docker compose stop
   ```

- 您可以使用 `docker compose down` 命令将所有内容降级，完全删除容器。

## 下一步

- 尝试 [Compose 示例应用](https://github.com/docker/awesome-compose)
- [浏览完整的 Compose 命令列表](/reference/cli/docker/compose.md)
- [浏览 Compose 文件参考](/reference/compose-file/_index.md)
- [查看 LinkedIn Learning 上的 Learning Docker Compose 视频](https://www.linkedin.com/learning/learning-docker-compose/)
