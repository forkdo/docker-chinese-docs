# 
title: Containerize a Ruby on Rails application
linkTitle: Containerize your app
weight: 10
description: Learn how to containerize a Ruby on Rails application.
keywords: "ruby, flask, containerize, initialize"
aliases:
  - /language/ruby/build-images/
  - /language/ruby/run-containers/
  - /language/ruby/containerize/
  - /guides/language/ruby/containerize/---
title: 容器化 Ruby on Rails 应用
linkTitle: 容器化你的应用
weight: 10
description: 了解如何容器化 Ruby on Rails 应用。---
## 前置条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例展示了 Git CLI，但你可以使用任何客户端。

## 概述

本节将指导你完成容器化并运行 [Ruby on Rails](https://rubyonrails.org/) 应用程序的过程。

从 Rails 7.1 开始，[开箱即支持 Docker](https://guides.rubyonrails.org/7_1_release_notes.html#generate-dockerfiles-for-new-rails-applications)。这意味着当你创建一个新的 Rails 应用程序时，系统会自动为你生成 `Dockerfile`、`.dockerignore` 和 `bin/docker-entrypoint` 文件。

如果你现有的 Rails 应用程序，则需要手动创建 Docker 资产。遗憾的是，`docker init` 命令尚不支持 Rails。这意味着如果你正在使用 Rails，则需要从下面的示例中手动复制 Dockerfile 和其他相关配置。

## 1. 初始化 Docker 资产

Rails 7.1 及更新版本开箱即生成多阶段 Dockerfile。以下是该文件的两个版本：一个使用 Docker Hardened Images (DHIs)，另一个使用 Docker Official Image (DOIs)。虽然 Dockerfile 是自动生成的，但了解其用途和功能非常重要。强烈建议查看以下示例。

[Docker Hardened Images (DHIs)](https://docs.docker.com/dhi/) 是由 Docker 维护的极简、安全且可用于生产的容器基础镜像和应用镜像。只要有可能，都推荐使用 DHIs 以获得更好的安全性。它们旨在减少漏洞并简化合规性，对所有人免费开放，无需订阅，无使用限制，且无供应商锁定。

多阶段 Dockerfile 通过分离构建和运行时依赖，帮助创建更小、更高效的镜像，确保最终镜像中仅包含必要的组件。在 [多阶段构建指南](/get-started/docker-concepts/building-images/multi-stage-builds/) 中了解更多信息。










<div
  class="tabs"
  
    x-data="{ selected: 'Using-DHIs' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Using-DHIs' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Using-DHIs'"
        
      >
        Using DHIs
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Using-DOIs' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Using-DOIs'"
        
      >
        Using DOIs
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Using-DHIs' && 'hidden'"
      >
        <p>在拉取 Docker Hardened Images 之前，你必须向 <code>dhi.io</code> 进行身份验证。运行 <code>docker login dhi.io</code> 进行身份验证。</p>
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
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQojIGNoZWNrPWVycm9yPXRydWUKCiMgVGhpcyBEb2NrZXJmaWxlIGlzIGRlc2lnbmVkIGZvciBwcm9kdWN0aW9uLCBub3QgZGV2ZWxvcG1lbnQuCiMgZG9ja2VyIGJ1aWxkIC10IGFwcCAuCiMgZG9ja2VyIHJ1biAtZCAtcCA4MDo4MCAtZSBSQUlMU19NQVNURVJfS0VZPTx2YWx1ZSBmcm9tIGNvbmZpZy9tYXN0ZXIua2V5PiAtLW5hbWUgYXBwIGFwcAoKIyBGb3IgYSBjb250YWluZXJpemVkIGRldiBlbnZpcm9ubWVudCwgc2VlIERldiBDb250YWluZXJzOiBodHRwczovL2d1aWRlcy5ydWJ5b25yYWlscy5vcmcvZ2V0dGluZ19zdGFydGVkX3dpdGhfZGV2Y29udGFpbmVyLmh0bWwKCiMgTWFrZSBzdXJlIFJVQllfVkVSU0lPTiBtYXRjaGVzIHRoZSBSdWJ5IHZlcnNpb24gaW4gLnJ1YnktdmVyc2lvbgpBUkcgUlVCWV9WRVJTSU9OPTMuNC44CkZST00gZGhpLmlvL3J1Ynk6JFJVQllfVkVSU0lPTi1kZXYgQVMgYmFzZQoKIyBSYWlscyBhcHAgbGl2ZXMgaGVyZQpXT1JLRElSIC9yYWlscwoKIyBJbnN0YWxsIGJhc2UgcGFja2FnZXMKIyBSZXBsYWNlIGxpYnBxLWRldiB3aXRoIHNxbGl0ZTMgaWYgdXNpbmcgU1FMaXRlLCBvciBsaWJteXNxbGNsaWVudC1kZXYgaWYgdXNpbmcgTXlTUUwKUlVOIGFwdC1nZXQgdXBkYXRlIC1xcSAmJiBcCiAgICBhcHQtZ2V0IGluc3RhbGwgLS1uby1pbnN0YWxsLXJlY29tbWVuZHMgLXkgY3VybCBsaWJqZW1hbGxvYzIgbGlidmlwcyBsaWJwcS1kZXYgJiYgXAogICAgcm0gLXJmIC92YXIvbGliL2FwdC9saXN0cyAvdmFyL2NhY2hlL2FwdC9hcmNoaXZlcwoKIyBTZXQgcHJvZHVjdGlvbiBlbnZpcm9ubWVudApFTlYgUkFJTFNfRU5WPSJwcm9kdWN0aW9uIiBcCiAgICBCVU5ETEVfREVQTE9ZTUVOVD0iMSIgXAogICAgQlVORExFX1BBVEg9Ii91c3IvbG9jYWwvYnVuZGxlIiBcCiAgICBCVU5ETEVfV0lUSE9VVD0iZGV2ZWxvcG1lbnQiCgojIFRocm93LWF3YXkgYnVpbGQgc3RhZ2UgdG8gcmVkdWNlIHNpemUgb2YgZmluYWwgaW1hZ2UKRlJPTSBiYXNlIEFTIGJ1aWxkCgojIEluc3RhbGwgcGFja2FnZXMgbmVlZGVkIHRvIGJ1aWxkIGdlbXMKUlVOIGFwdC1nZXQgdXBkYXRlIC1xcSAmJiBcCiAgICBhcHQtZ2V0IGluc3RhbGwgLS1uby1pbnN0YWxsLXJlY29tbWVuZHMgLXkgYnVpbGQtZXNzZW50aWFsIGN1cmwgZ2l0IHBrZy1jb25maWcgbGlieWFtbC1kZXYgJiYgXAogICAgcm0gLXJmIC92YXIvbGliL2FwdC9saXN0cyAvdmFyL2NhY2hlL2FwdC9hcmNoaXZlcwoKIyBJbnN0YWxsIEphdmFTY3JpcHQgZGVwZW5kZW5jaWVzIGFuZCBOb2RlLmpzIGZvciBhc3NldCBjb21waWxhdGlvbgojCiMgVW5jb21tZW50IHRoZSBmb2xsb3dpbmcgbGluZXMgaWYgeW91IGFyZSB1c2luZyBOb2RlSlMgbmVlZCB0byBjb21waWxlIGFzc2V0cwojCiMgQVJHIE5PREVfVkVSU0lPTj0xOC4xMi4wCiMgQVJHIFlBUk5fVkVSU0lPTj0xLjIyLjE5CiMgRU5WIFBBVEg9L3Vzci9sb2NhbC9ub2RlL2JpbjokUEFUSAojIFJVTiBjdXJsIC1zTCBodHRwczovL2dpdGh1Yi5jb20vbm9kZW52L25vZGUtYnVpbGQvYXJjaGl2ZS9tYXN0ZXIudGFyLmd6IHwgdGFyIHh6IC1DIC90bXAvICYmIFwKIyAgICAgL3RtcC9ub2RlLWJ1aWxkLW1hc3Rlci9iaW4vbm9kZS1idWlsZCAiJHtOT0RFX1ZFUlNJT059IiAvdXNyL2xvY2FsL25vZGUgJiYgXAojICAgICBucG0gaW5zdGFsbCAtZyB5YXJuQCRZQVJOX1ZFUlNJT04gJiYgXAojICAgICBucG0gaW5zdGFsbCAtZyBtam1sICYmIFwKIyAgICAgcm0gLXJmIC90bXAvbm9kZS1idWlsZC1tYXN0ZXIKCiMgSW5zdGFsbCBhcHBsaWNhdGlvbiBnZW1zCkNPUFkgR2VtZmlsZSBHZW1maWxlLmxvY2sgLi8KUlVOIGJ1bmRsZSBpbnN0YWxsICYmIFwKICAgIHJtIC1yZiB&#43;Ly5idW5kbGUvICIke0JVTkRMRV9QQVRIfSIvcnVieS8qL2NhY2hlICIke0JVTkRMRV9QQVRIfSIvcnVieS8qL2J1bmRsZXIvZ2Vtcy8qLy5naXQgJiYgXAogICAgYnVuZGxlIGV4ZWMgYm9vdHNuYXAgcHJlY29tcGlsZSAtLWdlbWZpbGUKCiMgSW5zdGFsbCBub2RlIG1vZHVsZXMKIwojIFVuY29tbWVudCB0aGUgZm9sbG93aW5nIGxpbmVzIGlmIHlvdSBhcmUgdXNpbmcgTm9kZUpTIG5lZWQgdG8gY29tcGlsZSBhc3NldHMKIwojIENPUFkgcGFja2FnZS5qc29uIHlhcm4ubG9jayAuLwojIFJVTiAtLW1vdW50PXR5cGU9Y2FjaGUsaWQ9eWFybix0YXJnZXQ9L3JhaWxzLy5jYWNoZS95YXJuIFlBUk5fQ0FDSEVfRk9MREVSPS9yYWlscy8uY2FjaGUveWFybiBcCiMgICAgIHlhcm4gaW5zdGFsbCAtLWZyb3plbi1sb2NrZmlsZQoKIyBDb3B5IGFwcGxpY2F0aW9uIGNvZGUKQ09QWSAuIC4KCiMgUHJlY29tcGlsZSBib290c25hcCBjb2RlIGZvciBmYXN0ZXIgYm9vdCB0aW1lcwpSVU4gYnVuZGxlIGV4ZWMgYm9vdHNuYXAgcHJlY29tcGlsZSBhcHAvIGxpYi8KCiMgUHJlY29tcGlsaW5nIGFzc2V0cyBmb3IgcHJvZHVjdGlvbiB3aXRob3V0IHJlcXVpcmluZyBzZWNyZXQgUkFJTFNfTUFTVEVSX0tFWQpSVU4gU0VDUkVUX0tFWV9CQVNFX0RVTU1ZPTEgLi9iaW4vcmFpbHMgYXNzZXRzOnByZWNvbXBpbGUKCiMgRmluYWwgc3RhZ2UgZm9yIGFwcCBpbWFnZQpGUk9NIGJhc2UKCiMgQ29weSBidWlsdCBhcnRpZmFjdHM6IGdlbXMsIGFwcGxpY2F0aW9uCkNPUFkgLS1mcm9tPWJ1aWxkICIke0JVTkRMRV9QQVRIfSIgIiR7QlVORExFX1BBVEh9IgpDT1BZIC0tZnJvbT1idWlsZCAvcmFpbHMgL3JhaWxzCgojIFJ1biBhbmQgb3duIG9ubHkgdGhlIHJ1bnRpbWUgZmlsZXMgYXMgYSBub24tcm9vdCB1c2VyIGZvciBzZWN1cml0eQpSVU4gZ3JvdXBhZGQgLS1zeXN0ZW0gLS1naWQgMTAwMCByYWlscyAmJiBcCiAgICB1c2VyYWRkIHJhaWxzIC0tdWlkIDEwMDAgLS1naWQgMTAwMCAtLWNyZWF0ZS1ob21lIC0tc2hlbGwgL2Jpbi9iYXNoICYmIFwKICAgIGNob3duIC1SIHJhaWxzOnJhaWxzIGRiIGxvZyBzdG9yYWdlIHRtcApVU0VSIDEwMDA6MTAwMAoKIyBFbnRyeXBvaW50IHByZXBhcmVzIHRoZSBkYXRhYmFzZS4KRU5UUllQT0lOVCBbIi9yYWlscy9iaW4vZG9ja2VyLWVudHJ5cG9pbnQiXQoKIyBTdGFydCBzZXJ2ZXIgdmlhIFRocnVzdGVyIGJ5IGRlZmF1bHQsIHRoaXMgY2FuIGJlIG92ZXJ3cml0dGVuIGF0IHJ1bnRpbWUKRVhQT1NFIDgwCkNNRCBbIi4vYmluL3RocnVzdCIsICIuL2Jpbi9yYWlscyIsICJzZXJ2ZXIiXQ==', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="c"># This Dockerfile is designed for production, not development.</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># docker build -t app .</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># docker run -d -p 80:80 -e RAILS_MASTER_KEY=&lt;value from config/master.key&gt; --name app app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># For a containerized dev environment, see Dev Containers: https://guides.rubyonrails.org/getting_started_with_devcontainer.html</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Make sure RUBY_VERSION matches the Ruby version in .ruby-version</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ARG</span> <span class="nv">RUBY_VERSION</span><span class="o">=</span><span class="m">3</span>.4.8<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/ruby:$RUBY_VERSION-dev</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Rails app lives here</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/rails</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Install base packages</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Replace libpq-dev with sqlite3 if using SQLite, or libmysqlclient-dev if using MySQL</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> apt-get update -qq <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    rm -rf /var/lib/apt/lists /var/cache/apt/archives<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Set production environment</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">RAILS_ENV</span><span class="o">=</span><span class="s2">&#34;production&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">BUNDLE_DEPLOYMENT</span><span class="o">=</span><span class="s2">&#34;1&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">BUNDLE_PATH</span><span class="o">=</span><span class="s2">&#34;/usr/local/bundle&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">BUNDLE_WITHOUT</span><span class="o">=</span><span class="s2">&#34;development&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Throw-away build stage to reduce size of final image</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">base</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Install packages needed to build gems</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> apt-get update -qq <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    rm -rf /var/lib/apt/lists /var/cache/apt/archives<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Install JavaScript dependencies and Node.js for asset compilation</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Uncomment the following lines if you are using NodeJS need to compile assets</span><span class="err">
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
</span></span></span><span class="line"><span class="cl"><span class="c"># Install application gems</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> Gemfile Gemfile.lock ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> bundle install <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    rm -rf ~/.bundle/ <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span>/ruby/*/cache <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span>/ruby/*/bundler/gems/*/.git <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    bundle <span class="nb">exec</span> bootsnap precompile --gemfile<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Install node modules</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Uncomment the following lines if you are using NodeJS need to compile assets</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># COPY package.json yarn.lock ./</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#     yarn install --frozen-lockfile</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Copy application code</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Precompile bootsnap code for faster boot times</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> bundle <span class="nb">exec</span> bootsnap precompile app/ lib/<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Precompiling assets for production without requiring secret RAILS_MASTER_KEY</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> <span class="nv">SECRET_KEY_BASE_DUMMY</span><span class="o">=</span><span class="m">1</span> ./bin/rails assets:precompile<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Final stage for app image</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Copy built artifacts: gems, application</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>build <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span> <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>build /rails /rails<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Run and own only the runtime files as a non-root user for security</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> groupadd --system --gid <span class="m">1000</span> rails <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    useradd rails --uid <span class="m">1000</span> --gid <span class="m">1000</span> --create-home --shell /bin/bash <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    chown -R rails:rails db log storage tmp<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">USER</span><span class="w"> </span><span class="s">1000:1000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Entrypoint prepares the database.</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span><span class="s2">&#34;/rails/bin/docker-entrypoint&#34;</span><span class="p">]</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Start server via Thruster by default, this can be overwritten at runtime</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">EXPOSE</span><span class="w"> </span><span class="s">80</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;./bin/thrust&#34;</span><span class="p">,</span> <span class="s2">&#34;./bin/rails&#34;</span><span class="p">,</span> <span class="s2">&#34;server&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Using-DOIs' && 'hidden'"
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
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQojIGNoZWNrPWVycm9yPXRydWUKCiMgVGhpcyBEb2NrZXJmaWxlIGlzIGRlc2lnbmVkIGZvciBwcm9kdWN0aW9uLCBub3QgZGV2ZWxvcG1lbnQuCiMgZG9ja2VyIGJ1aWxkIC10IGFwcCAuCiMgZG9ja2VyIHJ1biAtZCAtcCA4MDo4MCAtZSBSQUlMU19NQVNURVJfS0VZPTx2YWx1ZSBmcm9tIGNvbmZpZy9tYXN0ZXIua2V5PiAtLW5hbWUgYXBwIGFwcAoKIyBGb3IgYSBjb250YWluZXJpemVkIGRldiBlbnZpcm9ubWVudCwgc2VlIERldiBDb250YWluZXJzOiBodHRwczovL2d1aWRlcy5ydWJ5b25yYWlscy5vcmcvZ2V0dGluZ19zdGFydGVkX3dpdGhfZGV2Y29udGFpbmVyLmh0bWwKCiMgTWFrZSBzdXJlIFJVQllfVkVSU0lPTiBtYXRjaGVzIHRoZSBSdWJ5IHZlcnNpb24gaW4gLnJ1YnktdmVyc2lvbgpBUkcgUlVCWV9WRVJTSU9OPTMuNC44CkZST00gZG9ja2VyLmlvL2xpYnJhcnkvcnVieTokUlVCWV9WRVJTSU9OLXNsaW0gQVMgYmFzZQoKIyBSYWlscyBhcHAgbGl2ZXMgaGVyZQpXT1JLRElSIC9yYWlscwoKIyBJbnN0YWxsIGJhc2UgcGFja2FnZXMKIyBSZXBsYWNlIGxpYnBxLWRldiB3aXRoIHNxbGl0ZTMgaWYgdXNpbmcgU1FMaXRlLCBvciBsaWJteXNxbGNsaWVudC1kZXYgaWYgdXNpbmcgTXlTUUwKUlVOIGFwdC1nZXQgdXBkYXRlIC1xcSAmJiBcCiAgICBhcHQtZ2V0IGluc3RhbGwgLS1uby1pbnN0YWxsLXJlY29tbWVuZHMgLXkgY3VybCBsaWJqZW1hbGxvYzIgbGlidmlwcyBsaWJwcS1kZXYgJiYgXAogICAgcm0gLXJmIC92YXIvbGliL2FwdC9saXN0cyAvdmFyL2NhY2hlL2FwdC9hcmNoaXZlcwoKIyBTZXQgcHJvZHVjdGlvbiBlbnZpcm9ubWVudApFTlYgUkFJTFNfRU5WPSJwcm9kdWN0aW9uIiBcCiAgICBCVU5ETEVfREVQTE9ZTUVOVD0iMSIgXAogICAgQlVORExFX1BBVEg9Ii91c3IvbG9jYWwvYnVuZGxlIiBcCiAgICBCVU5ETEVfV0lUSE9VVD0iZGV2ZWxvcG1lbnQiCgojIFRocm93LWF3YXkgYnVpbGQgc3RhZ2UgdG8gcmVkdWNlIHNpemUgb2YgZmluYWwgaW1hZ2UKRlJPTSBiYXNlIEFTIGJ1aWxkCgojIEluc3RhbGwgcGFja2FnZXMgbmVlZGVkIHRvIGJ1aWxkIGdlbXMKUlVOIGFwdC1nZXQgdXBkYXRlIC1xcSAmJiBcCiAgICBhcHQtZ2V0IGluc3RhbGwgLS1uby1pbnN0YWxsLXJlY29tbWVuZHMgLXkgYnVpbGQtZXNzZW50aWFsIGN1cmwgZ2l0IHBrZy1jb25maWcgbGlieWFtbC1kZXYgJiYgXAogICAgcm0gLXJmIC92YXIvbGliL2FwdC9saXN0cyAvdmFyL2NhY2hlL2FwdC9hcmNoaXZlcwoKIyBJbnN0YWxsIEphdmFTY3JpcHQgZGVwZW5kZW5jaWVzIGFuZCBOb2RlLmpzIGZvciBhc3NldCBjb21waWxhdGlvbgojCiMgVW5jb21tZW50IHRoZSBmb2xsb3dpbmcgbGluZXMgaWYgeW91IGFyZSB1c2luZyBOb2RlSlMgbmVlZCB0byBjb21waWxlIGFzc2V0cwojCiMgQVJHIE5PREVfVkVSU0lPTj0xOC4xMi4wCiMgQVJHIFlBUk5fVkVSU0lPTj0xLjIyLjE5CiMgRU5WIFBBVEg9L3Vzci9sb2NhbC9ub2RlL2JpbjokUEFUSAojIFJVTiBjdXJsIC1zTCBodHRwczovL2dpdGh1Yi5jb20vbm9kZW52L25vZGUtYnVpbGQvYXJjaGl2ZS9tYXN0ZXIudGFyLmd6IHwgdGFyIHh6IC1DIC90bXAvICYmIFwKIyAgICAgL3RtcC9ub2RlLWJ1aWxkLW1hc3Rlci9iaW4vbm9kZS1idWlsZCAiJHtOT0RFX1ZFUlNJT059IiAvdXNyL2xvY2FsL25vZGUgJiYgXAojICAgICBucG0gaW5zdGFsbCAtZyB5YXJuQCRZQVJOX1ZFUlNJT04gJiYgXAojICAgICBucG0gaW5zdGFsbCAtZyBtam1sICYmIFwKIyAgICAgcm0gLXJmIC90bXAvbm9kZS1idWlsZC1tYXN0ZXIKCiMgSW5zdGFsbCBhcHBsaWNhdGlvbiBnZW1zCkNPUFkgR2VtZmlsZSBHZW1maWxlLmxvY2sgLi8KUlVOIGJ1bmRsZSBpbnN0YWxsICYmIFwKICAgIHJtIC1yZiB&#43;Ly5idW5kbGUvICIke0JVTkRMRV9QQVRIfSIvcnVieS8qL2NhY2hlICIke0JVTkRMRV9QQVRIfSIvcnVieS8qL2J1bmRsZXIvZ2Vtcy8qLy5naXQgJiYgXAogICAgYnVuZGxlIGV4ZWMgYm9vdHNuYXAgcHJlY29tcGlsZSAtLWdlbWZpbGUKCiMgSW5zdGFsbCBub2RlIG1vZHVsZXMKIwojIFVuY29tbWVudCB0aGUgZm9sbG93aW5nIGxpbmVzIGlmIHlvdSBhcmUgdXNpbmcgTm9kZUpTIG5lZWQgdG8gY29tcGlsZSBhc3NldHMKIwojIENPUFkgcGFja2FnZS5qc29uIHlhcm4ubG9jayAuLwojIFJVTiAtLW1vdW50PXR5cGU9Y2FjaGUsaWQ9eWFybix0YXJnZXQ9L3JhaWxzLy5jYWNoZS95YXJuIFlBUk5fQ0FDSEVfRk9MREVSPS9yYWlscy8uY2FjaGUveWFybiBcCiMgICAgIHlhcm4gaW5zdGFsbCAtLWZyb3plbi1sb2NrZmlsZQoKIyBDb3B5IGFwcGxpY2F0aW9uIGNvZGUKQ09QWSAuIC4KCiMgUHJlY29tcGlsZSBib290c25hcCBjb2RlIGZvciBmYXN0ZXIgYm9vdCB0aW1lcwpSVU4gYnVuZGxlIGV4ZWMgYm9vdHNuYXAgcHJlY29tcGlsZSBhcHAvIGxpYi8KCiMgUHJlY29tcGlsaW5nIGFzc2V0cyBmb3IgcHJvZHVjdGlvbiB3aXRob3V0IHJlcXVpcmluZyBzZWNyZXQgUkFJTFNfTUFTVEVSX0tFWQpSVU4gU0VDUkVUX0tFWV9CQVNFX0RVTU1ZPTEgLi9iaW4vcmFpbHMgYXNzZXRzOnByZWNvbXBpbGUKCiMgRmluYWwgc3RhZ2UgZm9yIGFwcCBpbWFnZQpGUk9NIGJhc2UKCiMgQ29weSBidWlsdCBhcnRpZmFjdHM6IGdlbXMsIGFwcGxpY2F0aW9uCkNPUFkgLS1mcm9tPWJ1aWxkICIke0JVTkRMRV9QQVRIfSIgIiR7QlVORExFX1BBVEh9IgpDT1BZIC0tZnJvbT1idWlsZCAvcmFpbHMgL3JhaWxzCgojIFJ1biBhbmQgb3duIG9ubHkgdGhlIHJ1bnRpbWUgZmlsZXMgYXMgYSBub24tcm9vdCB1c2VyIGZvciBzZWN1cml0eQpSVU4gZ3JvdXBhZGQgLS1zeXN0ZW0gLS1naWQgMTAwMCByYWlscyAmJiBcCiAgICB1c2VyYWRkIHJhaWxzIC0tdWlkIDEwMDAgLS1naWQgMTAwMCAtLWNyZWF0ZS1ob21lIC0tc2hlbGwgL2Jpbi9iYXNoICYmIFwKICAgIGNob3duIC1SIHJhaWxzOnJhaWxzIGRiIGxvZyBzdG9yYWdlIHRtcApVU0VSIDEwMDA6MTAwMAoKIyBFbnRyeXBvaW50IHByZXBhcmVzIHRoZSBkYXRhYmFzZS4KRU5UUllQT0lOVCBbIi9yYWlscy9iaW4vZG9ja2VyLWVudHJ5cG9pbnQiXQoKIyBTdGFydCBzZXJ2ZXIgdmlhIFRocnVzdGVyIGJ5IGRlZmF1bHQsIHRoaXMgY2FuIGJlIG92ZXJ3cml0dGVuIGF0IHJ1bnRpbWUKRVhQT1NFIDgwCkNNRCBbIi4vYmluL3RocnVzdCIsICIuL2Jpbi9yYWlscyIsICJzZXJ2ZXIiXQ==', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="c"># This Dockerfile is designed for production, not development.</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># docker build -t app .</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># docker run -d -p 80:80 -e RAILS_MASTER_KEY=&lt;value from config/master.key&gt; --name app app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># For a containerized dev environment, see Dev Containers: https://guides.rubyonrails.org/getting_started_with_devcontainer.html</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Make sure RUBY_VERSION matches the Ruby version in .ruby-version</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ARG</span> <span class="nv">RUBY_VERSION</span><span class="o">=</span><span class="m">3</span>.4.8<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">docker.io/library/ruby:$RUBY_VERSION-slim</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Rails app lives here</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/rails</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Install base packages</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Replace libpq-dev with sqlite3 if using SQLite, or libmysqlclient-dev if using MySQL</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> apt-get update -qq <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    rm -rf /var/lib/apt/lists /var/cache/apt/archives<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Set production environment</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">RAILS_ENV</span><span class="o">=</span><span class="s2">&#34;production&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">BUNDLE_DEPLOYMENT</span><span class="o">=</span><span class="s2">&#34;1&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">BUNDLE_PATH</span><span class="o">=</span><span class="s2">&#34;/usr/local/bundle&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">BUNDLE_WITHOUT</span><span class="o">=</span><span class="s2">&#34;development&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Throw-away build stage to reduce size of final image</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">base</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Install packages needed to build gems</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> apt-get update -qq <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    rm -rf /var/lib/apt/lists /var/cache/apt/archives<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Install JavaScript dependencies and Node.js for asset compilation</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Uncomment the following lines if you are using NodeJS need to compile assets</span><span class="err">
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
</span></span></span><span class="line"><span class="cl"><span class="c"># Install application gems</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> Gemfile Gemfile.lock ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> bundle install <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    rm -rf ~/.bundle/ <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span>/ruby/*/cache <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span>/ruby/*/bundler/gems/*/.git <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    bundle <span class="nb">exec</span> bootsnap precompile --gemfile<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Install node modules</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Uncomment the following lines if you are using NodeJS need to compile assets</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># COPY package.json yarn.lock ./</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c">#     yarn install --frozen-lockfile</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Copy application code</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Precompile bootsnap code for faster boot times</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> bundle <span class="nb">exec</span> bootsnap precompile app/ lib/<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Precompiling assets for production without requiring secret RAILS_MASTER_KEY</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> <span class="nv">SECRET_KEY_BASE_DUMMY</span><span class="o">=</span><span class="m">1</span> ./bin/rails assets:precompile<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Final stage for app image</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Copy built artifacts: gems, application</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>build <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span> <span class="s2">&#34;</span><span class="si">${</span><span class="nv">BUNDLE_PATH</span><span class="si">}</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>build /rails /rails<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Run and own only the runtime files as a non-root user for security</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> groupadd --system --gid <span class="m">1000</span> rails <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    useradd rails --uid <span class="m">1000</span> --gid <span class="m">1000</span> --create-home --shell /bin/bash <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl">    chown -R rails:rails db log storage tmp<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">USER</span><span class="w"> </span><span class="s">1000:1000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Entrypoint prepares the database.</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span><span class="s2">&#34;/rails/bin/docker-entrypoint&#34;</span><span class="p">]</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># Start server via Thruster by default, this can be overwritten at runtime</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">EXPOSE</span><span class="w"> </span><span class="s">80</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;./bin/thrust&#34;</span><span class="p">,</span> <span class="s2">&#34;./bin/rails&#34;</span><span class="p">,</span> <span class="s2">&#34;server&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


上面的 Dockerfile 假设你将 Thruster 与 Puma 一起作为应用服务器使用。如果你使用的是任何其他服务器，可以将最后三行替换为以下内容：

```dockerfile
# Start the application server
EXPOSE 3000
CMD ["./bin/rails", "server"]
```

此 Dockerfile 使用 `./bin/docker-entrypoint` 处的脚本作为容器的入口点。该脚本准备数据库并运行应用服务器。以下是此类脚本的一个示例。

```bash {title=docker-entrypoint}
#!/bin/bash -e

# Enable jemalloc for reduced memory usage and latency.
if [ -z "${LD_PRELOAD+x}" ]; then
    LD_PRELOAD=$(find /usr/lib -name libjemalloc.so.2 -print -quit)
    export LD_PRELOAD
fi

# If running the rails server then create or migrate existing database
if [ "${@: -2:1}" == "./bin/rails" ] && [ "${@: -1:1}" == "server" ]; then
  ./bin/rails db:prepare
fi

exec "${@}"
```

除了上述两个文件外，你还需要一个 `.dockerignore` 文件。该文件用于从构建上下文中排除文件和目录。以下是 `.dockerignore` 文件的一个示例。

```text {collapse=true,title=".dockerignore"}
# See https://docs.docker.com/engine/reference/builder/#dockerignore-file for more about ignoring files.

# Ignore git directory.
/.git/
/.gitignore

# Ignore bundler config.
/.bundle

# Ignore all environment files.
/.env*

# Ignore all default key files.
/config/master.key
/config/credentials/*.key

# Ignore all logfiles and tempfiles.
/log/*
/tmp/*
!/log/.keep
!/tmp/.keep

# Ignore pidfiles, but keep the directory.
/tmp/pids/*
!/tmp/pids/.keep

# Ignore storage (uploaded files in development and any SQLite databases).
/storage/*
!/storage/.keep
/tmp/storage/*
!/tmp/storage/.keep

# Ignore assets.
/node_modules/
/app/assets/builds/*
!/app/assets/builds/.keep
/public/assets

# Ignore CI service files.
/.github

# Ignore development files
/.devcontainer

# Ignore Docker-related files
/.dockerignore
/Dockerfile*
```

你可能需要的最后一个可选文件是 `compose.yaml` 文件，Docker Compose 使用该文件来定义组成应用程序的服务。由于使用 SQLite 作为数据库，因此无需为数据库定义单独的服务。唯一需要的服务是 Rails 应用程序本身。

```yaml {title=compose.yaml}
services:
  web:
    build: .
    environment:
      - RAILS_MASTER_KEY
    ports:
      - "3000:80"
```

现在，你的应用程序文件夹中应该包含以下文件：

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

要运行应用程序，请在应用程序目录内的终端中运行以下命令。

```console
$ RAILS_MASTER_KEY=<master_key_value> docker compose up --build
```

打开浏览器并在 [http://localhost:3000](http://localhost:3000) 查看应用程序。你应该会看到一个简单的 Ruby on Rails 应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

## 3. 在后台运行应用程序

你可以通过添加 `-d` 选项来运行与终端分离的应用程序。在 `docker-ruby-on-rails` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并在 [http://localhost:3000](http://localhost:3000) 查看应用程序。

你应该会看到一个简单的 Ruby on Rails 应用程序。

在终端中，运行以下命令以停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，你了解了如何使用 Docker 容器化并运行 Ruby 应用程序。

相关信息：

- [Docker Compose 概述](/manuals/compose/_index.md)

## 后续步骤

在下一节中，你将了解如何使用 GitHub Actions 设置 CI/CD 流水线。
