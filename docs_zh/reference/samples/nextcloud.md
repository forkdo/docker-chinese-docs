---
title: Nextcloud 示例
description: Nextcloud 的 Docker 示例。
service: nextcloud
aliases:
- /samples/nexcloud/
---
# Nextcloud 示例

这些示例旨在帮助你快速启动并运行 Nextcloud。它们使用 Docker Compose，因此你应该在系统上安装 Docker 和 Docker Compose。

## 基本示例

此示例启动一个 Nextcloud 实例，该实例使用 SQLite 数据库，并将数据存储在名为 `nextcloud_data` 的 Docker 卷中。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    volumes:
      - nextcloud_data:/var/www/html

volumes:
  nextcloud_data:
```

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

Nextcloud 将在 `http://localhost:8080` 上可用。

## 使用 MariaDB 的示例

此示例使用 MariaDB 作为数据库。它包含两个服务：`nextcloud` 和 `db`。`nextcloud` 服务依赖于 `db` 服务，因此 `db` 服务会首先启动。

```yaml
version: '3'

services:
  db:
    image: mariadb:10.6
    restart: always
    command: --transaction-isolation=READ-COMMITTED --binlog-format=ROW
    volumes:
      - db_data:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=your_root_password
      - MYSQL_PASSWORD=your_password
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud

  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    links:
      - db
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - MYSQL_HOST=db
      - MYSQL_PASSWORD=your_password
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud

volumes:
  db_data:
  nextcloud_data:
```

**注意：** 请将 `your_root_password` 和 `your_password` 替换为安全的密码。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

Nextcloud 将在 `http://localhost:8080` 上可用。首次启动时，系统会提示你创建管理员帐户。

## 使用 PostgreSQL 的示例

此示例使用 PostgreSQL 作为数据库。

```yaml
version: '3'

services:
  db:
    image: postgres:13
    restart: always
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - POSTGRES_PASSWORD=your_password

  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    links:
      - db
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - POSTGRES_HOST=db
      - POSTGRES_PASSWORD=your_password
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud

volumes:
  db_data:
  nextcloud_data:
```

**注意：** 请将 `your_password` 替换为安全的密码。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

Nextcloud 将在 `http://localhost:8080` 上可用。

## 使用 Redis 作为缓存的示例

此示例使用 Redis 作为缓存后端，以提升性能。

```yaml
version: '3'

services:
  redis:
    image: redis:6-alpine
    restart: always

  db:
    image: postgres:13
    restart: always
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - POSTGRES_PASSWORD=your_password

  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    links:
      - db
      - redis
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - POSTGRES_HOST=db
      - POSTGRES_PASSWORD=your_password
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - REDIS_HOST=redis

volumes:
  db_data:
  nextcloud_data:
```

**注意：** 请将 `your_password` 替换为安全的密码。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

Nextcloud 将在 `http://localhost:8080` 上可用。

## 使用 Apache 反向代理的示例

此示例使用 Apache 作为反向代理，并处理 SSL 终止。你需要拥有一个域名，并配置 DNS 将其指向你的服务器 IP。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - VIRTUAL_HOST=your_domain.com
      - LETSENCRYPT_HOST=your_domain.com
      - LETSENCRYPT_EMAIL=your_email@example.com

  apache:
    image: httpd:2.4
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./apache/conf:/usr/local/apache2/conf
      - ./apache/htdocs:/usr/local/apache2/htdocs
      - ./apache/ssl:/usr/local/apache2/ssl
    depends_on:
      - nextcloud

volumes:
  nextcloud_data:
```

**注意：** 你需要配置 Apache 以充当反向代理。请将 `your_domain.com` 和 `your_email@example.com` 替换为你的实际域名和电子邮件地址。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用 Traefik 反向代理的示例

此示例使用 Traefik 作为反向代理，并自动处理 SSL 证书。你需要拥有一个域名，并配置 DNS 将其指向你的服务器 IP。

```yaml
version: '3'

