# docker node promote

**Description:** Promote one or more nodes to manager in the swarm

**Usage:** `docker node promote NODE [NODE...]`



<!--
本页内容由 Docker 源码自动生成。如果您希望
建议对此处显示的文本进行修改，请在 GitHub 的源码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->






**Orchestrator:** Swarm

## Description

Promotes a node to manager. This command can only be executed on a manager node.

> [!NOTE]
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](/engine/swarm/) in the
> documentation.




## Examples

```console
$ docker node promote <node name>
```



