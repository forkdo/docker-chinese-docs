# Docker Hub

Docker Hub 简化了开发流程，它拥有世界上最大的容器注册表，用于存储、管理和共享 Docker 镜像。通过与您的工具无缝集成，它提高了生产力，并确保容器化应用程序的可靠部署、分发和访问。它还为开发者提供预构建镜像和资源，以加速开发工作流。

Docker Hub 的主要功能：

* 无限制的公共仓库
* 私有仓库
* Webhook 以自动化工作流
* GitHub 和 Bitbucket 集成
* 并发和自动化构建
* 可信内容，提供高质量、安全的镜像

除了图形界面外，您还可以使用 [Docker Hub API](../../reference/api/hub/latest.md) 或实验性的 [Docker Hub CLI 工具](https://github.com/docker/hub-tool#readme) 与 Docker Hub 交互。


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/docker-hub/quickstart" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-440q-17 0-28.5-11.5T440-480q0-17 11.5-28.5T480-520q17 0 28.5 11.5T520-480q0 17-11.5 28.5T480-440Zm0 360q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Zm0-60q142 0 241-99.5T820-480q0-142-99-241t-241-99q-141 0-240.5 99T140-480q0 141 99.5 240.5T480-140Zm0 0q-141 0-240.5-99.5T140-480q0-142 99.5-241T480-820q142 0 241 99t99 241q0 141-99 240.5T480-140Zm64-261q5-2 8.5-5.5t5.5-8.5l118-241q5-10-2.5-17.5T656-676L415-558q-5 2-8.5 5.5T401-544L283-303q-5 10 2.5 17.5T303-283l241-118Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Quickstart</h3>
    </div>
    <div class="card-content">
      <p class="card-description">获取在 Docker Hub 上开始使用的分步说明。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/docker-hub/image-library/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M220-80q-24 0-42-18t-18-42v-680q0-24 18-42t42-18h520q24 0 42 18t18 42v680q0 24-18 42t-42 18H220Zm266-740v241q0 8 7 12.5t15 .5l60-35q7-4 14.5-4t15.5 4l59 35q8 4 15.5-.5T680-579v-241H486Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Library</h3>
    </div>
    <div class="card-content">
      <p class="card-description">浏览内容库，其中包含数百万个操作系统、框架、数据库等镜像。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/docker-hub/repos" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M180-120q-24 0-42-18t-18-42v-600q0-24 18-42t42-18h600q24 0 42 18t18 42v600q0 24-18 42t-42 18H180Zm300-173q35 0 64-18t47-48q6-11 18-14t24-3h147v-404H180v404h147q12 0 24 3t18 14q18 30 47 48t64 18Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Repositories</h3>
    </div>
    <div class="card-content">
      <p class="card-description">创建仓库，与您的团队、客户或 Docker 社区共享您的镜像。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/admin/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M195-793h572q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H195q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5Zm5 627q-12.75 0-21.37-8.63Q170-183.25 170-196v-215h-25q-14.14 0-23.07-11T116-447l44-202q2-11 10.25-17.5T189-673h583q10.5 0 18.75 6.5T801-649l44 202q3 14-5.93 25T816-411h-25v215q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-215H552v215q0 12.75-8.62 21.37Q534.75-166 522-166H200Zm30-60h262v-185H230v185Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Organizations</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解组织管理。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/docker-hub/usage/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M110-120q-12.75 0-21.37-8.63Q80-137.25 80-150v-420q0-12.75 8.63-21.38Q97.25-600 110-600h150q12.75 0 21.38 8.62Q290-582.75 290-570v420q0 12.75-8.62 21.37Q272.75-120 260-120H110Zm295 0q-12.75 0-21.37-8.63Q375-137.25 375-150v-660q0-12.75 8.63-21.38Q392.25-840 405-840h150q12.75 0 21.38 8.62Q585-822.75 585-810v660q0 12.75-8.62 21.37Q567.75-120 555-120H405Zm295 0q-12.75 0-21.37-8.63Q670-137.25 670-150v-340q0-12.75 8.63-21.38Q687.25-520 700-520h150q12.75 0 21.38 8.62Q880-502.75 880-490v340q0 12.75-8.62 21.37Q862.75-120 850-120H700Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Usage and limits</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索使用限制以及如何更好地利用 Docker Hub。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/docker-hub/release-notes" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M220-80q-24 0-42-18t-18-42v-680q0-24 18-42t42-18h336q12.44 0 23.72 5T599-862l183 183q8 8 13 19.28 5 11.28 5 23.72v496q0 24-18 42t-42 18H220Zm331-584q0 12.75 8.63 21.37Q568.25-634 581-634h159L551-820v156ZM450-363v99q0 12.75 8.68 21.37 8.67 8.63 21.5 8.63 12.82 0 21.32-8.63 8.5-8.62 8.5-21.37v-99h100q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H510v-100q0-12.75-8.68-21.38-8.67-8.62-21.5-8.62-12.82 0-21.32 8.62-8.5 8.63-8.5 21.38v100H350q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5h100Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Release notes</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解新功能、改进和错误修复。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [Docker Hub 快速入门](/docker-hub/quickstart/)

- [仓库](/docker-hub/repos/)

- [内容库](/docker-hub/image-library/)

- [Docker Hub 使用情况和限制](/docker-hub/usage/)

- [服务账户](/docker-hub/service-accounts/)

- [排查 Docker Hub 问题](/docker-hub/troubleshoot/)

- [Docker Hub 发布说明](/docker-hub/release-notes/)

