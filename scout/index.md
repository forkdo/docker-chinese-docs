# Docker Scout

容器镜像由层（layers）和软件包组成，这些都可能存在漏洞。
这些漏洞可能会危及容器和应用程序的安全性。

Docker Scout 是一种主动增强软件供应链安全性的解决方案。
通过分析您的镜像，Docker Scout 会生成一个组件清单，也称为软件物料清单（SBOM）。
该 SBOM 会与一个持续更新的漏洞数据库进行比对，以识别安全弱点。

Docker Scout 是一个独立的服务和平台，您可以通过 Docker Desktop、Docker Hub、Docker CLI 和 Docker Scout Dashboard 与其交互。
Docker Scout 还支持与第三方系统（如容器注册表和 CI 平台）集成。


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/scout/quickstart/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-440q-17 0-28.5-11.5T440-480q0-17 11.5-28.5T480-520q17 0 28.5 11.5T520-480q0 17-11.5 28.5T480-440Zm0 360q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Zm0-60q142 0 241-99.5T820-480q0-142-99-241t-241-99q-141 0-240.5 99T140-480q0 141 99.5 240.5T480-140Zm0 0q-141 0-240.5-99.5T140-480q0-142 99.5-241T480-820q142 0 241 99t99 241q0 141-99 240.5T480-140Zm64-261q5-2 8.5-5.5t5.5-8.5l118-241q5-10-2.5-17.5T656-676L415-558q-5 2-8.5 5.5T401-544L283-303q-5 10 2.5 17.5T303-283l241-118Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">快速入门</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Scout 的功能以及如何使用。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/scout/image-analysis/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-80q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-60q63 0 118.5-20.5T699-219l-72-71q-31 23-68 36.5T480-240q-100 0-170-70t-70-170q0-100 70-170t170-70q100 0 170 70t70 170q0 42-13.5 79T670-333l71 71q37-45 58-100t21-118q0-142-99-241t-241-99q-142 0-241 99t-99 241q0 142 99 241t241 99Zm0-160q29 0 55.5-8.5T584-333l-74-73q-7 3-14.5 4.5T480-400q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 8-2 16t-5 16l74 72q16-22 24.5-48.5T660-480q0-75-52.5-127.5T480-660q-75 0-127.5 52.5T300-480q0 75 52.5 127.5T480-300Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">镜像分析</h3>
    </div>
    <div class="card-content">
      <p class="card-description">揭示并深入探究镜像的组成。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/scout/advisory-db-sources/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-520q161 0 260.5-49T840-680q0-63-99.5-111.5T480-840q-161 0-260.5 48.5T120-680q0 62 99.5 111T480-520Zm0 100q50 0 112-8.5T709.5-455q55.5-18 93-46.5T840-570v100q0 40-37.5 68.5t-93 46.5Q654-337 592-328.5T480-320q-49 0-111.5-8.5t-118-27q-55.5-18.5-93-47T120-470v-100q0 39 37.5 67.5t93 47q55.5 18.5 118 27T480-420Zm0 200q50 0 112-8.5T709.5-255q55.5-18 93-46.5T840-370v100q0 40-37.5 68.5t-93 46.5Q654-137 592-128.5T480-120q-49 0-111.5-8.5t-118-27q-55.5-18.5-93-47T120-270v-100q0 39 37.5 67.5t93 47q55.5 18.5 118 27T480-220Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">建议数据库</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Scout 使用的信息来源。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/scout/integrations/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m234-292 69 69q9 9 9 21t-9 21q-9 9-21 9t-21-9L141-301q-5-5-7-10t-2-11q0-6 2-11t7-10l120-120q9-9 21-9t21 9q9 9 9 21t-9 21l-69 69h256q13 0 21.5 8.5T520-322q0 13-8.5 21.5T490-292H234Zm376 0q-12 0-21-9t-9-21q0-13 9-21.5t21-8.5q13 0 21.5 8.5T640-322q0 12-8.5 21t-21.5 9Zm120 0q-12 0-21-9t-9-21q0-13 9-21.5t21-8.5q13 0 21.5 8.5T760-322q0 12-8.5 21t-21.5 9Zm-4-316H470q-13 0-21.5-8.5T440-638q0-13 8.5-21.5T470-668h256l-69-69q-9-9-9-21t9-21q9-9 21-9t21 9l120 120q5 5 7 10t2 11q0 6-2 11t-7 10L699-497q-9 9-21 9t-21-9q-9-9-9-21t9-21l69-69Zm-496 0q-12 0-21-9t-9-21q0-13 9-21.5t21-8.5q13 0 21.5 8.5T260-638q0 12-8.5 21t-21.5 9Zm120 0q-12 0-21-9t-9-21q0-13 9-21.5t21-8.5q13 0 21.5 8.5T380-638q0 12-8.5 21t-21.5 9Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">集成</h3>
    </div>
    <div class="card-content">
      <p class="card-description">将 Docker Scout 与您的 CI、注册表和其他第三方服务连接。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/scout/dashboard/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M540-570q-12.75 0-21.37-8.63Q510-587.25 510-600v-210q0-12.75 8.63-21.38Q527.25-840 540-840h270q12.75 0 21.38 8.62Q840-822.75 840-810v210q0 12.75-8.62 21.37Q822.75-570 810-570H540ZM150-450q-12.75 0-21.37-8.63Q120-467.25 120-480v-330q0-12.75 8.63-21.38Q137.25-840 150-840h270q12.75 0 21.38 8.62Q450-822.75 450-810v330q0 12.75-8.62 21.37Q432.75-450 420-450H150Zm390 330q-12.75 0-21.37-8.63Q510-137.25 510-150v-330q0-12.75 8.63-21.38Q527.25-510 540-510h270q12.75 0 21.38 8.62Q840-492.75 840-480v330q0 12.75-8.62 21.37Q822.75-120 810-120H540Zm-390 0q-12.75 0-21.37-8.63Q120-137.25 120-150v-210q0-12.75 8.63-21.38Q137.25-390 150-390h270q12.75 0 21.38 8.62Q450-372.75 450-360v210q0 12.75-8.62 21.37Q432.75-120 420-120H150Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">仪表板</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Docker Scout 的 Web 界面。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/scout/policy/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-83q-5.32 0-9.88-1-4.56-1-9.12-3-138-47-219.5-168.5T160-522.11V-718q0-19.26 10.88-34.66Q181.75-768.07 199-775l260-97q11-4 21-4t21 4l260 97q17.25 6.93 28.13 22.34Q800-737.26 800-718v196q0 64-17.79 125.56Q764.42-334.87 731-279L604-402q13-17 19-38t6-42q0-63-43.5-106.5T480-632q-62 0-105.5 43.5t-43.5 106q0 62.5 43.5 105.5T480-334q21.68 0 42.84-7 21.16-7 39.89-18L697-229q-42 52-88.5 86T499-87q-4.56 2-9.12 3T480-83Zm-.2-311q-36.8 0-62.8-25.5t-26-63q0-37.5 26.2-63.5 26.21-26 63-26 36.8 0 62.8 26t26 63.5q0 37.5-26.2 63-26.21 25.5-63 25.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">策略</h3>
    </div>
    <div class="card-content">
      <p class="card-description">确保您的制品符合供应链最佳实践。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/subscription/change/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M310-160q-13 0-21.5-8.5T280-190q0-13 8.5-21.5T310-220h340q13 0 21.5 8.5T680-190q0 13-8.5 21.5T650-160H310Zm170-170q-13 0-21.5-8.5T450-360v-326L350-586q-9 9-21 9t-21-9q-9-9-9-21t9-21l151-151q5-5 10-7t11-2q6 0 11 2t10 7l151 151q9 9 9 21t-9 21q-9 9-21 9t-21-9L510-686v326q0 13-8.5 21.5T480-330Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">升级</h3>
    </div>
    <div class="card-content">
      <p class="card-description">个人订阅最多包含 1 个仓库。升级以获得更多。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [安装 Docker Scout](/scout/install/)

- [Docker Scout 快速入门](/scout/quickstart/)

- [Docker Scout 中的策略评估入门](/scout/policy/)

- [将 Docker Scout 与其他系统集成](/scout/integrations/)

