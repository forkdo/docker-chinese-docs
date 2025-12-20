# 配置用户





  
  
  
  


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
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 
    
  
  <a class="link" href="/desktop/release-notes/#4420">4.42</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
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



配置 SSO 连接后，下一步是配置用户。此过程确保用户可以通过自动化用户管理访问您的组织。

本页概述了用户配置以及支持的配置方法。

## 什么是配置？

配置通过根据身份提供商 (IdP) 的数据自动执行帐户创建、更新和停用等任务来帮助管理用户。有三种用户配置方法，每种方法都为不同的组织需求提供优势：

| 配置方法 | 描述 | Docker 中的默认设置 | 推荐用于 |
| :--- | :--- | :------------- | :--- |
| 即时 (JIT) | 在用户首次通过 SSO 登录时自动创建和配置用户帐户 | 默认启用 | 需要最少设置的组织、较小的团队或低安全性环境 |
| 跨域身份管理系统 (SCIM) | 在您的 IdP 和 Docker 之间持续同步用户数据，确保用户属性保持更新而无需手动干预 | 默认禁用 | 大型组织或用户信息或角色频繁更改的环境 |
| 组映射 | 将来自您 IdP 的用户组映射到 Docker 内的特定角色和权限，从而实现基于组成员资格的细粒度访问控制 | 默认禁用 | 需要严格访问控制和基于角色的用户管理的组织 |

## 默认配置设置

默认情况下，当您配置 SSO 连接时，Docker 会启用 JIT 配置。启用 JIT 后，用户帐户会在用户首次使用您的 SSO 流程登录时自动创建。

JIT 配置可能无法为某些组织提供足够的控制或安全性。在这种情况下，可以配置 SCIM 或组映射，以使管理员能够更好地控制用户访问和属性。

## SSO 属性

当用户通过 SSO 登录时，Docker 会从您的 IdP 获取多个属性来管理用户的身份和权限。这些属性包括：

- 电子邮件地址：用户的唯一标识符
- 全名：用户的完整姓名
- 组：可选。用于基于组的访问控制
- Docker 组织：可选。指定用户所属的组织
- Docker 团队：可选。定义用户在组织内所属的团队
- Docker 角色：可选。确定用户在 Docker 中的权限
- Docker 会话分钟数：可选。设置用户必须使用其 IdP 重新进行身份验证之前的会话持续时间。必须是大于 0 的正整数。如果未提供，则应用默认会话超时

> [!NOTE]
>
> 当未指定 Docker 会话分钟数时，将应用默认会话超时。Docker Desktop 会话在 90 天后或 30 天不活动后过期。Docker Hub 和 Docker Home 会话在 24 小时后过期。

## SAML 属性映射

如果您的组织使用 SAML 进行 SSO，Docker 会从 SAML 断言消息中检索这些属性。不同的 IdP 可能对这些属性使用不同的名称。

| SSO 属性 | SAML 断言消息属性 |
| :--- | :--- |
| 电子邮件地址 | `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"`, `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn"`, `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"`, `email` |
| 全名 | `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"`, `name`, `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname"`, `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname"` |
| 组 (可选) | `"http://schemas.xmlsoap.org/claims/Group"`, `"http://schemas.microsoft.com/ws/2008/06/identity/claims/groups"`, `Groups`, `groups` |
| Docker 组织 (可选) | `dockerOrg` |
| Docker 团队 (可选) | `dockerTeam` |
| Docker 角色 (可选) | `dockerRole` |
| Docker 会话分钟数 (可选) | `dockerSessionMinutes`, 必须是大于 0 的正整数 |

## 下一步

选择最适合您组织需求的配置方法：


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="just-in-time/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M513-492v-171q0-13-8.5-21.5T483-693q-13 0-21.5 8.5T453-663v183q0 6 2 11t6 10l144 149q9 10 22.5 9.5T650-310q9-9 9-22t-9-22L513-492ZM480-80q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-82 31.5-155t86-127.5Q252-817 325-848.5T480-880q82 0 155 31.5t127.5 86Q817-708 848.5-635T880-480q0 82-31.5 155t-86 127.5Q708-143 635-111.5T480-80Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">即时 (JIT) 配置</h3>
    </div>
    <div class="card-content">
      <p class="card-description">设置首次登录时自动创建用户。适用于设置要求简单的较小团队。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="scim/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M220-477q0 63 23.5 109.5T307-287l30 21v-94q0-13 8.5-21.5T367-390q13 0 21.5 8.5T397-360v170q0 13-8.5 21.5T367-160H197q-13 0-21.5-8.5T167-190q0-13 8.5-21.5T197-220h100l-15-12q-64-51-93-111t-29-134q0-94 49.5-171.5T342-766q11-5 21 0t14 16q5 11 0 22.5T361-710q-64 34-102.5 96.5T220-477Zm520-6q0-48-23.5-97.5T655-668l-29-26v94q0 13-8.5 21.5T596-570q-13 0-21.5-8.5T566-600v-170q0-13 8.5-21.5T596-800h170q13 0 21.5 8.5T796-770q0 13-8.5 21.5T766-740H665l15 14q60 56 90 120t30 123q0 93-48 169.5T623-195q-11 6-22.5 1.5T584-210q-5-11 0-22.5t16-17.5q65-33 102.5-96T740-483Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">SCIM 配置</h3>
    </div>
    <div class="card-content">
      <p class="card-description">在您的 IdP 和 Docker 之间启用持续的用户数据同步。适用于大型组织。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="group-mapping/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M38-254q0-35 18-63.5t50-42.5q73-32 131.5-46T358-420q62 0 120 14t131 46q32 14 50.5 42.5T678-254v34q0 25-17.5 42.5T618-160H98q-25 0-42.5-17.5T38-220v-34Zm686 94q5-15 9.5-29.5T738-220v-34q0-63-29-101.5T622-420q69 8 130 22t99 34q33 19 52 47t19 63v34q0 25-17.5 42.5T862-160H724ZM358-481q-66 0-108-42t-42-108q0-66 42-108t108-42q66 0 108 42t42 108q0 66-42 108t-108 42Zm360-150q0 66-42 108t-108 42q-11 0-24.5-1.5T519-488q24-25 36.5-61.5T568-631q0-45-12.5-79.5T519-774q11-3 24.5-5t24.5-2q66 0 108 42t42 108Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">组映射</h3>
    </div>
    <div class="card-content">
      <p class="card-description">使用 IdP 组配置基于角色的访问控制。适用于严格的访问控制要求。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [即时配置 (JIT)](/enterprise/security/provisioning/just-in-time/)

- [组映射](/enterprise/security/provisioning/group-mapping/)

- [](/enterprise/security/provisioning/scim/)

