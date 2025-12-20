# 管理您的账单信息

您可以更新个人账户或组织的账单信息。当您更新账单信息时，这些更改将应用于未来的账单发票。您为账单账户提供的电子邮件地址是 Docker 发送所有发票和其他账单相关通信的位置。

> [!NOTE]
>
> 现有的发票（无论已支付或未支付）无法更新。
> 更改仅适用于未来的发票。



> [!重要]
>
> 对于美国客户，Docker 已于 2024 年 7 月 1 日开始征收销售税。
> 对于欧洲客户，Docker 已于 2025 年 3 月 1 日开始征收增值税 (VAT)。
> 对于英国客户，Docker 已于 2025 年 5 月 1 日开始征收增值税 (VAT)。
>
> 为确保税费计算准确，请确保您的[账单信息](/billing/details/)以及 VAT/税号（如适用）已更新。如果您免征销售税，请参阅[注册税务证明](/billing/tax-certificate/)。

## 管理账单信息

### 个人账户








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-subscription' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-subscription' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-subscription'"
        
      >
        Docker subscription
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Legacy-Docker-subscription' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Legacy-Docker-subscription'"
        
      >
        Legacy Docker subscription
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-subscription' && 'hidden'"
      >
        <p>要更新您的账单信息：</p>
<ol>
<li>
<p>登录到 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</p>
</li>
<li>
<p>选择 <strong>Billing</strong>。</p>
</li>
<li>
<p>从左侧导航中选择 <strong>Billing information</strong>。</p>
</li>
<li>
<p>在您的账单信息卡片上，选择 <strong>Change</strong>。</p>
</li>
<li>
<p>更新您的账单联系人和账单地址信息。</p>
</li>
<li>
<p>可选。要添加或更新增值税号（VAT ID），请选中 <strong>I'm purchasing as a business</strong> 复选框并输入您的税务 ID。</p>


  

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
      <p>您的增值税号必须包含国家前缀。例如，如果您为德国输入增值税号，应输入 <code>DE123456789</code>。</p>
    </div>
  </blockquote>

</li>
<li>
<p>选择 <strong>Update</strong>。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Legacy-Docker-subscription' && 'hidden'"
      >
        <p>要更新您的账单信息：</p>
<ol>
<li>
<p>登录到 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</p>
</li>
<li>
<p>选择您的组织，然后选择 <strong>Billing</strong>。</p>
</li>
<li>
<p>选择 <strong>Billing Address</strong> 并输入您的更新后的账单信息。</p>
</li>
<li>
<p>可选。要添加或更新增值税号（VAT ID），请输入您的 <strong>Tax ID/VAT</strong>。</p>


  

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
      <p>您的增值税号必须包含国家前缀。例如，如果您为德国输入增值税号，应输入 <code>DE123456789</code>。</p>
    </div>
  </blockquote>

</li>
<li>
<p>选择 <strong>Submit</strong>。</p>
</li>
</ol>

      </div>
    
  </div>
</div>


### 组织

> [!NOTE]
>
> 您必须是组织所有者才能更改账单信息。








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-subscription' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-subscription' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-subscription'"
        
      >
        Docker subscription
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Legacy-Docker-subscription' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Legacy-Docker-subscription'"
        
      >
        Legacy Docker subscription
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-subscription' && 'hidden'"
      >
        <p>要更新您的账单信息：</p>
<ol>
<li>
<p>登录到 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</p>
</li>
<li>
<p>选择 <strong>Billing</strong>。</p>
</li>
<li>
<p>从左侧导航中选择 <strong>Billing information</strong>。</p>
</li>
<li>
<p>在您的账单信息卡片上，选择 <strong>Change</strong>。</p>
</li>
<li>
<p>更新您的账单联系人和账单地址信息。</p>
</li>
<li>
<p>可选。要添加或更新增值税号（VAT ID），请选中 <strong>I'm purchasing as a business</strong> 复选框并输入您的税务 ID。</p>


  

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
      <p>您的增值税号必须包含国家前缀。例如，如果您为德国输入增值税号，应输入 <code>DE123456789</code>。</p>
    </div>
  </blockquote>

</li>
<li>
<p>选择 <strong>Update</strong>。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Legacy-Docker-subscription' && 'hidden'"
      >
        <p>要更新您的账单信息：</p>
<ol>
<li>
<p>登录到 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</p>
</li>
<li>
<p>选择您的组织，然后选择 <strong>Billing</strong>。</p>
</li>
<li>
<p>选择 <strong>Billing Address</strong>。</p>
</li>
<li>
<p>可选。要添加或更新增值税号（VAT ID），请输入您的 <strong>Tax ID/VAT</strong>。</p>


  

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
      <p>您的增值税号必须包含国家前缀。例如，如果您为德国输入增值税号，应输入 <code>DE123456789</code>。</p>
    </div>
  </blockquote>

</li>
<li>
<p>选择 <strong>Submit</strong>。</p>
</li>
</ol>

      </div>
    
  </div>
</div>


## 更新您的账单邮箱地址

Docker 会发送以下与账单相关的电子邮件：

- 确认邮件（新订阅、已支付发票）
- 通知邮件（卡片失败、卡片过期）
- 提醒邮件（订阅续订）

您可以随时更新接收账单发票的电子邮件地址。

### 个人账户








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-subscription' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-subscription' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-subscription'"
        
      >
        Docker subscription
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Legacy-Docker-subscription' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Legacy-Docker-subscription'"
        
      >
        Legacy Docker subscription
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-subscription' && 'hidden'"
      >
        <p>要更新您的账单邮箱地址：</p>
<ol>
<li>登录到 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</li>
<li>选择 <strong>Billing</strong>。</li>
<li>从左侧导航中选择 <strong>Billing information</strong>。</li>
<li>在您的账单信息卡片上，选择 <strong>Change</strong>。</li>
<li>更新您的账单联系人信息并选择 <strong>Update</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Legacy-Docker-subscription' && 'hidden'"
      >
        <p>要更新您的账单邮箱地址：</p>
<ol>
<li>登录到 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</li>
<li>选择您的组织，然后选择 <strong>Billing</strong>。</li>
<li>选择 <strong>Billing Address</strong>。</li>
<li>在 <strong>Billing contact</strong> 部分更新邮箱地址。</li>
<li>选择 <strong>Submit</strong>。</li>
</ol>

      </div>
    
  </div>
</div>


### 组织








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-subscription' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-subscription' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-subscription'"
        
      >
        Docker subscription
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Legacy-Docker-subscription' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Legacy-Docker-subscription'"
        
      >
        Legacy Docker subscription
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-subscription' && 'hidden'"
      >
        <p>要更新您的账单邮箱地址：</p>
<ol>
<li>登录到 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</li>
<li>选择 <strong>Billing</strong>。</li>
<li>从左侧导航中选择 <strong>Billing information</strong>。</li>
<li>在您的账单信息卡片上，选择 <strong>Change</strong>。</li>
<li>更新您的账单联系人信息并选择 <strong>Update</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Legacy-Docker-subscription' && 'hidden'"
      >
        <p>要更新您的账单邮箱地址：</p>
<ol>
<li>登录到 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</li>
<li>选择您的组织，然后选择 <strong>Billing</strong>。</li>
<li>选择组织名称。</li>
<li>选择 <strong>Billing Address</strong>。</li>
<li>在 <strong>Billing contact</strong> 部分更新邮箱地址。</li>
<li>选择 <strong>Submit</strong>。</li>
</ol>

      </div>
    
  </div>
</div>

