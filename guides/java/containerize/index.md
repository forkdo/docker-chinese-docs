# 容器化 Java 应用程序

## 先决条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
  Docker 会定期添加新功能，本指南的部分内容可能仅适用于最新版本的 Docker Desktop。

* 您已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但您可以使用任何客户端。

## 概述

本节将引导您完成容器化和运行 Java 应用程序的过程。

## 获取示例应用程序

将您要使用的示例应用程序克隆到本地开发机器。在终端中运行以下命令以克隆仓库。

```console
$ git clone https://github.com/spring-projects/spring-petclinic.git
```

示例应用程序是一个使用 Maven 构建的 Spring Boot 应用程序。有关更多详细信息，请参阅仓库中的 `readme.md`。

## 初始化 Docker 资源

现在您已有一个应用程序，可以创建必要的 Docker 资源来容器化您的应用程序。您可以使用 Docker Desktop 内置的 Docker Init 功能来帮助简化流程，也可以手动创建这些资源。








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
        :class="selected === '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA%E8%B5%84%E6%BA%90' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA%E8%B5%84%E6%BA%90'"
        
      >
        手动创建资源
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-Docker-Init' && 'hidden'"
      >
        <p>在 <code>spring-petclinic</code> 目录中，运行 <code>docker init</code> 命令。<code>docker init</code> 会提供一些默认配置，但您需要回答一些关于应用程序的问题。参考以下示例回答 <code>docker init</code> 的提示，并为您的提示使用相同的答案。</p>
