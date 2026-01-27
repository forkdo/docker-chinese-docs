# docker buildx

**Description:** Docker Buildx

**Usage:** `docker buildx`



<!--
此页面是自动从 Docker 的源代码生成的。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
打开工单或拉取请求：

https://github.com/docker/buildx
-->








## Description

Extended build capabilities with BuildKit


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--builder` |  |  Override the configured builder instance |
| `-D`, `--debug` |  |  Enable debug logging |



## Examples

### Override the configured builder instance (--builder) {#builder}

You can also use the `BUILDX_BUILDER` environment variable.


## Subcommands

| Command | Description |
|---------|-------------|
| [`docker buildx bake`](/reference/cli/docker/buildx/bake/) | Build from a file |
| [`docker buildx build`](/reference/cli/docker/buildx/build/) | Start a build |
| [`docker buildx create`](/reference/cli/docker/buildx/create/) | Create a new builder instance |
| [`docker buildx dap`](/reference/cli/docker/buildx/dap/) | Start debug adapter protocol compatible debugger |
| [`docker buildx debug`](/reference/cli/docker/buildx/debug/) | Start debugger |
| [`docker buildx du`](/reference/cli/docker/buildx/du/) | Disk usage |
| [`docker buildx history`](/reference/cli/docker/buildx/history/) | Commands to work on build records |
| [`docker buildx imagetools`](/reference/cli/docker/buildx/imagetools/) | Commands to work on images in registry |
| [`docker buildx inspect`](/reference/cli/docker/buildx/inspect/) | Inspect current builder instance |
| [`docker buildx ls`](/reference/cli/docker/buildx/ls/) | List builder instances |
| [`docker buildx prune`](/reference/cli/docker/buildx/prune/) | Remove build cache |
| [`docker buildx rm`](/reference/cli/docker/buildx/rm/) | Remove one or more builder instances |
| [`docker buildx stop`](/reference/cli/docker/buildx/stop/) | Stop builder instance |
| [`docker buildx use`](/reference/cli/docker/buildx/use/) | Set the current builder instance |
| [`docker buildx version`](/reference/cli/docker/buildx/version/) | Show buildx version information |


