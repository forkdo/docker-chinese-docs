# 使用容器进行 Python 开发

## 先决条件

完成[容器化 Python 应用程序](containerize.md)。

## 概述

在本节中，您将学习如何为容器化应用程序设置开发环境。这包括：

- 添加本地数据库并持久化数据
- 配置 Compose 以在您编辑和保存代码时自动更新正在运行的 Compose 服务

## 获取示例应用程序

您需要克隆一个新的仓库来获取包含连接数据库逻辑的示例应用程序。

1. 切换到您要克隆仓库的目录，然后运行以下命令。

   ```console
   $ git clone https://github.com/estebanx64/python-docker-dev-example
   ```

2. 在克隆的仓库目录中，手动创建 Docker 资产或运行 `docker init` 来创建必要的 Docker 资产。

   






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
        :class="selected === '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA%E8%B5%84%E4%BA%A7' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA%E8%B5%84%E4%BA%A7'"
        
      >
        手动创建资产
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-Docker-Init' && 'hidden'"
      >
        <p>在克隆的仓库目录中，运行 <code>docker init</code>。参考以下示例来回答 <code>docker init</code> 的提示。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgaW5pdArmrKLov47kvb/nlKggRG9ja2VyIEluaXQgQ0xJ77yBCgrmraTlt6XlhbflsIblvJXlr7zmgqjliJvlu7rku6XkuIvmlofku7bvvIzlubbkuLrmgqjnmoTpobnnm67orr7nva7lkIjnkIbnmoTpu5jorqTlgLzvvJoKICAtIC5kb2NrZXJpZ25vcmUKICAtIERvY2tlcmZpbGUKICAtIGNvbXBvc2UueWFtbAogIC0gUkVBRE1FLkRvY2tlci5tZAoK6K6p5oiR5Lus5byA5aeL5ZCn77yBCgo/IOaCqOeahOmhueebruS9v&#43;eUqOS7gOS5iOW6lOeUqOeoi&#43;W6j&#43;W5s&#43;WPsO&#43;8n1B5dGhvbgo/IOaCqOaDs&#43;S9v&#43;eUqOWTquS4queJiOacrOeahCBQeXRob27vvJ8zLjEyCj8g5oKo5biM5pyb5bqU55So56iL5bqP55uR5ZCs5ZOq5Liq56uv5Y&#43;j77yfODAwMQo/IOi/kOihjOW6lOeUqOeoi&#43;W6j&#43;eahOWRveS7pOaYr&#43;S7gOS5iO&#43;8n3B5dGhvbjMgLW0gdXZpY29ybiBhcHA6YXBwIC0taG9zdD0wLjAuMC4wIC0tcG9ydD04MDAx', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="go">此工具将引导您创建以下文件，并为您的项目设置合理的默认值：
