# 配置单点登录





  
  
  
  


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



了解如何通过添加并验证成员用于登录的域名，为您的 Docker 组织设置单点登录 (SSO)。

## 第一步：添加域名

> [!NOTE]
>
> Docker 支持多个身份提供商 (IdP) 配置。您可以将一个域名与多个 IdP 关联。

添加域名：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。如果该组织是公司的一部分，请先选择公司以在该级别管理域名。
1. 选择 **Admin Console**，然后选择 **Domain management**。
1. 选择 **Add a domain**。
1. 在文本框中输入您的域名，然后选择 **Add domain**。
1. 在弹出的窗口中，复制为域名验证提供的 **TXT Record Value**。

## 第二步：验证您的域名

要确认域名所有权，请使用 Docker 提供的 TXT 记录值向您的域名系统 (DNS) 主机添加 TXT 记录。DNS 传播最多可能需要 72 小时。Docker 会在此期间自动检查记录。

> [!TIP]
>
> 添加记录名称时，对于根域名（如 `example.com`），**请使用 `@` 或留空**。**避免使用常见值**，如 `docker`、`docker-verification`、`www` 或您的域名本身。请务必**查阅您的 DNS 提供商文档**以验证其特定的记录名称要求。








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
        :class="selected === '%E5%85%B6%E4%BB%96%E6%8F%90%E4%BE%9B%E5%95%86' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E5%85%B6%E4%BB%96%E6%8F%90%E4%BE%9B%E5%95%86'"
        
      >
        其他提供商
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'AWS-Route-53' && 'hidden'"
      >
        <ol>
<li>要将 TXT 记录添加到 AWS，请参阅 <a class="link" href="https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html" rel="noopener">使用 Amazon Route 53 控制台创建记录</a>。</li>
<li>等待 TXT 记录验证，最长 72 小时。</li>
<li>记录生效后，转到 <a class="link" href="https://app.docker.com/admin" rel="noopener">Admin Console</a> 中的 <strong>Domain management</strong> 并选择 <strong>Verify</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Google-Cloud-DNS' && 'hidden'"
      >
        <ol>
<li>要将 TXT 记录添加到 Google Cloud DNS，请参阅 <a class="link" href="https://cloud.google.com/identity/docs/verify-domain-txt" rel="noopener">使用 TXT 记录验证您的域名</a>。</li>
<li>等待 TXT 记录验证，最长 72 小时。</li>
<li>记录生效后，转到 <a class="link" href="https://app.docker.com/admin" rel="noopener">Admin Console</a> 中的 <strong>Domain management</strong> 并选择 <strong>Verify</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'GoDaddy' && 'hidden'"
      >
        <ol>
<li>要将 TXT 记录添加到 GoDaddy，请参阅 <a class="link" href="https://www.godaddy.com/help/add-a-txt-record-19232" rel="noopener">添加 TXT 记录</a>。</li>
<li>等待 TXT 记录验证，最长 72 小时。</li>
<li>记录生效后，转到 <a class="link" href="https://app.docker.com/admin" rel="noopener">Admin Console</a> 中的 <strong>Domain management</strong> 并选择 <strong>Verify</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E5%85%B6%E4%BB%96%E6%8F%90%E4%BE%9B%E5%95%86' && 'hidden'"
      >
        <ol>
<li>登录您的域名主机。</li>
<li>向您的 DNS 设置添加 TXT 记录并保存该记录。</li>
<li>等待 TXT 记录验证，最长 72 小时。</li>
<li>记录生效后，转到 <a class="link" href="https://app.docker.com/admin" rel="noopener">Admin Console</a> 中的 <strong>Domain management</strong> 并选择 <strong>Verify</strong>。</li>
</ol>

      </div>
    
  </div>
</div>


## 后续步骤

- [连接 Docker 和您的 IdP](connect.md)。
- [排查](/manuals/enterprise/troubleshoot/troubleshoot-sso.md) SSO 问题。
