# 使用 Docker Engine SDK 进行开发

Docker 提供了一个用于与 Docker 守护进程交互的 API（称为 Docker Engine API），以及用于 Go 和 Python 的 SDK。这些 SDK 让您可以高效地构建和扩展 Docker 应用程序和解决方案。如果 Go 或 Python 不适合您，您可以直接使用 Docker Engine API。

Docker Engine API 是一个 RESTful API，可以通过 `wget` 或 `curl` 等 HTTP 客户端访问，或者通过大多数现代编程语言附带的 HTTP 库访问。

## 安装 SDK

使用以下命令安装 Go 或 Python SDK。两个 SDK 可以同时安装并共存。

### Go SDK

```console
$ go get github.com/moby/moby/client
```

该客户端需要较新版本的 Go。运行 `go version` 并确保您运行的是当前受支持的 Go 版本。

更多信息，请参阅 [Go 客户端参考](https://pkg.go.dev/github.com/moby/moby/client)。

### Python SDK

- 推荐：运行 `pip install docker`。

- 如果您无法使用 `pip`：
  1.  [直接下载软件包](https://pypi.python.org/pypi/docker/)。
  2.  解压并切换到解压后的目录。
  3.  运行 `python setup.py install`。

更多信息，请参阅 [Docker Engine Python SDK 参考](https://docker-py.readthedocs.io/)。

## 查看 API 参考

您可以[查看最新版本 API 的参考](/reference/api/engine/latest/)或[选择特定版本](/reference/api/engine/#api-version-matrix)。

## 版本化的 API 和 SDK

您应该使用的 Docker Engine API 版本取决于您的 Docker 守护进程和 Docker 客户端的版本。有关详细信息，请参阅 API 文档中的[版本化 API 和 SDK](/reference/api/engine/#versioned-api-and-sdk)部分。

## SDK 和 API 快速入门

使用以下指南选择要在代码中使用的 SDK 或 API 版本：

- 如果您要启动一个新项目，请使用[最新版本](/reference/api/engine/latest/)，但要使用 API 版本协商或指定您正在使用的版本。这有助于避免意外情况。
- 如果您需要新功能，请将代码更新为至少使用支持该功能的最低版本，并优先使用您可以使用的最新版本。
- 否则，请继续使用代码已经在使用的版本。

例如，`docker run` 命令可以直接使用 Docker API 实现，也可以使用 Python 或 Go SDK 实现。








<div
  class="tabs"
  
    x-data="{ selected: 'Go' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Go' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Go'"
        
      >
        Go
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Python'"
        
      >
        Python
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'HTTP' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'HTTP'"
        
      >
        HTTP
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Go' && 'hidden'"
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
        x-data="{ code: 'cGFja2FnZSBtYWluCgppbXBvcnQgKAoJImNvbnRleHQiCgkiaW8iCgkib3MiCgoJImdpdGh1Yi5jb20vbW9ieS9tb2J5L2FwaS9wa2cvc3RkY29weSIKCSJnaXRodWIuY29tL21vYnkvbW9ieS9hcGkvdHlwZXMvY29udGFpbmVyIgoJImdpdGh1Yi5jb20vbW9ieS9tb2J5L2NsaWVudCIKKQoKZnVuYyBtYWluKCkgewoJY3R4IDo9IGNvbnRleHQuQmFja2dyb3VuZCgpCglhcGlDbGllbnQsIGVyciA6PSBjbGllbnQuTmV3KGNsaWVudC5Gcm9tRW52KQoJaWYgZXJyICE9IG5pbCB7CgkJcGFuaWMoZXJyKQoJfQoJZGVmZXIgYXBpQ2xpZW50LkNsb3NlKCkKCglyZWFkZXIsIGVyciA6PSBhcGlDbGllbnQuSW1hZ2VQdWxsKGN0eCwgImRvY2tlci5pby9saWJyYXJ5L2FscGluZSIsIGNsaWVudC5JbWFnZVB1bGxPcHRpb25ze30pCglpZiBlcnIgIT0gbmlsIHsKCQlwYW5pYyhlcnIpCgl9Cglpby5Db3B5KG9zLlN0ZG91dCwgcmVhZGVyKQoKCXJlc3AsIGVyciA6PSBhcGlDbGllbnQuQ29udGFpbmVyQ3JlYXRlKGN0eCwgY2xpZW50LkNvbnRhaW5lckNyZWF0ZU9wdGlvbnN7CgkJSW1hZ2U6ICJhbHBpbmUiLAoJCUNvbmZpZzogJmNvbnRhaW5lci5Db25maWd7CgkJCUNtZDogW11zdHJpbmd7ImVjaG8iLCAiaGVsbG8gd29ybGQifSwKCQl9LAoJfSkKCWlmIGVyciAhPSBuaWwgewoJCXBhbmljKGVycikKCX0KCglpZiBfLCBlcnIgOj0gYXBpQ2xpZW50LkNvbnRhaW5lclN0YXJ0KGN0eCwgcmVzcC5JRCwgY2xpZW50LkNvbnRhaW5lclN0YXJ0T3B0aW9uc3t9KTsgZXJyICE9IG5pbCB7CgkJcGFuaWMoZXJyKQoJfQoKCXdhaXQgOj0gYXBpQ2xpZW50LkNvbnRhaW5lcldhaXQoY3R4LCByZXNwLklELCBjbGllbnQuQ29udGFpbmVyV2FpdE9wdGlvbnN7fSkKCXNlbGVjdCB7CgljYXNlIGVyciA6PSA8LXdhaXQuRXJyb3I6CgkJaWYgZXJyICE9IG5pbCB7CgkJCXBhbmljKGVycikKCQl9CgljYXNlIDwtd2FpdC5SZXN1bHQ6Cgl9CgoJb3V0LCBlcnIgOj0gYXBpQ2xpZW50LkNvbnRhaW5lckxvZ3MoY3R4LCByZXNwLklELCBjbGllbnQuQ29udGFpbmVyTG9nc09wdGlvbnN7U2hvd1N0ZG91dDogdHJ1ZX0pCglpZiBlcnIgIT0gbmlsIHsKCQlwYW5pYyhlcnIpCgl9CgoJc3RkY29weS5TdGRDb3B5KG9zLlN0ZG91dCwgb3MuU3RkZXJyLCBvdXQpCn0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-go" data-lang="go"><span class="line"><span class="cl"><span class="kn">package</span> <span class="nx">main</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kn">import</span> <span class="p">(</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;context&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;io&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;os&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="s">&#34;github.com/moby/moby/api/pkg/stdcopy&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;github.com/moby/moby/api/types/container&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;github.com/moby/moby/client&#34;</span>
</span></span><span class="line"><span class="cl"><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kd">func</span> <span class="nf">main</span><span class="p">()</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">	<span class="nx">ctx</span> <span class="o">:=</span> <span class="nx">context</span><span class="p">.</span><span class="nf">Background</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">	<span class="nx">apiClient</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">client</span><span class="p">.</span><span class="nf">New</span><span class="p">(</span><span class="nx">client</span><span class="p">.</span><span class="nx">FromEnv</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">	<span class="k">defer</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">Close</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">reader</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ImagePull</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="s">&#34;docker.io/library/alpine&#34;</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ImagePullOptions</span><span class="p">{})</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">	<span class="nx">io</span><span class="p">.</span><span class="nf">Copy</span><span class="p">(</span><span class="nx">os</span><span class="p">.</span><span class="nx">Stdout</span><span class="p">,</span> <span class="nx">reader</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">resp</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerCreate</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerCreateOptions</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nx">Image</span><span class="p">:</span> <span class="s">&#34;alpine&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">		<span class="nx">Config</span><span class="p">:</span> <span class="o">&amp;</span><span class="nx">container</span><span class="p">.</span><span class="nx">Config</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">			<span class="nx">Cmd</span><span class="p">:</span> <span class="p">[]</span><span class="kt">string</span><span class="p">{</span><span class="s">&#34;echo&#34;</span><span class="p">,</span> <span class="s">&#34;hello world&#34;</span><span class="p">},</span>
</span></span><span class="line"><span class="cl">		<span class="p">},</span>
</span></span><span class="line"><span class="cl">	<span class="p">})</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">_</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerStart</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">resp</span><span class="p">.</span><span class="nx">ID</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerStartOptions</span><span class="p">{});</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">wait</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerWait</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">resp</span><span class="p">.</span><span class="nx">ID</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerWaitOptions</span><span class="p">{})</span>
</span></span><span class="line"><span class="cl">	<span class="k">select</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">	<span class="k">case</span> <span class="nx">err</span> <span class="o">:=</span> <span class="o">&lt;-</span><span class="nx">wait</span><span class="p">.</span><span class="nx">Error</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">		<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">			<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">		<span class="p">}</span>
</span></span><span class="line"><span class="cl">	<span class="k">case</span> <span class="o">&lt;-</span><span class="nx">wait</span><span class="p">.</span><span class="nx">Result</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">out</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerLogs</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">resp</span><span class="p">.</span><span class="nx">ID</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerLogsOptions</span><span class="p">{</span><span class="nx">ShowStdout</span><span class="p">:</span> <span class="kc">true</span><span class="p">})</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">stdcopy</span><span class="p">.</span><span class="nf">StdCopy</span><span class="p">(</span><span class="nx">os</span><span class="p">.</span><span class="nx">Stdout</span><span class="p">,</span> <span class="nx">os</span><span class="p">.</span><span class="nx">Stderr</span><span class="p">,</span> <span class="nx">out</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
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
        x-data="{ code: 'aW1wb3J0IGRvY2tlcgpjbGllbnQgPSBkb2NrZXIuZnJvbV9lbnYoKQpwcmludChjbGllbnQuY29udGFpbmVycy5ydW4oImFscGluZSIsIFsiZWNobyIsICJoZWxsbyIsICJ3b3JsZCJdKSk=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">docker</span>