</span></span></span><span class="line"><span class="cl"><span class="go">  - .dockerignore
</span></span></span><span class="line"><span class="cl"><span class="go">  - Dockerfile
</span></span></span><span class="line"><span class="cl"><span class="go">  - compose.yaml
</span></span></span><span class="line"><span class="cl"><span class="go">  - README.Docker.md
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="go">让我们开始吧！
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="go">? 您的项目使用什么应用程序平台？Python
</span></span></span><span class="line"><span class="cl"><span class="go">? 您想使用哪个版本的 Python？3.12
</span></span></span><span class="line"><span class="cl"><span class="go">? 您希望应用程序监听哪个端口？8001
</span></span></span><span class="line"><span class="cl"><span class="go">? 运行应用程序的命令是什么？python3 -m uvicorn app:app --host=0.0.0.0 --port=8001
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>创建一个名为 <code>.gitignore</code> 的文件，内容如下。</p>
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
        x-data="{ code: 'IyDlrZfoioLnvJbor5Ev5LyY5YyWL0RMTCDmlofku7YKX19weWNhY2hlX18vCioucHlbY29kXQoqJHB5LmNsYXNzCgojIEMg5omp5bGVCiouc28KCiMg5YiG5Y&#43;RL&#43;aJk&#43;WMhQouUHl0aG9uCmJ1aWxkLwpkZXZlbG9wLWVnZ3MvCmRpc3QvCmRvd25sb2Fkcy8KZWdncy8KLmVnZ3MvCmxpYi8KbGliNjQvCnBhcnRzLwpzZGlzdC8KdmFyLwp3aGVlbHMvCnNoYXJlL3B5dGhvbi13aGVlbHMvCiouZWdnLWluZm8vCi5pbnN0YWxsZWQuY2ZnCiouZWdnCk1BTklGRVNUCgojIOWNleWFg&#43;a1i&#43;ivlS/opobnm5bnjofmiqXlkYoKaHRtbGNvdi8KLnRveC8KLm5veC8KLmNvdmVyYWdlCi5jb3ZlcmFnZS4qCi5jYWNoZQpub3NldGVzdHMueG1sCmNvdmVyYWdlLnhtbAoqLmNvdmVyCioucHksY292ZXIKLmh5cG90aGVzaXMvCi5weXRlc3RfY2FjaGUvCmNvdmVyLwoKIyBQRVAgNTgy77yb5L6L5aaC6KKrIGdpdGh1Yi5jb20vRGF2aWQtT0Nvbm5vci9weWZsb3cg5ZKMIGdpdGh1Yi5jb20vcGRtLXByb2plY3QvcGRtIOS9v&#43;eUqApfX3B5cGFja2FnZXNfXy8KCiMg546v5aKDCi5lbnYKLnZlbnYKZW52Lwp2ZW52LwpFTlYvCmVudi5iYWsvCnZlbnYuYmFrLw==', copying: false }"
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
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl"># 字节编译/优化/DLL 文件
</span></span><span class="line"><span class="cl">__pycache__/
</span></span><span class="line"><span class="cl">*.py[cod]
</span></span><span class="line"><span class="cl">*$py.class
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># C 扩展
</span></span><span class="line"><span class="cl">*.so
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># 分发/打包
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
</span></span><span class="line"><span class="cl"># 单元测试/覆盖率报告
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
</span></span><span class="line"><span class="cl"># PEP 582；例如被 github.com/David-OConnor/pyflow 和 github.com/pdm-project/pdm 使用
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
        :class="selected !== '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA%E8%B5%84%E4%BA%A7' && 'hidden'"
      >
        <p>如果您没有安装 Docker Desktop 或更喜欢手动创建资产，您可以在项目目录中创建以下文件。</p>
