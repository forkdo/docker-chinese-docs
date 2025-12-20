# 连接单点登录





  
  
  
  


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



设置单点登录（SSO）连接需要同时配置 Docker 和您的身份提供商（IdP）。本指南将引导您完成在 Docker 中的设置、在 IdP 中的设置，以及最终的连接步骤。

> [!TIP]
>
> 您需要在 Docker 和 IdP 之间复制粘贴多个值。建议在一个会话中完成本指南，同时打开两个浏览器窗口分别访问 Docker 和您的 IdP。

## 支持的身份提供商

Docker 支持任何兼容 SAML 2.0 或 OIDC 的身份提供商。本指南为最常用的提供商（Okta 和 Microsoft Entra ID）提供了详细的设置说明。

如果您使用的是其他 IdP，基本流程保持一致：

1. 在 Docker 中配置连接。
1. 使用 Docker 提供的值在 IdP 中设置应用程序。
1. 将 IdP 的值输入回 Docker 以完成连接。
1. 测试连接。

## 前提条件

开始前请确保：

- 已验证您的域名
- 已在身份提供商（IdP）中设置账户
- 已完成[配置单点登录](configure.md)指南中的步骤

## 第一步：在 Docker 中创建 SSO 连接

> [!NOTE]
>
> 创建 SSO 连接前，您必须[至少验证一个域名](/manuals/enterprise/security/single-sign-on/configure.md)。

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 选择 **Create Connection** 并为连接命名。
1. 选择认证方式：**SAML** 或 **Azure AD (OIDC)**。
1. 复制 IdP 所需的值：
    - Okta SAML：**Entity ID**、**ACS URL**
    - Azure OIDC：**Redirect URL**

保持此窗口打开，以便稍后粘贴来自 IdP 的值。

## 第二步：在 IdP 中创建 SSO 连接

根据您的 IdP 提供商选择以下标签页。








<div
  class="tabs"
  
    x-data="{ selected: 'Okta-SAML' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Okta-SAML' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Okta-SAML'"
        
      >
        Okta SAML
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Entra-ID-SAML-2.0' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Entra-ID-SAML-2.0'"
        
      >
        Entra ID SAML 2.0
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Azure-Connect-OIDC' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Azure-Connect-OIDC'"
        
      >
        Azure Connect (OIDC)
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Okta-SAML' && 'hidden'"
      >
        <ol>
<li>登录 Okta 账户并打开管理员门户。</li>
<li>选择 <strong>Administration</strong>，然后选择 <strong>Create App Integration</strong>。</li>
<li>选择 <strong>SAML 2.0</strong>，然后选择 <strong>Next</strong>。</li>
<li>将应用命名为 &quot;Docker&quot;。</li>
<li>（可选）上传 Logo。</li>
<li>粘贴来自 Docker 的值：
<ul>
<li>Docker ACS URL -&gt; <strong>Single Sign On URL</strong></li>
<li>Docker Entity ID -&gt; <strong>Audience URI (SP Entity ID)</strong></li>
</ul>
</li>
<li>配置以下设置：
<ul>
<li>Name ID format: <code>EmailAddress</code></li>
<li>Application username: <code>Email</code></li>
<li>Update application on: <code>Create and update</code></li>
</ul>
</li>
<li>（可选）添加 SAML 属性。参见 
    
  
  <a class="link" href="https://docs.docker.com/enterprise/security/provisioning/#sso-attributes">SSO 属性</a>。</li>
<li>选择 <strong>Next</strong>。</li>
<li>勾选 <strong>This is an internal app that we have created</strong>。</li>
<li>选择 <strong>Finish</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Entra-ID-SAML-2.0' && 'hidden'"
      >
        <ol>
