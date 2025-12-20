# 洞察与分析

“洞察与分析”为 Docker Hub 上的 [Docker Verified Publisher (DVP)](https://www.docker.com/partners/programs/) 和 [Docker-Sponsored Open Source (DSOS)](https://www.docker.com/community/open-source/application/#) 镜像提供使用分析。这包括自助访问特定时间段内的镜像和扩展使用指标。您可以查看按标签或摘要划分的镜像拉取次数、地理位置、云服务提供商、客户端等信息。

> [!NOTE]
>
> 旧版 DVP 计划适用于尚未续订 DVP Core 的现有客户。DVP 旧版计划已弃用，并将被停用。有关更多信息，请联系您的 Docker 销售代表或 [Docker](https://www.docker.com/partners/programs/)。








<div
  class="tabs"
  
    x-data="{ selected: 'DVP-%E8%AE%A1%E5%88%92' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'DVP-%E8%AE%A1%E5%88%92' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'DVP-%E8%AE%A1%E5%88%92'"
        
      >
        DVP 计划
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'DSOS-%E5%92%8C%E6%97%A7%E7%89%88-DVP-%E8%AE%A1%E5%88%92' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'DSOS-%E5%92%8C%E6%97%A7%E7%89%88-DVP-%E8%AE%A1%E5%88%92'"
        
      >
        DSOS 和旧版 DVP 计划
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'DVP-%E8%AE%A1%E5%88%92' && 'hidden'"
      >
        <p>组织的所有成员均可访问分析数据。成员可以通过 <a class="link" href="https://hub.docker.com/" rel="noopener">Docker Hub</a> Web 界面或使用 
  <a class="link" href="/reference/api/dvp/latest/">DVP Data API</a> 访问分析数据。以下内容介绍 Web 界面的使用方法。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="可用报告">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%8f%af%e7%94%a8%e6%8a%a5%e5%91%8a">
    可用报告
  </a>
</h2>

<p>以下报告可能以 CSV 文件形式提供下载：</p>
<ul>
<li><a class="link" href="#%e6%91%98%e8%a6%81%e6%8a%a5%e5%91%8a">摘要</a></li>
<li><a class="link" href="#%e8%b6%8b%e5%8a%bf%e6%8a%a5%e5%91%8a">趋势</a></li>
<li><a class="link" href="#%e6%8a%80%e6%9c%af%e6%a0%88%e5%88%86%e6%9e%90%e6%8a%a5%e5%91%8a">技术栈分析</a></li>
<li><a class="link" href="#%e6%8a%80%e6%9c%af%e6%a0%88%e5%85%ac%e5%8f%b8%e5%88%86%e6%9e%90%e6%8a%a5%e5%91%8a">技术栈公司分析</a></li>
<li><a class="link" href="#%e8%bf%bd%e8%b8%aa%e5%85%ac%e5%8f%b8%e5%88%86%e6%9e%90%e6%8a%a5%e5%91%8a">追踪公司分析</a></li>
</ul>
<p>可供下载的报告可能因您组织的订阅而异。有关更多信息，请联系您的 Docker 销售代表或 <a class="link" href="https://www.docker.com/partners/programs/" rel="noopener">Docker</a>。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="摘要报告">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%91%98%e8%a6%81%e6%8a%a5%e5%91%8a">
    摘要报告
  </a>
</h3>

<p>摘要报告提供跨所有 Docker Hub 内容的高级使用指标，按命名空间和仓库组织。该报告让您全面了解镜像组合的表现，帮助您了解哪些仓库、标签和特定镜像版本最受用户欢迎。</p>
<p>您可以使用此报告回答以下问题：</p>
<ul>
<li>哪些仓库的使用量最大？</li>
<li>不同镜像标签在采用率方面有何差异？</li>
<li>在您的组合中，实际下载与版本检查的比率是多少？</li>
<li>哪些特定的镜像摘要被拉取得最频繁？</li>
<li>整个镜像集合的整体使用情况随时间如何变化？</li>
</ul>
<p>访问报告：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com/" rel="noopener">Docker Hub</a>。</li>
<li>在顶部导航中选择 <strong>My Hub</strong>。</li>
<li>在左侧导航中选择您的组织。</li>
<li>在左侧导航中选择 <strong>Analytics</strong> &gt; <strong>Overview</strong>。</li>
<li>通过以下任一方式下载报告：
<ul>
<li>选择 <strong>Download Weekly Summary</strong>。</li>
<li>选择 <strong>Download Monthly Summary</strong>。</li>
<li>展开 <strong>Summary reports for the year</strong> 下拉菜单，然后为所需周或月选择 <strong>Download report</strong>。</li>
</ul>
</li>
</ol>
<p>摘要报告是一个 CSV 文件，包含以下数据点：</p>
<div class="overflow-x-auto">
  <table
  >
    <thead class="bg-gray-100 dark:bg-gray-800">
        <tr>
            <th
              class="p-2">字段</th>
            <th
              class="p-2">描述</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td
              class="p-2"><code>DATE_GRANULARITY</code></td>
            <td
              class="p-2">数据的周或月粒度。指示数据是按周还是按月聚合。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DATE_REFERENCE</code></td>
            <td
              class="p-2">周或月的开始日期，格式为 YYYY-MM-DD（例如，<code>2025-09-29</code> 表示 2025 年 9 月 29 日开始的周）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>PUBLISHER_NAME</code></td>
            <td
              class="p-2">拥有该仓库的 Docker 组织名称（例如 <code>demonstrationorg</code>）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>LEVEL</code></td>
            <td
              class="p-2">数据的聚合级别 - <code>repository</code>（整个仓库的摘要）、<code>tag</code>（特定标签的摘要）或 <code>digest</code>（特定摘要的摘要）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>REFERENCE</code></td>
            <td
              class="p-2">被汇总的具体引用 - 仓库名称、标签名称或摘要哈希，具体取决于级别。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DATA_DOWNLOADS</code></td>
            <td
              class="p-2">实际镜像下载次数。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>VERSION_CHECKS</code></td>
            <td
              class="p-2">执行的版本检查次数（用于检查更新而不下载完整镜像的 HEAD 请求）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>EVENT_COUNT</code></td>
            <td
              class="p-2">事件总数，计算为数据下载和版本检查的总和。</td>
        </tr>
    </tbody>
  </table>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="趋势报告">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e8%b6%8b%e5%8a%bf%e6%8a%a5%e5%91%8a">
    趋势报告
  </a>
</h3>

<p>趋势报告帮助您了解容器镜像的采用情况随时间的变化。它提供了跨仓库和标签的拉取活动可见性，使您能够识别采用模式、版本迁移趋势和使用环境（例如，本地开发、CI/CD、生产）。</p>
<p>您可以使用此报告回答以下问题：</p>
<ul>
<li>哪些版本正在获得或失去关注？</li>
<li>新版本是否正在被采用？</li>
<li>使用情况在不同云服务提供商之间如何变化？</li>
</ul>
<p>访问报告：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com/" rel="noopener">Docker Hub</a>。</li>
<li>在顶部导航中选择 <strong>My Hub</strong>。</li>
<li>在左侧导航中选择您的组织。</li>
<li>在左侧导航中选择 <strong>Analytics</strong> &gt; <strong>Trends</strong>。</li>
<li>选择 <strong>DATA BY WEEK</strong> 或 <strong>DATA BY MONTH</strong> 以选择数据粒度。</li>
<li>为所需周或月选择 <strong>Download report</strong>。</li>
</ol>
<p>趋势报告是一个 CSV 文件，包含以下数据点：</p>
<div class="overflow-x-auto">
  <table
  >
    <thead class="bg-gray-100 dark:bg-gray-800">
        <tr>
            <th
              class="p-2">字段</th>
            <th
              class="p-2">描述</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td
              class="p-2"><code>DATE_GRANULARITY</code></td>
            <td
              class="p-2">数据的周或月粒度。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DATE_REFERENCE</code></td>
            <td
              class="p-2">周或月的开始日期。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>PUBLISHER_NAME</code></td>
            <td
              class="p-2">拥有该仓库的组织名称。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>IMAGE_REPOSITORY</code></td>
            <td
              class="p-2">镜像仓库的完整名称（例如 <code>demonstrationorg/scout-demo</code>）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>NAMESPACE</code></td>
            <td
              class="p-2">拥有该仓库的 Docker 组织或命名空间。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>IP_COUNTRY</code></td>
            <td
              class="p-2">拉取请求来源的国家/地区代码（ISO 3166-1 alpha-2）（例如 <code>US</code>, <code>CA</code>）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>CLOUD_SERVICE_PROVIDER</code></td>
            <td
              class="p-2">拉取请求使用的云服务提供商（例如 <code>gcp</code>, <code>aws</code>, <code>azure</code>）或非云提供商的 <code>no csp</code>。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>USER_AGENT</code></td>
            <td
              class="p-2">用于拉取镜像的客户端应用程序或工具（例如 <code>docker</code>, <code>docker-scout</code>, <code>node-fetch</code>, <code>regclient</code>）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>TAG</code></td>
            <td
              class="p-2">被拉取的特定镜像标签，如果未使用特定标签则为 <code>\\N</code>。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DATA_DOWNLOADS</code></td>
            <td
              class="p-2">指定条件下的数据下载次数。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>VERSION_CHECKS</code></td>
            <td
              class="p-2">在不下载完整镜像的情况下执行的版本检查（HEAD 请求）次数。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>PULLS</code></td>
            <td
              class="p-2">拉取请求总数（数据下载 + 版本检查）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>UNIQUE_AUTHENTICATED_USERS</code></td>
            <td
              class="p-2">执行拉取操作的唯一认证用户数。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>UNIQUE_UNAUTHENTICATED_USERS</code></td>
            <td
              class="p-2">执行拉取操作的唯一未认证用户数。</td>
        </tr>
    </tbody>
  </table>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="技术栈分析报告">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%8a%80%e6%9c%af%e6%a0%88%e5%88%86%e6%9e%90%e6%8a%a5%e5%91%8a">
    技术栈分析报告
  </a>
</h3>

<p>技术栈分析报告提供关于您的 Docker Verified Publisher (DVP) 镜像在真实世界技术栈中如何与其他容器镜像一起使用的洞察。该报告帮助您了解镜像运行的技术生态系统，并识别与其他镜像的共同使用模式。</p>
<p>您可以使用此报告回答以下问题：</p>
<ul>
<li>哪些其他镜像通常与您的镜像一起使用？</li>
<li>您的用户群中有多少百分比也使用特定的互补技术？</li>
<li>您的生态系统中有多少公司同时使用您的镜像和其他流行镜像？</li>
<li>您的用户中最受欢迎的技术栈是什么？</li>
</ul>
<p>访问报告：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com/" rel="noopener">Docker Hub</a>。</li>
<li>在顶部导航中选择 <strong>My Hub</strong>。</li>
<li>在左侧导航中选择您的组织。</li>
<li>在左侧导航中选择 <strong>Analytics</strong> &gt; <strong>Technographic</strong>。</li>
<li>选择 <strong>DATA BY WEEK</strong> 或 <strong>DATA BY MONTH</strong> 以选择数据粒度。</li>
<li>为所需周或月选择 <strong>Download report</strong>。</li>
</ol>
<p>技术栈分析报告是一个 CSV 文件，包含以下数据点：</p>
<div class="overflow-x-auto">
  <table
  >
    <thead class="bg-gray-100 dark:bg-gray-800">
        <tr>
            <th
              class="p-2">字段</th>
            <th
              class="p-2">描述</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td
              class="p-2"><code>DATE_GRANULARITY</code></td>
            <td
              class="p-2">数据的周或月粒度。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DATE_REFERENCE</code></td>
            <td
              class="p-2">周或月的开始日期，格式为 YYYY-MM-DD。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>PUBLISHER_ID</code></td>
            <td
              class="p-2">发布者组织的唯一标识符。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>PUBLISHER_NAME</code></td>
            <td
              class="p-2">拥有 DVP 仓库的组织名称。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DVPP_IMAGE</code></td>
            <td
              class="p-2">您的 Docker Verified Publisher 镜像仓库名称。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>PAIRED_IMAGE</code></td>
            <td
              class="p-2">与您的 DVP 镜像共同使用的其他镜像仓库。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>USERS</code></td>
            <td
              class="p-2">在时间段内同时拉取了您的 DVP 镜像和配对镜像的唯一用户数。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>TOTAL_PULLERS</code></td>
            <td
              class="p-2">在时间段内拉取了您的 DVP 镜像的唯一用户总数。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>PCT_USERS</code></td>
            <td
              class="p-2">同时使用配对镜像的您的镜像用户百分比（用户数/总拉取用户数）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DOMAINS</code></td>
            <td
              class="p-2">同时拉取了您的 DVP 镜像和配对镜像的唯一公司域名数量。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>TOTAL_DOMAINS</code></td>
            <td
              class="p-2">拉取了您的 DVP 镜像的唯一公司域名总数。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>PCT_DOMAINS</code></td>
            <td
              class="p-2">使用您镜像的公司域名中同时使用配对镜像的百分比（域名数/总域名数）。</td>
        </tr>
    </tbody>
  </table>
</div>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Note
      </span>
    </div>
    <div class="admonition-content">
      <p>为保护用户隐私并确保统计显著性，技术栈分析报告仅包含至少有 10 个唯一用户的镜像配对。个人、一次性使用和大学电子邮件域名不包括在公司域名分析中。</p>
    </div>
  </blockquote>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="技术栈公司分析报告">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%8a%80%e6%9c%af%e6%a0%88%e5%85%ac%e5%8f%b8%e5%88%86%e6%9e%90%e6%8a%a5%e5%91%8a">
    技术栈公司分析报告
  </a>
</h3>

<p>技术栈公司分析报告提供详细视图，显示哪些特定公司（通过其域名识别）正在将您的 Docker Verified Publisher (DVP) 镜像与其他容器镜像一起使用。该报告让您了解实际采用您技术栈组合的组织，从而实现有针对性的业务开发和合作伙伴机会。</p>
<p>您可以使用此报告回答以下问题：</p>
<ul>
<li>哪些公司正在将我的镜像与特定的互补技术一起使用？</li>
<li>我的目标市场中的企业客户采用了哪些技术栈？</li>
<li>哪些组织可能是合作伙伴讨论的良好候选对象？</li>
<li>如何识别已经在使用相关技术的潜在客户？</li>
</ul>
<p>访问报告：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com/" rel="noopener">Docker Hub</a>。</li>
<li>在顶部导航中选择 <strong>My Hub</strong>。</li>
<li>在左侧导航中选择您的组织。</li>
<li>在左侧导航中选择 <strong>Analytics</strong> &gt; <strong>Technographic</strong>。</li>
<li>选择 <strong>DATA BY WEEK</strong> 或 <strong>DATA BY MONTH</strong> 以选择数据粒度。</li>
<li>为所需周或月选择 <strong>Download report</strong>。</li>
</ol>
<p>技术栈公司分析报告是一个 CSV 文件，包含以下数据点：</p>
<div class="overflow-x-auto">
  <table
  >
    <thead class="bg-gray-100 dark:bg-gray-800">
        <tr>
            <th
              class="p-2">字段</th>
            <th
              class="p-2">描述</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td
              class="p-2"><code>DATE_GRANULARITY</code></td>
            <td
              class="p-2">数据的周或月粒度。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DATE_REFERENCE</code></td>
            <td
              class="p-2">周或月的开始日期，格式为 YYYY-MM-DD。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>PUBLISHER_NAME</code></td>
            <td
              class="p-2">拥有 DVP 仓库的组织名称。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DOMAIN</code></td>
            <td
              class="p-2">同时拉取了您的 DVP 镜像和配对镜像的公司域名（例如 <code>example.com</code>）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DVPP_IMAGE</code></td>
            <td
              class="p-2">您的 Docker Verified Publisher 镜像仓库名称。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>PAIRED_IMAGE</code></td>
            <td
              class="p-2">该公司与您的 DVP 镜像一起使用的其他镜像仓库。</td>
        </tr>
    </tbody>
  </table>
</div>
<p>每一行代表一个公司域名、您的 DVP 镜像和另一个镜像在指定时间段内共同使用的唯一组合。</p>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Note
      </span>
    </div>
    <div class="admonition-content">
      <p>为保护隐私和确保数据质量，此报告排除了个人电子邮件域名、一次性电子邮件服务和大学域名。分析中仅包含商业和组织域名。</p>
    </div>
  </blockquote>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="追踪公司分析报告">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e8%bf%bd%e8%b8%aa%e5%85%ac%e5%8f%b8%e5%88%86%e6%9e%90%e6%8a%a5%e5%91%8a">
    追踪公司分析报告
  </a>
</h3>

<p>追踪公司分析报告提供关于特定公司如何使用您的 Docker Verified Publisher (DVP) 镜像的详细洞察。该报告帮助您了解客户群和潜在客户中的使用模式、部署环境和采用趋势。</p>
<p>您可以使用此报告回答以下问题：</p>
<ul>
<li>特定公司在不同环境中如何使用我的镜像？</li>
<li>在本地开发、CI/CD 和生产中看到了哪些部署模式？</li>
<li>哪些公司是我的镜像的重度用户？</li>
<li>对于被追踪的公司，使用情况在地理位置和云服务提供商之间如何变化？</li>
</ul>
<p>访问报告：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com/" rel="noopener">Docker Hub</a>。</li>
<li>在顶部导航中选择 <strong>My Hub</strong>。</li>
<li>在左侧导航中选择您的组织。</li>
<li>在左侧导航中选择 <strong>Analytics</strong> &gt; <strong>Tracked Companies</strong>。</li>
<li>选择 <strong>DATA BY WEEK</strong> 或 <strong>DATA BY MONTH</strong> 以选择数据粒度。</li>
<li>为所需周或月选择 <strong>Download report</strong>。</li>
</ol>
<p>追踪公司分析报告是一个 CSV 文件，包含以下数据点：</p>
<div class="overflow-x-auto">
  <table
  >
    <thead class="bg-gray-100 dark:bg-gray-800">
        <tr>
            <th
              class="p-2">字段</th>
            <th
              class="p-2">描述</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td
              class="p-2"><code>DATE_GRANULARITY</code></td>
            <td
              class="p-2">数据的周或月粒度。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DATE_REFERENCE</code></td>
            <td
              class="p-2">周或月的开始日期，格式为 YYYY-MM-DD。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>PUBLISHER_NAME</code></td>
            <td
              class="p-2">拥有 DVP 仓库的组织名称。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DOMAIN</code></td>
            <td
              class="p-2">与镜像拉取相关的公司域名（例如 <code>docker.com</code>）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>IP_COUNTRY</code></td>
            <td
              class="p-2">拉取请求来源的国家/地区代码（ISO 3166-1 alpha-2）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>CLOUD_SERVICE_PROVIDER</code></td>
            <td
              class="p-2">拉取请求使用的云服务提供商或非云提供商的 <code>no csp</code>。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>USER_AGENT</code></td>
            <td
              class="p-2">用于拉取镜像的客户端应用程序或工具。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>INFERRED_USE_CASE</code></td>
            <td
              class="p-2">基于用户代理和云服务提供商分析推断的部署环境。值包括：<br>• <code>Local Dev</code>: 本地开发环境（例如 Docker Desktop、直接 <code>docker</code> 命令）<br>• <code>CI/CD</code>: 持续集成/部署管道（例如 containerd、构建工具、注册表镜像）<br>• <code>Prod</code>: 生产环境（例如 Kubernetes、容器编排平台）<br>• <code>Unknown</code>: 无法根据可用数据确定用例</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>IMAGE_REPOSITORY</code></td>
            <td
              class="p-2">被拉取的特定 DVP 镜像仓库。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>DATA_DOWNLOADS</code></td>
            <td
              class="p-2">此组合的实际镜像层下载次数。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>VERSION_CHECKS</code></td>
            <td
              class="p-2">在不下载完整镜像的情况下执行的版本检查（HEAD 请求）次数。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>PULLS</code></td>
            <td
              class="p-2">拉取请求总数（数据下载 + 版本检查）。</td>
        </tr>
        <tr>
            <td
              class="p-2"><code>UNIQUE_AUTHENTICATED_USERS</code></td>
            <td
              class="p-2">来自该域名并执行了拉取操作的唯一认证用户数。</td>
        </tr>
    </tbody>
  </table>
</div>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Note
      </span>
    </div>
    <div class="admonition-content">
      <p>用例推断是通过分析用户代理模式和云服务提供商使用情况来确定的。在云基础设施上使用的本地开发工具被重新归类为 CI/CD，在云基础设施上使用的 CI/CD 工具被重新归类为生产，以更好地反映实际的部署模式。</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'DSOS-%E5%92%8C%E6%97%A7%E7%89%88-DVP-%E8%AE%A1%E5%88%92' && 'hidden'"
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
      <p>旧版 DVP 计划适用于尚未续订 DVP Core 的现有客户。DVP 旧版计划已弃用，并将被停用。有关更多信息，请联系您的 Docker 销售代表或 <a class="link" href="https://www.docker.com/partners/programs/" rel="noopener">Docker</a>。</p>
    </div>
  </blockquote>


<h2 class=" scroll-mt-20 flex items-center gap-2" id="查看镜像的分析数据">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%9f%a5%e7%9c%8b%e9%95%9c%e5%83%8f%e7%9a%84%e5%88%86%e6%9e%90%e6%95%b0%e6%8d%ae">
    查看镜像的分析数据
  </a>
</h2>

<p>您可以在以下 URL 的 <strong>Insights and analytics</strong> 仪表板上找到仓库的分析数据：
<code>https://hub.docker.com/orgs/{namespace}/insights/images</code>。该仪表板包含使用数据的可视化图表和一个表格，您可以在其中将数据下载为 CSV 文件。</p>
<p>要在图表中查看数据：</p>
<ul>
<li>选择数据粒度：周或月</li>
<li>选择时间间隔：3、6 或 12 个月</li>
<li>在列表中选择一个或多个仓库</li>
</ul>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="https://docs.docker.com/docker-hub/images/chart.png"
    alt="洞察与分析图表可视化"
    
    
    class="mx-auto rounded-sm"
  />
  
  <template x-teleport="body">
    <div
      x-show="zoom"
      @click="zoom = false"
      x-transition.opacity.duration.250ms
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/100 p-6"
    >
      <button class="icon-svg fixed top-6 right-8 z-30 text-white">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-438 270-228q-9 9-21 9t-21-9q-9-9-9-21t9-21l210-210-210-210q-9-9-9-21t9-21q9-9 21-9t21 9l210 210 210-210q9-9 21-9t21 9q9 9 9 21t-9 21L522-480l210 210q9 9 9 21t-9 21q-9 9-21 9t-21-9L480-438Z"/></svg>
      </button>
      <img
        loading="lazy"
        class="max-h-full max-w-full rounded-sm"
        src="https://docs.docker.com/docker-hub/images/chart.png"
        alt="洞察与分析图表可视化"
      />
    </div>
  </template>
</figure>


  

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
      <p>将光标悬停在图表上会显示工具提示，显示时间点的精确数据。</p>
    </div>
  </blockquote>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="分享分析数据">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%88%86%e4%ba%ab%e5%88%86%e6%9e%90%e6%95%b0%e6%8d%ae">
    分享分析数据
  </a>
</h3>

<p>您可以使用图表顶部的 <strong>Share</strong> 图标与他人共享可视化图表。这是与组织内其他人共享统计数据的便捷方式。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="https://docs.docker.com/docker-hub/images/chart-share-icon.png"
    alt="图表分享图标"
    
    
    class="mx-auto rounded-sm"
  />
  
  <template x-teleport="body">
    <div
      x-show="zoom"
      @click="zoom = false"
      x-transition.opacity.duration.250ms
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/100 p-6"
    >
      <button class="icon-svg fixed top-6 right-8 z-30 text-white">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-438 270-228q-9 9-21 9t-21-9q-9-9-9-21t9-21l210-210-210-210q-9-9-9-21t9-21q9-9 21-9t21 9l210 210 210-210q9-9 21-9t21 9q9 9 9 21t-9 21L522-480l210 210q9 9 9 21t-9 21q-9 9-21 9t-21-9L480-438Z"/></svg>
      </button>
      <img
        loading="lazy"
        class="max-h-full max-w-full rounded-sm"
        src="https://docs.docker.com/docker-hub/images/chart-share-icon.png"
        alt="图表分享图标"
      />
    </div>
  </template>
</figure>
<p>选择该图标会生成一个链接并复制到您的剪贴板。该链接会保留您所做的显示选择。当有人访问该链接时，<strong>Insights and analytics</strong> 页面将打开，并显示与您创建链接时设置的相同配置的图表。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="扩展分析数据">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%89%a9%e5%b1%95%e5%88%86%e6%9e%90%e6%95%b0%e6%8d%ae">
    扩展分析数据
  </a>
</h2>

<p>如果您已在扩展市场中发布了 Docker 扩展，您还可以获取有关扩展使用情况的分析数据，以 CSV 文件形式提供。您可以从以下 URL 的 <strong>Insights and analytics</strong> 仪表板下载扩展 CSV 报告：
<code>https://hub.docker.com/orgs/{namespace}/insights/extensions</code>。如果您的 Docker 命名空间包含市场中已知的扩展，您将看到一个 <strong>Extensions</strong> 选项卡，其中列出了扩展的 CSV 文件。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="导出分析数据">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%af%bc%e5%87%ba%e5%88%86%e6%9e%90%e6%95%b0%e6%8d%ae">
    导出分析数据
  </a>
</h2>

<p>您可以从 Web 仪表板导出分析数据，或使用 
    
  
  <a class="link" href="https://docs.docker.com/reference/api/dvp/latest/">DVP Data API</a>。组织的所有成员均可访问分析数据。</p>
<p>数据以可下载的 CSV 文件形式提供，格式为每周（周一至周日）或每月。每月数据可从下一个日历月的第一天开始获取。您可以将此数据导入您自己的系统，或者作为电子表格进行手动分析。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="导出数据">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%af%bc%e5%87%ba%e6%95%b0%e6%8d%ae">
    导出数据
  </a>
</h3>

<p>使用 Docker Hub 网站导出组织镜像的使用数据，请按照以下步骤操作：</p>
<ol>
<li>
<p>登录 <a class="link" href="https://hub.docker.com/" rel="noopener">Docker Hub</a> 并选择 <strong>My Hub</strong>。</p>
</li>
<li>
<p>选择您的组织并选择 <strong>Analytics</strong>。</p>
</li>
<li>
<p>设置要导出分析数据的时间范围。</p>
<p>摘要和原始数据的可下载 CSV 文件将出现在右侧。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="https://docs.docker.com/docker-hub/images/download-analytics-data.png"
    alt="分析数据的筛选选项和下载链接"
    
    
    class="mx-auto rounded-sm"
  />
  
  <template x-teleport="body">
    <div
      x-show="zoom"
      @click="zoom = false"
      x-transition.opacity.duration.250ms
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/100 p-6"
    >
      <button class="icon-svg fixed top-6 right-8 z-30 text-white">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-438 270-228q-9 9-21 9t-21-9q-9-9-9-21t9-21l210-210-210-210q-9-9-9-21t9-21q9-9 21-9t21 9l210 210 210-210q9-9 21-9t21 9q9 9 9 21t-9 21L522-480l210 210q9 9 9 21t-9 21q-9 9-21 9t-21-9L480-438Z"/></svg>
      </button>
      <img
        loading="lazy"
        class="max-h-full max-w-full rounded-sm"
        src="https://docs.docker.com/docker-hub/images/download-analytics-data.png"
        alt="分析数据的筛选选项和下载链接"
      />
    </div>
  </template>
</figure>
</li>
</ol>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="使用-api-导出数据">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bd%bf%e7%94%a8-api-%e5%af%bc%e5%87%ba%e6%95%b0%e6%8d%ae">
    使用 API 导出数据
  </a>
</h3>

<p>HTTP API 端点位于：
<code>https://hub.docker.com/api/publisher/analytics/v1</code>。了解如何使用 API 导出数据，请参阅 
    
  
  <a class="link" href="https://docs.docker.com/reference/api/dvp/latest/">DVP Data API 文档</a>。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="数据点">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%95%b0%e6%8d%ae%e7%82%b9">
    数据点
  </a>
</h2>

<p>以原始或摘要格式导出数据。每种格式包含不同的数据点和结构。</p>
<p>以下部分描述了每种格式的可用数据点。<strong>Date added</strong> 列显示了字段首次引入的时间。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="镜像拉取原始数据">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%95%9c%e5%83%8f%e6%8b%89%e5%8f%96%e5%8e%9f%e5%a7%8b%e6%95%b0%e6%8d%ae">
    镜像拉取原始数据
  </a>
</h3>

<p>原始数据格式包含以下数据点。CSV 文件中的每一行代表一次镜像拉取。</p>
<div class="overflow-x-auto">
  <table
  >
    <thead class="bg-gray-100 dark:bg-gray-800">
        <tr>
            <th
              class="p-2">数据点</th>
            <th
              class="p-2">描述</th>
            <th
              class="p-2">添加日期</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td
              class="p-2">Action</td>
            <td
              class="p-2">请求类型，参见 <a class="link" href="#image-pulls-action-classification-rules">操作分类规则</a>。<code>pull_by_tag</code>、<code>pull_by_digest</code> 或 <code>version_check</code> 之一。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Action day</td>
            <td
              class="p-2">时间戳的日期部分：<code>YYYY-MM-DD</code>。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Country</td>
            <td
              class="p-2">请求来源国家/地区。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Digest</td>
            <td
              class="p-2">镜像摘要。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">HTTP method</td>
            <td
              class="p-2">请求中使用的 HTTP 方法，详情请参见 
  <a class="link" href="/registry/spec/api/">registry API 文档</a>。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Host</td>
            <td
              class="p-2">事件中使用的云服务提供商。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Namespace</td>
            <td
              class="p-2">Docker 
  <a class="link" href="/admin/organization/orgs/">组织</a>（镜像命名空间）。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Reference</td>
            <td
              class="p-2">请求中使用的镜像摘要或标签。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Repository</td>
            <td
              class="p-2">Docker 
  <a class="link" href="/docker-hub/repos/">仓库</a>（镜像名称）。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Tag (included when available)</td>
            <td
              class="p-2">仅当请求引用标签时才可用的标签名称。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Timestamp</td>
            <td
              class="p-2">请求的日期和时间：<code>YYYY-MM-DD 00:00:00</code>。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Type</td>
            <td
              class="p-2">事件来源的行业。<code>business</code>、<code>isp</code>、<code>hosting</code>、<code>education</code>、<code>null</code> 之一。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">User agent tool</td>
            <td
              class="p-2">用户用于拉取镜像的应用程序（例如 <code>docker</code> 或 <code>containerd</code>）。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">User agent version</td>
            <td
              class="p-2">用于拉取镜像的应用程序版本。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Domain</td>
            <td
              class="p-2">请求来源域名，参见 <a class="link" href="#%e9%9a%90%e7%a7%81">隐私</a>。</td>
            <td
              class="p-2">2022 年 10 月 11 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Owner</td>
            <td
              class="p-2">拥有该仓库的组织名称。</td>
            <td
              class="p-2">2022 年 12 月 19 日</td>
        </tr>
    </tbody>
  </table>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="镜像拉取摘要数据">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%95%9c%e5%83%8f%e6%8b%89%e5%8f%96%e6%91%98%e8%a6%81%e6%95%b0%e6%8d%ae">
    镜像拉取摘要数据
  </a>
</h3>

<p>有两种级别的摘要数据可用：</p>
<ul>
<li>仓库级别：每个命名空间和仓库的摘要</li>
<li>标签或摘要级别：每个命名空间、仓库和引用（标签或摘要）的摘要</li>
</ul>
<p>摘要数据格式包含选定时间范围内的以下数据点：</p>
<div class="overflow-x-auto">
  <table
  >
    <thead class="bg-gray-100 dark:bg-gray-800">
        <tr>
            <th
              class="p-2">数据点</th>
            <th
              class="p-2">描述</th>
            <th
              class="p-2">添加日期</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td
              class="p-2">Unique IP address</td>
            <td
              class="p-2">唯一 IP 地址的数量，参见 <a class="link" href="#%e9%9a%90%e7%a7%81">隐私</a>。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Pull by tag</td>
            <td
              class="p-2">GET 请求，按摘要或按标签。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Pull by digest</td>
            <td
              class="p-2">按摘要的 GET 或 HEAD 请求，或按摘要的 HEAD。</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Version check</td>
            <td
              class="p-2">按标签的 HEAD，后未跟随 GET</td>
            <td
              class="p-2">2022 年 1 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Owner</td>
            <td
              class="p-2">拥有该仓库的组织名称。</td>
            <td
              class="p-2">2022 年 12 月 19 日</td>
        </tr>
    </tbody>
  </table>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="镜像拉取操作分类规则">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%95%9c%e5%83%8f%e6%8b%89%e5%8f%96%e6%93%8d%e4%bd%9c%e5%88%86%e7%b1%bb%e8%a7%84%e5%88%99">
    镜像拉取操作分类规则
  </a>
</h3>

<p>一个操作代表与 <code>docker pull</code> 相关的多个请求事件。拉取操作按类别分组，以使数据在理解用户行为和意图方面更有意义。类别包括：</p>
<ul>
<li>版本检查</li>
<li>按标签拉取</li>
<li>按摘要拉取</li>
</ul>
<p>自动化系统会频繁检查您的镜像是否有新版本。能够区分 CI 中的“版本检查”与用户的实际镜像拉取，可以让您更深入地了解用户的行为。</p>
<p>下表描述了用于确定拉取背后意图的规则。要提供反馈或询问有关这些规则的问题，<a class="link" href="https://forms.gle/nb7beTUQz9wzXy1b6" rel="noopener">请填写 Google 表格</a>。</p>
<div class="overflow-x-auto">
  <table
  >
    <thead class="bg-gray-100 dark:bg-gray-800">
        <tr>
            <th
              class="p-2" style="text-align: left">起始事件</th>
            <th
              class="p-2" style="text-align: left">引用</th>
            <th
              class="p-2" style="text-align: left">后续操作</th>
            <th
              class="p-2" style="text-align: left">结果操作</th>
            <th
              class="p-2" style="text-align: left">用例</th>
            <th
              class="p-2" style="text-align: left">备注</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td
              class="p-2" style="text-align: left">HEAD</td>
            <td
              class="p-2" style="text-align: left">标签</td>
            <td
              class="p-2" style="text-align: left">N/A</td>
            <td
              class="p-2" style="text-align: left">版本检查</td>
            <td
              class="p-2" style="text-align: left">用户本地机器上已存在所有层</td>
            <td
              class="p-2" style="text-align: left">这类似于用户本地已存在所有镜像层时的按标签拉取用例，但它区分了用户意图并进行相应分类。</td>
        </tr>
        <tr>
            <td
              class="p-2" style="text-align: left">GET</td>
            <td
              class="p-2" style="text-align: left">标签</td>
            <td
              class="p-2" style="text-align: left">N/A</td>
            <td
              class="p-2" style="text-align: left">按标签拉取</td>
            <td
              class="p-2" style="text-align: left">用户本地机器上已存在所有层和/或镜像是单架构的</td>
            <td
              class="p-2" style="text-align: left"></td>
        </tr>
        <tr>
            <td
              class="p-2" style="text-align: left">GET</td>
            <td
              class="p-2" style="text-align: left">标签</td>
            <td
              class="p-2" style="text-align: left">按不同摘要获取</td>
            <td
              class="p-2" style="text-align: left">按标签拉取</td>
            <td
              class="p-2" style="text-align: left">镜像是多架构的</td>
            <td
              class="p-2" style="text-align: left">第二次按摘要的 GET 必须与第一次不同。</td>
        </tr>
        <tr>
            <td
              class="p-2" style="text-align: left">HEAD</td>
            <td
              class="p-2" style="text-align: left">标签</td>
            <td
              class="p-2" style="text-align: left">按相同摘要获取</td>
            <td
              class="p-2" style="text-align: left">按标签拉取</td>
            <td
              class="p-2" style="text-align: left">镜像是多架构的，但部分或所有镜像层已存在于本地机器上</td>
            <td
              class="p-2" style="text-align: left">按标签的 HEAD 发送最新的摘要，后续的 GET 必须是相同的摘要。如果镜像是多架构的，可能会发生额外的 GET（请参见本表中的下一行）。如果用户不需要最新的摘要，则用户执行按摘要的 HEAD。</td>
        </tr>
        <tr>
            <td
              class="p-2" style="text-align: left">HEAD</td>
            <td
              class="p-2" style="text-align: left">标签</td>
            <td
              class="p-2" style="text-align: left">按相同摘要获取，然后按不同摘要进行第二次获取</td>
            <td
              class="p-2" style="text-align: left">按标签拉取</td>
            <td
              class="p-2" style="text-align: left">镜像是多架构的</td>
            <td
              class="p-2" style="text-align: left">按标签的 HEAD 发送最新的摘要，后续的 GET 必须是相同的摘要。由于镜像是多架构的，因此存在按不同摘要的第二次 GET。如果用户不需要最新的摘要，则用户执行按摘要的 HEAD。</td>
        </tr>
        <tr>
            <td
              class="p-2" style="text-align: left">HEAD</td>
            <td
              class="p-2" style="text-align: left">标签</td>
            <td
              class="p-2" style="text-align: left">按相同摘要获取，然后按不同摘要进行第二次获取</td>
            <td
              class="p-2" style="text-align: left">按标签拉取</td>
            <td
              class="p-2" style="text-align: left">镜像是多架构的</td>
            <td
              class="p-2" style="text-align: left">按标签的 HEAD 发送最新的摘要，后续的 GET 必须是相同的摘要。由于镜像是多架构的，因此存在按不同摘要的第二次 GET。如果用户不需要最新的摘要，则用户执行按摘要的 HEAD。</td>
        </tr>
        <tr>
            <td
              class="p-2" style="text-align: left">GET</td>
            <td
              class="p-2" style="text-align: left">摘要</td>
            <td
              class="p-2" style="text-align: left">N/A</td>
            <td
              class="p-2" style="text-align: left">按摘要拉取</td>
            <td
              class="p-2" style="text-align: left">用户本地机器上已存在所有层和/或镜像是单架构的</td>
            <td
              class="p-2" style="text-align: left"></td>
        </tr>
        <tr>
            <td
              class="p-2" style="text-align: left">HEAD</td>
            <td
              class="p-2" style="text-align: left">摘要</td>
            <td
              class="p-2" style="text-align: left">N/A</td>
            <td
              class="p-2" style="text-align: left">按摘要拉取</td>
            <td
              class="p-2" style="text-align: left">用户本地机器上已存在所有层</td>
            <td
              class="p-2" style="text-align: left"></td>
        </tr>
        <tr>
            <td
              class="p-2" style="text-align: left">GET</td>
            <td
              class="p-2" style="text-align: left">摘要</td>
            <td
              class="p-2" style="text-align: left">按不同摘要获取</td>
            <td
              class="p-2" style="text-align: left">按摘要拉取</td>
            <td
              class="p-2" style="text-align: left">镜像是多架构的</td>
            <td
              class="p-2" style="text-align: left">第二次按摘要的 GET 必须与第一次不同。</td>
        </tr>
        <tr>
            <td
              class="p-2" style="text-align: left">HEAD</td>
            <td
              class="p-2" style="text-align: left">摘要</td>
            <td
              class="p-2" style="text-align: left">按相同摘要获取</td>
            <td
              class="p-2" style="text-align: left">按摘要拉取</td>
            <td
              class="p-2" style="text-align: left">镜像是单架构的和/或镜像是多架构的，但部分镜像已存在于本地机器上</td>
            <td
              class="p-2" style="text-align: left"></td>
        </tr>
        <tr>
            <td
              class="p-2" style="text-align: left">HEAD</td>
            <td
              class="p-2" style="text-align: left">摘要</td>
            <td
              class="p-2" style="text-align: left">按相同摘要获取，然后按不同摘要进行第二次获取</td>
            <td
              class="p-2" style="text-align: left">按摘要拉取</td>
            <td
              class="p-2" style="text-align: left">镜像是多架构的</td>
            <td
              class="p-2" style="text-align: left"></td>
        </tr>
    </tbody>
  </table>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="扩展摘要数据">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%89%a9%e5%b1%95%e6%91%98%e8%a6%81%e6%95%b0%e6%8d%ae">
    扩展摘要数据
  </a>
</h3>

<p>有两种级别的扩展摘要数据可用：</p>
<ul>
<li>核心摘要，包含基本的扩展使用信息：扩展安装次数、卸载次数和总安装次数</li>
</ul>
<p>核心摘要数据文件包含选定时间范围内的以下数据点：</p>
<div class="overflow-x-auto">
  <table
  >
    <thead class="bg-gray-100 dark:bg-gray-800">
        <tr>
            <th
              class="p-2">数据点</th>
            <th
              class="p-2">描述</th>
            <th
              class="p-2">添加日期</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td
              class="p-2">Installs</td>
            <td
              class="p-2">扩展的安装次数</td>
            <td
              class="p-2">2024 年 2 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">TotalInstalls</td>
            <td
              class="p-2">扩展的总安装次数</td>
            <td
              class="p-2">2024 年 2 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Uninstalls</td>
            <td
              class="p-2">扩展的卸载次数</td>
            <td
              class="p-2">2024 年 2 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">TotalUninstalls</td>
            <td
              class="p-2">扩展的总卸载次数</td>
            <td
              class="p-2">2024 年 2 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Updates</td>
            <td
              class="p-2">扩展的更新次数</td>
            <td
              class="p-2">2024 年 2 月 1 日</td>
        </tr>
    </tbody>
  </table>
</div>
<ul>
<li>高级摘要，包含高级的扩展使用信息：按唯一用户划分的安装、卸载，以及按唯一用户划分的扩展打开次数。</li>
</ul>
<p>核心摘要数据文件包含选定时间范围内的以下数据点：</p>
<div class="overflow-x-auto">
  <table
  >
    <thead class="bg-gray-100 dark:bg-gray-800">
        <tr>
            <th
              class="p-2">数据点</th>
            <th
              class="p-2">描述</th>
            <th
              class="p-2">添加日期</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td
              class="p-2">Installs</td>
            <td
              class="p-2">扩展的安装次数</td>
            <td
              class="p-2">2024 年 2 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">UniqueInstalls</td>
            <td
              class="p-2">安装扩展的唯一用户数</td>
            <td
              class="p-2">2024 年 2 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Uninstalls</td>
            <td
              class="p-2">扩展的卸载次数</td>
            <td
              class="p-2">2024 年 2 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">UniqueUninstalls</td>
            <td
              class="p-2">卸载扩展的唯一用户数</td>
            <td
              class="p-2">2024 年 2 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">Usage</td>
            <td
              class="p-2">扩展选项卡的打开次数</td>
            <td
              class="p-2">2024 年 2 月 1 日</td>
        </tr>
        <tr>
            <td
              class="p-2">UniqueUsers</td>
            <td
              class="p-2">打开扩展选项卡的唯一用户数</td>
            <td
              class="p-2">2024 年 2 月 1 日</td>
        </tr>
    </tbody>
  </table>
</div>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="数据随时间的变化">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%95%b0%e6%8d%ae%e9%9a%8f%e6%97%b6%e9%97%b4%e7%9a%84%e5%8f%98%e5%8c%96">
    数据随时间的变化
  </a>
</h2>

<p>洞察与分析服务不断改进，以增加其为发布者带来的价值。某些更改可能包括添加新的数据点，或改进现有数据以使其更有用。</p>
<p>数据集中的更改（例如添加或删除字段）通常仅从该字段首次引入的日期开始适用，并向后兼容。</p>
<p>请参阅 <a class="link" href="#%e6%95%b0%e6%8d%ae%e7%82%b9">数据点</a> 部分中的表格，以查看特定数据点从哪个日期开始可用。</p>

      </div>
    
  </div>
</div>


## 隐私

本节包含有关隐私保护措施的信息，这些措施确保 Docker Hub 上的内容消费者保持完全匿名。

> [!IMPORTANT]
>
> Docker 绝不会在分析数据中共享任何个人身份信息 (PII)。

镜像拉取摘要数据集包含唯一 IP 地址计数。该数据点仅包含请求镜像的不同唯一 IP 地址的数量。单个 IP 地址永远不会被共享。

镜像拉取原始数据集包含用户 IP 域名作为数据点。这是与用于拉取镜像的 IP 地址关联的域名。如果 IP 类型为 `business`，则该域名代表与该 IP 地址关联的公司或组织（例如 `docker.com`）。对于任何非 `business` 的其他 IP 类型，该域名代表用于发出请求的互联网服务提供商或托管提供商。平均而言，只有约 30% 的拉取操作被归类为 `business` IP 类型（这因发布者和镜像而异）。
