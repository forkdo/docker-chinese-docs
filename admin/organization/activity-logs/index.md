# 活动日志





  
  
  
  


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
    

    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">For:</span>
        <span>Administrators</span>
        
          <span class="icon-svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M693-80q-78 0-133-55.5T505-267q0-78 55-133.5T693-456q77 0 132.5 55.5T881-267q0 76-55.5 131.5T693-80ZM160-522v-197q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v190q0 14-11 21.5t-24 2.5q-17-5-35.5-8t-36.5-3q-103 0-175.5 73T445-267q0 40 13.5 79t38.5 71q10 13 2.5 26T478-82q-69-20-122-51.5T251-237q-43-60-67-132.5T160-522Zm531 252q26 0 44-19t18-45q0-26-18-44t-44-18q-26 0-45 18t-19 44q0 26 19 45t45 19Zm-1 125q28 0 53-11t43-31q4-5 2.5-11t-6.5-8q-22-10-45-15.5t-47-5.5q-24 0-47 5t-45 16q-5 2-7 8t2 11q18 21 43.5 31.5T690-145Z"/></svg>
          </span>
        
      </div>
    
  </div>



活动日志按时间顺序显示在组织和仓库级别发生的活动。活动日志为组织所有者提供了所有成员活动的记录。

通过活动日志，所有者可以查看和追踪：

 - 做了哪些更改
 - 更改发生的日期
 - 谁发起了更改

例如，活动日志会显示仓库创建或删除的日期、创建仓库的成员、仓库名称，以及隐私设置发生更改的时间。

如果仓库属于订阅了 Docker Business 或 Team 的组织，所有者还可以查看其仓库的活动日志。

## 访问活动日志








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-Home' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Home' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Home'"
        
      >
        Docker Home
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'API' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'API'"
        
      >
        API
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Home' && 'hidden'"
      >
        <p>要在 Docker Home 中查看活动日志：</p>
<ol>
<li>登录 <a class="link" href="https://app.docker.com" rel="noopener">Docker Home</a> 并选择您的组织。</li>
<li>选择 <strong>Admin Console</strong>，然后选择 <strong>Activity logs</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'API' && 'hidden'"
      >
        <p>要使用 Docker Hub API 查看活动日志，请使用 <a class="link" href="https://docs.docker.com/reference/api/hub/latest/#tag/audit-logs" rel="noopener">审计日志端点</a>。</p>

      </div>
    
  </div>
</div>


## 筛选和自定义活动日志

