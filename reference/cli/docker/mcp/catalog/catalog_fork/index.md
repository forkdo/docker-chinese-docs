# docker mcp catalog fork

**Description:** Create a copy of an existing catalog

**Usage:** `docker mcp catalog fork <src-catalog> <new-name>`



<!--
此页面由 Docker 源代码自动生成。如果您想对本文内容提出修改建议，请在 GitHub 上的源仓库中提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->








## Description

Create a new catalog by copying all servers from an existing catalog. Useful for creating variations of existing catalogs.





## Examples

  # Fork the Docker catalog to customize it
  docker mcp catalog fork docker-mcp my-custom-docker
  
  # Fork a team catalog for personal use
  docker mcp catalog fork team-servers my-servers



