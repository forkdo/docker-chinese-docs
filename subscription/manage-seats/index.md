# 管理订阅席位

您可以随时为 Docker Team 或 Business 订阅添加或移除席位，以适应团队变动。在计费周期中途添加席位时，系统会按额外席位的比例收取费用。



> [!重要]
>
> 对于美国客户，Docker 已于 2024 年 7 月 1 日开始征收销售税。
> 对于欧洲客户，Docker 已于 2025 年 3 月 1 日开始征收增值税 (VAT)。
> 对于英国客户，Docker 已于 2025 年 5 月 1 日开始征收增值税 (VAT)。
>
> 为确保税费计算准确，请确保您的[账单信息](/billing/details/)以及 VAT/税号（如适用）已更新。如果您免征销售税，请参阅[注册税务证明](/billing/tax-certificate/)。

## 为订阅添加席位








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
      <p>如果您使用的是销售协助的 Docker Business 订阅，请联系您的客户经理来添加席位。</p>
    </div>
  </blockquote>

<p>添加席位的方法如下：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</li>
<li>选择 <strong>Billing</strong>。</li>
<li>选择 <strong>Add seats</strong> 并按照屏幕上的说明完成席位添加。请注意，购买额外席位时不能使用发票支付，必须使用信用卡或美国银行账户。</li>
</ol>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Note
      </span>
    </div>
    <div class="admonition-content">
      <p>如果您选择使用美国银行账户支付，则必须验证账户。更多信息，请参阅 <a class="link" href="/billing/payment-method/#verify-a-bank-account">验证银行账户</a>。</p>
    </div>
  </blockquote>

<p>现在您可以向组织中添加更多成员。更多信息，请参阅 <a class="link" href="/admin/organization/members/">管理组织成员</a>。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Legacy-Docker-subscription' && 'hidden'"
      >
        

  

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
      <p>如果您使用的是销售协助的 Docker Business 订阅，请联系您的客户经理来添加席位。</p>
    </div>
  </blockquote>

<p>为 Legacy Docker 订阅添加席位的方法如下：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</li>
<li>选择您的组织，然后选择 <strong>Billing</strong>。</li>
<li>在 Billing 页面，选择 <strong>Add seats</strong>。</li>
<li>选择您要添加的席位数量，然后选择 <strong>Purchase</strong>。</li>
</ol>
<p>为 Docker Build Cloud 添加席位的方法如下：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com" rel="noopener">Docker Home</a> 并选择 <strong>Build Cloud</strong>。</li>
<li>选择 <strong>Account settings</strong>，然后选择 <strong>Add seats</strong>。</li>
<li>选择您要添加的席位数量，然后选择 <strong>Add seats</strong>。</li>
</ol>

      </div>
    
  </div>
</div>


## 批量定价

Docker 为 Docker Business 订阅提供批量定价，起订量为 25 个席位。请联系 [Docker 销售团队](https://www.docker.com/pricing/contact-sales/) 获取更多信息。

## 从订阅中移除席位

您可以随时从 Team 或 Business 订阅中移除席位。变更将在下一个计费周期生效，未使用的部分不予退款。

例如，如果您每月 8 日为 10 个席位付费，并在 15 日移除了 2 个席位，则这 2 个席位仍可使用，直到下一个计费周期开始。从下一个计费周期开始，您将只需支付 8 个席位的费用。








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
      <p>如果您使用的是销售协助的 Docker Business 订阅，请联系您的客户经理来移除席位。</p>
    </div>
  </blockquote>

<p>移除席位的方法如下：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</li>
<li>选择 <strong>Billing</strong>。</li>
<li>在 <strong>Seats</strong> 行中，选择操作图标，然后选择 <strong>Remove seats</strong>。</li>
<li>按照屏幕上的说明完成席位移除。</li>
</ol>
<p>在下一个计费周期开始之前，您可以取消席位移除操作。如需取消，请选择 <strong>Cancel change</strong>。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Legacy-Docker-subscription' && 'hidden'"
      >
        

  

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
      <p>如果您使用的是销售协助的 Docker Business 订阅，请联系您的客户经理来移除席位。</p>
    </div>
  </blockquote>

<p>从 Legacy Docker 订阅中移除席位的方法如下：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</li>
<li>选择您的组织，然后选择 <strong>Billing</strong>。</li>
<li>在 Billing 页面，选择 <strong>Remove seats</strong>。</li>
<li>按照屏幕上的说明完成席位移除。</li>
</ol>
<p>从 Docker Build Cloud 中移除席位的方法如下：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com" rel="noopener">Docker Home</a> 并选择 <strong>Build Cloud</strong>。</li>
<li>选择 <strong>Account settings</strong>，然后选择 <strong>Remove seats</strong>。</li>
<li>按照屏幕上的说明完成席位移除。</li>
</ol>

      </div>
    
  </div>
</div>

