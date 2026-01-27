# docker compose push

**Description:** Push service images

**Usage:** `docker compose push [OPTIONS] [SERVICE...]`



<!--
抱歉，此页面内容是自动生成自
Docker 的源代码。如果您想建议修改此处显示的文本，
您需要通过搜索此仓库来找到对应的字符串：
https://github.com/docker/compose
-->








## Description

Pushes images for services to their respective registry/repository.

The following assumptions are made:
- You are pushing an image you have built locally
- You have access to the build key

Examples

```yaml
services:
  service1:
    build: .
    image: localhost:5000/yourimage  ## goes to local registry

  service2:
    build: .
    image: your-dockerid/yourimage  ## goes to your repository on Docker Hub
```


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--ignore-push-failures` |  |  Push what it can and ignores images with push failures |
| `--include-deps` |  |  Also push images of services declared as dependencies |
| `-q`, `--quiet` |  |  Push without printing progress information |






