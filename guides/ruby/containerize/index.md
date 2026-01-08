# 容器化 Ruby on Rails 应用程序

## 先决条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您拥有 [Git 客户端](https://git-scm.com/downloads)。本节中的示例展示了 Git CLI，但您可以使用任何客户端。

## 概述

本节将引导您完成容器化和运行 [Ruby on Rails](https://rubyonrails.org/) 应用程序的过程。

从 Rails 7.1 开始，[开箱即用支持 Docker](https://guides.rubyonrails.org/7_1_release_notes.html#generate-dockerfiles-for-new-rails-applications)。这意味着当您创建新的 Rails 应用程序时，将为您生成 `Dockerfile`、`.dockerignore` 和 `bin/docker-entrypoint` 文件。

如果您有一个现有的 Rails 应用程序，则需要手动创建 Docker 资产。不幸的是，`docker init` 命令尚不支持 Rails。这意味着如果您使用 Rails，则需要从下面的示例中手动复制 Dockerfile 和其他相关配置。

## 1. 初始化 Docker 资产

Rails 7.1 及更新版本会开箱即用地生成多阶段 Dockerfile。以下是此类文件的两个版本：一个使用 Docker 硬化镜像 (DHIs)，另一个使用 Docker 官方镜像 (DOIs)。尽管 Dockerfile 是自动生成的，但了解其目的和功能非常重要。强烈建议查看以下示例。

[Docker 硬化镜像 (DHIs)](https://docs.docker.com/dhi/) 是由 Docker 维护的最小、安全且可用于生产的容器基础镜像和应用程序镜像。只要可能，都建议使用 DHIs 以获得更好的安全性。它们旨在减少漏洞并简化合规性，对所有人免费提供，无需订阅，没有使用限制，也没有供应商锁定。

多阶段 Dockerfile 通过分离构建和运行时依赖项，有助于创建更小、更高效的镜像，确保最终镜像中仅包含必要的组件。请在[多阶段构建指南](/get-started/docker-concepts/building-images/multi-stage-builds/)中阅读更多内容。








<div
  class="tabs"
  
    x-data="{ selected: '%E4%BD%BF%E7%94%A8-DHIs' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8-DHIs' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8-DHIs'"
        
      >
        使用 DHIs
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8-DOIs' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8-DOIs'"
        
      >
        使用 DOIs
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-DHIs' && 'hidden'"
      >
        <p>您必须先向 <code>dhi.io</code> 进行身份验证，然后才能拉取 Docker 硬化镜像。运行 <code>docker login dhi.io</code> 进行身份验证。</p>
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
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQojIGNoZWNrPWVycm9yPXRydWUKCiMg5q2kIERvY2tlcmZpbGUg5LiT5Li655Sf5Lqn546v5aKD6K6&#43;6K6h77yM6ICM6Z2e5byA5Y&#43;R546v5aKD44CCCiMgZG9ja2VyIGJ1aWxkIC10IGFwcCAuCiMgZG9ja2VyIHJ1biAtZCAtcCA4MDo4MCAtZSBSQUlMU19NQVNURVJfS0VZPTxjb25maWcvbWFzdGVyLmtleSDkuK3nmoTlgLw&#43;IC0tbmFtZSBhcHAgYXBwCgojIOacieWFs&#43;WuueWZqOWMluW8gOWPkeeOr&#43;Wig&#43;&#43;8jOivt&#43;WPgumYheW8gOWPkeWuueWZqO&#43;8mmh0dHBzOi8vZ3VpZGVzLnJ1YnlvbnJhaWxzLm9yZy9nZXR0aW5nX3N0YXJ0ZWRfd2l0aF9kZXZjb250YWluZXIuaHRtbAoKIyDnoa7kv50gUlVCWV9WRVJTSU9OIOS4jiAucnVieS12ZXJzaW9uIOS4reeahCBSdWJ5IOeJiOacrOWMuemFjQpBUkcgUlVCWV9WRVJTSU9OPTMuNC44CkZST00gZGhpLmlvL3J1Ynk6JFJVQllfVkVSU0lPTi1kZXYgQVMgYmFzZQoKIyBSYWlscyDlupTnlKjnqIvluo/kvY3kuo7mraTlpIQKV09SS0RJUiAvcmFpbHMKCiMg5a6J6KOF5Z&#43;656GA6L2v5Lu25YyFCiMg5aaC5p6c5L2/55SoIFNRTGl0Ze&#43;8jOivt&#43;WwhiBsaWJwcS1kZXYg5pu/5o2i5Li6IHNxbGl0ZTPvvJvlpoLmnpzkvb/nlKggTXlTUUzvvIzliJnmm7/mjaLkuLogbGlibXlzcWxjbGllbnQtZGV2ClJVTiBhcHQtZ2V0IHVwZGF0ZSAtcXEgJiYgXAogICAgYXB0LWdldCBpbnN0YWxsIC0tbm8taW5zdGFsbC1yZWNvbW1lbmRzIC15IGN1cmwgbGliamVtYWxsb2MyIGxpYnZpcHMgbGlicHEtZGV2ICYmIFwKICAgIHJtIC1yZiAvdmFyL2xpYi9hcHQvbGlzdHMgL3Zhci9jYWNoZS9hcHQvYXJjaGl2ZXMKCiMg6K6&#43;572u55Sf5Lqn546v5aKDCkVOViBSQUlMU19FTlY9InByb2R1Y3Rpb24iIFwKICAgIEJVTkRMRV9ERVBMT1lNRU5UPSIxIiBcCiAgICBCVU5ETEVfUEFUSD0iL3Vzci9sb2NhbC9idW5kbGUiIFwKICAgIEJVTkRMRV9XSVRIT1VUPSJkZXZlbG9wbWVudCIKCiMg55So5LqO5YeP5bCP5pyA57uI6ZWc5YOP5aSn5bCP55qE5Li05pe25p6E5bu66Zi25q61CkZST00gYmFzZSBBUyBidWlsZAoKIyDlronoo4XmnoTlu7ogZ2VtcyDmiYDpnIDnmoTova/ku7bljIUKUlVOIGFwdC1nZXQgdXBkYXRlIC1xcSAmJiBcCiAgICBhcHQtZ2V0IGluc3RhbGwgLS1uby1pbnN0YWxsLXJlY29tbWVuZHMgLXkgYnVpbGQtZXNzZW50aWFsIGN1cmwgZ2l0IHBrZy1jb25maWcgbGlieWFtbC1kZXYgJiYgXAogICAgcm0gLXJmIC92YXIvbGliL2FwdC9saXN0cyAvdmFyL2NhY2hlL2FwdC9hcmNoaXZlcwoKIyDlronoo4UgSmF2YVNjcmlwdCDkvp3otZbpobnlkowgTm9kZS5qcyDku6XnvJbor5HotYTkuqcKIwojIOWmguaenOaCqOS9v&#43;eUqCBOb2RlSlMg6ZyA6KaB57yW6K&#43;R6LWE5Lqn77yM6K&#43;35Y&#43;W5raI5rOo6YeK5Lul5LiL5Yeg6KGMCiMKIyBBUkcgTk9ERV9WRVJTSU9OPTE4LjEyLjAKIyBBUkcgWUFSTl9WRVJTSU9OPTEuMjIuMTkKIyBFTlYgUEFUSD0vdXNyL2xvY2FsL25vZGUvYmluOiRQQVRICiMgUlVOIGN1cmwgLXNMIGh0dHBzOi8vZ2l0aHViLmNvbS9ub2RlbnYvbm9kZS1idWlsZC9hcmNoaXZlL21hc3Rlci50YXIuZ3ogfCB0YXIgeHogLUMgL3RtcC8gJiYgXAojICAgICAvdG1wL25vZGUtYnVpbGQtbWFzdGVyL2Jpbi9ub2RlLWJ1aWxkICIke05PREVfVkVSU0lPTn0iIC91c3IvbG9jYWwvbm9kZSAmJiBcCiMgICAgIG5wbSBpbnN0YWxsIC1nIHlhcm5AJFlBUk5fVkVSU0lPTiAmJiBcCiMgICAgIG5wbSBpbnN0YWxsIC1nIG1qbWwgJiYgXAojICAgICBybSAtcmYgL3RtcC9ub2RlLWJ1aWxkLW1hc3RlcgoKIyDlronoo4XlupTnlKjnqIvluo8gZ2VtcwpDT1BZIEdlbWZpbGUgR2VtZmlsZS5sb2NrIC4vClJVTiBidW5kbGUgaW5zdGFsbCAmJiBcCiAgICBybSAtcmYgfi8uYnVuZGxlLyAiJHtCVU5ETEVfUEFUSH0iL3J1YnkvKi9jYWNoZSAiJHtCVU5ETEVfUEFUSH0iL3J1YnkvKi9idW5kbGVyL2dlbXMvKi8uZ2l0ICYmIFwKICAgIGJ1bmRsZSBleGVjIGJvb3RzbmFwIHByZWNvbXBpbGUgLS1nZW1maWxlCgojIOWuieijhSBub2RlIOaooeWdlwojCiMg5aaC5p6c5oKo5L2/55SoIE5vZGVKUyDpnIDopoHnvJbor5HotYTkuqfvvIzor7flj5bmtojms6jph4rku6XkuIvlh6DooYwKIwojIENPUFkgcGFja2FnZS5qc29uIHlhcm4ubG9jayAuLwojIFJVTiAtLW1vdW50PXR5cGU9Y2FjaGUsaWQ9eWFybix0YXJnZXQ9L3JhaWxzLy5jYWNoZS95YXJuIFlBUk5fQ0FDSEVfRk9MREVSPS9yYWlscy8uY2FjaGUveWFybiBcCiMgICAgIHlhcm4gaW5zdGFsbCAtLWZyb3plbi1sb2NrZmlsZQoKIyDlpI3liLblupTnlKjnqIvluo/ku6PnoIEKQ09QWSAuIC4KCiMg6aKE57yW6K&#43;RIGJvb3RzbmFwIOS7o&#43;eggeS7peWKoOW/q&#43;WQr&#43;WKqOaXtumXtApSVU4gYnVuZGxlIGV4ZWMgYm9vdHNuYXAgcHJlY29tcGlsZSBhcHAvIGxpYi8KCiMg6aKE57yW6K&#43;R55Sf5Lqn546v5aKD6LWE5Lqn77yM5peg6ZyAIFJBSUxTX01BU1RFUl9LRVkg5a&#43;G6ZKlClJVTiBTRUNSRVRfS0VZX0JBU0VfRFVNTVk9MSAuL2Jpbi9yYWlscyBhc3NldHM6cHJlY29tcGlsZQoKIyDlupTnlKjnqIvluo/plZzlg4/nmoTmnIDnu4jpmLbmrrUKRlJPTSBiYXNlCgojIOWkjeWItuaehOW7uueahOW3peS7tu&#43;8mmdlbXPjgIHlupTnlKjnqIvluo8KQ09QWSAtLWZyb209YnVpbGQgIiR7QlVORExFX1BBVEh9IiAiJHtCVU5ETEVfUEFUSH0iCkNPUFkgLS1mcm9tPWJ1aWxkIC9yYWlscyAvcmFpbHMKCiMg5L2c5Li66Z2eIHJvb3Qg55So5oi36L&#43;Q6KGM5bm25LuF5oul5pyJ6L&#43;Q6KGM5pe25paH5Lu255qE5omA5pyJ5p2D77yM5Lul56Gu5L&#43;d5a6J5YWoClJVTiBncm91cGFkZCAtLXN5c3RlbSAtLWdpZCAxMDAwIHJhaWxzICYmIFwKICAgIHVzZXJhZGQgcmFpbHMgLS11aWQgMTAwMCAtLWdpZCAxMDAwIC0tY3JlYXRlLWhvbWUgLS1zaGVsbCAvYmluL2Jhc2ggJiYgXAogICAgY2hvd24gLVIgcmFpbHM6cmFpbHMgZGIgbG9nIHN0b3JhZ2UgdG1wClVTRVIgMTAwMDoxMDAwCgojIOWFpeWPo&#43;eCueeUqOS6juWHhuWkh&#43;aVsOaNruW6k&#43;OAggpFTlRSWVBPSU5UIFsiL3JhaWxzL2Jpbi9kb2NrZXItZW50cnlwb2ludCJdCgojIOm7mOiupOmAmui/hyBUaHJ1c3RlciDlkK/liqjmnI3liqHlmajvvIzov5nlj6/ku6XlnKjov5DooYzml7booqvopobnm5YKRVhQT1NFIDgwCkNNRCBbIi4vYmluL3RocnVzdCIsICIuL2Jpbi9yYWlscyIsICJzZXJ2ZXIiXQ==', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="c"># check=error=true</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 此 Dockerfile 专为生产环境设计，而非开发环境。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># docker build -t app .</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># docker run -d -p 80:80 -e RAILS_MASTER_KEY=&lt;config/master.key 中的值&gt; --name app app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 有关容器化开发环境，请参阅开发容器：https://guides.rubyonrails.org/getting_started_with_devcontainer.html</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 确保 RUBY_VERSION 与 .ruby-version 中的 Ruby 版本匹配</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ARG</span> <span class="nv">RUBY_VERSION</span><span class="o">=</span><span class="m">3</span>.4.8<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/ruby:$RUBY_VERSION-dev</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Rails 应用程序位于此处</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/rails</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 安装基础软件包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果使用 SQLite，请将 libpq-dev 替换为 sqlite3；如果使用 MySQL，则替换为 libmysqlclient-dev</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> apt-get update -qq <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    rm -rf /var/lib/apt/lists /var/cache/apt/archives<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 设置生产环境</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">RAILS_ENV</span><span class="o">=</span><span class="s2">&#34;production&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">BUNDLE_DEPLOYMENT</span><span class="o">=</span><span class="s2">&#34;1&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">BUNDLE_PATH</span><span class="o">=</span><span class="s2">&#34;/usr/local/bundle&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">BUNDLE_WITHOUT</span><span class="o">=</span><span class="s2">&#34;development&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 用于减小最终镜像大小的临时构建阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">base</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 安装构建 gems 所需的软件包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> apt-get update -qq <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    rm -rf /var/lib/apt/lists /var/cache/apt/archives<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 安装 JavaScript 依赖项和 Node.js 以编译资产</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果您使用 NodeJS 需要编译资产，请取消注释以下几行</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># ARG NODE_VERSION=18.12.0</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># ARG YARN_VERSION=1.22.19</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># ENV PATH=/usr/local/node/bin:$PATH</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#     /tmp/node-build-master/bin/node-build &#34;${NODE_VERSION}&#34; /usr/local/node &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#     npm install -g yarn@$YARN_VERSION &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#     npm install -g mjml &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#     rm -rf /tmp/node-build-master</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 安装应用程序 gems</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> Gemfile Gemfile.lock ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> bundle install <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    rm -rf ~/.bundle/ <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span>/ruby/*/cache <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span>/ruby/*/bundler/gems/*/.git <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    bundle <span class="nb">exec</span> bootsnap precompile --gemfile<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 安装 node 模块</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果您使用 NodeJS 需要编译资产，请取消注释以下几行</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># COPY package.json yarn.lock ./</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#     yarn install --frozen-lockfile</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 复制应用程序代码</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 预编译 bootsnap 代码以加快启动时间</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> bundle <span class="nb">exec</span> bootsnap precompile app/ lib/<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 预编译生产环境资产，无需 RAILS_MASTER_KEY 密钥</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> <span class="nv">SECRET_KEY_BASE_DUMMY</span><span class="o">=</span><span class="m">1</span> ./bin/rails assets:precompile<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 应用程序镜像的最终阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 复制构建的工件：gems、应用程序</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>build <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span> <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>build /rails /rails<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 作为非 root 用户运行并仅拥有运行时文件的所有权，以确保安全</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> groupadd --system --gid <span class="m">1000</span> rails <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    useradd rails --uid <span class="m">1000</span> --gid <span class="m">1000</span> --create-home --shell /bin/bash <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    chown -R rails:rails db log storage tmp<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">USER</span><span class="w"> </span><span class="s">1000:1000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 入口点用于准备数据库。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span><span class="s2">&#34;/rails/bin/docker-entrypoint&#34;</span><span class="p">]</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 默认通过 Thruster 启动服务器，这可以在运行时被覆盖</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">EXPOSE</span><span class="w"> </span><span class="s">80</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;./bin/thrust&#34;</span><span class="p">,</span> <span class="s2">&#34;./bin/rails&#34;</span><span class="p">,</span> <span class="s2">&#34;server&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-DOIs' && 'hidden'"
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
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQojIGNoZWNrPWVycm9yPXRydWUKCiMg5q2kIERvY2tlcmZpbGUg5LiT5Li655Sf5Lqn546v5aKD6K6&#43;6K6h77yM6ICM6Z2e5byA5Y&#43;R546v5aKD44CCCiMgZG9ja2VyIGJ1aWxkIC10IGFwcCAuCiMgZG9ja2VyIHJ1biAtZCAtcCA4MDo4MCAtZSBSQUlMU19NQVNURVJfS0VZPTxjb25maWcvbWFzdGVyLmtleSDkuK3nmoTlgLw&#43;IC0tbmFtZSBhcHAgYXBwCgojIOacieWFs&#43;WuueWZqOWMluW8gOWPkeeOr&#43;Wig&#43;&#43;8jOivt&#43;WPgumYheW8gOWPkeWuueWZqO&#43;8mmh0dHBzOi8vZ3VpZGVzLnJ1YnlvbnJhaWxzLm9yZy9nZXR0aW5nX3N0YXJ0ZWRfd2l0aF9kZXZjb250YWluZXIuaHRtbAoKIyDnoa7kv50gUlVCWV9WRVJTSU9OIOS4jiAucnVieS12ZXJzaW9uIOS4reeahCBSdWJ5IOeJiOacrOWMuemFjQpBUkcgUlVCWV9WRVJTSU9OPTMuNC44CkZST00gZG9ja2VyLmlvL2xpYnJhcnkvcnVieTokUlVCWV9WRVJTSU9OLXNsaW0gQVMgYmFzZQoKIyBSYWlscyDlupTnlKjnqIvluo/kvY3kuo7mraTlpIQKV09SS0RJUiAvcmFpbHMKCiMg5a6J6KOF5Z&#43;656GA6L2v5Lu25YyFCiMg5aaC5p6c5L2/55SoIFNRTGl0Ze&#43;8jOivt&#43;WwhiBsaWJwcS1kZXYg5pu/5o2i5Li6IHNxbGl0ZTPvvJvlpoLmnpzkvb/nlKggTXlTUUzvvIzliJnmm7/mjaLkuLogbGlibXlzcWxjbGllbnQtZGV2ClJVTiBhcHQtZ2V0IHVwZGF0ZSAtcXEgJiYgXAogICAgYXB0LWdldCBpbnN0YWxsIC0tbm8taW5zdGFsbC1yZWNvbW1lbmRzIC15IGN1cmwgbGliamVtYWxsb2MyIGxpYnZpcHMgbGlicHEtZGV2ICYmIFwKICAgIHJtIC1yZiAvdmFyL2xpYi9hcHQvbGlzdHMgL3Zhci9jYWNoZS9hcHQvYXJjaGl2ZXMKCiMg6K6&#43;572u55Sf5Lqn546v5aKDCkVOViBSQUlMU19FTlY9InByb2R1Y3Rpb24iIFwKICAgIEJVTkRMRV9ERVBMT1lNRU5UPSIxIiBcCiAgICBCVU5ETEVfUEFUSD0iL3Vzci9sb2NhbC9idW5kbGUiIFwKICAgIEJVTkRMRV9XSVRIT1VUPSJkZXZlbG9wbWVudCIKCiMg55So5LqO5YeP5bCP5pyA57uI6ZWc5YOP5aSn5bCP55qE5Li05pe25p6E5bu66Zi25q61CkZST00gYmFzZSBBUyBidWlsZAoKIyDlronoo4XmnoTlu7ogZ2VtcyDmiYDpnIDnmoTova/ku7bljIUKUlVOIGFwdC1nZXQgdXBkYXRlIC1xcSAmJiBcCiAgICBhcHQtZ2V0IGluc3RhbGwgLS1uby1pbnN0YWxsLXJlY29tbWVuZHMgLXkgYnVpbGQtZXNzZW50aWFsIGN1cmwgZ2l0IHBrZy1jb25maWcgbGlieWFtbC1kZXYgJiYgXAogICAgcm0gLXJmIC92YXIvbGliL2FwdC9saXN0cyAvdmFyL2NhY2hlL2FwdC9hcmNoaXZlcwoKIyDlronoo4UgSmF2YVNjcmlwdCDkvp3otZbpobnlkowgTm9kZS5qcyDku6XnvJbor5HotYTkuqcKIwojIOWmguaenOaCqOS9v&#43;eUqCBOb2RlSlMg6ZyA6KaB57yW6K&#43;R6LWE5Lqn77yM6K&#43;35Y&#43;W5raI5rOo6YeK5Lul5LiL5Yeg6KGMCiMKIyBBUkcgTk9ERV9WRVJTSU9OPTE4LjEyLjAKIyBBUkcgWUFSTl9WRVJTSU9OPTEuMjIuMTkKIyBFTlYgUEFUSD0vdXNyL2xvY2FsL25vZGUvYmluOiRQQVRICiMgUlVOIGN1cmwgLXNMIGh0dHBzOi8vZ2l0aHViLmNvbS9ub2RlbnYvbm9kZS1idWlsZC9hcmNoaXZlL21hc3Rlci50YXIuZ3ogfCB0YXIgeHogLUMgL3RtcC8gJiYgXAojICAgICAvdG1wL25vZGUtYnVpbGQtbWFzdGVyL2Jpbi9ub2RlLWJ1aWxkICIke05PREVfVkVSU0lPTn0iIC91c3IvbG9jYWwvbm9kZSAmJiBcCiMgICAgIG5wbSBpbnN0YWxsIC1nIHlhcm5AJFlBUk5fVkVSU0lPTiAmJiBcCiMgICAgIG5wbSBpbnN0YWxsIC1nIG1qbWwgJiYgXAojICAgICBybSAtcmYgL3RtcC9ub2RlLWJ1aWxkLW1hc3RlcgoKIyDlronoo4XlupTnlKjnqIvluo8gZ2VtcwpDT1BZIEdlbWZpbGUgR2VtZmlsZS5sb2NrIC4vClJVTiBidW5kbGUgaW5zdGFsbCAmJiBcCiAgICBybSAtcmYgfi8uYnVuZGxlLyAiJHtCVU5ETEVfUEFUSH0iL3J1YnkvKi9jYWNoZSAiJHtCVU5ETEVfUEFUSH0iL3J1YnkvKi9idW5kbGVyL2dlbXMvKi8uZ2l0ICYmIFwKICAgIGJ1bmRsZSBleGVjIGJvb3RzbmFwIHByZWNvbXBpbGUgLS1nZW1maWxlCgojIOWuieijhSBub2RlIOaooeWdlwojCiMg5aaC5p6c5oKo5L2/55SoIE5vZGVKUyDpnIDopoHnvJbor5HotYTkuqfvvIzor7flj5bmtojms6jph4rku6XkuIvlh6DooYwKIwojIENPUFkgcGFja2FnZS5qc29uIHlhcm4ubG9jayAuLwojIFJVTiAtLW1vdW50PXR5cGU9Y2FjaGUsaWQ9eWFybix0YXJnZXQ9L3JhaWxzLy5jYWNoZS95YXJuIFlBUk5fQ0FDSEVfRk9MREVSPS9yYWlscy8uY2FjaGUveWFybiBcCiMgICAgIHlhcm4gaW5zdGFsbCAtLWZyb3plbi1sb2NrZmlsZQoKIyDlpI3liLblupTnlKjnqIvluo/ku6PnoIEKQ09QWSAuIC4KCiMg6aKE57yW6K&#43;RIGJvb3RzbmFwIOS7o&#43;eggeS7peWKoOW/q&#43;WQr&#43;WKqOaXtumXtApSVU4gYnVuZGxlIGV4ZWMgYm9vdHNuYXAgcHJlY29tcGlsZSBhcHAvIGxpYi8KCiMg6aKE57yW6K&#43;R55Sf5Lqn546v5aKD6LWE5Lqn77yM5peg6ZyAIFJBSUxTX01BU1RFUl9LRVkg5a&#43;G6ZKlClJVTiBTRUNSRVRfS0VZX0JBU0VfRFVNTVk9MSAuL2Jpbi9yYWlscyBhc3NldHM6cHJlY29tcGlsZQoKIyDlupTnlKjnqIvluo/plZzlg4/nmoTmnIDnu4jpmLbmrrUKRlJPTSBiYXNlCgojIOWkjeWItuaehOW7uueahOW3peS7tu&#43;8mmdlbXPjgIHlupTnlKjnqIvluo8KQ09QWSAtLWZyb209YnVpbGQgIiR7QlVORExFX1BBVEh9IiAiJHtCVU5ETEVfUEFUSH0iCkNPUFkgLS1mcm9tPWJ1aWxkIC9yYWlscyAvcmFpbHMKCiMg5L2c5Li66Z2eIHJvb3Qg55So5oi36L&#43;Q6KGM5bm25LuF5oul5pyJ6L&#43;Q6KGM5pe25paH5Lu255qE5omA5pyJ5p2D77yM5Lul56Gu5L&#43;d5a6J5YWoClJVTiBncm91cGFkZCAtLXN5c3RlbSAtLWdpZCAxMDAwIHJhaWxzICYmIFwKICAgIHVzZXJhZGQgcmFpbHMgLS11aWQgMTAwMCAtLWdpZCAxMDAwIC0tY3JlYXRlLWhvbWUgLS1zaGVsbCAvYmluL2Jhc2ggJiYgXAogICAgY2hvd24gLVIgcmFpbHM6cmFpbHMgZGIgbG9nIHN0b3JhZ2UgdG1wClVTRVIgMTAwMDoxMDAwCgojIOWFpeWPo&#43;eCueeUqOS6juWHhuWkh&#43;aVsOaNruW6k&#43;OAggpFTlRSWVBPSU5UIFsiL3JhaWxzL2Jpbi9kb2NrZXItZW50cnlwb2ludCJdCgojIOm7mOiupOmAmui/hyBUaHJ1c3RlciDlkK/liqjmnI3liqHlmajvvIzov5nlj6/ku6XlnKjov5DooYzml7booqvopobnm5YKRVhQT1NFIDgwCkNNRCBbIi4vYmluL3RocnVzdCIsICIuL2Jpbi9yYWlscyIsICJzZXJ2ZXIiXQ==', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="c"># check=error=true</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 此 Dockerfile 专为生产环境设计，而非开发环境。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># docker build -t app .</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># docker run -d -p 80:80 -e RAILS_MASTER_KEY=&lt;config/master.key 中的值&gt; --name app app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 有关容器化开发环境，请参阅开发容器：https://guides.rubyonrails.org/getting_started_with_devcontainer.html</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 确保 RUBY_VERSION 与 .ruby-version 中的 Ruby 版本匹配</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ARG</span> <span class="nv">RUBY_VERSION</span><span class="o">=</span><span class="m">3</span>.4.8<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">docker.io/library/ruby:$RUBY_VERSION-slim</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Rails 应用程序位于此处</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/rails</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 安装基础软件包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果使用 SQLite，请将 libpq-dev 替换为 sqlite3；如果使用 MySQL，则替换为 libmysqlclient-dev</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> apt-get update -qq <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    rm -rf /var/lib/apt/lists /var/cache/apt/archives<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 设置生产环境</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">RAILS_ENV</span><span class="o">=</span><span class="s2">&#34;production&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">BUNDLE_DEPLOYMENT</span><span class="o">=</span><span class="s2">&#34;1&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">BUNDLE_PATH</span><span class="o">=</span><span class="s2">&#34;/usr/local/bundle&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">BUNDLE_WITHOUT</span><span class="o">=</span><span class="s2">&#34;development&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 用于减小最终镜像大小的临时构建阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">base</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 安装构建 gems 所需的软件包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> apt-get update -qq <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    rm -rf /var/lib/apt/lists /var/cache/apt/archives<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 安装 JavaScript 依赖项和 Node.js 以编译资产</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果您使用 NodeJS 需要编译资产，请取消注释以下几行</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># ARG NODE_VERSION=18.12.0</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># ARG YARN_VERSION=1.22.19</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># ENV PATH=/usr/local/node/bin:$PATH</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#     /tmp/node-build-master/bin/node-build &#34;${NODE_VERSION}&#34; /usr/local/node &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#     npm install -g yarn@$YARN_VERSION &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#     npm install -g mjml &amp;&amp; \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#     rm -rf /tmp/node-build-master</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 安装应用程序 gems</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> Gemfile Gemfile.lock ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> bundle install <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    rm -rf ~/.bundle/ <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span>/ruby/*/cache <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span>/ruby/*/bundler/gems/*/.git <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    bundle <span class="nb">exec</span> bootsnap precompile --gemfile<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 安装 node 模块</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果您使用 NodeJS 需要编译资产，请取消注释以下几行</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># COPY package.json yarn.lock ./</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#     yarn install --frozen-lockfile</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 复制应用程序代码</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 预编译 bootsnap 代码以加快启动时间</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> bundle <span class="nb">exec</span> bootsnap precompile app/ lib/<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 预编译生产环境资产，无需 RAILS_MASTER_KEY 密钥</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> <span class="nv">SECRET_KEY_BASE_DUMMY</span><span class="o">=</span><span class="m">1</span> ./bin/rails assets:precompile<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 应用程序镜像的最终阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 复制构建的工件：gems、应用程序</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>build <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span> <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>build /rails /rails<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 作为非 root 用户运行并仅拥有运行时文件的所有权，以确保安全</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> groupadd --system --gid <span class="m">1000</span> rails <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    useradd rails --uid <span class="m">1000</span> --gid <span class="m">1000</span> --create-home --shell /bin/bash <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    chown -R rails:rails db log storage tmp<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">USER</span><span class="w"> </span><span class="s">1000:1000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 入口点用于准备数据库。</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span><span class="s2">&#34;/rails/bin/docker-entrypoint&#34;</span><span class="p">]</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 默认通过 Thruster 启动服务器，这可以在运行时被覆盖</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">EXPOSE</span><span class="w"> </span><span class="s">80</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;./bin/thrust&#34;</span><span class="p">,</span> <span class="s2">&#34;./bin/rails&#34;</span><span class="p">,</span> <span class="s2">&#34;server&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


上面的 Dockerfile 假设您将 Thruster 与 Puma 一起用作应用程序服务器。如果您使用任何其他服务器，可以用以下内容替换最后三行：

```dockerfile
# 启动应用程序服务器
EXPOSE 3000
CMD ["./bin/rails", "server"]
```

此 Dockerfile 使用 `./bin/docker-entrypoint` 处的脚本作为容器的入口点。该脚本用于准备数据库并运行应用程序服务器。以下是此类脚本的示例。

```bash {title=docker-entrypoint}
#!/bin/bash -e

# 启用 jemalloc 以减少内存使用和延迟。
if [ -z "${LD_PRELOAD+x}" ]; then
    LD_PRELOAD=$(find /usr/lib -name libjemalloc.so.2 -print -quit)
    export LD_PRELOAD
fi

# 如果运行 rails 服务器，则创建或迁移现有数据库
if [ "${@: -2:1}" == "./bin/rails" ] && [ "${@: -1:1}" == "server" ]; then
  ./bin/rails db:prepare
fi

exec "${@}"
```

除了上面的两个文件，您还需要一个 `.dockerignore` 文件。此文件用于从构建上下文中排除文件和目录。以下是 `.dockerignore` 文件的示例。

```text {collapse=true,title=".dockerignore"}
# 有关忽略文件的更多信息，请参阅 https://docs.docker.com/engine/reference/builder/#dockerignore-file。

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

# 忽略存储（开发中上传的文件和任何 SQLite 数据库）。
/storage/*
!/storage/.keep
/tmp/storage/*
!/tmp/storage/.keep

# 忽略资产。
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

您可能需要的最后一个可选文件是 `compose.yaml` 文件，Docker Compose 使用它来定义构成应用程序的服务。由于使用 SQLite 作为数据库，因此无需为数据库定义单独的服务。唯一需要的服务是 Rails 应用程序本身。

```yaml {title=compose.yaml}
services:
  web:
    build: .
    environment:
      - RAILS_MASTER_KEY
    ports:
      - "3000:80"
```

您现在应该在您的应用程序文件夹中拥有以下文件：

- `.dockerignore`
- `compose.yaml`
- `Dockerfile`
- `bin/docker-entrypoint`

要了解有关这些文件的更多信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile)
- [.dockerignore](/reference/dockerfile#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)
- [docker-entrypoint](/reference/dockerfile/#entrypoint)

## 2. 运行应用程序

要在应用程序的目录中运行应用程序，请在终端中运行以下命令。

```console
$ RAILS_MASTER_KEY=<master_key_value> docker compose up --build
```

打开浏览器并访问 [http://localhost:3000](http://localhost:3000) 查看应用程序。您应该会看到一个简单的 Ruby on Rails 应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

## 3. 在后台运行应用程序

您可以通过添加 `-d` 选项在终端中分离运行应用程序。在 `docker-ruby-on-rails` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:3000](http://localhost:3000) 查看应用程序。

您应该会看到一个简单的 Ruby on Rails 应用程序。

在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，您学习了如何使用 Docker 容器化和运行您的 Ruby 应用程序。

相关信息：

- [Docker Compose 概述](/manuals/compose/_index.md)

## 下一步

在下一节中，您将了解如何使用 GitHub Actions 设置 CI/CD 管道。
