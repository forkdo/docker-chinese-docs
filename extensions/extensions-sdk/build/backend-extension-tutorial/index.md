# Add a backend to your extension

Your extension can ship a backend part with which the frontend can interact with. This page provides information on why and how to add a backend.

Before you start, make sure you have installed the latest version of [Docker Desktop](https://www.docker.com/products/docker-desktop/).

> Tip
>
> Check the [Quickstart guide](../quickstart.md) and `docker extension init <my-extension>`. They provide a better base for your extension as it's more up-to-date and related to your install of Docker Desktop.

## Why add a backend?

Thanks to the Docker Extensions SDK, most of the time you should be able to do what you need from the Docker CLI
directly from [the frontend](frontend-extension-tutorial.md#use-the-extension-apis-client).

Nonetheless, there are some cases where you might need to add a backend to your extension. So far, extension
builders have used the backend to:
- Store data in a local database and serve them back with a REST API.
- Store the extension state, for example when a button starts a long-running process, so that if you navigate away from the extension user interface and comes back, the frontend can pick up where it left off.

For more information about extension backends, see [Architecture](../architecture/_index.md#the-backend).

## Add a backend to the extension

If you created your extension using the `docker extension init` command, you already have a backend setup. Otherwise, you have to first create a `vm` directory that contains the code and updates the Dockerfile to
containerize it.

Here is the extension folder structure with a backend:

```bash
.
├── Dockerfile # (1)
├── Makefile
├── metadata.json
├── ui
    └── index.html
└── vm # (2)
    ├── go.mod
    └── main.go
```

1. Contains everything required to build the backend and copy it in the extension's container filesystem.
2. The source folder that contains the backend code of the extension.

Although you can start from an empty directory or from the `vm-ui extension` [sample](https://github.com/docker/extensions-sdk/tree/main/samples),
it is highly recommended that you start from the `docker extension init` command and change it to suit your needs.

> [!TIP]
>
> The `docker extension init` generates a Go backend. But you can still use it as a starting point for
> your own extension and use any other language like Node.js, Python, Java, .Net, or any other language and framework.

In this tutorial, the backend service simply exposes one route that returns a JSON payload that says "Hello".

```json
{ "Message": "Hello" }
```

> [!IMPORTANT]
>
> We recommend that, the frontend and the backend communicate through sockets, and named pipes on Windows, instead of
> HTTP. This prevents port collision with any other running application or container running
> on the host. Also, some Docker Desktop users are running in constrained environments where they
> can't open ports on their machines. When choosing the language and framework for your backend, make sure it
> supports sockets connection.








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
        :class="selected === 'Node' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Node'})"
        
      >
        Node
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
        :class="selected === 'Java' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Java'})"
        
      >
        Java
      </button>
    
      <button
        class="tab-item"
        :class="selected === '.NET' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          '.NET'})"
        
      >
        .NET
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
        x-data="{ code: 'cGFja2FnZSBtYWluCgppbXBvcnQgKAoJImZsYWciCgkibG9nIgoJIm5ldCIKCSJuZXQvaHR0cCIKCSJvcyIKCgkiZ2l0aHViLmNvbS9sYWJzdGFjay9lY2hvIgoJImdpdGh1Yi5jb20vc2lydXBzZW4vbG9ncnVzIgopCgpmdW5jIG1haW4oKSB7Cgl2YXIgc29ja2V0UGF0aCBzdHJpbmcKCWZsYWcuU3RyaW5nVmFyKCZzb2NrZXRQYXRoLCAic29ja2V0IiwgIi9ydW4vZ3Vlc3Qvdm9sdW1lcy1zZXJ2aWNlLnNvY2siLCAiVW5peCBkb21haW4gc29ja2V0IHRvIGxpc3RlbiBvbiIpCglmbGFnLlBhcnNlKCkKCglvcy5SZW1vdmVBbGwoc29ja2V0UGF0aCkKCglsb2dydXMuTmV3KCkuSW5mb2YoIlN0YXJ0aW5nIGxpc3RlbmluZyBvbiAlc1xuIiwgc29ja2V0UGF0aCkKCXJvdXRlciA6PSBlY2hvLk5ldygpCglyb3V0ZXIuSGlkZUJhbm5lciA9IHRydWUKCglzdGFydFVSTCA6PSAiIgoKCWxuLCBlcnIgOj0gbGlzdGVuKHNvY2tldFBhdGgpCglpZiBlcnIgIT0gbmlsIHsKCQlsb2cuRmF0YWwoZXJyKQoJfQoJcm91dGVyLkxpc3RlbmVyID0gbG4KCglyb3V0ZXIuR0VUKCIvaGVsbG8iLCBoZWxsbykKCglsb2cuRmF0YWwocm91dGVyLlN0YXJ0KHN0YXJ0VVJMKSkKfQoKZnVuYyBsaXN0ZW4ocGF0aCBzdHJpbmcpIChuZXQuTGlzdGVuZXIsIGVycm9yKSB7CglyZXR1cm4gbmV0Lkxpc3RlbigidW5peCIsIHBhdGgpCn0KCmZ1bmMgaGVsbG8oY3R4IGVjaG8uQ29udGV4dCkgZXJyb3IgewoJcmV0dXJuIGN0eC5KU09OKGh0dHAuU3RhdHVzT0ssIEhUVFBNZXNzYWdlQm9keXtNZXNzYWdlOiAiaGVsbG8gd29ybGQifSkKfQoKdHlwZSBIVFRQTWVzc2FnZUJvZHkgc3RydWN0IHsKCU1lc3NhZ2Ugc3RyaW5nCn0=', copying: false }"
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
</span></span><span class="line"><span class="cl">	<span class="s">&#34;flag&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;log&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;net&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;net/http&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;os&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="s">&#34;github.com/labstack/echo&#34;</span>
</span></span><span class="line"><span class="cl">	<span class="s">&#34;github.com/sirupsen/logrus&#34;</span>
</span></span><span class="line"><span class="cl"><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kd">func</span> <span class="nf">main</span><span class="p">()</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">	<span class="kd">var</span> <span class="nx">socketPath</span> <span class="kt">string</span>
</span></span><span class="line"><span class="cl">	<span class="nx">flag</span><span class="p">.</span><span class="nf">StringVar</span><span class="p">(</span><span class="o">&amp;</span><span class="nx">socketPath</span><span class="p">,</span> <span class="s">&#34;socket&#34;</span><span class="p">,</span> <span class="s">&#34;/run/guest/volumes-service.sock&#34;</span><span class="p">,</span> <span class="s">&#34;Unix domain socket to listen on&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="nx">flag</span><span class="p">.</span><span class="nf">Parse</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">os</span><span class="p">.</span><span class="nf">RemoveAll</span><span class="p">(</span><span class="nx">socketPath</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">logrus</span><span class="p">.</span><span class="nf">New</span><span class="p">().</span><span class="nf">Infof</span><span class="p">(</span><span class="s">&#34;Starting listening on %s\n&#34;</span><span class="p">,</span> <span class="nx">socketPath</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="nx">router</span> <span class="o">:=</span> <span class="nx">echo</span><span class="p">.</span><span class="nf">New</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">	<span class="nx">router</span><span class="p">.</span><span class="nx">HideBanner</span> <span class="p">=</span> <span class="kc">true</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">startURL</span> <span class="o">:=</span> <span class="s">&#34;&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">ln</span><span class="p">,</span> <span class="nx">err</span> <span class="o">:=</span> <span class="nf">listen</span><span class="p">(</span><span class="nx">socketPath</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="k">if</span> <span class="nx">err</span> <span class="o">!=</span> <span class="kc">nil</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">		<span class="nx">log</span><span class="p">.</span><span class="nf">Fatal</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">	<span class="p">}</span>
</span></span><span class="line"><span class="cl">	<span class="nx">router</span><span class="p">.</span><span class="nx">Listener</span> <span class="p">=</span> <span class="nx">ln</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">router</span><span class="p">.</span><span class="nf">GET</span><span class="p">(</span><span class="s">&#34;/hello&#34;</span><span class="p">,</span> <span class="nx">hello</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">	<span class="nx">log</span><span class="p">.</span><span class="nf">Fatal</span><span class="p">(</span><span class="nx">router</span><span class="p">.</span><span class="nf">Start</span><span class="p">(</span><span class="nx">startURL</span><span class="p">))</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kd">func</span> <span class="nf">listen</span><span class="p">(</span><span class="nx">path</span> <span class="kt">string</span><span class="p">)</span> <span class="p">(</span><span class="nx">net</span><span class="p">.</span><span class="nx">Listener</span><span class="p">,</span> <span class="kt">error</span><span class="p">)</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">	<span class="k">return</span> <span class="nx">net</span><span class="p">.</span><span class="nf">Listen</span><span class="p">(</span><span class="s">&#34;unix&#34;</span><span class="p">,</span> <span class="nx">path</span><span class="p">)</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kd">func</span> <span class="nf">hello</span><span class="p">(</span><span class="nx">ctx</span> <span class="nx">echo</span><span class="p">.</span><span class="nx">Context</span><span class="p">)</span> <span class="kt">error</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">	<span class="k">return</span> <span class="nx">ctx</span><span class="p">.</span><span class="nf">JSON</span><span class="p">(</span><span class="nx">http</span><span class="p">.</span><span class="nx">StatusOK</span><span class="p">,</span> <span class="nx">HTTPMessageBody</span><span class="p">{</span><span class="nx">Message</span><span class="p">:</span> <span class="s">&#34;hello world&#34;</span><span class="p">})</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kd">type</span> <span class="nx">HTTPMessageBody</span> <span class="kd">struct</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">	<span class="nx">Message</span> <span class="kt">string</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Node' && 'hidden'"
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
      <p>We don't have a working example for Node yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.25798127=Node" rel="noopener">Fill out the form</a>
and let us know if you'd like a sample for Node.</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
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
      <p>We don't have a working example for Python yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.25798127=Python" rel="noopener">Fill out the form</a>
and let us know if you'd like a sample for Python.</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Java' && 'hidden'"
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
      <p>We don't have a working example for Java yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.25798127=Java" rel="noopener">Fill out the form</a>
and let us know if you'd like a sample for Java.</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '.NET' && 'hidden'"
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
      <p>We don't have a working example for .NET. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.25798127=.Net" rel="noopener">Fill out the form</a>
and let us know if you'd like a sample for .NET.</p>
    </div>
  </blockquote>


      </div>
    
  </div>
</div>


## Adapt the Dockerfile

> [!NOTE]
>
> When using the `docker extension init`, it creates a `Dockerfile` that already contains what is needed for a Go backend.








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
        :class="selected === 'Node' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Node'})"
        
      >
        Node
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
        :class="selected === 'Java' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          'Java'})"
        
      >
        Java
      </button>
    
      <button
        class="tab-item"
        :class="selected === '.NET' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'lang', name:
          '.NET'})"
        
      >
        .NET
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Go' && 'hidden'"
      >
        <p>To deploy your Go backend when installing the extension, you need first to configure the <code>Dockerfile</code>, so that it:</p>
<ul>
<li>Builds the backend application</li>
<li>Copies the binary in the extension's container filesystem</li>
<li>Starts the binary when the container starts listening on the extension socket</li>
</ul>


  

  <blockquote
    
    class="admonition admonition-tip admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<mask id="mask0_5432_1749" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="4" y="1" width="17" height="22">
<path d="M9.93896 22H14.939M10.439 10H14.439M12.439 10L12.439 16M15.439 15.3264C17.8039 14.2029 19.439 11.7924 19.439 9C19.439 5.13401 16.305 2 12.439 2C8.57297 2 5.43896 5.13401 5.43896 9C5.43896 11.7924 7.07402 14.2029 9.43896 15.3264V16C9.43896 16.9319 9.43896 17.3978 9.59121 17.7654C9.79419 18.2554 10.1835 18.6448 10.6736 18.8478C11.0411 19 11.5071 19 12.439 19C13.3708 19 13.8368 19 14.2043 18.8478C14.6944 18.6448 15.0837 18.2554 15.2867 17.7654C15.439 17.3978 15.439 16.9319 15.439 16V15.3264Z" stroke="#6C7E9D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</mask>
<g mask="url(#mask0_5432_1749)">
<rect width="24" height="24" fill="currentColor" fill-opacity="0.8"/>
</g>
</svg>

      </span>
      <span class="admonition-title">
        Tip
      </span>
    </div>
    <div class="admonition-content">
      <p>To ease version management, you can reuse the same image to build the frontend, build the
backend service, and package the extension.</p>
    </div>
  </blockquote>

<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQpGUk9NIG5vZGU6MTcuNy1hbHBpbmUzLjE0IEFTIGNsaWVudC1idWlsZGVyCiMgLi4uIGJ1aWxkIGZyb250ZW5kIGFwcGxpY2F0aW9uCgojIEJ1aWxkIHRoZSBHbyBiYWNrZW5kCkZST00gZ29sYW5nOjEuMTctYWxwaW5lIEFTIGJ1aWxkZXIKRU5WIENHT19FTkFCTEVEPTAKV09SS0RJUiAvYmFja2VuZApDT1BZIHZtL2dvLiogLgpSVU4gLS1tb3VudD10eXBlPWNhY2hlLHRhcmdldD0vZ28vcGtnL21vZCBcCiAgICAtLW1vdW50PXR5cGU9Y2FjaGUsdGFyZ2V0PS9yb290Ly5jYWNoZS9nby1idWlsZCBcCiAgICBnbyBtb2QgZG93bmxvYWQKQ09QWSB2bS8uIC4KUlVOIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L2dvL3BrZy9tb2QgXAogICAgLS1tb3VudD10eXBlPWNhY2hlLHRhcmdldD0vcm9vdC8uY2FjaGUvZ28tYnVpbGQgXAogICAgZ28gYnVpbGQgLXRyaW1wYXRoIC1sZGZsYWdzPSItcyAtdyIgLW8gYmluL3NlcnZpY2UKCkZST00gYWxwaW5lOjMuMTUKIyAuLi4gYWRkIGxhYmVscyBhbmQgY29weSB0aGUgZnJvbnRlbmQgYXBwbGljYXRpb24KCkNPUFkgLS1mcm9tPWJ1aWxkZXIgL2JhY2tlbmQvYmluL3NlcnZpY2UgLwpDTUQgL3NlcnZpY2UgLXNvY2tldCAvcnVuL2d1ZXN0LXNlcnZpY2VzL2V4dGVuc2lvbi1hbGx0aGV0aGluZ3MtZXh0ZW5zaW9uLnNvY2s=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> node:17.7-alpine3.14 AS client-builder</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ... build frontend application</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># Build the Go backend</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> golang:1.17-alpine AS builder</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">CGO_ENABLED</span><span class="o">=</span><span class="m">0</span>
</span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="s"> /backend</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> vm/go.* .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/go/pkg/mod <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.cache/go-build <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    go mod download<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> vm/. .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/go/pkg/mod <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.cache/go-build <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    go build -trimpath -ldflags<span class="o">=</span><span class="s2">&#34;-s -w&#34;</span> -o bin/service<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> alpine:3.15</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ... add labels and copy the frontend application</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>builder /backend/bin/service /<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">CMD</span> /service -socket /run/guest-services/extension-allthethings-extension.sock</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Node' && 'hidden'"
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
      <p>We don't have a working Dockerfile for Node yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.25798127=Node" rel="noopener">Fill out the form</a>
and let us know if you'd like a Dockerfile for Node.</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
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
      <p>We don't have a working Dockerfile for Python yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.25798127=Python" rel="noopener">Fill out the form</a>
and let us know if you'd like a Dockerfile for Python.</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Java' && 'hidden'"
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
      <p>We don't have a working Dockerfile for Java yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.25798127=Java" rel="noopener">Fill out the form</a>
and let us know if you'd like a Dockerfile for Java.</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '.NET' && 'hidden'"
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
      <p>We don't have a working Dockerfile for .Net. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.25798127=.Net" rel="noopener">Fill out the form</a>
and let us know if you'd like a Dockerfile for .Net.</p>
    </div>
  </blockquote>


      </div>
    
  </div>
</div>


## Configure the metadata file

To start the backend service of your extension inside the VM of Docker Desktop, you have to configure the image name
in the `vm` section of the `metadata.json` file.

```json
{
  "vm": {
    "image": "${DESKTOP_PLUGIN_IMAGE}"
  },
  "icon": "docker.svg",
  "ui": {
    ...
  }
}
```

For more information on the `vm` section of the `metadata.json`, see [Metadata](../architecture/metadata.md).

> [!WARNING]
>
> Do not replace the `${DESKTOP_PLUGIN_IMAGE}` placeholder in the `metadata.json` file. The placeholder is replaced automatically with the correct image name when the extension is installed.

## Invoke the extension backend from your frontend

Using the [advanced frontend extension example](frontend-extension-tutorial.md), we can invoke our extension backend.

Use the Docker Desktop Client object and then invoke the `/hello` route from the backend service with `ddClient.
extension.vm.service.get` that returns the body of the response.








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
        <p>Replace the <code>ui/src/App.tsx</code> file with the following code:</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Ci8vIHVpL3NyYy9BcHAudHN4CmltcG9ydCBSZWFjdCwgeyB1c2VFZmZlY3QgfSBmcm9tICdyZWFjdCc7CmltcG9ydCB7IGNyZWF0ZURvY2tlckRlc2t0b3BDbGllbnQgfSBmcm9tICJAZG9ja2VyL2V4dGVuc2lvbi1hcGktY2xpZW50IjsKCi8vb2J0YWluIGRvY2tlciBkZXNrdG9wIGV4dGVuc2lvbiBjbGllbnQKY29uc3QgZGRDbGllbnQgPSBjcmVhdGVEb2NrZXJEZXNrdG9wQ2xpZW50KCk7CgpleHBvcnQgZnVuY3Rpb24gQXBwKCkgewogIGNvbnN0IGRkQ2xpZW50ID0gY3JlYXRlRG9ja2VyRGVza3RvcENsaWVudCgpOwogIGNvbnN0IFtoZWxsbywgc2V0SGVsbG9dID0gdXNlU3RhdGU8c3RyaW5nPigpOwoKICB1c2VFZmZlY3QoKCkgPT4gewogICAgY29uc3QgZ2V0SGVsbG8gPSBhc3luYyAoKSA9PiB7CiAgICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IGRkQ2xpZW50LmV4dGVuc2lvbi52bT8uc2VydmljZT8uZ2V0KCcvaGVsbG8nKTsKICAgICAgc2V0SGVsbG8oSlNPTi5zdHJpbmdpZnkocmVzdWx0KSk7CiAgICB9CiAgICBnZXRIZWxsbygpCiAgfSwgW10pOwoKICByZXR1cm4gKAogICAgPFR5cG9ncmFwaHk&#43;e2hlbGxvfTwvVHlwb2dyYXBoeT4KICApOwp9', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-tsx" data-lang="tsx"><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1">// ui/src/App.tsx
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="kr">import</span> <span class="nx">React</span><span class="p">,</span> <span class="p">{</span> <span class="nx">useEffect</span> <span class="p">}</span> <span class="kr">from</span> <span class="s1">&#39;react&#39;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl"><span class="kr">import</span> <span class="p">{</span> <span class="nx">createDockerDesktopClient</span> <span class="p">}</span> <span class="kr">from</span> <span class="s2">&#34;@docker/extension-api-client&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1">//obtain docker desktop extension client
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="kr">const</span> <span class="nx">ddClient</span> <span class="o">=</span> <span class="nx">createDockerDesktopClient</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">export</span> <span class="kd">function</span> <span class="nx">App() {</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">ddClient</span> <span class="o">=</span> <span class="nx">createDockerDesktopClient</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="p">[</span><span class="nx">hello</span><span class="p">,</span> <span class="nx">setHello</span><span class="p">]</span> <span class="o">=</span> <span class="nx">useState</span><span class="p">&lt;</span><span class="nt">string</span><span class="p">&gt;();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">useEffect</span><span class="p">(()</span> <span class="o">=&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="kr">const</span> <span class="nx">getHello</span> <span class="o">=</span> <span class="kr">async</span> <span class="p">()</span> <span class="o">=&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="kr">const</span> <span class="nx">result</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">ddClient</span><span class="p">.</span><span class="nx">extension</span><span class="p">.</span><span class="nx">vm</span><span class="o">?</span><span class="p">.</span><span class="nx">service</span><span class="o">?</span><span class="p">.</span><span class="kr">get</span><span class="p">(</span><span class="s1">&#39;/hello&#39;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">      <span class="nx">setHello</span><span class="p">(</span><span class="nx">JSON</span><span class="p">.</span><span class="nx">stringify</span><span class="p">(</span><span class="nx">result</span><span class="p">));</span>
</span></span><span class="line"><span class="cl">    <span class="p">}</span>
</span></span><span class="line"><span class="cl">    <span class="nx">getHello</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">  <span class="p">},</span> <span class="p">[]);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">return</span> <span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="p">&lt;</span><span class="nt">Typography</span><span class="p">&gt;{</span><span class="nx">hello</span><span class="p">}&lt;/</span><span class="nt">Typography</span><span class="p">&gt;</span>
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
      <p>We don't have an example for Vue yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.1333218187=Vue" rel="noopener">Fill out the form</a>
and let us know if you'd like a sample with Vue.</p>
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
      <p>We don't have an example for Angular yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.1333218187=Angular" rel="noopener">Fill out the form</a>
and let us know if you'd like a sample with Angular.</p>
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
      <p>We don't have an example for Svelte yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.1333218187=Svelte" rel="noopener">Fill out the form</a>
and let us know if you'd like a sample with Svelte.</p>
    </div>
  </blockquote>


      </div>
    
  </div>
</div>


## Re-build the extension and update it

Since you have modified the configuration of the extension and added a stage in the Dockerfile, you must re-build the extension.

```bash
docker build --tag=awesome-inc/my-extension:latest .
```

Once built, you need to update it, or install it if you haven't already done so.

```bash
docker extension update awesome-inc/my-extension:latest
```

Now you can see the backend service running in the **Containers** view of the Docker Desktop Dashboard and watch the logs when you need to debug it.

> [!TIP]
>
> You may need to turn on the **Show system containers** option in **Settings** to see the backend container running.
> See [Show extension containers](../dev/test-debug.md#show-the-extension-containers) for more information.

Open the Docker Desktop Dashboard and select the **Containers** tab. You should see the response from the backend service
call displayed.

## What's next?

- Learn how to [share and publish your extension](../extensions/_index.md).
- Learn more about extensions [architecture](../architecture/_index.md).

