# docker container unpause

**Description:** Unpause all processes within one or more containers

**Usage:** `docker container unpause CONTAINER [CONTAINER...]`

**Aliases:** `docker unpause`

<!--
此页面由 Docker 源代码自动生成。如果您想修改此处显示的文本，
请在 GitHub 的源代码仓库中提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

The `docker unpause` command un-suspends all processes in the specified containers.
On Linux, it does this using the freezer cgroup.

See the
[freezer cgroup documentation](https://www.kernel.org/doc/Documentation/cgroup-v1/freezer-subsystem.txt)
for further details.




## Examples

```console
$ docker unpause my_container
my_container
```



