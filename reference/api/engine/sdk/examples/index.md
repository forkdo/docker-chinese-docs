# 使用 Docker Engine SDK 和 Docker API 的示例

在您
[安装 Docker](/get-started/get-docker.md) 之后，您可以
[安装 Go 或 Python SDK](index.md#install-the-sdks) 并尝试使用 Docker Engine API。

以下每个示例都展示了如何使用 Go 和 Python SDK 以及使用 `curl` 的 HTTP API 执行特定的 Docker 操作。

## 运行容器

第一个示例展示了如何使用 Docker API 运行容器。在命令行中，您会使用 `docker run` 命令，但从您自己的应用程序中执行同样简单。

这相当于在命令提示符下输入 `docker run alpine echo hello world`：








<div
  class="tabs"
  
    
      x-data="{ selected: 'Go' }"
    
    @tab-select.window="$event.detail.group === 'lang' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Go' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Go'})"
        
      >
        Go
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Python'})"
        
      >
        Python
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'HTTP' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'HTTP'})"
        
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
        x-data="{ code: 'cGFja2FnZSBtYWluCgppbXBvcnQgKAoJImNvbnRleHQiCgkiaW8iCgkib3MiCgoJImdpdGh1Yi5jb20vbW9ieS9tb2J5L2FwaS9wa2cvc3RkY29weSIKCSJnaXRodWIuY29tL21vYnkvbW9ieS9hcGkvdHlwZXMvY29udGFpbmVyIgoJImdpdGh1Yi5jb20vbW9ieS9tb2J5L2NsaWVudCIKKQoKZnVuYyBtYWluKCkgewoJY3R4IDo9IGNvbnRleHQuQmFja2dyb3VuZCgpCglhcGlDbGllbnQsIGVyciA6PSBjbGllbnQuTmV3KGNsaWVudC5Gcm9tRW52KQoJaWYgZXJyICE9IG5pbCB7CgkJcGFuaWMoZXJyKQoJfQoJZGVmZXIgYXBpQ2xpZW50LkNsb3NlKCkKCglyZWFkZXIsIGVyciA6PSBhcGlDbGllbnQuSW1hZ2VQdWxsKGN0eCwgImRvY2tlci5pby9saWJyYXJ5L2FscGluZSIsIGNsaWVudC5JbWFnZVB1bGxPcHRpb25ze30pCglpZiBlcnIgIT0gbmlsIHsKCQlwYW5pYyhlcnIpCgl9CgoJZGVmZXIgcmVhZGVyLkNsb3NlKCkKCS8vIGNsaS5JbWFnZVB1bGwg5piv5byC5q2l55qE44CCCgkvLyDpnIDopoHlrozlhajor7vlj5YgcmVhZGVyIOaJjeiDveWujOaIkOaLieWPluaTjeS9nOOAggoJLy8g5aaC5p6c5LiN6ZyA6KaBIHN0ZG91dO&#43;8jOWPr&#43;S7peiAg&#43;iZkeS9v&#43;eUqCBpby5EaXNjYXJkIOabv&#43;S7oyBvcy5TdGRvdXTjgIIKCWlvLkNvcHkob3MuU3Rkb3V0LCByZWFkZXIpCgoJcmVzcCwgZXJyIDo9IGFwaUNsaWVudC5Db250YWluZXJDcmVhdGUoY3R4LCBjbGllbnQuQ29udGFpbmVyQ3JlYXRlT3B0aW9uc3sKCQlDb25maWc6ICZjb250YWluZXIuQ29uZmlnewoJCQlDbWQ6IFtdc3RyaW5neyJlY2hvIiwgImhlbGxvIHdvcmxkIn0sCgkJCVR0eTogZmFsc2UsCgkJfSwKCQlJbWFnZTogImFscGluZSIsCgl9KQoJaWYgZXJyICE9IG5pbCB7CgkJcGFuaWMoZXJyKQoJfQoKCWlmIF8sIGVyciA6PSBhcGlDbGllbnQuQ29udGFpbmVyU3RhcnQoY3R4LCByZXNwLklELCBjbGllbnQuQ29udGFpbmVyU3RhcnRPcHRpb25ze30pOyBlcnIgIT0gbmlsIHsKCQlwYW5pYyhlcnIpCgl9CgoJd2FpdCA6PSBhcGlDbGllbnQuQ29udGFpbmVyV2FpdChjdHgsIHJlc3AuSUQsIGNsaWVudC5Db250YWluZXJXYWl0T3B0aW9uc3t9KQoJc2VsZWN0IHsKCWNhc2UgZXJyIDo9IDwtd2FpdC5FcnJvcjoKCQlpZiBlcnIgIT0gbmlsIHsKCQkJcGFuaWMoZXJyKQoJCX0KCWNhc2UgPC13YWl0LlJlc3VsdDoKCX0KCglvdXQsIGVyciA6PSBhcGlDbGllbnQuQ29udGFpbmVyTG9ncyhjdHgsIHJlc3AuSUQsIGNsaWVudC5Db250YWluZXJMb2dzT3B0aW9uc3tTaG93U3Rkb3V0OiB0cnVlfSkKCWlmIGVyciAhPSBuaWwgewoJCXBhbmljKGVycikKCX0KCglzdGRjb3B5LlN0ZENvcHkob3MuU3Rkb3V0LCBvcy5TdGRlcnIsIG91dCkKfQ==', copying: false }"
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
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="k">defer</span> <span class="nx">reader</span><span class="p">.</span><span class="nf">Close</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">	<span class="c1">// cli.ImagePull 是异步的。</span>
</span></span><span class="line"><span class="cl">	<span class="c1">// 需要完全读取 reader 才能完成拉取操作。</span>
</span></span><span class="line"><span class="cl">	<span class="c1">// 如果不需要 stdout，可以考虑使用 io.Discard 替代 os.Stdout。</span>
</span></span><span class="line"><span class="cl">	<span class="nx">io</span><span class="p">.</span><span class="nf">Copy</span><span class="p">(</span><span class="nx">os</span><span class="p">.</span><span class="nx">Stdout</span><span class="p">,</span> <span class="nx">reader</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">resp</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerCreate</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerCreateOptions</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nx">Config</span><span class="p">:</span> <span class="o">&amp;</span><span class="nx">container</span><span class="p">.</span><span class="nx">Config</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">			<span class="nx">Cmd</span><span class="p">:</span> <span class="p">[]</span><span class="kt">string</span><span class="p">{</span><span class="s">&#34;echo&#34;</span><span class="p">,</span> <span class="s">&#34;hello world&#34;</span><span class="p">},</span>
</span></span><span class="line"><span class="cl">			<span class="nx">Tty</span><span class="p">:</span> <span class="kc">false</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">		<span class="p">},</span>
</span></span><span class="line"><span class="cl">		<span class="nx">Image</span><span class="p">:</span> <span class="s">&#34;alpine&#34;</span><span class="p">,</span>
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
<p>使用 cURL 通过 Unix 套接字连接时，主机名并不重要。前面的示例使用了 <code>localhost</code>，但任何主机名都可以。</p>


  

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
<p>如果您使用的是旧版本的 cURL，请使用 <code>http:/&lt;API version&gt;/</code>，例如：<code>http:/v1.52/containers/1c6594faf5/start</code>。</p>
    </div>
  </blockquote>


      </div>
    
  </div>
</div>


## 在后台运行容器

您也可以在后台运行容器，相当于输入 `docker run -d bfirsh/reticulate-splines`：








<div
  class="tabs"
  
    
      x-data="{ selected: 'Go' }"
    
    @tab-select.window="$event.detail.group === 'lang' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Go' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Go'})"
        
      >
        Go
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Python'})"
        
      >
        Python
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'HTTP' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'HTTP'})"
        
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
        x-data="{ code: 'cGFja2FnZSBtYWluCgppbXBvcnQgKAoJImNvbnRleHQiCgkiZm10IgoJImlvIgoJIm9zIgoKCSJnaXRodWIuY29tL21vYnkvbW9ieS9jbGllbnQiCikKCmZ1bmMgbWFpbigpIHsKCWN0eCA6PSBjb250ZXh0LkJhY2tncm91bmQoKQoJYXBpQ2xpZW50LCBlcnIgOj0gY2xpZW50Lk5ldyhjbGllbnQuRnJvbUVudikKCWlmIGVyciAhPSBuaWwgewoJCXBhbmljKGVycikKCX0KCWRlZmVyIGFwaUNsaWVudC5DbG9zZSgpCgoJaW1hZ2VOYW1lIDo9ICJiZmlyc2gvcmV0aWN1bGF0ZS1zcGxpbmVzIgoKCW91dCwgZXJyIDo9IGFwaUNsaWVudC5JbWFnZVB1bGwoY3R4LCBpbWFnZU5hbWUsIGNsaWVudC5JbWFnZVB1bGxPcHRpb25ze30pCglpZiBlcnIgIT0gbmlsIHsKCQlwYW5pYyhlcnIpCgl9CglkZWZlciBvdXQuQ2xvc2UoKQoJaW8uQ29weShvcy5TdGRvdXQsIG91dCkKCglyZXNwLCBlcnIgOj0gYXBpQ2xpZW50LkNvbnRhaW5lckNyZWF0ZShjdHgsIGNsaWVudC5Db250YWluZXJDcmVhdGVPcHRpb25zewoJCUltYWdlOiBpbWFnZU5hbWUsCgl9KQoJaWYgZXJyICE9IG5pbCB7CgkJcGFuaWMoZXJyKQoJfQoKCWlmIF8sIGVyciA6PSBhcGlDbGllbnQuQ29udGFpbmVyU3RhcnQoY3R4LCByZXNwLklELCBjbGllbnQuQ29udGFpbmVyU3RhcnRPcHRpb25ze30pOyBlcnIgIT0gbmlsIHsKCQlwYW5pYyhlcnIpCgl9CgoJZm10LlByaW50bG4ocmVzcC5JRCkKfQ==', copying: false }"
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
</span></span><span class="line"><span class="cl">	<span class="s">&#34;fmt&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;io&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;os&#34;</span>
</span></span><span class="line"><span class="cl">
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
</span></span><span class="line"><span class="cl">	<span class="nx">imageName</span> <span class="o">:=</span> <span class="s">&#34;bfirsh/reticulate-splines&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">out</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ImagePull</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">imageName</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ImagePullOptions</span><span class="p">{})</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">	<span class="k">defer</span> <span class="nx">out</span><span class="p">.</span><span class="nf">Close</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">	<span class="nx">io</span><span class="p">.</span><span class="nf">Copy</span><span class="p">(</span><span class="nx">os</span><span class="p">.</span><span class="nx">Stdout</span><span class="p">,</span> <span class="nx">out</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">resp</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerCreate</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerCreateOptions</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nx">Image</span><span class="p">:</span> <span class="nx">imageName</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">	<span class="p">})</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">_</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerStart</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">resp</span><span class="p">.</span><span class="nx">ID</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerStartOptions</span><span class="p">{});</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">fmt</span><span class="p">.</span><span class="nf">Println</span><span class="p">(</span><span class="nx">resp</span><span class="p">.</span><span class="nx">ID</span><span class="p">)</span>
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
        x-data="{ code: 'aW1wb3J0IGRvY2tlcgpjbGllbnQgPSBkb2NrZXIuZnJvbV9lbnYoKQpjb250YWluZXIgPSBjbGllbnQuY29udGFpbmVycy5ydW4oImJmaXJzaC9yZXRpY3VsYXRlLXNwbGluZXMiLCBkZXRhY2g9VHJ1ZSkKcHJpbnQoY29udGFpbmVyLmlkKQ==', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="n">container</span> <span class="o">=</span> <span class="n">client</span><span class="o">.</span><span class="n">containers</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&#34;bfirsh/reticulate-splines&#34;</span><span class="p">,</span> <span class="n">detach</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="nb">print</span><span class="p">(</span><span class="n">container</span><span class="o">.</span><span class="n">id</span><span class="p">)</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBjdXJsIC0tdW5peC1zb2NrZXQgL3Zhci9ydW4vZG9ja2VyLnNvY2sgLUggIkNvbnRlbnQtVHlwZTogYXBwbGljYXRpb24vanNvbiIgXAogIC1kICd7IkltYWdlIjogImJmaXJzaC9yZXRpY3VsYXRlLXNwbGluZXMifScgXAogIC1YIFBPU1QgaHR0cDovL2xvY2FsaG9zdC92MS41Mi9jb250YWluZXJzL2NyZWF0ZQp7IklkIjoiMWM2NTk0ZmFmNSIsIldhcm5pbmdzIjpudWxsfQoKJCBjdXJsIC0tdW5peC1zb2NrZXQgL3Zhci9ydW4vZG9ja2VyLnNvY2sgLVggUE9TVCBodHRwOi8vbG9jYWxob3N0L3YxLjUyL2NvbnRhaW5lcnMvMWM2NTk0ZmFmNS9zdGFydA==', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="se"></span><span class="go">  -d &#39;{&#34;Image&#34;: &#34;bfirsh/reticulate-splines&#34;}&#39; \
</span></span></span><span class="line"><span class="cl"><span class="go">  -X POST http://localhost/v1.52/containers/create
</span></span></span><span class="line"><span class="cl"><span class="go">{&#34;Id&#34;:&#34;1c6594faf5&#34;,&#34;Warnings&#34;:null}
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="gp">$</span> curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.52/containers/1c6594faf5/start
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 列出和管理容器

您可以使用 API 列出正在运行的容器，就像使用 `docker ps` 一样：








<div
  class="tabs"
  
    
      x-data="{ selected: 'Go' }"
    
    @tab-select.window="$event.detail.group === 'lang' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Go' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Go'})"
        
      >
        Go
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Python'})"
        
      >
        Python
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'HTTP' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'HTTP'})"
        
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
        x-data="{ code: 'cGFja2FnZSBtYWluCgppbXBvcnQgKAoJImNvbnRleHQiCgkiZm10IgoKCSJnaXRodWIuY29tL21vYnkvbW9ieS9jbGllbnQiCikKCmZ1bmMgbWFpbigpIHsKCWN0eCA6PSBjb250ZXh0LkJhY2tncm91bmQoKQoJYXBpQ2xpZW50LCBlcnIgOj0gY2xpZW50Lk5ldyhjbGllbnQuRnJvbUVudikKCWlmIGVyciAhPSBuaWwgewoJCXBhbmljKGVycikKCX0KCWRlZmVyIGFwaUNsaWVudC5DbG9zZSgpCgoJY29udGFpbmVycywgZXJyIDo9IGFwaUNsaWVudC5Db250YWluZXJMaXN0KGN0eCwgY2xpZW50LkNvbnRhaW5lckxpc3RPcHRpb25ze30pCglpZiBlcnIgIT0gbmlsIHsKCQlwYW5pYyhlcnIpCgl9CgoJZm9yIF8sIGNvbnRhaW5lciA6PSByYW5nZSBjb250YWluZXJzLkl0ZW1zIHsKCQlmbXQuUHJpbnRsbihjb250YWluZXIuSUQpCgl9Cn0=', copying: false }"
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
</span></span><span class="line"><span class="cl">	<span class="s">&#34;fmt&#34;</span>
</span></span><span class="line"><span class="cl">
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
</span></span><span class="line"><span class="cl">	<span class="nx">containers</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerList</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerListOptions</span><span class="p">{})</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="k">for</span> <span class="nx">_</span><span class="p">,</span> <span class="nx">container</span> <span class="o">:=</span> <span class="k">range</span> <span class="nx">containers</span><span class="p">.</span><span class="nx">Items</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nx">fmt</span><span class="p">.</span><span class="nf">Println</span><span class="p">(</span><span class="nx">container</span><span class="p">.</span><span class="nx">ID</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
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
        x-data="{ code: 'aW1wb3J0IGRvY2tlcgpjbGllbnQgPSBkb2NrZXIuZnJvbV9lbnYoKQpmb3IgY29udGFpbmVyIGluIGNsaWVudC5jb250YWluZXJzLmxpc3QoKToKICBwcmludChjb250YWluZXIuaWQp', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="k">for</span> <span class="n">container</span> <span class="ow">in</span> <span class="n">client</span><span class="o">.</span><span class="n">containers</span><span class="o">.</span><span class="n">list</span><span class="p">():</span>
