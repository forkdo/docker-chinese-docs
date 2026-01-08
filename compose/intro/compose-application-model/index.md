# 
title: How Compose works
weight: 10
description: "Learn how Docker Compose works, from the application model to Compose files and CLI, whilst following a detailed example."
keywords: "docker compose, compose.yaml, docker compose model, compose cli, multi-container application, compose example"
aliases:
  - /compose/compose-file/02-model/
  - /compose/compose-yaml-file/
  - /compose/compose-application-model/---
title: Docker Compose 的工作原理
weight: 10
description: "了解 Docker Compose 的工作原理，从应用模型到 Compose 文件和 CLI，通过详细的示例进行学习。"---
使用 Docker Compose 时，您需要使用 YAML 配置文件（称为 [Compose 文件](#the-compose-file)）来配置应用的服务，然后通过 [Compose CLI](#cli) 从配置中创建并启动所有服务。

Compose 文件，即 `compose.yaml` 文件，遵循 [Compose 规范](/reference/compose-file/_index.md) 提供的规则来定义多容器应用。这是正式 [Compose 规范](https://github.com/compose-spec/compose-spec) 的 Docker Compose 实现。






<div
  id="compose-应用模型"
  x-data="{ open: false }"
  class="my-6 rounded-sm border border-gray-200 bg-white py-2 dark:border-gray-700 dark:bg-gray-900"
>
  <button
    class="not-prose flex w-full justify-between px-4 py-2"
    x-on:click="open = ! open"
  >
    <div class=" flex items-center gap-2">
      Compose 应用模型
    </div>
    <span :class="{ 'hidden' : !open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
    >
    <span :class="{ 'hidden' : open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
    >
  </button>
  <div x-show="open" x-collapse class="px-4">
    <p>应用的计算组件被定义为 
    
  
  <a class="link" href="/reference/compose-file/services/">服务</a>。服务是一个抽象概念，通过在平台上运行相同的容器镜像和配置，一次或多次实现。</p>
<p>服务之间通过 
    
  
  <a class="link" href="/reference/compose-file/networks/">网络</a> 进行通信。在 Compose 规范中，网络是建立连接在一起的服务容器之间 IP 路由的平台能力抽象。</p>
<p>服务将持久数据存储并共享到 
    
  
  <a class="link" href="/reference/compose-file/volumes/">卷</a> 中。规范将这种持久数据描述为具有全局选项的高级文件系统挂载。</p>
<p>某些服务需要依赖于运行时或平台的配置数据。为此，规范定义了专用的 
    
  
  <a class="link" href="/reference/compose-file/configs/">configs</a> 概念。在容器内部，configs 的行为类似于卷——它们被挂载为文件。然而，configs 在平台级别上的定义方式不同。</p>
<p>
    
  
  <a class="link" href="/reference/compose-file/secrets/">secret</a> 是配置数据的一种特殊类型，用于敏感数据，不应在不考虑安全的情况下暴露。Secrets 以挂载到容器中的文件形式提供给服务，但提供敏感数据的平台特定资源足够特殊，值得在 Compose 规范中拥有独立的概念和定义。</p>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Note
      </span>
    </div>
    <div class="admonition-content">
      <p>使用卷、configs 和 secrets，您可以在顶级进行简单声明，然后在服务级别添加更多平台特定信息。</p>
    </div>
  </blockquote>

<p>项目是在平台上部署应用规范的单个实例。项目的名称通过顶级 
    
  
  <a class="link" href="/reference/compose-file/version-and-name/"><code>name</code></a> 属性设置，用于将资源分组并与其他应用或具有不同参数的同一 Compose 指定应用的其他安装隔离。如果您在平台上创建资源，必须使用项目前缀命名资源，并设置标签 <code>com.docker.compose.project</code>。</p>
<p>Compose 提供了一种方式，让您设置自定义项目名称并覆盖此名称，这样相同的 <code>compose.yaml</code> 文件可以通过传递不同的名称在相同基础设施上部署两次，无需更改。</p>

  </div>
</div>

 

## Compose 文件

Compose 文件的默认路径是 `compose.yaml`（首选）或 `compose.yml`，放置在工作目录中。
Compose 也支持 `docker-compose.yaml` 和 `docker-compose.yml` 以保持与早期版本的向后兼容性。
如果两个文件都存在，Compose 优先选择标准的 `compose.yaml`。

您可以使用 [片段](/reference/compose-file/fragments.md) 和 [扩展](/reference/compose-file/extension.md) 来保持 Compose 文件的高效性和易维护性。

多个 Compose 文件可以 [合并](/reference/compose-file/merge.md) 在一起定义应用模型。YAML 文件的组合通过基于您设置的 Compose 文件顺序追加或覆盖 YAML 元素来实现。
简单属性和映射被最高顺序的 Compose 文件覆盖，列表通过追加合并。相对路径基于第一个 Compose 文件的父文件夹解析，当合并的补充文件托管在其他文件夹中时。
由于某些 Compose 文件元素既可以表示为单个字符串也可以表示为复杂对象，因此合并适用于展开形式。更多信息，请参阅 [使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)。

如果您想重用其他 Compose 文件，或将应用模型的部分分解为单独的 Compose 文件，您也可以使用 [`include`](/reference/compose-file/include.md)。如果您的 Compose 应用依赖于由不同团队管理的另一个应用，或者需要与他人共享，这非常有用。

## CLI

Docker CLI 让您通过 `docker compose` 命令及其子命令与 Docker Compose 应用进行交互。如果您使用 Docker Desktop，Docker Compose CLI 默认包含在内。

使用 CLI，您可以管理在 `compose.yaml` 文件中定义的多容器应用的生命周期。CLI 命令使您能够轻松地启动、停止和配置应用。

### 关键命令

启动 `compose.yaml` 文件中定义的所有服务：

```console
$ docker compose up
```

停止并移除正在运行的服务：

```console
$ docker compose down 
```

如果您想监视正在运行的容器的输出并调试问题，可以使用以下命令查看日志：

```console
$ docker compose logs
```

列出所有服务及其当前状态：

```console
$ docker compose ps
```

有关所有 Compose CLI 命令的完整列表，请参阅 [参考文档](/reference/cli/docker/compose/_index.md)。

## 示例说明

以下示例说明了上述 Compose 概念。该示例为非规范性。

考虑一个分为前端 Web 应用和后端服务的应用。

前端在运行时通过由基础设施管理的 HTTP 配置文件进行配置，提供外部域名，以及由平台安全密钥存储注入的 HTTPS 服务器证书。

后端将数据存储在持久卷中。

两个服务在隔离的后端网络上相互通信，而前端也连接到前端网络并为外部使用暴露端口 443。

![Compose 应用示例](../images/compose-application.webp)

示例应用由以下部分组成：

- 两个服务，由 Docker 镜像支持：`webapp` 和 `database`
- 一个密钥（HTTPS 证书），注入到前端
- 一个配置（HTTP），注入到前端
- 一个持久卷，附加到后端
- 两个网络

```yml
services:
  frontend:
    image: example/webapp
    ports:
      - "443:8043"
    networks:
      - front-tier
      - back-tier
    configs:
      - httpd-config
    secrets:
      - server-certificate

  backend:
    image: example/database
    volumes:
      - db-data:/etc/data
    networks:
      - back-tier

volumes:
  db-data:
    driver: flocker
    driver_opts:
      size: "10GiB"

configs:
  httpd-config:
    external: true

secrets:
  server-certificate:
    external: true

networks:
  # 这些对象的存在足以定义它们
  front-tier: {}
  back-tier: {}
```

`docker compose up` 命令启动 `frontend` 和 `backend` 服务，创建必要的网络和卷，并将配置和密钥注入前端服务。

`docker compose ps` 提供您服务当前状态的快照，便于查看哪些容器正在运行、它们的状态以及它们使用的端口：

```text
$ docker compose ps

NAME                IMAGE                COMMAND                  SERVICE             CREATED             STATUS              PORTS
example-frontend-1  example/webapp       "nginx -g 'daemon of…"   frontend            2 minutes ago       Up 2 minutes        0.0.0.0:443->8043/tcp
example-backend-1   example/database     "docker-entrypoint.s…"   backend             2 minutes ago       Up 2 minutes
```

## 下一步

- [尝试快速入门指南](/manuals/compose/gettingstarted.md)
- [探索一些示例应用](https://github.com/docker/awesome-compose)
- [熟悉 Compose 规范](/reference/compose-file/_index.md)
