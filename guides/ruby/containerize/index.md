# 容器化 Ruby on Rails 应用

## 前置条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用 Git CLI，但你可以使用任意客户端。

## 概述

本节将引导你完成容器化 [Ruby on Rails](https://rubyonrails.org/) 应用的全过程。

从 Rails 7.1 开始，[Docker 已原生支持](https://guides.rubyonrails.org/7_1_release_notes.html#generate-dockerfiles-for-new-rails-applications)。这意味着创建新 Rails 应用时，系统会自动生成 `Dockerfile`、`.dockerignore` 和 `bin/docker-entrypoint` 文件。

如果你已有 Rails 应用，则需要手动创建 Docker 资产。不幸的是，`docker init` 命令目前还不支持 Rails。这意味着如果你使用 Rails，需要从下方示例中手动复制 Dockerfile 和其他相关配置。

## 1. 初始化 Docker 资产

Rails 7.1 及以上版本默认生成多阶段 Dockerfile。以下是两种版本：一种使用 Docker Hardened Images (DHI)，另一种使用官方 Docker 镜像。

> [Docker Hardened Images (DHIs)](https://docs.docker.com/dhi/) 是由 Docker 维护的最小化、安全且可用于生产的容器基础镜像和应用镜像。

为提升安全性，建议在可能的情况下使用 DHI 镜像。它们旨在减少漏洞并简化合规性。

> 多阶段 Dockerfile 通过分离构建和运行时依赖，帮助创建更小、更高效的镜像，确保最终镜像仅包含必要组件。详见 [多阶段构建指南](/get-started/docker-concepts/building-images/multi-stage-builds/)。

虽然 Dockerfile 会自动生成，但理解其用途和功能很重要。强烈建议查看以下示例。








<div
  class="tabs"
  
    x-data="{ selected: '%E4%BD%BF%E7%94%A8-Docker-Hardened-Images' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8-Docker-Hardened-Images' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8-Docker-Hardened-Images'"
        
      >
        使用 Docker Hardened Images
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8%E5%AE%98%E6%96%B9-Docker-%E9%95%9C%E5%83%8F' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8%E5%AE%98%E6%96%B9-Docker-%E9%95%9C%E5%83%8F'"
        
      >
        使用官方 Docker 镜像
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-Docker-Hardened-Images' && 'hidden'"
      >
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
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQojIGNoZWNrPWVycm9yPXRydWUKCiMg5q2kIERvY2tlcmZpbGUg5LiT5Li655Sf5Lqn546v5aKD6K6&#43;6K6h77yM6Z2e5byA5Y&#43;R546v5aKD44CCCiMgZG9ja2VyIGJ1aWxkIC10IGFwcCAuCiMgZG9ja2VyIHJ1biAtZCAtcCA4MDo4MCAtZSBSQUlMU19NQVNURVJfS0VZPTxjb25maWcvbWFzdGVyLmtleSDkuK3nmoTlgLw&#43;IC0tbmFtZSBhcHAgYXBwCgojIOWmgumcgOWuueWZqOWMluW8gOWPkeeOr&#43;Wig&#43;&#43;8jOivt&#43;WPgumYhSBEZXYgQ29udGFpbmVyc&#43;&#43;8mmh0dHBzOi8vZ3VpZGVzLnJ1YnlvbnJhaWxzLm9yZy9nZXR0aW5nX3N0YXJ0ZWRfd2l0aF9kZXZjb250YWluZXIuaHRtbAoKIyDnoa7kv50gUlVCWV9WRVJTSU9OIOS4jiAucnVieS12ZXJzaW9uIOS4reeahCBSdWJ5IOeJiOacrOS4gOiHtApBUkcgUlVCWV9WRVJTSU9OPTMuNC43CkZST00gPHlvdXItbmFtZXNwYWNlPi9kaGktcnVieTokUlVCWV9WRVJTSU9OLWRldiBBUyBiYXNlCgojIFJhaWxzIOW6lOeUqOS9jeS6juatpOWkhApXT1JLRElSIC9yYWlscwoKIyDlronoo4Xln7rnoYDljIUKIyDoi6Xkvb/nlKggU1FMaXRl77yM6K&#43;35bCGIGxpYnBxLWRldiDmm7/mjaLkuLogc3FsaXRlM&#43;&#43;8m&#43;iLpeS9v&#43;eUqCBNeVNRTO&#43;8jOivt&#43;abv&#43;aNouS4uiBsaWJteXNxbGNsaWVudC1kZXYKUlVOIGFwdC1nZXQgdXBkYXRlIC1xcSAmJiBcCiAgICBhcHQtZ2V0IGluc3RhbGwgLS1uby1pbnN0YWxsLXJlY29tbWVuZHMgLXkgY3VybCBsaWJqZW1hbGxvYzIgbGlidmlwcyBsaWJwcS1kZXYgJiYgXAogICAgcm0gLXJmIC92YXIvbGliL2FwdC9saXN0cyAvdmFyL2NhY2hlL2FwdC9hcmNoaXZlcwoKIyDorr7nva7nlJ/kuqfnjq/looMKRU5WIFJBSUxTX0VOVj0icHJvZHVjdGlvbiIgXAogICAgQlVORExFX0RFUExPWU1FTlQ9IjEiIFwKICAgIEJVTkRMRV9QQVRIPSIvdXNyL2xvY2FsL2J1bmRsZSIgXAogICAgQlVORExFX1dJVEhPVVQ9ImRldmVsb3BtZW50IgoKIyDkvb/nlKjkuLTml7bmnoTlu7rpmLbmrrXku6Xlh4/lsJHmnIDnu4jplZzlg4/lpKflsI8KRlJPTSBiYXNlIEFTIGJ1aWxkCgojIOWuieijheaehOW7uiBnZW1zIOaJgOmcgOeahOWMhQpSVU4gYXB0LWdldCB1cGRhdGUgLXFxICYmIFwKICAgIGFwdC1nZXQgaW5zdGFsbCAtLW5vLWluc3RhbGwtcmVjb21tZW5kcyAteSBidWlsZC1lc3NlbnRpYWwgY3VybCBnaXQgcGtnLWNvbmZpZyBsaWJ5YW1sLWRldiAmJiBcCiAgICBybSAtcmYgL3Zhci9saWIvYXB0L2xpc3RzIC92YXIvY2FjaGUvYXB0L2FyY2hpdmVzCgojIOWuieijhSBKYXZhU2NyaXB0IOS&#43;nei1luWSjCBOb2RlLmpzIOS7pee8luivkei1hOa6kAojCiMg6Iul5L2/55SoIE5vZGVKUyDnvJbor5HotYTmupDvvIzor7flj5bmtojms6jph4rku6XkuIvooYwKIwojIEFSRyBOT0RFX1ZFUlNJT049MTguMTIuMAojIEFSRyBZQVJOX1ZFUlNJT049MS4yMi4xOQojIEVOViBQQVRIPS91c3IvbG9jYWwvbm9kZS9iaW46JFBBVEgKIyBSVU4gY3VybCAtc0wgaHR0cHM6Ly9naXRodWIuY29tL25vZGVudi9ub2RlLWJ1aWxkL2FyY2hpdmUvbWFzdGVyLnRhci5neiB8IHRhciB4eiAtQyAvdG1wLyAmJiBcCiMgICAgIC90bXAvbm9kZS1idWlsZC1tYXN0ZXIvYmluL25vZGUtYnVpbGQgIiR7Tk9ERV9WRVJTSU9OfSIgL3Vzci9sb2NhbC9ub2RlICYmIFwKIyAgICAgbnBtIGluc3RhbGwgLWcgeWFybkAkWUFSTl9WRVJTSU9OICYmIFwKIyAgICAgbnBtIGluc3RhbGwgLWcgbWptbCAmJiBcCiMgICAgIHJtIC1yZiAvdG1wL25vZGUtYnVpbGQtbWFzdGVyCgojIOWuieijheW6lOeUqCBnZW1zCkNPUFkgR2VtZmlsZSBHZW1maWxlLmxvY2sgLi8KUlVOIGJ1bmRsZSBpbnN0YWxsICYmIFwKICAgIHJtIC1yZiB&#43;Ly5idW5kbGUvICIke0JVTkRMRV9QQVRIfSIvcnVieS8qL2NhY2hlICIke0JVTkRMRV9QQVRIfSIvcnVieS8qL2J1bmRsZXIvZ2Vtcy8qLy5naXQgJiYgXAogICAgYnVuZGxlIGV4ZWMgYm9vdHNuYXAgcHJlY29tcGlsZSAtLWdlbWZpbGUKCiMg5a6J6KOFIG5vZGUgbW9kdWxlcwojCiMg6Iul5L2/55SoIE5vZGVKUyDnvJbor5HotYTmupDvvIzor7flj5bmtojms6jph4rku6XkuIvooYwKIwojIENPUFkgcGFja2FnZS5qc29uIHlhcm4ubG9jayAuLwojIFJVTiAtLW1vdW50PXR5cGU9Y2FjaGUsaWQ9eWFybix0YXJnZXQ9L3JhaWxzLy5jYWNoZS95YXJuIFlBUk5fQ0FDSEVfRk9MREVSPS9yYWlscy8uY2FjaGUveWFybiBcCiMgICAgIHlhcm4gaW5zdGFsbCAtLWZyb3plbi1sb2NrZmlsZQoKIyDlpI3liLblupTnlKjku6PnoIEKQ09QWSAuIC4KCiMg6aKE57yW6K&#43;RIGJvb3RzbmFwIOS7o&#43;eggeS7peaPkOWNh&#43;WQr&#43;WKqOmAn&#43;W6pgpSVU4gYnVuZGxlIGV4ZWMgYm9vdHNuYXAgcHJlY29tcGlsZSBhcHAvIGxpYi8KCiMg5peg6ZyA5a&#43;G6ZKlIFJBSUxTX01BU1RFUl9LRVkg5Y2z5Y&#43;v6aKE57yW6K&#43;R55Sf5Lqn6LWE5rqQClJVTiBTRUNSRVRfS0VZX0JBU0VfRFVNTVk9MSAuL2Jpbi9yYWlscyBhc3NldHM6cHJlY29tcGlsZQoKIyDlupTnlKjplZzlg4/nmoTmnIDnu4jpmLbmrrUKRlJPTSBiYXNlCgojIOWkjeWItuaehOW7uuS6p&#43;eJqe&#43;8mmdlbXMg5ZKM5bqU55SoCkNPUFkgLS1mcm9tPWJ1aWxkICIke0JVTkRMRV9QQVRIfSIgIiR7QlVORExFX1BBVEh9IgpDT1BZIC0tZnJvbT1idWlsZCAvcmFpbHMgL3JhaWxzCgojIOS7pemdniByb290IOeUqOaIt&#43;i/kOihjOW5tuS7heaLpeaciei/kOihjOaXtuaWh&#43;S7tu&#43;8jOaPkOWNh&#43;WuieWFqOaApwpSVU4gZ3JvdXBhZGQgLS1zeXN0ZW0gLS1naWQgMTAwMCByYWlscyAmJiBcCiAgICB1c2VyYWRkIHJhaWxzIC0tdWlkIDEwMDAgLS1naWQgMTAwMCAtLWNyZWF0ZS1ob21lIC0tc2hlbGwgL2Jpbi9iYXNoICYmIFwKICAgIGNob3duIC1SIHJhaWxzOnJhaWxzIGRiIGxvZyBzdG9yYWdlIHRtcApVU0VSIDEwMDA6MTAwMAoKIyDlhaXlj6PohJrmnKzlh4blpIfmlbDmja7lupMKRU5UUllQT0lOVCBbIi9yYWlscy9iaW4vZG9ja2VyLWVudHJ5cG9pbnQiXQoKIyDpu5jorqTpgJrov4cgVGhydXN0ZXIg5ZCv5Yqo5pyN5Yqh5Zmo77yM6L&#43;Q6KGM5pe25Y&#43;v6KaG55uWCkVYUE9TRSA4MApDTUQgWyIuL2Jpbi90aHJ1c3QiLCAiLi9iaW4vcmFpbHMiLCAic2VydmVyIl0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># check=error=true</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 此 Dockerfile 专为生产环境设计，非开发环境。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># docker build -t app .</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># docker run -d -p 80:80 -e RAILS_MASTER_KEY=&lt;config/master.key 中的值&gt; --name app app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 如需容器化开发环境，请参阅 Dev Containers：https://guides.rubyonrails.org/getting_started_with_devcontainer.html</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 确保 RUBY_VERSION 与 .ruby-version 中的 Ruby 版本一致</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ARG</span> <span class="nv">RUBY_VERSION</span><span class="o">=</span><span class="m">3</span>.4.7<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> &lt;your-namespace&gt;/dhi-ruby:$RUBY_VERSION-dev AS base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># Rails 应用位于此处</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">WORKDIR</span><span class="s"> /rails</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装基础包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 若使用 SQLite，请将 libpq-dev 替换为 sqlite3；若使用 MySQL，请替换为 libmysqlclient-dev</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> apt-get update -qq <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    rm -rf /var/lib/apt/lists /var/cache/apt/archives<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置生产环境</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">RAILS_ENV</span><span class="o">=</span><span class="s2">&#34;production&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">BUNDLE_DEPLOYMENT</span><span class="o">=</span><span class="s2">&#34;1&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">BUNDLE_PATH</span><span class="o">=</span><span class="s2">&#34;/usr/local/bundle&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">BUNDLE_WITHOUT</span><span class="o">=</span><span class="s2">&#34;development&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 使用临时构建阶段以减少最终镜像大小</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> base AS build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装构建 gems 所需的包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> apt-get update -qq <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    rm -rf /var/lib/apt/lists /var/cache/apt/archives<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装 JavaScript 依赖和 Node.js 以编译资源</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 若使用 NodeJS 编译资源，请取消注释以下行</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ARG NODE_VERSION=18.12.0</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ARG YARN_VERSION=1.22.19</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ENV PATH=/usr/local/node/bin:$PATH</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#     /tmp/node-build-master/bin/node-build &#34;${NODE_VERSION}&#34; /usr/local/node &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#     npm install -g yarn@$YARN_VERSION &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#     npm install -g mjml &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#     rm -rf /tmp/node-build-master</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装应用 gems</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> Gemfile Gemfile.lock ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> bundle install <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    rm -rf ~/.bundle/ <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span>/ruby/*/cache <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span>/ruby/*/bundler/gems/*/.git <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    bundle <span class="nb">exec</span> bootsnap precompile --gemfile<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装 node modules</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 若使用 NodeJS 编译资源，请取消注释以下行</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># COPY package.json yarn.lock ./</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#     yarn install --frozen-lockfile</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 复制应用代码</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 预编译 bootsnap 代码以提升启动速度</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> bundle <span class="nb">exec</span> bootsnap precompile app/ lib/<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 无需密钥 RAILS_MASTER_KEY 即可预编译生产资源</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> <span class="nv">SECRET_KEY_BASE_DUMMY</span><span class="o">=</span><span class="m">1</span> ./bin/rails assets:precompile<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 应用镜像的最终阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 复制构建产物：gems 和应用</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>build <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span> <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>build /rails /rails<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 以非 root 用户运行并仅拥有运行时文件，提升安全性</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> groupadd --system --gid <span class="m">1000</span> rails <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    useradd rails --uid <span class="m">1000</span> --gid <span class="m">1000</span> --create-home --shell /bin/bash <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    chown -R rails:rails db log storage tmp<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">USER</span><span class="s"> 1000:1000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 入口脚本准备数据库</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENTRYPOINT</span> <span class="p">[</span><span class="s2">&#34;/rails/bin/docker-entrypoint&#34;</span><span class="p">]</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 默认通过 Thruster 启动服务器，运行时可覆盖</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">EXPOSE</span><span class="s"> 80</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;./bin/thrust&#34;</span><span class="p">,</span> <span class="s2">&#34;./bin/rails&#34;</span><span class="p">,</span> <span class="s2">&#34;server&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8%E5%AE%98%E6%96%B9-Docker-%E9%95%9C%E5%83%8F' && 'hidden'"
      >
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
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQojIGNoZWNrPWVycm9yPXRydWUKCiMg5q2kIERvY2tlcmZpbGUg5LiT5Li655Sf5Lqn546v5aKD6K6&#43;6K6h77yM6Z2e5byA5Y&#43;R546v5aKD44CCCiMgZG9ja2VyIGJ1aWxkIC10IGFwcCAuCiMgZG9ja2VyIHJ1biAtZCAtcCA4MDo4MCAtZSBSQUlMU19NQVNURVJfS0VZPTxjb25maWcvbWFzdGVyLmtleSDkuK3nmoTlgLw&#43;IC0tbmFtZSBhcHAgYXBwCgojIOWmgumcgOWuueWZqOWMluW8gOWPkeeOr&#43;Wig&#43;&#43;8jOivt&#43;WPgumYhSBEZXYgQ29udGFpbmVyc&#43;&#43;8mmh0dHBzOi8vZ3VpZGVzLnJ1YnlvbnJhaWxzLm9yZy9nZXR0aW5nX3N0YXJ0ZWRfd2l0aF9kZXZjb250YWluZXIuaHRtbAoKIyDnoa7kv50gUlVCWV9WRVJTSU9OIOS4jiAucnVieS12ZXJzaW9uIOS4reeahCBSdWJ5IOeJiOacrOS4gOiHtApBUkcgUlVCWV9WRVJTSU9OPTMuNC43CkZST00gZG9ja2VyLmlvL2xpYnJhcnkvcnVieTokUlVCWV9WRVJTSU9OLXNsaW0gQVMgYmFzZQoKIyBSYWlscyDlupTnlKjkvY3kuo7mraTlpIQKV09SS0RJUiAvcmFpbHMKCiMg5a6J6KOF5Z&#43;656GA5YyFCiMg6Iul5L2/55SoIFNRTGl0Ze&#43;8jOivt&#43;WwhiBsaWJwcS1kZXYg5pu/5o2i5Li6IHNxbGl0ZTPvvJvoi6Xkvb/nlKggTXlTUUzvvIzor7fmm7/mjaLkuLogbGlibXlzcWxjbGllbnQtZGV2ClJVTiBhcHQtZ2V0IHVwZGF0ZSAtcXEgJiYgXAogICAgYXB0LWdldCBpbnN0YWxsIC0tbm8taW5zdGFsbC1yZWNvbW1lbmRzIC15IGN1cmwgbGliamVtYWxsb2MyIGxpYnZpcHMgbGlicHEtZGV2ICYmIFwKICAgIHJtIC1yZiAvdmFyL2xpYi9hcHQvbGlzdHMgL3Zhci9jYWNoZS9hcHQvYXJjaGl2ZXMKCiMg6K6&#43;572u55Sf5Lqn546v5aKDCkVOViBSQUlMU19FTlY9InByb2R1Y3Rpb24iIFwKICAgIEJVTkRMRV9ERVBMT1lNRU5UPSIxIiBcCiAgICBCVU5ETEVfUEFUSD0iL3Vzci9sb2NhbC9idW5kbGUiIFwKICAgIEJVTkRMRV9XSVRIT1VUPSJkZXZlbG9wbWVudCIKCiMg5L2/55So5Li05pe25p6E5bu66Zi25q615Lul5YeP5bCR5pyA57uI6ZWc5YOP5aSn5bCPCkZST00gYmFzZSBBUyBidWlsZAoKIyDlronoo4XmnoTlu7ogZ2VtcyDmiYDpnIDnmoTljIUKUlVOIGFwdC1nZXQgdXBkYXRlIC1xcSAmJiBcCiAgICBhcHQtZ2V0IGluc3RhbGwgLS1uby1pbnN0YWxsLXJlY29tbWVuZHMgLXkgYnVpbGQtZXNzZW50aWFsIGN1cmwgZ2l0IHBrZy1jb25maWcgbGlieWFtbC1kZXYgJiYgXAogICAgcm0gLXJmIC92YXIvbGliL2FwdC9saXN0cyAvdmFyL2NhY2hlL2FwdC9hcmNoaXZlcwoKIyDlronoo4UgSmF2YVNjcmlwdCDkvp3otZblkowgTm9kZS5qcyDku6XnvJbor5HotYTmupAKIwojIOiLpeS9v&#43;eUqCBOb2RlSlMg57yW6K&#43;R6LWE5rqQ77yM6K&#43;35Y&#43;W5raI5rOo6YeK5Lul5LiL6KGMCiMKIyBBUkcgTk9ERV9WRVJTSU9OPTE4LjEyLjAKIyBBUkcgWUFSTl9WRVJTSU9OPTEuMjIuMTkKIyBFTlYgUEFUSD0vdXNyL2xvY2FsL25vZGUvYmluOiRQQVRICiMgUlVOIGN1cmwgLXNMIGh0dHBzOi8vZ2l0aHViLmNvbS9ub2RlbnYvbm9kZS1idWlsZC9hcmNoaXZlL21hc3Rlci50YXIuZ3ogfCB0YXIgeHogLUMgL3RtcC8gJiYgXAojICAgICAvdG1wL25vZGUtYnVpbGQtbWFzdGVyL2Jpbi9ub2RlLWJ1aWxkICIke05PREVfVkVSU0lPTn0iIC91c3IvbG9jYWwvbm9kZSAmJiBcCiMgICAgIG5wbSBpbnN0YWxsIC1nIHlhcm5AJFlBUk5fVkVSU0lPTiAmJiBcCiMgICAgIG5wbSBpbnN0YWxsIC1nIG1qbWwgJiYgXAojICAgICBybSAtcmYgL3RtcC9ub2RlLWJ1aWxkLW1hc3RlcgoKIyDlronoo4XlupTnlKggZ2VtcwpDT1BZIEdlbWZpbGUgR2VtZmlsZS5sb2NrIC4vClJVTiBidW5kbGUgaW5zdGFsbCAmJiBcCiAgICBybSAtcmYgfi8uYnVuZGxlLyAiJHtCVU5ETEVfUEFUSH0iL3J1YnkvKi9jYWNoZSAiJHtCVU5ETEVfUEFUSH0iL3J1YnkvKi9idW5kbGVyL2dlbXMvKi8uZ2l0ICYmIFwKICAgIGJ1bmRsZSBleGVjIGJvb3RzbmFwIHByZWNvbXBpbGUgLS1nZW1maWxlCgojIOWuieijhSBub2RlIG1vZHVsZXMKIwojIOiLpeS9v&#43;eUqCBOb2RlSlMg57yW6K&#43;R6LWE5rqQ77yM6K&#43;35Y&#43;W5raI5rOo6YeK5Lul5LiL6KGMCiMKIyBDT1BZIHBhY2thZ2UuanNvbiB5YXJuLmxvY2sgLi8KIyBSVU4gLS1tb3VudD10eXBlPWNhY2hlLGlkPXlhcm4sdGFyZ2V0PS9yYWlscy8uY2FjaGUveWFybiBZQVJOX0NBQ0hFX0ZPTERFUj0vcmFpbHMvLmNhY2hlL3lhcm4gXAojICAgICB5YXJuIGluc3RhbGwgLS1mcm96ZW4tbG9ja2ZpbGUKCiMg5aSN5Yi25bqU55So5Luj56CBCkNPUFkgLiAuCgojIOmihOe8luivkSBib290c25hcCDku6PnoIHku6Xmj5DljYflkK/liqjpgJ/luqYKUlVOIGJ1bmRsZSBleGVjIGJvb3RzbmFwIHByZWNvbXBpbGUgYXBwLyBsaWIvCgojIOaXoOmcgOWvhumSpSBSQUlMU19NQVNURVJfS0VZIOWNs&#43;WPr&#43;mihOe8luivkeeUn&#43;S6p&#43;i1hOa6kApSVU4gU0VDUkVUX0tFWV9CQVNFX0RVTU1ZPTEgLi9iaW4vcmFpbHMgYXNzZXRzOnByZWNvbXBpbGUKCiMg5bqU55So6ZWc5YOP55qE5pyA57uI6Zi25q61CkZST00gYmFzZQoKIyDlpI3liLbmnoTlu7rkuqfnianvvJpnZW1zIOWSjOW6lOeUqApDT1BZIC0tZnJvbT1idWlsZCAiJHtCVU5ETEVfUEFUSH0iICIke0JVTkRMRV9QQVRIfSIKQ09QWSAtLWZyb209YnVpbGQgL3JhaWxzIC9yYWlscwoKIyDku6XpnZ4gcm9vdCDnlKjmiLfov5DooYzlubbku4Xmi6XmnInov5DooYzml7bmlofku7bvvIzmj5DljYflronlhajmgKcKUlVOIGdyb3VwYWRkIC0tc3lzdGVtIC0tZ2lkIDEwMDAgcmFpbHMgJiYgXAogICAgdXNlcmFkZCByYWlscyAtLXVpZCAxMDAwIC0tZ2lkIDEwMDAgLS1jcmVhdGUtaG9tZSAtLXNoZWxsIC9iaW4vYmFzaCAmJiBcCiAgICBjaG93biAtUiByYWlsczpyYWlscyBkYiBsb2cgc3RvcmFnZSB0bXAKVVNFUiAxMDAwOjEwMDAKCiMg5YWl5Y&#43;j6ISa5pys5YeG5aSH5pWw5o2u5bqTCkVOVFJZUE9JTlQgWyIvcmFpbHMvYmluL2RvY2tlci1lbnRyeXBvaW50Il0KCiMg6buY6K6k6YCa6L&#43;HIFRocnVzdGVyIOWQr&#43;WKqOacjeWKoeWZqO&#43;8jOi/kOihjOaXtuWPr&#43;imhueblgpFWFBPU0UgODAKQ01EIFsiLi9iaW4vdGhydXN0IiwgIi4vYmluL3JhaWxzIiwgInNlcnZlciJd', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># check=error=true</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 此 Dockerfile 专为生产环境设计，非开发环境。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># docker build -t app .</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># docker run -d -p 80:80 -e RAILS_MASTER_KEY=&lt;config/master.key 中的值&gt; --name app app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 如需容器化开发环境，请参阅 Dev Containers：https://guides.rubyonrails.org/getting_started_with_devcontainer.html</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 确保 RUBY_VERSION 与 .ruby-version 中的 Ruby 版本一致</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ARG</span> <span class="nv">RUBY_VERSION</span><span class="o">=</span><span class="m">3</span>.4.7<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> docker.io/library/ruby:$RUBY_VERSION-slim AS base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># Rails 应用位于此处</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">WORKDIR</span><span class="s"> /rails</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装基础包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 若使用 SQLite，请将 libpq-dev 替换为 sqlite3；若使用 MySQL，请替换为 libmysqlclient-dev</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> apt-get update -qq <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    rm -rf /var/lib/apt/lists /var/cache/apt/archives<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置生产环境</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">RAILS_ENV</span><span class="o">=</span><span class="s2">&#34;production&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">BUNDLE_DEPLOYMENT</span><span class="o">=</span><span class="s2">&#34;1&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">BUNDLE_PATH</span><span class="o">=</span><span class="s2">&#34;/usr/local/bundle&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">BUNDLE_WITHOUT</span><span class="o">=</span><span class="s2">&#34;development&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 使用临时构建阶段以减少最终镜像大小</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> base AS build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装构建 gems 所需的包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> apt-get update -qq <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    rm -rf /var/lib/apt/lists /var/cache/apt/archives<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装 JavaScript 依赖和 Node.js 以编译资源</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 若使用 NodeJS 编译资源，请取消注释以下行</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ARG NODE_VERSION=18.12.0</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ARG YARN_VERSION=1.22.19</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ENV PATH=/usr/local/node/bin:$PATH</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#     /tmp/node-build-master/bin/node-build &#34;${NODE_VERSION}&#34; /usr/local/node &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#     npm install -g yarn@$YARN_VERSION &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#     npm install -g mjml &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#     rm -rf /tmp/node-build-master</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装应用 gems</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> Gemfile Gemfile.lock ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> bundle install <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    rm -rf ~/.bundle/ <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span>/ruby/*/cache <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span>/ruby/*/bundler/gems/*/.git <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    bundle <span class="nb">exec</span> bootsnap precompile --gemfile<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装 node modules</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 若使用 NodeJS 编译资源，请取消注释以下行</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># COPY package.json yarn.lock ./</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c">#     yarn install --frozen-lockfile</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 复制应用代码</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 预编译 bootsnap 代码以提升启动速度</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> bundle <span class="nb">exec</span> bootsnap precompile app/ lib/<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 无需密钥 RAILS_MASTER_KEY 即可预编译生产资源</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> <span class="nv">SECRET_KEY_BASE_DUMMY</span><span class="o">=</span><span class="m">1</span> ./bin/rails assets:precompile<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 应用镜像的最终阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 复制构建产物：gems 和应用</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>build <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span> <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>build /rails /rails<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 以非 root 用户运行并仅拥有运行时文件，提升安全性</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> groupadd --system --gid <span class="m">1000</span> rails <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    useradd rails --uid <span class="m">1000</span> --gid <span class="m">1000</span> --create-home --shell /bin/bash <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    chown -R rails:rails db log storage tmp<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">USER</span><span class="s"> 1000:1000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 入口脚本准备数据库</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENTRYPOINT</span> <span class="p">[</span><span class="s2">&#34;/rails/bin/docker-entrypoint&#34;</span><span class="p">]</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 默认通过 Thruster 启动服务器，运行时可覆盖</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">EXPOSE</span><span class="s"> 80</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;./bin/thrust&#34;</span><span class="p">,</span> <span class="s2">&#34;./bin/rails&#34;</span><span class="p">,</span> <span class="s2">&#34;server&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


上述 Dockerfile 假设你将 Thruster 与 Puma 作为应用服务器一起使用。如果你使用其他服务器，可将最后三行替换为以下内容：

```dockerfile
# 启动应用服务器
EXPOSE 3000
CMD ["./bin/rails", "server"]
```

此 Dockerfile 使用 `./bin/docker-entrypoint` 脚本作为容器的入口点。该脚本准备数据库并运行应用服务器。以下是该脚本的示例。

```bash {title=docker-entrypoint}
#!/bin/bash -e

# 启用 jemalloc 以减少内存使用和延迟。
if [ -z "${LD_PRELOAD+x}" ]; then
    LD_PRELOAD=$(find /usr/lib -name libjemalloc.so.2 -print -quit)
    export LD_PRELOAD
fi

# 若运行 rails server，则创建或迁移现有数据库
if [ "${@: -2:1}" == "./bin/rails" ] && [ "${@: -1:1}" == "server" ]; then
  ./bin/rails db:prepare
fi

exec "${@}"
```

除了上述两个文件，你还需要 `.dockerignore` 文件。该文件用于排除构建上下文中的文件和目录。以下是 `.dockerignore` 文件的示例。

```text {collapse=true,title=".dockerignore"}
# 详见 https://docs.docker.com/engine/reference/builder/#dockerignore-file 了解忽略文件的更多信息。

# 忽略 git 目录。
/.git/
/.gitignore

# 忽略 bundler 配置。
/.bundle

# 忽略所有环境文件。
/.env*

# 忽略所有默认密钥文件。
/config/master.key
/config/credentials/*.key

# 忽略所有日志文件和临时文件。
/log/*
/tmp/*
!/log/.keep
!/tmp/.keep

# 忽略 pid 文件，但保留目录。
/tmp/pids/*
!/tmp/pids/.keep

# 忽略存储（开发中的上传文件和任何 SQLite 数据库）。
/storage/*
!/storage/.keep
/tmp/storage/*
!/tmp/storage/.keep

# 忽略资源。
/node_modules/
/app/assets/builds/*
!/app/assets/builds/.keep
/public/assets

# 忽略 CI 服务文件。
/.github

# 忽略开发文件
/.devcontainer

# 忽略 Docker 相关文件
/.dockerignore
/Dockerfile*
```

最后一个可选文件是 `compose.yaml`，Docker Compose 使用它定义应用的各个服务。由于使用 SQLite 作为数据库，无需定义单独的数据库服务。唯一需要的服务是 Rails 应用本身。

```yaml {title=compose.yaml}
services:
  web:
    build: .
    environment:
      - RAILS_MASTER_KEY
    ports:
      - "3000:80"
```

现在你的应用文件夹中应包含以下文件：

- `.dockerignore`
- `compose.yaml`
- `Dockerfile`
- `bin/docker-entrypoint`

如需了解更多文件信息，请参阅：

- [Dockerfile](/reference/dockerfile)
- [.dockerignore](/reference/dockerfile#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)
- [docker-entrypoint](/reference/dockerfile/#entrypoint)

## 2. 运行应用

要在终端中运行应用，请在应用目录中执行以下命令。

```console
$ RAILS_MASTER_KEY=<master_key_value> docker compose up --build
```

在浏览器中访问 [http://localhost:3000](http://localhost:3000)。你应该能看到一个简单的 Ruby on Rails 应用。

在终端中按 `ctrl`+`c` 停止应用。

## 3. 在后台运行应用

添加 `-d` 选项可使应用在后台运行。在 `docker-ruby-on-rails` 目录中，于终端执行以下命令。

```console
$ docker compose up --build -d
```

在浏览器中访问 [http://localhost:3000](http://localhost:3000)。

你应该能看到一个简单的 Ruby on Rails 应用。

在终端中执行以下命令停止应用。

```console
$ docker compose down
```

更多 Compose 命令信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 小结

在本节中，你学会了如何使用 Docker 容器化并运行 Ruby 应用。

相关信息：

- [Docker Compose 概述](/manuals/compose/_index.md)

## 后续步骤

在下一节中，你将学习如何使用 GitHub Actions 设置 CI/CD 流水线。