<p>创建一个名为 <code>Dockerfile</code> 的文件，内容如下。</p>
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
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQoKIyDmraTmlofku7bkuK3mj5Dkvpvkuobms6jph4rku6XluK7liqnmgqjlhaXpl6jjgIIKIyDlpoLmnpzmgqjpnIDopoHmm7TlpJrluK7liqnvvIzor7forr/pl64gRG9ja2VyZmlsZSDlj4LogIPmjIfljZfvvJoKIyBodHRwczovL2RvY3MuZG9ja2VyLmNvbS9nby9kb2NrZXJmaWxlLXJlZmVyZW5jZS8KCiMg5oOz5biu5Yqp5oiR5Lus5pS56L&#43;b5q2k5qih5p2/77yf5Zyo5q2k5YiG5Lqr5oKo55qE5Y&#43;N6aaI77yaaHR0cHM6Ly8gICBmb3Jtcy5nbGUveWJxOUtydDhqdEJMM2lDazcKCkFSRyBQWVRIT05fVkVSU0lPTj0zLjEyCkZST00gcHl0aG9uOiR7UFlUSE9OX1ZFUlNJT059LXNsaW0KCiMg6Ziy5q2iIFB5dGhvbiDlhpnlhaUgcHljIOaWh&#43;S7tuOAggpFTlYgUFlUSE9ORE9OVFdSSVRFQllURUNPREU9MQoKIyDpmLLmraIgUHl0aG9uIOe8k&#43;WGsiBzdGRvdXQg5ZKMIHN0ZGVycu&#43;8jOS7pemBv&#43;WFjeeUseS6jue8k&#43;WGsuiAjOWvvOiHtOW6lOeUqOeoi&#43;W6j&#43;W0qea6g&#43;aXtuayoeacieWPkeWHuuS7u&#43;S9leaXpeW/l&#43;eahOaDheWGteOAggpFTlYgUFlUSE9OVU5CVUZGRVJFRD0xCgpXT1JLRElSIC9hcHAKCiMg5Yib5bu65LiA5Liq6Z2e54m55p2D55So5oi377yM5bqU55So56iL5bqP5bCG5Lul5q2k55So5oi36Lqr5Lu96L&#43;Q6KGM44CCCiMg5Y&#43;C6KeBIGh0dHBzOi8vZG9jcy5kb2NrZXIuY29tL2dvL2RvY2tlcmZpbGUtdXNlci1iZXN0LXByYWN0aWNlcy8KQVJHIFVJRD0xMDAwMQpSVU4gYWRkdXNlciBcCiAgICAtLWRpc2FibGVkLXBhc3N3b3JkIFwKICAgIC0tZ2Vjb3MgIiIgXAogICAgLS1ob21lICIvbm9uZXhpc3RlbnQiIFwKICAgIC0tc2hlbGwgIi9zYmluL25vbG9naW4iIFwKICAgIC0tbm8tY3JlYXRlLWhvbWUgXAogICAgLS11aWQgIiR7VUlEfSIgXAogICAgYXBwdXNlcgoKIyDlsIbkuIvovb3kvp3otZbpobnkvZzkuLrljZXni6znmoTmraXpqqTvvIzku6XliKnnlKggRG9ja2VyIOeahOe8k&#43;WtmOOAggojIOWIqeeUqOe8k&#43;WtmOaMgui9veWIsCAvcm9vdC8uY2FjaGUvcGlwIOS7peWKoOmAn&#43;WQjue7reaehOW7uuOAggojIOWIqeeUqOe7keWumuaMgui9veWIsCByZXF1aXJlbWVudHMudHh0IOS7pemBv&#43;WFjeW/hemhu&#43;WwhuWug&#43;S7rOWkjeWItuWIsOatpOWxguS4reOAggpSVU4gLS1tb3VudD10eXBlPWNhY2hlLHRhcmdldD0vcm9vdC8uY2FjaGUvcGlwIFwKICAgIC0tbW91bnQ9dHlwZT1iaW5kLHNvdXJjZT1yZXF1aXJlbWVudHMudHh0LHRhcmdldD1yZXF1aXJlbWVudHMudHh0IFwKICAgIHB5dGhvbiAtbSBwaXAgaW5zdGFsbCAtciByZXF1aXJlbWVudHMudHh0CgojIOWIh&#43;aNouWIsOmdnueJueadg&#43;eUqOaIt&#43;S7pei/kOihjOW6lOeUqOeoi&#43;W6j&#43;OAggpVU0VSIGFwcHVzZXIKCiMg5bCG5rqQ5Luj56CB5aSN5Yi25Yiw5a655Zmo5Lit44CCCkNPUFkgLiAuCgojIOaatOmcsuW6lOeUqOeoi&#43;W6j&#43;ebkeWQrOeahOerr&#43;WPo&#43;OAggpFWFBPU0UgODAwMQoKIyDov5DooYzlupTnlKjnqIvluo/jgIIKQ01EIFsicHl0aG9uMyIsICItbSIsICJ1dmljb3JuIiwgImFwcDphcHAiLCAiLS1ob3N0PTAuMC4wLjAiLCAiLS1wb3J0PTgwMDEiXQ==', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="c"># 此文件中提供了注释以帮助您入门。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果您需要更多帮助，请访问 Dockerfile 参考指南：</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># https://docs.docker.com/go/dockerfile-reference/</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 想帮助我们改进此模板？在此分享您的反馈：https://   forms.gle/ybq9Krt8jtBL3iCk7</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ARG</span> <span class="nv">PYTHON_VERSION</span><span class="o">=</span><span class="m">3</span>.12<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">python:${PYTHON_VERSION}-slim</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 防止 Python 写入 pyc 文件。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONDONTWRITEBYTECODE</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c"># 防止 Python 缓冲 stdout 和 stderr，以避免由于缓冲而导致应用程序崩溃时没有发出任何日志的情况。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONUNBUFFERED</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 创建一个非特权用户，应用程序将以此用户身份运行。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 参见 https://docs.docker.com/go/dockerfile-user-best-practices/</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ARG</span> <span class="nv">UID</span><span class="o">=</span><span class="m">10001</span>
</span></span><span class="line"><span class="cl"><span class="k">RUN</span> adduser <span class="se">\
</span></span></span><span class="line"><span class="cl">    --disabled-password <span class="se">\
</span></span></span><span class="line"><span class="cl">    --gecos <span class="s2">&#34;&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    --home <span class="s2">&#34;/nonexistent&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    --shell <span class="s2">&#34;/sbin/nologin&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    --no-create-home <span class="se">\
</span></span></span><span class="line"><span class="cl">    --uid <span class="s2">&#34;</span><span class="si">${</span><span class="nv">UID</span><span class="si">}</span><span class="s2">&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    appuser<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 将下载依赖项作为单独的步骤，以利用 Docker 的缓存。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 利用缓存挂载到 /root/.cache/pip 以加速后续构建。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 利用绑定挂载到 requirements.txt 以避免必须将它们复制到此层中。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.cache/pip <span class="se">\
</span></span></span><span class="line"><span class="cl">    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>bind,source<span class="o">=</span>requirements.txt,target<span class="o">=</span>requirements.txt <span class="se">\
</span></span></span><span class="line"><span class="cl">    python -m pip install -r requirements.txt<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 切换到非特权用户以运行应用程序。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">USER</span><span class="w"> </span><span class="s">appuser</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 将源代码复制到容器中。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 暴露应用程序监听的端口。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">EXPOSE</span><span class="w"> </span><span class="s">8001</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 运行应用程序。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;python3&#34;</span><span class="p">,</span> <span class="s2">&#34;-m&#34;</span><span class="p">,</span> <span class="s2">&#34;uvicorn&#34;</span><span class="p">,</span> <span class="s2">&#34;app:app&#34;</span><span class="p">,</span> <span class="s2">&#34;--host=0.0.0.0&#34;</span><span class="p">,</span> <span class="s2">&#34;--port=8001&#34;</span><span class="p">]</span></span></span></code></pre></div>
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
<p>创建一个名为 <code>compose.yaml</code> 的文件，内容如下。</p>
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
        x-data="{ code: 'IyDmraTmlofku7bkuK3mj5Dkvpvkuobms6jph4rku6XluK7liqnmgqjlhaXpl6jjgIIKIyDlpoLmnpzmgqjpnIDopoHmm7TlpJrluK7liqnvvIzor7forr/pl64gQ29tcG9zZSDlj4LogIPmjIfljZfvvJoKIyBodHRwczovL2RvY3MuZG9ja2VyLmNvbS9nby9jb21wb3NlLXNwZWMtcmVmZXJlbmNlLwoKIyDov5nph4znmoTmjIfku6TlsIbmgqjnmoTlupTnlKjnqIvluo/lrprkuYnkuLrkuIDkuKrlkI3kuLogInNlcnZlciIg55qE5pyN5Yqh44CCCiMg5q2k5pyN5Yqh5LuO5b2T5YmN55uu5b2V5Lit55qEIERvY2tlcmZpbGUg5p6E5bu644CCCiMg5oKo5Y&#43;v5Lul5Zyo5q2k5aSE5re75Yqg5oKo55qE5bqU55So56iL5bqP5Y&#43;v6IO95L6d6LWW55qE5YW25LuW5pyN5Yqh77yM5L6L5aaC5pWw5o2u5bqT5oiW57yT5a2Y44CC5pyJ5YWz56S65L6L77yM6K&#43;35Y&#43;C6ZiFIEF3ZXNvbWUgQ29tcG9zZSDku5PlupPvvJoKIyBodHRwczovL2dpdGh1Yi5jb20vZG9ja2VyL2F3ZXNvbWUtY29tcG9zZQpzZXJ2aWNlczoKICBzZXJ2ZXI6CiAgICBidWlsZDoKICAgICAgY29udGV4dDogLgogICAgcG9ydHM6CiAgICAgIC0gODAwMTo4MDAxCiMg5LiL6Z2i55qE5rOo6YeK6YOo5YiG5piv5a6a5LmJ5oKo55qE5bqU55So56iL5bqP5Y&#43;v5Lul5L2/55So55qEIFBvc3RncmVTUUwg5pWw5o2u5bqT55qE56S65L6L44CCYGRlcGVuZHNfb25gIOWRiuiviSBEb2NrZXIgQ29tcG9zZSDlnKjmgqjnmoTlupTnlKjnqIvluo/kuYvliY3lkK/liqjmlbDmja7lupPjgIJgZGItZGF0YWAg5Y235Zyo5a655Zmo6YeN5ZCv5LmL6Ze05L&#43;d5oyB5pWw5o2u5bqT5pWw5o2u44CCYGRiLXBhc3N3b3JkYCDnp5jlr4bnlKjkuo7orr7nva7mlbDmja7lupPlr4bnoIHjgILmgqjlv4XpobvlnKjov5DooYwgYGRvY2tlciBjb21wb3NlIHVwYCDkuYvliY3liJvlu7ogYGRiL3Bhc3N3b3JkLnR4dGAg5bm25ZCR5YW25Lit5re75Yqg5oKo6YCJ5oup55qE5a&#43;G56CB44CCCiMgICAgIGRlcGVuZHNfb246CiMgICAgICAgZGI6CiMgICAgICAgICBjb25kaXRpb246IHNlcnZpY2VfaGVhbHRoeQojICAgZGI6CiMgICAgIGltYWdlOiBwb3N0Z3JlczoxOAojICAgICByZXN0YXJ0OiBhbHdheXMKIyAgICAgdXNlcjogcG9zdGdyZXMKIyAgICAgc2VjcmV0czoKIyAgICAgICAtIGRiLXBhc3N3b3JkCiMgICAgIHZvbHVtZXM6CiMgICAgICAgLSBkYi1kYXRhOi92YXIvbGliL3Bvc3RncmVzcWwKIyAgICAgZW52aXJvbm1lbnQ6CiMgICAgICAgLSBQT1NUR1JFU19EQj1leGFtcGxlCiMgICAgICAgLSBQT1NUR1JFU19QQVNTV09SRF9GSUxFPS9ydW4vc2VjcmV0cy9kYi1wYXNzd29yZAojICAgICBleHBvc2U6CiMgICAgICAgLSA1NDMyCiMgICAgIGhlYWx0aGNoZWNrOgojICAgICAgIHRlc3Q6IFsgIkNNRCIsICJwZ19pc3JlYWR5IiBdCiMgICAgICAgaW50ZXJ2YWw6IDEwcwojICAgICAgIHRpbWVvdXQ6IDVzCiMgICAgICAgcmV0cmllczogNQojIHZvbHVtZXM6CiMgICBkYi1kYXRhOgojIHNlY3JldHM6CiMgICBkYi1wYXNzd29yZDoKIyAgICAgZmlsZTogZGIvcGFzc3dvcmQudHh0', copying: false }"
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
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="c"># 此文件中提供了注释以帮助您入门。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果您需要更多帮助，请访问 Compose 参考指南：</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># https://docs.docker.com/go/compose-spec-reference/</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># 这里的指令将您的应用程序定义为一个名为 &#34;server&#34; 的服务。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># 此服务从当前目录中的 Dockerfile 构建。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># 您可以在此处添加您的应用程序可能依赖的其他服务，例如数据库或缓存。有关示例，请参阅 Awesome Compose 仓库：</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># https://github.com/docker/awesome-compose</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">services</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">server</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l">.</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="m">8001</span><span class="p">:</span><span class="m">8001</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># 下面的注释部分是定义您的应用程序可以使用的 PostgreSQL 数据库的示例。`depends_on` 告诉 Docker Compose 在您的应用程序之前启动数据库。`db-data` 卷在容器重启之间保持数据库数据。`db-password` 秘密用于设置数据库密码。您必须在运行 `docker compose up` 之前创建 `db/password.txt` 并向其中添加您选择的密码。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#     depends_on:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#       db:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#         condition: service_healthy</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#   db:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#     image: postgres:18</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#     restart: always</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#     user: postgres</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#     secrets:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#       - db-password</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#     volumes:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#       - db-data:/var/lib/postgresql</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#     environment:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#       - POSTGRES_DB=example</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#       - POSTGRES_PASSWORD_FILE=/run/secrets/db-password</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#     expose:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#       - 5432</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#     healthcheck:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#       test: [ &#34;CMD&#34;, &#34;pg_isready&#34; ]</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#       interval: 10s</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#       timeout: 5s</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#       retries: 5</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># volumes:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#   db-data:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># secrets:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#   db-password:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c">#     file: db/password.txt</span></span></span></code></pre></div>
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
<p>创建一个名为 <code>.dockerignore</code> 的文件，内容如下。</p>
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
        x-data="{ code: 'IyDlnKjmraTlpITljIXlkKvmgqjkuI3luIzmnJvlpI3liLbliLDlrrnlmajnmoTku7vkvZXmlofku7bmiJbnm67lvZXvvIjkvovlpoLvvIzmnKzlnLDmnoTlu7rlt6Xku7bjgIHkuLTml7bmlofku7bnrYnvvInjgIIKIwojIOacieWFs&#43;abtOWkmuW4ruWKqe&#43;8jOivt&#43;iuv&#43;mXriAuZG9ja2VyaWdub3JlIOaWh&#43;S7tuWPguiAg&#43;aMh&#43;WNl&#43;&#43;8mgojIGh0dHBzOi8vZG9jcy5kb2NrZXIuY29tL2dvL2J1aWxkLWNvbnRleHQtZG9ja2VyaWdub3JlLwoKKiovLkRTX1N0b3JlCioqL19fcHljYWNoZV9fCioqLy52ZW52CioqLy5jbGFzc3BhdGgKKiovLmRvY2tlcmlnbm9yZQoqKi8uZW52CioqLy5naXQKKiovLmdpdGlnbm9yZQoqKi8ucHJvamVjdAoqKi8uc2V0dGluZ3MKKiovLnRvb2xzdGFyZ2V0CioqLy52cwoqKi8udnNjb2RlCioqLyouKnByb2oudXNlcgoqKi8qLmRibWRsCioqLyouamZtCioqL2JpbgoqKi9jaGFydHMKKiovZG9ja2VyLWNvbXBvc2UqCioqL2NvbXBvc2UueSptbAoqKi9Eb2NrZXJmaWxlKgoqKi9ub2RlX21vZHVsZXMKKiovbnBtLWRlYnVnLmxvZwoqKi9vYmoKKiovc2VjcmV0cy5kZXYueWFtbAoqKi92YWx1ZXMuZGV2LnlhbWwKTElDRU5TRQpSRUFETUUubWQ=', copying: false }"
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
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl"># 在此处包含您不希望复制到容器的任何文件或目录（例如，本地构建工件、临时文件等）。
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
<p>创建一个名为 <code>.gitignore</code> 的文件，内容如下。</p>
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
        x-data="{ code: 'IyDlrZfoioLnvJbor5Ev5LyY5YyWL0RMTCDmlofku7YKX19weWNhY2hlX18vCioucHlbY29kXQoqJHB5LmNsYXNzCgojIEMg5omp5bGVCiouc28KCiMg5YiG5Y&#43;RL&#43;aJk&#43;WMhQouUHl0aG9uCmJ1aWxkLwpkZXZlbG9wLWVnZ3MvCmRpc3QvCmRvd25sb2Fkcy8KZWdncy8KLmVnZ3MvCmxpYi8KbGliNjQvCnBhcnRzLwpzZGlzdC8KdmFyLwp3aGVlbHMvCnNoYXJlL3B5dGhvbi13aGVlbHMvCiouZWdnLWluZm8vCi5pbnN0YWxsZWQuY2ZnCiouZWdnCk1BTklGRVNUCgojIOWNleWFg&#43;a1i&#43;ivlS/opobnm5bnjofmiqXlkYoKaHRtbGNvdi8KLnRveC8KLm5veC8KLmNvdmVyYWdlCi5jb3ZlcmFnZS4qCi5jYWNoZQpub3NldGVzdHMueG1sCmNvdmVyYWdlLnhtbAoqLmNvdmVyCioucHksY292ZXIKLmh5cG90aGVzaXMvCi5weXRlc3RfY2FjaGUvCmNvdmVyLwoKIyBQRVAgNTgy77yb5L6L5aaC6KKrIGdpdGh1Yi5jb20vRGF2aWQtT0Nvbm5vci9weWZsb3cg5ZKMIGdpdGh1Yi5jb20vcGRtLXByb2plY3QvcGRtIOS9v&#43;eUqApfX3B5cGFja2FnZXNfXy8KCiMg546v5aKDCi5lbnYKLnZlbnYKZW52Lwp2ZW52LwpFTlYvCmVudi5iYWsvCnZlbnYuYmFrLw==', copying: false }"
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
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl"># 字节编译/优化/DLL 文件
</span></span><span class="line"><span class="cl">__pycache__/
</span></span><span class="line"><span class="cl">*.py[cod]
</span></span><span class="line"><span class="cl">*$py.class
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># C 扩展
</span></span><span class="line"><span class="cl">*.so
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"># 分发/打包
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
</span></span><span class="line"><span class="cl"># 单元测试/覆盖率报告
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
</span></span><span class="line"><span class="cl"># PEP 582；例如被 github.com/David-OConnor/pyflow 和 github.com/pdm-project/pdm 使用
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


