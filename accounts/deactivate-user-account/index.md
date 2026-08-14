# 停用 Docker 账户


了解如何停用个人 Docker 账户，包括停用账户所需的前提条件。

有关停用组织的信息，请参阅
[停用组织](/manuals/admin/organization/deactivate-account.md)。

> [!WARNING]
>
> 停用账户后，所有使用 Docker 账户的 Docker 产品和服务都将无法访问。

## 前提条件

在停用 Docker 账户之前，请完成以下要求：

- 如果你是组织或公司的所有者，必须在停用 Docker 账户之前离开该
  组织或公司：
  1. 登录 [Docker Home](https://app.docker.com/admin) 并选择你的
     组织。
  1. 选择 **Members**（成员）并找到你的用户名。
  1. 选择 **Actions**（操作）菜单，然后选择 **Leave organization**（离开组织）。
- 如果你是组织的唯一所有者，必须将所有者角色分配给组织中的
  其他成员，然后将自己从组织中移除，或者停用该组织。同样，如果你
  是公司的唯一所有者，可以添加其他人为公司所有者，
  然后将自己移除，或者停用该公司。
- 如果你有活跃的 Docker 订阅，
  [请将其降级为 Docker Personal
  订阅](/manuals/subscription/plans/docker.md#cancel-a-docker-plan)。
- 下载你想保留的任何镜像和标签。使用
  `docker pull -a <image>` 拉取所有标签，或使用 `docker pull <image>:<tag>`
  拉取特定标签。
- 如果你为自动构建关联了 GitHub 或 Bitbucket 账户，请解除关联。
  请参阅
  [解除 GitHub 用户账户关联](/manuals/docker-hub/repos/manage/builds/link-source.md#unlink-a-github-user-account)
  或
  [解除 Bitbucket 用户账户关联](/manuals/docker-hub/repos/manage/builds/link-source.md#unlink-a-bitbucket-user-account)。

## 停用

完成前提条件后，你可以停用你的账户。

> [!WARNING]
>
> 停用账户是永久性的，无法撤销。请务必备份所有重要数据。

1. 登录 [Docker Home](https://app.docker.com/login)。
1. 选择你的头像以打开下拉菜单。
1. 选择 **账户设置**。
1. 选择 **停用**。
1. 选择 **停用账户**，然后再次选择以确认。

## 删除个人数据

停用账户不会删除你的个人数据。如需申请删除个人数据，请填写 Docker 的[隐私请求表单](https://preferences.docker.com/)。

