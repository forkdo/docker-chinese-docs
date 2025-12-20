# 更改您的订阅



> [!重要]
>
> 对于美国客户，Docker 已于 2024 年 7 月 1 日开始征收销售税。
> 对于欧洲客户，Docker 已于 2025 年 3 月 1 日开始征收增值税 (VAT)。
> 对于英国客户，Docker 已于 2025 年 5 月 1 日开始征收增值税 (VAT)。
>
> 为确保税费计算准确，请确保您的[账单信息](/billing/details/)以及 VAT/税号（如适用）已更新。如果您免征销售税，请参阅[注册税务证明](/billing/tax-certificate/)。

您可以随时升级或降级您的 Docker 订阅，以满足不断变化的需求。本页介绍如何更改订阅，以及账单和功能访问方面会发生什么变化。

> [!NOTE]
>
> 旧版 Docker 订阅者更改订阅的界面有所不同。旧版订阅适用于在 2024 年 12 月 10 日之前最后一次购买或续订的订阅者。有关详细信息，请参阅[宣布升级后的 Docker 计划](https://www.docker.com/blog/november-2024-updated-plans-announcement/)。

## 升级您的订阅

当您升级 Docker 订阅时，您将立即获得新订阅层级中的所有功能和权益。有关详细的功能信息，请参阅 [Docker 定价](https://www.docker.com/pricing)。








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-%E8%AE%A2%E9%98%85' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-%E8%AE%A2%E9%98%85' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-%E8%AE%A2%E9%98%85'"
        
      >
        Docker 订阅
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E6%97%A7%E7%89%88-Docker-%E8%AE%A2%E9%98%85' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%97%A7%E7%89%88-Docker-%E8%AE%A2%E9%98%85'"
        
      >
        旧版 Docker 订阅
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-%E8%AE%A2%E9%98%85' && 'hidden'"
      >
        <p>要升级您的订阅：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您要升级的组织。</li>
<li>选择 <strong>Billing</strong>（账单）。</li>
<li>（可选）如果您要从免费的 Personal 订阅升级到 Team 订阅并希望保留您的用户名，请<a class="link" href="/admin/organization/convert-account/">将您的用户帐户转换为组织</a>。</li>
<li>选择 <strong>Upgrade</strong>（升级）。</li>
<li>按照屏幕上的说明完成升级。</li>
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
      <p>如果您选择使用美国银行帐户付款，则必须验证该帐户。有关更多信息，请参阅<a class="link" href="/billing/payment-method/#verify-a-bank-account">验证银行帐户</a>。</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%97%A7%E7%89%88-Docker-%E8%AE%A2%E9%98%85' && 'hidden'"
      >
        <p>要将您的旧版 Docker 订阅升级为包含所有工具访问权限的新版 Docker 订阅，请联系 <a class="link" href="https://www.docker.com/pricing/contact-sales/" rel="noopener">Docker 销售团队</a>。</p>

      </div>
    
  </div>
</div>


## 降级您的订阅

您可以在续订日期之前的任何时间降级您的 Docker 订阅。未使用的部分不予退款，但您在下一个计费周期之前仍可继续使用付费功能。

### 降级注意事项

在降级之前，请考虑以下几点：

- **团队规模和仓库**：您可能需要减少团队成员，并根据新订阅的限制将私有仓库转换为公共仓库或删除它们。
- **SSO 和 SCIM**：如果您要从 Docker Business 降级，并且您的组织使用了单点登录 (SSO)，请先移除您的 SSO 连接和已验证的域名。通过 SCIM 自动配置的组织成员需要重置其密码才能在没有 SSO 的情况下登录。
- **私有仓库协作者**：个人订阅不包含私有仓库的协作者。当从 Pro 降级到 Personal 时，所有协作者都会被移除，额外的私有仓库将被锁定。

有关每个层级的功能限制，请参阅 [Docker 定价](https://www.docker.com/pricing)。








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-%E8%AE%A2%E9%98%85' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-%E8%AE%A2%E9%98%85' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-%E8%AE%A2%E9%98%85'"
        
      >
        Docker 订阅
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E6%97%A7%E7%89%88-Docker-%E8%AE%A2%E9%98%85' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%97%A7%E7%89%88-Docker-%E8%AE%A2%E9%98%85'"
        
      >
        旧版 Docker 订阅
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-%E8%AE%A2%E9%98%85' && 'hidden'"
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
      <p>如果您拥有通过销售协助购买的 Docker Business 订阅，请联系您的客户经理以降级您的订阅。</p>
    </div>
  </blockquote>

<p>要降级您的订阅：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您要降级的组织。</li>
<li>选择 <strong>Billing</strong>（账单）。</li>
<li>选择操作图标，然后选择 <strong>Cancel subscription</strong>（取消订阅）。</li>
<li>填写反馈调查以继续取消。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%97%A7%E7%89%88-Docker-%E8%AE%A2%E9%98%85' && 'hidden'"
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
      <p>如果您拥有通过销售协助购买的 Docker Business 订阅，请联系您的客户经理以降级您的订阅。</p>
    </div>
  </blockquote>

<p>要降级您的旧版 Docker 订阅：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com/billing" rel="noopener">Docker Hub</a>。</li>
<li>选择您要降级的组织，然后选择 <strong>Billing</strong>（账单）。</li>
<li>要降级，您必须导航到升级计划页面。选择 <strong>Upgrade</strong>（升级）。</li>
<li>在升级页面上，在 <strong>Free Team</strong> 计划卡片中选择 <strong>Downgrade</strong>（降级）。</li>
<li>按照屏幕上的说明完成降级。</li>
</ol>
<p>要降级您的 Docker Build Cloud 订阅：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com" rel="noopener">Docker Home</a> 并选择 <strong>Build Cloud</strong>。</li>
<li>选择 <strong>Account settings</strong>（帐户设置），然后选择 <strong>Downgrade</strong>（降级）。</li>
<li>要确认降级，请在文本字段中输入 <strong>DOWNGRADE</strong>，然后选择 <strong>Yes, continue</strong>（是，继续）。</li>
<li>帐户设置页面将更新一个通知栏，告知您的降级日期（下一个计费周期开始时）。</li>
</ol>

      </div>
    
  </div>
</div>


## 订阅暂停政策

您无法暂停或延迟订阅。如果订阅发票在到期日未支付，则从到期日开始有 15 天的宽限期。
