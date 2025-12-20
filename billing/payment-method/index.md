# 添加或更新支付方式

本文介绍如何为您的个人账户或组织添加或更新支付方式。

您可以随时添加支付方式或更新账户现有的支付方式。

> [!重要]
>
> 如果要移除所有支付方式，您必须先将订阅降级为免费订阅。请参阅[降级](../subscription/change.md)。

支持的支付方式如下：

- 银行卡
  - Visa
  - MasterCard
  - American Express
  - Discover
  - JCB
  - Diners
  - UnionPay
- 电子钱包
  - Stripe Link
- 银行账户
  - 通过[已验证](manuals/billing/payment-method.md#verify-a-bank-account)的美国银行账户进行自动清算所 (ACH) 转账
- [发票付款](/manuals/billing/history.md)

所有费用均以美元 (USD) 计价。



> [!重要]
>
> 对于美国客户，Docker 已于 2024 年 7 月 1 日开始征收销售税。
> 对于欧洲客户，Docker 已于 2025 年 3 月 1 日开始征收增值税 (VAT)。
> 对于英国客户，Docker 已于 2025 年 5 月 1 日开始征收增值税 (VAT)。
>
> 为确保税费计算准确，请确保您的[账单信息](/billing/details/)以及 VAT/税号（如适用）已更新。如果您免征销售税，请参阅[注册税务证明](/billing/tax-certificate/)。

## 管理支付方式

### 个人账户








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
        <p>添加支付方式：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</li>
<li>选择<strong>计费</strong>。</li>
<li>从左侧菜单中选择<strong>支付方式</strong>。</li>
<li>选择<strong>添加支付方式</strong>。</li>
<li>输入新的支付信息：
<ul>
<li>添加银行卡：
<ul>
<li>选择<strong>银行卡</strong>并填写银行卡信息表单。</li>
</ul>
</li>
<li>添加 Link 支付：
<ul>
<li>选择<strong>使用 Link 安全一键结账</strong>，并输入您的 Link <strong>电子邮箱地址</strong>和<strong>手机号码</strong>。</li>
<li>如果您还不是 Link 用户，则必须填写银行卡信息表单以存储用于 Link 支付的银行卡。</li>
</ul>
</li>
<li>添加银行账户：
<ul>
<li>选择<strong>美国银行账户</strong>。</li>
<li>验证您的<strong>电子邮箱</strong>和<strong>全名</strong>。</li>
<li>如果您的银行在列表中，请选择您的银行名称。</li>
<li>如果您的银行不在列表中，请选择<strong>搜索您的银行</strong>。</li>
<li>要验证银行账户，请参阅<a class="link" href="/billing/payment-method/#verify-a-bank-account">验证银行账户</a>。</li>
</ul>
</li>
</ul>
</li>
<li>选择<strong>添加支付方式</strong>。</li>
<li>可选。您可以通过选择<strong>设为默认</strong>操作来设置新的默认支付方式。</li>
<li>可选。您可以通过选择<strong>删除</strong>操作来移除非默认支付方式。</li>
</ol>


  

<blockquote
  
  class="admonition not-prose">
  <p>[!注意]</p>
<p>如果要将美国银行账户设为默认支付方式，您必须先<a class="link" href="#verify-a-bank-account">验证该账户</a>。</p>

  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%97%A7%E7%89%88-Docker-%E8%AE%A2%E9%98%85' && 'hidden'"
      >
        <p>添加支付方式：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</li>
<li>选择<strong>计费</strong>。</li>
<li>选择<strong>支付方式</strong>链接。</li>
<li>选择<strong>添加支付方式</strong>。</li>
<li>输入新的支付信息：
<ul>
<li>添加银行卡：
<ul>
<li>选择<strong>银行卡</strong>并填写银行卡信息表单。</li>
</ul>
</li>
<li>添加 Link 支付：
<ul>
<li>选择<strong>使用 Link 安全一键结账</strong>，并输入您的 Link <strong>电子邮箱地址</strong>和<strong>手机号码</strong>。</li>
<li>如果您还不是 Link 用户，则必须填写银行卡信息表单以存储用于 Link 支付的银行卡。</li>
</ul>
</li>
</ul>
</li>
<li>选择<strong>添加</strong>。</li>
<li>选择<strong>操作</strong>图标，然后选择<strong>设为默认</strong>，以确保您的新支付方式适用于所有购买和订阅。</li>
<li>可选。您可以通过选择<strong>操作</strong>图标来移除非默认支付方式。然后选择<strong>删除</strong>。</li>
</ol>

      </div>
    
  </div>
</div>


### 组织

> [!注意]
>
> 您必须是组织所有者才能更改支付信息。








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
        <p>添加支付方式：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com/" rel="noopener">Docker Home</a> 并选择您的组织。</li>
<li>选择<strong>计费</strong>。</li>
<li>从左侧菜单中选择<strong>支付方式</strong>。</li>
<li>选择<strong>添加支付方式</strong>。</li>
<li>输入新的支付信息：
<ul>
<li>添加银行卡：
<ul>
<li>选择<strong>银行卡</strong>并填写银行卡信息表单。</li>
</ul>
</li>
<li>添加 Link 支付：
<ul>
<li>选择<strong>使用 Link 安全一键结账</strong>，并输入您的 Link <strong>电子邮箱地址</strong>和<strong>手机号码</strong>。</li>
<li>如果您还不是 Link 用户，则必须填写银行卡信息表单以存储用于 Link 支付的银行卡。</li>
</ul>
</li>
<li>添加银行账户：
<ul>
<li>选择<strong>美国银行账户</strong>。</li>
<li>验证您的<strong>电子邮箱</strong>和<strong>全名</strong>。</li>
<li>如果您的银行在列表中，请选择您的银行名称。</li>
<li>如果您的银行不在列表中，请选择<strong>搜索您的银行</strong>。</li>
<li>要验证银行账户，请参阅<a class="link" href="/billing/payment-method/#verify-a-bank-account">验证银行账户</a>。</li>
</ul>
</li>
</ul>
</li>
<li>选择<strong>添加支付方式</strong>。</li>
<li>可选。您可以通过选择<strong>设为默认</strong>操作来设置新的默认支付方式。</li>
<li>可选。您可以通过选择<strong>删除</strong>操作来移除非默认支付方式。</li>
</ol>


  

<blockquote
  
  class="admonition not-prose">
  <p>[!注意]</p>
<p>如果要将美国银行账户设为默认支付方式，您必须先验证该账户。</p>

  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%97%A7%E7%89%88-Docker-%E8%AE%A2%E9%98%85' && 'hidden'"
      >
        <p>添加支付方式：</p>
<ol>
<li>登录 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a>。</li>
<li>选择您的组织，然后选择<strong>计费</strong>。</li>
<li>选择<strong>支付方式</strong>链接。</li>
<li>选择<strong>添加支付方式</strong>。</li>
<li>输入新的支付信息：
<ul>
<li>添加银行卡：
<ul>
<li>选择<strong>银行卡</strong>并填写银行卡信息表单。</li>
</ul>
</li>
<li>添加 Link 支付：
<ul>
<li>选择<strong>使用 Link 安全一键结账</strong>，并输入您的 Link <strong>电子邮箱地址</strong>和<strong>手机号码</strong>。</li>
<li>如果您还不是 Link 用户，则必须填写银行卡信息表单以存储用于 Link 支付的银行卡。</li>
</ul>
</li>
</ul>
</li>
<li>选择<strong>添加支付方式</strong>。</li>
<li>选择<strong>操作</strong>图标，然后选择<strong>设为默认</strong>，以确保您的新支付方式适用于所有购买和订阅。</li>
<li>可选。您可以通过选择<strong>操作</strong>图标来移除非默认支付方式。然后选择<strong>删除</strong>。</li>
</ol>

      </div>
    
  </div>
</div>


## 启用发票付款





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Subscription:</span>
        
          <span>Team</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M30-240q-12.75 0-21.37-8.63Q0-257.25 0-270v-23q0-38.57 41.5-62.78Q83-380 150.38-380q12.16 0 23.39.5t22.23 2.15q-8 17.35-12 35.17-4 17.81-4 37.18v65H30Zm240 0q-12.75 0-21.37-8.63Q240-257.25 240-270v-35q0-32 17.5-58.5T307-410q32-20 76.5-30t96.5-10q53 0 97.5 10t76.5 30q32 20 49 46.5t17 58.5v35q0 12.75-8.62 21.37Q702.75-240 690-240H270Zm510 0v-65q0-19.86-3.5-37.43T765-377.27q11-1.73 22.17-2.23 11.17-.5 22.83-.5 67.5 0 108.75 23.77T960-293v23q0 12.75-8.62 21.37Q942.75-240 930-240H780ZM149.57-410q-28.57 0-49.07-20.56Q80-451.13 80-480q0-29 20.56-49.5Q121.13-550 150-550q29 0 49.5 20.5t20.5 49.93q0 28.57-20.5 49.07T149.57-410Zm660 0q-28.57 0-49.07-20.56Q740-451.13 740-480q0-29 20.56-49.5Q781.13-550 810-550q29 0 49.5 20.5t20.5 49.93q0 28.57-20.5 49.07T809.57-410ZM480-480q-50 0-85-35t-35-85q0-51 35-85.5t85-34.5q51 0 85.5 34.5T600-600q0 50-34.5 85T480-480Z"/></svg>
            
          </span>
        
          <span>Business</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M80-180v-600q0-24.75 17.63-42.38Q115.25-840 140-840h270q24.75 0 42.38 17.62Q470-804.75 470-780v105h350q24.75 0 42.38 17.62Q880-639.75 880-615v435q0 24.75-17.62 42.37Q844.75-120 820-120H140q-24.75 0-42.37-17.63Q80-155.25 80-180Zm60 0h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm165 495h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm165 495h350v-435H470v105h80v60h-80v105h80v60h-80v105Zm185-270v-60h60v60h-60Zm0 165v-60h60v60h-60Z"/></svg>
            
          </span>
        
      </div>
    

    

    

    
  </div>



发票付款适用于拥有年度订阅的团队和企业客户，从首次续订开始可用。选择此支付方式时，您将使用支付卡或 ACH 银行转账预付首个订阅周期的费用。

续订时，您将收到一封电子邮件发票，需要手动支付，而不是自动扣款。发票付款不适用于订阅升级或变更。

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择**计费**。
1. 选择**支付方式**，然后选择**发票付款**。
1. 要启用发票付款，请选择切换开关。
1. 确认您的计费联系信息。如果需要更改，请选择**更改**并输入新的详细信息。

## 验证银行账户

有两种方式可以将银行账户验证为支付方式：

- 即时验证：Docker 支持多家主要银行进行即时验证。
- 手动验证：所有其他银行必须手动验证。








<div
  class="tabs"
  
    x-data="{ selected: '%E5%8D%B3%E6%97%B6%E9%AA%8C%E8%AF%81' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E5%8D%B3%E6%97%B6%E9%AA%8C%E8%AF%81' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E5%8D%B3%E6%97%B6%E9%AA%8C%E8%AF%81'"
        
      >
        即时验证
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E6%89%8B%E5%8A%A8%E9%AA%8C%E8%AF%81' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%89%8B%E5%8A%A8%E9%AA%8C%E8%AF%81'"
        
      >
        手动验证
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E5%8D%B3%E6%97%B6%E9%AA%8C%E8%AF%81' && 'hidden'"
      >
        
<h3 class=" scroll-mt-20 flex items-center gap-2" id="即时验证">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%8d%b3%e6%97%b6%e9%aa%8c%e8%af%81">
    即时验证
  </a>
</h3>

<p>要即时验证银行账户，您必须从 Docker 计费流程登录您的银行账户：</p>
<ol>
<li>选择<strong>美国银行账户</strong>作为支付方式。</li>
<li>验证您的<strong>电子邮箱</strong>和<strong>全名</strong>。</li>
<li>如果您的银行在列表中，请选择您的银行名称或选择<strong>搜索您的银行</strong>。</li>
<li>登录您的银行账户并查看条款和条件。此协议允许 Docker 从您连接的银行账户扣款。</li>
<li>选择<strong>同意并继续</strong>。</li>
<li>选择要链接和验证的账户，然后选择<strong>连接账户</strong>。</li>
</ol>
<p>账户验证成功后，您将在弹出窗口中看到成功消息。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%89%8B%E5%8A%A8%E9%AA%8C%E8%AF%81' && 'hidden'"
      >
        
<h3 class=" scroll-mt-20 flex items-center gap-2" id="手动验证">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%89%8b%e5%8a%a8%e9%aa%8c%e8%af%81">
    手动验证
  </a>
</h3>

<p>要手动验证银行账户，您必须输入银行对账单中的小额存款金额：</p>
<ol>
<li>选择<strong>美国银行账户</strong>作为支付方式。</li>
<li>验证您的<strong>电子邮箱</strong>和<strong>姓名</strong>。</li>
<li>选择<strong>改为手动输入银行详细信息</strong>。</li>
<li>输入银行详细信息：<strong>路由号码</strong>和<strong>账号</strong>。</li>
<li>选择<strong>提交</strong>。</li>
<li>您将收到一封电子邮件，其中包含手动验证的说明。</li>
</ol>
<p>手动验证使用小额存款。您将在 1-2 个工作日内在银行账户中看到一笔小额存款（例如 $0.01）。打开手动验证电子邮件并输入该存款金额以验证您的账户。</p>

      </div>
    
  </div>
</div>


## 支付失败

> [!注意]
>
> 您无法手动重试失败的支付。Docker 将根据重试计划重试失败的支付。

如果订阅支付失败，将有 15 天的宽限期（包括到期日）。Docker 将按照以下计划重试收取支付 3 次：

- 到期日后 3 天
- 上次尝试后 5 天
- 上次尝试后 7 天

Docker 还会在每次支付失败后发送一封电子邮件通知 `需要操作 - 信用卡支付失败`，并附上未付发票。

宽限期结束后，如果发票仍未支付，订阅将降级为免费订阅，所有付费功能将被禁用。
