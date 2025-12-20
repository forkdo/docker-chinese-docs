# 发票和账单历史记录

了解如何查看和支付发票、查看账单历史记录以及核实账单续订日期。所有月度和年度订阅都会在订阅期结束时使用您的默认支付方式自动续订。



> [!重要]
>
> 对于美国客户，Docker 已于 2024 年 7 月 1 日开始征收销售税。
> 对于欧洲客户，Docker 已于 2025 年 3 月 1 日开始征收增值税 (VAT)。
> 对于英国客户，Docker 已于 2025 年 5 月 1 日开始征收增值税 (VAT)。
>
> 为确保税费计算准确，请确保您的[账单信息](/billing/details/)以及 VAT/税号（如适用）已更新。如果您免征销售税，请参阅[注册税务证明](/billing/tax-certificate/)。

## 查看发票

您的发票包含以下内容：

- 发票编号
- 签发日期
- 到期日
- 您的“账单接收方”信息
- 应付金额（美元）
- 在线支付：选择此链接在线支付发票
- 订单描述、适用时的单位、单价和金额（美元）
- 小计、折扣（如适用）和总计

发票“账单接收方”部分列出的信息基于您的账单信息。并非所有字段都是必填项。账单信息包括：

- 姓名（必填）：管理员或公司的名称
- 地址（必填）
- 电子邮件地址（必填）：接收账户所有与账单相关邮件的电子邮件地址
- 电话号码
- 税号或增值税号

您无法修改已支付或未支付的账单发票。当您更新账单信息时，此更改不会更新现有发票。

如果您需要更新账单信息，请确保在订阅续订日期之前完成，此时您的发票已最终确定。

更多信息，请参阅[更新账单信息](details.md)。

## 支付发票

> [!NOTE]
>
> 仅年度账单周期的订阅者可以使用发票支付。要更改您的账单周期，请参阅[更改账单周期](/manuals/billing/cycle.md)。

如果您已为订阅选择发票支付，您将在到期日前 10 天、到期日当天以及到期日后 15 天收到支付发票的电子邮件提醒。

您可以通过 Docker 账单控制台支付发票：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Billing**（账单）。
3. 选择 **Invoices**（发票）并找到您要支付的发票。
4. 在 **Actions**（操作）列中，选择 **Pay invoice**（支付发票）。
5. 填写您的支付详细信息，然后选择 **Pay**（支付）。

当您的支付处理完毕后，发票的 **Status**（状态）列将更新为 **Paid**（已支付），您将收到一封确认邮件。

如果您选择使用美国银行账户支付，则必须验证该账户。更多信息，请参阅[验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。

### 查看续订日期








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
        <p>您会在订阅续订时收到发票。要核实您的续订日期，请登录 <a class="link" href="https://app.docker.com/billing" rel="noopener">Docker Home 账单</a>。您的续订日期和金额会显示在订阅计划卡片上。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Legacy-Docker-subscription' && 'hidden'"
      >
        <p>您会在订阅续订时收到发票。要核实您的续订日期：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</li>
<li>选择您的用户头像以打开下拉菜单。</li>
<li>选择 <strong>Billing</strong>（账单）。</li>
<li>选择用户或组织账户以查看账单详细信息。在此处您可以找到您的续订日期和续订金额。</li>
</ol>

      </div>
    
  </div>
</div>


## 在发票上包含您的增值税号

> [!NOTE]
>
> 如果增值税号字段不可用，请填写[联系支持表单](https://hub.docker.com/support/contact/)。此字段可能需要手动添加。








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
        <p>要添加或更新您的增值税号：</p>
<ol>
<li>
<p>登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</p>
</li>
<li>
<p>选择 <strong>Billing</strong>（账单）。</p>
</li>
<li>
<p>从左侧菜单中选择 <strong>Billing information</strong>（账单信息）。</p>
</li>
<li>
<p>在您的账单信息卡片上选择 <strong>Change</strong>（更改）。</p>
</li>
<li>
<p>确保选中 <strong>I'm purchasing as a business</strong>（我是以企业身份购买）复选框。</p>
</li>
<li>
<p>在税号部分输入您的增值税号。</p>


  

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
      <p>您的增值税号必须包含国家/地区前缀。例如，如果您要输入德国的增值税号，则应输入 <code>DE123456789</code>。</p>
    </div>
  </blockquote>

</li>
<li>
<p>选择 <strong>Update</strong>（更新）。</p>
</li>
</ol>
<p>您的增值税号将包含在您的下一张发票上。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Legacy-Docker-subscription' && 'hidden'"
      >
        <p>要添加或更新您的增值税号：</p>
<ol>
<li>
<p>登录 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</p>
</li>
<li>
<p>选择您的组织，然后选择 <strong>Billing</strong>（账单）。</p>
</li>
<li>
<p>选择 <strong>Billing address</strong>（账单地址）链接。</p>
</li>
<li>
<p>在 <strong>Billing Information</strong>（账单信息）部分，选择 <strong>Update information</strong>（更新信息）。</p>
</li>
<li>
<p>在税号部分输入您的增值税号。</p>


  

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
      <p>您的增值税号必须包含国家/地区前缀。例如，如果您要输入德国的增值税号，则应输入 <code>DE123456789</code>。</p>
    </div>
  </blockquote>

</li>
<li>
<p>选择 <strong>Save</strong>（保存）。</p>
</li>
</ol>
<p>您的增值税号将包含在您的下一张发票上。</p>

      </div>
    
  </div>
</div>


## 查看账单历史记录

您可以查看个人账户或组织的账单历史记录并下载过去的发票。

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
        <p>要查看账单历史记录：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</li>
<li>选择 <strong>Billing</strong>（账单）。</li>
<li>从左侧菜单中选择 <strong>Invoices</strong>（发票）。</li>
<li>（可选）选择 <strong>Invoice number</strong>（发票编号）以打开发票详情。</li>
<li>（可选）选择 <strong>Download</strong>（下载）按钮以下载发票。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Legacy-Docker-subscription' && 'hidden'"
      >
        <p>要查看账单历史记录：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</li>
<li>选择您的组织，然后选择 <strong>Billing</strong>（账单）。</li>
<li>选择 <strong>Payment methods and billing history</strong>（支付方式和账单历史记录）链接。</li>
</ol>
<p>您可以在 <strong>Invoice History</strong>（发票历史记录）部分找到过去的发票，并可以下载发票。</p>

      </div>
    
  </div>
</div>


### 组织

您必须是组织的所有者才能查看账单历史记录。








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
        <p>要查看账单历史记录：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</li>
<li>选择 <strong>Billing</strong>（账单）。</li>
<li>从左侧菜单中选择 <strong>Invoices</strong>（发票）。</li>
<li>（可选）选择 <strong>invoice number</strong>（发票编号）以打开发票详情。</li>
<li>（可选）选择 <strong>download</strong>（下载）按钮以下载发票。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Legacy-Docker-subscription' && 'hidden'"
      >
        <p>要查看账单历史记录：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</li>
<li>选择您的组织，然后选择 <strong>Billing</strong>（账单）。</li>
<li>选择 <strong>Payment methods and billing history</strong>（支付方式和账单历史记录）链接。</li>
</ol>
<p>您可以在 <strong>Invoice History</strong>（发票历史记录）部分找到过去的发票，并可以下载发票。</p>

      </div>
    
  </div>
</div>

