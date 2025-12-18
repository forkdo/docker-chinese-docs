---
description: Docker 文档中使用的组件和格式示例
title: Callouts
toc_max: 3
---

我们支持以下几类 callouts：

- 警示类：Note（注意）、Tip（提示）、Important（重要）、Warning（警告）、Caution（小心）

我们还支持摘要栏（summary bars），用于表示功能所需的订阅、版本或管理员角色。
要添加摘要栏：

将功能名称添加到 `/data/summary.yaml` 文件中。使用以下属性：

| 属性           | 描述                                             | 可能的值                                           |
|----------------|--------------------------------------------------|---------------------------------------------------|
| `subscription` | 注明使用该功能所需的订阅                         | All（全部）、Personal（个人）、Pro（专业）、Team（团队）、Business（企业） |
| `availability` | 注明该功能所处的产品开发阶段                     | Experimental（实验性）、Beta（测试版）、Early Access（早期访问）、GA（正式发布）、Retired（已退役） |
| `requires`     | 注明该功能所需的最低版本                         | 无特定值，使用字符串描述版本并链接到相关发布说明 |
| `for`          | 注明该功能是否面向 IT 管理员                     | Administrators（管理员）                          |

然后，在需要添加摘要栏的页面上添加 `summary-bar` 短代码。注意，功能名称区分大小写。摘要栏中显示的图标会自动渲染。

## 示例

{{< summary-bar feature_name="PKG installer" >}}

> [!NOTE]
>
> 注意 `get_hit_count` 函数的写法。这个基本的重试循环允许我们在 Redis 服务不可用时多次尝试请求。这在应用程序启动时很有用，当服务正在上线时，同时在 Redis 服务需要在应用程序生命周期中重启时，也能提高应用程序的弹性。在集群中，这也有助于处理节点之间的瞬时连接中断。

> [!TIP]
>
> 为了获得更小的基础镜像，请使用 `alpine`。

> [!IMPORTANT]
>
> 请像保护密码一样保护访问令牌，并将它们保密。安全地存储令牌（例如，在凭据管理器中）。

> [!WARNING]
>
> 删除卷
>
> 默认情况下，运行 `docker compose down` 时，compose 文件中的命名卷不会被删除。如果你想删除卷，需要添加 `--volumes` 标志。
>
> Docker Desktop 仪表板在删除应用栈时不会删除卷。

> [!CAUTION]
>
> 此处有龙（危险）。

对于以下两种 callouts，请参考 [Docker 发布生命周期](/release-lifecycle) 以获取更多关于何时使用它们的信息。

## 格式

```md
{{</* summary-bar feature_name="PKG installer" */>}}
```

```html
> [!NOTE]
>
> 注意 `get_hit_count` 函数的写法。这个基本的重试循环允许我们在 Redis 服务不可用时多次尝试请求。这在应用程序启动时很有用，当服务正在上线时，同时在 Redis 服务需要在应用程序生命周期中重启时，也能提高应用程序的弹性。在集群中，这也有助于处理节点之间的瞬时连接中断。

> [!TIP]
>
> 为了获得更小的基础镜像，请使用 `alpine`。

> [!IMPORTANT]
>
> 请像保护密码一样保护访问令牌，并将它们保密。安全地存储令牌（例如，在凭据管理器中）。

> [!WARNING]
>
> 删除卷
>
> 默认情况下，运行 `docker compose down` 时，compose 文件中的命名卷不会被删除。如果你想删除卷，需要添加 `--volumes` 标志。
>
> Docker Desktop 仪表板在删除应用栈时不会删除卷。

> [!CAUTION]
>
> 此处有龙（危险）。
```