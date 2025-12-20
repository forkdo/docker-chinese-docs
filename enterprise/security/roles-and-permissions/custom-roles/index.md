# 自定义角色





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">For:</span>
        <span>Administrators</span>
        
          <span class="icon-svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M693-80q-78 0-133-55.5T505-267q0-78 55-133.5T693-456q77 0 132.5 55.5T881-267q0 76-55.5 131.5T693-80ZM160-522v-197q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v190q0 14-11 21.5t-24 2.5q-17-5-35.5-8t-36.5-3q-103 0-175.5 73T445-267q0 40 13.5 79t38.5 71q10 13 2.5 26T478-82q-69-20-122-51.5T251-237q-43-60-67-132.5T160-522Zm531 252q26 0 44-19t18-45q0-26-18-44t-44-18q-26 0-45 18t-19 44q0 26 19 45t45 19Zm-1 125q28 0 53-11t43-31q4-5 2.5-11t-6.5-8q-22-10-45-15.5t-47-5.5q-24 0-47 5t-45 16q-5 2-7 8t2 11q18 21 43.5 31.5T690-145Z"/></svg>
          </span>
        
      </div>
    
  </div>



自定义角色允许您创建符合组织特定需求的定制权限集。本页面介绍自定义角色以及创建和管理它们的步骤。

## 什么是自定义角色？

自定义角色让您可以为组织创建定制的权限集。您可以将自定义角色分配给单个用户或团队。用户和团队要么获得核心角色，要么获得自定义角色，但不能同时拥有两者。

当 Docker 的核心角色无法满足您的需求时，请使用自定义角色。

## 先决条件

要配置自定义角色，您需要在 Docker 组织中拥有所有者权限。

## 创建自定义角色

在将自定义角色分配给用户之前，您必须在管理控制台中创建一个：

