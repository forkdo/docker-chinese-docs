# 公司管理概览





  
  
  
  


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



公司提供了跨多个组织的单一可见性视图，简化了组织和设置管理。

拥有 Docker Business 订阅的组织所有者可以创建公司并通过 [Docker 管理控制台](https://app.docker.com/admin) 进行管理。

下图展示了公司与其关联组织之间的关系。

![展示公司与 Docker 组织关系的图表](/admin/images/docker-admin-structure.webp)

## 主要功能

通过公司，管理员可以：

- 查看和管理所有嵌套组织
- 集中配置公司和组织设置
- 控制对公司访问权限
- 最多可将十名唯一用户分配为公司所有者角色
- 为所有嵌套组织配置 SSO 和 SCIM
- 强制公司中所有用户使用 SSO

## 创建和管理公司

在以下章节中了解如何创建和管理公司。


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/admin/company/new-company/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M180-120q-24.75 0-42.37-17.63Q120-155.25 120-180v-435q0-24.75 17.63-42.38Q155.25-675 180-675h105v-105q0-24.75 17.63-42.38Q320.25-840 345-840h270q24.75 0 42.38 17.62Q675-804.75 675-780v270h105q24.75 0 42.38 17.62Q840-474.75 840-450v270q0 24.75-17.62 42.37Q804.75-120 780-120H533v-165H427v165H180Zm0-60h105v-105H180v105Zm0-165h105v-105H180v105Zm0-165h105v-105H180v105Zm165 165h105v-105H345v105Zm0-165h105v-105H345v105Zm0-165h105v-105H345v105Zm165 330h105v-105H510v105Zm0-165h105v-105H510v105Zm0-165h105v-105H510v105Zm165 495h105v-105H675v105Zm0-165h105v-105H675v105Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">创建公司</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何创建公司。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/admin/company/organizations/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M195-793h572q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H195q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5Zm5 627q-12.75 0-21.37-8.63Q170-183.25 170-196v-215h-25q-14.14 0-23.07-11T116-447l44-202q2-11 10.25-17.5T189-673h583q10.5 0 18.75 6.5T801-649l44 202q3 14-5.93 25T816-411h-25v215q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-215H552v215q0 12.75-8.62 21.37Q534.75-166 522-166H200Zm30-60h262v-185H230v185Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">管理组织</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何在公司中添加和管理组织以及席位。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/admin/company/owners/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-80q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-155.5t86-127Q252-817 325-848.5T480-880q83 0 155.5 31.5t127 86q54.5 54.5 86 127T880-480q0 82-31.5 155t-86 127.5q-54.5 54.5-127 86T480-80ZM373-420q57 0 97.5-40.5T511-558q0-57-40.5-97.5T373-696q-57 0-97.5 40.5T235-558q0 57 40.5 97.5T373-420Zm301 46q44 0 75-31t31-75q0-44-31-75t-75-31q-44 0-75 31t-31 75q0 44 31 75t75 31ZM480-140q86 0 158-39t119-104q-21-6-40.5-10.5T674-298q-55 0-129.5 32.5T422-145q14 2 28.5 3.5T480-140Zm-135-28q32-71 75-107t60-47q-23-10-50.5-14t-56.5-4q-47 0-91.5 12.5T196-293q27 42 65 73.5t84 51.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">管理公司所有者</h3>
    </div>
    <div class="card-content">
      <p class="card-description">详细了解公司所有者以及如何管理他们。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/admin/company/users/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M474-486q26-32 38.5-66t12.5-79q0-45-12.5-79T474-776q76-17 133.5 23T665-631q0 82-57.5 122T474-486Zm202 326q5-15 9.5-29.5T690-220v-34q0-51-26-95t-90-74q173 22 236.5 64T874-254v34q0 24.75-17.62 42.37Q838.75-160 814-160H676Zm124-389h-70q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h70v-70q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v70h70q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-70v70q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-70Zm-485 68q-66 0-108-42t-42-108q0-66 42-108t108-42q66 0 108 42t42 108q0 66-42 108t-108 42ZM0-220v-34q0-35 18.5-63.5T68-360q72-32 128.5-46T315-420q62 0 118 14t128 46q31 14 50 42.5t19 63.5v34q0 24.75-17.62 42.37Q594.75-160 570-160H60q-24.75 0-42.37-17.63Q0-195.25 0-220Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">管理用户</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索如何管理所有组织中的用户。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/security/for-admins/single-sign-on/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M280-351q-54 0-91.5-37.5T151-480q0-54 37.5-91.5T280-609q54 0 91.5 37.5T409-480q0 54-37.5 91.5T280-351Zm0 111q81 0 142.5-46T503-407h32l50 50q5 5 10 7t11 2q6 0 11-2t10-7l63-63 63 63q5 5 10 7t11 2q6 0 11-2t10-7l104-104q5-5 7-10t2-11q0-6-2-11t-7-10l-43-43q-5-5-10-7t-11-2H503q-23-72-80.5-118.5T280-720q-100 0-170 70T40-480q0 100 70 170t170 70Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">配置单点登录</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何为整个公司配置 SSO。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/security/for-admins/provisioning/scim/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m222-299 158-158q9-9 21-8.5t21.39 9.5q8.61 9 8.61 21t-9 21L243-235q-9 9-21 9t-21-9L101-335q-9-9-9-21t9-21q9-9 21-8.5t21 8.5l79 78Zm0-320 158-158q9-9 21-8.5t21.39 9.5q8.61 9 8.61 21t-9 21L243-555q-9 9-21 9t-21-9L101-655q-9-9-9-21t9-21q9-9 21-8.5t21 8.5l79 78Zm328 329q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h300q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H550Zm0-320q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h300q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H550Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">设置 SCIM</h3>
    </div>
    <div class="card-content">
      <p class="card-description">设置 SCIM 以自动配置和取消配置公司中的用户。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/security/for-admins/domain-management/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m438-400-62-62q-9-9-22-9t-22 9q-9 9-9 22t9 22l85 85q9 9 21 9t21-9l169-169q9-9 9-22t-9-22q-9-9-22-9t-22 9L438-400ZM140-656h680v-84H140v84Zm0 496q-24 0-42-18t-18-42v-520q0-24 18-42t42-18h680q24 0 42 18t18 42v520q0 24-18 42t-42 18H140Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">域名管理</h3>
    </div>
    <div class="card-content">
      <p class="card-description">添加并验证公司的域名。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/faq/admin/company-faqs/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M484.03-247Q500-247 511-258.03q11-11.03 11-27T510.97-312q-11.03-11-27-11T457-311.97q-11 11.03-11 27T457.03-258q11.03 11 27 11Zm-3.76 167q-82.74 0-155.5-31.5Q252-143 197.5-197.5t-86-127.34Q80-397.68 80-480.5t31.5-155.66Q143-709 197.5-763t127.34-85.5Q397.68-880 480.5-880t155.66 31.5Q709-817 763-763t85.5 127Q880-563 880-480.27q0 82.74-31.5 155.5Q817-252 763-197.68q-54 54.31-127 86Q563-80 480.27-80Zm2.5-580Q513-660 536-641.5q23 18.5 23 47.2 0 26.3-15.65 45.73Q527.7-529.14 508-512q-23 19-40 42.38-17 23.39-17 52.62 0 11 8.4 17.5T479-393q12 0 19.88-8 7.87-8 10.12-20 3-21 16-38t30.23-30.78Q580-510 596-537q16-27 16-58.61 0-50.39-37.5-83.89T485.55-713Q450-713 417-698t-54 44q-7 10-6.5 21.5t9.47 18.5q11.41 8 23.65 5 12.23-3 20.38-14 12.75-17.9 31.88-27.45Q461-660 482.77-660Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">常见问题</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索有关公司的常见问题。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [创建公司](/admin/company/new-company/)

- [管理公司成员](/admin/company/users/)

- [管理公司所有者](/admin/company/owners/)

- [管理公司组织](/admin/company/organizations/)

