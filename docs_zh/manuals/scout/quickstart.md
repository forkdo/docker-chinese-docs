---
title: Docker Scout 快速入门
linkTitle: 快速入门
weight: 20
keywords: scout, supply chain, vulnerabilities, packages, cves, scan, analysis, analyze
description: 了解如何开始使用 Docker Scout 分析镜像并修复漏洞
---

Docker Scout 会分析镜像内容，并生成详细的报告，列出检测到的软件包和漏洞。
它还能为你提供修复建议，帮助你解决镜像分析中发现的问题。

本指南将带你分析一个存在漏洞的容器镜像，展示如何使用 Docker Scout 识别并修复漏洞，对比镜像版本随时间的变化，并与团队共享结果。

## 步骤 1：准备工作

[本示例项目](https://github.com/docker/scout-demo-service) 包含一个存在漏洞的 Node.js 应用，你可以使用它来跟随本指南操作。

1. 克隆仓库：

   ```console
   $ git clone https://github.com/docker/scout-demo-service.git
   ```

2. 进入目录：

   ```console
   $ cd scout-demo-service
   ```

3. 确保你已登录 Docker 账户，可通过运行 `docker login` 命令或使用 Docker Desktop 登录。

4. 构建镜像并推送到 `<ORG_NAME>/scout-demo:v1`，其中 `<ORG_NAME>` 是你要推送到的 Docker Hub 命名空间。

   ```console
   $ docker build --push -t <ORG_NAME>/scout-demo:v1 .
   ```

## 步骤 2：启用 Docker Scout

Docker Scout 默认会分析所有本地镜像。要分析远程仓库中的镜像，你需要先启用它。你可以通过 Docker Hub、Docker Scout 仪表板或 CLI 来启用。[在概述指南中了解如何操作](/scout)。

1. 使用 `docker login` 命令登录 Docker 账户，或使用 Docker Desktop 中的 **Sign in** 按钮。

2. 接下来，使用 `docker scout enroll` 命令为你的组织注册 Docker Scout。

   ```console
   $ docker scout enroll <ORG_NAME>
   ```

3. 使用 `docker scout repo enable` 命令为你的镜像仓库启用 Docker Scout。

   ```console
   $ docker scout repo enable --org <ORG_NAME> <ORG_NAME>/scout-demo
   ```

## 步骤 3：分析镜像漏洞

构建完成后，使用 `docker scout` CLI 命令查看 Docker Scout 检测到的漏洞。

本指南的示例应用使用了存在漏洞的 Express 版本。以下命令显示镜像中影响 Express 的所有 CVE：

```console
$ docker scout cves --only-package express
```

Docker Scout 默认分析最近构建的镜像，因此在这种情况下无需指定镜像名称。

在 [CLI 参考文档](/reference/cli/docker/scout/cves) 中了解 `docker scout cves` 命令的更多信息。

## 步骤 4：修复应用漏洞

经过 Docker Scout 分析后，发现了一个高危漏洞 CVE-2022-24999，它是由 **express** 软件包的旧版本引起的。

express 软件包的 4.17.3 版本修复了该漏洞。因此，将 `package.json` 文件更新到新版本：

   ```diff
      "dependencies": {
   -    "express": "4.17.1"
   +    "express": "4.17.3"
      }
   ```
   
使用新标签重新构建镜像并推送到 Docker Hub 仓库：

   ```console
   $ docker build --push -t <ORG_NAME>/scout-demo:v2 .
   ```

再次运行 `docker scout` 命令，验证高危漏洞 CVE-2022-24999 已不再存在：

```console
$ docker scout cves --only-package express
    ✓ Provenance obtained from attestation
    ✓ Image stored for indexing
    ✓ Indexed 79 packages
    ✓ No vulnerable package detected


  ## Overview

                      │                  Analyzed Image                   
  ────────────────────┼───────────────────────────────────────────────────
    Target            │  mobywhale/scout-demo:v2                   
      digest          │  ef68417b2866                                     
      platform        │ linux/arm64                                       
      provenance      │ https://github.com/docker/scout-demo-service.git  
                      │  7c3a06793fc8f97961b4a40c73e0f7ed85501857         
      vulnerabilities │    0C     0H     0M     0L                        
      size            │ 19 MB                                             
      packages        │ 1                                                 


  ## Packages and Vulnerabilities

  No vulnerable packages detected

```

## 步骤 5：评估策略合规性

虽然基于特定软件包检查漏洞很有用，但这并不是改善供应链安全的最有效方法。

Docker Scout 还支持策略评估，这是一种更高级的概念，用于检测和修复镜像中的问题。策略是一组可自定义的规则，让组织能够跟踪镜像是否符合其供应链要求。

由于策略规则对每个组织都是特定的，你必须指定要评估哪个组织的策略。使用 `docker scout config` 命令配置你的 Docker 组织。

```console
$ docker scout config organization <ORG_NAME>
    ✓ Successfully set organization to <ORG_NAME>
```

现在你可以运行 `quickview` 命令，获取刚刚构建的镜像的合规性概览。镜像将根据默认策略配置进行评估。你会看到类似以下的输出：

```console
$ docker scout quickview

...
Policy status  FAILED  (2/6 policies met, 2 missing data)

  Status │                  Policy                      │           Results
─────────┼──────────────────────────────────────────────┼──────────────────────────────
  ✓      │ No copyleft licenses                         │    0 packages
  !      │ Default non-root user                        │
  !      │ No fixable critical or high vulnerabilities  │    2C    16H     0M     0L
  ✓      │ No high-profile vulnerabilities              │    0C     0H     0M     0L
  ?      │ No outdated base images                      │    No data
  ?      │ Supply chain attestations                    │    No data
```

状态列中的感叹号表示违反的策略。问号表示没有足够的元数据来完成评估。勾号表示合规。

## 步骤 6：改善合规性

`quickview` 命令的输出显示还有改进空间。一些策略未能成功评估（`No data`），因为镜像缺少来源和 SBOM 证明。镜像在几个评估中也未能通过。

策略评估不仅仅是检查漏洞。以 `Default non-root user` 策略为例。该策略通过确保镜像默认不以 `root` 超级用户身份运行来提高运行时安全性。

要解决此策略违规，编辑 Dockerfile，添加 `USER` 指令，指定非 root 用户：

```diff
  CMD ["node","/app/app.js"]
  EXPOSE 3000
+ USER appuser
```

此外，为了获得更完整的策略评估结果，你的镜像应附带 SBOM 和来源证明。Docker Scout 使用来源证明来确定镜像的构建方式，从而提供更好的评估结果。

在使用证明构建镜像之前，你必须启用 [containerd 镜像存储](/manuals/desktop/features/containerd.md)（或使用 `docker-container` 驱动创建自定义构建器）。经典镜像存储不支持清单列表，而清单列表是来源证明附加到镜像的方式。

在 Docker Desktop 中打开 **Settings**。在 **General** 部分下，确保选中 **Use containerd for pulling and storing images** 选项，然后选择 **Apply**。请注意，更改镜像存储会暂时隐藏非活动镜像存储的镜像和容器，直到你切换回来。

启用 containerd 镜像存储后，使用新的 `v3` 标签重新构建镜像。这次，添加 `--provenance=true` 和 `--sbom=true` 标志。

```console
$ docker build --provenance=true --sbom=true --push -t <ORG_NAME>/scout-demo:v3 .
```

## 步骤 7：在仪表板中查看

推送带有证明的更新镜像后，是时候通过另一个视角查看结果：Docker Scout 仪表板。

1. 打开 [Docker Scout 仪表板](https://scout.docker.com/)。
2. 使用你的 Docker 账户登录。
3. 在左侧导航中选择 **Images**。

镜像页面列出你的 Scout 启用的仓库。

在行中除链接外的任何位置选择要查看的镜像行，打开 **Image details** 侧边栏。

侧边栏显示仓库最后推送标签的合规性概览。

> [!NOTE]
>
> 如果策略结果尚未出现，请尝试刷新页面。如果是首次使用 Docker Scout 仪表板，可能需要几分钟才能显示结果。

返回镜像列表，选择 **Most recent image** 列中的镜像版本。然后，在页面右上角选择 **Update base image** 按钮检查策略。

此策略检查你使用的基础镜像是否最新。它当前状态为不合规，因为示例镜像使用了旧版本的 `alpine` 作为基础镜像。

关闭 **Recommended fixes for base image** 模态框。在策略列表中，选择策略名称旁边的 **View fixes** 按钮，查看违规详情以及如何解决的建议。

在这种情况下，建议的操作是启用 [Docker Scout 的 GitHub 集成](./integrations/source-code-management/github.md)，它能帮助你自动保持基础镜像最新。

> [!TIP]
>
> 你无法为本指南中使用的演示应用启用此集成。可以随意将代码推送到你拥有的 GitHub 仓库，在那里尝试该集成！

## 总结

本快速入门指南简要介绍了 Docker Scout 支持软件供应链管理的一些方式：

- 如何为仓库启用 Docker Scout
- 分析镜像漏洞
- 策略和合规性
- 修复漏洞并改善合规性

## 接下来学什么？

还有更多内容等待探索，从第三方集成到策略自定义，以及运行时环境的实时监控。

查看以下部分：

- [镜像分析](/manuals/scout/explore/analysis.md)
- [数据源](/scout/advisory-db-sources)
- [Docker Scout 仪表板](/scout/dashboard)
- [集成](./integrations/_index.md)
- [策略评估](./policy/_index.md)