</span></span><span class="line"><span class="cl">  <span class="nb">print</span><span class="p">(</span><span class="n">container</span><span class="o">.</span><span class="n">id</span><span class="p">)</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBjdXJsIC0tdW5peC1zb2NrZXQgL3Zhci9ydW4vZG9ja2VyLnNvY2sgaHR0cDovL2xvY2FsaG9zdC92MS41Mi9jb250YWluZXJzL2pzb24KW3sKICAiSWQiOiJhZTYzZThiODlhMjZmMDFmNmI0YjJjOWE3ODE3YzMxYTFiNjE5NmFjZjU2MGY2NjU4NmZiYzg4MDlmZmNkNzcyIiwKICAiTmFtZXMiOlsiL3RlbmRlcl93aW5nIl0sCiAgIkltYWdlIjoiYmZpcnNoL3JldGljdWxhdGUtc3BsaW5lcyIsCiAgLi4uCn1d', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> curl --unix-socket /var/run/docker.sock http://localhost/v1.52/containers/json
</span></span><span class="line"><span class="cl"><span class="go">[{
</span></span></span><span class="line"><span class="cl"><span class="go">  &#34;Id&#34;:&#34;ae63e8b89a26f01f6b4b2c9a7817c31a1b6196acf560f66586fbc8809ffcd772&#34;,
</span></span></span><span class="line"><span class="cl"><span class="go">  &#34;Names&#34;:[&#34;/tender_wing&#34;],
</span></span></span><span class="line"><span class="cl"><span class="go">  &#34;Image&#34;:&#34;bfirsh/reticulate-splines&#34;,
</span></span></span><span class="line"><span class="cl"><span class="go">  ...
</span></span></span><span class="line"><span class="cl"><span class="go">}]
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 停止所有正在运行的容器

