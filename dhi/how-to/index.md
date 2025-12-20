# 操作指南

本节提供使用 Docker Hardened Images (DHIs) 的实用、基于任务的指导。无论您是首次评估 DHIs 还是将其集成到生产 CI/CD 流水线中，这些主题涵盖了从发现到调试的整个采用过程中的关键任务。

这些主题围绕使用 DHIs 的典型生命周期组织，但您可以根据特定的工作流按需使用它们。

探索下面符合您当前需求的主题。

## 发现

探索 DHI 目录中可用的镜像和元数据。


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/how-to/explore/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q137 0 241.5 80T863-595q4 13-2 24.5t-18.88 14.77Q830-553 820-560.5q-10-7.5-14-19.5-22-74-74-131.5T607-799v18q0 35-24 61t-59 26h-87v87q0 16.58-13.5 27.79T393-568h-83v88h80q12.75 0 21.38 8.62Q420-462.75 420-450v95h-67L149-559q-5 20-7 39.67-2 19.66-2 39.33 0 128.02 82.5 223.51Q305-161 431-144q11.68 1.68 19.34 11.34T458-110.5q0 12.5-9.14 20.5T427-84q-148-20-247.5-131.5T80-480Zm749 351L716-241q-21 15-45.5 23t-50.07 8q-71.01 0-120.72-49.62Q450-309.24 450-380.12t49.62-120.38q49.62-49.5 120.5-49.5t120.38 49.71Q790-450.58 790-379.57q0 25.57-8.5 50.07T759-283l112 112q9 9 9.5 21t-8.5 21q-9 9-21.5 9t-21.5-9ZM619.86-270Q666-270 698-301.86t32-78Q730-426 698.14-458t-78-32Q574-490 542-458.14t-32 78Q510-334 541.86-302t78 32Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">探索 Docker Hardened Images</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何在 Docker Hub 上的 DHI 目录中查找和评估镜像仓库、变体、元数据和认证。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 采用

