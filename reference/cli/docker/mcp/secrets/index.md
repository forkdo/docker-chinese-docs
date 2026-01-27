# docker mcp secret

**Description:** Manage secrets





<!--
此页面由 Docker 的源代码自动生成。如果您想对本文内容提出修改建议，请在 GitHub 上的源仓库中提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->








## Description

Manage secrets




## Examples

### Use secrets for postgres password with default policy

> docker mcp secret set POSTGRES_PASSWORD=my-secret-password
> docker run -d -l x-secret:POSTGRES_PASSWORD=/pwd.txt -e POSTGRES_PASSWORD_FILE=/pwd.txt -p 5432 postgres

### Pass the secret via STDIN

> echo my-secret-password > pwd.txt
> cat pwd.txt | docker mcp secret set POSTGRES_PASSWORD


## Subcommands

| Command | Description |
|---------|-------------|
| [`docker mcp secret export`](/reference/cli/docker/mcp/secrets/secret_export/) | Export secrets for the specified servers |
| [`docker mcp secret ls`](/reference/cli/docker/mcp/secrets/secret_ls/) | List all secret names in Docker Desktop's secret store |
| [`docker mcp secret rm`](/reference/cli/docker/mcp/secrets/secret_rm/) | Remove secrets from Docker Desktop's secret store |
| [`docker mcp secret set`](/reference/cli/docker/mcp/secrets/secret_set/) | Set a secret in Docker Desktop's secret store |