services:
  traefik:
    image: traefik:v2.5
    restart: always
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.myresolver.acme.tlschallenge=true"
      - "--certificatesresolvers.myresolver.acme.email=your_email@example.com"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./letsencrypt:/letsencrypt

  nextcloud:
    image: nextcloud
    restart: always
    volumes:
      - nextcloud_data:/var/www/html
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.nextcloud.rule=Host(`your_domain.com`)"
      - "traefik.http.routers.nextcloud.entrypoints=websecure"
      - "traefik.http.routers.nextcloud.tls.certresolver=myresolver"
    depends_on:
      - traefik

volumes:
  nextcloud_data:
```

**注意：** 请将 `your_email@example.com` 和 `your_domain.com` 替换为你的实际电子邮件地址和域名。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用 Collabora Online 的示例

此示例使用 Collabora Online 集成，允许在 Nextcloud 中编辑 Office 文档。你需要一个有效的域名，因为 Collabora Online 需要通过 HTTPS 提供服务。

```yaml
version: '3'

services:
  db:
    image: postgres:13
    restart: always
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - POSTGRES_PASSWORD=your_password

  redis:
    image: redis:6-alpine
    restart: always

  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    links:
      - db
      - redis
      - collabora
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - POSTGRES_HOST=db
      - POSTGRES_PASSWORD=your_password
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - REDIS_HOST=redis

  collabora:
    image: collabora/code
    restart: always
    environment:
      - domain=your_domain\\.com
      - username=admin
      - password=your_collabora_password
    cap_add:
      - MKNOD
    ports:
      - 9980:9980

volumes:
  db_data:
  nextcloud_data:
```

**注意：** 请将 `your_password`、`your_domain\\.com` 和 `your_collabora_password` 替换为安全的值。`domain` 环境变量需要转义的反斜杠。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

你需要在 Nextcloud 中安装并配置 Collabora Online Connector 应用。

## 使用 OnlyOffice 的示例

此示例使用 OnlyOffice 集成，允许在 Nextcloud 中编辑 Office 文档。

```yaml
version: '3'

services:
  db:
    image: postgres:13
    restart: always
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - POSTGRES_PASSWORD=your_password

  redis:
    image: redis:6-alpine
    restart: always

  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    links:
      - db
      - redis
      - onlyoffice
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - POSTGRES_HOST=db
      - POSTGRES_PASSWORD=your_password
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - REDIS_HOST=redis

  onlyoffice:
    image: onlyoffice/documentserver
    restart: always
    ports:
      - 80:80
    environment:
      - JWT_ENABLED=true
      - JWT_SECRET=your_jwt_secret
      - JWT_HEADER=Authorization
      - JWT_IN_BODY=true

volumes:
  db_data:
  nextcloud_data:
```

**注意：** 请将 `your_password` 和 `your_jwt_secret` 替换为安全的值。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

你需要在 Nextcloud 中安装并配置 OnlyOffice Connector 应用。

## 使用 Talk 的示例

此示例使用 Nextcloud Talk 服务，该服务需要 TURN/STUN 服务器才能正常工作，尤其是在 NAT 环境中。

```yaml
version: '3'

services:
  db:
    image: postgres:13
    restart: always
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - POSTGRES_PASSWORD=your_password

  redis:
    image: redis:6-alpine
    restart: always

  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    links:
      - db
      - redis
      - turnserver
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - POSTGRES_HOST=db
      - POSTGRES_PASSWORD=your_password
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - REDIS_HOST=redis
      - NC_TALK_BOT_TOKEN=your_talk_bot_token

  turnserver:
    image: coturn/coturn
    restart: always
    ports:
      - "3478:3478/tcp"
      - "3478:3478/udp"
      - "5349:5349/tcp"
      - "5349:5349/udp"
    environment:
      - TURN_REALM=your_domain.com
      - TURN_USER=your_turn_user
      - TURN_PASSWORD=your_turn_password
    command: ["-n", "--log-file=stdout", "--fingerprint", "--lt-cred-mech", "--use-auth-secret", "--static-auth-secret=your_turn_secret"]

volumes:
  db_data:
  nextcloud_data:
