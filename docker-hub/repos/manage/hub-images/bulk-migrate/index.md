---
title: 批量迁移镜像
url: /docker-hub/repos/manage/hub-images/bulk-migrate/
parent:
  title: 镜像管理
  url: /docker-hub/repos/manage/hub-images/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Hub
    url: /docker-hub/
  - title: 仓库
    url: /docker-hub/repos/
  - title: 镜像管理
    url: /docker-hub/repos/manage/hub-images/
  - title: 批量迁移镜像
    url: /docker-hub/repos/manage/hub-images/bulk-migrate/
next:
  title: 在仓库之间移动镜像
  url: /docker-hub/repos/manage/hub-images/move/
---


本指南介绍如何在 Docker Hub 组织或命名空间之间批量迁移 Docker 镜像。无论您是合并仓库、更改组织结构，还是将镜像迁移到新账户，这些技术都能帮助您高效迁移，同时保持镜像完整性。

主题按规模递增进行结构化：

1. [迁移单个镜像标签](#迁移单个镜像标签)
2. [迁移仓库的所有标签](#迁移仓库的所有标签)
3. [迁移多个仓库](#迁移多个仓库)

此工作流的推荐工具是 `crane`。同时展示了使用 `regctl` 的等效替代方案。这两种工具都能在不将镜像拉取到本地的情况下执行注册表到注册表的复制，并保留多架构镜像。

推荐 `crane` 是因为其简单性和专注的镜像复制工作流。`regctl` 也是一个不错的选择，特别是如果您已经使用它进行更广泛的注册表管理任务（超出镜像复制范围）。

> [!NOTE]
>
> 本主题中的主要工作流仅对标记的镜像进行操作。未标记的清单或不再从标签可达的内容不会被迁移。在实践中，这些通常是未使用的工件，但在迁移前请注意此限制。虽然您可以使用[摘要引用](#migrate-by-digest)迁移特定的未标记清单，但没有 API 可以枚举仓库中的未标记清单。

## 先决条件

开始之前，请确保您已满足以下条件：

- 安装了以下工具之一，并且在您的 `$PATH` 中可用：
  - [`crane`](https://github.com/google/go-containerregistry)
  - [`regctl`](https://regclient.org/usage/regctl/)
- 对源组织和目标组织都有推送权限
- 为您选择的工具配置了注册表身份验证

## 向注册表进行身份验证

两种工具都直接向注册表进行身份验证：

- `crane` 使用 Docker 凭证助手和 `~/.docker/config.json`。请参阅 [crane 文档](https://github.com/google/go-containerregistry/tree/main/cmd/crane/doc)。
- `regctl` 使用其自己的配置文件，并且可以导入 Docker 凭证。请参阅 [regctl 文档](https://github.com/regclient/regclient/tree/main/docs)。

请遵循您所选注册表和工具的身份验证说明。

## 迁移单个镜像标签

这是最简单且最常见的迁移场景。

以下示例脚本直接在注册表之间复制镜像清单，并在存在时保留多架构镜像。为您想要迁移的每个标签重复此过程。将环境变量值替换为您的源和目标组织名称、仓库名称和标签。

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC_ORG="oldorg"
DEST_ORG="neworg"
REPO="myapp"
TAG="1.2.3"

SRC_IMAGE="${SRC_ORG}/${REPO}:${TAG}"
DEST_IMAGE="${DEST_ORG}/${REPO}:${TAG}"

# 使用 crane（推荐）
crane cp "${SRC_IMAGE}" "${DEST_IMAGE}"

# 使用 regctl（替代方案）
# regctl image copy "${SRC_IMAGE}" "${DEST_IMAGE}"
```

### 按摘要迁移

要按摘要迁移特定镜像而不是标签，请在源引用中使用摘要。当您需要迁移确切的镜像版本（即使标签已更新）时，这非常有用。将环境变量值替换为您的源和目标组织名称、仓库名称、摘要和标签。您可以在复制操作中选择 `crane` 或 `regctl`。

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC_ORG="oldorg"
DEST_ORG="neworg"
REPO="myapp"
DIGEST="sha256:abcd1234..."
TAG="stable"

SRC_IMAGE="${SRC_ORG}/${REPO}@${DIGEST}"
DEST_IMAGE="${DEST_ORG}/${REPO}:${TAG}"

# 使用 crane
crane cp "${SRC_IMAGE}" "${DEST_IMAGE}"

# 使用 regctl
# regctl image copy "${SRC_IMAGE}" "${DEST_IMAGE}"
```

## 迁移仓库的所有标签

要迁移仓库中的每个标记镜像，请使用 Docker Hub API 枚举标签并复制每个标签。以下示例脚本检索给定仓库的所有标签，并在循环中迁移它们。这种方法可以扩展到具有许多标签的仓库，而不会使本地资源不堪重负。请注意，Docker Hub 请求有速率限制，因此对于大型仓库，您可能需要添加延迟或分页处理。

将环境变量值替换为您的源和目标组织名称和仓库名称。如果您的源仓库是私有的，还需要设置 `HUB_USER` 和 `HUB_TOKEN` 以及具有拉取权限的凭据。您也可以在复制操作中选择 `crane` 或 `regctl`。

```bash
#!/usr/bin/env bash
set -euo pipefail

# 如果设置了环境变量则使用，否则使用默认值
SRC_ORG="${SRC_ORG:-oldorg}"
DEST_ORG="${DEST_ORG:-neworg}"
REPO="${REPO:-myapp}"

# 可选：用于私有仓库
# HUB_USER="your-username"
# HUB_TOKEN="your-access-token"
# AUTH="-u ${HUB_USER}:${HUB_TOKEN}"
AUTH=""

TOOL="crane"   # 或：TOOL="regctl"

TAGS_URL="https://hub.docker.com/v2/repositories/${SRC_ORG}/${REPO}/tags?page_size=100"

while [[ -n "${TAGS_URL}" && "${TAGS_URL}" != "null" ]]; do
  RESP=$(curl -fsSL ${AUTH} "${TAGS_URL}")

  echo "${RESP}" | jq -r '.results[].name' | while read -r TAG; do
    [[ -z "${TAG}" ]] && continue

    SRC_IMAGE="${SRC_ORG}/${REPO}:${TAG}"
    DEST_IMAGE="${DEST_ORG}/${REPO}:${TAG}"

    echo "正在迁移 ${SRC_IMAGE} → ${DEST_IMAGE}"

    case "${TOOL}" in
      crane)
        crane cp "${SRC_IMAGE}" "${DEST_IMAGE}"
        ;;
      regctl)
        regctl image copy "${SRC_IMAGE}" "${DEST_IMAGE}"
        ;;
    esac
  done

  TAGS_URL=$(echo "${RESP}" | jq -r '.next')
done
```

> [!NOTE]
>
> 如果您的账户有权限，Docker Hub 会在首次推送时自动创建目标仓库。

## 迁移多个仓库

要迁移多个仓库，请创建一个列表，并为每个仓库运行单仓库脚本。

例如，创建一个包含仓库名称的 `repos.txt` 文件：

```text
api
web
worker
```

将上一节的脚本保存为 `migrate-single-repo.sh`。然后，运行以下示例脚本，该脚本处理文件中的每个仓库。将环境变量值替换为您的源和目标组织名称。

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC_ORG="oldorg"
DEST_ORG="neworg"

while read -r REPO; do
  [[ -z "${REPO}" ]] && continue
  echo "==== 正在迁移仓库：${REPO}"
  SRC_ORG="${SRC_ORG}" DEST_ORG="${DEST_ORG}" REPO="${REPO}" ./migrate-single-repo.sh
done < repos.txt
```

## 验证迁移完整性

复制后，通过比较摘要来验证源和目标是否匹配。

### 基本摘要验证

以下示例脚本从源和目标检索特定标签的镜像摘要并进行比较。如果摘要匹配，则迁移成功。将环境变量值替换为您的源和目标组织名称、仓库名称和标签。您可以在检索摘要时选择 `crane` 或 `regctl`。

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC_ORG="oldorg"
DEST_ORG="neworg"
REPO="myapp"
TAG="1.2.3"

SRC_IMAGE="${SRC_ORG}/${REPO}:${TAG}"
DEST_IMAGE="${DEST_ORG}/${REPO}:${TAG}"

# 使用 crane
SRC_DIGEST=$(crane digest "${SRC_IMAGE}")
DEST_DIGEST=$(crane digest "${DEST_IMAGE}")

# 使用 regctl（替代方案）
# SRC_DIGEST=$(regctl image digest "${SRC_IMAGE}")
# DEST_DIGEST=$(regctl image digest "${DEST_IMAGE}")

echo "源：      ${SRC_DIGEST}"
echo "目标：    ${DEST_DIGEST}"

if [[ "${SRC_DIGEST}" == "${DEST_DIGEST}" ]]; then
  echo "✓ 迁移已验证：摘要匹配"
else
  echo "✗ 迁移失败：摘要不匹配"
  exit 1
fi
```

### 多架构验证

对于多架构镜像，还需验证清单列表以确保所有平台都已正确复制。将环境变量值替换为您的源和目标组织名称、仓库名称和标签。您可以在检索清单时选择 `crane` 或 `regctl`。

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC_ORG="oldorg"
DEST_ORG="neworg"
REPO="myapp"
TAG="1.2.3"

SRC_IMAGE="${SRC_ORG}/${REPO}:${TAG}"
DEST_IMAGE="${DEST_ORG}/${REPO}:${TAG}"

# 使用 crane
SRC_MANIFEST=$(crane manifest "${SRC_IMAGE}")
DEST_MANIFEST=$(crane manifest "${DEST_IMAGE}")

# 使用 regctl（替代方案）
# SRC_MANIFEST=$(regctl image manifest --format raw-body "${SRC_IMAGE}")
# DEST_MANIFEST=$(regctl image manifest --format raw-body "${DEST_IMAGE}")

# 检查是否为清单列表（多架构）
if echo "${SRC_MANIFEST}" | jq -e '.manifests' > /dev/null 2>&1; then
  echo "检测到多架构镜像"
  
  # 比较平台列表
  SRC_PLATFORMS=$(echo "${SRC_MANIFEST}" | jq -r '.manifests[] | "\(.platform.os)/\(.platform.architecture)"' | sort)
  DEST_PLATFORMS=$(echo "${DEST_MANIFEST}" | jq -r '.manifests[] | "\(.platform.os)/\(.platform.architecture)"' | sort)
  
  if [[ "${SRC_PLATFORMS}" == "${DEST_PLATFORMS}" ]]; then
    echo "✓ 平台列表匹配："
    echo "${SRC_PLATFORMS}"
  else
    echo "✗ 平台列表不匹配"
    echo "源平台："
    echo "${SRC_PLATFORMS}"
    echo "目标平台："
    echo "${DEST_PLATFORMS}"
    exit 1
  fi
else
  echo "单架构镜像"
fi
```

## 完成迁移

迁移镜像后，完成以下附加步骤：

1. 在 Docker Hub UI 中或通过 API 复制仓库元数据：
   - README 内容
   - 仓库描述
   - 主题和标签

2. 配置仓库设置以匹配源：
   - 可见性（公开或私有）
   - 团队权限和访问控制

3. 在目标组织中重新配置集成：
   - Webhook
   - 自动化构建
   - 安全扫描器

4. 更新项目中的镜像引用：
   - 在 Dockerfile 中将 `FROM oldorg/repo:tag` 更改为 `FROM neworg/repo:tag`
   - 更新部署配置
   - 更新文档

5. 弃用旧位置：
   - 更新源仓库描述以指向新位置
   - 考虑在将旧仓库设为私有或只读之前添加宽限期
