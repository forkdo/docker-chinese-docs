# 更改账单周期

购买订阅时，您可以在月度或年度账单周期之间进行选择。如果您当前是月度账单周期，可以选择切换到年度账单周期。

如果您使用的是月度计划，可以随时切换到年度计划。但是，不支持从年度计划切换到月度计划。

当您更改账单周期时：

- 您的下一个账单日期将反映新的周期。要查找下一个账单日期，请参阅[查看续订日期](history.md#view-renewal-date)。
- 您的订阅开始日期将重置。例如，如果月度订阅从 3 月 1 日开始，到 4 月 1 日结束，那么在 2024 年 3 月 15 日切换账单周期时，新的开始日期将重置为 2024 年 3 月 15 日，结束日期为 2025 年 3 月 15 日。
- 月度订阅中任何未使用的部分将按比例折算，并作为信用额度用于年度订阅。例如，如果您的月度费用为 10 美元，您的已使用价值为 5 美元，当您切换到年度周期（100 美元）时，最终费用为 95 美元（100 美元 - 5 美元）。



> [!重要]
>
> 对于美国客户，Docker 已于 2024 年 7 月 1 日开始征收销售税。
> 对于欧洲客户，Docker 已于 2025 年 3 月 1 日开始征收增值税 (VAT)。
> 对于英国客户，Docker 已于 2025 年 5 月 1 日开始征收增值税 (VAT)。
>
> 为确保税费计算准确，请确保您的[账单信息](/billing/details/)以及 VAT/税号（如适用）已更新。如果您免征销售税，请参阅[注册税务证明](/billing/tax-certificate/)。

## 将个人账户更改为年度周期








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
      <p>订阅升级或更改不支持通过发票付款。</p>
    </div>
  </blockquote>

<p>更改账单周期的步骤：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</li>
<li>选择 <strong>Billing</strong>（账单）。</li>
<li>在计划和用量页面上，选择 <strong>Switch to annual billing</strong>（切换到年度账单）。</li>
<li>验证您的账单信息。</li>
<li>选择 <strong>Continue to payment</strong>（继续付款）。</li>
<li>验证付款信息并选择 <strong>Upgrade subscription</strong>（升级订阅）。</li>
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
      <p>如果您选择使用美国银行账户付款，则必须验证该账户。有关更多信息，请参阅<a class="link" href="/billing/payment-method/#verify-a-bank-account">验证银行账户</a>。</p>
    </div>
  </blockquote>

<p>计划和用量页面现在将显示您的新年度计划详细信息。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Legacy-Docker-subscription' && 'hidden'"
      >
        <p>请按照以下步骤将旧版 Docker 订阅从月度切换到年度账单周期：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</li>
<li>选择您的组织，然后选择 <strong>Billing</strong>（账单）。</li>
<li>在 <strong>Plan</strong>（计划）选项卡的右下角，选择 <strong>Switch to annual billing</strong>（切换到年度账单）。</li>
<li>查看 <strong>Change to an Annual subscription</strong>（更改为年度订阅）页面上显示的信息，然后选择 <strong>Accept Terms and Purchase</strong>（接受条款并购买）进行确认。</li>
</ol>

      </div>
    
  </div>
</div>


## 将组织更改为年度周期

您必须是组织所有者才能更改付款信息。








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
      <p>订阅升级或更改不支持通过发票付款。</p>
    </div>
  </blockquote>

<p>请按照以下步骤将组织的 Docker 订阅从月度切换到年度账单周期：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</li>
<li>选择 <strong>Billing</strong>（账单）。</li>
<li>在计划和用量页面上，选择 <strong>Switch to annual billing</strong>（切换到年度账单）。</li>
<li>验证您的账单信息。</li>
<li>选择 <strong>Continue to payment</strong>（继续付款）。</li>
<li>验证付款信息并选择 <strong>Upgrade subscription</strong>（升级订阅）。</li>
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
      <p>如果您选择使用美国银行账户付款，则必须验证该账户。有关更多信息，请参阅<a class="link" href="/billing/payment-method/#verify-a-bank-account">验证银行账户</a>。</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Legacy-Docker-subscription' && 'hidden'"
      >
        <p>请按照以下步骤将旧版 Docker 组织订阅从月度切换到年度账单周期：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</li>
<li>选择您的组织，然后选择 <strong>Billing</strong>（账单）。</li>
<li>选择 <strong>Switch to annual billing</strong>（切换到年度账单）。</li>
<li>查看 <strong>Change to an Annual subscription</strong>（更改为年度订阅）页面上显示的信息，然后选择 <strong>Accept Terms and Purchase</strong>（接受条款并购买）进行确认。</li>
</ol>

      </div>
    
  </div>
</div>

