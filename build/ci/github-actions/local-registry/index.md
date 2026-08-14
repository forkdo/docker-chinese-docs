# 配合 GitHub Actions 使用本地注册表


出于测试目的，你可能需要创建一个 [本地注册表](https://hub.docker.com/_/registry)
来推送镜像：

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    services:
      registry:
        image: registry:3
        ports:
          - 5000:5000
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4
        with:
          driver-opts: network=host
      
      - name: Build and push to local registry
        uses: docker/build-push-action@v7
        with:
          push: true
          tags: localhost:5000/name/app:latest
      
      - name: Inspect
        run: |
          docker buildx imagetools inspect localhost:5000/name/app:latest
```

