# 容器化 Python 应用程序

## 先决条件

- 已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 已安装 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但你可以使用任何客户端。

## 概览

本节将引导你完成容器化和运行 Python 应用程序的过程。

## 获取示例应用程序

示例应用程序使用了流行的 [FastAPI](https://fastapi.tiangolo.com) 框架。

克隆示例应用程序以配合本指南使用。打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/estebanx64/python-docker-example && cd python-docker-example
```

## 初始化 Docker 资源

现在你已经有了一个应用程序，可以创建必要的 Docker 资源来容器化你的应用程序。你可以使用 Docker Desktop 内置的 Docker Init 功能来帮助简化这个过程，也可以手动创建这些资源。








<div
  class="tabs"
  
    x-data="{ selected: '%E4%BD%BF%E7%94%A8-Docker-Init' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8-Docker-Init' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8-Docker-Init'"
        
      >
        使用 Docker Init
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8%E5%AE%98%E6%96%B9-Docker-%E9%95%9C%E5%83%8F' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8%E5%AE%98%E6%96%B9-Docker-%E9%95%9C%E5%83%8F'"
        
      >
        使用官方 Docker 镜像
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8-Docker-%E5%8A%A0%E5%9B%BA%E9%95%9C%E5%83%8F' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8-Docker-%E5%8A%A0%E5%9B%BA%E9%95%9C%E5%83%8F'"
        
      >
        使用 Docker 加固镜像
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-Docker-Init' && 'hidden'"
      >
        <p>在 <code>python-docker-example</code> 目录中，运行 <code>docker init</code> 命令。<code>docker init</code> 会提供一些默认配置，但你需要回答一些关于你的应用程序的问题。例如，这个应用程序使用 FastAPI 来运行。参考以下示例来回答 <code>docker init</code> 的提示，并在你的提示中使用相同的答案。</p>
<p>在编辑 Dockerfile 之前，你需要选择一个基础镜像。你可以使用 <a class="link" href="https://hub.docker.com/_/python" rel="noopener">Python Docker 官方镜像</a>，或者 <a class="link" href="https://hub.docker.com/hardened-images/catalog/dhi/python" rel="noopener">Docker 加固镜像 (DHI)</a>。</p>
<p>Docker 加固镜像 (DHIs) 是由 Docker 维护的最小、安全且生产就绪的基础镜像。它们有助于减少漏洞并简化合规性。更多详情，请参阅 
  <a class="link" href="/dhi/">Docker 加固镜像</a>。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgaW5pdArmrKLov47kvb/nlKggRG9ja2VyIEluaXQgQ0xJ77yBCgrmraTlt6XlhbflsIblvJXlr7zkvaDliJvlu7rku6XkuIvmlofku7bvvIzlubbkuLrkvaDnmoTpobnnm67orr7nva7lkIjnkIbnmoTpu5jorqTlgLzvvJoKICAtIC5kb2NrZXJpZ25vcmUKICAtIERvY2tlcmZpbGUKICAtIGNvbXBvc2UueWFtbAogIC0gUkVBRE1FLkRvY2tlci5tZAoK6K6p5oiR5Lus5byA5aeL5ZCn77yBCgo/IOS9oOeahOmhueebruS9v&#43;eUqOS7gOS5iOW6lOeUqOeoi&#43;W6j&#43;W5s&#43;WPsO&#43;8n1B5dGhvbgo/IOS9oOaDs&#43;S9v&#43;eUqOWTquS4queJiOacrOeahCBQeXRob27vvJ8zLjEyCj8g5L2g55qE5bqU55So56iL5bqP6KaB55uR5ZCs5ZOq5Liq56uv5Y&#43;j77yfODAwMAo/IOi/kOihjOS9oOeahOW6lOeUqOeoi&#43;W6j&#43;eahOWRveS7pOaYr&#43;S7gOS5iO&#43;8n3B5dGhvbjMgLW0gdXZpY29ybiBhcHA6YXBwIC0taG9zdD0wLjAuMC4wIC0tcG9ydD04MDAw', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker init
</span></span><span class="line"><span class="cl"><span class="go">欢迎使用 Docker Init CLI！
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="go">此工具将引导你创建以下文件，并为你的项目设置合理的默认值：
</span></span></span><span class="line"><span class="cl"><span class="go">  - .dockerignore
</span></span></span><span class="line"><span class="cl"><span class="go">  - Dockerfile
</span></span></span><span class="line"><span class="cl"><span class="go">  - compose.yaml
</span></span></span><span class="line"><span class="cl"><span class="go">  - README.Docker.md
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="go">让我们开始吧！
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="go">? 你的项目使用什么应用程序平台？Python
</span></span></span><span class="line"><span class="cl"><span class="go">? 你想使用哪个版本的 Python？3.12
</span></span></span><span class="line"><span class="cl"><span class="go">? 你的应用程序要监听哪个端口？8000
</span></span></span><span class="line"><span class="cl"><span class="go">? 运行你的应用程序的命令是什么？python3 -m uvicorn app:app --host=0.0.0.0 --port=8000
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>创建一个名为 <code>.gitignore</code> 的文件，内容如下：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
    <div class="flex w-full items-center gap-2">
      <div
        class="flex items-center gap-2.5 rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800"
      >
        <div class="font-normal text-gray-500 dark:text-gray-200">
          .gitignore
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDlrZfoioLnvJbor5EgLyDkvJjljJYgLyBETEwg5paH5Lu2Cl9fcHljYWNoZV9fLwoqLnB5W2NvZF0KKiRweS5jbGFzcwoKIyBDIOaJqeWxlQoqLnNvCgojIOWIhuWPkSAvIOaJk&#43;WMhQouUHl0aG9uCmJ1aWxkLwpkZXZlbG9wLWVnZ3MvCmRpc3QvCmRvd25sb2Fkcy8KZWdncy8KLmVnZ3MvCmxpYi8KbGliNjQvCnBhcnRzLwpzZGlzdC8KdmFyLwp3aGVlbHMvCnNoYXJlL3B5dGhvbi13aGVlbHMvCiouZWdnLWluZm8vCi5pbnN0YWxsZWQuY2ZnCiouZWdnCk1BTklGRVNUCgojIOWNleWFg&#43;a1i&#43;ivlSAvIOimhueblueOh&#43;aKpeWRigpodG1sY292LwoudG94Lwoubm94LwouY292ZXJhZ2UKLmNvdmVyYWdlLioKLmNhY2hlCm5vc2V0ZXN0cy54bWwKY292ZXJhZ2UueG1sCiouY292ZXIKKi5weSxjb3ZlcgouaHlwb3RoZXNpcy8KLnB5dGVzdF9jYWNoZS8KY292ZXIvCgojIFBFUCA1ODLvvJvkvovlpoIgZ2l0aHViLmNvbS9EYXZpZC1PQ29ubm9yL3B5ZmxvdyDlkowgZ2l0aHViLmNvbS9wZG0tcHJvamVjdC9wZG0g5L2/55SoCl9fcHlwYWNrYWdlc19fLwoKIyDnjq/looMKLmVudgoudmVudgplbnYvCnZlbnYvCkVOVi8KZW52LmJhay8KdmVudi5iYWsv', copying: false }"
        class="
          -top-10
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
      
        <div
          x-data="{ collapse: true }"
          class="relative overflow-clip"
          x-init="$watch('collapse', value => $refs.root.scrollIntoView({ behavior: 'smooth'}))"
        >
          <div
            x-show="collapse"
            class="absolute z-10 flex h-32 w-full flex-col-reverse items-center overflow-clip pb-4"
          >
            <button @click="collapse = false" class="chip">
              <span>Show more</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
              >
            </button>
          </div>
          <div :class="{ 'h-32': collapse }">
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl"># 字节编译 / 优化 / DLL 文件
</span></span><span class="line"><span class="cl">__pycache__/
</span></span><span class="line"><span class="cl">*.py[cod]
</span></span><span class="line"><span class="cl">*$py.class
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># C 扩展
</span></span><span class="line"><span class="cl">*.so
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># 分发 / 打包
</span></span><span class="line"><span class="cl">.Python
</span></span><span class="line"><span class="cl">build/
</span></span><span class="line"><span class="cl">develop-eggs/
</span></span><span class="line"><span class="cl">dist/
</span></span><span class="line"><span class="cl">downloads/
</span></span><span class="line"><span class="cl">eggs/
</span></span><span class="line"><span class="cl">.eggs/
</span></span><span class="line"><span class="cl">lib/
</span></span><span class="line"><span class="cl">lib64/
</span></span><span class="line"><span class="cl">parts/
</span></span><span class="line"><span class="cl">sdist/
</span></span><span class="line"><span class="cl">var/
</span></span><span class="line"><span class="cl">wheels/
</span></span><span class="line"><span class="cl">share/python-wheels/
</span></span><span class="line"><span class="cl">*.egg-info/
</span></span><span class="line"><span class="cl">.installed.cfg
</span></span><span class="line"><span class="cl">*.egg
</span></span><span class="line"><span class="cl">MANIFEST
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># 单元测试 / 覆盖率报告
</span></span><span class="line"><span class="cl">htmlcov/
</span></span><span class="line"><span class="cl">.tox/
</span></span><span class="line"><span class="cl">.nox/
</span></span><span class="line"><span class="cl">.coverage
</span></span><span class="line"><span class="cl">.coverage.*
</span></span><span class="line"><span class="cl">.cache
</span></span><span class="line"><span class="cl">nosetests.xml
</span></span><span class="line"><span class="cl">coverage.xml
</span></span><span class="line"><span class="cl">*.cover
</span></span><span class="line"><span class="cl">*.py,cover
</span></span><span class="line"><span class="cl">.hypothesis/
</span></span><span class="line"><span class="cl">.pytest_cache/
</span></span><span class="line"><span class="cl">cover/
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># PEP 582；例如 github.com/David-OConnor/pyflow 和 github.com/pdm-project/pdm 使用
</span></span><span class="line"><span class="cl">__pypackages__/
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># 环境
</span></span><span class="line"><span class="cl">.env
</span></span><span class="line"><span class="cl">.venv
</span></span><span class="line"><span class="cl">env/
</span></span><span class="line"><span class="cl">venv/
</span></span><span class="line"><span class="cl">ENV/
</span></span><span class="line"><span class="cl">env.bak/
</span></span><span class="line"><span class="cl">venv.bak/</span></span></code></pre></div>
            <button
              @click="collapse = true"
              x-show="!collapse"
              class="chip mx-auto mt-4 flex items-center  text-sm"
            >
              <span>Hide</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
              >
            </button>
          </div>
        </div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8%E5%AE%98%E6%96%B9-Docker-%E9%95%9C%E5%83%8F' && 'hidden'"
      >
        <p>如果你没有安装 Docker Desktop 或更喜欢手动创建资源，你可以在项目目录中创建以下文件。</p>
<p>创建一个名为 <code>Dockerfile</code> 的文件，内容如下：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
    <div class="flex w-full items-center gap-2">
      <div
        class="flex items-center gap-2.5 rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800"
      >
        <div class="font-normal text-gray-500 dark:text-gray-200">
          Dockerfile
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQoKIyDmraTmlofku7bkuK3mj5Dkvpvkuobms6jph4rku6XluK7liqnkvaDlhaXpl6jjgIIKIyDlpoLmnpzkvaDpnIDopoHmm7TlpJrluK7liqnvvIzor7forr/pl64gRG9ja2VyZmlsZSDlj4LogIPmjIfljZfvvJoKIyBodHRwczovL2RvY3MuZG9ja2VyLmNvbS9nby9kb2NrZXJmaWxlLXJlZmVyZW5jZS8KCiMg5oOz5biu5Yqp5oiR5Lus5pS56L&#43;b5q2k5qih5p2/77yf6K&#43;35Zyo5q2k5aSE5YiG5Lqr5L2g55qE5Y&#43;N6aaI77yaaHR0cHM6Ly9mb3Jtcy5nbGUveWJxOUtydDhqdEJMM2lDazcKCiMg5q2kIERvY2tlcmZpbGUg5L2/55SoIERvY2tlciDliqDlm7rplZzlg48gKERISSkg5Lul5aKe5by65a6J5YWo5oCn44CCCiMg5pu05aSa5L&#43;h5oGv77yM6K&#43;35Y&#43;C6ZiFIGh0dHBzOi8vZG9jcy5kb2NrZXIuY29tL2RoaS8KQVJHIFBZVEhPTl9WRVJTSU9OPTMuMTIKRlJPTSBweXRob246JHtQWVRIT05fVkVSU0lPTn0tc2xpbQoKIyDpmLvmraIgUHl0aG9uIOWGmeWFpSBweWMg5paH5Lu244CCCkVOViBQWVRIT05ET05UV1JJVEVCWVRFQ09ERT0xCgojIOmYsuatoiBQeXRob24g57yT5YayIHN0ZG91dCDlkowgc3RkZXJy77yM5Lul6YG/5YWN55Sx5LqO57yT5Yay6ICM5a&#43;86Ie05bqU55So56iL5bqP5bSp5rqD5pe25rKh5pyJ5Y&#43;R5Ye65Lu75L2V5pel5b&#43;X55qE5oOF5Ya144CCCkVOViBQWVRIT05VTkJVRkZFUkVEPTEKCldPUktESVIgL2FwcAoKIyDliJvlu7rkuIDkuKrpnZ7nibnmnYPnlKjmiLfvvIzlupTnlKjnqIvluo/lsIbku6XmraTnlKjmiLfouqvku73ov5DooYzjgIIKIyDlj4Lop4EgaHR0cHM6Ly9kb2NzLmRvY2tlci5jb20vZ28vZG9ja2VyZmlsZS11c2VyLWJlc3QtcHJhY3RpY2VzLwpBUkcgVUlEPTEwMDAxClJVTiBhZGR1c2VyIFwKICAgIC0tZGlzYWJsZWQtcGFzc3dvcmQgXAogICAgLS1nZWNvcyAiIiBcCiAgICAtLWhvbWUgIi9ub25leGlzdGVudCIgXAogICAgLS1zaGVsbCAiL3NiaW4vbm9sb2dpbiIgXAogICAgLS1uby1jcmVhdGUtaG9tZSBcCiAgICAtLXVpZCAiJHtVSUR9IiBcCiAgICBhcHB1c2VyCgojIOWwhuS4i&#43;i9veS&#43;nei1lumhueS9nOS4uuWNleeLrOeahOatpemqpO&#43;8jOS7peWIqeeUqCBEb2NrZXIg55qE57yT5a2Y44CCCiMg5Yip55So57yT5a2Y5oyC6L295YiwIC9yb290Ly5jYWNoZS9waXAg5Lul5Yqg6YCf5ZCO57ut5p6E5bu644CCCiMg5Yip55So57uR5a6a5oyC6L295YiwIHJlcXVpcmVtZW50cy50eHQg5Lul6YG/5YWN5b&#43;F6aG75bCG5a6D5Lus5aSN5Yi25Yiw5q2k5bGC5Lit44CCClJVTiAtLW1vdW50PXR5cGU9Y2FjaGUsdGFyZ2V0PS9yb290Ly5jYWNoZS9waXAgXAogICAgLS1tb3VudD10eXBlPWJpbmQsc291cmNlPXJlcXVpcmVtZW50cy50eHQsdGFyZ2V0PXJlcXVpcmVtZW50cy50eHQgXAogICAgcHl0aG9uIC1tIHBpcCBpbnN0YWxsIC1yIHJlcXVpcmVtZW50cy50eHQKCiMg5YiH5o2i5Yiw6Z2e54m55p2D55So5oi35Lul6L&#43;Q6KGM5bqU55So56iL5bqP44CCClVTRVIgYXBwdXNlcgoKIyDlsIbmupDku6PnoIHlpI3liLbliLDlrrnlmajkuK3jgIIKQ09QWSAuIC4KCiMg5pq06Zyy5bqU55So56iL5bqP55uR5ZCs55qE56uv5Y&#43;j44CCCkVYUE9TRSA4MDAwCgojIOi/kOihjOW6lOeUqOeoi&#43;W6j&#43;OAggpDTUQgWyJweXRob24zIiwgIi1tIiwgInV2aWNvcm4iLCAiYXBwOmFwcCIsICItLWhvc3Q9MC4wLjAuMCIsICItLXBvcnQ9ODAwMCJd', copying: false }"
        class="
          -top-10
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
      
        <div
          x-data="{ collapse: true }"
          class="relative overflow-clip"
          x-init="$watch('collapse', value => $refs.root.scrollIntoView({ behavior: 'smooth'}))"
        >
          <div
            x-show="collapse"
            class="absolute z-10 flex h-32 w-full flex-col-reverse items-center overflow-clip pb-4"
          >
            <button @click="collapse = false" class="chip">
              <span>Show more</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
              >
            </button>
          </div>
          <div :class="{ 'h-32': collapse }">
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 此文件中提供了注释以帮助你入门。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 如果你需要更多帮助，请访问 Dockerfile 参考指南：</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># https://docs.docker.com/go/dockerfile-reference/</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 想帮助我们改进此模板？请在此处分享你的反馈：https://forms.gle/ybq9Krt8jtBL3iCk7</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 此 Dockerfile 使用 Docker 加固镜像 (DHI) 以增强安全性。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 更多信息，请参阅 https://docs.docker.com/dhi/</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ARG</span> <span class="nv">PYTHON_VERSION</span><span class="o">=</span><span class="m">3</span>.12<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> python:${PYTHON_VERSION}-slim</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 阻止 Python 写入 pyc 文件。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">PYTHONDONTWRITEBYTECODE</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c"># 防止 Python 缓冲 stdout 和 stderr，以避免由于缓冲而导致应用程序崩溃时没有发出任何日志的情况。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">PYTHONUNBUFFERED</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="s"> /app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 创建一个非特权用户，应用程序将以此用户身份运行。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 参见 https://docs.docker.com/go/dockerfile-user-best-practices/</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ARG</span> <span class="nv">UID</span><span class="o">=</span><span class="m">10001</span>
</span></span><span class="line"><span class="cl"><span class="k">RUN</span> adduser <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --disabled-password <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --gecos <span class="s2">&#34;&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --home <span class="s2">&#34;/nonexistent&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --shell <span class="s2">&#34;/sbin/nologin&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --no-create-home <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --uid <span class="s2">&#34;</span><span class="si">${</span><span class="nv">UID</span><span class="si">}</span><span class="s2">&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    appuser<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 将下载依赖项作为单独的步骤，以利用 Docker 的缓存。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 利用缓存挂载到 /root/.cache/pip 以加速后续构建。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 利用绑定挂载到 requirements.txt 以避免必须将它们复制到此层中。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.cache/pip <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>bind,source<span class="o">=</span>requirements.txt,target<span class="o">=</span>requirements.txt <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    python -m pip install -r requirements.txt<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 切换到非特权用户以运行应用程序。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">USER</span><span class="s"> appuser</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 将源代码复制到容器中。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 暴露应用程序监听的端口。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">EXPOSE</span><span class="s"> 8000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 运行应用程序。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;python3&#34;</span><span class="p">,</span> <span class="s2">&#34;-m&#34;</span><span class="p">,</span> <span class="s2">&#34;uvicorn&#34;</span><span class="p">,</span> <span class="s2">&#34;app:app&#34;</span><span class="p">,</span> <span class="s2">&#34;--host=0.0.0.0&#34;</span><span class="p">,</span> <span class="s2">&#34;--port=8000&#34;</span><span class="p">]</span></span></span></code></pre></div>
            <button
              @click="collapse = true"
              x-show="!collapse"
              class="chip mx-auto mt-4 flex items-center  text-sm"
            >
              <span>Hide</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
              >
            </button>
          </div>
        </div>
      
    </div>
  </div>
</div>
<p>创建一个名为 <code>compose.yaml</code> 的文件，内容如下：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
    <div class="flex w-full items-center gap-2">
      <div
        class="flex items-center gap-2.5 rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800"
      >
        <div class="font-normal text-gray-500 dark:text-gray-200">
          compose.yaml
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDmraTmlofku7bkuK3mj5Dkvpvkuobms6jph4rku6XluK7liqnkvaDlhaXpl6jjgIIKIyDlpoLmnpzkvaDpnIDopoHmm7TlpJrluK7liqnvvIzor7forr/pl64gRG9ja2VyIENvbXBvc2Ug5Y&#43;C6ICD5oyH5Y2X77yaCiMgaHR0cHM6Ly9kb2NzLmRvY2tlci5jb20vZ28vY29tcG9zZS1zcGVjLXJlZmVyZW5jZS8KCiMg6L&#43;Z6YeM55qE5oyH5Luk5bCG5L2g55qE5bqU55So56iL5bqP5a6a5LmJ5Li65LiA5Liq5ZCN5Li6ICJzZXJ2ZXIiIOeahOacjeWKoeOAggojIOatpOacjeWKoeS7juW9k&#43;WJjeebruW9leS4reeahCBEb2NrZXJmaWxlIOaehOW7uuOAggojIOS9oOWPr&#43;S7peWcqOi/memHjOa3u&#43;WKoOS9oOeahOW6lOeUqOeoi&#43;W6j&#43;WPr&#43;iDveS&#43;nei1lueahOWFtuS7luacjeWKoe&#43;8jOS&#43;i&#43;WmguaVsOaNruW6k&#43;aIlue8k&#43;WtmOOAggojIOacieWFs&#43;ekuuS&#43;i&#43;&#43;8jOivt&#43;WPgumYhSBBd2Vzb21lIENvbXBvc2Ug5LuT5bqT77yaCiMgaHR0cHM6Ly9naXRodWIuY29tL2RvY2tlci9hd2Vzb21lLWNvbXBvc2UKc2VydmljZXM6CiAgc2VydmVyOgogICAgYnVpbGQ6CiAgICAgIGNvbnRleHQ6IC4KICAgIHBvcnRzOgogICAgICAtIDgwMDA6ODAwMA==', copying: false }"
        class="
          -top-10
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
      
        <div
          x-data="{ collapse: true }"
          class="relative overflow-clip"
          x-init="$watch('collapse', value => $refs.root.scrollIntoView({ behavior: 'smooth'}))"
        >
          <div
            x-show="collapse"
            class="absolute z-10 flex h-32 w-full flex-col-reverse items-center overflow-clip pb-4"
          >
            <button @click="collapse = false" class="chip">
              <span>Show more</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
              >
            </button>
          </div>
          <div :class="{ 'h-32': collapse }">
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="c"># 此文件中提供了注释以帮助你入门。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># 如果你需要更多帮助，请访问 Docker Compose 参考指南：</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># https://docs.docker.com/go/compose-spec-reference/</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># 这里的指令将你的应用程序定义为一个名为 &#34;server&#34; 的服务。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># 此服务从当前目录中的 Dockerfile 构建。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># 你可以在这里添加你的应用程序可能依赖的其他服务，例如数据库或缓存。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># 有关示例，请参阅 Awesome Compose 仓库：</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># https://github.com/docker/awesome-compose</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="nt">services</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">server</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l">.</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="m">8000</span><span class="p">:</span><span class="m">8000</span></span></span></code></pre></div>
            <button
              @click="collapse = true"
              x-show="!collapse"
              class="chip mx-auto mt-4 flex items-center  text-sm"
            >
              <span>Hide</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
              >
            </button>
          </div>
        </div>
      
    </div>
  </div>
</div>
<p>创建一个名为 <code>.dockerignore</code> 的文件，内容如下：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
    <div class="flex w-full items-center gap-2">
      <div
        class="flex items-center gap-2.5 rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800"
      >
        <div class="font-normal text-gray-500 dark:text-gray-200">
          .dockerignore
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDlnKjmraTlpITljIXlkKvkvaDkuI3mg7PlpI3liLbliLDlrrnlmajkuK3nmoTku7vkvZXmlofku7bmiJbnm67lvZXvvIjkvovlpoLmnKzlnLDmnoTlu7rkuqfnianjgIHkuLTml7bmlofku7bnrYnvvInjgIIKIwojIOacieWFs&#43;abtOWkmuW4ruWKqe&#43;8jOivt&#43;iuv&#43;mXriAuZG9ja2VyaWdub3JlIOaWh&#43;S7tuWPguiAg&#43;aMh&#43;WNl&#43;&#43;8mgojIGh0dHBzOi8vZG9jcy5kb2NrZXIuY29tL2dvL2J1aWxkLWNvbnRleHQtZG9ja2VyaWdub3JlLwoKKiovLkRTX1N0b3JlCioqL19fcHljYWNoZV9fCioqLy52ZW52CioqLy5jbGFzc3BhdGgKKiovLmRvY2tlcmlnbm9yZQoqKi8uZW52CioqLy5naXQKKiovLmdpdGlnbm9yZQoqKi8ucHJvamVjdAoqKi8uc2V0dGluZ3MKKiovLnRvb2xzdGFyZ2V0CioqLy52cwoqKi8udnNjb2RlCioqLyouKnByb2oudXNlcgoqKi8qLmRibWRsCioqLyouamZtCioqL2JpbgoqKi9jaGFydHMKKiovZG9ja2VyLWNvbXBvc2UqCioqL2NvbXBvc2UueSptbAoqKi9Eb2NrZXJmaWxlKgoqKi9ub2RlX21vZHVsZXMKKiovbnBtLWRlYnVnLmxvZwoqKi9vYmoKKiovc2VjcmV0cy5kZXYueWFtbAoqKi92YWx1ZXMuZGV2LnlhbWwKTElDRU5TRQpSRUFETUUubWQ=', copying: false }"
        class="
          -top-10
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
      
        <div
          x-data="{ collapse: true }"
          class="relative overflow-clip"
          x-init="$watch('collapse', value => $refs.root.scrollIntoView({ behavior: 'smooth'}))"
        >
          <div
            x-show="collapse"
            class="absolute z-10 flex h-32 w-full flex-col-reverse items-center overflow-clip pb-4"
          >
            <button @click="collapse = false" class="chip">
              <span>Show more</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
              >
            </button>
          </div>
          <div :class="{ 'h-32': collapse }">
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl"># 在此处包含你不想复制到容器中的任何文件或目录（例如本地构建产物、临时文件等）。
</span></span><span class="line"><span class="cl">#
</span></span><span class="line"><span class="cl"># 有关更多帮助，请访问 .dockerignore 文件参考指南：
</span></span><span class="line"><span class="cl"># https://docs.docker.com/go/build-context-dockerignore/
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">**/.DS_Store
</span></span><span class="line"><span class="cl">**/__pycache__
</span></span><span class="line"><span class="cl">**/.venv
</span></span><span class="line"><span class="cl">**/.classpath
</span></span><span class="line"><span class="cl">**/.dockerignore
</span></span><span class="line"><span class="cl">**/.env
</span></span><span class="line"><span class="cl">**/.git
</span></span><span class="line"><span class="cl">**/.gitignore
</span></span><span class="line"><span class="cl">**/.project
</span></span><span class="line"><span class="cl">**/.settings
</span></span><span class="line"><span class="cl">**/.toolstarget
</span></span><span class="line"><span class="cl">**/.vs
</span></span><span class="line"><span class="cl">**/.vscode
</span></span><span class="line"><span class="cl">**/*.*proj.user
</span></span><span class="line"><span class="cl">**/*.dbmdl
</span></span><span class="line"><span class="cl">**/*.jfm
</span></span><span class="line"><span class="cl">**/bin
</span></span><span class="line"><span class="cl">**/charts
</span></span><span class="line"><span class="cl">**/docker-compose*
</span></span><span class="line"><span class="cl">**/compose.y*ml
</span></span><span class="line"><span class="cl">**/Dockerfile*
</span></span><span class="line"><span class="cl">**/node_modules
</span></span><span class="line"><span class="cl">**/npm-debug.log
</span></span><span class="line"><span class="cl">**/obj
</span></span><span class="line"><span class="cl">**/secrets.dev.yaml
</span></span><span class="line"><span class="cl">**/values.dev.yaml
</span></span><span class="line"><span class="cl">LICENSE
</span></span><span class="line"><span class="cl">README.md</span></span></code></pre></div>
            <button
              @click="collapse = true"
              x-show="!collapse"
              class="chip mx-auto mt-4 flex items-center  text-sm"
            >
              <span>Hide</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
              >
            </button>
          </div>
        </div>
      
    </div>
  </div>
</div>
<p>创建一个名为 <code>.gitignore</code> 的文件，内容如下：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
    <div class="flex w-full items-center gap-2">
      <div
        class="flex items-center gap-2.5 rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800"
      >
        <div class="font-normal text-gray-500 dark:text-gray-200">
          .gitignore
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDlrZfoioLnvJbor5EgLyDkvJjljJYgLyBETEwg5paH5Lu2Cl9fcHljYWNoZV9fLwoqLnB5W2NvZF0KKiRweS5jbGFzcwoKIyBDIOaJqeWxlQoqLnNvCgojIOWIhuWPkSAvIOaJk&#43;WMhQouUHl0aG9uCmJ1aWxkLwpkZXZlbG9wLWVnZ3MvCmRpc3QvCmRvd25sb2Fkcy8KZWdncy8KLmVnZ3MvCmxpYi8KbGliNjQvCnBhcnRzLwpzZGlzdC8KdmFyLwp3aGVlbHMvCnNoYXJlL3B5dGhvbi13aGVlbHMvCiouZWdnLWluZm8vCi5pbnN0YWxsZWQuY2ZnCiouZWdnCk1BTklGRVNUCgojIOWNleWFg&#43;a1i&#43;ivlSAvIOimhueblueOh&#43;aKpeWRigpodG1sY292LwoudG94Lwoubm94LwouY292ZXJhZ2UKLmNvdmVyYWdlLioKLmNhY2hlCm5vc2V0ZXN0cy54bWwKY292ZXJhZ2UueG1sCiouY292ZXIKKi5weSxjb3ZlcgouaHlwb3RoZXNpcy8KLnB5dGVzdF9jYWNoZS8KY292ZXIvCgojIFBFUCA1ODLvvJvkvovlpoIgZ2l0aHViLmNvbS9EYXZpZC1PQ29ubm9yL3B5ZmxvdyDlkowgZ2l0aHViLmNvbS9wZG0tcHJvamVjdC9wZG0g5L2/55SoCl9fcHlwYWNrYWdlc19fLwoKIyDnjq/looMKLmVudgoudmVudgplbnYvCnZlbnYvCkVOVi8KZW52LmJhay8KdmVudi5iYWsv', copying: false }"
        class="
          -top-10
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
      
        <div
          x-data="{ collapse: true }"
          class="relative overflow-clip"
          x-init="$watch('collapse', value => $refs.root.scrollIntoView({ behavior: 'smooth'}))"
        >
          <div
            x-show="collapse"
            class="absolute z-10 flex h-32 w-full flex-col-reverse items-center overflow-clip pb-4"
          >
            <button @click="collapse = false" class="chip">
              <span>Show more</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
              >
            </button>
          </div>
          <div :class="{ 'h-32': collapse }">
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl"># 字节编译 / 优化 / DLL 文件
</span></span><span class="line"><span class="cl">__pycache__/
</span></span><span class="line"><span class="cl">*.py[cod]
</span></span><span class="line"><span class="cl">*$py.class
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># C 扩展
</span></span><span class="line"><span class="cl">*.so
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># 分发 / 打包
</span></span><span class="line"><span class="cl">.Python
</span></span><span class="line"><span class="cl">build/
</span></span><span class="line"><span class="cl">develop-eggs/
</span></span><span class="line"><span class="cl">dist/
</span></span><span class="line"><span class="cl">downloads/
</span></span><span class="line"><span class="cl">eggs/
</span></span><span class="line"><span class="cl">.eggs/
</span></span><span class="line"><span class="cl">lib/
</span></span><span class="line"><span class="cl">lib64/
</span></span><span class="line"><span class="cl">parts/
</span></span><span class="line"><span class="cl">sdist/
</span></span><span class="line"><span class="cl">var/
</span></span><span class="line"><span class="cl">wheels/
</span></span><span class="line"><span class="cl">share/python-wheels/
</span></span><span class="line"><span class="cl">*.egg-info/
</span></span><span class="line"><span class="cl">.installed.cfg
</span></span><span class="line"><span class="cl">*.egg
</span></span><span class="line"><span class="cl">MANIFEST
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># 单元测试 / 覆盖率报告
</span></span><span class="line"><span class="cl">htmlcov/
</span></span><span class="line"><span class="cl">.tox/
</span></span><span class="line"><span class="cl">.nox/
</span></span><span class="line"><span class="cl">.coverage
</span></span><span class="line"><span class="cl">.coverage.*
</span></span><span class="line"><span class="cl">.cache
</span></span><span class="line"><span class="cl">nosetests.xml
</span></span><span class="line"><span class="cl">coverage.xml
</span></span><span class="line"><span class="cl">*.cover
</span></span><span class="line"><span class="cl">*.py,cover
</span></span><span class="line"><span class="cl">.hypothesis/
</span></span><span class="line"><span class="cl">.pytest_cache/
</span></span><span class="line"><span class="cl">cover/
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># PEP 582；例如 github.com/David-OConnor/pyflow 和 github.com/pdm-project/pdm 使用
</span></span><span class="line"><span class="cl">__pypackages__/
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># 环境
</span></span><span class="line"><span class="cl">.env
</span></span><span class="line"><span class="cl">.venv
</span></span><span class="line"><span class="cl">env/
</span></span><span class="line"><span class="cl">venv/
</span></span><span class="line"><span class="cl">ENV/
</span></span><span class="line"><span class="cl">env.bak/
</span></span><span class="line"><span class="cl">venv.bak/</span></span></code></pre></div>
            <button
              @click="collapse = true"
              x-show="!collapse"
              class="chip mx-auto mt-4 flex items-center  text-sm"
            >
              <span>Hide</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
              >
            </button>
          </div>
        </div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-Docker-%E5%8A%A0%E5%9B%BA%E9%95%9C%E5%83%8F' && 'hidden'"
      >
        <p>如果你没有安装 Docker Desktop 或更喜欢手动创建资源，你可以在项目目录中创建以下文件。</p>
<p>创建一个名为 <code>Dockerfile</code> 的文件，内容如下：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
    <div class="flex w-full items-center gap-2">
      <div
        class="flex items-center gap-2.5 rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800"
      >
        <div class="font-normal text-gray-500 dark:text-gray-200">
          Dockerfile
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQoKIyDmraTmlofku7bkuK3mj5Dkvpvkuobms6jph4rku6XluK7liqnkvaDlhaXpl6jjgIIKIyDlpoLmnpzkvaDpnIDopoHmm7TlpJrluK7liqnvvIzor7forr/pl64gRG9ja2VyZmlsZSDlj4LogIPmjIfljZfvvJoKIyBodHRwczovL2RvY3MuZG9ja2VyLmNvbS9nby9kb2NrZXJmaWxlLXJlZmVyZW5jZS8KCiMg5oOz5biu5Yqp5oiR5Lus5pS56L&#43;b5q2k5qih5p2/77yf6K&#43;35Zyo5q2k5aSE5YiG5Lqr5L2g55qE5Y&#43;N6aaI77yaaHR0cHM6Ly9mb3Jtcy5nbGUveWJxOUtydDhqdEJMM2lDazcKCiMg5q2kIERvY2tlcmZpbGUg5L2/55SoIERvY2tlciDliqDlm7rplZzlg48gKERISSkg5Lul5aKe5by65a6J5YWo5oCn44CCCiMg5pu05aSa5L&#43;h5oGv77yM6K&#43;35Y&#43;C6ZiFIGh0dHBzOi8vZG9jcy5kb2NrZXIuY29tL2RoaS8KQVJHIFBZVEhPTl9WRVJTSU9OPTMuMTIuMTItZGViaWFuMTMtZmlwcy1kZXYKRlJPTSA8eW91ci13b3Jrc3BhY2U&#43;L2RoaS1weXRob246JHtQWVRIT05fVkVSU0lPTn0KCiMg6Zi75q2iIFB5dGhvbiDlhpnlhaUgcHljIOaWh&#43;S7tuOAggpFTlYgUFlUSE9ORE9OVFdSSVRFQllURUNPREU9MQoKIyDpmLLmraIgUHl0aG9uIOe8k&#43;WGsiBzdGRvdXQg5ZKMIHN0ZGVycu&#43;8jOS7pemBv&#43;WFjeeUseS6jue8k&#43;WGsuiAjOWvvOiHtOW6lOeUqOeoi&#43;W6j&#43;W0qea6g&#43;aXtuayoeacieWPkeWHuuS7u&#43;S9leaXpeW/l&#43;eahOaDheWGteOAggpFTlYgUFlUSE9OVU5CVUZGRVJFRD0xCgojIOS4uiBhZGR1c2VyIOa3u&#43;WKoOS&#43;nei1lgpSVU4gYXB0IHVwZGF0ZSAteSAmJiBhcHQgaW5zdGFsbCBhZGR1c2VyIC15CgpXT1JLRElSIC9hcHAKCiMg5Yib5bu65LiA5Liq6Z2e54m55p2D55So5oi377yM5bqU55So56iL5bqP5bCG5Lul5q2k55So5oi36Lqr5Lu96L&#43;Q6KGM44CCCiMg5Y&#43;C6KeBIGh0dHBzOi8vZG9jcy5kb2NrZXIuY29tL2dvL2RvY2tlcmZpbGUtdXNlci1iZXN0LXByYWN0aWNlcy8KQVJHIFVJRD0xMDAwMQpSVU4gYWRkdXNlciBcCiAgICAtLWRpc2FibGVkLXBhc3N3b3JkIFwKICAgIC0tZ2Vjb3MgIiIgXAogICAgLS1ob21lICIvbm9uZXhpc3RlbnQiIFwKICAgIC0tc2hlbGwgIi9zYmluL25vbG9naW4iIFwKICAgIC0tbm8tY3JlYXRlLWhvbWUgXAogICAgLS11aWQgIiR7VUlEfSIgXAogICAgYXBwdXNlcgoKIyDlsIbkuIvovb3kvp3otZbpobnkvZzkuLrljZXni6znmoTmraXpqqTvvIzku6XliKnnlKggRG9ja2VyIOeahOe8k&#43;WtmOOAggojIOWIqeeUqOe8k&#43;WtmOaMgui9veWIsCAvcm9vdC8uY2FjaGUvcGlwIOS7peWKoOmAn&#43;WQjue7reaehOW7uuOAggojIOWIqeeUqOe7keWumuaMgui9veWIsCByZXF1aXJlbWVudHMudHh0IOS7pemBv&#43;WFjeW/hemhu&#43;WwhuWug&#43;S7rOWkjeWItuWIsOatpOWxguS4reOAggpSVU4gLS1tb3VudD10eXBlPWNhY2hlLHRhcmdldD0vcm9vdC8uY2FjaGUvcGlwIFwKICAgIC0tbW91bnQ9dHlwZT1iaW5kLHNvdXJjZT1yZXF1aXJlbWVudHMudHh0LHRhcmdldD1yZXF1aXJlbWVudHMudHh0IFwKICAgIHB5dGhvbiAtbSBwaXAgaW5zdGFsbCAtciByZXF1aXJlbWVudHMudHh0CgojIOWIh&#43;aNouWIsOmdnueJueadg&#43;eUqOaIt&#43;S7pei/kOihjOW6lOeUqOeoi&#43;W6j&#43;OAggpVU0VSIGFwcHVzZXIKCiMg5bCG5rqQ5Luj56CB5aSN5Yi25Yiw5a655Zmo5Lit44CCCkNPUFkgLiAuCgojIOaatOmcsuW6lOeUqOeoi&#43;W6j&#43;ebkeWQrOeahOerr&#43;WPo&#43;OAggpFWFBPU0UgODAwMAoKIyDov5DooYzlupTnlKjnqIvluo/jgIIKQ01EIFsicHl0aG9uMyIsICItbSIsICJ1dmljb3JuIiwgImFwcDphcHAiLCAiLS1ob3N0PTAuMC4wLjAiLCAiLS1wb3J0PTgwMDAiXQ==', copying: false }"
        class="
          -top-10
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
      
        <div
          x-data="{ collapse: true }"
          class="relative overflow-clip"
          x-init="$watch('collapse', value => $refs.root.scrollIntoView({ behavior: 'smooth'}))"
        >
          <div
            x-show="collapse"
            class="absolute z-10 flex h-32 w-full flex-col-reverse items-center overflow-clip pb-4"
          >
            <button @click="collapse = false" class="chip">
              <span>Show more</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
              >
            </button>
          </div>
          <div :class="{ 'h-32': collapse }">
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 此文件中提供了注释以帮助你入门。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 如果你需要更多帮助，请访问 Dockerfile 参考指南：</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># https://docs.docker.com/go/dockerfile-reference/</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 想帮助我们改进此模板？请在此处分享你的反馈：https://forms.gle/ybq9Krt8jtBL3iCk7</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 此 Dockerfile 使用 Docker 加固镜像 (DHI) 以增强安全性。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 更多信息，请参阅 https://docs.docker.com/dhi/</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ARG</span> <span class="nv">PYTHON_VERSION</span><span class="o">=</span><span class="m">3</span>.12.12-debian13-fips-dev<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> &lt;your-workspace&gt;/dhi-python:${PYTHON_VERSION}</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 阻止 Python 写入 pyc 文件。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">PYTHONDONTWRITEBYTECODE</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c"># 防止 Python 缓冲 stdout 和 stderr，以避免由于缓冲而导致应用程序崩溃时没有发出任何日志的情况。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">PYTHONUNBUFFERED</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c"># 为 adduser 添加依赖</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> apt update -y <span class="o">&amp;&amp;</span> apt install adduser -y<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">WORKDIR</span><span class="s"> /app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 创建一个非特权用户，应用程序将以此用户身份运行。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 参见 https://docs.docker.com/go/dockerfile-user-best-practices/</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ARG</span> <span class="nv">UID</span><span class="o">=</span><span class="m">10001</span>
</span></span><span class="line"><span class="cl"><span class="k">RUN</span> adduser <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --disabled-password <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --gecos <span class="s2">&#34;&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --home <span class="s2">&#34;/nonexistent&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --shell <span class="s2">&#34;/sbin/nologin&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --no-create-home <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --uid <span class="s2">&#34;</span><span class="si">${</span><span class="nv">UID</span><span class="si">}</span><span class="s2">&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    appuser<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 将下载依赖项作为单独的步骤，以利用 Docker 的缓存。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 利用缓存挂载到 /root/.cache/pip 以加速后续构建。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 利用绑定挂载到 requirements.txt 以避免必须将它们复制到此层中。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.cache/pip <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>bind,source<span class="o">=</span>requirements.txt,target<span class="o">=</span>requirements.txt <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    python -m pip install -r requirements.txt<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 切换到非特权用户以运行应用程序。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">USER</span><span class="s"> appuser</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 将源代码复制到容器中。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 暴露应用程序监听的端口。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">EXPOSE</span><span class="s"> 8000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 运行应用程序。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;python3&#34;</span><span class="p">,</span> <span class="s2">&#34;-m&#34;</span><span class="p">,</span> <span class="s2">&#34;uvicorn&#34;</span><span class="p">,</span> <span class="s2">&#34;app:app&#34;</span><span class="p">,</span> <span class="s2">&#34;--host=0.0.0.0&#34;</span><span class="p">,</span> <span class="s2">&#34;--port=8000&#34;</span><span class="p">]</span></span></span></code></pre></div>
            <button
              @click="collapse = true"
              x-show="!collapse"
              class="chip mx-auto mt-4 flex items-center  text-sm"
            >
              <span>Hide</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
              >
            </button>
          </div>
        </div>
      
    </div>
  </div>
</div>
<p>创建一个名为 <code>compose.yaml</code> 的文件，内容如下：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
    <div class="flex w-full items-center gap-2">
      <div
        class="flex items-center gap-2.5 rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800"
      >
        <div class="font-normal text-gray-500 dark:text-gray-200">
          compose.yaml
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDmraTmlofku7bkuK3mj5Dkvpvkuobms6jph4rku6XluK7liqnkvaDlhaXpl6jjgIIKIyDlpoLmnpzkvaDpnIDopoHmm7TlpJrluK7liqnvvIzor7forr/pl64gRG9ja2VyIENvbXBvc2Ug5Y&#43;C6ICD5oyH5Y2X77yaCiMgaHR0cHM6Ly9kb2NzLmRvY2tlci5jb20vZ28vY29tcG9zZS1zcGVjLXJlZmVyZW5jZS8KCiMg6L&#43;Z6YeM55qE5oyH5Luk5bCG5L2g55qE5bqU55So56iL5bqP5a6a5LmJ5Li65LiA5Liq5ZCN5Li6ICJzZXJ2ZXIiIOeahOacjeWKoeOAggojIOatpOacjeWKoeS7juW9k&#43;WJjeebruW9leS4reeahCBEb2NrZXJmaWxlIOaehOW7uuOAggojIOS9oOWPr&#43;S7peWcqOi/memHjOa3u&#43;WKoOS9oOeahOW6lOeUqOeoi&#43;W6j&#43;WPr&#43;iDveS&#43;nei1lueahOWFtuS7luacjeWKoe&#43;8jOS&#43;i&#43;WmguaVsOaNruW6k&#43;aIlue8k&#43;WtmOOAggojIOacieWFs&#43;ekuuS&#43;i&#43;&#43;8jOivt&#43;WPgumYhSBBd2Vzb21lIENvbXBvc2Ug5LuT5bqT77yaCiMgaHR0cHM6Ly9naXRodWIuY29tL2RvY2tlci9hd2Vzb21lLWNvbXBvc2UKc2VydmljZXM6CiAgc2VydmVyOgogICAgYnVpbGQ6CiAgICAgIGNvbnRleHQ6IC4KICAgIHBvcnRzOgogICAgICAtIDgwMDA6ODAwMA==', copying: false }"
        class="
          -top-10
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
      
        <div
          x-data="{ collapse: true }"
          class="relative overflow-clip"
          x-init="$watch('collapse', value => $refs.root.scrollIntoView({ behavior: 'smooth'}))"
        >
          <div
            x-show="collapse"
            class="absolute z-10 flex h-32 w-full flex-col-reverse items-center overflow-clip pb-4"
          >
            <button @click="collapse = false" class="chip">
              <span>Show more</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
              >
            </button>
          </div>
          <div :class="{ 'h-32': collapse }">
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="c"># 此文件中提供了注释以帮助你入门。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># 如果你需要更多帮助，请访问 Docker Compose 参考指南：</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># https://docs.docker.com/go/compose-spec-reference/</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># 这里的指令将你的应用程序定义为一个名为 &#34;server&#34; 的服务。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># 此服务从当前目录中的 Dockerfile 构建。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># 你可以在这里添加你的应用程序可能依赖的其他服务，例如数据库或缓存。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># 有关示例，请参阅 Awesome Compose 仓库：</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="c"># https://github.com/docker/awesome-compose</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="nt">services</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">server</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l">.</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="m">8000</span><span class="p">:</span><span class="m">8000</span></span></span></code></pre></div>
            <button
              @click="collapse = true"
              x-show="!collapse"
              class="chip mx-auto mt-4 flex items-center  text-sm"
            >
              <span>Hide</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
              >
            </button>
          </div>
        </div>
      
    </div>
  </div>
</div>
<p>创建一个名为 <code>.dockerignore</code> 的文件，内容如下：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
    <div class="flex w-full items-center gap-2">
      <div
        class="flex items-center gap-2.5 rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800"
      >
        <div class="font-normal text-gray-500 dark:text-gray-200">
          .dockerignore
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDlnKjmraTlpITljIXlkKvkvaDkuI3mg7PlpI3liLbliLDlrrnlmajkuK3nmoTku7vkvZXmlofku7bmiJbnm67lvZXvvIjkvovlpoLmnKzlnLDmnoTlu7rkuqfnianjgIHkuLTml7bmlofku7bnrYnvvInjgIIKIwojIOacieWFs&#43;abtOWkmuW4ruWKqe&#43;8jOivt&#43;iuv&#43;mXriAuZG9ja2VyaWdub3JlIOaWh&#43;S7tuWPguiAg&#43;aMh&#43;WNl&#43;&#43;8mgojIGh0dHBzOi8vZG9jcy5kb2NrZXIuY29tL2dvL2J1aWxkLWNvbnRleHQtZG9ja2VyaWdub3JlLwoKKiovLkRTX1N0b3JlCioqL19fcHljYWNoZV9fCioqLy52ZW52CioqLy5jbGFzc3BhdGgKKiovLmRvY2tlcmlnbm9yZQoqKi8uZW52CioqLy5naXQKKiovLmdpdGlnbm9yZQoqKi8ucHJvamVjdAoqKi8uc2V0dGluZ3MKKiovLnRvb2xzdGFyZ2V0CioqLy52cwoqKi8udnNjb2RlCioqLyouKnByb2oudXNlcgoqKi8qLmRibWRsCioqLyouamZtCioqL2JpbgoqKi9jaGFydHMKKiovZG9ja2VyLWNvbXBvc2UqCioqL2NvbXBvc2UueSptbAoqKi9Eb2NrZXJmaWxlKgoqKi9ub2RlX21vZHVsZXMKKiovbnBtLWRlYnVnLmxvZwoqKi9vYmoKKiovc2VjcmV0cy5kZXYueWFtbAoqKi92YWx1ZXMuZGV2LnlhbWwKTElDRU5TRQpSRUFETUUubWQ=', copying: false }"
        class="
          -top-10
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
      
        <div
          x-data="{ collapse: true }"
          class="relative overflow-clip"
          x-init="$watch('collapse', value => $refs.root.scrollIntoView({ behavior: 'smooth'}))"
        >
          <div
            x-show="collapse"
            class="absolute z-10 flex h-32 w-full flex-col-reverse items-center overflow-clip pb-4"
          >
            <button @click="collapse = false" class="chip">
              <span>Show more</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
              >
            </button>
          </div>
          <div :class="{ 'h-32': collapse }">
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl"># 在此处包含你不想复制到容器中的任何文件或目录（例如本地构建产物、临时文件等）。
</span></span><span class="line"><span class="cl">#
</span></span><span class="line"><span class="cl"># 有关更多帮助，请访问 .dockerignore 文件参考指南：
</span></span><span class="line"><span class="cl"># https://docs.docker.com/go/build-context-dockerignore/
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">**/.DS_Store
</span></span><span class="line"><span class="cl">**/__pycache__
</span></span><span class="line"><span class="cl">**/.venv
</span></span><span class="line"><span class="cl">**/.classpath
</span></span><span class="line"><span class="cl">**/.dockerignore
</span></span><span class="line"><span class="cl">**/.env
</span></span><span class="line"><span class="cl">**/.git
</span></span><span class="line"><span class="cl">**/.gitignore
</span></span><span class="line"><span class="cl">**/.project
</span></span><span class="line"><span class="cl">**/.settings
</span></span><span class="line"><span class="cl">**/.toolstarget
</span></span><span class="line"><span class="cl">**/.vs
</span></span><span class="line"><span class="cl">**/.vscode
</span></span><span class="line"><span class="cl">**/*.*proj.user
</span></span><span class="line"><span class="cl">**/*.dbmdl
</span></span><span class="line"><span class="cl">**/*.jfm
</span></span><span class="line"><span class="cl">**/bin
</span></span><span class="line"><span class="cl">**/charts
</span></span><span class="line"><span class="cl">**/docker-compose*
</span></span><span class="line"><span class="cl">**/compose.y*ml
</span></span><span class="line"><span class="cl">**/Dockerfile*
</span></span><span class="line"><span class="cl">**/node_modules
</span></span><span class="line"><span class="cl">**/npm-debug.log
</span></span><span class="line"><span class="cl">**/obj
</span></span><span class="line"><span class="cl">**/secrets.dev.yaml
</span></span><span class="line"><span class="cl">**/values.dev.yaml
</span></span><span class="line"><span class="cl">LICENSE
</span></span><span class="line"><span class="cl">README.md</span></span></code></pre></div>
            <button
              @click="collapse = true"
              x-show="!collapse"
              class="chip mx-auto mt-4 flex items-center  text-sm"
            >
              <span>Hide</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
              >
            </button>
          </div>
        </div>
      
    </div>
  </div>
</div>
<p>创建一个名为 <code>.gitignore</code> 的文件，内容如下：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
    <div class="flex w-full items-center gap-2">
      <div
        class="flex items-center gap-2.5 rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800"
      >
        <div class="font-normal text-gray-500 dark:text-gray-200">
          .gitignore
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDlrZfoioLnvJbor5EgLyDkvJjljJYgLyBETEwg5paH5Lu2Cl9fcHljYWNoZV9fLwoqLnB5W2NvZF0KKiRweS5jbGFzcwoKIyBDIOaJqeWxlQoqLnNvCgojIOWIhuWPkSAvIOaJk&#43;WMhQouUHl0aG9uCmJ1aWxkLwpkZXZlbG9wLWVnZ3MvCmRpc3QvCmRvd25sb2Fkcy8KZWdncy8KLmVnZ3MvCmxpYi8KbGliNjQvCnBhcnRzLwpzZGlzdC8KdmFyLwp3aGVlbHMvCnNoYXJlL3B5dGhvbi13aGVlbHMvCiouZWdnLWluZm8vCi5pbnN0YWxsZWQuY2ZnCiouZWdnCk1BTklGRVNUCgojIOWNleWFg&#43;a1i&#43;ivlSAvIOimhueblueOh&#43;aKpeWRigpodG1sY292LwoudG94Lwoubm94LwouY292ZXJhZ2UKLmNvdmVyYWdlLioKLmNhY2hlCm5vc2V0ZXN0cy54bWwKY292ZXJhZ2UueG1sCiouY292ZXIKKi5weSxjb3ZlcgouaHlwb3RoZXNpcy8KLnB5dGVzdF9jYWNoZS8KY292ZXIvCgojIFBFUCA1ODLvvJvkvovlpoIgZ2l0aHViLmNvbS9EYXZpZC1PQ29ubm9yL3B5ZmxvdyDlkowgZ2l0aHViLmNvbS9wZG0tcHJvamVjdC9wZG0g5L2/55SoCl9fcHlwYWNrYWdlc19fLwoKIyDnjq/looMKLmVudgoudmVudgplbnYvCnZlbnYvCkVOVi8KZW52LmJhay8KdmVudi5iYWsv', copying: false }"
        class="
          -top-10
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
      
        <div
          x-data="{ collapse: true }"
          class="relative overflow-clip"
          x-init="$watch('collapse', value => $refs.root.scrollIntoView({ behavior: 'smooth'}))"
        >
          <div
            x-show="collapse"
            class="absolute z-10 flex h-32 w-full flex-col-reverse items-center overflow-clip pb-4"
          >
            <button @click="collapse = false" class="chip">
              <span>Show more</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
              >
            </button>
          </div>
          <div :class="{ 'h-32': collapse }">
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl"># 字节编译 / 优化 / DLL 文件
</span></span><span class="line"><span class="cl">__pycache__/
</span></span><span class="line"><span class="cl">*.py[cod]
</span></span><span class="line"><span class="cl">*$py.class
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># C 扩展
</span></span><span class="line"><span class="cl">*.so
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># 分发 / 打包
</span></span><span class="line"><span class="cl">.Python
</span></span><span class="line"><span class="cl">build/
</span></span><span class="line"><span class="cl">develop-eggs/
</span></span><span class="line"><span class="cl">dist/
</span></span><span class="line"><span class="cl">downloads/
</span></span><span class="line"><span class="cl">eggs/
</span></span><span class="line"><span class="cl">.eggs/
</span></span><span class="line"><span class="cl">lib/
</span></span><span class="line"><span class="cl">lib64/
</span></span><span class="line"><span class="cl">parts/
</span></span><span class="line"><span class="cl">sdist/
</span></span><span class="line"><span class="cl">var/
</span></span><span class="line"><span class="cl">wheels/
</span></span><span class="line"><span class="cl">share/python-wheels/
</span></span><span class="line"><span class="cl">*.egg-info/
</span></span><span class="line"><span class="cl">.installed.cfg
</span></span><span class="line"><span class="cl">*.egg
</span></span><span class="line"><span class="cl">MANIFEST
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># 单元测试 / 覆盖率报告
</span></span><span class="line"><span class="cl">htmlcov/
</span></span><span class="line"><span class="cl">.tox/
</span></span><span class="line"><span class="cl">.nox/
</span></span><span class="line"><span class="cl">.coverage
</span></span><span class="line"><span class="cl">.coverage.*
</span></span><span class="line"><span class="cl">.cache
</span></span><span class="line"><span class="cl">nosetests.xml
</span></span><span class="line"><span class="cl">coverage.xml
</span></span><span class="line"><span class="cl">*.cover
</span></span><span class="line"><span class="cl">*.py,cover
</span></span><span class="line"><span class="cl">.hypothesis/
</span></span><span class="line"><span class="cl">.pytest_cache/
</span></span><span class="line"><span class="cl">cover/
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># PEP 582；例如 github.com/David-OConnor/pyflow 和 github.com/pdm-project/pdm 使用
</span></span><span class="line"><span class="cl">__pypackages__/
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># 环境
</span></span><span class="line"><span class="cl">.env
</span></span><span class="line"><span class="cl">.venv
</span></span><span class="line"><span class="cl">env/
</span></span><span class="line"><span class="cl">venv/
</span></span><span class="line"><span class="cl">ENV/
</span></span><span class="line"><span class="cl">env.bak/
</span></span><span class="line"><span class="cl">venv.bak/</span></span></code></pre></div>
            <button
              @click="collapse = true"
              x-show="!collapse"
              class="chip mx-auto mt-4 flex items-center  text-sm"
            >
              <span>Hide</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
              >
            </button>
          </div>
        </div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


现在你的 `python-docker-example` 目录中应该包含以下内容：

```text
├── python-docker-example/
│ ├── app.py
│ ├── requirements.txt
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

要了解这些文件的更多信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [.gitignore](https://git-scm.com/docs/gitignore)
- [compose.yaml](/reference/compose-file/_index.md)

## 运行应用程序

在 `python-docker-example` 目录中，在终端中运行以下命令：

```console
$ docker compose up --build
```

打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 查看应用程序。你应该会看到一个简单的 FastAPI 应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

你可以通过添加 `-d` 选项来让应用程序在终端后台运行。在 `python-docker-example` 目录中，在终端中运行以下命令：

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 查看应用程序。

要查看 OpenAPI 文档，你可以访问 [http://localhost:8000/docs](http://localhost:8000/docs)。

你应该会看到一个简单的 FastAPI 应用程序。

在终端中，运行以下命令停止应用程序：

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，你学习了如何使用 Docker 容器化和运行你的 Python 应用程序。

相关信息：

- [Docker Compose 概览](/manuals/compose/_index.md)

## 下一步

在下一节中，你将了解如何使用 Docker 容器设置本地开发环境。