</span></span><span class="line"><span class="cl"><span class="n">client</span> <span class="o">=</span> <span class="n">docker</span><span class="o">.</span><span class="n">from_env</span><span class="p">()</span>
</span></span><span class="line"><span class="cl"><span class="nb">print</span><span class="p">(</span><span class="n">client</span><span class="o">.</span><span class="n">containers</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&#34;alpine&#34;</span><span class="p">,</span> <span class="p">[</span><span class="s2">&#34;echo&#34;</span><span class="p">,</span> <span class="s2">&#34;hello&#34;</span><span class="p">,</span> <span class="s2">&#34;world&#34;</span><span class="p">]))</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'HTTP' && 'hidden'"
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
        x-data="{ code: 'JCBjdXJsIC0tdW5peC1zb2NrZXQgL3Zhci9ydW4vZG9ja2VyLnNvY2sgLUggIkNvbnRlbnQtVHlwZTogYXBwbGljYXRpb24vanNvbiIgXAogIC1kICd7IkltYWdlIjogImFscGluZSIsICJDbWQiOiBbImVjaG8iLCAiaGVsbG8gd29ybGQiXX0nIFwKICAtWCBQT1NUIGh0dHA6Ly9sb2NhbGhvc3QvdjEuNTIvY29udGFpbmVycy9jcmVhdGUKeyJJZCI6IjFjNjU5NGZhZjUiLCJXYXJuaW5ncyI6bnVsbH0KCiQgY3VybCAtLXVuaXgtc29ja2V0IC92YXIvcnVuL2RvY2tlci5zb2NrIC1YIFBPU1QgaHR0cDovL2xvY2FsaG9zdC92MS41Mi9jb250YWluZXJzLzFjNjU5NGZhZjUvc3RhcnQKCiQgY3VybCAtLXVuaXgtc29ja2V0IC92YXIvcnVuL2RvY2tlci5zb2NrIC1YIFBPU1QgaHR0cDovL2xvY2FsaG9zdC92MS41Mi9jb250YWluZXJzLzFjNjU5NGZhZjUvd2FpdAp7IlN0YXR1c0NvZGUiOjB9CgokIGN1cmwgLS11bml4LXNvY2tldCAvdmFyL3J1bi9kb2NrZXIuc29jayAiaHR0cDovL2xvY2FsaG9zdC92MS41Mi9jb250YWluZXJzLzFjNjU5NGZhZjUvbG9ncz9zdGRvdXQ9MSIKaGVsbG8gd29ybGQ=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> curl --unix-socket /var/run/docker.sock -H <span class="s2">&#34;Content-Type: application/json&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span><span class="go">  -d &#39;{&#34;Image&#34;: &#34;alpine&#34;, &#34;Cmd&#34;: [&#34;echo&#34;, &#34;hello world&#34;]}&#39; \
</span></span></span><span class="line"><span class="cl"><span class="go">  -X POST http://localhost/v1.52/containers/create
</span></span></span><span class="line"><span class="cl"><span class="go">{&#34;Id&#34;:&#34;1c6594faf5&#34;,&#34;Warnings&#34;:null}
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="gp">$</span> curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.52/containers/1c6594faf5/start
</span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="gp">$</span> curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.52/containers/1c6594faf5/wait
</span></span><span class="line"><span class="cl"><span class="go">{&#34;StatusCode&#34;:0}
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="gp">$</span> curl --unix-socket /var/run/docker.sock <span class="s2">&#34;http://localhost/v1.52/containers/1c6594faf5/logs?stdout=1&#34;</span>
</span></span><span class="line"><span class="cl"><span class="go">hello world
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>当使用 cURL 通过 Unix 套接字连接时，主机名并不重要。前面的示例使用 <code>localhost</code>，但任何主机名都可以工作。</p>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 8V12M12 16H12.01M7.8 21H16.2C17.8802 21 18.7202 21 19.362 20.673C19.9265 20.3854 20.3854 19.9265 20.673 19.362C21 18.7202 21 17.8802 21 16.2V7.8C21 6.11984 21 5.27976 20.673 4.63803C20.3854 4.07354 19.9265 3.6146 19.362 3.32698C18.7202 3 17.8802 3 16.2 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Important
      </span>
    </div>
    <div class="admonition-content">
      <p>前面的示例假设您使用的是 cURL 7.50.0 或更高版本。旧版本的 cURL 在使用套接字连接时使用了<a class="link" href="https://github.com/moby/moby/issues/17960" rel="noopener">非标准 URL 表示法</a>。</p>
<p>如果您使用的是旧版本的 cURL，请改用 <code>http:/&lt;API version&gt;/</code>，例如：<code>http:/v1.52/containers/1c6594faf5/start</code>。</p>
    </div>
  </blockquote>


      </div>
    
  </div>
</div>


更多示例，请参阅 [SDK 示例](examples.md)。

## 非官方库

有许多社区支持的其他语言库。它们未经 Docker 测试，因此如果您遇到任何问题，请向库维护者提交问题。

| 语言 | 库 |
| :------- | :-------------------------------------------------------------------------- |
| C | [libdocker](https://github.com/danielsuo/libdocker) |
| C# | [Docker.DotNet](https://github.com/ahmetalpbalkan/Docker.DotNet) |
| C++ | [lasote/docker_client](https://github.com/lasote/docker_client) |
| Clojure | [clj-docker-client](https://github.com/into-docker/clj-docker-client) |
| Clojure | [contajners](https://github.com/lispyclouds/contajners) |
| Dart | [bwu_docker](https://github.com/bwu-dart/bwu_docker) |
| Erlang | [erldocker](https://github.com/proger/erldocker) |
| Gradle | [gradle-docker-plugin](https://github.com/gesellix/gradle-docker-plugin) |
| Groovy | [docker-client](https://github.com/gesellix/docker-client) |
| Haskell | [docker-hs](https://github.com/denibertovic/docker-hs) |
| Java | [docker-client](https://github.com/spotify/docker-client) |
| Java | [docker-java](https://github.com/docker-java/docker-java) |
| Java | [docker-java-api](https://github.com/amihaiemil/docker-java-api) |
| Java | [jocker](https://github.com/ndeloof/jocker) |
| NodeJS | [dockerode](https://github.com/apocas/dockerode) |
| NodeJS | [harbor-master](https://github.com/arhea/harbor-master) |
| NodeJS | [the-moby-effect](https://github.com/leonitousconforti/the-moby-effect) |
| Perl | [Eixo::Docker](https://github.com/alambike/eixo-docker) |
| PHP | [Docker-PHP](https://github.com/docker-php/docker-php) |
| Ruby | [docker-api](https://github.com/swipely/docker-api) |
| Rust | [bollard](https://github.com/fussybeaver/bollard) |
| Rust | [docker-rust](https://github.com/abh1nav/docker-rust) |
| Rust | [shiplift](https://github.com/softprops/shiplift) |
| Scala | [tugboat](https://github.com/softprops/tugboat) |
| Scala | [reactive-docker](https://github.com/almoehi/reactive-docker) |
| Swift | [docker-client-swift](https://github.com/valeriomazzeo/docker-client-swift) |

- [使用 Docker Engine SDK 和 Docker API 的示例](https://docs.docker.com/reference/api/engine/sdk/examples/)

