# docker scout config

**Description:** Manage Docker Scout configuration

**Usage:** `docker scout config [KEY] [VALUE]`



<!--
此页面是自动从 Docker 的源代码生成的。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
提交工单：

https://github.com/docker/scout-cli
-->








## Description

`docker scout config` allows you to list, get and set Docker Scout configuration.

Available configuration key:

- `organization`: Namespace of the Docker organization to be used by default.




## Examples

### List existing configuration

```console
$ docker scout config
organization=my-org-namespace
```

### Print configuration value

```console
$ docker scout config organization
my-org-namespace
```

### Set configuration value

```console
$ docker scout config organization my-org-namespace
    ✓ Successfully set organization to my-org-namespace
```