1. 登录 [Docker Home](https://app.docker.com)。
2. 选择 **Admin Console**（管理控制台）。
3. 在 **User management**（用户管理）下，选择 **Roles** > **Create role**（创建角色）。
4. 创建名称并描述该角色的用途：
   - 提供 **Label**（标签）
   - 输入唯一的 **Name**（名称）标识符（以后无法更改）
   - 添加可选的 **Description**（描述）
5. 通过展开权限类别并选中权限的复选框来设置角色的权限。有关可用权限的完整列表，请参阅[自定义角色权限参考](#custom-roles-permissions-reference)。
6. 选择 **Review**（审查）以审查您的自定义角色配置并查看所选权限的摘要。
7. 选择 **Create**（创建）。

创建自定义角色后，您现在可以[将自定义角色分配给用户](#assign-custom-roles)。

## 编辑自定义角色

1. 登录 [Docker Home](https://app.docker.com)。
2. 选择 **Admin Console**（管理控制台）。
3. 在 **User management**（用户管理）下，选择 **Roles**（角色）。
4. 从列表中找到您的自定义角色，然后选择 **Actions menu**（操作菜单）。
5. 选择 **Edit**（编辑）。
6. 您可以编辑以下自定义角色设置：
   - Label（标签）
   - Description（描述）
   - Permissions（权限）
7. 编辑完成后，选择 **Save**（保存）。

## 分配自定义角色








<div
  class="tabs"
  
    x-data="{ selected: 'Individual-users' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Individual-users' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Individual-users'"
        
      >
        Individual users
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Bulk-users' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Bulk-users'"
        
      >
        Bulk users
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Teams' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Teams'"
        
      >
        Teams
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Individual-users' && 'hidden'"
      >
        <ol>
<li>登录 <a class="link" href="https://app.docker.com" rel="noopener">Docker Home</a>。</li>
<li>选择 <strong>Members</strong>（成员）。</li>
<li>找到要分配自定义角色的成员，然后选择 <strong>Actions menu</strong>（操作菜单）。</li>
<li>在下拉菜单中，选择 <strong>Change role</strong>（更改角色）。</li>
<li>在 <strong>Select a role</strong>（选择角色）下拉菜单中，选择您的自定义角色。</li>
<li>选择 <strong>Save</strong>（保存）。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Bulk-users' && 'hidden'"
      >
        <ol>
<li>登录 <a class="link" href="https://app.docker.com" rel="noopener">Docker Home</a>。</li>
<li>选择 <strong>Members</strong>（成员）。</li>
<li>使用用户名列中的复选框选择所有要分配自定义角色的用户。</li>
<li>选择 <strong>Change role</strong>（更改角色）。</li>
<li>在 <strong>Select a role</strong>（选择角色）下拉菜单中，选择您的自定义角色或核心角色。</li>
<li>选择 <strong>Save</strong>（保存）。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Teams' && 'hidden'"
      >
        <ol>
<li>登录 <a class="link" href="https://app.docker.com" rel="noopener">Docker Home</a>。</li>
<li>选择 <strong>Teams</strong>（团队）。</li>
<li>找到要分配自定义角色的团队，然后选择 <strong>Actions menu</strong>（操作菜单）。</li>
<li>选择 <strong>Assign role</strong>（分配角色）。</li>
<li>选择您的自定义角色，然后选择 <strong>Assign</strong>（分配）。</li>
</ol>
<p>角色列将更新为新分配的角色。</p>

      </div>
    
  </div>
</div>


## 查看角色分配

要查看哪些用户和团队被分配了角色：

1. 登录 [Docker Home](https://app.docker.com)。
2. 选择 **Admin Console**（管理控制台）。
3. 在 **User management**（用户管理）下，选择 **Roles**（角色）。
4. 在角色列表中，查看 **Users**（用户）和 **Teams**（团队）列以查看分配数量。
5. 选择特定角色以详细查看其权限和分配情况。

## 重新分配自定义角色








<div
  class="tabs"
  
    x-data="{ selected: 'Individual-users' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Individual-users' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Individual-users'"
        
      >
        Individual users
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Bulk-users' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Bulk-users'"
        
      >
        Bulk users
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Teams' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Teams'"
        
      >
        Teams
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Individual-users' && 'hidden'"
      >
        <ol>
<li>登录 <a class="link" href="https://app.docker.com" rel="noopener">Docker Home</a>。</li>
<li>选择 <strong>Members</strong>（成员）。</li>
<li>找到要重新分配的成员，然后选择 <strong>Actions menu</strong>（操作菜单）。</li>
<li>选择 <strong>Change role</strong>（更改角色）。</li>
<li>在 <strong>Select a role</strong>（选择角色）下拉菜单中，选择新角色。</li>
<li>选择 <strong>Save</strong>（保存）。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Bulk-users' && 'hidden'"
      >
        <ol>
<li>登录 <a class="link" href="https://app.docker.com" rel="noopener">Docker Home</a>。</li>
<li>选择 <strong>Members</strong>（成员）。</li>
<li>使用用户名列中的复选框选择所有要重新分配的用户。</li>
<li>选择 <strong>Change role</strong>（更改角色）。</li>
<li>在 <strong>Select a role</strong>（选择角色）下拉菜单中，选择新角色。</li>
<li>选择 <strong>Save</strong>（保存）。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Teams' && 'hidden'"
      >
        <ol>
<li>登录 <a class="link" href="https://app.docker.com" rel="noopener">Docker Home</a>。</li>
<li>选择 <strong>Teams</strong>（团队）。</li>
<li>找到团队，然后选择 <strong>Actions menu</strong>（操作菜单）。</li>
<li>选择 <strong>Change role</strong>（更改角色）。</li>
<li>在弹出窗口中，从下拉菜单中选择一个角色，然后选择 <strong>Save</strong>（保存）。</li>
</ol>

      </div>
    
  </div>
</div>


## 删除自定义角色

删除自定义角色之前，您必须将所有用户和团队重新分配到不同的角色。

1. 登录 [Docker Home](https://app.docker.com)。
2. 选择 **Admin Console**（管理控制台）。
3. 在 **User management**（用户管理）下，选择 **Roles**（角色）。
4. 从列表中找到您的自定义角色，然后选择 **Actions menu**（操作菜单）。
5. 如果该角色已分配用户或团队：
   - 导航到 **Members**（成员）页面，更改所有分配给此自定义角色的用户的角色
   - 导航到 **Teams**（团队）页面，重新分配所有拥有此自定义角色的团队
6. 一旦没有用户或团队被分配，请返回 **Roles**（角色）。
7. 找到您的自定义角色并选择 **Actions menu**（操作菜单）。
8. 选择 **Delete**（删除）。
9. 在确认窗口中，选择 **Delete**（删除）以确认。

## 自定义角色权限参考

自定义角色是通过在不同类别中选择特定权限来构建的。以下表格列出了您可以分配给自定义角色的所有可用权限。

### 组织管理

| 权限 (Permission)                      | 描述 (Description)                                                                                     |
| :-------------------------------- | :---------------------------------------------------------------------------------------------- |
| View teams                        | 查看团队和团队成员                                                                     |
| Manage teams                      | 创建、更新和删除团队和团队成员                                               |
| Manage registry access            | 控制成员可以访问哪些注册表                                                     |
| Manage image access               | 设置成员可以拉取和使用哪些镜像的策略                                          |
| Update organization information   | 更新组织信息，例如名称和位置                                       |
| Member management                 | 管理组织成员、邀请和角色                                                 |
| View custom roles                 | 查看现有自定义角色及其权限                                                |
| Manage custom roles               | 完全访问自定义角色管理和分配                                            |
| Manage organization access tokens | 在此组织中创建、更新和删除仓库。不包括推送/拉取或注册表操作 |
| View activity logs                | 访问组织审计日志和活动历史                                             |
| View domains                      | 查看域和域审计设置                                                          |
| Manage domains                    | 管理已验证域和域审计设置                                               |
| View SSO and SCIM                 | 查看单点登录和用户配置配置                                        |
| Manage SSO and SCIM               | 完全访问 SSO 和 SCIM 管理                                                          |
| Manage Desktop settings           | 配置 Docker Desktop 设置策略并查看使用报告                               |

### Docker Hub

| 权限 (Permission)          | 描述 (Description)                                                |
| :------------------ | :--------------------------------------------------------- |
| View repositories   | 查看仓库详情和内容                       |
| Manage repositories | 创建、更新和删除仓库及其内容 |

### 计费

| 权限 (Permission)     | 描述 (Description)                                      |
| :------------- | :----------------------------------------------- |
| View billing   | 查看组织计费信息            |
| Manage billing | 完全访问管理组织计费 |
