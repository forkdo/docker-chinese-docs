# 调用主机二进制文件

在某些情况下，您的扩展可能需要调用主机上的某些命令。例如，您可能希望调用云提供商的 CLI 来创建新资源，或调用扩展提供的工具的 CLI，甚至运行主机上的 shell 脚本。

您可以通过使用扩展 SDK 在容器中执行 CLI 来实现这一点。但是，如果 CLI 在容器中运行，则它需要访问主机的文件系统，这既不容易也不快速。

本页介绍了如何运行作为扩展的一部分并部署到主机上的可执行文件（二进制文件、shell 脚本）。由于扩展可以在多个平台上运行，这意味着您需要为所有希望支持的平台提供可执行文件。

了解更多关于扩展的[架构](../architecture/_index.md)。

> [!NOTE]
>
> 请注意，扩展以用户访问权限运行，此 API 不限于扩展元数据中[主机部分](../architecture/metadata.md#host-section)列出的二进制文件（某些扩展可能在用户交互期间安装软件，并调用新安装的二进制文件，即使未在扩展元数据中列出）。

在此示例中，CLI 是一个简单的 `Hello world` 脚本，必须使用参数调用并返回字符串。

## 将可执行文件添加到扩展中








<div
  class="tabs"
  
    x-data="{ selected: 'Mac-%E5%92%8C-Linux' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Mac-%E5%92%8C-Linux' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Mac-%E5%92%8C-Linux'"
        
      >
        Mac 和 Linux
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Windows' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Windows'"
        
      >
        Windows
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Mac-%E5%92%8C-Linux' && 'hidden'"
      >
        <p>为 macOS 和 Linux 创建一个 <code>bash</code> 脚本，文件名为 <code>binaries/unix/hello.sh</code>，内容如下：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyEvYmluL3NoCmVjaG8gIkhlbGxvLCAkMSEi', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl"><span class="cp">#!/bin/sh
</span></span></span><span class="line"><span class="cl"><span class="cp"></span><span class="nb">echo</span> <span class="s2">&#34;Hello, </span><span class="nv">$1</span><span class="s2">!&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Windows' && 'hidden'"
      >
        <p>为 Windows 创建另一个 <code>批处理脚本</code>，文件名为 <code>binaries/windows/hello.cmd</code>，内容如下：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'QGVjaG8gb2ZmCmVjaG8gIkhlbGxvLCAlMSEi', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">@echo off
</span></span><span class="line"><span class="cl"><span class="nb">echo</span> <span class="s2">&#34;Hello, %1!&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


然后更新 `Dockerfile`，将 `binaries` 文件夹复制到扩展的容器文件系统中，并使文件可执行。

```dockerfile
# 将二进制文件复制到正确的文件夹
COPY --chmod=0755 binaries/windows/hello.cmd /windows/hello.cmd
COPY --chmod=0755 binaries/unix/hello.sh /linux/hello.sh
COPY --chmod=0755 binaries/unix/hello.sh /darwin/hello.sh
```

## 从 UI 调用可执行文件

在您的扩展中，使用 Docker Desktop 客户端对象通过 `ddClient.extension.host.cli.exec()` 函数[调用扩展提供的主机上的 shell 脚本](../dev/api/backend.md#invoke-an-extension-binary-on-the-host)。
在此示例中，二进制文件返回一个字符串作为结果，通过 `result?.stdout` 获取，一旦扩展视图被渲染。








<div
  class="tabs"
  
    
      x-data="{ selected: 'React' }"
    
    @tab-select.window="$event.detail.group === 'framework' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'React' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'framework', name:
          'React'})"
        
      >
        React
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Vue' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'framework', name:
          'Vue'})"
        
      >
        Vue
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Angular' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'framework', name:
          'Angular'})"
        
      >
        Angular
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Svelte' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'framework', name:
          'Svelte'})"
        
      >
        Svelte
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'React' && 'hidden'"
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
        x-data="{ code: 'ZXhwb3J0IGZ1bmN0aW9uIEFwcCgpIHsKICBjb25zdCBkZENsaWVudCA9IGNyZWF0ZURvY2tlckRlc2t0b3BDbGllbnQoKTsKICBjb25zdCBbaGVsbG8sIHNldEhlbGxvXSA9IHVzZVN0YXRlKCIiKTsKCiAgdXNlRWZmZWN0KCgpID0&#43;IHsKICAgIGNvbnN0IHJ1biA9IGFzeW5jICgpID0&#43;IHsKICAgICAgbGV0IGJpbmFyeSA9ICJoZWxsby5zaCI7CiAgICAgIGlmIChkZENsaWVudC5ob3N0LnBsYXRmb3JtID09PSAnd2luMzInKSB7CiAgICAgICAgYmluYXJ5ID0gImhlbGxvLmNtZCI7CiAgICAgIH0KCiAgICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IGRkQ2xpZW50LmV4dGVuc2lvbi5ob3N0Py5jbGkuZXhlYyhiaW5hcnksIFsid29ybGQiXSk7CiAgICAgIHNldEhlbGxvKHJlc3VsdD8uc3Rkb3V0KTsKCiAgICB9OwogICAgcnVuKCk7CiAgfSwgW2RkQ2xpZW50XSk7CiAgICAKICByZXR1cm4gKAogICAgPGRpdj4KICAgICAge2hlbGxvfQogICAgPC9kaXY&#43;CiAgKTsKfQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="kr">export</span> <span class="kd">function</span> <span class="nx">App() {</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">ddClient</span> <span class="o">=</span> <span class="nx">createDockerDesktopClient</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="p">[</span><span class="nx">hello</span><span class="p">,</span> <span class="nx">setHello</span><span class="p">]</span> <span class="o">=</span> <span class="nx">useState</span><span class="p">(</span><span class="s2">&#34;&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">useEffect</span><span class="p">(()</span> <span class="o">=&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="kr">const</span> <span class="nx">run</span> <span class="o">=</span> <span class="kr">async</span> <span class="p">()</span> <span class="o">=&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="kd">let</span> <span class="nx">binary</span> <span class="o">=</span> <span class="s2">&#34;hello.sh&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">      <span class="k">if</span> <span class="p">(</span><span class="nx">ddClient</span><span class="p">.</span><span class="nx">host</span><span class="p">.</span><span class="nx">platform</span> <span class="o">===</span> <span class="s1">&#39;win32&#39;</span><span class="p">)</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">binary</span> <span class="o">=</span> <span class="s2">&#34;hello.cmd&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">      <span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">      <span class="kr">const</span> <span class="nx">result</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">ddClient</span><span class="p">.</span><span class="nx">extension</span><span class="p">.</span><span class="nx">host</span><span class="o">?</span><span class="p">.</span><span class="nx">cli</span><span class="p">.</span><span class="nx">exec</span><span class="p">(</span><span class="nx">binary</span><span class="p">,</span> <span class="p">[</span><span class="s2">&#34;world&#34;</span><span class="p">]);</span>
</span></span><span class="line"><span class="cl">      <span class="nx">setHello</span><span class="p">(</span><span class="nx">result</span><span class="o">?</span><span class="p">.</span><span class="nx">stdout</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="p">};</span>
</span></span><span class="line"><span class="cl">    <span class="nx">run</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="p">},</span> <span class="p">[</span><span class="nx">ddClient</span><span class="p">]);</span>
</span></span><span class="line"><span class="cl">    
</span></span><span class="line"><span class="cl">  <span class="k">return</span> <span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="p">&lt;</span><span class="nt">div</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">      <span class="p">{</span><span class="nx">hello</span><span class="p">}</span>
</span></span><span class="line"><span class="cl">    <span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Vue' && 'hidden'"
      >
        

  

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
      <p>我们还没有 Vue 的示例。<a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.1333218187=Vue" rel="noopener">填写表单</a>
