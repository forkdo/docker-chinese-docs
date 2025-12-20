# 管理单点登录





  
  
  
  


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



本页介绍在初始设置后如何管理单点登录 (SSO)，
包括管理域、连接、用户和配置设置。

## 管理域

### 添加域

要将域添加到现有的 SSO 连接：

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角的帐户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**（管理控制台），然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择您的连接的 **Actions**（操作）菜单，然后选择 **Edit connection**（编辑连接）。
1. 选择 **Next**（下一步）导航到域部分。
1. 在 **Domains**（域）部分，选择 **Add domain**（添加域）。
1. 输入要添加到连接的域。
1. 选择 **Next**（下一步）确认或更改连接的组织。
1. 选择 **Next**（下一步）确认或更改默认组织和团队配置选择。
1. 查看连接详细信息，然后选择 **Update connection**（更新连接）。

### 从 SSO 连接中移除域

> [!IMPORTANT]
>
> 如果您对同一域使用多个身份提供者，则必须从每个 SSO 连接中单独移除该域。

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角的帐户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**（管理控制台），然后选择 **SSO and SCIM**。
1. 在 **SSO connections**（SSO 连接）表中，选择您的连接的 **Actions**（操作）菜单，然后选择 **Edit connection**（编辑连接）。
1. 选择 **Next**（下一步）导航到域部分。
1. 在 **Domain**（域）部分，选择您要移除的域旁边的 **X** 图标。
1. 选择 **Next**（下一步）确认或更改连接的组织。
1. 选择 **Next**（下一步）确认或更改默认组织和团队配置选择。
1. 查看连接详细信息，然后选择 **Update connection**（更新连接）。

> [!NOTE]
>
> 当您重新添加域时，Docker 会分配一个新的 TXT 记录值。您必须使用新的 TXT 记录再次完成域验证。

## 管理 SSO 连接

### 查看连接

要查看所有已配置的 SSO 连接：

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角的帐户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**（管理控制台），然后选择 **SSO and SCIM**。
1. 在 **SSO connections**（SSO 连接）表中查看所有已配置的连接。

### 编辑连接

要修改现有的 SSO 连接：

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角的帐户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**（管理控制台），然后选择 **SSO and SCIM**。
1. 在 **SSO connections**（SSO 连接）表中，选择您的连接的 **Actions**（操作）菜单，然后选择 **Edit connection**（编辑连接）。
1. 按照屏幕上的说明修改您的连接设置。

### 删除连接

要移除 SSO 连接：

1. 登录 [Docker Home](https://app.docker.com)，然后从左上角的帐户下拉菜单中选择您的公司或组织。
1. 选择 **Admin Console**（管理控制台），然后选择 **SSO and SCIM**。
1. 在 **SSO connections**（SSO 连接）表中，选择您的连接的 **Actions**（操作）菜单，然后选择 **Delete connection**（删除连接）。
1. 按照屏幕上的说明确认删除。

> [!WARNING]
>
> 删除 SSO 连接会移除所有通过该连接进行身份验证的用户的访问权限。

## 管理用户和配置

Docker 会在用户通过 SSO 登录时，通过即时 (JIT) 配置自动配置用户。您也可以手动管理用户并配置不同的配置方法。

### 配置工作原理

Docker 支持以下配置方法：

- JIT 配置（默认）：用户通过 SSO 登录时会自动添加到您的组织
- SCIM 配置：将用户和组从您的身份提供者同步到 Docker
- 组映射：将您的身份提供者中的用户组与 Docker 组织中的团队同步
- 手动配置：关闭自动配置并手动邀请用户

有关配置方法的更多信息，请参阅[配置用户](/manuals/enterprise/security/provisioning/_index.md)。

### 添加访客用户

要邀请不通过您的身份提供者进行身份验证的用户：

1. 登录 [Docker Home](https://app.docker.com/)，然后选择您的组织。
1. 选择 **Members**（成员）。
1. 选择 **Invite**（邀请）。
1. 按照屏幕上的说明邀请用户。

用户将收到一封电子邮件邀请，并可以创建 Docker 帐户或使用其现有帐户登录。

### 移除用户

要从您的组织中移除用户：

1. 登录 [Docker Home](https://app.docker.com/)，然后选择您的组织。
1. 选择 **Members**（成员）。
1. 找到您要移除的用户，然后选择其姓名旁边的 **Actions**（操作）菜单。
1. 选择 **Remove**（移除）并确认移除。

用户在被移除后会立即失去对您组织的访问权限。
