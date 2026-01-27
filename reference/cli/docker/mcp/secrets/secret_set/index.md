# docker mcp secret set

**Description:** Set a secret in Docker Desktop's secret store

**Usage:** `docker mcp secret set key[=value]`



<!--
此页面由 Docker 的源代码自动生成。如果您想建议修改此处显示的文本，请在 GitHub 上的源代码仓库中提交 issue 或 pull request：

https://github.com/docker/mcp-gateway
-->








## Description

Set a secret in Docker Desktop's secret store


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--provider` |  |  Supported: credstore, oauth/<provider> |



## Examples

### Use secrets for postgres password with default policy

```console
docker mcp secret set POSTGRES_PASSWORD=my-secret-password
docker run -d -l x-secret:POSTGRES_PASSWORD=/pwd.txt -e POSTGRES_PASSWORD_FILE=/pwd.txt -p 5432 postgres
```

### Pass the secret via STDIN

```console
echo my-secret-password > pwd.txt
cat pwd.txt | docker mcp secret set POSTGRES_PASSWORD
```



