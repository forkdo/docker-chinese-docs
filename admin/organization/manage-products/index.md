# 管理 Docker 产品





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Subscription:</span>
        
          <span>Team</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M30-240q-12.75 0-21.37-8.63Q0-257.25 0-270v-23q0-38.57 41.5-62.78Q83-380 150.38-380q12.16 0 23.39.5t22.23 2.15q-8 17.35-12 35.17-4 17.81-4 37.18v65H30Zm240 0q-12.75 0-21.37-8.63Q240-257.25 240-270v-35q0-32 17.5-58.5T307-410q32-20 76.5-30t96.5-10q53 0 97.5 10t76.5 30q32 20 49 46.5t17 58.5v35q0 12.75-8.62 21.37Q702.75-240 690-240H270Zm510 0v-65q0-19.86-3.5-37.43T765-377.27q11-1.73 22.17-2.23 11.17-.5 22.83-.5 67.5 0 108.75 23.77T960-293v23q0 12.75-8.62 21.37Q942.75-240 930-240H780ZM149.57-410q-28.57 0-49.07-20.56Q80-451.13 80-480q0-29 20.56-49.5Q121.13-550 150-550q29 0 49.5 20.5t20.5 49.93q0 28.57-20.5 49.07T149.57-410Zm660 0q-28.57 0-49.07-20.56Q740-451.13 740-480q0-29 20.56-49.5Q781.13-550 810-550q29 0 49.5 20.5t20.5 49.93q0 28.57-20.5 49.07T809.57-410ZM480-480q-50 0-85-35t-35-85q0-51 35-85.5t85-34.5q51 0 85.5 34.5T600-600q0 50-34.5 85T480-480Z"/></svg>
            
          </span>
        
          <span>Business</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M80-180v-600q0-24.75 17.63-42.38Q115.25-840 140-840h270q24.75 0 42.38 17.62Q470-804.75 470-780v105h350q24.75 0 42.38 17.62Q880-639.75 880-615v435q0 24.75-17.62 42.37Q844.75-120 820-120H140q-24.75 0-42.37-17.63Q80-155.25 80-180Zm60 0h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm165 495h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm165 495h350v-435H470v105h80v60h-80v105h80v60h-80v105Zm185-270v-60h60v60h-60Zm0 165v-60h60v60h-60Z"/></svg>
            
          </span>
        
      </div>
    

    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">For:</span>
        <span>Administrators</span>
        
          <span class="icon-svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M693-80q-78 0-133-55.5T505-267q0-78 55-133.5T693-456q77 0 132.5 55.5T881-267q0 76-55.5 131.5T693-80ZM160-522v-197q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v190q0 14-11 21.5t-24 2.5q-17-5-35.5-8t-36.5-3q-103 0-175.5 73T445-267q0 40 13.5 79t38.5 71q10 13 2.5 26T478-82q-69-20-122-51.5T251-237q-43-60-67-132.5T160-522Zm531 252q26 0 44-19t18-45q0-26-18-44t-44-18q-26 0-45 18t-19 44q0 26 19 45t45 19Zm-1 125q28 0 53-11t43-31q4-5 2.5-11t-6.5-8q-22-10-45-15.5t-47-5.5q-24 0-47 5t-45 16q-5 2-7 8t2 11q18 21 43.5 31.5T690-145Z"/></svg>
          </span>
        
      </div>
    
  </div>



在本节中，您将学习如何为您的组织管理访问权限并查看 Docker 产品的使用情况。有关每个产品的更详细信息，包括如何设置和配置它们，请参阅以下手册：

