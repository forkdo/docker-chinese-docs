# docker mcp catalog create

**Description:** Create a new empty catalog

**Usage:** `docker mcp catalog create <name>`



<!--
此页面内容自动从 Docker 的源代码生成。如果您希望
修改此处显示的文本，请在 GitHub 上的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->








## Description

Create a new empty catalog for organizing custom MCP servers. The catalog will be stored locally and can be populated using 'docker mcp catalog add'.





## Examples

  # Create a new catalog for development servers
  docker mcp catalog create dev-servers
  
  # Create a catalog for production monitoring tools  
  docker mcp catalog create prod-monitoring