<p>示例应用程序已包含 Docker 资源。系统会提示您覆盖现有的 Docker 资源。要继续本指南，请选择 <code>y</code> 以覆盖它们。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgaW5pdApXZWxjb21lIHRvIHRoZSBEb2NrZXIgSW5pdCBDTEkhCgpUaGlzIHV0aWxpdHkgd2lsbCB3YWxrIHlvdSB0aHJvdWdoIGNyZWF0aW5nIHRoZSBmb2xsb3dpbmcgZmlsZXMgd2l0aCBzZW5zaWJsZSBkZWZhdWx0cyBmb3IgeW91ciBwcm9qZWN0OgogIC0gLmRvY2tlcmlnbm9yZQogIC0gRG9ja2VyZmlsZQogIC0gY29tcG9zZS55YW1sCiAgLSBSRUFETUUuRG9ja2VyLm1kCgpMZXQncyBnZXQgc3RhcnRlZCEKCldBUk5JTkc6IFRoZSBmb2xsb3dpbmcgRG9ja2VyIGZpbGVzIGFscmVhZHkgZXhpc3QgaW4gdGhpcyBkaXJlY3Rvcnk6CiAgLSBkb2NrZXItY29tcG9zZS55bWwKPyBEbyB5b3Ugd2FudCB0byBvdmVyd3JpdGUgdGhlbT8gWWVzCj8gV2hhdCBhcHBsaWNhdGlvbiBwbGF0Zm9ybSBkb2VzIHlvdXIgcHJvamVjdCB1c2U/IEphdmEKPyBXaGF0J3MgdGhlIHJlbGF0aXZlIGRpcmVjdG9yeSAod2l0aCBhIGxlYWRpbmcgLikgZm9yIHlvdXIgYXBwPyAuL3NyYwo/IFdoYXQgdmVyc2lvbiBvZiBKYXZhIGRvIHlvdSB3YW50IHRvIHVzZT8gMjEKPyBXaGF0IHBvcnQgZG9lcyB5b3VyIHNlcnZlciBsaXN0ZW4gb24/IDgwODA=', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="go">Welcome to the Docker Init CLI!
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="go">This utility will walk you through creating the following files with sensible defaults for your project:
</span></span></span><span class="line"><span class="cl"><span class="go">  - .dockerignore
</span></span></span><span class="line"><span class="cl"><span class="go">  - Dockerfile
</span></span></span><span class="line"><span class="cl"><span class="go">  - compose.yaml
</span></span></span><span class="line"><span class="cl"><span class="go">  - README.Docker.md
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="go">Let&#39;s get started!
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="go">WARNING: The following Docker files already exist in this directory:
</span></span></span><span class="line"><span class="cl"><span class="go">  - docker-compose.yml
</span></span></span><span class="line"><span class="cl"><span class="go">? Do you want to overwrite them? Yes
</span></span></span><span class="line"><span class="cl"><span class="go">? What application platform does your project use? Java
</span></span></span><span class="line"><span class="cl"><span class="go">? What&#39;s the relative directory (with a leading .) for your app? ./src
</span></span></span><span class="line"><span class="cl"><span class="go">? What version of Java do you want to use? 21
</span></span></span><span class="line"><span class="cl"><span class="go">? What port does your server listen on? 8080
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>在上面的示例中，请注意 <code>WARNING</code>。<code>docker-compose.yaml</code> 已存在，因此 <code>docker init</code> 会覆盖该文件，而不是创建新的 <code>compose.yaml</code> 文件。这样可以防止目录中出现多个 Compose 文件。两种名称都受支持，但 Compose 首选标准名称 <code>compose.yaml</code>。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA%E8%B5%84%E6%BA%90' && 'hidden'"
      >
        <p>如果您未安装 Docker Desktop 或更喜欢手动创建资源，可以在项目目录中创建以下文件。</p>
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
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQoKIyDmnKzmlofku7blkITlpITmj5Dkvpvkuobms6jph4rvvIzluK7liqnmgqjlhaXpl6jjgIIKIyDlpoLmnpzmgqjpnIDopoHmm7TlpJrluK7liqnvvIzor7forr/pl64gRG9ja2VyZmlsZSDlj4LogIPmjIfljZfvvJoKIyBodHRwczovL2RvY3MuZG9ja2VyLmNvbS9nby9kb2NrZXJmaWxlLXJlZmVyZW5jZS8KCiMg5oOz5biu5Yqp5oiR5Lus5pS56L&#43;b5q2k5qih5p2/77yf6K&#43;35Zyo5q2k5aSE5YiG5Lqr5oKo55qE5Y&#43;N6aaI77yaaHR0cHM6Ly9mb3Jtcy5nbGUveWJxOUtydDhqdEJMM2lDazcKCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCgojIOWIm&#43;W7uuS4gOS4queUqOS6juino&#43;aekOWSjOS4i&#43;i9veS&#43;nei1lumhueeahOmYtuauteOAggpGUk9NIGVjbGlwc2UtdGVtdXJpbjoyMS1qZGstamFtbXkgYXMgZGVwcwoKV09SS0RJUiAvYnVpbGQKCiMg5aSN5Yi25YW35pyJ5Y&#43;v5omn6KGM5p2D6ZmQ55qEIG12bncg5YyF6KOF5Zmo44CCCkNPUFkgLS1jaG1vZD0wNzU1IG12bncgbXZudwpDT1BZIC5tdm4vIC5tdm4vCgojIOWwhuS4i&#43;i9veS&#43;nei1lumhueS9nOS4uuWNleeLrOatpemqpO&#43;8jOS7peWIqeeUqCBEb2NrZXIg55qE57yT5a2Y44CCCiMg5Yip55So57yT5a2Y5oyC6L295YiwIC9yb290Ly5tMu&#43;8jOS7peS&#43;v&#43;WQjue7reaehOW7uuaXoOmcgOmHjeaWsOS4i&#43;i9veWMheOAggpSVU4gLS1tb3VudD10eXBlPWJpbmQsc291cmNlPXBvbS54bWwsdGFyZ2V0PXBvbS54bWwgXAogICAgLS1tb3VudD10eXBlPWNhY2hlLHRhcmdldD0vcm9vdC8ubTIgLi9tdm53IGRlcGVuZGVuY3k6Z28tb2ZmbGluZSAtRHNraXBUZXN0cwoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCiMg5Yib5bu65LiA5Liq5Z&#43;65LqO5bey5LiL6L295L6d6LWW6aG56Zi25q6155qE5p6E5bu65bqU55So56iL5bqP6Zi25q6144CCCiMg5q2kIERvY2tlcmZpbGUg6ZKI5a&#43;56L6T5Ye6IHViZXIgamFyIOeahCBKYXZhIOW6lOeUqOeoi&#43;W6j&#43;i/m&#43;ihjOS6huS8mOWMlu&#43;8jHViZXIgamFyIOWMheWQq&#43;WcqCBKVk0g5Lit6L&#43;Q6KGM5bqU55So5omA6ZyA55qE5omA5pyJ5L6d6LWW6aG544CCCiMg5aaC5p6c5oKo55qE5bqU55So5LiN6L6T5Ye6IHViZXIgamFy77yM6ICM5piv5L6d6LWWIEFwYWNoZSBUb21jYXQg562J5bqU55So5pyN5Yqh5Zmo77yM5YiZ6ZyA6KaB5pu05paw5q2k6Zi25q6155qE5YyF5paH5Lu25ZCN77yMCiMg5bm25pu05pawICJmaW5hbCIg6Zi25q6155qE5Z&#43;656GA6ZWc5YOP5Lul5L2/55So55u45YWz5bqU55So5pyN5Yqh5Zmo77yM5L6L5aaC5L2/55SoIHRvbWNhdO&#43;8iGh0dHBzOi8vaHViLmRvY2tlci5jb20vXy90b21jYXQv77yJ5L2c5Li65Z&#43;656GA6ZWc5YOP44CCCkZST00gZGVwcyBhcyBwYWNrYWdlCgpXT1JLRElSIC9idWlsZAoKQ09QWSAuL3NyYyBzcmMvClJVTiAtLW1vdW50PXR5cGU9YmluZCxzb3VyY2U9cG9tLnhtbCx0YXJnZXQ9cG9tLnhtbCBcCiAgICAtLW1vdW50PXR5cGU9Y2FjaGUsdGFyZ2V0PS9yb290Ly5tMiBcCiAgICAuL212bncgcGFja2FnZSAtRHNraXBUZXN0cyAmJiBcCiAgICBtdiB0YXJnZXQvJCguL212bncgaGVscDpldmFsdWF0ZSAtRGV4cHJlc3Npb249cHJvamVjdC5hcnRpZmFjdElkIC1xIC1EZm9yY2VTdGRvdXQpLSQoLi9tdm53IGhlbHA6ZXZhbHVhdGUgLURleHByZXNzaW9uPXByb2plY3QudmVyc2lvbiAtcSAtRGZvcmNlU3Rkb3V0KS5qYXIgdGFyZ2V0L2FwcC5qYXIKCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCgojIOWIm&#43;W7uuS4gOS4queUqOS6juWwhuW6lOeUqOeoi&#43;W6j&#43;aPkOWPluWIsOWNleeLrOWxgueahOmYtuauteOAggojIOWIqeeUqCBTcHJpbmcgQm9vdCDnmoTlsYLlt6XlhbflkowgRG9ja2VyIOeahOe8k&#43;WtmO&#43;8jOWwhuaJk&#43;WMheeahOW6lOeUqOeoi&#43;W6j&#43;aPkOWPluWIsOWPr&#43;WkjeWItuWIsOacgOe7iOmYtuauteeahOWNleeLrOWxguS4reOAggojIOWPguiAgyBTcHJpbmcg5paH5qGj77yaCiMgaHR0cHM6Ly9kb2NzLnNwcmluZy5pby9zcHJpbmctYm9vdC9kb2NzL2N1cnJlbnQvcmVmZXJlbmNlL2h0bWwvY29udGFpbmVyLWltYWdlcy5odG1sCkZST00gcGFja2FnZSBhcyBleHRyYWN0CgpXT1JLRElSIC9idWlsZAoKUlVOIGphdmEgLURqYXJtb2RlPWxheWVydG9vbHMgLWphciB0YXJnZXQvYXBwLmphciBleHRyYWN0IC0tZGVzdGluYXRpb24gdGFyZ2V0L2V4dHJhY3RlZAoKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKCiMg5Yib5bu65LiA5Liq5paw55qE6L&#43;Q6KGM5bqU55So56iL5bqP6Zi25q6177yM6K&#43;l6Zi25q615YyF5ZCr5bqU55So56iL5bqP55qE5pyA5bCP6L&#43;Q6KGM5pe25L6d6LWW6aG544CCCiMg5q2k6Zi25q616YCa5bi45L2/55So5LiO5a6J6KOF5oiW5p6E5bu66Zi25q615LiN5ZCM55qE5Z&#43;656GA6ZWc5YOP77yM5b&#43;F6KaB5paH5Lu25LuO5a6J6KOF6Zi25q615aSN5Yi244CCCiMKIyDku6XkuIvnpLrkvovkvb/nlKggZWNsaXBzZS10dXJtaW4g55qEIEpSRSDplZzlg4/kvZzkuLrov5DooYzlupTnlKjnmoTln7rnoYDjgIIKIyDpgJrov4fmjIflrpogIjE3LWpyZS1qYW1teSIg5qCH562&#43;77yM5a6D6L&#43;Y5Lya5L2/55So5p6E5bu6IERvY2tlcmZpbGUg5pe26K&#43;l5qCH562&#43;55qE5pyA5paw54mI5pys44CCCiMg5aaC5p6c5Y&#43;v6YeN546w5oCn5b6I6YeN6KaB77yM6K&#43;36ICD6JmR5L2/55So54m55a6a55qE5pGY6KaBIFNIQe&#43;8jOS&#43;i&#43;WmggojIGVjbGlwc2UtdGVtdXJpbkBzaGEyNTY6OTljZWRlNDkzZGZkODg3MjBiNjEwZWI4MDc3Yzg2ODhkM2NjYTUwMDAzZDc2ZDFkNTM5YjBlZmM4Y2NhNzJiNOOAggpGUk9NIGVjbGlwc2UtdGVtdXJpbjoyMS1qcmUtamFtbXkgQVMgZmluYWwKCiMg5Yib5bu65LiA5Liq5bqU55So5bCG5Lul5YW26Lqr5Lu96L&#43;Q6KGM55qE6Z2e54m55p2D55So5oi344CCCiMg5Y&#43;C6KeBIGh0dHBzOi8vZG9jcy5kb2NrZXIuY29tL2dvL2RvY2tlcmZpbGUtdXNlci1iZXN0LXByYWN0aWNlcy8KQVJHIFVJRD0xMDAwMQpSVU4gYWRkdXNlciBcCiAgICAtLWRpc2FibGVkLXBhc3N3b3JkIFwKICAgIC0tZ2Vjb3MgIiIgXAogICAgLS1ob21lICIvbm9uZXhpc3RlbnQiIFwKICAgIC0tc2hlbGwgIi9zYmluL25vbG9naW4iIFwKICAgIC0tbm8tY3JlYXRlLWhvbWUgXAogICAgLS11aWQgIiR7VUlEfSIgXAogICAgYXBwdXNlcgpVU0VSIGFwcHVzZXIKCiMg5LuOICJwYWNrYWdlIiDpmLbmrrXlpI3liLblj6/miafooYzmlofku7bjgIIKQ09QWSAtLWZyb209ZXh0cmFjdCBidWlsZC90YXJnZXQvZXh0cmFjdGVkL2RlcGVuZGVuY2llcy8gLi8KQ09QWSAtLWZyb209ZXh0cmFjdCBidWlsZC90YXJnZXQvZXh0cmFjdGVkL3NwcmluZy1ib290LWxvYWRlci8gLi8KQ09QWSAtLWZyb209ZXh0cmFjdCBidWlsZC90YXJnZXQvZXh0cmFjdGVkL3NuYXBzaG90LWRlcGVuZGVuY2llcy8gLi8KQ09QWSAtLWZyb209ZXh0cmFjdCBidWlsZC90YXJnZXQvZXh0cmFjdGVkL2FwcGxpY2F0aW9uLyAuLwoKRVhQT1NFIDgwODAKCkVOVFJZUE9JTlQgWyAiamF2YSIsICJvcmcuc3ByaW5nZnJhbWV3b3JrLmJvb3QubG9hZGVyLmxhdW5jaC5KYXJMYXVuY2hlciIgXQ==', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="c"># 本文件各处提供了注释，帮助您入门。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果您需要更多帮助，请访问 Dockerfile 参考指南：</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># https://docs.docker.com/go/dockerfile-reference/</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 想帮助我们改进此模板？请在此处分享您的反馈：https://forms.gle/ybq9Krt8jtBL3iCk7</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">################################################################################</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 创建一个用于解析和下载依赖项的阶段。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">eclipse-temurin:21-jdk-jammy</span><span class="w"> </span><span class="k">as</span><span class="w"> </span><span class="s">deps</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 复制具有可执行权限的 mvnw 包装器。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --chmod<span class="o">=</span><span class="m">0755</span> mvnw mvnw<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> .mvn/ .mvn/<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 将下载依赖项作为单独步骤，以利用 Docker 的缓存。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 利用缓存挂载到 /root/.m2，以便后续构建无需重新下载包。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>bind,source<span class="o">=</span>pom.xml,target<span class="o">=</span>pom.xml <span class="se">\
</span></span></span><span class="line"><span class="cl">    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.m2 ./mvnw dependency:go-offline -DskipTests<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">################################################################################</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 创建一个基于已下载依赖项阶段的构建应用程序阶段。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 此 Dockerfile 针对输出 uber jar 的 Java 应用程序进行了优化，uber jar 包含在 JVM 中运行应用所需的所有依赖项。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果您的应用不输出 uber jar，而是依赖 Apache Tomcat 等应用服务器，则需要更新此阶段的包文件名，</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 并更新 &#34;final&#34; 阶段的基础镜像以使用相关应用服务器，例如使用 tomcat（https://hub.docker.com/_/tomcat/）作为基础镜像。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">deps</span><span class="w"> </span><span class="k">as</span><span class="w"> </span><span class="s">package</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> ./src src/<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>bind,source<span class="o">=</span>pom.xml,target<span class="o">=</span>pom.xml <span class="se">\
</span></span></span><span class="line"><span class="cl">    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.m2 <span class="se">\
</span></span></span><span class="line"><span class="cl">    ./mvnw package -DskipTests <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    mv target/<span class="k">$(</span>./mvnw help:evaluate -Dexpression<span class="o">=</span>project.artifactId -q -DforceStdout<span class="k">)</span>-<span class="k">$(</span>./mvnw help:evaluate -Dexpression<span class="o">=</span>project.version -q -DforceStdout<span class="k">)</span>.jar target/app.jar<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">################################################################################</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 创建一个用于将应用程序提取到单独层的阶段。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 利用 Spring Boot 的层工具和 Docker 的缓存，将打包的应用程序提取到可复制到最终阶段的单独层中。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 参考 Spring 文档：</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># https://docs.spring.io/spring-boot/docs/current/reference/html/container-images.html</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">package</span><span class="w"> </span><span class="k">as</span><span class="w"> </span><span class="s">extract</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> java -Djarmode<span class="o">=</span>layertools -jar target/app.jar extract --destination target/extracted<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">################################################################################</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 创建一个新的运行应用程序阶段，该阶段包含应用程序的最小运行时依赖项。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 此阶段通常使用与安装或构建阶段不同的基础镜像，必要文件从安装阶段复制。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 以下示例使用 eclipse-turmin 的 JRE 镜像作为运行应用的基础。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 通过指定 &#34;17-jre-jammy&#34; 标签，它还会使用构建 Dockerfile 时该标签的最新版本。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果可重现性很重要，请考虑使用特定的摘要 SHA，例如</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># eclipse-temurin@sha256:99cede493dfd88720b610eb8077c8688d3cca50003d76d1d539b0efc8cca72b4。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">eclipse-temurin:21-jre-jammy</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">final</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 创建一个应用将以其身份运行的非特权用户。</span><span class="err">
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
</span></span></span><span class="line"><span class="cl"><span class="k">USER</span><span class="w"> </span><span class="s">appuser</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 从 &#34;package&#34; 阶段复制可执行文件。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>extract build/target/extracted/dependencies/ ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>extract build/target/extracted/spring-boot-loader/ ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>extract build/target/extracted/snapshot-dependencies/ ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>extract build/target/extracted/application/ ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">EXPOSE</span><span class="w"> </span><span class="s">8080</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span> <span class="s2">&#34;java&#34;</span><span class="p">,</span> <span class="s2">&#34;org.springframework.boot.loader.launch.JarLauncher&#34;</span> <span class="p">]</span></span></span></code></pre></div>
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
<p>示例已包含 Compose 文件。覆盖此文件以继续本指南。使用以下内容更新 <code>docker-compose.yaml</code>。</p>
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
          docker-compose.yaml
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDmnKzmlofku7blkITlpITmj5Dkvpvkuobms6jph4rvvIzluK7liqnmgqjlhaXpl6jjgIIKIyDlpoLmnpzmgqjpnIDopoHmm7TlpJrluK7liqnvvIzor7forr/pl64gRG9ja2VyIENvbXBvc2Ug5Y&#43;C6ICD5oyH5Y2X77yaCiMgaHR0cHM6Ly9kb2NzLmRvY2tlci5jb20vZ28vY29tcG9zZS1zcGVjLXJlZmVyZW5jZS8KCiMg5q2k5aSE5oyH5Luk5bCG5oKo55qE5bqU55So56iL5bqP5a6a5LmJ5Li65ZCN5Li6ICJzZXJ2ZXIiIOeahOacjeWKoeOAggojIOatpOacjeWKoeS7juW9k&#43;WJjeebruW9leeahCBEb2NrZXJmaWxlIOaehOW7uuOAggojIOaCqOWPr&#43;S7peWcqOatpOWkhOa3u&#43;WKoOW6lOeUqOeoi&#43;W6j&#43;WPr&#43;iDveS&#43;nei1lueahOWFtuS7luacjeWKoe&#43;8jOS&#43;i&#43;WmguaVsOaNruW6k&#43;aIlue8k&#43;WtmOOAguacieWFs&#43;ekuuS&#43;i&#43;&#43;8jOivt&#43;WPgumYhSBBd2Vzb21lIENvbXBvc2Ug5LuT5bqT77yaCiMgaHR0cHM6Ly9naXRodWIuY29tL2RvY2tlci9hd2Vzb21lLWNvbXBvc2UKc2VydmljZXM6CiAgc2VydmVyOgogICAgYnVpbGQ6CiAgICAgIGNvbnRleHQ6IC4KICAgIHBvcnRzOgogICAgICAtIDgwODA6ODA4MAojIOS7peS4i&#43;azqOmHiumDqOWIhuaYr&#43;WumuS5iSBQb3N0Z3JlU1FMIOaVsOaNruW6k&#43;eahOekuuS&#43;i&#43;&#43;8jOaCqOeahOW6lOeUqOeoi&#43;W6j&#43;WPr&#43;S7peS9v&#43;eUqOOAggojIGBkZXBlbmRzX29uYCDlkYror4kgRG9ja2VyIENvbXBvc2Ug5Zyo5bqU55So56iL5bqP5LmL5YmN5ZCv5Yqo5pWw5o2u5bqT44CCCiMgYGRiLWRhdGFgIOWNt&#43;WcqOWuueWZqOmHjeWQr&#43;S5i&#43;mXtOaMgeS5heWMluaVsOaNruW6k&#43;aVsOaNruOAggojIGBkYi1wYXNzd29yZGAg5a&#43;G6ZKl55So5LqO6K6&#43;572u5pWw5o2u5bqT5a&#43;G56CB44CC5Zyo6L&#43;Q6KGMIGBkb2NrZXIgY29tcG9zZSB1cGAg5LmL5YmN77yMCiMg5oKo5b&#43;F6aG75Yib5bu6IGBkYi9wYXNzd29yZC50eHRgIOW5tuWQkeWFtuS4rea3u&#43;WKoOaCqOmAieaLqeeahOWvhueggeOAggojICAgICBkZXBlbmRzX29uOgojICAgICAgIGRiOgojICAgICAgICAgY29uZGl0aW9uOiBzZXJ2aWNlX2hlYWx0aHkKIyAgIGRiOgojICAgICBpbWFnZTogcG9zdGdyZXM6MTgKIyAgICAgcmVzdGFydDogYWx3YXlzCiMgICAgIHVzZXI6IHBvc3RncmVzCiMgICAgIHNlY3JldHM6CiMgICAgICAgLSBkYi1wYXNzd29yZAojICAgICB2b2x1bWVzOgojICAgICAgIC0gZGItZGF0YTovdmFyL2xpYi9wb3N0Z3Jlc3FsCiMgICAgIGVudmlyb25tZW50OgojICAgICAgIC0gUE9TVEdSRVNfREI9ZXhhbXBsZQojICAgICAgIC0gUE9TVEdSRVNfUEFTU1dPUkRfRklMRT0vcnVuL3NlY3JldHMvZGItcGFzc3dvcmQKIyAgICAgZXhwb3NlOgojICAgICAgIC0gNTQzMgojICAgICBoZWFsdGhjaGVjazoKIyAgICAgICB0ZXN0OiBbICJDTUQiLCAicGdfaXNyZWFkeSIgXQojICAgICAgIGludGVydmFsOiAxMHMKIyAgICAgICB0aW1lb3V0OiA1cwojICAgICAgIHJldHJpZXM6IDUKIyB2b2x1bWVzOgojICAgZGItZGF0YToKIyBzZWNyZXRzOgojICAgZGItcGFzc3dvcmQ6CiMgICAgIGZpbGU6IGRiL3Bhc3N3b3JkLnR4dA==', copying: false }"
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
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="c"># 本文件各处提供了注释，帮助您入门。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果您需要更多帮助，请访问 Docker Compose 参考指南：</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># https://docs.docker.com/go/compose-spec-reference/</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># 此处指令将您的应用程序定义为名为 &#34;server&#34; 的服务。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># 此服务从当前目录的 Dockerfile 构建。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># 您可以在此处添加应用程序可能依赖的其他服务，例如数据库或缓存。有关示例，请参阅 Awesome Compose 仓库：</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># https://github.com/docker/awesome-compose</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">services</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">server</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">build</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span><span class="nt">context</span><span class="p">:</span><span class="w"> </span><span class="l">.</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="m">8080</span><span class="p">:</span><span class="m">8080</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># 以下注释部分是定义 PostgreSQL 数据库的示例，您的应用程序可以使用。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># `depends_on` 告诉 Docker Compose 在应用程序之前启动数据库。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># `db-data` 卷在容器重启之间持久化数据库数据。</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># `db-password` 密钥用于设置数据库密码。在运行 `docker compose up` 之前，</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c"># 您必须创建 `db/password.txt` 并向其中添加您选择的密码。</span><span class="w">
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
        x-data="{ code: 'IyDlnKjmraTlpITljIXlkKvmgqjkuI3luIzmnJvlpI3liLbliLDlrrnlmajkuK3nmoTku7vkvZXmlofku7bmiJbnm67lvZXvvIjkvovlpoLvvIzmnKzlnLDmnoTlu7rkuqfnianjgIHkuLTml7bmlofku7bnrYnvvInjgIIKIwojIOWmgumcgOabtOWkmuW4ruWKqe&#43;8jOivt&#43;iuv&#43;mXriAuZG9ja2VyaWdub3JlIOaWh&#43;S7tuWPguiAg&#43;aMh&#43;WNl&#43;&#43;8mgojIGh0dHBzOi8vZG9jcy5kb2NrZXIuY29tL2dvL2J1aWxkLWNvbnRleHQtZG9ja2VyaWdub3JlLwoKKiovLmNsYXNzcGF0aAoqKi8uZG9ja2VyaWdub3JlCioqLy5lbnYKKiovLmdpdAoqKi8uZ2l0aWdub3JlCioqLy5wcm9qZWN0CioqLy5zZXR0aW5ncwoqKi8udG9vbHN0YXJnZXQKKiovLnZzCioqLy52c2NvZGUKKiovLm5leHQKKiovLmNhY2hlCioqLyouKnByb2oudXNlcgoqKi8qLmRibWRsCioqLyouamZtCioqL2NoYXJ0cwoqKi9kb2NrZXItY29tcG9zZSoKKiovY29tcG9zZS55Km1sCioqL3RhcmdldAoqKi9Eb2NrZXJmaWxlKgoqKi9ub2RlX21vZHVsZXMKKiovbnBtLWRlYnVnLmxvZwoqKi9vYmoKKiovc2VjcmV0cy5kZXYueWFtbAoqKi92YWx1ZXMuZGV2LnlhbWwKKiovdmVuZG9yCkxJQ0VOU0UKUkVBRE1FLm1k', copying: false }"
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
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl"># 在此处包含您不希望复制到容器中的任何文件或目录（例如，本地构建产物、临时文件等）。
</span></span><span class="line"><span class="cl">#
</span></span><span class="line"><span class="cl"># 如需更多帮助，请访问 .dockerignore 文件参考指南：
</span></span><span class="line"><span class="cl"># https://docs.docker.com/go/build-context-dockerignore/
</span></span><span class="line"><span class="cl">
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
</span></span><span class="line"><span class="cl">**/.next
</span></span><span class="line"><span class="cl">**/.cache
</span></span><span class="line"><span class="cl">**/*.*proj.user
</span></span><span class="line"><span class="cl">**/*.dbmdl
</span></span><span class="line"><span class="cl">**/*.jfm
</span></span><span class="line"><span class="cl">**/charts
</span></span><span class="line"><span class="cl">**/docker-compose*
</span></span><span class="line"><span class="cl">**/compose.y*ml
</span></span><span class="line"><span class="cl">**/target
</span></span><span class="line"><span class="cl">**/Dockerfile*
</span></span><span class="line"><span class="cl">**/node_modules
</span></span><span class="line"><span class="cl">**/npm-debug.log
</span></span><span class="line"><span class="cl">**/obj
</span></span><span class="line"><span class="cl">**/secrets.dev.yaml
</span></span><span class="line"><span class="cl">**/values.dev.yaml
</span></span><span class="line"><span class="cl">**/vendor
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

      </div>
    
  </div>
</div>


现在您的 `spring-petclinic` 目录中应包含以下三个文件。

- [Dockerfile](/reference/dockerfile/)
- [.dockerignore](/reference/dockerfile/#dockerignore-file)
- [docker-compose.yaml](/reference/compose-file/_index.md)

## 运行应用程序

在 `spring-petclinic` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

首次构建和运行应用时，Docker 会下载依赖项并构建应用。根据您的网络连接，可能需要几分钟时间。

打开浏览器并访问 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该能看到一个简单的宠物诊所应用。

在终端中按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项在终端后台运行应用程序。在 `spring-petclinic` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该能看到一个简单的宠物诊所应用。

在终端中运行以下命令以停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅
[Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，您学习了如何使用 Docker 容器化和运行 Java 应用程序。

相关信息：

- [docker init 参考](/reference/cli/docker/init/)

## 下一步

在下一节中，您将学习如何使用 Docker 容器开发您的应用程序。