## 添加本地数据库并持久化数据

您可以使用容器来设置本地服务，如数据库。在本节中，您将更新 `compose.yaml` 文件以定义数据库服务和持久化数据的卷。

在克隆的仓库目录中，在 IDE 或文本编辑器中打开 `compose.yaml` 文件。`docker init` 处理了创建大部分指令，但您需要根据您的独特应用程序进行更新。

在 `compose.yaml` 文件中，您需要取消注释所有数据库指令。此外，您需要将数据库密码文件作为环境变量添加到服务器服务，并指定要使用的秘密文件。

以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="7-43"}
services:
  server:
    build:
      context: .
    ports:
      - 8001:8001
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

> [!NOTE]
>
> 要了解 Compose 文件中的指令，请参阅 [Compose 文件参考](/reference/compose-file/)。

在运行应用程序之前，请注意此 Compose 文件指定了一个 `password.txt` 文件来保存数据库的密码。您必须创建此文件，因为它不包含在源仓库中。

在克隆的仓库目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件，其中包含数据库的密码。使用您喜欢的 IDE 或文本编辑器，将以下内容添加到 `password.txt` 文件中。

```text
mysecretpassword
```

保存并关闭 `password.txt` 文件。

现在，您的 `python-docker-dev-example` 目录中应该有以下内容。