- [Docker Desktop](../../desktop/_index.md)
- [Docker Hub](../../docker-hub/_index.md)
- [Docker Build Cloud](../../build-cloud/_index.md)
- [Docker Scout](../../scout/_index.md)
- [Testcontainers Cloud](https://testcontainers.com/cloud/docs/#getting-started)
- [Docker Offload](../../offload/_index.md)

## 管理您组织的产品访问权限

您的订阅中包含的 Docker 产品的访问权限默认对所有用户开启。有关您订阅中包含的产品的概述，请参阅 [Docker 订阅和功能](https://www.docker.com/pricing/)。








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-Desktop' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Desktop' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Desktop'"
        
      >
        Docker Desktop
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Hub' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Hub'"
        
      >
        Docker Hub
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Build-Cloud' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Build-Cloud'"
        
      >
        Docker Build Cloud
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Scout' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Scout'"
        
      >
        Docker Scout
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Testcontainers-Cloud' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Testcontainers-Cloud'"
        
      >
        Testcontainers Cloud
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Offload' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Offload'"
        
      >
        Docker Offload
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Desktop' && 'hidden'"
      >
        
<h3 class=" scroll-mt-20 flex items-center gap-2" id="管理-docker-desktop-访问权限">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%ae%a1%e7%90%86-docker-desktop-%e8%ae%bf%e9%97%ae%e6%9d%83%e9%99%90">
    管理 Docker Desktop 访问权限
  </a>
</h3>

<p>要管理 Docker Desktop 访问权限：</p>
<ol>
<li>
    
  
  <a class="link" href="https://docs.docker.com/enterprise/security/enforce-sign-in/">强制登录</a>。</li>
<li>手动管理成员 <a class="link" href="https://docs.docker.com/admin/organization/members/">手动</a> 或使用 
    
  
  <a class="link" href="https://docs.docker.com/enterprise/security/provisioning/">配置</a>。</li>
</ol>
<p>启用强制登录后，只有您组织的成员才能在登录后使用 Docker Desktop。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Hub' && 'hidden'"
      >
        
<h3 class=" scroll-mt-20 flex items-center gap-2" id="管理-docker-hub-访问权限">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%ae%a1%e7%90%86-docker-hub-%e8%ae%bf%e9%97%ae%e6%9d%83%e9%99%90">
    管理 Docker Hub 访问权限
  </a>
</h3>

<p>要管理 Docker Hub 访问权限，请登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并配置 
    
  
  <a class="link" href="https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/">Registry Access Management</a> 或 
    
  
  <a class="link" href="https://docs.docker.com/enterprise/security/hardened-desktop/image-access-management/">Image Access Management</a>。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Build-Cloud' && 'hidden'"
      >
        
<h3 class=" scroll-mt-20 flex items-center gap-2" id="管理-docker-build-cloud-访问权限">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%ae%a1%e7%90%86-docker-build-cloud-%e8%ae%bf%e9%97%ae%e6%9d%83%e9%99%90">
    管理 Docker Build Cloud 访问权限
  </a>
</h3>

<p>要初步设置和配置 Docker Build Cloud，请登录 <a class="link" href="https://app.docker.com/build" rel="noopener">Docker Build Cloud</a> 并按照屏幕上的说明进行操作。</p>
<p>要管理 Docker Build Cloud 访问权限：</p>
<ol>
<li>以组织所有者身份登录 <a class="link" href="http://app.docker.com/build" rel="noopener">Docker Build Cloud</a>。</li>
<li>选择 <strong>Account settings</strong>。</li>
<li>选择 <strong>Lock access to Docker Build Account</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Scout' && 'hidden'"
      >
        
<h3 class=" scroll-mt-20 flex items-center gap-2" id="管理-docker-scout-访问权限">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%ae%a1%e7%90%86-docker-scout-%e8%ae%bf%e9%97%ae%e6%9d%83%e9%99%90">
    管理 Docker Scout 访问权限
  </a>
</h3>

<p>要初步设置和配置 Docker Scout，请登录 <a class="link" href="https://scout.docker.com/" rel="noopener">Docker Scout</a> 并按照屏幕上的说明进行操作。</p>
<p>要管理 Docker Scout 访问权限：</p>
<ol>
<li>以组织所有者身份登录 <a class="link" href="https://scout.docker.com/" rel="noopener">Docker Scout</a>。</li>
<li>选择您的组织，然后选择 <strong>Settings</strong>。</li>
<li>要管理为 Docker Scout 分析启用的仓库，请选择 <strong>Repository settings</strong>。有关更多信息，请参阅 <a class="link" href="https://docs.docker.com/scout/explore/dashboard/#repository-settings">仓库设置</a>。</li>
<li>要管理对 Docker Scout 的访问以在 Docker Desktop 上用于本地镜像，请使用 
    
  
  <a class="link" href="https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/">Settings Management</a> 并将 <code>sbomIndexing</code> 设置为 <code>false</code> 以禁用，或设置为 <code>true</code> 以启用。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Testcontainers-Cloud' && 'hidden'"
      >
        
<h3 class=" scroll-mt-20 flex items-center gap-2" id="管理-testcontainers-cloud-访问权限">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%ae%a1%e7%90%86-testcontainers-cloud-%e8%ae%bf%e9%97%ae%e6%9d%83%e9%99%90">
    管理 Testcontainers Cloud 访问权限
  </a>
</h3>

<p>要初步设置和配置 Testcontainers Cloud，请登录 <a class="link" href="https://app.testcontainers.cloud/" rel="noopener">Testcontainers Cloud</a> 并按照屏幕上的说明进行操作。</p>
<p>要管理对 Testcontainers Cloud 的访问权限：</p>
<ol>
<li>登录 <a class="link" href="https://app.testcontainers.cloud/" rel="noopener">Testcontainers Cloud</a> 并选择 <strong>Account</strong>。</li>
<li>选择 <strong>Settings</strong>，然后选择 <strong>Lock access to Testcontainers Cloud</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Offload' && 'hidden'"
      >
        
<h3 class=" scroll-mt-20 flex items-center gap-2" id="管理-docker-offload-访问权限">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%ae%a1%e7%90%86-docker-offload-%e8%ae%bf%e9%97%ae%e6%9d%83%e9%99%90">
    管理 Docker Offload 访问权限
  </a>
</h3>



  

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
      <p>Docker Offload 不包含在核心 Docker 订阅计划中。要使 Docker Offload 可用，您必须 <a class="link" href="https://www.docker.com/products/docker-offload/" rel="noopener">注册</a> 并订阅。</p>
    </div>
  </blockquote>

<p>要管理您组织的 Docker Offload 访问权限，请使用 
    
  
  <a class="link" href="https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/">Settings Management</a>：</p>
<ol>
<li>以组织所有者身份登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a>。</li>
<li>选择 <strong>Admin Console</strong> &gt; <strong>Desktop Settings Management</strong>。</li>
<li>配置 <strong>Enable Docker Offload</strong> 设置以控制 Docker Offload 功能在 Docker Desktop 中是否可用。您可以将此设置配置为五种状态：
<ul>
<li><strong>Always enabled</strong>：Docker Offload 始终启用，用户无法禁用。Offload 切换开关在 Docker Desktop 标题中始终可见。推荐用于无法在本地执行 Docker 的 VDI 环境。</li>
<li><strong>Enabled</strong>：Docker Offload 默认启用，但用户可以在 Docker Desktop 设置中禁用它。适用于混合环境。</li>
<li><strong>Disabled</strong>：Docker Offload 默认禁用，但用户可以在 Docker Desktop 设置中启用它。</li>
<li><strong>Always disabled</strong>：Docker Offload 被禁用，用户无法启用它。该选项可见但被锁定。当 Docker Offload 未被批准用于组织使用时使用。</li>
<li><strong>User defined</strong>：无强制默认值。用户可以选择在他们的 Docker Desktop 设置中启用或禁用 Docker Offload。</li>
</ul>
</li>
<li>选择 <strong>Save</strong>。</li>
</ol>
<p>有关 Settings Management 的更多详细信息，请参阅 
    
  
  <a class="link" href="https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/settings-reference/#enable-docker-offload">设置参考</a>。</p>

      </div>
    
  </div>
</div>


## 监控您组织的产品使用情况

要查看 Docker 产品的使用情况：

- Docker Desktop：在 [Docker Home](https://app.docker.com/) 中查看 **Insights** 页面。有关更多详细信息，请参阅 [Insights](./insights.md)。
- Docker Hub：在 Docker Hub 中查看 [**Usage** 页面](https://hub.docker.com/usage)。
- Docker Build Cloud：在 [Docker Build Cloud](http://app.docker.com/build) 中查看 **Build minutes** 页面。
- Docker Scout：在 Docker Scout 中查看 [**Repository settings** 页面](https://scout.docker.com/settings/repos)。
- Testcontainers Cloud：在 Testcontainers Cloud 中查看 [**Billing** 页面](https://app.testcontainers.cloud/dashboard/billing)。
- Docker Offload：在 [Docker Home](https://app.docker.com/) 中查看 **Offload** > **Offload overview** 页面。有关更多详细信息，请参阅 [Docker Offload 使用和计费](/offload/usage/)。

如果您的使用量或席位数量超过订阅额度，您可以 [扩展您的订阅](../../subscription/scale.md) 以满足您的需求。
