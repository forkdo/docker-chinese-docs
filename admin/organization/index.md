# 组织管理概览

Docker 组织是一个由团队和仓库组成的集合，并采用集中式管理。它帮助管理员以一种精简且可扩展的方式对成员进行分组并分配访问权限。

## 组织结构

下图展示了组织与团队及成员之间的关系。

![展示 Docker 组织内团队与成员关系的示意图](/admin/images/org-structure.webp)

## 组织成员

组织所有者拥有完整的管理员访问权限，可以管理整个组织内的成员、角色和团队。

一个组织包含成员和可选的团队。团队帮助对成员进行分组并简化权限管理。

## 创建和管理您的组织

在以下章节中，您将学习如何创建和管理您的组织。


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/admin/organization/onboard" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-440q-17 0-28.5-11.5T440-480q0-17 11.5-28.5T480-520q17 0 28.5 11.5T520-480q0 17-11.5 28.5T480-440Zm0 360q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Zm0-60q142 0 241-99.5T820-480q0-142-99-241t-241-99q-141 0-240.5 99T140-480q0 141 99.5 240.5T480-140Zm0 0q-141 0-240.5-99.5T140-480q0-142 99.5-241T480-820q142 0 241 99t99 241q0 141-99 240.5T480-140Zm64-261q5-2 8.5-5.5t5.5-8.5l118-241q5-10-2.5-17.5T656-676L415-558q-5 2-8.5 5.5T401-544L283-303q-5 10 2.5 17.5T303-283l241-118Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">组织入门</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何入门并保障您的组织安全。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/admin/organization/members/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M474-486q26-32 38.5-66t12.5-79q0-45-12.5-79T474-776q76-17 133.5 23T665-631q0 82-57.5 122T474-486Zm202 326q5-15 9.5-29.5T690-220v-34q0-51-26-95t-90-74q173 22 236.5 64T874-254v34q0 24.75-17.62 42.37Q838.75-160 814-160H676Zm124-389h-70q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h70v-70q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v70h70q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-70v70q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-70Zm-485 68q-66 0-108-42t-42-108q0-66 42-108t108-42q66 0 108 42t42 108q0 66-42 108t-108 42ZM0-220v-34q0-35 18.5-63.5T68-360q72-32 128.5-46T315-420q62 0 118 14t128 46q31 14 50 42.5t19 63.5v34q0 24.75-17.62 42.37Q594.75-160 570-160H60q-24.75 0-42.37-17.63Q0-195.25 0-220Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">管理成员</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索如何管理成员。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/admin/organization/activity-logs/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M180-120q-24.75 0-42.37-17.63Q120-155.25 120-180v-600q0-24.75 17.63-42.38Q155.25-840 180-840h375q12.44 0 23.72 5T598-822l224 224q8 8 13 19.28 5 11.28 5 23.72v375q0 24.75-17.62 42.37Q804.75-120 780-120H180Zm129-171h342q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H309q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm0-159h342q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H309q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm0-159h216q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H309q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">活动日志</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何审计成员的活动。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/admin/organization/image-access/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M345-377h391L609-548 506-413l-68-87-93 123Zm-85 177q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h560q24 0 42 18t18 42v560q0 24-18 42t-42 18H260Zm0-60h560v-560H260v560ZM140-80q-24 0-42-18t-18-42v-620h60v620h620v60H140Zm120-740h560v560H260v-560Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">镜像访问管理</h3>
    </div>
    <div class="card-content">
      <p class="card-description">控制您的开发者可以拉取的镜像类型。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/admin/organization/registry-access/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M251-120q-22 0-38.5-14T192-170l-66-395q-2-14 6.5-24.5T155-600h650q14 0 22.5 10.5T834-565l-66 395q-4 22-20.5 36T709-120H251Zm149-260h160q13 0 21.5-9t8.5-21q0-13-8.5-21.5T560-440H400q-12 0-21 8.5t-9 21.5q0 12 9 21t21 9ZM240-660q-12 0-21-9t-9-21q0-13 9-21.5t21-8.5h480q13 0 21.5 8.5T750-690q0 12-8.5 21t-21.5 9H240Zm80-120q-12 0-21-9t-9-21q0-13 9-21.5t21-8.5h320q13 0 21.5 8.5T670-810q0 12-8.5 21t-21.5 9H320Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">仓库访问管理</h3>
    </div>
    <div class="card-content">
      <p class="card-description">定义您的开发者可以访问的仓库。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/admin/organization/general-settings/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M421-80q-14 0-25-9t-13-23l-15-94q-19-7-40-19t-37-25l-86 40q-14 6-28 1.5T155-226L97-330q-8-13-4.5-27t15.5-23l80-59q-2-9-2.5-20.5T185-480q0-9 .5-20.5T188-521l-80-59q-12-9-15.5-23t4.5-27l58-104q8-13 22-17.5t28 1.5l86 40q16-13 37-25t40-18l15-95q2-14 13-23t25-9h118q14 0 25 9t13 23l15 94q19 7 40.5 18.5T669-710l86-40q14-6 27.5-1.5T804-734l59 104q8 13 4.5 27.5T852-580l-80 57q2 10 2.5 21.5t.5 21.5q0 10-.5 21t-2.5 21l80 58q12 8 15.5 22.5T863-330l-58 104q-8 13-22 17.5t-28-1.5l-86-40q-16 13-36.5 25.5T592-206l-15 94q-2 14-13 23t-25 9H421Zm59-270q54 0 92-38t38-92q0-54-38-92t-92-38q-54 0-92 38t-38 92q0 54 38 92t92 38Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">组织设置</h3>
    </div>
    <div class="card-content">
      <p class="card-description">为您的组织配置信息并管理设置。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M280-351q-54 0-91.5-37.5T151-480q0-54 37.5-91.5T280-609q54 0 91.5 37.5T409-480q0 54-37.5 91.5T280-351Zm0 111q81 0 142.5-46T503-407h32l50 50q5 5 10 7t11 2q6 0 11-2t10-7l63-63 63 63q5 5 10 7t11 2q6 0 11-2t10-7l104-104q5-5 7-10t2-11q0-6-2-11t-7-10l-43-43q-5-5-10-7t-11-2H503q-23-72-80.5-118.5T280-720q-100 0-170 70T40-480q0 100 70 170t170 70Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">SSO 和 SCIM</h3>
    </div>
    <div class="card-content">
      <p class="card-description">为您的组织设置
  <a class="link" href="/security/for-admins/single-sign-on/">单点登录</a> 和 
  <a class="link" href="/security/for-admins/provisioning/scim/">SCIM</a>。</p>
    </div>
  
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
      <p class="card-description">添加、验证和审计您的域名。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/faq/admin/organization-faqs/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M484.03-247Q500-247 511-258.03q11-11.03 11-27T510.97-312q-11.03-11-27-11T457-311.97q-11 11.03-11 27T457.03-258q11.03 11 27 11Zm-3.76 167q-82.74 0-155.5-31.5Q252-143 197.5-197.5t-86-127.34Q80-397.68 80-480.5t31.5-155.66Q143-709 197.5-763t127.34-85.5Q397.68-880 480.5-880t155.66 31.5Q709-817 763-763t85.5 127Q880-563 880-480.27q0 82.74-31.5 155.5Q817-252 763-197.68q-54 54.31-127 86Q563-80 480.27-80Zm2.5-580Q513-660 536-641.5q23 18.5 23 47.2 0 26.3-15.65 45.73Q527.7-529.14 508-512q-23 19-40 42.38-17 23.39-17 52.62 0 11 8.4 17.5T479-393q12 0 19.88-8 7.87-8 10.12-20 3-21 16-38t30.23-30.78Q580-510 596-537q16-27 16-58.61 0-50.39-37.5-83.89T485.55-713Q450-713 417-698t-54 44q-7 10-6.5 21.5t9.47 18.5q11.41 8 23.65 5 12.23-3 20.38-14 12.75-17.9 31.88-27.45Q461-660 482.77-660Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">常见问题</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索常见的组织相关问题。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [创建您的组织](/admin/organization/orgs/)

- [为您的组织完成上车流程](/admin/organization/onboard/)

- [管理组织成员](/admin/organization/members/)

- [将账户转换为组织](/admin/organization/convert-account/)

- [创建和管理团队](/admin/organization/manage-a-team/)

- [停用组织](/admin/organization/deactivate-account/)

- [管理 Docker 产品](/admin/organization/manage-products/)

- [活动日志](/admin/organization/activity-logs/)

- [组织信息](/admin/organization/general-settings/)

- [洞察 (Insights)](/admin/organization/insights/)

