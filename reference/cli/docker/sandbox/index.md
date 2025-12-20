# Docker 沙箱
# Docker 沙箱

Docker 沙箱是一个隔离的环境，用于在容器中运行代码，而不会影响主机系统。这对于测试、开发和安全实验非常有用。

## 前置条件

- Docker 已安装并运行
- 基本的 Docker 知识

## 快速开始

### 1. 创建沙箱

```bash
# 创建一个新的 Docker 沙箱
docker run -d --name my-sandbox \
  -v /path/to/your/code:/workspace \
  -p 8080:8080 \
  --restart unless-stopped \
  ubuntu:latest tail -f /dev/null

# 进入沙箱
docker exec -it my-sandbox bash
```

### 2. 使用沙箱

```bash
# 在沙箱中安装软件
apt-get update && apt-get install -y python3 python3-pip

# 运行你的代码
python3 /workspace/app.py
```

## 常用命令

| 命令 | 描述 |
|------|------|
| `docker ps` | 查看运行中的沙箱 |
| `docker stop <name>` | 停止沙箱 |
| `docker start <name>` | 启动沙箱 |
| `docker rm <name>` | 删除沙箱 |
| `docker logs <name>` | 查看沙箱日志 |

## 配置示例

### docker-compose.yml

```yaml
version: '3.8'
services:
  sandbox:
    image: ubuntu:latest
    container_name: my-sandbox
    volumes:
      - ./code:/workspace
    ports:
      - "8080:8080"
    restart: unless-stopped
    command: tail -f /dev/null
```

## 最佳实践

1. **使用非 root 用户**：在容器中创建专用用户
2. **限制资源**：使用 `--cpus` 和 `--memory` 参数
3. **只读挂载**：对于不需要写入的目录使用只读挂载
4. **清理**：定期删除不再使用的沙箱

## 故障排除

### 问题：沙箱无法启动

**解决方案**：
```bash
# 检查 Docker 状态
systemctl status docker

# 检查端口冲突
netstat -tulpn | grep 8080
```

### 问题：无法访问沙箱中的文件

**解决方案**：
```bash
# 检查挂载点
docker inspect my-sandbox | grep Mounts -A 10

# 验证权限
ls -la /path/to/your/code
```

## 安全提示

- 不要在沙箱中存储敏感信息
- 使用网络隔离（`--network none`）
- 定期更新基础镜像
- 监控容器资源使用情况

## 相关链接

- [Docker 官方文档](https://docs.docker.com/)
- [Docker CLI 参考](https://docs.docker.com/engine/reference/commandline/docker/)
- [最佳实践指南](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

- [](https://docs.docker.com/reference/cli/docker/sandbox/version/)

- [docker sandbox inspect](https://docs.docker.com/reference/cli/docker/sandbox/inspect/)

- [docker sandbox ls](https://docs.docker.com/reference/cli/docker/sandbox/ls/)

- [docker sandbox run](https://docs.docker.com/reference/cli/docker/sandbox/run/)

- [docker sandbox 删除](https://docs.docker.com/reference/cli/docker/sandbox/rm/)