> [!IMPORTANT]
>
> Docker Home 保留活动日志 30 天。要检索 30 天前的活动，您必须使用
> [Docker Hub API](https://docs.docker.com/reference/api/hub/latest/#tag/audit-logs)。

默认情况下，**Activity** 标签页显示过去 30 天内记录的所有事件。要缩小查看范围，请使用日历选择特定的日期范围。日志将更新，仅显示该期间内发生的活动。

您还可以按活动类型筛选。使用 **All Activities** 下拉菜单，重点关注组织级别、仓库级别或账单相关的事件。在 Docker Hub 中，查看仓库时，**Activities** 标签页仅显示该仓库的事件。

选择 **Organization**、**Repository** 或 **Billing** 类别后，使用 **All Actions** 下拉菜单，按特定事件类型进一步细化结果。

> [!NOTE]
>
> Docker Support 触发的事件显示在用户名 **dockersupport** 下。

## 活动日志事件类型

请参考以下部分，了解事件及其描述的列表：

### 组织事件

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Team Created | 与团队创建相关的活动 |
| Team Updated | 与团队修改相关的活动 |
| Team Deleted | 与团队删除相关的活动 |
| Team Member Added | 添加到团队的成员详情 |
| Team Member Removed | 从团队中移除的成员详情 |
| Team Member Invited | 邀请到团队的成员详情 |
| Organization Member Added | 添加到组织的成员详情 |
| Organization Member Removed | 从组织中移除的成员详情 |
| Member Role Changed | 组织中成员角色更改的详情 |
| Organization Created | 与新组织创建相关的活动 |
| Organization Settings Updated | 与组织设置更新相关的详情 |
| Registry Access Management enabled | 与启用注册表访问管理相关的活动 |
| Registry Access Management disabled | 与禁用注册表访问管理相关的活动 |
| Registry Access Management registry added | 与添加注册表相关的活动 |
| Registry Access Management registry removed | 与移除注册表相关的活动 |
| Registry Access Management registry updated | 与更新注册表相关的详情 |
| Single Sign-On domain added | 添加到组织的单点登录域详情 |
| Single Sign-On domain removed | 从组织中移除的单点登录域详情 |
| Single Sign-On domain verified | 为组织验证的单点登录域详情 |
| Access token created | 在组织中创建的访问令牌 |
| Access token updated | 在组织中更新的访问令牌 |
| Access token deleted | 在组织中删除的访问令牌 |
| Policy created | 添加设置策略的详情 |
| Policy updated | 更新设置策略的详情 |
| Policy deleted | 删除设置策略的详情 |
| Policy transferred | 将设置策略转移到另一个所有者的详情 |
| Create SSO Connection | 创建新组织/公司 SSO 连接的详情 |
| Update SSO Connection | 更新现有组织/公司 SSO 连接的详情 |
| Delete SSO Connection | 删除现有组织/公司 SSO 连接的详情 |
| Enforce SSO | 切换现有组织/公司 SSO 连接的强制执行的详情 |
| Enforce SCIM | 切换现有组织/公司 SSO 连接的 SCIM 的详情 |
| Refresh SCIM Token | 刷新现有组织/公司 SSO 连接的 SCIM 令牌的详情 |
| Change SSO Connection Type | 更改现有组织/公司 SSO 连接的连接类型的详情 |
| Toggle JIT provisioning | 切换现有组织/公司 SSO 连接的 JIT 配置的详情 |

### 仓库事件

> [!NOTE]
>
> 包含用户操作的事件描述可能指 Docker 用户名、个人访问令牌 (PAT) 或组织访问令牌 (OAT)。例如，如果用户推送标签到仓库，事件将包含描述：`<user-access-token>` 推送标签到仓库。

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Repository Created | 与新仓库创建相关的活动 |
| Repository Deleted | 与仓库删除相关的活动 |
| Repository Updated | 与更新仓库的描述、完整描述或状态相关的活动 |
| Privacy Changed | 与更新的隐私策略相关的详情 |
| Tag Pushed | 与推送标签相关的活动 |
| Tag Deleted | 与删除标签相关的活动 |
| Categories Updated | 与设置或更新仓库类别相关的活动 |

### 账单事件

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Plan Upgraded | 当组织的账单计划升级到更高层级计划时发生。|
| Plan Downgraded | 当组织的账单计划降级到更低层级计划时发生。 |
| Seat Added | 当座位添加到组织的账单计划时发生。 |
| Seat Removed | 当座位从组织的账单计划移除时发生。 |
| Billing Cycle Changed | 当组织的收费周期发生变化时发生。|
| Plan Downgrade Canceled | 当组织的计划降级被取消时发生。|
| Seat Removal Canceled | 当组织的账单计划中的座位移除被取消时发生。 |
| Plan Upgrade Requested | 当组织中的用户请求计划升级时发生。 |
| Plan Downgrade Requested | 当组织中的用户请求计划降级时发生。 |
| Seat Addition Requested | 当组织中的用户请求增加座位数量时发生。 |
| Seat Removal Requested | 当组织中的用户请求减少座位数量时发生。 |
| Billing Cycle Change Requested | 当组织中的用户请求更改账单周期时发生。 |
| Plan Downgrade Cancellation Requested | 当组织中的用户请求取消计划降级时发生。 |
| Seat Removal Cancellation Requested | 当组织中的用户请求取消座位移除时发生。 |

### 卸载事件

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Offload Lease Start | 当组织中的卸载租约开始时发生。 |
| Offload Lease End | 当组织中的卸载租约结束时发生。 |