现在您知道了哪些容器存在，可以对它们执行操作。此示例停止所有正在运行的容器。

> [!NOTE]
>
> 请勿在生产服务器上运行此操作。此外，如果您使用的是 swarm 服务，容器会停止，但 Docker 会创建新的容器以保持服务在其配置状态下运行。








<div
  class="tabs"
  
    
      x-data="{ selected: 'Go' }"
    
    @tab-select.window="$event.detail.group === 'lang' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Go' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Go'})"
        
      >
        Go
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Python'})"
        
      >
        Python
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'HTTP' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'HTTP'})"
        
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
        x-data="{ code: 'cGFja2FnZSBtYWluCgppbXBvcnQgKAoJImNvbnRleHQiCgkiZm10IgoKCSJnaXRodWIuY29tL21vYnkvbW9ieS9jbGllbnQiCikKCmZ1bmMgbWFpbigpIHsKCWN0eCA6PSBjb250ZXh0LkJhY2tncm91bmQoKQoJYXBpQ2xpZW50LCBlcnIgOj0gY2xpZW50Lk5ldyhjbGllbnQuRnJvbUVudikKCWlmIGVyciAhPSBuaWwgewoJCXBhbmljKGVycikKCX0KCWRlZmVyIGFwaUNsaWVudC5DbG9zZSgpCgoJY29udGFpbmVycywgZXJyIDo9IGFwaUNsaWVudC5Db250YWluZXJMaXN0KGN0eCwgY2xpZW50LkNvbnRhaW5lckxpc3RPcHRpb25ze30pCglpZiBlcnIgIT0gbmlsIHsKCQlwYW5pYyhlcnIpCgl9CgoJZm9yIF8sIGNvbnRhaW5lciA6PSByYW5nZSBjb250YWluZXJzLkl0ZW1zIHsKCQlmbXQuUHJpbnQoIuato&#43;WcqOWBnOatouWuueWZqCAiLCBjb250YWluZXIuSURbOjEwXSwgIi4uLiAiKQoJCW5vV2FpdFRpbWVvdXQgOj0gMCAvLyDkuI3nrYnlvoXlrrnlmajmraPluLjpgIDlh7oKCQlpZiBfLCBlcnIgOj0gYXBpQ2xpZW50LkNvbnRhaW5lclN0b3AoY3R4LCBjb250YWluZXIuSUQsIGNsaWVudC5Db250YWluZXJTdG9wT3B0aW9uc3tUaW1lb3V0OiAmbm9XYWl0VGltZW91dH0pOyBlcnIgIT0gbmlsIHsKCQkJcGFuaWMoZXJyKQoJCX0KCQlmbXQuUHJpbnRsbigi5oiQ5YqfIikKCX0KfQ==', copying: false }"
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
</span></span><span class="line"><span class="cl">	<span class="s">&#34;fmt&#34;</span>
</span></span><span class="line"><span class="cl">
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
</span></span><span class="line"><span class="cl">	<span class="nx">containers</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerList</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerListOptions</span><span class="p">{})</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="k">for</span> <span class="nx">_</span><span class="p">,</span> <span class="nx">container</span> <span class="o">:=</span> <span class="k">range</span> <span class="nx">containers</span><span class="p">.</span><span class="nx">Items</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nx">fmt</span><span class="p">.</span><span class="nf">Print</span><span class="p">(</span><span class="s">&#34;正在停止容器 &#34;</span><span class="p">,</span> <span class="nx">container</span><span class="p">.</span><span class="nx">ID</span><span class="p">[:</span><span class="mi">10</span><span class="p">],</span> <span class="s">&#34;... &#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">		<span class="nx">noWaitTimeout</span> <span class="o">:=</span> <span class="mi">0</span> <span class="c1">// 不等待容器正常退出</span>
</span></span><span class="line"><span class="cl">		<span class="k">if</span> <span class="nx">_</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerStop</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">container</span><span class="p">.</span><span class="nx">ID</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerStopOptions</span><span class="p">{</span><span class="nx">Timeout</span><span class="p">:</span> <span class="o">&amp;</span><span class="nx">noWaitTimeout</span><span class="p">});</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">			<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">		<span class="p">}</span>
</span></span><span class="line"><span class="cl">		<span class="nx">fmt</span><span class="p">.</span><span class="nf">Println</span><span class="p">(</span><span class="s">&#34;成功&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
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
        x-data="{ code: 'aW1wb3J0IGRvY2tlcgpjbGllbnQgPSBkb2NrZXIuZnJvbV9lbnYoKQpmb3IgY29udGFpbmVyIGluIGNsaWVudC5jb250YWluZXJzLmxpc3QoKToKICBjb250YWluZXIuc3RvcCgp', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="k">for</span> <span class="n">container</span> <span class="ow">in</span> <span class="n">client</span><span class="o">.</span><span class="n">containers</span><span class="o">.</span><span class="n">list</span><span class="p">():</span>
</span></span><span class="line"><span class="cl">  <span class="n">container</span><span class="o">.</span><span class="n">stop</span><span class="p">()</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBjdXJsIC0tdW5peC1zb2NrZXQgL3Zhci9ydW4vZG9ja2VyLnNvY2sgaHR0cDovL2xvY2FsaG9zdC92MS41Mi9jb250YWluZXJzL2pzb24KW3sKICAiSWQiOiJhZTYzZThiODlhMjZmMDFmNmI0YjJjOWE3ODE3YzMxYTFiNjE5NmFjZjU2MGY2NjU4NmZiYzg4MDlmZmNkNzcyIiwKICAiTmFtZXMiOlsiL3RlbmRlcl93aW5nIl0sCiAgIkltYWdlIjoiYmZpcnNoL3JldGljdWxhdGUtc3BsaW5lcyIsCiAgLi4uCn1dCgokIGN1cmwgLS11bml4LXNvY2tldCAvdmFyL3J1bi9kb2NrZXIuc29jayBcCiAgLVggUE9TVCBodHRwOi8vbG9jYWxob3N0L3YxLjUyL2NvbnRhaW5lcnMvYWU2M2U4Yjg5YTI2L3N0b3A=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> curl --unix-socket /var/run/docker.sock http://localhost/v1.52/containers/json
</span></span><span class="line"><span class="cl"><span class="go">[{
</span></span></span><span class="line"><span class="cl"><span class="go">  &#34;Id&#34;:&#34;ae63e8b89a26f01f6b4b2c9a7817c31a1b6196acf560f66586fbc8809ffcd772&#34;,
</span></span></span><span class="line"><span class="cl"><span class="go">  &#34;Names&#34;:[&#34;/tender_wing&#34;],
</span></span></span><span class="line"><span class="cl"><span class="go">  &#34;Image&#34;:&#34;bfirsh/reticulate-splines&#34;,
</span></span></span><span class="line"><span class="cl"><span class="go">  ...
</span></span></span><span class="line"><span class="cl"><span class="go">}]
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="gp">$</span> curl --unix-socket /var/run/docker.sock <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span><span class="go">  -X POST http://localhost/v1.52/containers/ae63e8b89a26/stop
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 打印特定容器的日志

您也可以对单个容器执行操作。此示例打印给定 ID 的容器的日志。在运行代码之前，您需要修改代码以更改硬编码的容器 ID，以打印对应容器的日志。








<div
  class="tabs"
  
    
      x-data="{ selected: 'Go' }"
    
    @tab-select.window="$event.detail.group === 'lang' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Go' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Go'})"
        
      >
        Go
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Python'})"
        
      >
        Python
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'HTTP' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'HTTP'})"
        
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
        x-data="{ code: 'cGFja2FnZSBtYWluCgppbXBvcnQgKAoJImNvbnRleHQiCgkiaW8iCgkib3MiCgoJImdpdGh1Yi5jb20vbW9ieS9tb2J5L2NsaWVudCIKKQoKZnVuYyBtYWluKCkgewoJY3R4IDo9IGNvbnRleHQuQmFja2dyb3VuZCgpCglhcGlDbGllbnQsIGVyciA6PSBjbGllbnQuTmV3KGNsaWVudC5Gcm9tRW52KQoJaWYgZXJyICE9IG5pbCB7CgkJcGFuaWMoZXJyKQoJfQoJZGVmZXIgYXBpQ2xpZW50LkNsb3NlKCkKCglvcHRpb25zIDo9IGNsaWVudC5Db250YWluZXJMb2dzT3B0aW9uc3tTaG93U3Rkb3V0OiB0cnVlfQoJLy8g5bCG5q2kIElEIOabv&#43;aNouS4uuWunumZheWtmOWcqOeahOWuueWZqAoJb3V0LCBlcnIgOj0gYXBpQ2xpZW50LkNvbnRhaW5lckxvZ3MoY3R4LCAiZjEwNjRhOGE0YzgyIiwgb3B0aW9ucykKCWlmIGVyciAhPSBuaWwgewoJCXBhbmljKGVycikKCX0KCglpby5Db3B5KG9zLlN0ZG91dCwgb3V0KQp9', copying: false }"
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
</span></span><span class="line"><span class="cl">	<span class="nx">options</span> <span class="o">:=</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerLogsOptions</span><span class="p">{</span><span class="nx">ShowStdout</span><span class="p">:</span> <span class="kc">true</span><span class="p">}</span>
</span></span><span class="line"><span class="cl">	<span class="c1">// 将此 ID 替换为实际存在的容器</span>
</span></span><span class="line"><span class="cl">	<span class="nx">out</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerLogs</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="s">&#34;f1064a8a4c82&#34;</span><span class="p">,</span> <span class="nx">options</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">io</span><span class="p">.</span><span class="nf">Copy</span><span class="p">(</span><span class="nx">os</span><span class="p">.</span><span class="nx">Stdout</span><span class="p">,</span> <span class="nx">out</span><span class="p">)</span>
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
        x-data="{ code: 'aW1wb3J0IGRvY2tlcgpjbGllbnQgPSBkb2NrZXIuZnJvbV9lbnYoKQpjb250YWluZXIgPSBjbGllbnQuY29udGFpbmVycy5nZXQoJ2YxMDY0YThhNGM4MicpCnByaW50KGNvbnRhaW5lci5sb2dzKCkp', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="n">container</span> <span class="o">=</span> <span class="n">client</span><span class="o">.</span><span class="n">containers</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;f1064a8a4c82&#39;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="nb">print</span><span class="p">(</span><span class="n">container</span><span class="o">.</span><span class="n">logs</span><span class="p">())</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBjdXJsIC0tdW5peC1zb2NrZXQgL3Zhci9ydW4vZG9ja2VyLnNvY2sgImh0dHA6Ly9sb2NhbGhvc3QvdjEuNTIvY29udGFpbmVycy9jYTVmNTVjZGIvbG9ncz9zdGRvdXQ9MSIKUmV0aWN1bGF0aW5nIHNwbGluZSAxLi4uClJldGljdWxhdGluZyBzcGxpbmUgMi4uLgpSZXRpY3VsYXRpbmcgc3BsaW5lIDMuLi4KUmV0aWN1bGF0aW5nIHNwbGluZSA0Li4uClJldGljdWxhdGluZyBzcGxpbmUgNS4uLg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> curl --unix-socket /var/run/docker.sock <span class="s2">&#34;http://localhost/v1.52/containers/ca5f55cdb/logs?stdout=1&#34;</span>
