# docker mcp policy set

**Description:** Set a policy for secret management in Docker Desktop

**Usage:** `docker mcp policy set <content>`



<!--
此页面由 Docker 的源代码自动生成。如果您想
建议更改此处显示的文本，请在 GitHub 上的
源代码仓库中提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->








## Description

Set a policy for secret management in Docker Desktop




## Examples

### Backup the current policy to a file
docker mcp policy dump > policy.conf

### Set a new policy
docker mcp policy set "my-secret allows postgres"

### Restore the previous policy
cat policy.conf | docker mcp policy set