```

**注意：** 请将 `your_password`、`your_talk_bot_token`、`your_domain.com`、`your_turn_user`、`your_turn_password` 和 `your_turn_secret` 替换为安全的值。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

你需要在 Nextcloud 中安装并配置 Talk 应用。

## 使用 OnlyOffice 和 Collabora Online 的示例

此示例同时使用 OnlyOffice 和 Collabora Online，允许你选择使用哪个 Office 套件。

```yaml
version: '3'

services:
  db:
    image: postgres:13
    restart: always
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - POSTGRES_PASSWORD=your_password

  redis:
    image: redis:6-alpine
    restart: always

  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    links:
      - db
      - redis
      - onlyoffice
      - collabora
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - POSTGRES_HOST=db
      - POSTGRES_PASSWORD=your_password
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - REDIS_HOST=redis

  onlyoffice:
    image: onlyoffice/documentserver
    restart: always
    ports:
      - 80:80
    environment:
      - JWT_ENABLED=true
      - JWT_SECRET=your_jwt_secret
      - JWT_HEADER=Authorization
      - JWT_IN_BODY=true

  collabora:
    image: collabora/code
    restart: always
    environment:
      - domain=your_domain\\.com
      - username=admin
      - password=your_collabora_password
    cap_add:
      - MKNOD
    ports:
      - 9980:9980

volumes:
  db_data:
  nextcloud_data:
```

**注意：** 请将 `your_password`、`your_jwt_secret`、`your_domain\\.com` 和 `your_collabora_password` 替换为安全的值。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

你需要在 Nextcloud 中安装并配置 OnlyOffice Connector 和 Collabora Online Connector 应用。

## 使用高可用性配置的示例

此示例展示了一个高可用性配置，其中包含多个 Nextcloud 实例、一个共享数据库和一个共享 Redis 实例。

```yaml
version: '3'

services:
  db:
    image: postgres:13
    restart: always
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - POSTGRES_PASSWORD=your_password
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager

  redis:
    image: redis:6-alpine
    restart: always
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager

  nextcloud:
    image: nextcloud
    restart: always
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - POSTGRES_HOST=db
      - POSTGRES_PASSWORD=your_password
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - REDIS_HOST=redis

volumes:
  db_data:
  nextcloud_data:
```

**注意：** 此配置适用于 Docker Swarm。请将 `your_password` 替换为安全的密码。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker stack deploy -c docker-compose.yml nextcloud
```

## 使用外部存储的示例

此示例使用 Docker 卷将外部存储挂载到 Nextcloud 中。这对于使用 NFS、S3 或其他外部存储很有用。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    volumes:
      - nextcloud_data:/var/www/html
      - /path/to/external/storage:/external_storage

volumes:
  nextcloud_data:
```

**注意：** 请将 `/path/to/external/storage` 替换为你的外部存储的实际路径。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用自定义配置的示例

此示例使用自定义配置文件覆盖默认的 Nextcloud 配置。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    volumes:
      - nextcloud_data:/var/www/html
      - ./config:/var/www/html/config

volumes:
  nextcloud_data:
```

**注意：** 你需要在 `./config` 目录中创建 `config.php` 文件。请参阅 Nextcloud 文档以获取更多关于自定义配置的信息。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用自定义主题的示例

此示例使用自定义主题覆盖默认的 Nextcloud 外观。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    volumes:
      - nextcloud_data:/var/www/html
      - ./themes:/var/www/html/themes

volumes:
  nextcloud_data:
```

**注意：** 你需要在 `./themes` 目录中创建自定义主题文件。请参阅 Nextcloud 文档以获取更多关于自定义主题的信息。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用预配置的管理员帐户的示例

此示例预配置了管理员帐户，以便在首次启动时无需手动创建。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - NEXTCLOUD_ADMIN_USER=admin
      - NEXTCLOUD_ADMIN_PASSWORD=your_admin_password
      - NEXTCLOUD_DATA_DIR=/var/www/html/data
      - MYSQL_HOST=db
      - MYSQL_PASSWORD=your_password
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
    depends_on:
      - db

  db:
    image: mariadb:10.6
    restart: always
    command: --transaction-isolation=READ-COMMITTED --binlog-format=ROW
    volumes:
      - db_data:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=your_root_password
      - MYSQL_PASSWORD=your_password
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud

volumes:
  db_data:
  nextcloud_data:
```