</span></span><span class="line"><span class="cl"><span class="go">Reticulating spline 1...
</span></span></span><span class="line"><span class="cl"><span class="go">Reticulating spline 2...
</span></span></span><span class="line"><span class="cl"><span class="go">Reticulating spline 3...
</span></span></span><span class="line"><span class="cl"><span class="go">Reticulating spline 4...
</span></span></span><span class="line"><span class="cl"><span class="go">Reticulating spline 5...
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 列出所有镜像

列出引擎上的镜像，类似于 `docker image ls`：








<div
  class="tabs"
  
    
      x-data="{ selected: 'Go' }"
    
    @tab-select.window="$event.detail.group === 'lang' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Go' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Go'})"
        
      >
        Go
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Python'})"
        
      >
        Python
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'HTTP' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'HTTP'})"
        
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
        x-data="{ code: 'cGFja2FnZSBtYWluCgppbXBvcnQgKAoJImNvbnRleHQiCgkiZm10IgoKCSJnaXRodWIuY29tL21vYnkvbW9ieS9jbGllbnQiCikKCmZ1bmMgbWFpbigpIHsKCWN0eCA6PSBjb250ZXh0LkJhY2tncm91bmQoKQoJYXBpQ2xpZW50LCBlcnIgOj0gY2xpZW50Lk5ldyhjbGllbnQuRnJvbUVudikKCWlmIGVyciAhPSBuaWwgewoJCXBhbmljKGVycikKCX0KCWRlZmVyIGFwaUNsaWVudC5DbG9zZSgpCgoJaW1hZ2VzLCBlcnIgOj0gYXBpQ2xpZW50LkltYWdlTGlzdChjdHgsIGNsaWVudC5JbWFnZUxpc3RPcHRpb25ze30pCglpZiBlcnIgIT0gbmlsIHsKCQlwYW5pYyhlcnIpCgl9CgoJZm9yIF8sIGltYWdlIDo9IHJhbmdlIGltYWdlcy5JdGVtcyB7CgkJZm10LlByaW50bG4oaW1hZ2UuSUQpCgl9Cn0=', copying: false }"
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
</span></span><span class="line"><span class="cl">	<span class="s">&#34;fmt&#34;</span>
</span></span><span class="line"><span class="cl">
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
</span></span><span class="line"><span class="cl">	<span class="nx">images</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ImageList</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ImageListOptions</span><span class="p">{})</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="k">for</span> <span class="nx">_</span><span class="p">,</span> <span class="nx">image</span> <span class="o">:=</span> <span class="k">range</span> <span class="nx">images</span><span class="p">.</span><span class="nx">Items</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nx">fmt</span><span class="p">.</span><span class="nf">Println</span><span class="p">(</span><span class="nx">image</span><span class="p">.</span><span class="nx">ID</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
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
        x-data="{ code: 'aW1wb3J0IGRvY2tlcgpjbGllbnQgPSBkb2NrZXIuZnJvbV9lbnYoKQpmb3IgaW1hZ2UgaW4gY2xpZW50LmltYWdlcy5saXN0KCk6CiAgcHJpbnQoaW1hZ2UuaWQp', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="k">for</span> <span class="n">image</span> <span class="ow">in</span> <span class="n">client</span><span class="o">.</span><span class="n">images</span><span class="o">.</span><span class="n">list</span><span class="p">():</span>
