# 批量迁移 Docker 镜像

本指南介绍如何在 Docker Hub 组织或命名空间之间批量迁移 Docker 镜像。无论您是要整合仓库、更改组织结构，还是将镜像迁移到新账户，这些技术都能帮助您高效迁移，同时保持镜像完整性。

## 先决条件

开始之前，请确保您已具备：

- 已安装 Docker CLI 20.10 或更高版本
- Docker Buildx（可选，但推荐用于多架构镜像）
- 对源组织和目标组织的推送权限
- 已安装 `jq`，用于脚本中的 JSON 解析
- 用于 API 调用的 `curl`

## 验证 Docker Hub 登录状态

登录 Docker Hub 以验证您的会话：

```console
$ docker login
```

按提示输入您的凭据。此身份验证会在您的会话期间持续有效，并防止速率限制问题。

## 迁移单个镜像标签

迁移单个镜像标签的基本工作流程包括三个步骤：拉取、标记和推送。

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

3. 为目标组织标记镜像：

   ```console
   $ docker tag ${SRC_ORG}/${REPO}:${TAG} ${DEST_ORG}/${REPO}:${TAG}
   ```

4. 将镜像推送到目标组织：

   ```console
   $ docker push ${DEST_ORG}/${REPO}:${TAG}
   ```

对需要迁移的任何其他标签重复这些步骤，包括适用的 `latest` 标签。

## 迁移仓库的所有标签

要迁移单个仓库的所有标签，请使用此脚本，它会查询 Docker Hub API 并处理每个标签：

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC_ORG="oldorg"
DEST_ORG="neworg"
REPO="myapp"

# 分页处理标签
TAGS_URL="https://hub.docker.com/v2/repositories/${SRC_ORG}/${REPO}/tags?page_size=100"
while [[ -n "${TAGS_URL}" && "${TAGS_URL}" != "null" ]]; do
  RESP=$(curl -fsSL "${TAGS_URL}")
  echo "${RESP}" | jq -r '.results[].name' | while read -r TAG; do
    echo "==> Migrating ${SRC_ORG}/${REPO}:${TAG} → ${DEST_ORG}/${REPO}:${TAG}"
    docker pull "${SRC_ORG}/${REPO}:${TAG}"
    docker tag  "${SRC_ORG}/${REPO}:${TAG}" "${DEST_ORG}/${REPO}:${TAG}"
    docker push "${DEST_ORG}/${REPO}:${TAG}"
  done
  TAGS_URL=$(echo "${RESP}" | jq -r '.next')
done
```

当仓库的标签超过 100 个时，此脚本会自动处理分页。

> [!NOTE]
>
> 如果您的账户具有必要的权限，Docker Hub 会在首次推送时自动创建目标仓库。

### 迁移私有仓库标签

对于私有仓库，请使用 Docker Hub 访问令牌对您的 API 调用进行身份验证：

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
> 如果遇到拉取速率或吞吐量限制，请保持 `docker login` 处于活动状态以避免匿名拉取。如果迁移大量镜像，请考虑添加限流或仔细的并行化处理。

## 迁移多个仓库

要一次性迁移多个仓库，请创建一个仓库名称列表并在循环中处理它们。

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
     echo "==== Migrating repo: ${REPO}"
     export REPO
     ./migrate-single-repo.sh
   done < repos.txt
   ```

## 保留多架构镜像

标准的 `docker pull` 仅检索当前平台的镜像。对于多架构镜像，这种方法会丢失其他平台的变体。

### 使用 Buildx imagetools（推荐）

推荐的方法是使用 Buildx 复制完整的清单，而无需在本地拉取镜像：

```console
$ docker buildx imagetools create \
  -t ${DEST_ORG}/${REPO}:${TAG} \
     ${SRC_ORG}/${REPO}:${TAG}
```

此命令将包含所有平台的源清单直接复制到目标标签。

通过检查两个清单来验证迁移：

```console
$ docker buildx imagetools inspect ${SRC_ORG}/${REPO}:${TAG}
$ docker buildx imagetools inspect ${DEST_ORG}/${REPO}:${TAG}
```

比较输出中的平台和摘要以确认它们匹配。

### 手动创建清单

如果您需要对多架构镜像使用拉取/标记/推送工作流程，则必须拉取每个平台变体，并使用 `docker manifest create` 和 `docker manifest push` 重新创建清单。这种方法比使用 Buildx imagetools 更慢且更容易出错。

## 验证迁移完整性

迁移镜像后，请验证它们是否正确传输。

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

迁移镜像后，请完成以下附加步骤：

1. 在 Docker Hub UI 中或通过 API 复制仓库元数据：

   - README 内容
   - 仓库描述
   - 主题和标签

2. 配置仓库设置以匹配源：

   - 可见性（公共或私有）
   - 团队权限和访问控制

3. 在目标组织中重新配置集成：

   - Webhook
   - 自动构建
   - 安全扫描器

4. 更新项目中的镜像引用：

   - 在 Dockerfile 中将 `FROM oldorg/repo:tag` 更改为 `FROM neworg/repo:tag`
   - 更新部署配置
   - 更新文档

5. 弃用旧位置：
   - 更新源仓库描述以指向新位置
   - 考虑在将旧仓库设为私有或只读之前设置宽限期