**注意：** 请将 `your_admin_password`、`your_root_password` 和 `your_password` 替换为安全的密码。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用 Memcached 的示例

此示例使用 Memcached 作为缓存后端。

```yaml
version: '3'

services:
  memcached:
    image: memcached:1.6-alpine
    restart: always

  db:
    image: postgres:13
    restart: always
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - POSTGRES_PASSWORD=your_password

  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    links:
      - db
      - memcached
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - POSTGRES_HOST=db
      - POSTGRES_PASSWORD=your_password
      - POSTGRES_DB=nextcloud
      - POSTGRES_USER=nextcloud
      - MEMCACHED_HOST=memcached

volumes:
  db_data:
  nextcloud_data:
```

**注意：** 请将 `your_password` 替换为安全的密码。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

Nextcloud 将在 `http://localhost:8080` 上可用。

## 使用 SMTP 的示例

此示例使用 SMTP 发送电子邮件通知。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - SMTP_HOST=smtp.example.com
      - SMTP_PORT=587
      - SMTP_SECURE=tls
      - SMTP_NAME=your_smtp_username
      - SMTP_PASSWORD=your_smtp_password
      - MAIL_FROM_ADDRESS=nextcloud
      - MAIL_DOMAIN=example.com

volumes:
  nextcloud_data:
```

**注意：** 请将 `smtp.example.com`、`your_smtp_username`、`your_smtp_password` 和 `example.com` 替换为你的 SMTP 服务器的实际值。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用 LDAP 的示例

此示例使用 LDAP 进行身份验证。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - LDAP_HOST=ldap.example.com
      - LDAP_PORT=389
      - LDAP_BASE_DN=dc=example,dc=com
      - LDAP_BASE_USERS_DN=ou=users,dc=example,dc=com
      - LDAP_BASE_GROUPS_DN=ou=groups,dc=example,dc=com
      - LDAP_FILTER=(&(objectClass=person)(memberOf=cn=nextcloud,ou=groups,dc=example,dc=com))
      - LDAP_LOGIN_FILTER=(&(uid=%uid)(objectClass=person))
      - LDAP_USER_NAME_ATTRIBUTE=uid
      - LDAP_EMAIL_ATTRIBUTE=mail
      - LDAP_GROUP_NAME_ATTRIBUTE=cn
      - LDAP_GROUP_FILTER=(&(objectClass=groupOfNames))
      - LDAP_GROUP_MEMBERS_ATTRIBUTE=member
      - LDAP_CONFIG_ADMIN_USERNAME=admin
      - LDAP_CONFIG_ADMIN_PASSWORD=your_ldap_admin_password
      - LDAP_AGENT_USERNAME=cn=admin,dc=example,dc=com
      - LDAP_AGENT_PASSWORD=your_ldap_agent_password

volumes:
  nextcloud_data:
```

**注意：** 请将所有占位符值替换为你的 LDAP 服务器的实际值。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用 S3 外部存储的示例

此示例使用 S3 作为外部存储后端。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - OBJECTSTORE_S3_HOST=s3.amazonaws.com
      - OBJECTSTORE_S3_PORT=443
      - OBJECTSTORE_S3_SSL=true
      - OBJECTSTORE_S3_BUCKET=your_bucket_name
      - OBJECTSTORE_S3_KEY=your_access_key
      - OBJECTSTORE_S3_SECRET=your_secret_key
      - OBJECTSTORE_S3_REGION=us-east-1
      - OBJECTSTORE_S3_USE_PATH_STYLE=false

volumes:
  nextcloud_data:
