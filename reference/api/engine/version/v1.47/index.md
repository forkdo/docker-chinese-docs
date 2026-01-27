# Docker Engine API v1.47 参考文档


<h1 class=" scroll-mt-20 flex items-center gap-2" id="docker-engine-api-v147">
  <a class="text-black dark:text-white no-underline hover:underline" href="#docker-engine-api-v147">
    Docker Engine API v1.47
  </a>
</h1>

<p>本文档描述了 Docker Engine API 的 v1.47 版本。</p>
<p>Docker Engine API 是 Docker 客户端与 Docker 守护进程通信的接口。本文档详细说明了 API 的端点、请求和响应格式。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="api-端点">
  <a class="text-black dark:text-white no-underline hover:underline" href="#api-%e7%ab%af%e7%82%b9">
    API 端点
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="容器相关端点">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%ae%b9%e5%99%a8%e7%9b%b8%e5%85%b3%e7%ab%af%e7%82%b9">
    容器相关端点
  </a>
</h3>

<ul>
<li><strong>创建容器</strong>: <code>POST /containers/create</code></li>
<li><strong>启动容器</strong>: <code>POST /containers/{id}/start</code></li>
<li><strong>停止容器</strong>: <code>POST /containers/{id}/stop</code></li>
<li><strong>删除容器</strong>: <code>DELETE /containers/{id}</code></li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="镜像相关端点">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%95%9c%e5%83%8f%e7%9b%b8%e5%85%b3%e7%ab%af%e7%82%b9">
    镜像相关端点
  </a>
</h3>

<ul>
<li><strong>拉取镜像</strong>: <code>POST /images/create</code></li>
<li><strong>列出镜像</strong>: <code>GET /images/json</code></li>
<li><strong>删除镜像</strong>: <code>DELETE /images/{name}</code></li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="网络相关端点">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%bd%91%e7%bb%9c%e7%9b%b8%e5%85%b3%e7%ab%af%e7%82%b9">
    网络相关端点
  </a>
</h3>

<ul>
<li><strong>创建网络</strong>: <code>POST /networks/create</code></li>
<li><strong>列出网络</strong>: <code>GET /networks</code></li>
<li><strong>删除网络</strong>: <code>DELETE /networks/{id}</code></li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="卷相关端点">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%8d%b7%e7%9b%b8%e5%85%b3%e7%ab%af%e7%82%b9">
    卷相关端点
  </a>
</h3>

<ul>
<li><strong>创建卷</strong>: <code>POST /volumes/create</code></li>
<li><strong>列出卷</strong>: <code>GET /volumes</code></li>
<li><strong>删除卷</strong>: <code>DELETE /volumes/{name}</code></li>
</ul>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="请求格式">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e8%af%b7%e6%b1%82%e6%a0%bc%e5%bc%8f">
    请求格式
  </a>
</h2>

<p>所有 API 请求都使用 JSON 格式。请求头必须包含：</p>
<ul>
<li><code>Content-Type: application/json</code></li>
<li><code>Accept: application/json</code></li>
</ul>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="响应格式">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%93%8d%e5%ba%94%e6%a0%bc%e5%bc%8f">
    响应格式
  </a>
</h2>

<p>API 响应使用 JSON 格式。成功响应的状态码为 200，错误响应包含错误信息和相应的 HTTP 状态码。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="认证">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e8%ae%a4%e8%af%81">
    认证
  </a>
</h2>

<p>API 使用基于证书的认证。客户端需要提供：</p>
<ul>
<li>客户端证书</li>
<li>私钥</li>
<li>CA 证书</li>
</ul>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="版本信息">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%89%88%e6%9c%ac%e4%bf%a1%e6%81%af">
    版本信息
  </a>
</h2>

<p>此 API 版本为 v1.47，与 Docker Engine 24.0 及更高版本兼容。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="注意事项">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%b3%a8%e6%84%8f%e4%ba%8b%e9%a1%b9">
    注意事项
  </a>
</h2>

<ul>
<li>API 端点可能因 Docker 版本而异</li>
<li>某些功能可能需要特定的 Docker 版本支持</li>
<li>建议使用最新版本的 Docker Engine 以获得最佳兼容性</li>
</ul>


**OpenAPI Specification:** [Docker Engine API v1.47 参考文档 API Spec](/reference/api/engine/version/v1.47.yaml)

This page provides interactive API documentation. For the machine-readable OpenAPI specification, see the link above.
