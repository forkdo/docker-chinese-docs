---
title: 将 Node.js 应用迁移到 DHI
summary: |
  示例展示如何将 Node.js 应用程序迁移到 Docker Hardened Images
type: redirect
target: /dhi/migration/examples/node/
tags: [dhi]

params:
  time: 10 分钟
  featured: true
  image: /images/guides/dhi-examples-nodejs.webp
---
# 将 Node.js 应用迁移到 Docker Hardened Images

本指南将引导您完成将 Node.js 应用程序迁移到 Docker Hardened Images (DHI) 的过程。DHI 提供了增强的安全性和合规性功能，同时保持与标准 Docker 镜像的兼容性。

## 前提条件

- 已安装 Docker
- 现有的 Node.js 应用程序
- 基本的 Docker 知识

## 迁移步骤

### 1. 识别当前基础镜像

首先，检查您当前的 Dockerfile，找到使用的 Node.js 基础镜像：

```dockerfile
# 传统方式
FROM node:18-alpine
```

### 2. 替换为 DHI 镜像

将基础镜像替换为对应的 DHI 镜像。DHI 提供了与官方 Node.js 镜像兼容的版本：

```dockerfile
# DHI 方式
FROM docker.io/library/node:18-alpine

# 或者使用特定的 DHI 标签
FROM docker.io/library/node:18-alpine-dhi
```

### 3. 完整的迁移示例

以下是一个完整的 Dockerfile 示例：

```dockerfile
# 使用 DHI 基础镜像
FROM docker.io/library/node:18-alpine

# 设置工作目录
WORKDIR /app

# 复制 package.json 和安装依赖
COPY package*.json ./
RUN npm ci --only=production

# 复制应用代码
COPY . .

# 创建非 root 用户
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# 更改文件所有权
RUN chown -R nextjs:nodejs /app

# 切换到非 root 用户
USER nextjs

# 暴露端口
EXPOSE 3000

# 启动应用
CMD ["node", "server.js"]
```

### 4. 构建和测试

```bash
# 构建镜像
docker build -t my-nodejs-app:dhi .

# 运行容器
docker run -p 3000:3000 my-nodejs-app:dhi
```

## 最佳实践

### 使用多阶段构建

```dockerfile
# 构建阶段
FROM docker.io/library/node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 运行阶段
FROM docker.io/library/node:18-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

USER nextjs

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

### 安全加固配置

```dockerfile
FROM docker.io/library/node:18-alpine

# 设置非 root 用户
USER node

# 只读文件系统
WORKDIR /app

# 最小化层
COPY package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

COPY . .

EXPOSE 3000

# 使用 exec 形式
CMD ["node", "server.js"]
```

## 验证迁移

1. **功能测试**: 确保应用正常运行
2. **安全扫描**: 使用 Docker Scout 或 Trivy 扫描镜像
3. **性能测试**: 验证性能没有显著下降

```bash
# 使用 Docker Scout 扫描
docker scout cves my-nodejs-app:dhi

# 检查镜像大小
docker images my-nodejs-app:dhi
```

## 常见问题

**Q: DHI 镜像与官方镜像完全兼容吗？**
A: 是的，DHI 镜像保持与官方 Node.js 镜像的 API 和行为兼容。

**Q: 迁移后需要修改应用代码吗？**
A: 通常不需要，除非您的应用依赖特定的系统配置或用户权限。

**Q: 如何处理自定义的 Node.js 版本？**
A: DHI 支持所有主流的 Node.js 版本，您可以选择对应版本的 DHI 镜像。

## 下一步

- 阅读 [DHI 安全指南](/dhi/security/)
- 了解 [DHI 镜像构建最佳实践](/dhi/build/best-practices/)
- 探索更多[迁移示例](/dhi/migration/examples/)