# Compose 的工作原理

使用 Docker Compose 时，您需要使用一个 YAML 配置文件（即 [Compose 文件](#the-compose-file)）来配置应用程序的服务，然后使用 [Compose CLI](#cli) 根据配置创建并启动所有服务。

Compose 文件（即 `compose.yaml` 文件）遵循 [Compose 规范](/reference/compose-file/_index.md) 中关于如何定义多容器应用的规则。这是 Docker Compose 对正式 [Compose 规范](https://github.com/compose-spec/compose-spec) 的实现。






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
    <p>应用程序的计算组件被定义为 
    
  
  <a class="link" href="/reference/compose-file/services/">服务</a>。服务是一个抽象概念，在平台上通过运行相同的容器镜像和配置（一次或多次）来实现。</p>
<p>服务之间通过 
    
  
  <a class="link" href="/reference/compose-file/networks/">网络</a> 进行通信。在 Compose 规范中，网络是一种平台能力抽象，用于在连接在一起的服务内的容器之间建立 IP 路由。</p>
<p>服务将持久数据存储并共享到 
    
  
  <a class="link" href="/reference/compose-file/volumes/">卷</a> 中。该规范将此类持久数据描述为具有全局选项的高级文件系统挂载。</p>
<p>某些服务需要依赖于运行时或平台的配置数据。为此，规范定义了一个专门的 
    
  
  <a class="link" href="/reference/compose-file/configs/">配置 (configs)</a> 概念。在容器内部，配置的行为类似于卷——它们作为文件被挂载。但是，配置在平台级别的定义方式不同。</p>
<p>
    
  
  <a class="link" href="/reference/compose-file/secrets/">密钥 (secret)</a> 是配置数据的一种特定类型，用于处理敏感数据，这些数据不应在没有安全考虑的情况下暴露。密钥作为文件挂载到其容器中提供给服务使用，但提供敏感数据的特定于平台的资源足够独特，值得在 Compose 规范中拥有一个独立的概念和定义。</p>


  

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
      <p>使用卷、配置和密钥时，您可以在顶层进行简单声明，然后在服务级别添加更多特定于平台的信息。</p>
    </div>
  </blockquote>

<p>项目是在平台上对应用规范进行的单独部署。项目的名称（通过顶层 
    
  
  <a class="link" href="/reference/compose-file/version-and-name/"><code>name</code></a> 属性设置）用于将资源分组在一起，并将其与其他应用程序或具有不同参数的同一 Compose 规范应用程序的其他安装隔离开来。如果您在平台上创建资源，则必须在资源名称前加上项目名称前缀，并设置标签 <code>com.docker.compose.project</code>。</p>
<p>Compose 提供了一种设置自定义项目名称并覆盖此名称的方法，因此同一个 <code>compose.yaml</code> 文件可以通过传递不同的名称在相同基础设施上部署两次，而无需更改。</p>

  </div>
</div>

 

## Compose 文件

Compose 文件的默认路径是工作目录中的 `compose.yaml`（推荐）或 `compose.yml`。
Compose 还支持 `docker-compose.yaml` 和 `docker-compose.yml`，以实现与早期版本的向后兼容。
如果两个文件都存在，Compose 优先使用规范的 `compose.yaml`。

您可以使用 [片段](/reference/compose-file/fragments.md) 和 [扩展](/reference/compose-file/extension.md) 来保持 Compose 文件的高效和易于维护。

可以 [合并](/reference/compose-file/merge.md) 多个 Compose 文件来定义应用模型。YAML 文件的组合是通过根据您设置的 Compose 文件顺序追加或覆盖 YAML 元素来实现的。
简单属性和映射会被顺序最高的 Compose 文件覆盖，列表则通过追加进行合并。相对路径是基于第一个 Compose 文件的父文件夹解析的，无论要合并的补充文件托管在哪个文件夹中。由于某些 Compose 文件元素既可以表示为单个字符串，也可以表示为复杂对象，因此合并适用于扩展形式。更多信息，请参阅 [使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)。

如果您想重用其他 Compose 文件，或将应用模型的部分内容分解到单独的 Compose 文件中，也可以使用 [`include`](/reference/compose-file/include.md)。如果您的 Compose 应用程序依赖于另一个由不同团队管理的应用程序，或者需要与他人共享，这将非常有用。

## CLI

Docker CLI 允许您通过 `docker compose` 命令及其子命令与您的 Docker Compose 应用程序进行交互。如果您使用的是 Docker Desktop，则默认包含 Docker Compose CLI。

使用 CLI，您可以管理在 `compose.yaml` 文件中定义的多容器应用程序的生命周期。CLI 命令使您可以轻松启动、停止和配置您的应用程序。

### 关键命令 

要启动 `compose.yaml` 文件中定义的所有服务：

```console
$ docker compose up
```

要停止并移除正在运行的服务：

```console
$ docker compose down 
```

如果您想监控正在运行的容器的输出并调试问题，可以使用以下命令查看日志：

```console
$ docker compose logs
```

要列出所有服务及其当前状态：

```console
$ docker compose ps
```

有关所有 Compose CLI 命令的完整列表，请参阅 [参考文档](/reference/cli/docker/compose/_index.md)。

## 示例说明

以下示例说明了上述概述的 Compose 概念。该示例仅供参考。

考虑一个拆分为前端 Web 应用程序和后端服务的应用程序。

前端在运行时通过基础设施管理的 HTTP 配置文件进行配置，该文件提供外部域名，以及由平台的安全密钥存储注入的 HTTPS 服务器证书。

后端将数据存储在持久卷中。

两个服务在隔离的后端网络上相互通信，而前端还连接到前端网络并暴露端口 443 以供外部使用。

![Compose 应用示例](../images/compose-application.webp)

示例应用程序由以下部分组成：

- 两个由 Docker 镜像支持的服务：`webapp` 和 `database`
- 一个密钥（HTTPS 证书），注入到前端
- 一个配置（HTTP），注入到前端
- 一个持久卷，挂载到后端
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

`docker compose up` 命令启动 `frontend` 和 `backend` 服务，创建必要的网络和卷，并将配置和密钥注入到前端服务。

`docker compose ps` 提供服务当前状态的快照，可以轻松查看哪些容器正在运行、它们的状态以及它们使用的端口：

```text
$ docker compose ps

NAME                IMAGE                COMMAND                  SERVICE             CREATED             STATUS              PORTS
example-frontend-1  example/webapp       "nginx -g 'daemon of…"   frontend            2 minutes ago       Up 2 minutes        0.0.0.0:443->8043/tcp
example-backend-1   example/database     "docker-entrypoint.s…"   backend             2 minutes ago       Up 2 minutes
```

## 下一步

- [尝试快速入门指南](/manuals/compose/gettingstarted.md)
- [探索一些示例应用程序](/manuals/compose/support-and-feedback/samples-for-compose.md)
- [熟悉 Compose 规范](/reference/compose-file/_index.md)
