# Docker Hardened Images

Docker Hardened Images (DHI) 是由 Docker 维护的精简、安全且可用于生产环境的容器基础镜像和应用程序镜像。旨在减少漏洞并简化合规性，DHI 可以轻松集成到您现有的基于 Docker 的工作流中，几乎无需重新调整工具。

DHI 提供两个版本：**DHI Free** 免费提供核心安全功能，而 **DHI Enterprise** 则为有高级需求的组织增加了 SLA 支持保障、合规性变体、定制化服务和延长生命周期支持。

![DHI Subscription](./images/dhi-subscription.png)

探索以下部分，以开始使用 Docker Hardened Images，将它们集成到您的工作流中，并了解是什么使其安全且企业就绪。


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/get-started/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M263-465q26-69 64.5-130.5T415-712l-77-15q-20-4-39.5 2T265-705L129-568q-11 11-8 26.5t17 21.5l125 55Zm580-398q-109-8-206.5 37.5T461-702q-50 50-88.5 106.5T309-473q-4 10-4 20t8 18l135 135q8 8 18 8t20-4q66-24 122.5-63T715-448q78-78 124-175.5T877-830q-1-6-3.5-11.5T866-852q-5-5-10.5-7.5T843-863ZM586-573q-20-20-20-49.5t20-49.5q20-20 49.5-20t49.5 20q20 20 20 49.5T685-573q-20 20-49.5 20T586-573ZM479-250l54 125q6 15 22 17.5t27-8.5l136-136q14-14 20-33.5t2-39.5l-14-77q-55 49-116.5 87.5T479-250Zm-317-68q35-35 85-35.5t85 34.5q35 35 35 85t-35 85q-48 48-113.5 57T87-74q9-66 18.5-131.5T162-318Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">快速入门</h3>
    </div>
    <div class="card-content">
      <p class="card-description">跟随分步指南来探索和运行 Docker Hardened Image。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/explore/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M483.18-280q12.82 0 21.32-8.63 8.5-8.62 8.5-21.37v-180q0-12.75-8.68-21.38-8.67-8.62-21.5-8.62-12.82 0-21.32 8.62-8.5 8.63-8.5 21.38v180q0 12.75 8.68 21.37 8.67 8.63 21.5 8.63Zm-3.2-314q14.02 0 23.52-9.2T513-626q0-14.45-9.48-24.22-9.48-9.78-23.5-9.78t-23.52 9.78Q447-640.45 447-626q0 13.6 9.48 22.8 9.48 9.2 23.5 9.2Zm.29 514q-82.74 0-155.5-31.5Q252-143 197.5-197.5t-86-127.34Q80-397.68 80-480.5t31.5-155.66Q143-709 197.5-763t127.34-85.5Q397.68-880 480.5-880t155.66 31.5Q709-817 763-763t85.5 127Q880-563 880-480.27q0 82.74-31.5 155.5Q817-252 763-197.68q-54 54.31-127 86Q563-80 480.27-80Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">探索</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解什么是 Docker Hardened Images、它们如何构建，以及它们与典型基础镜像的区别所在。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/features/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M220-80q-24.75 0-42.37-17.63Q160-115.25 160-140v-434q0-24.75 17.63-42.38Q195.25-634 220-634h70v-96q0-78.85 55.61-134.42Q401.21-920 480.11-920q78.89 0 134.39 55.58Q670-808.85 670-730v96h70q24.75 0 42.38 17.62Q800-598.75 800-574v434q0 24.75-17.62 42.37Q764.75-80 740-80H220Zm260.17-200q31.83 0 54.33-22.03T557-355q0-30-22.67-54.5t-54.5-24.5q-31.83 0-54.33 24.5t-22.5 55q0 30.5 22.67 52.5t54.5 22ZM350-634h260v-96q0-54.17-37.88-92.08-37.88-37.92-92-37.92T388-822.08q-38 37.91-38 92.08v96Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">功能特性</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索内置于 Docker Hardened Images 中的安全性、合规性及企业就绪特性。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/how-to/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M320-258v-450q0-14 9-22t21-8q4 0 8 1t8 3l354 226q7 5 10.5 11t3.5 14q0 8-3.5 14T720-458L366-232q-4 2-8 3t-8 1q-12 0-21-8t-9-22Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">操作指南</h3>
    </div>
    <div class="card-content">
      <p class="card-description">使用、验证、扫描和迁移到 Docker Hardened Images 的分步指南。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M132-120q-24 0-42-18t-18-42v-600q0-24 18-42t42-18h696q24 0 42 18t18 42v600q0 24-18 42t-42 18H132Zm228-160q17 0 28.5-11.5T400-320q0-17-11.5-28.5T360-360H240q-17 0-28.5 11.5T200-320q0 17 11.5 28.5T240-280h120Zm222-193-29-29q-12-12-28-11.5T497-501q-11 12-11.5 28t11.5 28l64 64q9 9 21 9t21-9l149-149q12-12 12-28t-12-28q-12-12-28.5-12T695-586L582-473Zm-222 33q17 0 28.5-11.5T400-480q0-17-11.5-28.5T360-520H240q-17 0-28.5 11.5T200-480q0 17 11.5 28.5T240-440h120Zm0-160q17 0 28.5-11.5T400-640q0-17-11.5-28.5T360-680H240q-17 0-28.5 11.5T200-640q0 17 11.5 28.5T240-600h120Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">核心概念</h3>
    </div>
    <div class="card-content">
      <p class="card-description">理解使 Docker Hardened Images 可用于生产环境的安全供应链原则。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/troubleshoot/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M477-246q16 0 27-11t11-27q0-16-11-27t-27-11q-16 0-27 11t-11 27q0 16 11 27t27 11Zm128-355q0-53-34-84t-92-31q-42 0-75.5 17.5T350-648q-6 9-1 19.5t16 15.5q11 5 21.5 1.5T405-624q14-17 32.5-26t41.5-9q32 0 50.5 16t18.5 44q0 20-11 38.5T500-517q-28 26-40 47t-15 48q-1 11 7.5 19.5T473-394q11 0 19.5-8t10.5-20q4-17 13.5-32t29.5-35q32-32 45.5-57.5T605-601ZM180-120q-24 0-42-18t-18-42v-600q0-24 18-42t42-18h600q24 0 42 18t18 42v600q0 24-18 42t-42 18H180Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">故障排除</h3>
    </div>
    <div class="card-content">
      <p class="card-description">解决构建、运行或调试 Docker Hardened Images 时的常见问题。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/resources/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M280-280q-83 0-141.5-58.5T80-480q0-83 58.5-141.5T280-680h140q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H280q-58.33 0-99.17 40.76-40.83 40.77-40.83 99Q140-422 180.83-381q40.84 41 99.17 41h140q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H280Zm75-170q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h250q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H355Zm185 170q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h140q58.33 0 99.17-40.76 40.83-40.77 40.83-99Q820-538 779.17-579q-40.84-41-99.17-41H540q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h140q83 0 141.5 58.5T880-480q0 83-58.5 141.5T680-280H540Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">其他资源</h3>
    </div>
    <div class="card-content">
      <p class="card-description">指向博客文章、Docker Hub 目录、GitHub 仓库等的链接。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [Docker Hardened Images 快速开始](/dhi/get-started/)

- [Docker Hardened Images 功能](/dhi/features/)

- [探索 Docker Hardened Images](/dhi/explore/)

- [迁移](/dhi/migration/)

- [操作指南](/dhi/how-to/)

- [核心概念](/dhi/core-concepts/)

- [故障排除](/dhi/troubleshoot/)

- [Docker Hardened Images 资源](/dhi/resources/)

