# 停用组织





  
  
  
  


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



了解如何停用 Docker 组织，包括所需的先决条件步骤。有关停用用户账户的信息，请参阅 [停用用户账户](../../accounts/deactivate-user-account.md)。

> [!WARNING]
>
> 停用账户后，所有使用您的 Docker 账户或组织账户的 Docker 产品和服务将无法访问。

## 先决条件

在停用组织之前，您必须完成以下所有步骤：

- 下载您要保留的所有镜像和标签：
  `docker pull -a <image>:<tag>`。
- 如果您有活跃的 Docker 订阅，[将其降级为免费订阅](../../subscription/change.md)。
- 移除组织内的所有其他成员。
- 解除 [GitHub 和 Bitbucket 账户](../../docker-hub/repos/manage/builds/link-source.md#unlink-a-github-user-account) 的链接。
- 对于 Business 组织，[移除您的 SSO 连接](/manuals/enterprise/security/single-sign-on/manage.md#remove-an-organization)。

## 停用

您可以使用 Admin Console 或 Docker Hub 停用您的组织。

> [!WARNING]
>
> 此操作无法撤销。请确保在停用组织之前已收集所有需要的数据。

1. 登录 [Docker Home](https://app.docker.com) 并选择要停用的组织。
1. 选择 **Admin Console**，然后选择 **Deactivate**。如果 **Deactivate** 按钮不可用，请确认您已完成所有 [先决条件](#先决条件)。
1. 输入组织名称以确认停用。
1. 选择 **Deactivate organization**。
