# 使用 GitHub Actions 更新 Docker Hub 描述


你可以使用一个名为 [Docker Hub Description](https://github.com/peter-evans/dockerhub-description)
的第三方 action 来更新 Docker Hub 仓库描述：

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          push: true
          tags: user/app:latest

      - name: Update repo description
        uses: peter-evans/dockerhub-description@e98e4d1628a5f3be2be7c231e50981aee98723ae # v4.0.0
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
          repository: user/app
```

