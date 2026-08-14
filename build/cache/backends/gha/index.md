# GitHub Actions 缓存




GitHub Actions 缓存利用了
[GitHub 提供的 Action's cache](https://github.com/actions/cache) 或其他支持 GitHub Actions 缓存协议的服务。只要你的用例在
[GitHub 设定的大小和使用限制](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#usage-limits-and-eviction-policy)
之内，这就是在你的 GitHub Actions 工作流中推荐的缓存方案。

默认的 `docker` 驱动不支持这种缓存存储后端。要使用此功能，请使用不同的驱动创建一个新的 builder。更多信息请参阅 [Build drivers](/manuals/build/builders/drivers/_index.md)。

## 概要（Synopsis）

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=gha[,parameters...] \
  --cache-from type=gha[,parameters...] .
```

下表描述了你可以传递给 `--cache-to` 和 `--cache-from` 的可用 CSV 参数。

| Name           | Option                  | Type        | Default                                        | Description                                                          |
|----------------|-------------------------|-------------|------------------------------------------------|----------------------------------------------------------------------|
| `url`          | `cache-to`,`cache-from` | String      | `$ACTIONS_CACHE_URL` or `$ACTIONS_RESULTS_URL` | 缓存服务器 URL，参见 [authentication][1]。在 `version=2` 时被忽略。  |
| `url_v2`       | `cache-to`,`cache-from` | String      | `$ACTIONS_RESULTS_URL`                         | 缓存 v2 服务器 URL，参见 [authentication][1]。                       |
| `token`        | `cache-to`,`cache-from` | String      | `$ACTIONS_RUNTIME_TOKEN`                       | 访问令牌，参见 [authentication][1]。                                 |
| `scope`        | `cache-to`,`cache-from` | String      | `buildkit`                                     | 缓存对象所属的 scope，参见 [scope][2]                                |
| `mode`         | `cache-to`              | `min`,`max` | `min`                                          | 要导出的缓存层，参见 [cache mode][3]。                               |
| `ignore-error` | `cache-to`              | Boolean     | `false`                                        | 忽略由缓存导出失败引起的错误。                                       |
| `timeout`      | `cache-to`,`cache-from` | String      | `10m`                                          | 在超时之前导入或导出缓存的最大持续时间。                             |
| `repository`   | `cache-to`              | String      |                                                | 用于缓存存储的 GitHub 仓库。                                         |
| `ghtoken`      | `cache-to`              | String      |                                                | 访问 GitHub API 所需的 GitHub 令牌。                                 |
| `version`      | `cache-to`,`cache-from` | String      | `1` unless `$ACTIONS_CACHE_SERVICE_V2` is set, then `2` | 选择 GitHub Actions 缓存版本，参见 [version][4]                     |

[1]: #authentication
[2]: #scope
[3]: _index.md#cache-mode
[4]: #version

## 身份验证（Authentication）

如果 `url`、`url_v2` 或 `token` 参数未指定，`gha` 缓存后端将回退到使用环境变量。如果你从内联步骤手动调用 `docker buildx` 命令，则必须手动暴露这些变量。可以考虑使用
[`crazy-max/ghaction-github-runtime`](https://github.com/crazy-max/ghaction-github-runtime)
这个 GitHub Action 作为暴露变量的辅助工具。

## 作用域（Scope）

作用域（scope）是用于标识缓存对象的键。默认情况下，它被设置为 `buildkit`。如果你构建多个镜像，每次构建都会覆盖上一次的缓存，只留下最终的缓存。

为了为多次构建保留缓存，你可以用特定的名称指定这个 scope 属性。在以下示例中，缓存被设置为镜像名称，以确保每个镜像都有自己的缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=gha,url=...,token=...,scope=image \
  --cache-from type=gha,url=...,token=...,scope=image .
$ docker buildx build --push -t <registry>/<image2> \
  --cache-to type=gha,url=...,token=...,scope=image2 \
  --cache-from type=gha,url=...,token=...,scope=image2 .
```

GitHub 的 [缓存访问限制](https://docs.github.com/en/actions/advanced-guides/caching-dependencies-to-speed-up-workflows#restrictions-for-accessing-a-cache)
仍然适用。工作流只能访问当前分支、基础分支和默认分支的缓存。

## 版本（Version）

如果你不明确设置 `version`，默认是 v1。但是，如果环境变量 `$ACTIONS_CACHE_SERVICE_V2` 被设置为被解释为 `true` 的值（`1`、`true`、`yes`），则会自动使用 v2。

同一时刻只有一个 URL 是相关的：

 - 使用 v1 时，使用 `url`（默认 `$ACTIONS_CACHE_URL`）。
 - 使用 v2 时，使用 `url_v2`（默认 `$ACTIONS_RESULTS_URL`）。

### 使用 `docker/build-push-action`

当使用
[`docker/build-push-action`](https://github.com/docker/build-push-action) 时，
`url` 和 `token` 参数会被自动填充。无需手动指定它们，也不需包含任何额外的变通方案。

例如：

```yaml
- name: Build and push
  uses: docker/build-push-action@v7
  with:
    context: .
    push: true
    tags: "<registry>/<image>:latest"
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## 避免 GitHub Actions 缓存 API 限流（Avoid GitHub Actions cache API throttling）

GitHub 的 [使用限制和驱逐策略](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#usage-limits-and-eviction-policy)
会导致陈旧的缓存条目在一段时间后会被移除。默认情况下，`gha` 缓存后端使用 GitHub Actions 缓存 API 来检查缓存条目的状态。

GitHub Actions 缓存 API 会受到速率限制，如果你在短时间内发出过多请求（这可能会在使用 `gha` 缓存后端的构建过程中因缓存查找而发生），就会触发限流。

```text
#31 exporting to GitHub Actions Cache
#31 preparing build cache for export
#31 preparing build cache for export 600.3s done
#31 ERROR: maximum timeout reached
------
 > exporting to GitHub Actions Cache:
------
ERROR: failed to solve: maximum timeout reached
make: *** [Makefile:35: release] Error 1
Error: Process completed with exit code 2.
```

为了缓解此问题，你可以向 BuildKit 提供一个 GitHub 令牌。这样 BuildKit 就能利用标准的 GitHub API 来检查缓存键，从而减少向缓存 API 发出的请求数量。

要提供 GitHub 令牌，你可以使用 `ghtoken` 参数，以及一个 `repository` 参数来指定用于缓存存储的仓库。`ghtoken` 参数是一个带有 `repo` 作用域的 GitHub 令牌，访问 GitHub Actions 缓存 API 需要它。

当你使用 `docker/build-push-action` action 进行构建时，`ghtoken` 参数会自动设置为 `secrets.GITHUB_TOKEN` 的值。你也可以使用 `github-token` 输入手动设置 `ghtoken` 参数，如下例所示：

```yaml
- name: Build and push
  uses: docker/build-push-action@v7
  with:
    context: .
    push: true
    tags: "<registry>/<image>:latest"
    cache-from: type=gha
    cache-to: type=gha,mode=max
    github-token: ${{ secrets.MY_CUSTOM_TOKEN }}
```

## 延伸阅读（Further reading）

有关缓存的入门介绍，请参阅 [Docker 构建缓存](../_index.md)。

有关 `gha` 缓存后端的更多信息，请参阅
[BuildKit README](https://github.com/moby/buildkit#github-actions-cache-experimental)。

有关将 GitHub Actions 与 Docker 配合使用的更多信息，请参阅
[GitHub Actions 简介](../../ci/github-actions/_index.md)

