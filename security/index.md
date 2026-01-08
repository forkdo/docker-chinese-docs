# 开发者安全

Docker 通过其开发者级别的安全功能，帮助您保护本地环境、基础设施和网络。

使用双因素认证 (2FA)、个人访问令牌和 Docker Scout 等工具来管理工作访问，并在工作流早期检测漏洞。您还可以使用 Docker Compose 安全地集成密钥到您的开发栈中，或者使用 Docker Hardened Images 增强软件供应链安全。

请浏览以下章节以了解更多信息。

## 面向开发者


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/security/2fa/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M634-320q-14 0-24-10t-10-24v-132q0-14 10-24t24-10h6v-40q0-33 23.5-56.5T720-640q33 0 56.5 23.5T800-560v40h6q14 0 24 10t10 24v132q0 14-10 24t-24 10H634Zm46-200h80v-40q0-17-11.5-28.5T720-600q-17 0-28.5 10.92Q680-578.15 680-562v42ZM260-40q-24.75 0-42.37-17.63Q200-75.25 200-100v-760q0-24.75 17.63-42.38Q235.25-920 260-920h440q24.75 0 42.38 17.62Q760-884.75 760-860v116q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-26H260v580h440v-26q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v116q0 24.75-17.62 42.37Q724.75-40 700-40H260Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">设置双因素认证</h3>
    </div>
    <div class="card-content">
      <p class="card-description">为您的 Docker 账户添加额外的身份验证层。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/security/access-tokens/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M111-261h739q13 0 21.5 8.5T880-231q0 13-9 22t-22 9H110q-13 0-21.5-9T80-231q0-13 9-21.5t22-8.5Zm45-260-27 48q-5 8-13.5 10.5T99-465q-8-5-11-14t2-17l28-48H62q-9 0-15.5-7T40-567q0-9 7-15.5t16-6.5h55l-28-48q-5-8-2.5-17T98-668q8-5 17-2t14 11l27 47 27-48q5-8 13.5-10.5T213-668q8 5 11 14t-2 17l-28 48h56q9 0 15.5 6.5T272-567q0 9-6.5 16t-15.5 7h-56l28 48q5 8 2.5 17T214-465q-8 5-17 2t-14-11l-27-47Zm324 0-26 47q-5 8-14.5 10.5T422-466q-8-5-10.5-14.5T414-498l28-48h-56q-9 0-15.5-7t-6.5-16q0-9 7-15.5t16-6.5h55l-28-48q-5-8-2.5-17t10.5-14q8-5 17-2t14 11l27 47 27-48q5-8 13.5-10.5T537-670q8 5 11 14t-2 17l-28 48h56q9 0 15.5 6.5T596-569q0 9-6.5 16t-15.5 7h-56l29 48q5 8 2 17.5T538-466q-8 5-17.5 2T506-475l-26-46Zm324 0-26 47q-5 8-14.5 10.5T746-466q-8-5-10.5-14.5T738-498l28-48h-56q-9 0-15.5-7t-6.5-16q0-9 7-15.5t16-6.5h55l-28-48q-5-8-2.5-17t10.5-14q8-5 17-2t14 11l27 47 27-48q5-8 13.5-10.5T861-670q8 5 11 14t-2 17l-28 48h56q9 0 15.5 6.5T920-569q0 9-6.5 16t-15.5 7h-56l29 48q5 8 2 17.5T862-466q-8 5-17.5 2T830-475l-26-46Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">管理访问令牌</h3>
    </div>
    <div class="card-content">
      <p class="card-description">创建个人访问令牌作为密码的替代方案。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/docker-hub/repos/manage/vulnerability-scanning/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M180-120q-24 0-42-18t-18-42v-600q0-24 18-42t42-18h183q13 0 21.5 8.5T393-810q0 13-8.5 21.5T363-780H180v600h600v-211q0-13 8.5-21.5T810-421q13 0 21.5 8.5T840-391v211q0 24-18 42t-42 18H180Zm267-182 118-154q5-6 12-6t12 6l117 155q5 8 1 16t-13 8H268q-9 0-13.5-8t1.5-16l86-111q5-6 12-6t12 6l81 110Zm205-246q-70 0-118-48t-48-118q0-70 48-118t118-48q70 0 118 48t48 118q0 28-8 53t-22 46l109 109q9 9 9 21t-9 21q-9 9-21.5 9t-21.5-9L742-575q-21 14-41.5 20.5T652-548Zm0-60q46 0 76-30t30-76q0-46-30-76t-76-30q-46 0-76 30t-30 76q0 46 30 76t76 30Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">静态漏洞扫描</h3>
    </div>
    <div class="card-content">
      <p class="card-description">对您的 Docker 镜像自动执行一次性漏洞扫描。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/engine/security/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-142q106-35 175.5-128.5T737-480H480v-335l-260 97v196q0 12 .5 20.5T223-480h257v338Zm0 58q-5 0-9.5-1t-9.5-3q-139-47-220-168.5T160-523v-196q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v196q0 145-81 266.5T499-88q-5 2-9.5 3t-9.5 1Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Docker Engine 安全</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何保持 Docker Engine 的安全性。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/compose/how-tos/use-secrets/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480.18-284q12.82 0 21.32-8.63 8.5-8.62 8.5-21.37v-197q0-12.75-8.68-21.38-8.67-8.62-21.5-8.62-12.82 0-21.32 8.62-8.5 8.63-8.5 21.38v197q0 12.75 8.68 21.37 8.67 8.63 21.5 8.63ZM480-607q14.45 0 24.23-9.78Q514-626.55 514-641t-9.77-24.22Q494.45-675 480-675q-14.45 0-24.23 9.78Q446-655.45 446-641t9.77 24.22Q465.55-607 480-607Zm0 523q-5.32 0-9.88-1-4.56-1-9.12-3-139-47-220-168.5t-81-266.61V-719q0-19.26 10.88-34.66Q181.75-769.07 199-776l260-97q11-4 21-4t21 4l260 97q17.25 6.93 28.13 22.34Q800-738.26 800-719v195.89Q800-378 719-256.5T499-88q-4.56 2-9.12 3T480-84Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Docker Compose 中的密钥</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何在 Docker Compose 中使用密钥。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 更多资源


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/faq/security/general/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M484.03-247Q500-247 511-258.03q11-11.03 11-27T510.97-312q-11.03-11-27-11T457-311.97q-11 11.03-11 27T457.03-258q11.03 11 27 11Zm-3.76 167q-82.74 0-155.5-31.5Q252-143 197.5-197.5t-86-127.34Q80-397.68 80-480.5t31.5-155.66Q143-709 197.5-763t127.34-85.5Q397.68-880 480.5-880t155.66 31.5Q709-817 763-763t85.5 127Q880-563 880-480.27q0 82.74-31.5 155.5Q817-252 763-197.68q-54 54.31-127 86Q563-80 480.27-80Zm2.5-580Q513-660 536-641.5q23 18.5 23 47.2 0 26.3-15.65 45.73Q527.7-529.14 508-512q-23 19-40 42.38-17 23.39-17 52.62 0 11 8.4 17.5T479-393q12 0 19.88-8 7.87-8 10.12-20 3-21 16-38t30.23-30.78Q580-510 596-537q16-27 16-58.61 0-50.39-37.5-83.89T485.55-713Q450-713 417-698t-54 44q-7 10-6.5 21.5t9.47 18.5q11.41 8 23.65 5 12.23-3 20.38-14 12.75-17.9 31.88-27.45Q461-660 482.77-660Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">安全常见问题</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索常见的安全问题解答。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/develop/security-best-practices/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m289-572 167-267q5-7 11-10.5t14-3.5q8 0 14 3.5t11 10.5l167 267q5 8 4.5 16t-4.5 15q-4 7-10.6 11t-15.4 4H315q-8.91 0-15.6-4.13-6.69-4.12-10.4-10.87-4-7-4.5-15t4.5-16ZM706-80q-72.5 0-123.25-50.75T532-254q0-72.5 50.75-123.25T706-428q72.5 0 123.25 50.75T880-254q0 72.5-50.75 123.25T706-80Zm-586-55v-244q0-12.75 8.63-21.38Q137.25-409 150-409h244q12.75 0 21.38 8.62Q424-391.75 424-379v244q0 12.75-8.62 21.37Q406.75-105 394-105H150q-12.75 0-21.37-8.63Q120-122.25 120-135Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">安全最佳实践</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解您可以采取的提升容器安全性的步骤。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/scout/guides/vex/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M63.06-268.41q-10.15-6.88-12.11-18.74Q49-299 55-309l151-241q8-13 23.5-14t25.5 10l93 109 135-218q8-14 24.5-14.5T533-664l60 89q8 12 5 23.5T585-534q-10 6-21.81 4.87Q551.38-530.25 543-543l-33-50-131 214q-8 13-23.5 14T330-375l-94-110-130 208q-7 11-19.5 14t-23.44-5.41ZM647-143q-70.83 0-120.42-49.62Q477-242.24 477-313.12t49.62-120.38q49.62-49.5 120.5-49.5t120.38 49.58Q817-383.83 817-313q0 26-8.5 50.5T786-216l112 112q9.23 9 9.62 21 .38 12-8.67 21-9.06 9-21.5 9Q865-53 856-62L743-174q-21 15-45.5 23t-50.5 8Zm-.14-60Q693-203 725-234.86t32-78Q757-359 725.14-391t-78-32Q601-423 569-391.14t-32 78Q537-267 568.86-235t78 32ZM690-539q-10-6-13.5-17.5T681-581l173-272q7-11 19.5-13.5t23.53 5.91q10.24 6.88 12.61 18.74Q912-830 905-820L732-548q-8 13-20 14t-22-5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">使用 VEX 抑制 CVE</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何抑制在镜像中发现的不适用或已修复的漏洞。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M678-250v73.64q0 7.36 5.14 11.86 5.15 4.5 12 4.5 6.86 0 11.36-5.1 4.5-5.1 4.5-11.9v-73h73.64q7.36 0 11.86-5.14 4.5-5.15 4.5-12 0-6.86-4.5-11.36-4.5-4.5-11.86-4.5H711v-73.64q0-7.36-4.5-11.86-4.5-4.5-11.36-4.5-6.85 0-12 4.5Q678-364 678-356.64V-283h-73.64q-7.36 0-11.86 4.5-4.5 4.5-4.5 11.36 0 6.85 5.1 12Q598.2-250 605-250h73Zm14.5 170Q615-80 560-135.5T505-267q0-78.43 54.99-133.72Q614.98-456 693-456q77 0 132.5 55.28Q881-345.43 881-267q0 76-55.5 131.5T692.5-80ZM160-522v-197q0-19.26 10.88-34.66Q181.75-769.07 199-776l260-97q11-4 21-4t21 4l260 97q17.25 6.93 28.13 22.34Q800-738.26 800-719v190q0 14-11.17 21.5T765-505q-17-5-35.5-8t-36.5-3q-102.74 0-175.37 72.92Q445-370.16 445-267q0 40 13.5 79t38.5 71q10 13 2.5 26T478-82q-69-20-122-51.5T251-237q-43-60.48-67-132.74Q160-442 160-522Zm319.91-118Q451-640 430-619.41q-21 20.59-21 49.5T429.86-520q20.85 21 50.14 21 14 0 26.5-5.5T529-520q10-10 15.5-23.04Q550-556.09 550-570q0-28.88-20.59-49.44T479.91-640Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Docker Hardened Images</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何使用 Docker Hardened Images 增强软件供应链安全。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [个人访问令牌](/security/access-tokens/)

- [为您的 Docker 账户启用双因素认证](/security/2fa/)

- [Docker 安全公告](/security/security-announcements/)