```

**注意：** 请将 `your_bucket_name`、`your_access_key`、`your_secret_key` 和 `us-east-1` 替换为你的 S3 存储桶的实际值。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用 Fail2ban 的示例

此示例使用 Fail2ban 防止暴力破解攻击。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    volumes:
      - nextcloud_data:/var/www/html
      - ./logs:/var/log/nginx
    environment:
      - APACHE_LOG_DIR=/var/log/nginx

  fail2ban:
    image: crazymax/fail2ban:latest
    restart: always
    network_mode: "host"
    cap_add:
      - NET_ADMIN
      - NET_RAW
    volumes:
      - ./fail2ban/data:/data
      - ./logs:/var/log/nginx:ro
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - F2B_LOG_TARGET=/var/log/fail2ban.log
      - F2B_LOG_LEVEL=INFO
      - F2B_DB_PURGE_AGE=86400

volumes:
  nextcloud_data:
```

**注意：** 你需要配置 Fail2ban 规则。请参阅 Fail2ban 文档以获取更多信息。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用 ClamAV 的示例

此示例使用 ClamAV 进行病毒扫描。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    ports:
      - 8080:80
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - CLAMAV_HOST=clamav
      - CLAMAV_PORT=3310

  clamav:
    image: clamav/clamav:latest
    restart: always
    ports:
      - 3310:3310
    volumes:
      - clamav_data:/var/lib/clamav

volumes:
  nextcloud_data:
  clamav_data:
```

**注意：** 你需要在 Nextcloud 中安装并配置 Antivirus 应用。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用 OnlyOffice 和 Collabora Online 的示例（带反向代理）

此示例使用反向代理（Traefik）来处理 OnlyOffice 和 Collabora Online 的 SSL 终止。

```yaml
version: '3'

services:
  traefik:
    image: traefik:v2.5
    restart: always
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.myresolver.acme.tlschallenge=true"
      - "--certificatesresolvers.myresolver.acme.email=your_email@example.com"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./letsencrypt:/letsencrypt

  nextcloud:
    image: nextcloud
    restart: always
    volumes:
      - nextcloud_data:/var/www/html
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.nextcloud.rule=Host(`your_domain.com`)"
      - "traefik.http.routers.nextcloud.entrypoints=websecure"
      - "traefik.http.routers.nextcloud.tls.certresolver=myresolver"
    depends_on:
      - traefik

  onlyoffice:
    image: onlyoffice/documentserver
    restart: always
    environment:
      - JWT_ENABLED=true
      - JWT_SECRET=your_jwt_secret
      - JWT_HEADER=Authorization
      - JWT_IN_BODY=true
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.onlyoffice.rule=Host(`onlyoffice.your_domain.com`)"
      - "traefik.http.routers.onlyoffice.entrypoints=websecure"
      - "traefik.http.routers.onlyoffice.tls.certresolver=myresolver"
    depends_on:
      - traefik

  collabora:
    image: collabora/code
    restart: always
    environment:
      - domain=your_domain\\.com
      - username=admin
      - password=your_collabora_password
    cap_add:
      - MKNOD
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.collabora.rule=Host(`collabora.your_domain.com`)"
      - "traefik.http.routers.collabora.entrypoints=websecure"
      - "traefik.http.routers.collabora.tls.certresolver=myresolver"
    depends_on:
      - traefik

volumes:
  nextcloud_data:
```

**注意：** 请将 `your_email@example.com`、`your_domain.com`、`your_jwt_secret`、`onlyoffice.your_domain.com`、`collabora.your_domain.com` 和 `your_collabora_password` 替换为你的实际值。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用 OnlyOffice 和 Collabora Online 的示例（带 Apache 反向代理）

此示例使用 Apache 作为反向代理来处理 OnlyOffice 和 Collabora Online 的 SSL 终止。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - VIRTUAL_HOST=your_domain.com
      - LETSENCRYPT_HOST=your_domain.com
      - LETSENCRYPT_EMAIL=your_email@example.com

  onlyoffice:
    image: onlyoffice/documentserver
    restart: always
    environment:
      - JWT_ENABLED=true
      - JWT_SECRET=your_jwt_secret
      - JWT_HEADER=Authorization
      - JWT_IN_BODY=true
      - VIRTUAL_HOST=onlyoffice.your_domain.com
      - LETSENCRYPT_HOST=onlyoffice.your_domain.com
      - LETSENCRYPT_EMAIL=your_email@example.com

  collabora:
    image: collabora/code
    restart: always
    environment:
      - domain=your_domain\\.com
      - username=admin
      - password=your_collabora_password
      - VIRTUAL_HOST=collabora.your_domain.com
      - LETSENCRYPT_HOST=collabora.your_domain.com
      - LETSENCRYPT_EMAIL=your_email@example.com
    cap_add:
      - MKNOD

  apache:
    image: httpd:2.4
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./apache/conf:/usr/local/apache2/conf
      - ./apache/htdocs:/usr/local/apache2/htdocs
      - ./apache/ssl:/usr/local/apache2/ssl
    depends_on:
      - nextcloud
      - onlyoffice
      - collabora

volumes:
  nextcloud_data:
```

