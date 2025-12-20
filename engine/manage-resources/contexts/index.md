# Docker contexts

## 简介

本指南展示了如何使用上下文从单个客户端管理 Docker 守护进程。

每个上下文都包含管理守护进程上资源所需的所有信息。
`docker context` 命令使配置这些上下文并在它们之间切换变得简单。

例如，单个 Docker 客户端可能配置了两个上下文：

- 一个默认的本地上下文
- 一个远程共享上下文

一旦配置了这些上下文，你就可以使用 `docker context use <context-name>` 命令在它们之间切换。

## 前置条件

要遵循本指南中的示例，你需要：

- 一个支持顶级 `context` 命令的 Docker 客户端

运行 `docker context` 以验证你的 Docker 客户端是否支持上下文。

## 上下文的结构

上下文是多个属性的组合。这些属性包括：

- 名称和描述
- 端点配置
- TLS 信息

要列出可用的上下文，请使用 `docker context ls` 命令。

```console
$ docker context ls
NAME        DESCRIPTION                               DOCKER ENDPOINT               ERROR
default *                                             unix:///var/run/docker.sock
```

这显示了一个名为 "default" 的上下文。
它被配置为通过本地 `/var/run/docker.sock` Unix 套接字与守护进程通信。

`NAME` 列中的星号表示这是活动上下文。
这意味着所有 `docker` 命令都针对此上下文运行，
除非通过环境变量（如 `DOCKER_HOST` 和 `DOCKER_CONTEXT`）或命令行标志（如 `--context` 和 `--host`）覆盖。

使用 `docker context inspect` 进一步查看。以下示例展示了如何检查名为 `default` 的上下文。

```console
$ docker context inspect default
[
    {
        "Name": "default",
        "Metadata": {},
        "Endpoints": {
            "docker": {
                "Host": "unix:///var/run/docker.sock",
                "SkipTLSVerify": false
            }
        },
        "TLSMaterial": {},
        "Storage": {
            "MetadataPath": "\u003cIN MEMORY\u003e",
            "TLSPath": "\u003cIN MEMORY\u003e"
        }
    }
]
```

### 创建新上下文

你可以使用 `docker context create` 命令创建新上下文。

以下示例创建了一个名为 `docker-test` 的新上下文，并指定该上下文的主机端点为 TCP 套接字 `tcp://docker:2375`。

```console
$ docker context create docker-test --docker host=tcp://docker:2375
docker-test
Successfully created context "docker-test"
```

新上下文存储在 `~/.docker/contexts/` 目录下的 `meta.json` 文件中。
你创建的每个新上下文都在 `~/.docker/contexts/` 的专用子目录中拥有自己的 `meta.json`。

你可以使用 `docker context ls` 和 `docker context inspect <context-name>` 查看新上下文。

```console
$ docker context ls
NAME          DESCRIPTION                             DOCKER ENDPOINT               ERROR
default *                                             unix:///var/run/docker.sock
docker-test                                           tcp://docker:2375
```

当前上下文用星号 ("\*") 标识。

## 使用不同的上下文

你可以使用 `docker context use` 在上下文之间切换。

以下命令将 `docker` CLI 切换到使用 `docker-test` 上下文。

```console
$ docker context use docker-test
docker-test
Current context is now "docker-test"
```

通过列出所有上下文并确保星号 ("\*") 出现在 `docker-test` 上下文旁边来验证操作。

```console
$ docker context ls
NAME            DESCRIPTION                           DOCKER ENDPOINT               ERROR
default                                               unix:///var/run/docker.sock
docker-test *                                         tcp://docker:2375
```

现在 `docker` 命令将针对 `docker-test` 上下文中定义的端点。

你也可以使用 `DOCKER_CONTEXT` 环境变量设置当前上下文。
环境变量会覆盖使用 `docker context use` 设置的上下文。

使用以下适当的命令通过环境变量将上下文设置为 `docker-test`。








<div
  class="tabs"
  
    x-data="{ selected: 'PowerShell' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'PowerShell' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'PowerShell'"
        
      >
        PowerShell
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Bash' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Bash'"
        
      >
        Bash
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'PowerShell' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'PiAkZW52OkRPQ0tFUl9DT05URVhUPSdkb2NrZXItdGVzdCc=', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-ps" data-lang="ps"><span class="line"><span class="cl"><span class="p">&gt;</span> <span class="err">$env:DOCKER_CONTEXT=&#39;docker-test&#39;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Bash' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBleHBvcnQgRE9DS0VSX0NPTlRFWFQ9ZG9ja2VyLXRlc3Q=', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> <span class="nb">export</span> <span class="nv">DOCKER_CONTEXT</span><span class="o">=</span>docker-test
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


运行 `docker context ls` 以验证 `docker-test` 上下文现在是否为活动上下文。

你也可以使用全局 `--context` 标志来覆盖上下文。
以下命令使用名为 `production` 的上下文。

```console
$ docker --context production container ls
```

## 导出和导入 Docker 上下文

你可以使用 `docker context export` 和 `docker context import` 命令在不同主机之间导出和导入上下文。

`docker context export` 命令将现有上下文导出到文件。
该文件可以在任何安装了 `docker` 客户端的主机上导入。

### 导出和导入上下文

以下示例导出一个名为 `docker-test` 的现有上下文。
它将被写入名为 `docker-test.dockercontext` 的文件。

```console
$ docker context export docker-test
Written file "docker-test.dockercontext"
```

检查导出文件的内容。

```console
$ cat docker-test.dockercontext
```

在另一台主机上使用 `docker context import` 导入此文件，以创建具有相同配置的上下文。

```console
$ docker context import docker-test docker-test.dockercontext
docker-test
Successfully imported context "docker-test"
```

你可以使用 `docker context ls` 验证上下文是否已导入。

导入命令的格式为 `docker context import <context-name> <context-file>`。

## 更新上下文

你可以使用 `docker context update` 更新现有上下文中的字段。

以下示例更新现有 `docker-test` 上下文中的描述字段。

```console
$ docker context update docker-test --description "Test context"
docker-test
Successfully updated context "docker-test"
```
