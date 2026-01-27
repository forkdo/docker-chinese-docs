# docker config rm

**Description:** Remove one or more configs

**Usage:** `docker config rm CONFIG [CONFIG...]`

**Aliases:** `docker config remove`

<!--
此页面由 Docker 源代码自动生成。如果您希望修改此处显示的文本，请在 GitHub 上的源代码仓库中提交问题或拉取请求：

https://github.com/docker/cli
-->






**Orchestrator:** Swarm

## Description

Removes the specified configs from the Swarm.

For detailed information about using configs, refer to [store configuration data using Docker Configs](/engine/swarm/configs/).

> [!NOTE]
> This is a cluster management command, and must be executed on a Swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](/engine/swarm/) in the
> documentation.




## Examples

This example removes a config:

```console
$ docker config rm my_config
sapth4csdo5b6wz2p5uimh5xg
```

> [!WARNING]
> This command doesn't ask for confirmation before removing a config.
{ .warning }



