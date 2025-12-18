---
title: 管理漏洞例外项
description: |
  例外项允许您为漏洞如何影响您的制品提供额外的上下文和文档，
  并提供抑制不适用漏洞的能力
keywords: scout, cves, suppress, vex, exceptions
---

容器镜像中发现的漏洞有时需要额外的上下文信息。仅仅因为镜像包含易受攻击的软件包，
并不意味着该漏洞可以被利用。Docker Scout 中的**例外项**允许您确认可接受的风险
或解决镜像分析中的误报问题。

通过否定不适用的漏洞，您可以更轻松地理解漏洞在镜像上下文中的安全影响，
无论是对您自己还是对镜像的下游使用者而言都是如此。

在 Docker Scout 中，例外项会自动纳入分析结果。如果镜像包含将某个 CVE 标记为
不适用的例外项，则该 CVE 将从分析结果中排除。

## 创建例外项

要为镜像创建例外项，您可以：

- 在 [Docker Scout 仪表板或 Docker Desktop 的 GUI](/manuals/scout/how-tos/create-exceptions-gui.md) 中创建例外项
- 创建 [VEX](/manuals/scout/how-tos/create-exceptions-vex.md) 文档并将其附加到镜像

推荐使用 Docker Scout 仪表板或 Docker Desktop 创建例外项。GUI 提供了用户友好的
界面来创建例外项。它还允许您一次为多个镜像或整个组织创建例外项。

## 查看例外项

要查看镜像的例外项，您需要具备相应的权限。

- 使用 [GUI](/manuals/scout/how-tos/create-exceptions-gui.md) 创建的例外项
  对您 Docker 组织的成员可见。未认证用户或非您组织成员的用户无法看到这些例外项。
- 使用 [VEX 文档](/manuals/scout/how-tos/create-exceptions-vex.md) 创建的例外项
  对任何可以拉取镜像的用户可见，因为 VEX 文档存储在镜像清单或镜像的文件系统中。

### 在 Docker Scout Dashboard 或 Docker Desktop 中查看例外项

Docker Scout 仪表板中漏洞页面的[**例外项**标签页](https://scout.docker.com/reports/vulnerabilities/exceptions)
列出了您组织中所有镜像的所有例外项。在这里，您可以查看每个例外项的更多详细信息、
被抑制的 CVE、例外项适用的镜像、例外项类型及其创建方式等。

对于使用 [GUI](/manuals/scout/how-tos/create-exceptions-gui.md) 创建的例外项，
选择操作菜单可以编辑或删除该例外项。

要查看特定镜像标签的所有例外项：

{{< tabs >}}
{{< tab name="Docker Scout Dashboard" >}}

1. 转到 [Images 页面](https://scout.docker.com/reports/images)。
2. 选择您要检查的标签。
3. 打开 **Exceptions** 标签页。

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 在 Docker Desktop 中打开 **Images** 视图。
2. 打开 **Hub** 标签页。
3. 选择您要检查的标签。
4. 打开 **Exceptions** 标签页。

{{< /tab >}}
{{< /tabs >}}

### 在 CLI 中查看例外项

{{< summary-bar feature_name="Docker Scout exceptions" >}}

当您运行 `docker scout cves <image>` 时，CLI 会高亮显示漏洞例外项。如果某个 CVE
被例外项抑制，则 CVE ID 旁边会显示 `SUPPRESSED` 标签，并显示有关例外项的详细信息。

![CLI 输出中的 SUPPRESSED 标签](/scout/images/suppressed-cve-cli.png)

> [!IMPORTANT]
> 要在 CLI 中查看例外项，您必须将 CLI 配置为使用与创建例外项时相同的 Docker 组织。
>
> 要为 CLI 配置组织，请运行：
>
> ```console
> $ docker scout configure organization <organization>
> ```
>
> 将 `<organization>` 替换为您的 Docker 组织名称。
>
> 您也可以使用 `--org` 标志在每个命令上单独设置组织：
>
> ```console
> $ docker scout cves --org <organization> <image>
> ```

要从输出中排除被抑制的 CVE，请使用 `--ignore-suppressed` 标志：

```console
$ docker scout cves --ignore-suppressed <image>
```