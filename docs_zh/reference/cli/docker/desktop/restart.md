```markdown
---
datafolder: desktop-cli
datafile: docker_desktop_restart
title: docker desktop restart
layout: cli
---
# docker desktop restart

```text
用法：docker desktop restart [选项]
```

重新启动 Docker Desktop。

**注意**：此命令仅在 Docker Desktop 的 CLI 模式下可用。

### 选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `--wait` | bool | `false` | 等待 Docker Desktop 完全启动后再返回 |

### 示例

#### 重新启动 Docker Desktop

```bash
docker desktop restart
```

#### 重新启动 Docker Desktop 并等待其完全启动

```bash
docker desktop restart --wait
```