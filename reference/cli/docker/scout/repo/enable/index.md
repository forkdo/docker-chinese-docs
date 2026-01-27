# docker scout repo enable

**Description:** Enable Docker Scout

**Usage:** `docker scout repo enable [REPOSITORY]`



<!--
此页面是自动生成的，来源于 Docker 的源代码。如果您想
建议修改此处显示的文本，请在 GitHub 上的源代码仓库中提交工单：

https://github.com/docker/scout-cli
-->








## Description

The docker scout repo enable command enables Docker Scout on repositories.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--all` |  |  Enable all repositories of the organization. Can not be used with --filter.<br> |
| `--filter` |  |  Regular expression to filter repositories by name |
| `--integration` |  |  Name of the integration to use for enabling an image |
| `--org` |  |  Namespace of the Docker organization |
| `--registry` |  |  Container Registry |



## Examples

### Enable a specific repository

```console
$ docker scout repo enable my/repository
```

### Enable all repositories of the organization

```console
$ docker scout repo enable --all
```

### Enable some repositories based on a filter

```console
$ docker scout repo enable --filter namespace/backend
```

### Enable a repository from a specific registry

```console
$ docker scout repo enable my/repository --registry 123456.dkr.ecr.us-east-1.amazonaws.com
```



