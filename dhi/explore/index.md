# 探索 Docker Hardened Images

Docker Hardened Images (DHI) 是由 Docker 维护的最小化、安全且可直接用于生产的容器基础镜像和应用镜像。DHI 旨在减少漏洞并简化合规性，能够轻松集成到您现有的基于 Docker 的工作流中，几乎无需重新配置工具。

本节帮助您了解 Docker Hardened Images 是什么，它们如何构建和测试，有哪些可用的类型，以及 Docker 和您作为用户之间的责任如何分担。有关 DHI 功能和特性的完整列表，请参阅[功能](/dhi/features/)。

## 了解更多关于 Docker Hardened Images 的信息


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/explore/what/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M483.18-280q12.82 0 21.32-8.63 8.5-8.62 8.5-21.37v-180q0-12.75-8.68-21.38-8.67-8.62-21.5-8.62-12.82 0-21.32 8.62-8.5 8.63-8.5 21.38v180q0 12.75 8.68 21.37 8.67 8.63 21.5 8.63Zm-3.2-314q14.02 0 23.52-9.2T513-626q0-14.45-9.48-24.22-9.48-9.78-23.5-9.78t-23.52 9.78Q447-640.45 447-626q0 13.6 9.48 22.8 9.48 9.2 23.5 9.2Zm.29 514q-82.74 0-155.5-31.5Q252-143 197.5-197.5t-86-127.34Q80-397.68 80-480.5t31.5-155.66Q143-709 197.5-763t127.34-85.5Q397.68-880 480.5-880t155.66 31.5Q709-817 763-763t85.5 127Q880-563 880-480.27q0 82.74-31.5 155.5Q817-252 763-197.68q-54 54.31-127 86Q563-80 480.27-80Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">什么是加固镜像，为什么使用它们？</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解什么是加固镜像，Docker Hardened Images 如何构建，它们与典型的基础镜像和应用镜像的区别，以及为何应使用它们。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/explore/build-process/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M354-370q-97 0-165-67.5T121-602q0-20 3-37.5t11-36.5q3-8 9-12t13-6q7-2 14 0t13 8l113 113 92-86-118-118q-6-6-8-13t0-14q2-7 6-12.5t12-8.5q19-8 36-11.5t37-3.5q99 0 168.5 69.5T592-602q0 24-5 47t-13 46l221 221q27 26 26.5 63.5T793-161q-26 24-61.5 23.5T670-164L447-388q-23 8-46 13t-47 5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">构建流程</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker 如何通过自动化的、以安全为重点的流水线构建、测试和维护 Docker Hardened Images。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/explore/test/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M172-120q-41.78 0-59.39-39T124-230l248-280v-270h-52q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h320q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-52v270l248 280q29 32 11.39 71T788-120H172Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">镜像测试</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Hardened Images 如何自动测试标准合规性、功能性和安全性。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/explore/responsibility/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M38-254q0-35 18-63.5t50-42.5q73-32 131.5-46T358-420q62 0 120 14t131 46q32 14 50.5 42.5T678-254v34q0 25-17.5 42.5T618-160H98q-25 0-42.5-17.5T38-220v-34Zm686 94q5-15 9.5-29.5T738-220v-34q0-63-29-101.5T622-420q69 8 130 22t99 34q33 19 52 47t19 63v34q0 25-17.5 42.5T862-160H724ZM358-481q-66 0-108-42t-42-108q0-66 42-108t108-42q66 0 108 42t42 108q0 66-42 108t-108 42Zm360-150q0 66-42 108t-108 42q-11 0-24.5-1.5T519-488q24-25 36.5-61.5T568-631q0-45-12.5-79.5T519-774q11-3 24.5-5t24.5-2q66 0 108 42t42 108Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">责任概述</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解在使用 Docker Hardened Images 作为安全软件供应链的一部分时，Docker 和您作为用户各自的责任。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/explore/available/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M681-495q-24 0-42-18t-18-42v-145q0-24 18-42t42-18h99q24 0 42 18t18 42v145q0 24-18 42t-42 18h-99Zm-250 0q-24 0-42-18t-18-42v-145q0-24 18-42t42-18h99q24 0 42 18t18 42v145q0 24-18 42t-42 18h-99Zm-251 0q-24 0-42-18t-18-42v-145q0-24 18-42t42-18h99q24 0 42 18t18 42v145q0 24-18 42t-42 18h-99Zm0 295q-24 0-42-18t-18-42v-145q0-24 18-42t42-18h99q24 0 42 18t18 42v145q0 24-18 42t-42 18h-99Zm251 0q-24 0-42-18t-18-42v-145q0-24 18-42t42-18h99q24 0 42 18t18 42v145q0 24-18 42t-42 18h-99Zm250 0q-24 0-42-18t-18-42v-145q0-24 18-42t42-18h99q24 0 42 18t18 42v145q0 24-18 42t-42 18h-99Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">镜像类型</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Hardened Images 目录中提供的不同镜像类型、发行版和变体。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/explore/feedback" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-40q-112 0-216-66T100-257v107q0 13-8.5 21.5T70-120q-13 0-21.5-8.5T40-150v-180q0-13 8.5-21.5T70-360h180q13 0 21.5 8.5T280-330q0 13-8.5 21.5T250-300H143q51 77 145.5 138.5T480-100q150 0 258.5-101T859-449q1-13 9.5-22t21.5-9q12 0 21 8.5t8 20.5q-6 86-42.5 161T781-159.5Q722-104 644.5-72T480-40Zm0-820q-150 0-258.5 101T101-511q-1 13-9.5 22T70-480q-12 0-21-8.5T41-509q6-86 42.5-161T179-800.5Q238-856 315.5-888T480-920q112 0 216 66t164 151v-107q0-13 8.5-21.5T890-840q13 0 21.5 8.5T920-810v180q0 13-8.5 21.5T890-600H710q-13 0-21.5-8.5T680-630q0-13 8.5-21.5T710-660h107q-51-77-145-138.5T480-860Zm-3 614q16 0 27-11t11-27q0-16-11-27t-27-11q-16 0-27 11t-11 27q0 16 11 27t27 11Zm69-243q33-33 46-58.5t13-53.5q0-52-36-83.5T479-716q-41 0-73.5 16T353-652q-7 11-3 22.5t15 16.5q11 5 23 .5t20-14.5q14-15 32-23.5t39-8.5q29 0 49 16t20 44q0 20-11 38.5T500-517q-29 27-40.5 47.5T445-424q-2 12 7 21t21 9q12 0 20-8.5t11-20.5q4-18 14-33t28-33Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">提供反馈</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Docker 欢迎所有贡献和反馈。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [什么是加固镜像，为什么要使用它们？](/dhi/explore/what/)

- [Docker 强化镜像的构建方式](/dhi/explore/build-process/)

- [Docker Hardened Images 可用类型](/dhi/explore/available/)

- [Docker 强化镜像如何进行测试](/dhi/explore/test/)

- [了解 Docker Hardened Images 的角色和职责](/dhi/explore/responsibility/)

- [提供反馈](/dhi/explore/feedback/)

