# 强化版 Docker Desktop





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Subscription:</span>
        
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



强化版 Docker Desktop 提供了一系列安全特性，旨在加强开发者环境的安全性，同时不影响生产力或开发者体验。

借助强化版 Docker Desktop，您可以强制执行严格的安全策略，防止开发者和容器绕过组织控制。您还可以增强容器隔离，以防范可能破坏 Docker Desktop Linux 虚拟机或底层主机系统的恶意载荷等安全威胁。

## 哪些人应该使用强化版 Docker Desktop？

强化版 Docker Desktop 非常适合注重安全性的组织机构，特别是那些：

- 不为开发者机器提供 root 或管理员权限
- 希望对 Docker Desktop 配置进行集中控制
- 必须满足特定合规性要求

## 强化版 Docker Desktop 的工作原理

强化版 Docker Desktop 的各项特性既可以独立工作，也可以协同工作，从而创建一种纵深防御的安全策略。它们保护开发者工作站免受多层面的攻击，包括 Docker Desktop 配置、容器镜像管理和容器运行时安全：

- 注册表访问管理和镜像访问管理可防止访问未经授权的容器注册表和镜像类型，从而减少暴露于恶意载荷的风险
- 增强型容器隔离在 Linux 用户命名空间中以非 root 权限运行容器，限制恶意容器的影响
- 气隙容器允许您为容器配置网络限制，防止恶意容器访问组织的内部网络资源
- 设置管理可以锁定 Docker Desktop 配置，以强制执行公司策略并防止开发者有意或无意地引入不安全的设置

## 后续步骤

探索强化版 Docker Desktop 的各项特性，了解它们如何加强组织的安全态势：


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/enterprise/security/hardened-desktop/settings-management/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-84q-5.32 0-9.88-1-4.56-1-9.12-3-139-47-220-167.55Q160-376.11 160-523v-196q0-19.26 10.88-34.66Q181.75-769.07 199-776l260-97q11-4 21-4t21 4l260 97q17.25 6.93 28.13 22.34Q800-738.26 800-719v215q0 13.81-9.5 23.41Q781-471 767-470q-37 2-67.5 13.5T640-418.04q-27 25.1-43 58.57T581-286v142q0 28-27.5 37T499-88q-4.56 2-9.12 3T480-84Zm195 4q-17.29 0-29.65-12.35Q633-104.71 633-122v-122q0-17.29 12.35-29.65Q657.71-286 675-286v-40q0-35.48 23.5-60.74Q722-412 757-412t58 25.26q23 25.26 23 60.74v40h1q16.88 0 28.94 12.35Q880-261.29 880-244v122q0 17.29-12.06 29.65Q855.88-80 839-80H675Zm40-206h84v-40q0-19-12.11-32.5-12.1-13.5-30-13.5Q739-372 727-358.5T715-326v40Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">设置管理</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解设置管理如何保护开发者的工作流程。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/enterprise/security/hardened-desktop/enhanced-container-isolation/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-142q106-35 175.5-128.5T737-480H480v-335l-260 97v196q0 12 .5 20.5T223-480h257v338Zm0 58q-5 0-9.5-1t-9.5-3q-139-47-220-168.5T160-523v-196q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v196q0 145-81 266.5T499-88q-5 2-9.5 3t-9.5 1Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">增强型容器隔离</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解增强型容器隔离如何防范容器攻击。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/enterprise/security/hardened-desktop/registry-access-management/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M251-120q-22 0-38.5-14T192-170l-66-395q-2-14 6.5-24.5T155-600h650q14 0 22.5 10.5T834-565l-66 395q-4 22-20.5 36T709-120H251Zm149-260h160q13 0 21.5-9t8.5-21q0-13-8.5-21.5T560-440H400q-12 0-21 8.5t-9 21.5q0 12 9 21t21 9ZM240-660q-12 0-21-9t-9-21q0-13 9-21.5t21-8.5h480q13 0 21.5 8.5T750-690q0 12-8.5 21t-21.5 9H240Zm80-120q-12 0-21-9t-9-21q0-13 9-21.5t21-8.5h320q13 0 21.5 8.5T670-810q0 12-8.5 21t-21.5 9H320Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">注册表访问管理</h3>
    </div>
    <div class="card-content">
      <p class="card-description">控制开发者在使用 Docker Desktop 时可以访问的注册表。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/enterprise/security/hardened-desktop/image-access-management/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M345-377h391L609-548 506-413l-68-87-93 123Zm-85 177q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h560q24 0 42 18t18 42v560q0 24-18 42t-42 18H260Zm0-60h560v-560H260v560ZM140-80q-24 0-42-18t-18-42v-620h60v620h620v60H140Zm120-740h560v560H260v-560Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">镜像访问管理</h3>
    </div>
    <div class="card-content">
      <p class="card-description">控制开发者可以从 Docker Hub 拉取的镜像。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/enterprise/security/hardened-desktop/air-gapped-containers/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M481-80q-84 0-157-31t-127.5-85Q142-250 111-323T80-480q0-84 31-157t84.5-127q53.5-54 125-85T473-880q35 0 72.5 5.5T610-861q11 3 17.5 13t6.5 21v47q0 34-26.5 60.5T547-693H433v80q0 19-13.5 32.5T387-567h-80v87h253q20 0 33.5 13.5T607-433v127h40q29 0 51.5 16t30.5 42q45-51 68-109.5T820-476v-18q0-10-1-21-1-13 7.5-22.5T848-547q12 0 21 8t10 20q1 9 1 19v19q0 84-31 157.5T764-196q-54 54-126.5 85T481-80Zm-48-55v-91q-33 0-56.5-23.5T353-306v-40L147-552q-4 23-5.5 37.5T140-483q0 134 83 232t210 116Zm291-472q-13 0-21.5-8.5T694-637v-146q0-13 8.5-21.5T724-813h16v-40q0-33 22.5-57t54.5-24q32 0 54.5 24t22.5 57v40h17q13 0 21.5 8.5T941-783v146q0 13-8.5 21.5T911-607H724Zm50-206h86v-40q0-19-12-33t-31-14q-19 0-31 14t-12 33v40Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">气隙容器</h3>
    </div>
    <div class="card-content">
      <p class="card-description">限制容器访问不需要的网络资源。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [Settings Management](/enterprise/security/hardened-desktop/settings-management/)

- [增强容器隔离](/enterprise/security/hardened-desktop/enhanced-container-isolation/)

- [注册表访问管理](/enterprise/security/hardened-desktop/registry-access-management/)

- [镜像访问管理](/enterprise/security/hardened-desktop/image-access-management/)

- [气隙容器](/enterprise/security/hardened-desktop/air-gapped-containers/)

