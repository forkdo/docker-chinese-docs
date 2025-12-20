# 单点登录概述





  
  
  
  


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
    
  
  <a class="link" href="https://docs.docker.com/desktop/release-notes/#4420">4.42</a> and later</span>
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



单点登录 (SSO) 允许用户通过其身份提供者 (IdP) 进行身份验证来访问 Docker。SSO 可以为整个公司（包括所有关联的组织）或具有 Docker Business 订阅的单个组织配置。

## SSO 的工作原理

启用 SSO 后，Docker 支持用户登录的非 IdP 初始化流程。用户不再使用 Docker 用户名和密码登录，而是被重定向到您的 IdP 登录页面。用户必须通过登录 Docker Hub 或 Docker Desktop 来启动 SSO 身份验证过程。

下图说明了 SSO 在 Docker Hub、Docker Desktop 和您的 IdP 之间如何运行和管理。

![SSO 架构](images/SSO.png)

## 设置 SSO

要在 Docker 中配置 SSO，请按照以下步骤操作：

1. [配置您的域名](configure.md)，创建并验证它。
1. [在 Docker 和您的 IdP 中创建 SSO 连接](connect.md)。
1. 将 Docker 链接到您的身份提供者。
1. 测试您的 SSO 连接。
1. 在 Docker 中配置用户。
1. 可选。[强制登录](../enforce-sign-in/_index.md)。
1. [管理您的 SSO 配置](manage.md)。

配置完成后，用户可以使用其公司电子邮件地址登录 Docker 服务。登录后，用户将被添加到您的公司，分配到组织，并加入团队。

## 先决条件

开始之前，请确保满足以下条件：

- 通知您的公司即将进行的 SSO 登录流程。
- 确保所有用户已安装 Docker Desktop 4.42 或更高版本。
- 确认每个 Docker 用户都有一个有效的 IdP 账户，使用与其唯一主要标识符 (UPN) 相同的电子邮件地址。
- 如果您计划 [强制 SSO](/manuals/enterprise/security/single-sign-on/connect.md#optional-enforce-sso)，通过 CLI 访问 Docker 的用户必须 [创建个人访问令牌 (PAT)](/docker-hub/access-tokens/)。PAT 替代其用户名和密码进行身份验证。
- 确保 CI/CD 管道使用 PAT 或 OAT 而非密码。

> [!IMPORTANT]
>
> Docker 计划在未来的版本中弃用基于密码的 CLI 登录。使用 PAT 可确保继续 CLI 访问。更多信息请参阅 [安全公告](/manuals/security/security-announcements.md#deprecation-of-password-logins-on-cli-when-sso-enforced)。

## 后续步骤

- 开始 [配置 SSO](configure.md)。
- 阅读 [常见问题](/manuals/enterprise/security/single-sign-on/faqs/general.md)。
- [排查](/manuals/enterprise/troubleshoot/troubleshoot-sso.md) SSO 问题。

- [管理单点登录](https://docs.docker.com/enterprise/security/single-sign-on/manage/)

- [连接单点登录](https://docs.docker.com/enterprise/security/single-sign-on/connect/)

- [配置单点登录](https://docs.docker.com/enterprise/security/single-sign-on/configure/)

