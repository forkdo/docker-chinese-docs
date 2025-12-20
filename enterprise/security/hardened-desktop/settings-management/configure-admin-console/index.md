# 使用 Admin Console 配置设置管理





  
  
  
  


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
        <span class="font-bold">For:</span>
        <span>Administrators</span>
        
          <span class="icon-svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M693-80q-78 0-133-55.5T505-267q0-78 55-133.5T693-456q77 0 132.5 55.5T881-267q0 76-55.5 131.5T693-80ZM160-522v-197q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v190q0 14-11 21.5t-24 2.5q-17-5-35.5-8t-36.5-3q-103 0-175.5 73T445-267q0 40 13.5 79t38.5 71q10 13 2.5 26T478-82q-69-20-122-51.5T251-237q-43-60-67-132.5T160-522Zm531 252q26 0 44-19t18-45q0-26-18-44t-44-18q-26 0-45 18t-19 44q0 26 19 45t45 19Zm-1 125q28 0 53-11t43-31q4-5 2.5-11t-6.5-8q-22-10-45-15.5t-47-5.5q-24 0-47 5t-45 16q-5 2-7 8t2 11q18 21 43.5 31.5T690-145Z"/></svg>
          </span>
        
      </div>
    
  </div>



使用 Docker Admin Console 为整个组织的 Docker Desktop 创建和管理设置策略。设置策略可让您标准化配置、强制执行安全要求并保持一致的 Docker Desktop 环境。

## 先决条件

在开始之前，请确保您已具备：

- 已安装 [Docker Desktop 4.37.1 或更高版本](/manuals/desktop/release-notes.md)
- [已验证的域名](/manuals/enterprise/security/single-sign-on/configure.md#step-one-add-and-verify-your-domain)
- 为您的组织[强制执行登录](/manuals/enterprise/security/enforce-sign-in/_index.md)
- Docker Business 订阅

> [!IMPORTANT]
>
> 您必须将用户添加到已验证的域名，设置才能生效。

## 创建设置策略

要创建新的设置策略：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Admin Console**，然后选择 **Desktop Settings Management**。
3. 选择 **Create a settings policy**。
4. 提供名称和可选描述。

      > [!TIP]
      >
      > 您可以上传现有的 `admin-settings.json` 文件来预填充表单。
      Admin Console 策略会覆盖本地的 `admin-settings.json` 文件。

5. 选择策略适用对象：
   - 所有用户
   - 特定用户

      > [!NOTE]
      >
      > 针对特定用户的策略会覆盖全局默认策略。在全组织范围应用策略之前，请先用小范围群体测试您的策略。

6. 使用以下状态配置每个设置：
   - **User-defined**：用户可以更改该设置。
   - **Always enabled**：设置开启并锁定。
   - **Enabled**：设置开启但可以更改。
   - **Always disabled**：设置关闭并锁定。
   - **Disabled**：设置关闭但可以更改。

      > [!TIP]
      >
      > 有关可配置设置、支持平台和配置方法的完整列表，请参阅[设置参考](settings-reference.md)。

7. 选择 **Create** 以保存您的策略。

## 应用策略

设置策略在 Docker Desktop 重启且用户重新登录后生效。

对于新安装：

1. 启动 Docker Desktop。
2. 使用您的 Docker 账户登录。

对于现有安装：

1. 完全退出 Docker Desktop。
2. 重新启动 Docker Desktop。

> [!IMPORTANT]
>
> 用户必须完全退出并重新打开 Docker Desktop。从 Docker Desktop 菜单中重启是不够的。

Docker Desktop 在启动时以及运行期间每 60 分钟检查一次策略更新。

## 验证应用的设置

应用策略后：

- Docker Desktop 将大多数设置显示为灰色（不可更改）
- 某些设置，特别是增强型容器隔离配置，可能不会出现在 GUI 中
- 您可以通过检查系统上的 [`settings-store.json` 文件](/manuals/desktop/settings-and-maintenance/settings.md) 来验证所有应用的设置

## 管理现有策略

在 Admin Console 的 **Desktop Settings Management** 页面中，使用 **Actions** 菜单可以：

- 编辑或删除现有的设置策略
- 将设置策略导出为 `admin-settings.json` 文件
- 将特定用户策略提升为新的全局默认策略

## 回滚策略

要回滚设置策略：

- 完全回滚：删除整个策略。
- 部分回滚：将特定设置设置为 **User-defined**。

当您回滚设置时，用户将重新获得对这些设置配置的控制权。
