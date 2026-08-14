# 将组织仓库导出为 CSV


本指南介绍如何从 Docker Hub 组织中导出所有仓库的完整列表，包括私有仓库。您将使用来自管理员账户的[个人访问令牌 (PAT)](/security/access-tokens/) 对 Docker Hub API 进行身份验证，并将仓库详细信息导出到 CSV 文件，以便用于报告或分析。

导出的数据包括仓库名称、可见性状态、最后更新时间、拉取次数和星标数。

## 先决条件

开始前，请确保您具备以下条件：

- 对 Docker Hub 组织的管理员访问权限
- 已安装 `curl` 用于发起 API 请求
- 已安装 `jq` 用于 JSON 解析
- 电子表格应用程序，用于查看 CSV 文件

## 创建个人访问令牌

从具有该组织仓库访问权限的用户账户[创建个人访问令牌](/security/access-tokens/)。创建令牌时，至少选择 **只读** 访问权限以列出仓库。

> [!重要]
>
> 使用属于该组织成员的用户账户的 PAT。具有所有者角色的用户可以导出所有组织仓库。成员只能导出他们有权访问的仓库。

## 使用 Docker Hub API 进行身份验证

将您的个人访问令牌交换为 JWT 承载令牌，用于后续的 API 请求。

1. 将您的 Docker Hub 用户名、组织名称和个人访问令牌设置为变量：

   ```bash
   USERNAME="<your-docker-username>"
   ORG="<org-name>"
   PAT="<your_personal_access_token>"
   ```

2. 调用身份验证端点以获取 JWT：

   ```bash
   TOKEN=$(
     curl -s https://hub.docker.com/v2/auth/token \
       -H 'Content-Type: application/json' \
       -d "{\"identifier\":\"$USERNAME\",\"secret\":\"$PAT\"}" \
     | jq -r '.access_token'
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

与您的个人访问令牌关联的 Docker Hub 账户可能无权访问组织中的私有仓库。

要解决此问题：

1. 验证该账户是组织的成员
2. 检查该账户是否具有适当的权限（所有者或成员角色）
3. 确保个人访问令牌具有足够的访问权限
4. 重新生成 JWT 并重试导出

### API 返回 403 或缺少字段

确保您使用的是来自 `/v2/auth/token` 端点的 JWT 作为 `Authorization` 头部中的承载令牌，而不是直接使用个人访问令牌。

验证您的身份验证：

```console
$ curl -s "https://hub.docker.com/v2/namespaces/$ORG/repositories?page_size=1" \
  -H "Authorization: Bearer $TOKEN" | jq
```

如果此操作返回错误，请重新运行身份验证步骤以获取新的 JWT。