</span></span><span class="line"><span class="cl">  <span class="nb">print</span><span class="p">(</span><span class="n">image</span><span class="o">.</span><span class="n">id</span><span class="p">)</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBjdXJsIC0tdW5peC1zb2NrZXQgL3Zhci9ydW4vZG9ja2VyLnNvY2sgaHR0cDovL2xvY2FsaG9zdC92MS41Mi9pbWFnZXMvanNvbgpbewogICJJZCI6InNoYTI1NjozMWQ5YTMxZTFkZDgwMzQ3MGM1YTE1MWI4OTE5ZWYxOTg4YWMzZWZkNDQyODFhYzU5ZDQzYWQ2MjNmMjc1ZGNkIiwKICAiUGFyZW50SWQiOiJzaGEyNTY6ZWU0NjAzMjYwZGFhZmUxYThjMmYzYjc4ZmQ3NjA5MjI5MThhYjI0NDFjYmIyODUzZWQ1YzQzOWU1OWM1MmY5NiIsCiAgLi4uCn1d', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> curl --unix-socket /var/run/docker.sock http://localhost/v1.52/images/json
</span></span><span class="line"><span class="cl"><span class="go">[{
</span></span></span><span class="line"><span class="cl"><span class="go">  &#34;Id&#34;:&#34;sha256:31d9a31e1dd803470c5a151b8919ef1988ac3efd44281ac59d43ad623f275dcd&#34;,
</span></span></span><span class="line"><span class="cl"><span class="go">  &#34;ParentId&#34;:&#34;sha256:ee4603260daafe1a8c2f3b78fd760922918ab2441cbb2853ed5c439e59c52f96&#34;,
</span></span></span><span class="line"><span class="cl"><span class="go">  ...
</span></span></span><span class="line"><span class="cl"><span class="go">}]
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 拉取镜像

拉取镜像，类似于 `docker pull`：