**注意：** 请将 `your_email@example.com`、`your_domain.com`、`your_jwt_secret`、`onlyoffice.your_domain.com`、`collabora.your_domain.com` 和 `your_collabora_password` 替换为你的实际值。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用 OnlyOffice 和 Collabora Online 的示例（带 Nginx 反向代理）

此示例使用 Nginx 作为反向代理来处理 OnlyOffice 和 Collabora Online 的 SSL 终止。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - VIRTUAL_HOST=your_domain.com
      - LETSENCRYPT_HOST=your_domain.com
      - LETSENCRYPT_EMAIL=your_email@example.com

  onlyoffice:
    image: onlyoffice/documentserver
    restart: always
    environment:
      - JWT_ENABLED=true
      - JWT_SECRET=your_jwt_secret
      - JWT_HEADER=Authorization
      - JWT_IN_BODY=true
      - VIRTUAL_HOST=onlyoffice.your_domain.com
      - LETSENCRYPT_HOST=onlyoffice.your_domain.com
      - LETSENCRYPT_EMAIL=your_email@example.com

  collabora:
    image: collabora/code
    restart: always
    environment:
      - domain=your_domain\\.com
      - username=admin
      - password=your_collabora_password
      - VIRTUAL_HOST=collabora.your_domain.com
      - LETSENCRYPT_HOST=collabora.your_domain.com
      - LETSENCRYPT_EMAIL=your_email@example.com
    cap_add:
      - MKNOD

  nginx-proxy:
    image: nginxproxy/nginx-proxy
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/vhost.d:/etc/nginx/vhost.d
      - ./nginx/html:/usr/share/nginx/html
      - ./nginx/certs:/etc/nginx/certs
    depends_on:
      - nextcloud
      - onlyoffice
      - collabora

volumes:
  nextcloud_data:
```

**注意：** 请将 `your_email@example.com`、`your_domain.com`、`your_jwt_secret`、`onlyoffice.your_domain.com`、`collabora.your_domain.com` 和 `your_collabora_password` 替换为你的实际值。

将此内容保存为 `docker-compose.yml`，然后运行：

```bash
docker-compose up -d
```

## 使用 OnlyOffice 和 Collabora Online 的示例（带 Caddy 反向代理）

此示例使用 Caddy 作为反向代理来处理 OnlyOffice 和 Collabora Online 的 SSL 终止。

```yaml
version: '3'

services:
  nextcloud:
    image: nextcloud
    restart: always
    volumes:
      - nextcloud_data:/var/www/html
    environment:
      - VIRTUAL_HOST=your_domain.com
      - LETSENCRYPT_HOST=your_domain.com
      - LETSENCRYPT_EMAIL=your_email@example.com

  onlyoffice:
    image: onlyoffice/documentserver
    restart: always
    environment:
      - JWT_ENABLED=true
      - JWT_SECRET=your_jwt_secret
      - JWT_HEADER=Authorization
      - JWT_IN_BODY=true
      - VIRTUAL_HOST=onlyoffice.your_domain.com
      - LETSENCRYPT_HOST=onlyoffice.your_domain.com
      - LETSENCRYPT_EMAIL=your_email@example.com

  collabora:
    image: collabora/code
    restart: always
    environment:
      - domain=your_domain\\.com
      - username=admin
      - password=your_collabora_password