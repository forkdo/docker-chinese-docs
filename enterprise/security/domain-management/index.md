# 管理域名





  
  
  
  


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



域名管理允许您为组织添加和验证域名，然后启用自动配置功能，当用户使用与已验证域名匹配的电子邮件地址登录时，自动将其添加到组织中。这种方法简化了用户管理，确保安全设置的一致性，并降低了未受管理的用户访问 Docker 的风险。

本页提供了添加和删除域名、配置自动配置以及审核未捕获用户的步骤。

## 添加和验证域名

添加域名需要验证以确认所有权。验证过程使用 DNS 记录来证明您控制该域名。

### 添加域名

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司并在公司级别为组织配置域名。
1. 选择 **管理控制台**，然后选择 **域名管理**。
1. 选择 **添加域名**。
1. 输入您的域名并选择 **添加域名**。
1. 在弹出的模态框中，复制 **TXT 记录值** 以验证您的域名。

### 验证域名

通过在域名系统 (DNS) 主机中添加 TXT 记录来验证您拥有该域名。DNS 更改可能需要最多 72 小时才能传播。Docker 会自动检查记录，并在识别到更改后确认所有权。

> [!TIP]
>
> 记录名称字段决定了 TXT 记录在您的域名中的添加位置（根域名或子域名）。对于 `example.com` 等根域名，根据您的提供商使用 `@` 或将记录名称留空。不要输入 docker、`docker-verification`、`www` 或您的域名等值，因为这些可能会指向错误的位置。请查阅您的 DNS 提供商文档以确认记录名称要求。

按照您的 DNS 提供商的步骤添加 **TXT 记录值**。如果您的提供商未列出，请使用“其他提供商”的步骤：








<div
  class="tabs"
  
    x-data="{ selected: 'AWS-Route-53' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'AWS-Route-53' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'AWS-Route-53'"
        
      >
        AWS Route 53
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Google-Cloud-DNS' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Google-Cloud-DNS'"
        
      >
        Google Cloud DNS
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'GoDaddy' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'GoDaddy'"
        
      >
        GoDaddy
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Other-providers' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Other-providers'"
        
      >
        Other providers
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'AWS-Route-53' && 'hidden'"
      >
        <ol>
<li>按照 <a class="link" href="https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html" rel="noopener">使用 Amazon Route 53 控制台创建记录</a> 将 TXT 记录添加到 AWS。</li>
<li>等待最多 72 小时以完成 TXT 记录验证。</li>
<li>返回 <a class="link" href="https://app.docker.com/admin" rel="noopener">管理控制台</a> 的 <strong>域名管理</strong> 页面，选择您域名旁边的 <strong>验证</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Google-Cloud-DNS' && 'hidden'"
      >
        <ol>
<li>按照 <a class="link" href="https://cloud.google.com/identity/docs/verify-domain-txt" rel="noopener">使用 TXT 记录验证您的域名</a> 将 TXT 记录添加到 Google Cloud DNS。</li>
<li>等待最多 72 小时以完成 TXT 记录验证。</li>
<li>返回 <a class="link" href="https://app.docker.com/admin" rel="noopener">管理控制台</a> 的 <strong>域名管理</strong> 页面，选择您域名旁边的 <strong>验证</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'GoDaddy' && 'hidden'"
      >
        <ol>
<li>按照 <a class="link" href="https://www.godaddy.com/help/add-a-txt-record-19232" rel="noopener">添加 TXT 记录</a> 将 TXT 记录添加到 GoDaddy。</li>
<li>等待最多 72 小时以完成 TXT 记录验证。</li>
<li>返回 <a class="link" href="https://app.docker.com/admin" rel="noopener">管理控制台</a> 的 <strong>域名管理</strong> 页面，选择您域名旁边的 <strong>验证</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Other-providers' && 'hidden'"
      >
        <ol>
<li>登录您的域名主机。</li>
<li>使用 Docker 提供的 <strong>TXT 记录值</strong> 将 TXT 记录添加到您的 DNS 设置中。</li>
<li>等待最多 72 小时以完成 TXT 记录验证。</li>
<li>返回 <a class="link" href="https://app.docker.com/admin" rel="noopener">管理控制台</a> 的 <strong>域名管理</strong> 页面，选择您域名旁边的 <strong>验证</strong>。</li>
</ol>

      </div>
    
  </div>
</div>


## 配置自动配置

自动配置会在用户使用与已验证域名匹配的电子邮件地址登录时，自动将用户添加到您的组织中。您必须先验证域名，然后才能启用自动配置。

> [!IMPORTANT]
>
> 对于属于 SSO 连接的域名，在将用户添加到组织时，即时 (JIT) 配置优先于自动配置。

### 自动配置的工作原理

当为已验证域名启用自动配置时：

- 使用匹配电子邮件地址登录 Docker 的用户将自动添加到您的组织中。
- 自动配置仅将现有的 Docker 用户添加到您的组织，不会创建新帐户。
- 用户的登录过程不会发生任何变化。
- 公司和组织所有者会在新用户添加时收到电子邮件通知。
- 您可能需要 [管理席位](/manuals/subscription/manage-seats.md) 以容纳新用户。

### 启用自动配置

自动配置按域名配置。要启用它：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的公司或组织。
1. 选择 **管理控制台**，然后选择 **域名管理**。
1. 选择您要启用自动配置的域名旁边的 **操作菜单**。
1. 选择 **启用自动配置**。
1. 可选。如果在公司级别启用自动配置，请选择一个组织。
1. 选择 **启用** 以确认。

**自动配置** 列将更新为 **已启用**。

### 禁用自动配置

要为用户禁用自动配置：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司并在公司级别为组织配置域名。
1. 选择 **管理控制台**，然后选择 **域名管理**。
1. 选择您域名旁边的 **操作菜单**。
1. 选择 **禁用自动配置**。
1. 选择 **禁用** 以确认。

## 审核未捕获用户的域名





  
  
  
  


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



域名审核可识别未捕获的用户。未捕获的用户是指使用与您的已验证域名关联的电子邮件地址进行身份验证但并非 Docker 组织成员的 Docker 用户。

### 限制

域名审核无法识别：

- 未进行身份验证而访问 Docker Desktop 的用户
- 使用未关联您已验证域名的电子邮件地址的帐户进行身份验证的用户

为防止无法识别的用户访问 Docker Desktop，请 [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。

### 运行域名审核

1. 登录 [Docker Home](https://app.docker.com) 并选择您的公司。
1. 选择 **管理控制台**，然后选择 **域名管理**。
1. 在 **域名审核** 中，选择 **导出用户** 以导出未捕获用户的 CSV 文件。

CSV 文件包含以下列：
- 名称：Docker 用户的显示名称
- 用户名：用户的 Docker ID
- 电子邮件：用户的电子邮件地址

### 邀请未捕获的用户

您可以使用导出的 CSV 文件批量邀请未捕获的用户加入您的组织。有关批量邀请用户的更多信息，请参阅
[管理组织成员](/manuals/admin/organization/members.md)。

## 删除域名

删除域名会删除其 TXT 记录值并禁用任何关联的自动配置。

>[!WARNING]
>
> 删除域名将禁用该域名的自动配置并移除验证。此操作无法撤销。

要删除域名：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果您的组织属于某个公司，请选择该公司并在公司级别为组织配置域名。
1. 选择 **管理控制台**，然后选择 **域名管理**。
1. 对于您要删除的域名，选择 **操作** 菜单，然后选择 **删除域名**。
1. 在弹出的模态框中选择 **删除域名** 以确认。

