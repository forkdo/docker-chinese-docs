---
title: docker context show
url: /reference/cli/docker/context/show/
parent:
  title: docker context
  url: /reference/cli/docker/context/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker context
    url: /reference/cli/docker/context/
  - title: docker context show
    url: /reference/cli/docker/context/show/
next:
  title: docker context rm
  url: /reference/cli/docker/context/rm/
prev:
  title: docker context update
  url: /reference/cli/docker/context/update/
---

**Description:** Print the name of the current context

**Usage:** `docker context show`



<!--
此页面由 Docker 源代码自动生成。如果你想建议修改此处显示的文本，请在 GitHub 上的源代码仓库中提交问题或拉取请求：

https://github.com/docker/cli
-->








## Description

Print the name of the current context, possibly set by `DOCKER_CONTEXT` environment
variable or `--context` global option.




## Examples

### Print the current context

The following example prints the currently used [`docker context`](/reference/cli/docker/context/):

```console
$ docker context show'
default
```

As an example, this output can be used to dynamically change your shell prompt
to indicate your active context. The example below illustrates how this output
could be used when using Bash as your shell.

Declare a function to obtain the current context in your `~/.bashrc`, and set
this command as your `PROMPT_COMMAND`

```console
function docker_context_prompt() {
        PS1="context: $(docker context show)> "
}

PROMPT_COMMAND=docker_context_prompt
```

After reloading the `~/.bashrc`, the prompt now shows the currently selected
`docker context`:

```console
$ source ~/.bashrc
context: default> docker context create --docker host=unix:///var/run/docker.sock my-context
my-context
Successfully created context "my-context"
context: default> docker context use my-context
my-context
Current context is now "my-context"
context: my-context> docker context use default
default
Current context is now "default"
context: default>
```



