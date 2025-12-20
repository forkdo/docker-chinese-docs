# 组映射





  
  
  
  


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



组映射功能可自动将身份提供程序 (IdP) 中的用户组与 Docker 组织中的团队进行同步。例如，当您在 IdP 中将开发者添加到 "backend-team" 组时，他们会自动添加到 Docker 中的相应团队。

本文档将介绍组映射的工作原理以及如何设置组映射。

> [!TIP]
>
> 如果您需要将用户添加到多个组织或一个组织内的多个团队，组映射是理想的选择。如果您不需要设置多组织或多团队分配，SCIM [用户级属性](scim.md#set-up-role-mapping) 可能更适合您的需求。

## 前提条件

在开始之前，您必须满足以下条件：

- 为您的组织配置了 SSO
- 拥有 Docker Home 和身份提供程序的管理员访问权限

## 组映射的工作原理

组映射通过以下关键组件使您的 Docker 团队与 IdP 组保持同步：

- **认证流程**：当用户通过 SSO 登录时，您的 IdP 会与 Docker 共享用户属性，包括电子邮件、姓名和组成员资格。
- **自动更新**：Docker 使用这些属性创建或更新用户配置文件，并根据 IdP 组的更改管理团队分配。
- **唯一标识**：Docker 使用电子邮件地址作为唯一标识符，因此每个 Docker 账户必须拥有唯一的电子邮件地址。
- **团队同步**：用户的团队成员资格在 Docker 中会自动反映您在 IdP 组中所做的更改。

## 设置组映射

组映射的设置涉及配置您的身份提供程序以与 Docker 共享组信息。这需要：

- 使用 Docker 的命名格式在 IdP 中创建组
- 配置属性，以便您的 IdP 在认证期间发送组数据
- 将用户添加到相应的组中
- 测试连接以确保组正确同步

您可以将组映射与仅使用 SSO 的场景配合使用，也可以与 SSO 和 SCIM 结合使用，以实现增强的用户生命周期管理。

### 组命名格式

在 IdP 中使用以下格式创建组：`organization:team`。

例如：

- 对于 "moby" 组织中的 "developers" 团队：`moby:developers`
- 对于多组织访问：`moby:backend` 和 `whale:desktop`

如果组同步时团队尚不存在，Docker 会自动创建团队。

### 支持的属性

| 属性 | 描述 |
|:--------- | :---------- |
| `id` | 组的唯一 ID，采用 UUID 格式。此属性为只读。 |
| `displayName` | 组的名称，遵循组映射格式：`organization:team`。 |
| `members` | 属于此组的成员用户列表。 |
| `members(x).value` | 作为此组成员的用户的唯一 ID。成员通过 ID 引用。 |

## 使用 SSO 配置组映射

将组映射与使用 SAML 认证方法的 SSO 连接配合使用。

> [!NOTE]
>
> 使用 Azure AD (OIDC) 认证方法时不支持通过 SSO 进行组映射。这些配置不需要 SCIM。








<div
  class="tabs"
  
    x-data="{ selected: 'Okta' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Okta' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Okta'"
        
      >
        Okta
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Entra-ID' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Entra-ID'"
        
      >
        Entra ID
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Okta' && 'hidden'"
      >
        <p>您的 IdP 用户界面可能与以下步骤略有不同。请参阅 <a class="link" href="https://help.okta.com/oie/en-us/content/topics/apps/define-group-attribute-statements.htm" rel="noopener">Okta 文档</a> 进行验证。</p>
<p>设置组映射：</p>
<ol>
<li>登录 Okta 并打开您的应用程序。</li>
<li>导航到应用程序的 <strong>SAML 设置</strong> 页面。</li>
<li>在 <strong>组属性声明（可选）</strong> 部分，按如下方式配置：
<ul>
<li><strong>名称</strong>：<code>groups</code></li>
<li><strong>名称格式</strong>：<code>Unspecified</code></li>
<li><strong>筛选器</strong>：<code>Starts with</code> + <code>organization:</code>，其中 <code>organization</code> 是您组织的名称
筛选器选项将筛选掉与您的 Docker 组织无关的组。</li>
</ul>
</li>
<li>选择 <strong>目录</strong>，然后选择 <strong>组</strong> 来创建您的组。</li>
<li>使用格式 <code>organization:team</code> 添加您的组，该格式应与 Docker 中的组织和团队名称匹配。</li>
<li>将用户分配到您创建的组。</li>
</ol>
<p>下次与 Docker 同步组时，您的用户将映射到您定义的 Docker 组。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Entra-ID' && 'hidden'"
      >
        <p>您的 IdP 用户界面可能与以下步骤略有不同。请参阅 <a class="link" href="https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes" rel="noopener">Entra ID 文档</a> 进行验证。</p>
<p>设置组映射：</p>
<ol>
<li>登录 Entra ID 并打开您的应用程序。</li>
<li>选择 <strong>管理</strong>，然后选择 <strong>单一登录</strong>。</li>
<li>选择 <strong>添加组声明</strong>。</li>
<li>在组声明部分，选择 <strong>分配给应用程序的组</strong>，源属性为 <strong>仅限云的组显示名称（预览）</strong>。</li>
<li>选择 <strong>高级选项</strong>，然后选择 <strong>筛选组</strong> 选项。</li>
<li>按如下方式配置属性：
<ul>
<li><strong>要匹配的属性</strong>：<code>显示名称</code></li>
<li><strong>匹配方式</strong>：<code>包含</code></li>
<li><strong>字符串</strong>：<code>:</code></li>
</ul>
</li>
<li>选择 <strong>保存</strong>。</li>
<li>选择 <strong>组</strong>、<strong>所有组</strong>，然后选择 <strong>新建组</strong> 来创建您的组。</li>
<li>将用户分配到您创建的组。</li>
</ol>
<p>下次与 Docker 同步组时，您的用户将映射到您定义的 Docker 组。</p>

      </div>
    
  </div>
</div>


## 使用 SCIM 配置组映射

将组映射与 SCIM 结合使用，以实现更高级的用户生命周期管理。在开始之前，请确保您已先 [设置 SCIM](./scim.md#enable-scim)。








<div
  class="tabs"
  
    x-data="{ selected: 'Okta' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Okta' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Okta'"
        
      >
        Okta
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Entra-ID' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Entra-ID'"
        
      >
        Entra ID
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Okta' && 'hidden'"
      >
        <p>您的 IdP 用户界面可能与以下步骤略有不同。请参阅 <a class="link" href="https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-enable-group-push.htm" rel="noopener">Okta 文档</a> 进行验证。</p>
<p>设置您的组：</p>
<ol>
<li>登录 Okta 并打开您的应用程序。</li>
<li>选择 <strong>应用程序</strong>，然后选择 <strong>配置</strong> 和 <strong>集成</strong>。</li>
<li>选择 <strong>编辑</strong> 以在您的连接上启用组，然后选择 <strong>推送组</strong>。</li>
<li>选择 <strong>保存</strong>。保存此配置会将 <strong>推送组</strong> 选项卡添加到您的应用程序。</li>
<li>选择 <strong>目录</strong>，然后选择 <strong>组</strong> 来创建您的组。</li>
<li>使用格式 <code>organization:team</code> 添加您的组，该格式应与 Docker 中的组织和团队名称匹配。</li>
<li>将用户分配到您创建的组。</li>
<li>返回到 <strong>集成</strong> 页面，然后选择 <strong>推送组</strong> 选项卡以打开可控制和管理组配置方式的视图。</li>
<li>选择 <strong>推送组</strong>，然后选择 <strong>按规则查找组</strong>。</li>
<li>按规则配置组，如下所示：
<ul>
<li>输入规则名称，例如 <code>与 Docker Hub 同步组</code></li>
<li>按名称匹配组，例如以 <code>docker:</code> 开头或包含 <code>:</code>（用于多组织）</li>
<li>如果启用 <strong>立即按规则推送组</strong>，则组或组分配发生更改时同步会立即发生。如果您不想手动推送组，请启用此选项。</li>
</ul>
</li>
</ol>
<p>在 <strong>推送的组</strong> 列的 <strong>按规则</strong> 下找到您的新规则。匹配该规则的组会列在右侧的组表中。</p>
<p>要推送此表中的组：</p>
<ol>
<li>选择 <strong>Okta 中的组</strong>。</li>
<li>选择 <strong>推送状态</strong> 下拉菜单。</li>
<li>选择 <strong>立即推送</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Entra-ID' && 'hidden'"
      >
        <p>您的 IdP 用户界面可能与以下步骤略有不同。请参阅 <a class="link" href="https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes" rel="noopener">Entra ID 文档</a> 进行验证。</p>
<p>在配置组映射之前，请完成以下操作：</p>
<ol>
<li>登录 Entra ID 并转到您的应用程序。</li>
<li>在您的应用程序中，选择 <strong>配置</strong>，然后选择 <strong>映射</strong>。</li>
<li>选择 <strong>配置 Microsoft Entra ID 组</strong>。</li>
<li>选择 <strong>显示高级选项</strong>，然后选择 <strong>编辑属性列表</strong>。</li>
<li>将 <code>externalId</code> 类型更新为 <code>reference</code>，然后选中 <strong>多值</strong> 复选框并选择引用的对象属性 <code>urn:ietf:params:scim:schemas:core:2.0:Group</code>。</li>
<li>选择 <strong>保存</strong>，然后选择 <strong>是</strong> 进行确认。</li>
<li>转到 <strong>配置</strong>。</li>
<li>将 <strong>配置状态</strong> 切换为 <strong>开</strong>，然后选择 <strong>保存</strong>。</li>
</ol>
<p>接下来，设置组映射：</p>
<ol>
<li>转到应用程序概览页面。</li>
<li>在 <strong>配置用户账户</strong> 下，选择 <strong>开始</strong>。</li>
<li>选择 <strong>添加用户/组</strong>。</li>
<li>使用 <code>organization:team</code> 格式创建您的组。</li>
<li>将组分配给配置组。</li>
<li>选择 <strong>开始配置</strong> 以开始同步。</li>
</ol>
<p>要进行验证，请选择 <strong>监视</strong>，然后选择 <strong>配置日志</strong> 以查看您的组是否已成功配置。在您的 Docker 组织中，您可以检查组是否已正确配置以及成员是否已添加到相应的团队。</p>

      </div>
    
  </div>
</div>


完成后，通过 SSO 登录 Docker 的用户将自动添加到 IdP 中映射的组织和团队。

> [!TIP]
>
> [启用 SCIM](scim.md) 以利用自动用户配置和取消配置功能。如果您不启用 SCIM，用户只会自动配置。您必须手动取消配置。
