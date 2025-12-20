# 控制 Compose 中的启动和关闭顺序

您可以使用 [depends_on](/reference/compose-file/services.md#depends_on) 属性控制服务启动和关闭的顺序。Compose 总是按照依赖顺序启动和停止容器，其中依赖关系由 `depends_on`、`links`、`volumes_from` 和 `network_mode: "service:..."` 确定。

例如，如果您的应用程序需要访问数据库，并且这两个服务都通过 `docker compose up` 启动，那么可能会失败，因为应用程序服务可能在数据库服务之前启动，找不到能够处理其 SQL 语句的数据库。

## 控制启动

在启动时，Compose 不会等待容器“就绪”，只会等待它运行。如果您的关系型数据库系统需要先启动自己的服务才能处理传入连接，这可能会导致问题。

检测服务就绪状态的解决方案是使用 `condition` 属性，可选以下选项之一：

- `service_started`
- `service_healthy`。这指定依赖项在启动依赖服务之前应该是“健康”的，通过 `healthcheck` 定义。
- `service_completed_successfully`。这指定依赖项在启动依赖服务之前应该成功运行到完成。

## 示例

```yaml
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
        restart: true
      redis:
        condition: service_started
  redis:
    image: redis
  db:
    image: postgres:18
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 10s
      retries: 5
      start_period: 30s
      timeout: 10s
```

Compose 按依赖顺序创建服务。`db` 和 `redis` 在 `web` 之前创建。

Compose 等待标记为 `service_healthy` 的依赖项的健康检查通过。`db` 在 `web` 创建之前应该是“健康”的（由 `healthcheck` 指示）。

`restart: true` 确保如果 `db` 由于显式的 Compose 操作（例如 `docker compose restart`）而被更新或重启，`web` 服务也会自动重启，确保它能正确重新建立连接或依赖关系。

`db` 服务的健康检查使用 `pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}` 命令检查 PostgreSQL 数据库是否就绪。该服务每 10 秒重试一次，最多 5 次。

Compose 也按依赖顺序删除服务。`web` 在 `db` 和 `redis` 之前删除。

## 参考信息

- [`depends_on`](/reference/compose-file/services.md#depends_on)
- [`healthcheck`](/reference/compose-file/services.md#healthcheck)
