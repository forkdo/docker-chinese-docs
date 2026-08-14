---
title: 构建垃圾回收
description: 了解 BuildKit 守护进程中的垃圾回收
keywords: build, buildx, buildkit, garbage collection, prune, gc
aliases:
  - /build/building/cache/garbage-collection/
---

虽然 [`docker builder prune`](/reference/cli/docker/builder/prune/)
或 [`docker buildx prune`](/reference/cli/docker/buildx/prune/)
命令是一次性的，但垃圾回收（GC）会定期运行，并遵循一组有序的 prune 策略。当缓存大小变得过大，或者缓存年龄到期时，BuildKit 守护进程会清除构建缓存。

对大多数用户而言，默认的 GC 行为已经足够，无需任何干预。高级用户，特别是那些处理大规模构建、自管理 builder 或存储受限环境的用户，可能会受益于自定义这些设置，以更好地契合其工作流需求。以下各节将解释 GC 的工作原理，并提供通过自定义配置来调整其行为的指导。

## 垃圾回收策略（Garbage collection policies）

GC 策略定义了一组规则，用于确定如何管理和清理构建缓存。这些策略包含用于决定何时移除缓存条目的标准，例如缓存的使用时长、已用空间大小，以及要 prune 的缓存记录类型。

每个 GC 策略按序列依次评估，从最具体的标准开始，如果前面的策略未能释放足够的缓存，则继续更宽泛的规则。这让 BuildKit 能够优先处理缓存条目，在保留最有价值的缓存的同时，确保系统维持性能和可用性。

例如，假设你有以下 GC 策略：

1. 找出过去 48 小时内未使用过的"陈旧"缓存记录，并删除记录，直到最多剩 5GB 的"陈旧"缓存。
2. 如果构建缓存大小超过 10GB，则删除记录，直到总缓存大小不超过 10GB。

第一条规则更具体，优先考虑陈旧缓存记录并为这类价值较低的缓存设定了较低的限制。第二条规则施加了适用于任何类型缓存记录的更高硬限制。有了这些策略，如果你有 11GB 的构建缓存，其中：

- 其中 7GB 是"陈旧"缓存
- 4GB 是其他更有价值的缓存

GC 扫描会作为第 1 条策略的一部分删除 5GB 的陈旧缓存，剩余 6GB，这意味着第 2 条策略无需再清理任何缓存。

默认的 GC 策略（大约）如下：

1. 移除可轻松重新生成的缓存，例如来自本地目录或远程 Git 仓库的构建上下文，以及缓存挂载（如果已超 48 小时未使用）。
2. 移除超过 60 天未在构建中使用的缓存。
3. 移除超过构建缓存大小限制的未共享缓存。未共享缓存记录指的是未被其他资源（通常作为镜像层）使用的层 blob。
4. 移除任何超过构建缓存大小限制的构建缓存。

