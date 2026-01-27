# docker scout policy

**Description:** Evaluate policies against an image and display the policy evaluation results (experimental)


**Usage:** `docker scout policy [IMAGE | REPO]`



<!--
此页面是自动从 Docker 的源代码生成的。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中提交工单：

https://github.com/docker/scout-cli
-->



> [!NOTE]
> **Experimental**
>
> This command is experimental. Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.





## Description

The `docker scout policy` command evaluates policies against an image.
The image analysis is uploaded to Docker Scout where policies get evaluated.

The policy evaluation results may take a few minutes to become available.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-e`, `--exit-code` |  |  Return exit code '2' if policies are not met, '0' otherwise |
| `--only-policy` |  |  Comma separated list of policies to evaluate |
| `--org` |  |  Namespace of the Docker organization |
| `-o`, `--output` |  |  Write the report to a file |
| `--platform` |  |  Platform of image to pull policy results from |
| `--to-env` |  |  Name of the environment to compare to |
| `--to-latest` |  |  Latest image processed to compare to |



## Examples

### Evaluate policies against an image and display the results

```console
$ docker scout policy dockerscoutpolicy/customers-api-service:0.0.1
```

### Evaluate policies against an image for a specific organization

```console
$ docker scout policy dockerscoutpolicy/customers-api-service:0.0.1 --org dockerscoutpolicy
```

### Evaluate policies against an image with a specific platform

```console
$ docker scout policy dockerscoutpolicy/customers-api-service:0.0.1 --platform linux/amd64
```

### Compare policy results for a repository in a specific environment

```console
$ docker scout policy dockerscoutpolicy/customers-api-service --to-env production
```



