# 迁移

本节提供将您的应用程序迁移到 Docker Hardened Images (DHI) 的指导。迁移到 DHI 可通过利用具有内置安全功能的强化基础镜像，增强容器化应用程序的安全状况。

## 迁移路径

选择最适合您需求的迁移方法：


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/migration/migrate-with-ai/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M147-376q-45 0-76-31.21T40-483q0-44.58 31.21-75.79Q102.42-590 147-590v-123q0-24 18-42t42-18h166q0-45 31.21-76T480-880q44.58 0 75.79 31.21Q587-817.58 587-773h166q24 0 42 18t18 42v123q45 0 76 31.21T920-483q0 44.58-31.21 75.79Q857.58-376 813-376v196q0 24-18 42t-42 18H207q-24 0-42-18t-18-42v-196Zm196.24-100q16.76 0 28.26-11.74 11.5-11.73 11.5-28.5 0-16.76-11.74-28.26-11.73-11.5-28.5-11.5-16.76 0-28.26 11.74-11.5 11.73-11.5 28.5 0 16.76 11.74 28.26 11.73 11.5 28.5 11.5Zm274 0q16.76 0 28.26-11.74 11.5-11.73 11.5-28.5 0-16.76-11.74-28.26-11.73-11.5-28.5-11.5-16.76 0-28.26 11.74-11.5 11.73-11.5 28.5 0 16.76 11.74 28.26 11.73 11.5 28.5 11.5ZM342-285h276q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H342q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">使用 Docker 的 AI 助手进行迁移</h3>
    </div>
    <div class="card-content">
      <p class="card-description">使用 Docker 的 AI 助手，在指导和建议下自动将您的 Dockerfile 迁移到 Docker Hardened Images。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/migration/migrate-from-doi/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m166-482 176 176q9 9 8.5 21t-9.5 21q-9 9-21.5 9t-21.5-9L101-461q-5-5-7-10t-2-11q0-6 2-11t7-10l200-200q9-9 21.5-9t21.5 9q9 9 9 21.5t-9 21.5L166-482Zm628 0L618-658q-9-9-8.5-21t9.5-21q9-9 21.5-9t21.5 9l197 197q5 5 7 10t2 11q0 6-2 11t-7 10L659-261q-9 9-21 8.5t-21-9.5q-9-9-9-21.5t9-21.5l177-177Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">从 Alpine 或 Debian 镜像迁移</h3>
    </div>
    <div class="card-content">
      <p class="card-description">从 Docker 官方镜像（基于 Alpine 或 Debian）迁移到 Docker Hardened Images 的手动迁移指南。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/migration/migrate-from-wolfi/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M290-607H110q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32Q97.25-667 110-667h180v-139l-59 59q-9 9-21 9t-21.39-9q-8.61-9-8.61-21t9-21l110-110q9-9 21-9t21 9l110 110q9 9 9 21t-8.61 21q-9.39 9-21.39 9t-21-9l-59-59v453h500q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H670v139l59-59q9-9 21-9t21.39 9q8.61 9 8.61 21t-9 21L661-61q-9 9-21 9t-21-9L509-171q-9-9-9-21t8.61-21q9.39-9 21.39-9t21 9l59 59v-139H350q-26 0-43-17t-17-43v-254Zm320 194v-194H410v-60h200q26 0 43 17t17 43v194h-60Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">从 Wolfi 迁移</h3>
    </div>
    <div class="card-content">
      <p class="card-description">从基于 Wolfi 的镜像过渡到 Docker Hardened Images 的手动迁移指南。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 资源


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/migration/checklist/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m222-299 158-158q9-9 21-8.5t21.39 9.5q8.61 9 8.61 21t-9 21L243-235q-9 9-21 9t-21-9L101-335q-9-9-9-21t9-21q9-9 21-8.5t21 8.5l79 78Zm0-320 158-158q9-9 21-8.5t21.39 9.5q8.61 9 8.61 21t-9 21L243-555q-9 9-21 9t-21-9L101-655q-9-9-9-21t9-21q9-9 21-8.5t21 8.5l79 78Zm328 329q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h300q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H550Zm0-320q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h300q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H550Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">迁移检查清单</h3>
    </div>
    <div class="card-content">
      <p class="card-description">全面的迁移注意事项清单，确保成功过渡到 Docker Hardened Images。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/migration/examples/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M180-120q-24.75 0-42.37-17.63Q120-155.25 120-180v-600q0-24.75 17.63-42.38Q155.25-840 180-840h600q24.75 0 42.38 17.62Q840-804.75 840-780v600q0 24.75-17.62 42.37Q804.75-120 780-120H180Zm0-60h600v-520H180v520Zm300.04-105Q400-285 337-328.15q-63-43.15-92-112Q274-509 336.96-552q62.96-43 143-43Q560-595 623-551.85q63 43.15 92 112Q686-371 623.04-328q-62.96 43-143 43Zm-.16-105q-20.88 0-35.38-14.62-14.5-14.62-14.5-35.5 0-20.88 14.62-35.38 14.62-14.5 35.5-14.5 20.88 0 35.38 14.62 14.5 14.62 14.5 35.5 0 20.88-14.62 35.38-14.62 14.5-35.5 14.5Zm.12 30q33.6 0 56.8-23.2Q560-406.4 560-440q0-33.6-23.2-56.8Q513.6-520 480-520q-33.6 0-56.8 23.2Q400-473.6 400-440q0 33.6 23.2 56.8Q446.4-360 480-360Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">示例</h3>
    </div>
    <div class="card-content">
      <p class="card-description">针对不同编程语言和框架的 Dockerfile 迁移示例，为您的迁移过程提供指导。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [迁移清单](/dhi/migration/checklist/)

- [使用 Docker 的 AI 助手进行迁移](/dhi/migration/migrate-with-ai/)

- [从 Alpine 或 Debian 迁移](/dhi/migration/migrate-from-doi/)

- [从 Wolfi 迁移](/dhi/migration/migrate-from-wolfi/)

- [迁移示例](/dhi/migration/examples/)