<li>登录 Microsoft Entra（原 Azure AD）。</li>
<li>选择 <strong>Default Directory</strong> &gt; <strong>Add</strong> &gt; <strong>Enterprise Application</strong>。</li>
<li>选择 <strong>Create your own application</strong>，命名为 &quot;Docker&quot;，并选择 <strong>Non-gallery</strong>。</li>
<li>创建应用后，进入 <strong>Single Sign-On</strong> 并选择 <strong>SAML</strong>。</li>
<li>在 <strong>Basic SAML configuration</strong> 部分选择 <strong>Edit</strong>。</li>
<li>编辑 <strong>Basic SAML configuration</strong> 并粘贴来自 Docker 的值：
<ul>
<li>Docker Entity ID -&gt; <strong>Identifier</strong></li>
<li>Docker ACS URL -&gt; <strong>Reply URL</strong></li>
</ul>
</li>
<li>（可选）添加 SAML 属性。参见 
    
  
  <a class="link" href="https://docs.docker.com/enterprise/security/provisioning/#sso-attributes">SSO 属性</a>。</li>
<li>保存配置。</li>
<li>在 <strong>SAML Signing Certificate</strong> 部分，下载您的 <strong>Certificate (Base64)</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Azure-Connect-OIDC' && 'hidden'"
      >
        
<h3 class=" scroll-mt-20 flex items-center gap-2" id="注册应用">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%b3%a8%e5%86%8c%e5%ba%94%e7%94%a8">
    注册应用
  </a>
</h3>

<ol>
<li>登录 Microsoft Entra（原 Azure AD）。</li>
<li>选择 <strong>App Registration</strong> &gt; <strong>New Registration</strong>。</li>
<li>将应用命名为 &quot;Docker&quot;。</li>
<li>设置账户类型并粘贴来自 Docker 的 <strong>Redirect URI</strong>。</li>
<li>选择 <strong>Register</strong>。</li>
<li>复制 <strong>Client ID</strong>。</li>
</ol>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="创建客户端密钥">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%88%9b%e5%bb%ba%e5%ae%a2%e6%88%b7%e7%ab%af%e5%af%86%e9%92%a5">
    创建客户端密钥
  </a>
</h3>

<ol>
<li>在应用中，进入 <strong>Certificates &amp; secrets</strong>。</li>
<li>选择 <strong>New client secret</strong>，填写描述并配置有效期，然后选择 <strong>Add</strong>。</li>
<li>复制新密钥的 <strong>value</strong>。</li>
</ol>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="设置-api-权限">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e8%ae%be%e7%bd%ae-api-%e6%9d%83%e9%99%90">
    设置 API 权限
  </a>
</h3>

<ol>
<li>在应用中，进入 <strong>API permissions</strong>。</li>
<li>选择 <strong>Grant admin consent</strong> 并确认。</li>
<li>选择 <strong>Add a permissions</strong> &gt; <strong>Delegated permissions</strong>。</li>
<li>搜索并选择 <code>User.Read</code>。</li>
<li>确认已授予管理员同意。</li>
</ol>

      </div>
    
  </div>
</div>


## 第三步：将 Docker 连接到 IdP

通过将 IdP 的值粘贴到 Docker 中完成集成。








<div
  class="tabs"
  
    x-data="{ selected: 'Okta-SAML' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Okta-SAML' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Okta-SAML'"
        
      >
        Okta SAML
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Entra-ID-SAML-2.0' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Entra-ID-SAML-2.0'"
        
      >
        Entra ID SAML 2.0
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Azure-Connect-OIDC' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Azure-Connect-OIDC'"
        
      >
        Azure Connect (OIDC)
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Okta-SAML' && 'hidden'"
      >
        <ol>
<li>
<p>在 Okta 中，选择您的应用并进入 <strong>View SAML setup instructions</strong>。</p>
</li>
<li>
<p>复制 <strong>SAML Sign-in URL</strong> 和 <strong>x509 Certificate</strong>。</p>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 8V12M12 16H12.01M7.8 21H16.2C17.8802 21 18.7202 21 19.362 20.673C19.9265 20.3854 20.3854 19.9265 20.673 19.362C21 18.7202 21 17.8802 21 16.2V7.8C21 6.11984 21 5.27976 20.673 4.63803C20.3854 4.07354 19.9265 3.6146 19.362 3.32698C18.7202 3 17.8802 3 16.2 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Important
      </span>
    </div>
    <div class="admonition-content">
      <p>请复制整个证书，包括 <code>----BEGIN CERTIFICATE----</code> 和 <code>----END CERTIFICATE----</code> 行。</p>
    </div>
  </blockquote>

