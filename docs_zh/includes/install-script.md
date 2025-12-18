### 使用便捷脚本安装

Docker 在 [https://get.docker.com/](https://get.docker.com/) 提供了一个便捷脚本，用于在开发环境中非交互式地安装 Docker。虽然便捷脚本不推荐用于生产环境，但它对于创建符合您需求的配置脚本非常有用。您也可以参考[使用仓库安装](#install-using-the-repository)的步骤，了解如何使用软件包仓库进行安装。该脚本的源代码是开源的，您可以在 GitHub 上的 [`docker-install` 仓库](https://github.com/docker/docker-install) 中找到。

<!-- prettier-ignore -->
在本地运行从互联网下载的脚本之前，请始终检查其内容。安装前，请先熟悉便捷脚本的潜在风险和限制：

- 该脚本需要 `root` 或 `sudo` 权限才能运行。
- 该脚本会尝试检测您的 Linux 发行版和版本，并为您配置包管理系统。
- 该脚本不允许您自定义大多数安装参数。
- 该脚本会自动安装依赖项和推荐项，而无需确认。这可能会根据您主机的当前配置安装大量软件包。
- 默认情况下，该脚本会安装最新稳定版的 Docker、containerd 和 runc。当使用此脚本配置机器时，可能会导致 Docker 意外的主要版本升级。在部署到生产系统之前，请始终先在测试环境中测试升级。
- 该脚本不是为升级现有 Docker 安装而设计的。当使用该脚本更新现有安装时，依赖项可能不会升级到预期版本，从而导致版本过时。

> [!TIP]
>
> 运行前预览脚本步骤。您可以使用 `--dry-run` 选项运行脚本，以了解脚本被调用时将执行哪些步骤：
>
> ```console
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh ./get-docker.sh --dry-run
> ```

此示例从 [https://get.docker.com/](https://get.docker.com/) 下载脚本，并在 Linux 上运行它以安装最新稳定版的 Docker：

```console
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```

现在您已成功安装并启动了 Docker Engine。在基于 Debian 的发行版中，`docker` 服务会自动启动。在基于 `RPM` 的发行版（如 CentOS、Fedora 或 RHEL）中，您需要使用适当的 `systemctl` 或 `service` 命令手动启动它。如消息所示，默认情况下非 root 用户无法运行 Docker 命令。

> **以非特权用户身份使用 Docker，或以无根模式安装？**
>
> 安装脚本需要 `root` 或 `sudo` 权限才能安装和使用 Docker。如果您想授予非 root 用户访问 Docker 的权限，请参考 [Linux 的安装后步骤](/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)。您也可以在无需 `root` 权限的情况下安装 Docker，或配置为以无根模式运行。有关以无根模式运行 Docker 守护进程的说明，请参考 [以非 root 用户身份运行 Docker 守护进程（无根模式）](/engine/security/rootless/)。

#### 安装预发布版本

Docker 还在 [https://test.docker.com/](https://test.docker.com/) 提供了一个便捷脚本，用于在 Linux 上安装 Docker 的预发布版本。此脚本与 `get.docker.com` 上的脚本相同，但它配置您的包管理器使用 Docker 软件包仓库的测试频道。测试频道包含 Docker 的稳定版和预发布版本（测试版、发布候选版）。使用此脚本可以提前访问新版本，并在它们作为稳定版发布之前在测试环境中评估它们。

要从测试频道在 Linux 上安装最新版本的 Docker，请运行：

```console
$ curl -fsSL https://test.docker.com -o test-docker.sh
$ sudo sh test-docker.sh
```

#### 使用便捷脚本安装后升级 Docker

如果您使用便捷脚本安装了 Docker，则应直接使用您的包管理器升级 Docker。重新运行便捷脚本没有任何优势。如果它尝试重新安装主机上已存在的仓库，重新运行可能会导致问题。