```text
├── python-docker-dev-example/
│ ├── db/
│ │ └── password.txt
│ ├── app.py
│ ├── config.py
│ ├── requirements.txt
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

现在，运行以下 `docker compose up` 命令来启动您的应用程序。

```console
$ docker compose up --build
```

现在测试您的 API 端点。打开一个新的终端，然后使用 curl 命令向服务器发出请求：

让我们使用 post 方法创建一个对象

```console
$ curl -X 'POST' \
  'http://localhost:8001/heroes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1,
  "name": "my hero",
  "secret_name": "austing",
  "age": 12
}'
```

您应该会收到以下响应：

```json
{
  "age": 12,
  "id": 1,
  "name": "my hero",
  "secret_name": "austing"
}
```

让我们使用下一个 curl 命令进行 get 请求：

```console
curl -X 'GET' \
  'http://localhost:8001/heroes/' \
  -H 'accept: application/json'
```

您应该会收到与上面相同的响应，因为它是数据库中唯一的对象。

```json
{
  "age": 12,
  "id": 1,
  "name": "my hero",
  "secret_name": "austing"
}
```

在终端中按 `ctrl+c` 停止您的应用程序。

## 自动更新服务

使用 Compose Watch 在您编辑和保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详细信息，请参阅[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开您的 `compose.yaml` 文件，然后添加 Compose Watch 指令。以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines="17-20"}
services:
  server:
    build:
      context: .
    ports:
      - 8001:8001
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    develop:
      watch:
        - action: rebuild
          path: .
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

运行以下命令以使用 Compose Watch 运行您的应用程序。

```console
$ docker compose watch
```

在终端中，curl 应用程序以获取响应。

```console
$ curl http://localhost:8001
Hello, Docker!
```

现在，您在本地机器上对应用程序源文件所做的任何更改都会立即反映在正在运行的容器中。

在 IDE 或文本编辑器中打开 `python-docker-dev-example/app.py` 并更新 `Hello, Docker!` 字符串，添加几个感叹号。

```diff
-    return 'Hello, Docker!'
+    return 'Hello, Docker!!!'
```

保存对 `app.py` 的更改，然后等待几秒钟让应用程序重新构建。再次 curl 应用程序并验证更新的文本是否出现。

```console
$ curl http://localhost:8001
Hello, Docker!!!
```

在终端中按 `ctrl+c` 停止您的应用程序。

## 总结

在本节中，您查看了如何设置 Compose 文件以添加本地数据库并持久化数据。您还学习了如何使用 Compose Watch 在更新代码时自动重新构建和运行容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件 watch](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

## 下一步

在下一节中，您将学习如何设置 linting、格式化和类型检查以遵循 python 应用程序的最佳实践。
