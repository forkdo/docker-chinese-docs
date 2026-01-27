# docker context update

**Description:** Update a context

**Usage:** `docker context update [OPTIONS] CONTEXT`



<!--
This page is automatically generated from Docker's source code. If you want to
suggest a change to the text that appears here, open a ticket or pull request
in the source repository on GitHub:

https://github.com/docker/cli
-->








## Description

Updates an existing `context`.
See [context create](/reference/cli/docker/context/create/).


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--description` |  |  Description of the context |
| `--docker` |  |  set the docker endpoint |



## Examples

### Update an existing context

```console
$ docker context update \
    --description "some description" \
    --docker "host=tcp://myserver:2376,ca=~/ca-file,cert=~/cert-file,key=~/key-file" \
    my-context
```



