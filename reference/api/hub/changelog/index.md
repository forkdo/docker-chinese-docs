# Docker Hub API 变更日志

在这里，您可以了解 Docker Service API 的最新变更、新功能、错误修复和已知问题。

---

## 2025-11-21

### 更新

- 在 [PAT 管理](/reference/api/hub/latest/#tag/access-tokens) 端点中添加缺失的 `expires_at` 字段。

## 2025-09-25

### 更新

- 修复 [分配仓库组](/reference/api/hub/latest/#tag/repositories/operation/CreateRepositoryGroup) 端点的请求/响应。

---

## 2025-09-19

### 新增

- 为给定的 `namespace` 添加 [创建仓库](/reference/api/hub/latest/#tag/repositories/operation/CreateRepository) 端点。
- 为给定的 `namespace` 添加 [获取仓库](/reference/api/hub/latest/#tag/repositories/operation/GetRepository) 端点。
- 为给定的 `namespace` 添加 [检查仓库](/reference/api/hub/latest/#tag/repositories/operation/CheckRepository) 端点。

### 弃用

- [弃用 POST /v2/repositories](/reference/api/hub/deprecated/#deprecate-legacy-createrepository)
- [弃用 POST /v2/repositories/{namespace}](/reference/api/hub/deprecated/#deprecate-legacy-createrepository)
- [弃用 GET /v2/repositories/{namespace}/{repository}](/reference/api/hub/deprecated/#deprecate-legacy-getrepository)
- [弃用 HEAD /v2/repositories/{namespace}/{repository}](/reference/api/hub/deprecated/#deprecate-legacy-getrepository)

---

## 2025-07-29

### 新增

- 为给定的 `namespace` 和 `repository` 添加 [更新仓库不可变标签设置](/reference/api/hub/latest/#tag/repositories/operation/UpdateRepositoryImmutableTags) 端点。
- 为给定的 `namespace` 和 `repository` 添加 [验证仓库不可变标签](/reference/api/hub/latest/#tag/repositories/operation/VerifyRepositoryImmutableTags) 端点。

---

## 2025-06-27

### 新增

- 为给定的 `namespace` 添加 [列出仓库](/reference/api/hub/latest/#tag/repositories/operation/listNamespaceRepositories) 端点。

### 弃用

- [弃用 /v2/repositories/{namespace}](/reference/api/hub/deprecated/#deprecate-legacy-listnamespacerepositories)

---

## 2025-03-25

### 新增

- 添加用于组织访问令牌（OATs）管理的 [API](/reference/api/hub/latest/#tag/org-access-tokens)。

---

## 2025-03-18

### 新增

- 为组织访问令牌添加访问 [审计日志](/reference/api/hub/latest/#tag/audit-logs) 的功能。
