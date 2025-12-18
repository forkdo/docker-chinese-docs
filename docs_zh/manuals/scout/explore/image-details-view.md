---
title: 镜像详情视图
keywords: scout, supply chain, vulnerabilities, packages, cves, image, tag, scan,
  analysis, analyze
description: Docker Scout 镜像详情视图分析镜像，展示其层次结构、层、软件包和漏洞
aliases:
  - /scout/image-details-view
---

镜像详情视图展示了 Docker Scout 分析的详细分解。您可以通过 Docker Scout 仪表板、Docker Desktop 的 **Images** 视图，以及 Docker Hub 上的镜像标签页面访问此视图。镜像详情展示了镜像的层次结构（基础镜像）、镜像层、软件包和漏洞的详细分解。

![Docker Desktop 中的镜像详情视图](../images/dd-image-view.png)

Docker Desktop 首先在本地分析镜像，生成软件物料清单 (SBOM)。Docker Desktop、Docker Hub 以及 Docker Scout 仪表板和 CLI 都使用此 SBOM 中的 [软件包 URL (PURL) 链接](https://github.com/package-url/purl-spec) 查询 [Docker Scout 的咨询数据库](/manuals/scout/deep-dive/advisory-db-sources.md) 中匹配的通用漏洞与暴露 (CVE)。

## 镜像层次结构

您检查的镜像可能有一个或多个基础镜像，显示在 **Image hierarchy** 下。这意味着镜像作者在构建镜像时使用了其他镜像作为起点。通常，这些基础镜像是操作系统镜像（如 Debian、Ubuntu 和 Alpine），或编程语言镜像（如 PHP、Python 和 Java）。

选择链中的每个镜像，您可以查看哪些层来自每个基础镜像。选择 **ALL** 行将选中所有层和基础镜像。

一个或多个基础镜像可能有可用的更新，这些更新可能包含安全补丁，从而消除镜像中的漏洞。任何有可用更新的基础镜像都会在 **Image hierarchy** 右侧注明。

## 层

Docker 镜像由层组成。镜像层按从上到下（最早层在顶部，最新层在底部）的顺序列出。通常，列表顶部的层来自基础镜像，而底部的层由镜像作者添加，通常使用 Dockerfile 中的命令。在 **Image hierarchy** 下选择基础镜像可以高亮显示哪些层来自该基础镜像。

选择单个或多个层会过滤右侧的软件包和漏洞，显示所选层添加的内容。

## 漏洞

**Vulnerabilities** 标签页显示在镜像中检测到的漏洞和漏洞利用列表。列表按软件包分组，并按严重性排序。

展开列表项可以找到有关漏洞或漏洞利用的进一步信息，包括是否有可用的修复方案。

## 修复建议

当您在 Docker Desktop 或 Docker Hub 中检查镜像时，Docker Scout 可以提供改进该镜像安全性的建议。

### Docker Desktop 中的建议

要在 Docker Desktop 中查看镜像的安全建议：

1. 转到 Docker Desktop 的 **Images** 视图。
2. 选择您要查看建议的镜像标签。
3. 在顶部附近，选择 **Recommended fixes** 下拉按钮。

下拉菜单允许您选择是查看当前镜像还是任何用于构建它的基础镜像的建议：

- [**Recommendations for this image**](#recommendations-for-current-image) 提供当前正在检查的镜像的建议。
- [**Recommendations for base image**](#recommendations-for-base-image) 提供用于构建镜像的基础镜像的建议。

如果正在查看的镜像没有关联的基础镜像，下拉菜单仅显示查看当前镜像建议的选项。

### Docker Hub 中的建议

要在 Docker Hub 中查看镜像的安全建议：

1. 转到已激活 Docker Scout 镜像分析的镜像仓库页面。
2. 打开 **Tags** 标签页。
3. 选择您要查看建议的标签。
4. 选择 **View recommended base image fixes** 按钮。

   这将打开一个窗口，为您提供改进建议，通过使用更好的基础镜像来提高镜像安全性。详见
   [基础镜像建议](#recommendations-for-base-image) 部分。

### 当前镜像的建议

当前镜像建议视图帮助您确定正在使用的镜像版本是否过时。如果使用的标签引用了旧的摘要，视图会显示通过拉取最新版本来更新标签的建议。

选择 **Pull new image** 按钮获取更新版本。勾选复选框可在拉取最新版本后删除旧版本。

### 基础镜像的建议

基础镜像建议视图包含两个标签页，用于在不同类型的建议之间切换：

- **Refresh base image**
- **Change base image**

这些基础镜像建议只有在您是正在检查的镜像的作者时才可操作。这是因为更改镜像的基础镜像需要您更新 Dockerfile 并重新构建镜像。

#### 刷新基础镜像

此标签页显示所选基础镜像标签是否为最新可用版本，或是否已过时。

如果用于构建当前镜像的基础镜像标签不是最新的，则两个版本之间的差异会在此窗口中显示。差异信息包括：

- 推荐（较新）版本的标签名称和别名
- 当前基础镜像版本的发布时间
- 最新可用版本的发布时间
- 每个版本影响的 CVE 数量

在窗口底部，您还会收到可以运行的命令片段，以使用最新版本重新构建镜像。

#### 更改基础镜像

此标签页显示您可以使用的不同替代标签，并概述每个标签版本的优缺点。选择基础镜像会显示该标签的推荐选项。

例如，如果您正在检查的镜像使用旧版本的 `debian` 作为基础镜像，它会推荐更新、更安全的 `debian` 版本供您使用。通过提供多个替代选项，您可以自行比较选项之间的差异，并决定使用哪一个。

![基础镜像建议](../images/change-base-image.png)

选择标签建议以查看建议的更多详细信息。它会显示标签的优点和潜在缺点、推荐原因，以及如何更新您的 Dockerfile 以使用此版本。