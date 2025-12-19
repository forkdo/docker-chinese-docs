---
title: 镜像详情视图
keywords: scout, supply chain, vulnerabilities, packages, cves, image, tag, scan, analysis, analyze
description: Docker Scout 镜像详情视图可分析镜像，展示其层级结构、各层、软件包和漏洞
aliases:
  - /scout/image-details-view
---

镜像详情视图展示了 Docker Scout 分析的细目。您可以从 Docker Scout Dashboard、Docker Desktop 的 **Images** 视图以及 Docker Hub 上的镜像标签页面访问镜像视图。镜像详情展示了镜像层级结构（基础镜像）、镜像层、软件包和漏洞的细目。

![Docker Desktop 中的镜像详情视图](../images/dd-image-view.png)

Docker Desktop 首先在本地分析镜像，生成软件物料清单（SBOM）。Docker Desktop、Docker Hub、Docker Scout Dashboard 和 CLI 都使用此 SBOM 中的 [package URL (PURL) 链接](https://github.com/package-url/purl-spec) 来查询 [Docker Scout 咨询数据库](/manuals/scout/deep-dive/advisory-db-sources.md) 中匹配的常见漏洞和暴露（CVE）。

## 镜像层级结构

您检查的镜像可能有一个或多个基础镜像，显示在 **Image hierarchy** 下。这意味着镜像作者在构建镜像时使用了其他镜像作为起点。这些基础镜像通常是操作系统镜像（如 Debian、Ubuntu 和 Alpine）或编程语言镜像（如 PHP、Python 和 Java）。

选择链中的每个镜像可以查看哪些层源自每个基础镜像。选择 **ALL** 行会选中所有层和基础镜像。

一个或多个基础镜像可能有可用更新，其中可能包含更新的安全补丁，可从您的镜像中移除漏洞。任何有可用更新的基础镜像都会在 **Image hierarchy** 右侧注明。

## 层

Docker 镜像由多层组成。镜像层从上到下列出，最顶层的层在最上面，最新的层在最下面。通常，列表顶部的层源自基础镜像，底部的层由镜像作者添加，通常使用 Dockerfile 中的命令。在 **Image hierarchy** 下选择基础镜像会高亮显示源自该基础镜像的层。

选择单个或多个层会筛选右侧的软件包和漏洞，以显示所选层添加的内容。

## 漏洞

**Vulnerabilities** 选项卡显示在镜像中检测到的漏洞和利用的列表。列表按软件包分组，并按严重性排序。

您可以通过展开列表项来查找有关漏洞或利用的更多信息，包括是否有可用的修复。

## 修复建议

当您在 Docker Desktop 或 Docker Hub 中检查镜像时，Docker Scout 可以提供有关如何提高该镜像安全性的建议。

### Docker Desktop 中的建议

要在 Docker Desktop 中查看镜像的安全建议：

1. 转到 Docker Desktop 中的 **Images** 视图。
2. 选择您要查看建议的镜像标签。
3. 在顶部附近，选择 **Recommended fixes** 下拉按钮。

下拉菜单让您选择是要查看当前镜像的建议，还是查看用于构建它的任何基础镜像的建议：

- [**Recommendations for this image**](#recommendations-for-current-image) 为您正在检查的当前镜像提供建议。
- [**Recommendations for base image**](#recommendations-for-base-image) 为用于构建镜像的基础镜像提供建议。

如果您正在查看的镜像没有关联的基础镜像，下拉菜单仅显示查看当前镜像建议的选项。

### Docker Hub 中的建议

要在 Docker Hub 中查看镜像的安全建议：

1. 转到已激活 Docker Scout 镜像分析的镜像的仓库页面。
2. 打开 **Tags** 选项卡。
3. 选择您要查看建议的标签。
4. 选择 **View recommended base image fixes** 按钮。

   这将打开一个窗口，为您提供有关如何通过使用更好的基础镜像来提高镜像安全性的建议。有关更多详细信息，请参阅 [基础镜像建议](#recommendations-for-base-image)。

### 当前镜像的建议

当前镜像的建议视图帮助您确定您正在使用的镜像版本是否已过时。如果您使用的标签引用了旧的摘要，该视图会显示一个建议，通过拉取最新版本来更新标签。

选择 **Pull new image** 按钮以获取更新的版本。勾选复选框可在拉取最新版本后移除旧版本。

### 基础镜像的建议

基础镜像建议视图包含两个选项卡，用于在不同类型的建议之间切换：

- **Refresh base image**
- **Change base image**

这些基础镜像建议仅在您是正在检查的镜像的作者时才可操作。这是因为更改镜像的基础镜像需要您更新 Dockerfile 并重新构建镜像。

#### 刷新基础镜像

此选项卡显示所选基础镜像标签是否是可用的最新版本，或者是否已过时。

如果用于构建当前镜像的基础镜像标签不是最新的，则两个版本之间的差异将显示在此窗口中。差异信息包括：

- 推荐（较新）版本的标签名称和别名
- 当前基础镜像版本的发布时间
- 最新可用版本的发布时间
- 影响每个版本的 CVE 数量

在窗口底部，您还会收到命令片段，您可以运行这些命令以使用最新版本重新构建镜像。

#### 更改基础镜像

此选项卡显示您可以使用的不同替代标签，并概述每个标签版本的优缺点。选择基础镜像会显示该标签的推荐选项。

例如，如果您正在检查的镜像使用旧版本的 `debian` 作为基础镜像，它会显示推荐使用更新、更安全的 `debian` 版本。通过提供多个备选方案供您选择，您可以自行比较这些选项，并决定使用哪一个。

![基础镜像建议](../images/change-base-image.png)

选择标签建议以查看该建议的更多详细信息。它会显示该标签的优点和潜在缺点、为何推荐它，以及如何更新您的 Dockerfile 以使用此版本。