</li>
<li>
<p>返回 Docker Admin Console。</p>
</li>
<li>
<p>粘贴 <strong>SAML Sign-in URL</strong> 和 <strong>x509 Certificate</strong> 的值。</p>
</li>
<li>
<p>（可选）选择默认团队。</p>
</li>
<li>
<p>检查后选择 <strong>Create connection</strong>。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Entra-ID-SAML-2.0' && 'hidden'"
      >
        <ol>
<li>
<p>用文本编辑器打开下载的 <strong>Certificate (Base64)</strong>。</p>
</li>
<li>
<p>复制以下值：</p>
<ul>
<li>来自 Azure AD 的：<strong>Login URL</strong></li>
<li><strong>Certificate (Base64)</strong> 内容</li>
</ul>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 8V12M12 16H12.01M7.8 21H16.2C17.8802 21 18.7202 21 19.362 20.673C19.9265 20.3854 20.3854 19.9265 20.673 19.362C21 18.7202 21 17.8802 21 16.2V7.8C21 6.11984 21 5.27976 20.673 4.63803C20.3854 4.07354 19.9265 3.6146 19.362 3.32698C18.7202 3 17.8802 3 16.2 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Important
      </span>
    </div>
    <div class="admonition-content">
      <p>请复制整个证书，包括 <code>----BEGIN CERTIFICATE----</code> 和 <code>----END CERTIFICATE----</code> 行。</p>
    </div>
  </blockquote>

</li>
<li>
<p>返回 Docker Admin Console。</p>
</li>
<li>
<p>粘贴 <strong>Login URL</strong> 和 <strong>Certificate (Base64)</strong> 的值。</p>
</li>
<li>
<p>（可选）选择默认团队。</p>
</li>
<li>
<p>检查后选择 <strong>Create connection</strong>。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Azure-Connect-OIDC' && 'hidden'"
      >
        <ol>
<li>返回 Docker Admin Console。</li>
<li>粘贴以下值：
<ul>
<li><strong>Client ID</strong></li>
<li><strong>Client Secret</strong></li>
<li><strong>Azure AD Domain</strong></li>
</ul>
</li>
<li>（可选）选择默认团队。</li>
<li>检查后选择 <strong>Create connection</strong>。</li>
</ol>

      </div>
    
  </div>
</div>


## 第四步：测试连接

1. 打开一个无痕浏览器窗口。
1. 使用您的**域名邮箱地址**登录 Admin Console。
1. 浏览器将重定向到您的身份提供商的登录页面进行认证。如果您有[多个 IdP](#optional-configure-multiple-idps)，请选择 **Continue with SSO** 登录选项。
1. 通过域名邮箱认证，而非使用 Docker ID。

如果您使用 CLI，则必须使用个人访问令牌进行认证。

## 可选：配置多个 IdP

Docker 支持多个 IdP 配置。要为同一域名使用多个 IdP：

- 对每个 IdP 重复本页的步骤 1-4。
- 每个连接必须使用相同的域名。
- 用户登录时选择 **Continue with SSO** 以选择其 IdP。

## 可选：强制启用 SSO

> [!IMPORTANT]
>
> 如果未强制启用 SSO，用户仍可使用 Docker 用户名和密码登录。

强制启用 SSO 后，用户在登录 Docker 时必须使用 SSO。这将集中认证流程，并强制执行 IdP 设置的策略。

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织或公司。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 SSO 连接表中，选择 **Action** 菜单，然后选择 **Enable enforcement**。
1. 按照屏幕上的说明操作。
1. 选择 **Turn on enforcement**。

启用 SSO 强制策略后，用户将无法修改其邮箱地址和密码、将用户账户转换为组织，或通过 Docker Hub 设置 2FA。如果您希望使用 2FA，则必须通过 IdP 启用 2FA。

## 后续步骤

- [配置用户预配](/manuals/enterprise/security/provisioning/_index.md)。
- [强制登录](../enforce-sign-in/_index.md)。
- [创建个人访问令牌](/manuals/enterprise/security/access-tokens.md)。
- [排查 SSO 问题](/manuals/enterprise/troubleshoot/troubleshoot-sso.md)。