同步受信任的镜像，根据需要进行自定义，并将其集成到您的工作流中。


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/how-to/mirror/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M396-323H110q-13 0-21.5-8.5T80-353q0-13 8.5-21.5T110-383h286L296-483q-9-9-9-21t9-21q9-9 21-9t21 9l151 151q5 5 7 10t2 11q0 6-2 11t-7 10L338-181q-9 9-21 9t-21-9q-9-9-9-21t9-21l100-100Zm168-254 100 100q9 9 9 21t-9 21q-9 9-21 9t-21-9L471-586q-5-5-7-10t-2-11q0-6 2-11t7-10l151-151q9-9 21-9t21 9q9 9 9 21t-9 21L564-637h286q13 0 21.5 8.5T880-607q0 13-8.5 21.5T850-577H564Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">镜像 Docker Hardened Image 仓库</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何将镜像同步到组织的命名空间，并可选择将其推送到另一个私有仓库。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/how-to/customize/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M421-80q-14 0-25-9t-13-23l-15-94q-19-7-40-19t-37-25l-86 40q-14 6-28 1.5T155-226L97-330q-8-13-4.5-27t15.5-23l80-59q-2-9-2.5-20.5T185-480q0-9 .5-20.5T188-521l-80-59q-12-9-15.5-23t4.5-27l58-104q8-13 22-17.5t28 1.5l86 40q16-13 37-25t40-18l15-95q2-14 13-23t25-9h118q14 0 25 9t13 23l15 94q19 7 40.5 18.5T669-710l86-40q14-6 27.5-1.5T804-734l59 104q8 13 4.5 27.5T852-580l-80 57q2 10 2.5 21.5t.5 21.5q0 10-.5 21t-2.5 21l80 58q12 8 15.5 22.5T863-330l-58 104q-8 13-22 17.5t-28-1.5l-86-40q-16 13-36.5 25.5T592-206l-15 94q-2 14-13 23t-25 9H421Zm59-270q54 0 92-38t38-92q0-54-38-92t-92-38q-54 0-92 38t-38 92q0 54 38 92t92 38Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">自定义 Docker Hardened Image 或 chart</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何自定义 Docker Hardened Images 和 charts。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/how-to/use/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M320-258v-450q0-14 9-22t21-8q4 0 8 1t8 3l354 226q7 5 10.5 11t3.5 14q0 8-3.5 14T720-458L366-232q-4 2-8 3t-8 1q-12 0-21-8t-9-22Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">使用 Docker Hardened Image</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何在 Dockerfiles、CI 流水线和标准开发工作流中拉取、运行和引用 Docker Hardened Images。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/how-to/k8s/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M320-258v-450q0-14 9-22t21-8q4 0 8 1t8 3l354 226q7 5 10.5 11t3.5 14q0 8-3.5 14T720-458L366-232q-4 2-8 3t-8 1q-12 0-21-8t-9-22Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">在 Kubernetes 中使用 Docker Hardened Image</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何在 Kubernetes 部署中使用 Docker Hardened Images。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/how-to/helm/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M110-120q-12.75 0-21.37-8.63Q80-137.25 80-150v-420q0-12.75 8.63-21.38Q97.25-600 110-600h150q12.75 0 21.38 8.62Q290-582.75 290-570v420q0 12.75-8.62 21.37Q272.75-120 260-120H110Zm295 0q-12.75 0-21.37-8.63Q375-137.25 375-150v-660q0-12.75 8.63-21.38Q392.25-840 405-840h150q12.75 0 21.38 8.62Q585-822.75 585-810v660q0 12.75-8.62 21.37Q567.75-120 555-120H405Zm295 0q-12.75 0-21.37-8.63Q670-137.25 670-150v-340q0-12.75 8.63-21.38Q687.25-520 700-520h150q12.75 0 21.38 8.62Q880-502.75 880-490v340q0 12.75-8.62 21.37Q862.75-120 850-120H700Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">使用 Docker Hardened Image chart</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何使用 Docker Hardened Image chart。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/how-to/els/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M483-120q-75 0-141-28.5T226.5-226q-49.5-49-78-115T120-482q0-75 28.5-140t78-113.5Q276-784 342-812t141-28q80 0 151.5 35T758-709v-76q0-13 8.5-21.5T788-815q13 0 21.5 8.5T818-785v148q0 13-8.5 21.5T788-607H639q-13 0-21.5-8.5T609-637q0-13 8.5-21.5T639-667h75q-44-51-103.5-82T483-780q-125 0-214 85.5T180-485q0 127 88 216t215 89q117 0 201-78t95-193q2-13 10.5-21.5T810-481q13 0 21.5 9t7.5 21q-11 140-112.5 235.5T483-120Zm28-374 115 113q9 9 9 21.5t-9 21.5q-9 9-21 9t-21-9L460-460q-5-5-7-10.5t-2-11.5v-171q0-13 8.5-21.5T481-683q13 0 21.5 8.5T511-653v159Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">为 Docker Hardened Images 使用扩展生命周期支持</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何为 Docker Hardened Images 使用扩展生命周期支持。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/how-to/manage/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M150-200q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h660q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H150Zm0-167q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h660q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H150Zm0-166q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h660q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H150Zm0-167q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h660q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H150Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">管理 Docker Hardened Images 和 charts</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何在组织中管理已同步和自定义的 Docker Hardened Images。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 评估

与其他镜像进行比较，以了解安全改进。


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/how-to/compare/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M422-120H180q-24 0-42-18t-18-42v-600q0-24 18-42t42-18h242v-50q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v820q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63-12.82 0-21.32-8.63Q422-57.25 422-70v-50ZM180-222h242v-277L180-222Zm362 102v-375l238 273v-558H542v-60h238q24 0 42 18t18 42v600q0 24-18 42t-42 18H542Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">比较 Docker Hardened Images</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何比较 Docker Hardened Images 与其他容器镜像，以评估安全改进和差异。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 验证

