# OIDC 连接规则集和主题声明




规则集（rulesets）和主题声明（subject claims）定义了您的 GitHub 工作流可以使用您的 Docker 资源执行哪些操作。使用它们为 OIDC 连接授权 GitHub 工作流行为。

## 规则集

规则集是 Docker 针对传入的 GitHub ID 令牌进行评估的一组条件。当工作流触发 OIDC 交换时，Docker 会根据您连接中定义的每个规则集检查令牌。如果某个规则集的条件得到满足，Docker 会根据该规则集设置的参数授予访问权限。

每个规则集包含以下字段：

- Label：规则集的名称。
- Rules：一个或多个基于 OIDC 令牌声明的条件，例如仓库名称、分支或工作流路径。
  - 这些以主题声明字符串的形式表达。
  - 请参阅 [主题声明](#主题声明)。
- Resources：当规则集匹配时，工作流可以访问的 Docker 资源。请参阅 [资源](#资源)。
- Scopes：在这些资源上授予的权限，例如读取或写入访问。

每个连接可以定义 1 到 5 个规则集。使用多个规则集可以在不同的工作流或分支上应用不同的访问级别。如果有多个规则集与传入的令牌匹配，Docker 会合并所有匹配规则集的资源，并授予对合并后集合的访问权限。

## 主题声明

主题声明是 GitHub 签发的 JWT ID 令牌中的 `sub` 字段。它将工作流的详细信息编码为单个字符串，通过组织、仓库、分支、环境等来标识工作流。

Docker 在评估您的规则集规则时，将主题声明作为主要条件。默认的主题声明格式为：

```text
repo:<org>/<repo>:ref:refs/heads/<branch>
```

例如：

```text
repo:octo-org/octo-repo:ref:refs/heads/main
```

确切的格式各不相同，取决于触发工作流的原因。

- 分支推送、拉取请求、标签或环境部署各自产生不同的 `sub` 值。
- 有关格式的完整列表，请参阅 [GitHub 的 OpenID Connect 参考](https://docs.github.com/en/actions/reference/security/oidc)。

> [!NOTE]
> 2026 年 7 月 15 日之后创建的 GitHub 仓库对默认主题声明使用不可变标识符。例如：
> `repo:octocat@123456/my-repo@456789:ref:refs/heads/main`。更多详情请参阅 [GitHub 变更日志](https://github.blog/changelog/2026-04-23-immutable-subject-claims-for-github-actions-oidc-tokens/)。

您可以使用通配符跨仓库或分支进行匹配：

| 模式                                        | 匹配                                         |
| :--------------------------------------------- | :---------------------------------------------- |
| `repo:my-org/my-repo:ref:refs/heads/main`      | 仅特定仓库的 `main` 分支 |
| `repo:my-org/*`                                | 组织中的所有仓库                   |
| `repo:my-org/my-repo:ref:refs/heads/release-*` | 所有以 `release-` 开头的分支           |

## 资源

资源定义了当规则集匹配时，工作流可以访问的 Docker 资源。您在每个规则集中指定资源，同时指定确定所授予访问级别的权限范围。

Docker Hub 仓库和 Docker Build Cloud 是受支持的资源。

## 后续步骤

- [OIDC 连接概述](/manuals/enterprise/security/oidc-connections/_index.md)
- [创建或管理 OIDC 连接](/manuals/enterprise/security/oidc-connections/create-manage.md)