精确的算法以及配置策略的方式，会因你使用的 builder 类型而略有不同。请参阅 [Configuration](#configuration) 了解详情。

## 配置（Configuration）

> [!NOTE]
> 如果你对默认的垃圾回收行为感到满意，且不需要微调其设置，可以跳过本节。默认配置对大多数用例都表现良好，无需额外设置。

根据你使用的 [build driver](../builders/drivers/_index.md) 类型，你会使用不同的配置文件来更改 builder 的 GC 设置：

- 如果你使用 Docker Engine 的默认 builder（即 `docker` 驱动），请使用 [Docker 守护进程配置文件](#docker-daemon-configuration-file)。
- 如果你使用自定义 builder，请使用 [BuildKit 配置文件](#buildkit-configuration-file)。

### Docker 守护进程配置文件（Docker daemon configuration file）

如果你使用默认的 [`docker` driver](../builders/drivers/docker.md)，GC 是在 [`daemon.json` 配置文件](/reference/cli/dockerd.md#daemon-configuration-file) 中配置的；如果你使用 Docker Desktop，则是在 [**Settings > Docker Engine**](/manuals/desktop/settings-and-maintenance/settings.md) 中配置。

以下片段展示了 Docker Desktop 用户针对 `docker` 驱动的默认 builder 配置：

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  }
}
```

`defaultKeepStorage` 选项配置了构建缓存的大小限制，它会影响 GC 策略。`docker` 驱动的默认策略工作方式如下：

1. 移除超过 48 小时未使用的临时构建缓存（如果它超过 `defaultKeepStorage` 的 13.8%，或至少 512MB）。
2. 移除超过 60 天未使用的构建缓存。
3. 移除超过 `defaultKeepStorage` 限制的未共享构建缓存。
4. 移除任何超过 `defaultKeepStorage` 限制的构建缓存。

鉴于 Docker Desktop 中 `defaultKeepStorage` 的默认值为 20GB，默认的 GC 策略解析为：

```json
{
  "builder": {
    "gc": {
      "enabled": true,
      "policy": [
        {
          "reservedSpace": "2.764GB",
          "keepDuration": "48h",
          "filter": [
            "type=source.local,type=exec.cachemount,type=source.git.checkout"
          ]
        },
        { "reservedSpace": "20GB", "keepDuration": ["1440h"] },
        { "reservedSpace": "20GB" },
        { "reservedSpace": "20GB", "all": true }
      ]
    }
  }
}
```

调整 `docker` 驱动的构建缓存配置最简单的方法是调整 `defaultKeepStorage` 选项：

- 如果你觉得 GC 过于激进，请提高该限制。
- 如果你需要保留空间，请降低该限制。

#### Docker 守护进程配置文件中的自定义 GC 策略（Custom GC policies in the Docker daemon configuration file）

如果你需要更强的控制力，可以直接定义自己的 GC 策略。以下示例定义了一个更保守的 GC 配置，包含以下策略：

1. 如果构建缓存超过 50GB，移除超过 1440 小时（即 60 天）未使用的缓存条目。
2. 如果构建缓存超过 50GB，移除未共享的缓存条目。
3. 如果构建缓存超过 100GB，移除任何缓存条目。

```json
{
  "builder": {
    "gc": {
      "enabled": true,
      "policy": [
        { "reservedSpace": "50GB", "keepDuration": ["1440h"] },
        { "reservedSpace": "50GB" },
        { "reservedSpace": "100GB", "all": true }
      ]
    }
  }
}
```

> [!NOTE]
> 在 Docker 守护进程配置文件中，GC 过滤器中的"等于"运算符用单个 `=` 表示，而 BuildKit 的配置文件使用 `==`：
>
> | `daemon.json`       | `buildkitd.toml`     |
> |---------------------|----------------------|
> | `type=source.local` | `type==source.local` |
> | `private=true`      | `private==true`      |
> | `shared=true`       | `shared==true`       |
>
> 有关可用 GC 过滤器的信息，请参阅 [prune filters](/reference/cli/docker/buildx/prune/#filter)。`daemon.json` 中的 GC 配置支持除 `mutable` 和 `immutable` 之外的所有过滤器。

### BuildKit 配置文件（BuildKit configuration file）

对于除 `docker` 之外的构建驱动，GC 是通过
[`buildkitd.toml`](../buildkit/toml-configuration.md) 配置文件配置的。该文件使用以下高级配置选项，你可以用它们来调整 BuildKit 应为缓存使用多少磁盘空间的阈值：

| Option          | Description                                                                                                                                             | Default value                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `reservedSpace` | BuildKit 允许为缓存分配的最小磁盘空间量。低于此阈值的用量在垃圾回收期间不会被回收。                                                                    | 总磁盘空间的 10% 或 10GB（取两者中较低者）           |
| `maxUsedSpace`  | BuildKit 允许使用的最大磁盘空间量。超过此阈值的用量会在垃圾回收期间被回收。                                                                            | 总磁盘空间的 60% 或 100GB（取两者中较低者）          |
| `minFreeSpace`  | 必须保持空闲的磁盘空间量。                                                                                                                              | 20GB                                                  |

你可以将这些选项设置为字节数、单位字符串（例如 `512MB`），或总磁盘大小的百分比。更改这些选项会影响 BuildKit worker 使用的默认 GC 策略。在默认阈值下，GC 策略解析如下：

```toml
# Global defaults
[worker.oci]
  gc = true
  reservedSpace = "10GB"
  maxUsedSpace = "100GB"
  minFreeSpace = "20%"

# Policy 1
[[worker.oci.gcpolicy]]
  filters = [ "type==source.local", "type==exec.cachemount", "type==source.git.checkout" ]
  keepDuration = "48h"
  maxUsedSpace = "512MB"

# Policy 2
[[worker.oci.gcpolicy]]
  keepDuration = "1440h" # 60 days
  reservedSpace = "10GB"
  maxUsedSpace = "100GB"

# Policy 3
[[worker.oci.gcpolicy]]
  reservedSpace = "10GB"
  maxUsedSpace = "100GB"

# Policy 4
[[worker.oci.gcpolicy]]
  all = true
  reservedSpace = "10GB"
  maxUsedSpace = "100GB"
```

具体来说，这意味着：

- 策略 1：如果构建缓存超过 512MB，BuildKit 会移除最近 48 小时内未使用过的本地构建上下文、远程 Git 上下文和缓存挂载的缓存记录。
- 策略 2：如果磁盘用量超过 100GB，会移除超过 60 天的未共享构建缓存，确保至少为缓存保留 10GB 磁盘空间。
- 策略 3：如果磁盘用量超过 100GB，会移除任何未共享缓存，确保至少为缓存保留 10GB 磁盘空间。
- 策略 4：如果磁盘用量超过 100GB，会移除所有缓存——包括共享和内部记录——确保至少为缓存保留 10GB 磁盘空间。

`reservedSpace` 在定义构建缓存大小的下限时具有最高优先级。如果 `maxUsedSpace` 或 `minFreeSpace` 会定义更低的值，最小缓存大小永远不会低于 `reservedSpace`。

如果同时设置了 `reservedSpace` 和 `maxUsedSpace`，GC 扫描会将缓存大小控制在这两个阈值之间。例如，如果 `reservedSpace` 设为 10GB，`maxUsedSpace` 设为 20GB，则 GC 运行后的缓存量小于 20GB，但至少为 10GB。

你也可以定义完全自定义的 GC 策略。自定义策略还允许你定义过滤器，从而精确指定某个策略允许 prune 的缓存条目类型。

#### BuildKit 中的自定义 GC 策略（Custom GC policies in BuildKit）

自定义 GC 策略让你能够微调 BuildKit 管理其缓存的方式，并根据缓存类型、持续时间或磁盘空间阈值等标准，对缓存保留拥有完全的控制权。如果你需要对缓存阈值以及缓存记录应如何排序拥有完全的控制，定义自定义 GC 策略就是正确的做法。

要定义自定义 GC 策略，请在 `buildkitd.toml` 中使用 `[[worker.oci.gcpolicy]]` 配置块。每个策略定义该策略将使用的阈值。如果你使用自定义策略，则 `reservedSpace`、`maxUsedSpace` 和 `minFreeSpace` 的全局值不适用。

以下是一个示例配置：

```toml
# Custom GC Policy 1: Remove unused local contexts older than 24 hours
[[worker.oci.gcpolicy]]
  filters = ["type==source.local"]
  keepDuration = "24h"
  reservedSpace = "5GB"
  maxUsedSpace = "50GB"

# Custom GC Policy 2: Remove remote Git contexts older than 30 days
[[worker.oci.gcpolicy]]
  filters = ["type==source.git.checkout"]
  keepDuration = "720h"
  reservedSpace = "5GB"
  maxUsedSpace = "30GB"

# Custom GC Policy 3: Aggressively clean all cache if disk usage exceeds 90GB
[[worker.oci.gcpolicy]]
  all = true
  reservedSpace = "5GB"
  maxUsedSpace = "90GB"
```

除了 `reservedSpace`、`maxUsedSpace` 和 `minFreeSpace` 阈值之外，在定义 GC 策略时你还有两个额外的配置选项：

- `all`：默认情况下，BuildKit 会排除一些缓存记录，使其不参与 GC prune。将此选项设置为 `true` 将允许任何缓存记录被 prune。
- `filters`：过滤器让你指定某个 GC 策略允许 prune 的特定类型缓存记录。

有关可用 GC 过滤器的信息，请参阅 [buildx prune filters](/reference/cli/docker/buildx/prune/#filter)。