并告诉我们您是否需要一个 Vue 的示例。</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Angular' && 'hidden'"
      >
        

  

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
      <p>我们还没有 Angular 的示例。<a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.1333218187=Angular" rel="noopener">填写表单</a>
并告诉我们您是否需要一个 Angular 的示例。</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Svelte' && 'hidden'"
      >
        

  

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
      <p>我们还没有 Svelte 的示例。<a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.1333218187=Svelte" rel="noopener">填写表单</a>
并告诉我们您是否需要一个 Svelte 的示例。</p>
    </div>
  </blockquote>


      </div>
    
  </div>
</div>


## 配置元数据文件

主机二进制文件必须在 `metadata.json` 文件中指定，以便 Docker Desktop 在安装扩展时将其复制到主机上。一旦扩展被卸载，复制的二进制文件也会被删除。

```json
{
  "vm": {
    ...
  },
  "ui": {
    ...
  },
  "host": {
    "binaries": [
      {
        "darwin": [
          {
            "path": "/darwin/hello.sh"
          }
        ],
        "linux": [
          {
            "path": "/linux/hello.sh"
          }
        ],
        "windows": [
          {
            "path": "/windows/hello.cmd"
          }
        ]
      }
    ]
  }
}
```

`path` 必须引用容器内二进制文件的路径。
