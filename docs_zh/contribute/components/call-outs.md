---
description: Docker 文档中使用的组件和格式化示例
title: 提示框
toc_max: 3
---

我们支持以下主要类别的提示框：

- 提示类型：Note（注意）、Tip（提示）、Important（重要）、Warning（警告）、Caution（小心）

我们还支持摘要栏，用于表示某项功能所需的订阅、版本或管理员角色。
添加摘要栏的方法：

将功能名称添加到 `/data/summary.yaml` 文件中。使用以下属性：

| 属性           | 说明                                                   | 可选值                                                      |
|----------------|-------------------------------------------------------|------------------------------------------------------------|
| `subscription` | 注明使用该功能所需的订阅等级                           | All, Personal, Pro, Team, Business                         |
| `availability` | 注明该功能所处的产品开发阶段                           | Experimental, Beta, Early Access, GA, Retired              |
| `requires`     | 注明该功能所需的最低版本                               | 无特定值，使用字符串描述版本并链接到相关发布说明             |
| `for`          | 注明该功能是否面向 IT 管理员                           | Administrators                                             |

然后，在需要添加摘要栏的页面中使用 `summary-bar` 短代码。注意，功能名称区分大小写。摘要栏中显示的图标会自动渲染。

## 示例

{{< summary-bar feature_name="PKG installer" >}}

> [!NOTE]
>
> 注意 `get_hit_count` 函数的编写方式。这个基本的重试循环让我们可以在 redis 服务不可用时多次尝试请求。这在应用启动时非常有用，同时也能在 Redis 服务需要重启时增强应用的弹性。在集群环境中，这也有助于处理节点间的短暂连接中断。

> [!TIP]
>
> 为了使用更小的基础镜像，请使用 `alpine`。

> [!IMPORTANT]
>
> 请将访问令牌视为密码并严格保密。请安全地存储您的令牌（例如，存储在凭据管理器中）。

> [!WARNING]
>
> 删除卷
>
> 默认情况下，运行 `docker compose down` 时不会删除 compose 文件中的命名卷。如果您想删除卷，需要添加 `--volumes` 标志。
>
> Docker Desktop Dashboard 在删除应用堆栈时不会删除卷。

> [!CAUTION]
>
> 此处有风险。

对于以下两种提示框，请参考 [Docker 发布生命周期](/release-lifecycle) 了解更多使用场景信息。

## 格式化

```md
{{</* summary-bar feature_name="PKG installer" */>}}
```

```html
> [!NOTE]
>
> 注意 `get_hit_count` 函数的编写方式。这个基本的重试循环让我们可以在 redis 服务不可用时多次尝试请求。这在应用启动时非常有用，同时也能在 Redis 服务需要重启时增强应用的弹性。在集群环境中，这也有助于处理节点间的短暂连接中断。

> [!TIP]
>
> 为了使用更小的基础镜像，请使用 `alpine`。

> [!IMPORTANT]
>
> 请将访问令牌视为密码并严格保密。请安全地存储您的令牌（例如，存储在凭据管理器中）。

> [!WARNING]
>
> 删除卷
>
> 默认情况下，运行 `docker compose down` 时不会删除 compose 文件中的命名卷。如果您想删除卷，需要添加 `--volumes` 标志。
>
> Docker Desktop Dashboard 在删除应用堆栈时不会删除卷。

> [!CAUTION]
>
> 此处有风险。
```