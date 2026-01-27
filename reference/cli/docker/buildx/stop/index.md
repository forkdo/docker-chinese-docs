# docker buildx stop

**Description:** Stop builder instance

**Usage:** `docker buildx stop [NAME]`



<!--
本页内容由 Docker 源代码自动生成。如果您希望
建议对此处显示的文本进行修改，请在 GitHub 上的源存储库中
打开工单或拉取请求：

https://github.com/docker/buildx
-->








## Description

Stops the specified or current builder. This does not prevent buildx build to
restart the builder. The implementation of stop depends on the driver.




## Examples

### Override the configured builder instance (--builder) {#builder}

Same as [`buildx --builder`](/reference/cli/docker/buildx/#builder).



