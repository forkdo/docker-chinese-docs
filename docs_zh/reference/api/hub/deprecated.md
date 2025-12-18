---
description: 已弃用的 Docker Hub API 端点
keywords: 弃用
title: 已弃用的 Docker Hub API 端点
linkTitle: 已弃用
weight: 3
aliases:
    - /docker-hub/api/deprecated/
---

本页面概述了 Docker Hub API 中已弃用的端点。

## 端点弃用策略

随着 Docker 的变化，有时需要移除或替换现有端点。在移除现有端点之前，会在文档中标记为“已弃用”。一段时间后，该端点可能会被移除。

## 已弃用的端点

下表概述了当前已弃用端点的状态：

**已弃用 (Deprecated)**：端点已标记为“已弃用”，不应再使用。  
该端点可能在未来的版本中被移除、禁用或更改行为。

**已移除 (Removed)**：端点已被移除、禁用或隐藏。

---

| 状态       | 功能                                                                                              | 日期       |
|------------|---------------------------------------------------------------------------------------------------|------------|
| 已弃用     | [弃用未记录的创建/获取仓库端点](#deprecate-legacy-createrepository-and-getrepository)             | 2025-09-19 |
| 已弃用     | [弃用 /v2/repositories/{namespace}](#deprecate-legacy-listnamespacerepositories)                  | 2025-06-27 |
|            | [创建弃用日志表](#create-deprecation-log-table)                                                   | 2025-06-27 |
| 已移除     | [Docker Hub API v1 弃用](#docker-hub-api-v1-deprecation)                                          | 2022-08-23 |

---

### 弃用旧版 CreateRepository 和 GetRepository

弃用未记录的端点：
- `POST /v2/repositories` 和 `POST /v2/repositories/{namespace}` 被 [创建仓库](/reference/api/hub/latest/#tag/repositories/operation/CreateRepository) 替代
- `GET /v2/repositories/{namespace}/{repository}` 被 [获取仓库](/reference/api/hub/latest/#tag/repositories/operation/GetRepository) 替代
- `HEAD /v2/repositories/{namespace}/{repository}` 被 [检查仓库](/reference/api/hub/latest/#tag/repositories/operation/CheckRepository) 替代

---

### 弃用旧版 ListNamespaceRepositories

弃用未记录的端点 `GET /v2/repositories/{namespace}`，被 [列出仓库](/reference/api/hub/latest/#tag/repositories/operation/listNamespaceRepositories) 替代。

---

### 创建弃用日志表

重新整理页面

---

### Docker Hub API v1 弃用

Docker Hub API v1 已被弃用。请改用 Docker Hub API v2。

v1 路径中的以下 API 路由将不再工作，并返回 410 状态码：
* `/v1/repositories/{name}/images`
* `/v1/repositories/{name}/tags`
* `/v1/repositories/{name}/tags/{tag_name}`
* `/v1/repositories/{namespace}/{name}/images`
* `/v1/repositories/{namespace}/{name}/tags`
* `/v1/repositories/{namespace}/{name}/tags/{tag_name}`

如果您想在当前应用程序中继续使用 Docker Hub API，请将客户端更新为使用 v2 端点。

| **旧版**                                                                                                                                                              | **新版**                                                                                                                                   |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| [/v1/repositories/{name}/tags](https://github.com/moby/moby/blob/v1.8.3/docs/reference/api/registry_api.md#list-repository-tags)                                     | [/v2/namespaces/{namespace}/repositories/{repository}/tags](/reference/api/hub/latest/#tag/repositories/operation/ListRepositoryTags)     |
| [/v1/repositories/{namespace}/{name}/tags](https://github.com/moby/moby/blob/v1.8.3/docs/reference/api/registry_api.md#list-repository-tags)                         | [/v2/namespaces/{namespace}/repositories/{repository}/tags](/reference/api/hub/latest.md/#tag/repositories/operation/ListRepositoryTags)  |
| [/v1/repositories/{namespace}/{name}/tags](https://github.com/moby/moby/blob/v1.8.3/docs/reference/api/registry_api.md#get-image-id-for-a-particular-tag)            | [/v2/namespaces/{namespace}/repositories/{repository}/tags/{tag}](/reference/api/hub/latest/#tag/repositories/operation/GetRepositoryTag) |
| [/v1/repositories/{namespace}/{name}/tags/{tag_name}](https://github.com/moby/moby/blob/v1.8.3/docs/reference/api/registry_api.md#get-image-id-for-a-particular-tag) | [/v2/namespaces/{namespace}/repositories/{repository}/tags/{tag}](/reference/api/hub/latest/#tag/repositories/operation/GetRepositoryTag) |