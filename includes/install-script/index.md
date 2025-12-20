# 
### 使用便捷脚本安装

Docker 提供了一个便捷脚本，位于 [https://get.docker.com/](https://get.docker.com/)，用于以非交互方式将 Docker 安装到开发环境中。该便捷脚本不推荐用于生产环境，但对于创建符合您需求的配置脚本很有用。另请参阅[使用仓库安装](#install-using-the-repository)步骤，了解使用软件包仓库进行安装的相关步骤。该脚本的源代码是开源的，您可以在 GitHub 上的 [`docker-install` 仓库](https://github.com/docker/docker-install) 中找到它。

<!-- prettier-ignore -->
在本地运行从互联网下载的脚本之前，请务必仔细检查。在安装之前，请熟悉便捷脚本的潜在风险和限制：

- 该脚本需要 `root` 或 `sudo` 权限才能运行。
- 该脚本会尝试检测您的 Linux 发行版和版本，并为您配置包管理系统。
- 该脚本不允许您自定义大多数安装参数。
- 该脚本会安装依赖项和推荐包，而不会要求确认。根据主机机器的当前配置，这可能会安装大量软件包。
- 默认情况下，该脚本会安装 Docker、containerd 和 runc 的最新稳定版本。使用此脚本配置机器时，可能会导致 Docker 意外地进行主要版本升级。在将升级部署到生产系统之前，请务必在测试环境中测试升级。
- 该脚本并非用于升级现有的 Docker 安装。使用该脚本更新现有安装时，依赖项可能不会更新到预期版本，从而导致版本过时。

> [!TIP]
>
> 在运行脚本之前预览脚本步骤。您可以使用 `--dry-run` 选项运行脚本，以了解脚本被调用时将运行的步骤：
>
> ```console
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh ./get-docker.sh --dry-run
> ```

此示例从 [https://get.docker.com/](https://get.docker.com/) 下载脚本并运行它，以在 Linux 上安装 Docker 的最新稳定版本：

```console
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```

现在，您已成功安装并启动了 Docker 引擎。基于 Debian 的发行版会自动启动 `docker` 服务。在基于 `RPM` 的发行版（如 CentOS、Fedora 或 RHEL）上，您需要使用适当的 `systemctl` 或 `service` 命令手动启动它。如消息所示，默认情况下，非 root 用户无法运行 Docker 命令。

> **以非特权用户使用 Docker，或以无根模式安装？**
>
> 安装脚本需要 `root` 或 `sudo` 权限才能安装和使用 Docker。如果您想授予非 root 用户访问 Docker 的权限，请参阅 [Linux 安装后步骤](/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)。您也可以在没有 `root` 权限的情况下安装 Docker，或配置为以无根模式运行。有关以无根模式运行 Docker 的说明，请参阅[以非 root 用户身份运行 Docker 守护进程（无根模式）](/engine/security/rootless/)。

#### 安装预发布版本

Docker 还在 [https://test.docker.com/](https://test.docker.com/) 提供了一个便捷脚本，用于在 Linux 上安装 Docker 的预发布版本。该脚本与 `get.docker.com` 上的脚本相同，但会将您的包管理器配置为使用 Docker 软件包仓库的测试通道。测试通道包括 Docker 的稳定版本和预发布版本（测试版本、候选发布版本）。使用此脚本可以提前获取新版本，并在它们作为稳定版本发布之前在测试环境中对其进行评估。

要在 Linux 上从测试通道安装 Docker 的最新版本，请运行：

```console
$ curl -fsSL https://test.docker.com -o test-docker.sh
$ sudo sh test-docker.sh
```

#### 使用便捷脚本后升级 Docker

如果您使用便捷脚本安装了 Docker，则应直接使用包管理器升级 Docker。重新运行便捷脚本没有任何优势。如果它尝试重新安装主机上已存在的仓库，重新运行它可能会导致问题。