检查签名、SBOM 和来源，并扫描漏洞。


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/how-to/verify/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">验证 Docker Hardened Image 或 chart</h3>
    </div>
    <div class="card-content">
      <p class="card-description">使用 Docker Scout 或 cosign 验证 Docker Hardened Images 和 charts 的签名认证，如 SBOM、来源和漏洞数据。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/how-to/scan/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-120q-65.37 0-121.18-31Q303-182 276-240h-86q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h62q-7-26-7-52.67V-406h-56q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h56q0-29 .5-57.5T254-580h-64q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h90q14-28 37-49t51-35l-57-56q-8-8-8-19.79 0-11.78 8.42-20.35 7.72-7.86 19.65-7.86t19.93 8l74 74q27.67-10 56.34-10Q510-756 538-746l74-74q8-8 19.79-8 11.78 0 20.35 8.42 7.86 7.72 7.86 19.65T652-780l-56 56q28 14 49.4 35.67Q666.8-666.67 683-640h88q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-65q9 28 8.5 56.67-.5 28.66-.5 57.33h57q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-57q0 27 .5 53.5T708-300h63q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-86q-26 59-82.45 89.5Q546.11-120 480-120Zm-50-200h100q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H430q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm0-173h100q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H430q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">扫描 Docker Hardened Images</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何使用 Docker Scout、Grype 或 Trivy 扫描 Docker Hardened Images 中的已知漏洞。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 治理

执行策略以保持安全性和合规性。


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/how-to/policies/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-83q-5.32 0-9.88-1-4.56-1-9.12-3-138-47-219.5-168.5T160-522.11V-718q0-19.26 10.88-34.66Q181.75-768.07 199-775l260-97q11-4 21-4t21 4l260 97q17.25 6.93 28.13 22.34Q800-737.26 800-718v196q0 64-17.79 125.56Q764.42-334.87 731-279L604-402q13-17 19-38t6-42q0-63-43.5-106.5T480-632q-62 0-105.5 43.5t-43.5 106q0 62.5 43.5 105.5T480-334q21.68 0 42.84-7 21.16-7 39.89-18L697-229q-42 52-88.5 86T499-87q-4.56 2-9.12 3T480-83Zm-.2-311q-36.8 0-62.8-25.5t-26-63q0-37.5 26.2-63.5 26.21-26 63-26 36.8 0 62.8 26t26 63.5q0 37.5-26.2 63-26.21 25.5-63 25.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">使用策略强制执行 Docker Hardened Image 使用</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何为 Docker Hardened Images 使用 Docker Scout 的镜像策略。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 故障排除

调试基于 DHIs 的容器，而无需修改镜像。


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/how-to/debug/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-160q-24 0-42-18t-18-42v-520q0-24 18-42t42-18h680q24 0 42 18t18 42v520q0 24-18 42t-42 18H140Zm0-60h680v-436H140v436Zm221-218-83-83q-9-9-8.5-21t9.5-21q9-9 21-9t21 9l104 104q9 9 9 21t-9 21L321-313q-9 9-21 9t-21-9q-9-9-9-21t9-21l82-83Zm159 150q-13 0-21.5-8.5T490-318q0-13 8.5-21.5T520-348h160q13 0 21.5 8.5T710-318q0 13-8.5 21.5T680-288H520Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">调试 Docker Hardened Image</h3>
    </div>
    <div class="card-content">
      <p class="card-description">使用 Docker Debug 检查基于加固镜像运行的容器，而无需修改镜像。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [探索 Docker 硬化镜像](https://docs.docker.com/dhi/how-to/explore/)

- [镜像 Docker Hardened Image 仓库 <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>](https://docs.docker.com/dhi/how-to/mirror/)

- [自定义 Docker 强化镜像或图表 <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>](https://docs.docker.com/dhi/how-to/customize/)

- [使用 Docker Hardened Image](https://docs.docker.com/dhi/how-to/use/)

- [在 Kubernetes 中使用 Docker Hardened 镜像](https://docs.docker.com/dhi/how-to/k8s/)

- [使用 Docker 加固镜像（DHI）Helm chart](https://docs.docker.com/dhi/how-to/helm/)

- [管理 Docker Hardened Images 和 charts <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>](https://docs.docker.com/dhi/how-to/manage/)

- [使用 Docker Hardened Images 的扩展生命周期支持 <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>](https://docs.docker.com/dhi/how-to/els/)

- [对比 Docker Hardened 镜像](https://docs.docker.com/dhi/how-to/compare/)

- [验证 Docker Hardened Image 或 chart](https://docs.docker.com/dhi/how-to/verify/)

- [扫描 Docker Hardened Images](https://docs.docker.com/dhi/how-to/scan/)

- [使用策略强制执行 Docker Hardened Image 用法](https://docs.docker.com/dhi/how-to/policies/)

- [调试 Docker Hardened Image 容器](https://docs.docker.com/dhi/how-to/debug/)