<div
  class="tabs"
  
    
      x-data="{ selected: 'Go' }"
    
    @tab-select.window="$event.detail.group === 'lang' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Go' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Go'})"
        
      >
        Go
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Python'})"
        
      >
        Python
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'HTTP' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'HTTP'})"
        
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
        x-data="{ code: 'cGFja2FnZSBtYWluCgppbXBvcnQgKAoJImNvbnRleHQiCgkiaW8iCgkib3MiCgoJImdpdGh1Yi5jb20vbW9ieS9tb2J5L2NsaWVudCIKKQoKZnVuYyBtYWluKCkgewoJY3R4IDo9IGNvbnRleHQuQmFja2dyb3VuZCgpCglhcGlDbGllbnQsIGVyciA6PSBjbGllbnQuTmV3KGNsaWVudC5Gcm9tRW52KQoJaWYgZXJyICE9IG5pbCB7CgkJcGFuaWMoZXJyKQoJfQoJZGVmZXIgYXBpQ2xpZW50LkNsb3NlKCkKCglvdXQsIGVyciA6PSBhcGlDbGllbnQuSW1hZ2VQdWxsKGN0eCwgImFscGluZSIsIGNsaWVudC5JbWFnZVB1bGxPcHRpb25ze30pCglpZiBlcnIgIT0gbmlsIHsKCQlwYW5pYyhlcnIpCgl9CgoJZGVmZXIgb3V0LkNsb3NlKCkKCglpby5Db3B5KG9zLlN0ZG91dCwgb3V0KQp9', copying: false }"
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
</span></span><span class="line"><span class="cl">	<span class="nx">out</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ImagePull</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="s">&#34;alpine&#34;</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ImagePullOptions</span><span class="p">{})</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="k">defer</span> <span class="nx">out</span><span class="p">.</span><span class="nf">Close</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">io</span><span class="p">.</span><span class="nf">Copy</span><span class="p">(</span><span class="nx">os</span><span class="p">.</span><span class="nx">Stdout</span><span class="p">,</span> <span class="nx">out</span><span class="p">)</span>
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
        x-data="{ code: 'aW1wb3J0IGRvY2tlcgpjbGllbnQgPSBkb2NrZXIuZnJvbV9lbnYoKQppbWFnZSA9IGNsaWVudC5pbWFnZXMucHVsbCgiYWxwaW5lIikKcHJpbnQoaW1hZ2UuaWQp', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="n">image</span> <span class="o">=</span> <span class="n">client</span><span class="o">.</span><span class="n">images</span><span class="o">.</span><span class="n">pull</span><span class="p">(</span><span class="s2">&#34;alpine&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="nb">print</span><span class="p">(</span><span class="n">image</span><span class="o">.</span><span class="n">id</span><span class="p">)</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBjdXJsIC0tdW5peC1zb2NrZXQgL3Zhci9ydW4vZG9ja2VyLnNvY2sgXAogIC1YIFBPU1QgImh0dHA6Ly9sb2NhbGhvc3QvdjEuNTIvaW1hZ2VzL2NyZWF0ZT9mcm9tSW1hZ2U9YWxwaW5lIgp7InN0YXR1cyI6IlB1bGxpbmcgZnJvbSBsaWJyYXJ5L2FscGluZSIsImlkIjoiMy4xIn0KeyJzdGF0dXMiOiJQdWxsaW5nIGZzIGxheWVyIiwicHJvZ3Jlc3NEZXRhaWwiOnt9LCJpZCI6IjhmMTM3MDM1MDlmNyJ9Cnsic3RhdHVzIjoiRG93bmxvYWRpbmciLCJwcm9ncmVzc0RldGFpbCI6eyJjdXJyZW50IjozMjc2OCwidG90YWwiOjIyNDQwMjd9LCJwcm9ncmVzcyI6IltcdTAwM2UgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIF0gMzIuNzcga0IvMi4yNDQgTUIiLCJpZCI6IjhmMTM3MDM1MDlmNyJ9Ci4uLg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> curl --unix-socket /var/run/docker.sock <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span><span class="go">  -X POST &#34;http://localhost/v1.52/images/create?fromImage=alpine&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">{&#34;status&#34;:&#34;Pulling from library/alpine&#34;,&#34;id&#34;:&#34;3.1&#34;}
</span></span></span><span class="line"><span class="cl"><span class="go">{&#34;status&#34;:&#34;Pulling fs layer&#34;,&#34;progressDetail&#34;:{},&#34;id&#34;:&#34;8f13703509f7&#34;}
</span></span></span><span class="line"><span class="cl"><span class="go">{&#34;status&#34;:&#34;Downloading&#34;,&#34;progressDetail&#34;:{&#34;current&#34;:32768,&#34;total&#34;:2244027},&#34;progress&#34;:&#34;[\u003e                                                  ] 32.77 kB/2.244 MB&#34;,&#34;id&#34;:&#34;8f13703509f7&#34;}
</span></span></span><span class="line"><span class="cl"><span class="go">...
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 使用身份验证拉取镜像

使用身份验证拉取镜像，类似于 `docker pull`：

> [!NOTE]
>
> 凭据以明文形式发送。Docker 的官方注册表使用 HTTPS。私有注册表也应配置为使用 HTTPS。








<div
  class="tabs"
  
    
      x-data="{ selected: 'Go' }"
    
    @tab-select.window="$event.detail.group === 'lang' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Go' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Go'})"
        
      >
        Go
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Python'})"
        
      >
        Python
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'HTTP' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'HTTP'})"
        
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
        x-data="{ code: 'cGFja2FnZSBtYWluCgppbXBvcnQgKAoJImNvbnRleHQiCgkiZW5jb2RpbmcvYmFzZTY0IgoJImVuY29kaW5nL2pzb24iCgkiaW8iCgkib3MiCgoJImdpdGh1Yi5jb20vbW9ieS9tb2J5L2FwaS90eXBlcy9yZWdpc3RyeSIKCSJnaXRodWIuY29tL21vYnkvbW9ieS9jbGllbnQiCikKCmZ1bmMgbWFpbigpIHsKCWN0eCA6PSBjb250ZXh0LkJhY2tncm91bmQoKQoJYXBpQ2xpZW50LCBlcnIgOj0gY2xpZW50Lk5ldyhjbGllbnQuRnJvbUVudikKCWlmIGVyciAhPSBuaWwgewoJCXBhbmljKGVycikKCX0KCWRlZmVyIGFwaUNsaWVudC5DbG9zZSgpCgoJYXV0aENvbmZpZyA6PSByZWdpc3RyeS5BdXRoQ29uZmlnewoJCVVzZXJuYW1lOiAidXNlcm5hbWUiLAoJCVBhc3N3b3JkOiAicGFzc3dvcmQiLAoJfQoJZW5jb2RlZEpTT04sIGVyciA6PSBqc29uLk1hcnNoYWwoYXV0aENvbmZpZykKCWlmIGVyciAhPSBuaWwgewoJCXBhbmljKGVycikKCX0KCWF1dGhTdHIgOj0gYmFzZTY0LlVSTEVuY29kaW5nLkVuY29kZVRvU3RyaW5nKGVuY29kZWRKU09OKQoKCW91dCwgZXJyIDo9IGFwaUNsaWVudC5JbWFnZVB1bGwoY3R4LCAiYWxwaW5lIiwgY2xpZW50LkltYWdlUHVsbE9wdGlvbnN7UmVnaXN0cnlBdXRoOiBhdXRoU3RyfSkKCWlmIGVyciAhPSBuaWwgewoJCXBhbmljKGVycikKCX0KCglkZWZlciBvdXQuQ2xvc2UoKQoJaW8uQ29weShvcy5TdGRvdXQsIG91dCkKfQ==', copying: false }"
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
</span></span><span class="line"><span class="cl">	<span class="s">&#34;encoding/base64&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;encoding/json&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;io&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;os&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="s">&#34;github.com/moby/moby/api/types/registry&#34;</span>
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
</span></span><span class="line"><span class="cl">	<span class="nx">authConfig</span> <span class="o">:=</span> <span class="nx">registry</span><span class="p">.</span><span class="nx">AuthConfig</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nx">Username</span><span class="p">:</span> <span class="s">&#34;username&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">		<span class="nx">Password</span><span class="p">:</span> <span class="s">&#34;password&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">	<span class="nx">encodedJSON</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">json</span><span class="p">.</span><span class="nf">Marshal</span><span class="p">(</span><span class="nx">authConfig</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">	<span class="nx">authStr</span> <span class="o">:=</span> <span class="nx">base64</span><span class="p">.</span><span class="nx">URLEncoding</span><span class="p">.</span><span class="nf">EncodeToString</span><span class="p">(</span><span class="nx">encodedJSON</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">out</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ImagePull</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="s">&#34;alpine&#34;</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ImagePullOptions</span><span class="p">{</span><span class="nx">RegistryAuth</span><span class="p">:</span> <span class="nx">authStr</span><span class="p">})</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="k">defer</span> <span class="nx">out</span><span class="p">.</span><span class="nf">Close</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">	<span class="nx">io</span><span class="p">.</span><span class="nf">Copy</span><span class="p">(</span><span class="nx">os</span><span class="p">.</span><span class="nx">Stdout</span><span class="p">,</span> <span class="nx">out</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
      >
        <p>Python SDK 从 
  <a class="link" href="/reference/cli/docker/login/#credential-stores">凭据存储</a> 文件中检索身份验证信息，并与 <a class="link" href="https://github.com/docker/docker-credential-helpers" rel="noopener">凭据助手</a> 集成。可以覆盖这些凭据，但这超出了本示例指南的范围。使用 <code>docker login</code> 后，Python SDK 会自动使用这些凭据。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0IGRvY2tlcgpjbGllbnQgPSBkb2NrZXIuZnJvbV9lbnYoKQppbWFnZSA9IGNsaWVudC5pbWFnZXMucHVsbCgiYWxwaW5lIikKcHJpbnQoaW1hZ2UuaWQp', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="n">image</span> <span class="o">=</span> <span class="n">client</span><span class="o">.</span><span class="n">images</span><span class="o">.</span><span class="n">pull</span><span class="p">(</span><span class="s2">&#34;alpine&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="nb">print</span><span class="p">(</span><span class="n">image</span><span class="o">.</span><span class="n">id</span><span class="p">)</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'HTTP' && 'hidden'"
      >
        <p>此示例将凭据保留在 shell 的历史记录中，因此请将其视为一种简单的实现方式。凭据以 Base-64 编码的 JSON 结构传递。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBKU09OPSQoZWNobyAneyJ1c2VybmFtZSI6ICJzdHJpbmciLCAicGFzc3dvcmQiOiAic3RyaW5nIiwgInNlcnZlcmFkZHJlc3MiOiAic3RyaW5nIn0nIHwgYmFzZTY0KQoKJCBjdXJsIC0tdW5peC1zb2NrZXQgL3Zhci9ydW4vZG9ja2VyLnNvY2sgXAogIC1IICJDb250ZW50LVR5cGU6IGFwcGxpY2F0aW9uL3RhciIKICAtWCBQT1NUICJodHRwOi8vbG9jYWxob3N0L3YxLjUyL2ltYWdlcy9jcmVhdGU/ZnJvbUltYWdlPWFscGluZSIKICAtSCAiWC1SZWdpc3RyeS1BdXRoIgogIC1kICIkSlNPTiIKeyJzdGF0dXMiOiJQdWxsaW5nIGZyb20gbGlicmFyeS9hbHBpbmUiLCJpZCI6IjMuMSJ9Cnsic3RhdHVzIjoiUHVsbGluZyBmcyBsYXllciIsInByb2dyZXNzRGV0YWlsIjp7fSwiaWQiOiI4ZjEzNzAzNTA5ZjcifQp7InN0YXR1cyI6IkRvd25sb2FkaW5nIiwicHJvZ3Jlc3NEZXRhaWwiOnsiY3VycmVudCI6MzI3NjgsInRvdGFsIjoyMjQ0MDI3fSwicHJvZ3Jlc3MiOiJbXHUwMDNlICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBdIDMyLjc3IGtCLzIuMjQ0IE1CIiwiaWQiOiI4ZjEzNzAzNTA5ZjcifQouLi4=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> <span class="nv">JSON</span><span class="o">=</span><span class="k">$(</span><span class="nb">echo</span> <span class="s1">&#39;{&#34;username&#34;: &#34;string&#34;, &#34;password&#34;: &#34;string&#34;, &#34;serveraddress&#34;: &#34;string&#34;}&#39;</span> <span class="p">|</span> base64<span class="k">)</span>
</span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="gp">$</span> curl --unix-socket /var/run/docker.sock <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span><span class="go">  -H &#34;Content-Type: application/tar&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">  -X POST &#34;http://localhost/v1.52/images/create?fromImage=alpine&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">  -H &#34;X-Registry-Auth&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">  -d &#34;$JSON&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">{&#34;status&#34;:&#34;Pulling from library/alpine&#34;,&#34;id&#34;:&#34;3.1&#34;}
</span></span></span><span class="line"><span class="cl"><span class="go">{&#34;status&#34;:&#34;Pulling fs layer&#34;,&#34;progressDetail&#34;:{},&#34;id&#34;:&#34;8f13703509f7&#34;}
</span></span></span><span class="line"><span class="cl"><span class="go">{&#34;status&#34;:&#34;Downloading&#34;,&#34;progressDetail&#34;:{&#34;current&#34;:32768,&#34;total&#34;:2244027},&#34;progress&#34;:&#34;[\u003e                                                  ] 32.77 kB/2.244 MB&#34;,&#34;id&#34;:&#34;8f13703509f7&#34;}
</span></span></span><span class="line"><span class="cl"><span class="go">...
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 提交容器

提交容器以从其内容创建镜像：








<div
  class="tabs"
  
    
      x-data="{ selected: 'Go' }"
    
    @tab-select.window="$event.detail.group === 'lang' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Go' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Go'})"
        
      >
        Go
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Python'})"
        
      >
        Python
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'HTTP' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'HTTP'})"
        
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
        x-data="{ code: 'cGFja2FnZSBtYWluCgppbXBvcnQgKAoJImNvbnRleHQiCgkiZm10IgoKCSJnaXRodWIuY29tL21vYnkvbW9ieS9hcGkvdHlwZXMvY29udGFpbmVyIgoJImdpdGh1Yi5jb20vbW9ieS9tb2J5L2NsaWVudCIKKQoKZnVuYyBtYWluKCkgewoJY3R4IDo9IGNvbnRleHQuQmFja2dyb3VuZCgpCglhcGlDbGllbnQsIGVyciA6PSBjbGllbnQuTmV3KGNsaWVudC5Gcm9tRW52KQoJaWYgZXJyICE9IG5pbCB7CgkJcGFuaWMoZXJyKQoJfQoJZGVmZXIgYXBpQ2xpZW50LkNsb3NlKCkKCgljcmVhdGVSZXNwLCBlcnIgOj0gYXBpQ2xpZW50LkNvbnRhaW5lckNyZWF0ZShjdHgsIGNsaWVudC5Db250YWluZXJDcmVhdGVPcHRpb25zewoJCUNvbmZpZzogJmNvbnRhaW5lci5Db25maWd7CgkJCUNtZDogW11zdHJpbmd7InRvdWNoIiwgIi9oZWxsb3dvcmxkIn0sCgkJfSwKCQlJbWFnZTogImFscGluZSIsCgl9KQoJaWYgZXJyICE9IG5pbCB7CgkJcGFuaWMoZXJyKQoJfQoKCWlmIF8sIGVyciA6PSBhcGlDbGllbnQuQ29udGFpbmVyU3RhcnQoY3R4LCBjcmVhdGVSZXNwLklELCBjbGllbnQuQ29udGFpbmVyU3RhcnRPcHRpb25ze30pOyBlcnIgIT0gbmlsIHsKCQlwYW5pYyhlcnIpCgl9CgoJd2FpdCA6PSBhcGlDbGllbnQuQ29udGFpbmVyV2FpdChjdHgsIGNyZWF0ZVJlc3AuSUQsIGNsaWVudC5Db250YWluZXJXYWl0T3B0aW9uc3t9KQoJc2VsZWN0IHsKCWNhc2UgZXJyIDo9IDwtd2FpdC5FcnJvcjoKCQlpZiBlcnIgIT0gbmlsIHsKCQkJcGFuaWMoZXJyKQoJCX0KCWNhc2UgPC13YWl0LlJlc3VsdDoKCX0KCgljb21taXRSZXNwLCBlcnIgOj0gYXBpQ2xpZW50LkNvbnRhaW5lckNvbW1pdChjdHgsIGNyZWF0ZVJlc3AuSUQsIGNsaWVudC5Db250YWluZXJDb21taXRPcHRpb25ze1JlZmVyZW5jZTogImhlbGxvd29ybGQifSkKCWlmIGVyciAhPSBuaWwgewoJCXBhbmljKGVycikKCX0KCglmbXQuUHJpbnRsbihjb21taXRSZXNwLklEKQp9', copying: false }"
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
</span></span><span class="line"><span class="cl">	<span class="s">&#34;fmt&#34;</span>
</span></span><span class="line"><span class="cl">
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
</span></span><span class="line"><span class="cl">	<span class="nx">createResp</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerCreate</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerCreateOptions</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nx">Config</span><span class="p">:</span> <span class="o">&amp;</span><span class="nx">container</span><span class="p">.</span><span class="nx">Config</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">			<span class="nx">Cmd</span><span class="p">:</span> <span class="p">[]</span><span class="kt">string</span><span class="p">{</span><span class="s">&#34;touch&#34;</span><span class="p">,</span> <span class="s">&#34;/helloworld&#34;</span><span class="p">},</span>
</span></span><span class="line"><span class="cl">		<span class="p">},</span>
</span></span><span class="line"><span class="cl">		<span class="nx">Image</span><span class="p">:</span> <span class="s">&#34;alpine&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">	<span class="p">})</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">_</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerStart</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">createResp</span><span class="p">.</span><span class="nx">ID</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerStartOptions</span><span class="p">{});</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">wait</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerWait</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">createResp</span><span class="p">.</span><span class="nx">ID</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerWaitOptions</span><span class="p">{})</span>
</span></span><span class="line"><span class="cl">	<span class="k">select</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">	<span class="k">case</span> <span class="nx">err</span> <span class="o">:=</span> <span class="o">&lt;-</span><span class="nx">wait</span><span class="p">.</span><span class="nx">Error</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">		<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">			<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">		<span class="p">}</span>
</span></span><span class="line"><span class="cl">	<span class="k">case</span> <span class="o">&lt;-</span><span class="nx">wait</span><span class="p">.</span><span class="nx">Result</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">commitResp</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nx">apiClient</span><span class="p">.</span><span class="nf">ContainerCommit</span><span class="p">(</span><span class="nx">ctx</span><span class="p">,</span> <span class="nx">createResp</span><span class="p">.</span><span class="nx">ID</span><span class="p">,</span> <span class="nx">client</span><span class="p">.</span><span class="nx">ContainerCommitOptions</span><span class="p">{</span><span class="nx">Reference</span><span class="p">:</span> <span class="s">&#34;helloworld&#34;</span><span class="p">})</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">fmt</span><span class="p">.</span><span class="nf">Println</span><span class="p">(</span><span class="nx">commitResp</span><span class="p">.</span><span class="nx">ID</span><span class="p">)</span>
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
        x-data="{ code: 'aW1wb3J0IGRvY2tlcgpjbGllbnQgPSBkb2NrZXIuZnJvbV9lbnYoKQpjb250YWluZXIgPSBjbGllbnQuY29udGFpbmVycy5ydW4oImFscGluZSIsIFsidG91Y2giLCAiL2hlbGxvd29ybGQiXSwgZGV0YWNoPVRydWUpCmNvbnRhaW5lci53YWl0KCkKaW1hZ2UgPSBjb250YWluZXIuY29tbWl0KCJoZWxsb3dvcmxkIikKcHJpbnQoaW1hZ2UuaWQp', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="n">container</span> <span class="o">=</span> <span class="n">client</span><span class="o">.</span><span class="n">containers</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="s2">&#34;alpine&#34;</span><span class="p">,</span> <span class="p">[</span><span class="s2">&#34;touch&#34;</span><span class="p">,</span> <span class="s2">&#34;/helloworld&#34;</span><span class="p">],</span> <span class="n">detach</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="n">container</span><span class="o">.</span><span class="n">wait</span><span class="p">()</span>
</span></span><span class="line"><span class="cl"><span class="n">image</span> <span class="o">=</span> <span class="n">container</span><span class="o">.</span><span class="n">commit</span><span class="p">(</span><span class="s2">&#34;helloworld&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="nb">print</span><span class="p">(</span><span class="n">image</span><span class="o">.</span><span class="n">id</span><span class="p">)</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kIGFscGluZSB0b3VjaCAvaGVsbG93b3JsZAowODg4MjY5YTlkNTg0ZjBmYThmYzk2YjNjMGQ4ZDU3OTY5Y2VlYTNhNjRhY2Y0N2NkMzRlZWJiNDc0NGRiYzUyCiQgY3VybCAtLXVuaXgtc29ja2V0IC92YXIvcnVuL2RvY2tlci5zb2NrXAogIC1YIFBPU1QgImh0dHA6Ly9sb2NhbGhvc3QvdjEuNTIvY29tbWl0P2NvbnRhaW5lcj0wODg4MjY5YTlkJnJlcG89aGVsbG93b3JsZCIKeyJJZCI6InNoYTI1Njo2Yzg2YTVjZDRiODdmMjc3MTY0OGNlNjE5ZTMxOWYzZTUwODM5NGI1YmZjMmNkYmQyZDYwZjU5ZDUyYWNkYTZjIn0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -d alpine touch /helloworld
</span></span><span class="line"><span class="cl"><span class="go">0888269a9d584f0fa8fc96b3c0d8d57969ceea3a64acf47cd34eebb4744dbc52
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="gp">$</span> curl --unix-socket /var/run/docker.sock<span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span><span class="go">  -X POST &#34;http://localhost/v1.52/commit?container=0888269a9d&amp;repo=helloworld&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">{&#34;Id&#34;:&#34;sha256:6c86a5cd4b87f2771648ce619e319f3e508394b5bfc2cdbd2d60f59d52acda6c&#34;}
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>

