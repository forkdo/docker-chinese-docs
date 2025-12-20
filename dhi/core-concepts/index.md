# 核心概念

Docker Hardened Images（DHIs）建立在安全的软件供应链实践基础之上。本节解释了这些基础背后的核心概念，从签名认证和不可变摘要到 SLSA 和 VEX 等标准。

如果您想了解 Docker Hardened Images 如何支持合规性、透明性和安全性，请从这里开始。


## 安全元数据和认证


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/attestations/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M180-120q-24.75 0-42.37-17.63Q120-155.25 120-180v-600q0-24.75 17.63-42.38Q155.25-840 180-840h205q5-35 32-57.5t63-22.5q36 0 63 22.5t32 57.5h205q24.75 0 42.38 17.62Q840-804.75 840-780v600q0 24.75-17.62 42.37Q804.75-120 780-120H180Zm130-160h213q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H310q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm0-170h340q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H310q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm0-170h340q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H310q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm170-177q14 0 24.5-10.5T515-832q0-14-10.5-24.5T480-867q-14 0-24.5 10.5T445-832q0 14 10.5 24.5T480-797Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">认证（Attestations）</h3>
    </div>
    <div class="card-content">
      <p class="card-description">查看每个 Docker Hardened Image 附带的完整签名认证集合，例如 SBOM、VEX、构建来源和扫描结果。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/sbom/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-286q12 0 21-9t9-21q0-12-9-21t-21-9q-12 0-21 9t-9 21q0 12 9 21t21 9Zm0-164q12 0 21-9t9-21q0-12-9-21t-21-9q-12 0-21 9t-9 21q0 12 9 21t21 9Zm0-164q12 0 21-9t9-21q0-12-9-21t-21-9q-12 0-21 9t-9 21q0 12 9 21t21 9Zm162 328h184q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H462q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm0-164h184q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H462q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm0-164h184q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H462q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5ZM180-120q-24 0-42-18t-18-42v-600q0-24 18-42t42-18h600q24 0 42 18t18 42v600q0 24-18 42t-42 18H180Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">软件物料清单（SBOM）</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 SBOM 是什么、为何重要，以及 Docker Hardened Images 如何包含签名 SBOM 以支持透明性和合规性。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/slsa/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M132-120q-24 0-42-18t-18-42v-600q0-24 18-42t42-18h696q24 0 42 18t18 42v600q0 24-18 42t-42 18H132Zm228-160q17 0 28.5-11.5T400-320q0-17-11.5-28.5T360-360H240q-17 0-28.5 11.5T200-320q0 17 11.5 28.5T240-280h120Zm222-193-29-29q-12-12-28-11.5T497-501q-11 12-11.5 28t11.5 28l64 64q9 9 21 9t21-9l149-149q12-12 12-28t-12-28q-12-12-28.5-12T695-586L582-473Zm-222 33q17 0 28.5-11.5T400-480q0-17-11.5-28.5T360-520H240q-17 0-28.5 11.5T200-480q0 17 11.5 28.5T240-440h120Zm0-160q17 0 28.5-11.5T400-640q0-17-11.5-28.5T360-680H240q-17 0-28.5 11.5T200-640q0 17 11.5 28.5T240-600h120Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">软件制品供应链级别（SLSA）</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Hardened Images 如何符合 SLSA 构建级别 3，以及如何验证来源以实现安全、防篡改的构建。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/provenance/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-80q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q13 0 21.5 8.5T510-850v296q22 9 36 29t14 45q0 33-23.5 56.5T480-400q-33 0-56.5-23.5T400-480q0-25 14-45t36-29v-104q-65 11-107.5 60.5T300-480q0 75 52.5 127.5T480-300q75 0 127.5-52.5T660-480q0-32-10.5-60T621-591q-8-10-8-23t9-22q9-9 21.5-8.5T664-634q26 32 41 70.5t15 83.5q0 100-70 170t-170 70q-100 0-170-70t-70-170q0-93 60-160.5T450-719v-100q-131 11-220.5 108T140-480q0 142 99 241t241 99q142 0 241-99t99-241q0-65-22-122t-62-102q-9-10-9.5-23t8.5-22q9-9 22-8.5t21 10.5q48 54 75 121.5T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">镜像来源（Image provenance）</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解构建来源元数据如何帮助追踪 Docker Hardened Images 的来源并支持 SLSA 合规性。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 合规性标准


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/fips/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m437-433-73-76q-9-10-22-10t-23 9q-10 10-10 23t10 23l97 96q9 9 21 9t21-9l183-182q9-9 9-22t-10-22q-9-8-21.5-7.5T598-593L437-433ZM332-84l-62-106-124-25q-11-2-18.5-12t-5.5-21l14-120-79-92q-8-8-8-20t8-20l79-91-14-120q-2-11 5.5-21t18.5-12l124-25 62-107q6-10 17-14t22 1l109 51 109-51q11-5 22-1.5t17 13.5l63 108 123 25q11 2 18.5 12t5.5 21l-14 120 79 91q8 8 8 20t-8 20l-79 92 14 120q2 11-5.5 21T814-215l-123 25-63 107q-6 10-17 13.5T589-71l-109-51-109 51q-11 5-22 1t-17-14Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">FIPS</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Hardened Images 如何通过经过验证的加密模块和签名认证支持 FIPS 140，以满足合规审计要求。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/stig/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-83q-5.32 0-9.88-1-4.56-1-9.12-3-138-47-219.5-168.5T160-522.11V-718q0-19.26 10.88-34.66Q181.75-768.07 199-775l260-97q11-4 21-4t21 4l260 97q17.25 6.93 28.13 22.34Q800-737.26 800-718v196q0 64-17.79 125.56Q764.42-334.87 731-279L604-402q13-17 19-38t6-42q0-63-43.5-106.5T480-632q-62 0-105.5 43.5t-43.5 106q0 62.5 43.5 105.5T480-334q21.68 0 42.84-7 21.16-7 39.89-18L697-229q-42 52-88.5 86T499-87q-4.56 2-9.12 3T480-83Zm-.2-311q-36.8 0-62.8-25.5t-26-63q0-37.5 26.2-63.5 26.21-26 63-26 36.8 0 62.8 26t26 63.5q0 37.5-26.2 63-26.21 25.5-63 25.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">STIG</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Hardened Images 如何提供符合 STIG 标准的容器镜像，并附带可验证的安全扫描认证，以满足政府和企业的合规要求。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/cis/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">CIS 基准</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Hardened Images 如何帮助您满足互联网安全中心（CIS）Docker 基准要求，以实现安全的容器配置和部署。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 漏洞和风险管理


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/cves/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M479.98-280q14.02 0 23.52-9.48t9.5-23.5q0-14.02-9.48-23.52t-23.5-9.5q-14.02 0-23.52 9.48t-9.5 23.5q0 14.02 9.48 23.52t23.5 9.5Zm3.2-153q12.82 0 21.32-8.63 8.5-8.62 8.5-21.37v-193q0-12.75-8.68-21.38-8.67-8.62-21.5-8.62-12.82 0-21.32 8.62-8.5 8.63-8.5 21.38v193q0 12.75 8.68 21.37 8.67 8.63 21.5 8.63Zm-2.91 353q-82.74 0-155.5-31.5Q252-143 197.5-197.5t-86-127.34Q80-397.68 80-480.5t31.5-155.66Q143-709 197.5-763t127.34-85.5Q397.68-880 480.5-880t155.66 31.5Q709-817 763-763t85.5 127Q880-563 880-480.27q0 82.74-31.5 155.5Q817-252 763-197.68q-54 54.31-127 86Q563-80 480.27-80Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">常见漏洞和暴露（CVE）</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 CVE 是什么、Docker Hardened Images 如何减少暴露风险，以及如何使用流行工具扫描镜像中的漏洞。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/vex/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M92-120q-9 0-15.65-4.13Q69.7-128.25 66-135q-4.17-6.6-4.58-14.3Q61-157 66-165l388-670q5-8 11.5-11.5T480-850q8 0 14.5 3.5T506-835l388 670q5 8 4.58 15.7-.41 7.7-4.58 14.3-3.7 6.75-10.35 10.87Q877-120 868-120H92Zm392.18-117q12.82 0 21.32-8.68 8.5-8.67 8.5-21.5 0-12.82-8.68-21.32-8.67-8.5-21.5-8.5-12.82 0-21.32 8.68-8.5 8.67-8.5 21.5 0 12.82 8.68 21.32 8.67 8.5 21.5 8.5Zm0-111q12.82 0 21.32-8.63 8.5-8.62 8.5-21.37v-164q0-12.75-8.68-21.38-8.67-8.62-21.5-8.62-12.82 0-21.32 8.62-8.5 8.63-8.5 21.38v164q0 12.75 8.68 21.37 8.67 8.63 21.5 8.63Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">漏洞可利用性交换（VEX）</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 VEX 如何通过识别 Docker Hardened Images 中实际可利用的漏洞，帮助您优先处理真实风险。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/sscs/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-84q-5 0-9.5-1t-9.5-3q-139-47-220-168.5T160-523v-196q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v196q0 145-81 266.5T499-88q-5 2-9.5 3t-9.5 1Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">软件供应链安全</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Hardened Images 如何通过签名元数据、来源信息和最小攻击面，帮助您保护软件供应链的每个阶段。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/ssdlc/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m643-273 44-41q7-7 7-15.5t-7-15.5L535-497q5-14 8-27t3-27q0-58-41-99t-99-41q-11 0-21 1.5t-20 5.5q-9 5-13 13t2 14l73 72-54 51-71-70q-5-5-13-4t-11 9q-5 11-7 23.5t-2 24.5q0 57 40 96.5t97 39.5q14 0 27.5-2.5T461-425l151 152q6 6 15.5 6t15.5-6ZM480-80q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">安全软件开发生命周期（SSDLC）</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Hardened Images 如何通过与扫描、签名和调试工具的集成，支持安全的 SDLC。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 镜像结构和行为


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/distroless/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M779-609q23 18 23 47t-23 47l-108 84q-9 7-20.5 6t-19.5-9L359-706q-10-10-9-23.5t12-21.5l81-63q17-13 37-12.5t37 13.5l262 204Zm30 522L641-255l-124 96q-17 13-37 13t-37-13L151-386q-12-9-11.5-23.5T152-433q8-6 18-6t18 6l292 227 118-92-55-55h28l-54 42q-17 13-37 13t-37-13L181-515q-23-18-23-47t23-47l59-47L95-801q-9-9-9-21t9-21q9-9 21.5-9t21.5 9l714 714q9 9 9 21t-9 21q-9 9-21.5 9T809-87Zm-1-346q12 9 12 23.5T809-386l-52 41q-9 7-20.5 6t-19.5-9q-10-10-9-23.5t12-21.5l52-40q8-6 18-6t18 6Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">无发行版镜像（Distroless images）</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Hardened Images 如何使用无发行版变体来最小化攻击面并移除不必要的组件。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/glibc-musl/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M352.82-450q-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-286L223-666q-9 9-21.16 9t-21-8.61Q172-675 172-687.1q0-12.1 9-20.9l151-151q5-5 10.13-7 5.14-2 11-2 5.87 0 10.87 2 5 2 10 7l151 151q9 9 9 21t-9 21.39q-9 8.61-21 8.61t-21-9L383-766v286q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63ZM606.87-92Q601-92 596-94q-5-2-10-7L435-252q-9-9-9-21t9-21.39q9-8.61 21-8.61t21 9l100 100v-286q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v286l100-100q9-9 21.16-9t21 8.61Q788-285 788-272.9q0 12.1-9 20.9L628-101q-5 5-10.13 7-5.14 2-11 2Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Docker Hardened Images 中的 glibc 和 musl 支持</h3>
    </div>
    <div class="card-content">
      <p class="card-description">比较 DHIs 的 glibc 和 musl 变体，为您的应用程序在兼容性、大小和性能需求方面选择合适的基准镜像。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/immutability/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M310-453h340q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H310q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5ZM480.27-80q-82.74 0-155.5-31.5Q252-143 197.5-197.5t-86-127.34Q80-397.68 80-480.5t31.5-155.66Q143-709 197.5-763t127.34-85.5Q397.68-880 480.5-880t155.66 31.5Q709-817 763-763t85.5 127Q880-563 880-480.27q0 82.74-31.5 155.5Q817-252 763-197.68q-54 54.31-127 86Q563-80 480.27-80Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">镜像不可变性</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解镜像摘要、只读容器和签名元数据如何确保 Docker Hardened Images 防篡改且不可变。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/hardening/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-142q106-35 175.5-128.5T737-480H480v-335l-260 97v196q0 12 .5 20.5T223-480h257v338Zm0 58q-5 0-9.5-1t-9.5-3q-139-47-220-168.5T160-523v-196q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v196q0 145-81 266.5T499-88q-5 2-9.5 3t-9.5 1Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">镜像加固</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Hardened Images 如何为安全性而设计，包括最小化组件、非 root 执行和默认安全配置。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 验证和可追溯性


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/digests/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M481-779q108 0 203.5 46T843-601q3 5 2.5 8t-3.5 6q-3 3-7.5 3t-8.5-5q-59-82-150.5-126T481-759q-103 0-193 44.5T138-589q-4 5-7.5 6t-7.5-1q-4-2-4-6.5t2-8.5q62-86 157-133t203-47Zm0 96q136 0 233.5 90T812-371q0 46-34 78t-82 32q-49 0-84-32t-35-78q0-39-28.5-65T481-462q-39 0-68 26t-29 65q0 104 63 173.5T604-100q6 2 7.5 5t.5 7q-1 5-4 7t-8 0q-103-26-169.5-103T364-371q0-47 34.5-79t82.5-32q48 0 82.5 32t34.5 79q0 38 29.5 64t68.5 26q38 0 66.5-26t28.5-64q0-123-91.5-206T481-660q-127 0-218.5 83T171-371q0 24 5.5 62.5T200-221q2 5 0 7.5t-5 4.5q-4 2-8.5 1t-6.5-6q-13-38-20.5-77.5T152-371q0-129 98-220.5T481-683Zm0-197q65 0 127.5 16T728-819q5 2 5.5 6t-1.5 7q-2 3-5.5 5t-8.5 0q-55-27-115-42.5T481-859q-62 0-121 14.5T247-801q-5 2-7.5.5T235-805q-2-2-2-6t3-6q57-31 119.5-47T481-880Zm0 298q92 0 158.5 61T706-371q0 5-2.5 7.5T696-361q-5 0-8-2.5t-3-7.5q0-81-60.5-136T481-562q-83 0-142.5 55T279-371q0 85 29.5 145T396-106q4 4 3.5 7.5T396-92q-2 2-6.5 3.5T381-92q-58-60-90.5-126T258-371q0-89 65.5-150T481-582Zm-1 200q5 0 7.5 3t2.5 8q0 81 59.5 133.5T687-185q8 0 19-1t24-3q5-1 8 1.5t4 5.5q1 4-.5 7t-6.5 4q-18 5-31.5 5.5t-16.5.5q-88 0-152.5-58.5T470-371q0-5 2.5-8t7.5-3Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">摘要（Digests）</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何使用不可变镜像摘要来保证一致性并验证您正在运行的精确 Docker Hardened Image。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/dhi/core-concepts/signatures/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M280-351q-54 0-91.5-37.5T151-480q0-54 37.5-91.5T280-609q54 0 91.5 37.5T409-480q0 54-37.5 91.5T280-351Zm0 111q81 0 142.5-46T503-407h32l50 50q5 5 10 7t11 2q6 0 11-2t10-7l63-63 63 63q5 5 10 7t11 2q6 0 11-2t10-7l104-104q5-5 7-10t2-11q0-6-2-11t-7-10l-43-43q-5-5-10-7t-11-2H503q-23-72-80.5-118.5T280-720q-100 0-170 70T40-480q0 100 70 170t170 70Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">代码签名</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Hardened Images 如何使用 Cosign 进行加密签名，以验证真实性、完整性和安全来源。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [CIS 基准](/dhi/core-concepts/cis/)

- [常见漏洞和暴露 (CVE)](/dhi/core-concepts/cves/)

- [FIPS <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>](/dhi/core-concepts/fips/)

- [Docker Hardened Images 中的 glibc 和 musl 支持](/dhi/core-concepts/glibc-musl/)

- [软件物料清单 (SBOM)](/dhi/core-concepts/sbom/)

- [软件制品供应链安全等级 (SLSA)](/dhi/core-concepts/slsa/)

- [安全软件开发生命周期](/dhi/core-concepts/ssdlc/)

- [STIG <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>](/dhi/core-concepts/stig/)

- [漏洞可利用性交换 (VEX)](/dhi/core-concepts/vex/)

- [不可变基础设施](/dhi/core-concepts/immutability/)

- [代码签名](/dhi/core-concepts/signatures/)

- [基础镜像加固](/dhi/core-concepts/hardening/)

- [极简或无发行版镜像](/dhi/core-concepts/distroless/)

- [证明](/dhi/core-concepts/attestations/)

- [软件供应链安全](/dhi/core-concepts/sscs/)

- [镜像摘要](/dhi/core-concepts/digests/)

- [镜像溯源](/dhi/core-concepts/provenance/)

