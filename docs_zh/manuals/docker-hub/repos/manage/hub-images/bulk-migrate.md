---
title: 批量迁移 Docker 镜像
description: 了解如何使用脚本和自动化在组织之间批量迁移 Docker 镜像和标签。
keywords: docker hub, 迁移, 批量, 镜像, 标签, 多架构, buildx
---

本指南展示了如何在 Docker Hub 组织或命名空间之间批量迁移 Docker 镜像。无论您是要合并仓库、更改组织结构，还是将镜像移动到新账户，这些技术都能帮助您高效迁移，同时保持镜像完整性。

## 前置条件

开始之前，请确保您已具备：

- 安装 Docker CLI 20.10 或更高版本
- Docker Buildx（可选，但推荐用于多架构镜像）
- 对源组织和目标组织的推送权限
- 安装 `jq` 用于脚本中的 JSON 解析
- `curl` 用于 API 调用

## 身份验证到 Docker Hub

登录 Docker Hub 以验证您的会话：

```console
$ docker login
```

提示时输入您的凭据。此身份验证在您的会话期间持续有效，可防止限流问题。

## 迁移单个镜像标签

迁移单个镜像标签的基本工作流包括三个步骤：拉取、标记和推送。

1. 设置源和目标变量：

   ```bash
   SRC_ORG=oldorg
   DEST_ORG=neworg
   REPO=myapp
   TAG=1.2.3
   ```

2. 从源组织拉取镜像：

   ```console
   $ docker pull ${SRC_ORG}/${REPO}:${TAG}
   ```

3. 为镜像标记目标组织：

   ```console
   $ docker tag ${SRC_ORG}/${REPO}:${TAG} ${DEST_ORG}/${REPO}:${TAG}
   ```

4. 将镜像推送到目标组织：

   ```console
   $ docker push ${DEST_ORG}/${REPO}:${TAG}
   ```

对需要迁移的任何其他标签重复这些步骤，包括适用的 `latest` 标签。

## 迁移仓库的所有标签

要迁移单个仓库的所有标签，请使用此脚本，它查询 Docker Hub API 并处理每个标签：

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC_ORG="oldorg"
DEST_ORG="neworg"
REPO="myapp"

# 分页遍历标签
TAGS_URL="https://hub.docker.com/v2/repositories/${SRC_ORG}/${REPO}/tags?page_size=100"
while [[ -n "${TAGS_URL}" && "${TAGS_URL}" != "null" ]]; do
  RESP=$(curl -fsSL "${TAGS_URL}")
  echo "${RESP}" | jq -r '.results[].name' | while read -r TAG; do
    echo "==> 迁移 ${SRC_ORG}/${REPO}:${TAG} → ${DEST_ORG}/${REPO}:${TAG}"
    docker pull "${SRC_ORG}/${REPO}:${TAG}"
    docker tag  "${SRC_ORG}/${REPO}:${TAG}" "${DEST_ORG}/${REPO}:${TAG}"
    docker push "${DEST_ORG}/${REPO}:${TAG}"
  done
  TAGS_URL=$(echo "${RESP}" | jq -r '.next')
done
```

当仓库有超过 100 个标签时，此脚本会自动处理分页。

> [!NOTE]
>
> 如果您的账户有必要的权限，Docker Hub 会在首次推送时自动创建目标仓库。

### 迁移私有仓库标签

对于私有仓库，请使用 Docker Hub 访问令牌验证您的 API 调用：

1. 在您的 [Docker Hub 账户设置](https://hub.docker.com/settings/security) 中创建个人访问令牌。

2. 将您的凭据设置为变量：

   ```bash
   HUB_USER="your-username"
   HUB_TOKEN="your-access-token"
   ```

3. 修改脚本中的 `curl` 命令以包含身份验证：

   ```bash
   RESP=$(curl -fsSL -u "${HUB_USER}:${HUB_TOKEN}" "${TAGS_URL}")
   ```

> [!IMPORTANT]
>
> 如果遇到拉取限流或吞吐量限制，请保持 `docker login` 活跃以避免匿名拉取。如果迁移大量镜像，请考虑添加节流或谨慎的并行化。

## 迁移多个仓库

要一次迁移多个仓库，请创建仓库名称列表并在循环中处理它们。

1. 创建一个名为 `repos.txt` 的文件，每行一个仓库名称：

   ```text
   api
   web
   worker
   database
   ```

2. 将上一节中的单仓库脚本保存为 `migrate-single-repo.sh` 并使其可执行。

3. 使用此包装脚本处理所有仓库：

   ```bash
   #!/usr/bin/env bash
   set -euo pipefail

   SRC_ORG="oldorg"
   DEST_ORG="neworg"

   while read -r REPO; do
     [[ -z "${REPO}" ]] && continue
     echo "==== 迁移仓库: ${REPO}"
     export REPO
     ./migrate-single-repo.sh
   done < repos.txt
   ```

## 保留多架构镜像

标准 `docker pull` 仅检索当前平台的镜像。对于多架构镜像，此方法会丢失其他平台变体。

### 使用 Buildx imagetools（推荐）

推荐的方法是使用 Buildx 复制完整清单，而无需在本地拉取镜像：

```console
$ docker buildx imagetools create \
  -t ${DEST_ORG}/${REPO}:${TAG} \
     ${SRC_ORG}/${REPO}:${TAG}
```

此命令将源清单（包含所有平台）直接复制到目标标签。

通过检查两个清单来验证迁移：

```console
$ docker buildx imagetools inspect ${SRC_ORG}/${REPO}:${TAG}
$ docker buildx imagetools inspect ${DEST_ORG}/${REPO}:${TAG}
```

比较输出以确认它们匹配。

### 手动清单创建

如果您需要对多架构镜像使用拉取/标记/推送工作流，则必须拉取每个平台变体并使用 `docker manifest create` 和 `docker manifest push` 重建清单。此方法比使用 Buildx imagetools 更慢且更容易出错。

## 验证迁移完整性

迁移镜像后，验证它们是否正确传输。

### 单架构镜像

比较源和目标之间的镜像摘要：

```console
$ docker pull ${SRC_ORG}/${REPO}:${TAG}
$ docker inspect --format='{{index .RepoDigests 0}}' ${SRC_ORG}/${REPO}:${TAG}

$ docker pull ${DEST_ORG}/${REPO}:${TAG}
$ docker inspect --format='{{index .RepoDigests 0}}' ${DEST_ORG}/${REPO}:${TAG}
```

如果迁移成功，SHA256 摘要应该匹配。

### 多架构镜像

对于多架构镜像，比较 Buildx imagetools 的输出：

```console
$ docker buildx imagetools inspect ${SRC_ORG}/${REPO}:${TAG}
$ docker buildx imagetools inspect ${DEST_ORG}/${REPO}:${TAG}
```

验证源和目标之间的平台和清单摘要是否匹配。

## 完成迁移

迁移镜像后，完成以下附加步骤：

1. 在 Docker Hub UI 或通过 API 复制仓库元数据：

   - README 内容
   - 仓库描述
   - 话题和标签

2. 配置仓库设置以匹配源：

   - 可见性（公开或私有）
   - 团队权限和访问控制

3. 在目标组织中重新配置集成：

   - Webhook
   - 自动构建
   - 安全扫描器

4. 更新项目中的镜像引用：

   - 在 Dockerfile 中将 `FROM oldorg/repo:tag` 更改为 `FROM neworg/repo:tag`
   - 更新部署配置
   - 更新文档

5. 停用旧位置：
   - 更新源仓库描述以指向新位置
   - 考虑在将旧仓库设为私有或只读之前设置宽限期