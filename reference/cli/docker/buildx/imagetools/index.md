# docker buildx imagetools

**Description:** Commands to work on images in registry

**Usage:** `docker buildx imagetools`



<!--
本页面由 Docker 源代码自动生成。如果您想修改此处显示的文本内容，请在 GitHub 上的源代码仓库中提交问题或拉取请求：

https://github.com/docker/buildx
-->








## Description

The `imagetools` commands contains subcommands for working with manifest lists
in container registries. These commands are useful for inspecting manifests
to check multi-platform configuration and attestations.




## Examples

### Override the configured builder instance (--builder) {#builder}

Same as [`buildx --builder`](/reference/cli/docker/buildx/#builder).


## Subcommands

| Command | Description |
|---------|-------------|
| [`docker buildx imagetools create`](/reference/cli/docker/buildx/imagetools/create/) | Create a new image based on source images |
| [`docker buildx imagetools inspect`](/reference/cli/docker/buildx/imagetools/inspect/) | Show details of an image in the registry |


