---
title: 将组织仓库导出为 CSV
linkTitle: 导出仓库
description: 了解如何使用 API 导出 Docker Hub 组织下所有仓库的完整列表。
keywords: docker hub, organization, repositories, export, csv, api, access token
---

本指南介绍如何从 Docker Hub 组织中导出所有仓库的完整列表，包括私有仓库。您将使用组织访问令牌 (OAT) 对 Docker Hub API 进行身份验证，并将仓库详细信息导出到 CSV 文件，以便用于报告或分析。

导出的数据包括仓库名称、可见性状态、最后更新时间、拉取次数和星标数。

## 先决条件

开始前，请确保您具备以下条件：

- 对 Docker Hub 组织的管理员访问权限
- 已安装 `curl` 用于发起 API 请求
- 已安装 `jq` 用于 JSON 解析
- 电子表格应用程序，用于查看 CSV 文件

## 创建组织访问令牌

组织访问令牌允许您对 API 请求进行身份验证，而无需交互式登录步骤。

1. 在 [Docker Home](https://app.docker.com) 中导航到您的组织，然后选择 **Admin Console**（管理控制台）。

2. 从侧边栏选择 **Access tokens**（访问令牌）。

3. 选择 **Generate access token**（生成访问令牌）。

4. 配置令牌权限：

   - 在 **Repository permissions**（仓库权限）下，添加您希望令牌访问的每个仓库
   - 为每个仓库分配至少 **Image Pull**（读取）访问权限
   - 每个令牌最多可添加 50 个仓库

5. 复制生成的令牌并安全存储。

> [!重要]
>
> 如果您只启用 **Read public repositories**（读取公共仓库），API 将仅返回公共仓库。要在导出中包含私有仓库，您必须明确将它们添加到令牌的仓库权限中。

## 使用 Docker Hub API 进行身份验证

将您的组织访问令牌交换为 JWT 承载令牌，用于后续的 API 请求。

1. 将您的组织名称和访问令牌设置为变量：

   ```bash
   ORG="<your-org>"
   OAT="<your_org_access_token>"
   ```

2. 调用身份验证端点以获取 JWT：

   ```bash
   TOKEN=$(
     curl -s https://hub.docker.com/v2/users/login \
       -H 'Content-Type: application/json' \
       -d "{\"username\":\"$ORG\",\"password\":\"$OAT\"}" \
     | jq -r '.token'
   )
   ```

3. 验证令牌是否成功获取：

   ```console
   $ echo "Got JWT: ${#TOKEN} chars"
   ```

您将在所有后续 API 调用的 `Authorization` 头部中使用此 JWT 作为承载令牌。

## 检索所有仓库

Docker Hub API 会对仓库列表进行分页。此脚本会检索所有页面并合并结果。

1. 设置页面大小和初始 API 端点：

   ```bash
   PAGE_SIZE=100
   URL="https://hub.docker.com/v2/namespaces/$ORG/repositories?page_size=$PAGE_SIZE"
   ```

2. 遍历所有结果：

   ```bash
   ALL=$(
     while [ -n "$URL" ] && [ "$URL" != "null" ]; do
       RESP=$(curl -s "$URL" -H "Authorization: Bearer $TOKEN")
       echo "$RESP" | jq -c '.results[]'
       URL=$(echo "$RESP" | jq -r '.next')
     done | jq -s '.'
   )
   ```

3. 验证检索到的仓库数量：

   ```console
   $ echo "$ALL" | jq 'length'
   ```

脚本会继续请求每个响应中的 `next` URL，直到分页完成。

## 导出为 CSV

生成包含仓库详细信息的 CSV 文件，您可以在电子表格应用程序中打开该文件。

运行以下命令以创建 `repos.csv`：

```bash
echo "$ALL" | jq -r '
  (["namespace","name","is_private","last_updated","pull_count","star_count"] | @csv),
  (.[] | [
    .namespace, .name, .is_private, .last_updated, (.pull_count//0), (.star_count//0)
  ] | @csv)
' > repos.csv
```

验证导出是否完成：

```console
$ echo "Rows:" $(wc -l < repos.csv)
```

在您偏好的电子表格应用程序中打开 `repos.csv` 文件，以查看和分析您的仓库数据。

## 故障排除

### 仅显示公共仓库

您的组织访问令牌可能只启用了 **Read public repositories**（读取公共仓库），或者缺少对特定私有仓库的权限。

要解决此问题：

1. 在 Docker Hub 中导航到组织的访问令牌
2. 选择您创建的令牌
3. 将私有仓库添加到令牌的权限中，并至少分配 **Image Pull**（镜像拉取）访问权限
4. 重新生成 JWT 并重试导出

### API 返回 403 或缺少字段

确保您使用的是来自 `/v2/users/login` 端点的 JWT 作为 `Authorization` 头部中的承载令牌，而不是直接使用组织访问令牌。

验证您的身份验证：

```console
$ curl -s "https://hub.docker.com/v2/namespaces/$ORG/repositories?page_size=1" \
  -H "Authorization: Bearer $TOKEN" | jq
```

如果此操作返回错误，请重新运行身份验证步骤以获取新的 JWT。

### 需要访问所有仓库

组织访问令牌的作用域限定为您在创建令牌时选择的特定仓库。要导出所有仓库，您有两个选择：

1. 将所有仓库添加到组织访问令牌中（最多 50 个仓库）
2. 使用具有整个组织访问权限的管理员账户的个人访问令牌 (PAT)

这两种方法之间的选择取决于您组织的安全策略。