---
title: 管理漏洞例外
description: |
  例外允许您为漏洞如何影响您的制品提供额外的上下文和文档，并提供抑制不适用漏洞的能力
keywords: scout, cves, suppress, vex, exceptions
---

容器镜像中发现的漏洞有时需要额外的上下文。
仅仅因为镜像包含一个有漏洞的软件包，并不意味着该漏洞可被利用。Docker Scout 中的**例外**允许您确认已接受的风险或解决镜像分析中的误报。

通过否定不适用的漏洞，您可以更轻松地理解漏洞在镜像上下文中的安全影响，并帮助您和镜像的下游消费者更好地理解这些影响。

在 Docker Scout 中，例外会自动纳入分析结果。如果镜像包含将 CVE 标记为不适用的例外，则该 CVE 会从分析结果中排除。

## 创建例外

要为镜像创建例外，您可以：

- 在 [Docker Scout 仪表板](/manuals/scout/how-tos/create-exceptions-gui.md) 或 Docker Desktop 的 GUI 中创建例外。
- 创建 [VEX](/manuals/scout/how-tos/create-exceptions-vex.md) 文档并将其附加到镜像。

推荐的创建例外方式是使用 Docker Scout 仪表板或 Docker Desktop。GUI 提供了用户友好的界面来创建例外。它还允许您为多个镜像或整个组织一次性创建例外。

## 查看例外

要查看镜像的例外，您需要具备适当的权限。

- 使用 [GUI](/manuals/scout/how-tos/create-exceptions-gui.md) 创建的例外对您的 Docker 组织成员可见。未认证用户或非您组织成员的用户无法看到这些例外。
- 使用 [VEX 文档](/manuals/scout/how-tos/create-exceptions-vex.md) 创建的例外对任何可以拉取镜像的用户可见，因为 VEX 文档存储在镜像清单或镜像的文件系统中。

### 在 Docker Scout 仪表板或 Docker Desktop 中查看例外

Docker Scout 仪表板中漏洞页面的 **Exceptions** 选项卡列出了您组织中所有镜像的所有例外。在这里，您可以查看每个例外的更多详细信息、被抑制的 CVE、例外适用的镜像、例外类型和创建方式等。

对于使用 [GUI](/manuals/scout/how-tos/create-exceptions-gui.md) 创建的例外，选择操作菜单可以编辑或删除例外。

要查看特定镜像标签的所有例外：

{{< tabs >}}
{{< tab name="Docker Scout Dashboard" >}}

1. 转到 [Images 页面](https://scout.docker.com/reports/images)。
2. 选择您要检查的标签。
3. 打开 **Exceptions** 选项卡。

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 在 Docker Desktop 中打开 **Images** 视图。
2. 打开 **Hub** 选项卡。
3. 选择您要检查的标签。
4. 打开 **Exceptions** 选项卡。

{{< /tab >}}
{{< /tabs >}}

### 在 CLI 中查看例外

{{< summary-bar feature_name="Docker Scout exceptions" >}}

当您运行 `docker scout cves <image>` 时，CLI 中会突出显示漏洞例外。如果 CVE 被例外抑制，CVE ID 旁边会显示 `SUPPRESSED` 标签。还会显示有关例外的详细信息。

![CLI 输出中的 SUPPRESSED 标签](/scout/images/suppressed-cve-cli.png)

> [!IMPORTANT]
> 要在 CLI 中查看例外，您必须将 CLI 配置为使用与创建例外相同的 Docker 组织。
>
> 要为 CLI 配置组织，请运行：
>
> ```console
> $ docker scout configure organization <organization>
> ```
>
> 将 `<organization>` 替换为您的 Docker 组织名称。
>
> 您也可以使用 `--org` 标志为每个命令单独设置组织：
>
> ```console
> $ docker scout cves --org <organization> <image>
> ```

要从输出中排除被抑制的 CVE，请使用 `--ignore-suppressed` 标志：

```console
$ docker scout cves --ignore-suppressed <image>
```