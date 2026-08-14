# 使用 GitHub Actions 导出到 Docker


你可能希望借助 `docker images` 让构建结果在 Docker 客户端中可用，以便在你的工作流另一步骤中使用：

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4
      
      - name: Build
        uses: docker/build-push-action@v7
        with:
          load: true
          tags: myimage:latest
      
      - name: Inspect
        run: |
          docker image inspect myimage:latest
```

