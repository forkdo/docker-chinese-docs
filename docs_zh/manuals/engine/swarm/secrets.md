---
title: 使用 Docker secrets 管理敏感数据
description: 如何安全地存储、检索和使用 Docker 服务的敏感数据
keywords: swarm, secrets, credentials, sensitive strings, sensitive data, security, encryption, encryption at rest
tags:
- Secrets
---

## 关于 secrets

从 Docker Swarm 服务的角度来看，_secret_ 是一段数据块，例如密码、SSH 私钥、SSL 证书，或者其他不应通过网络传输或在 Dockerfile 或应用程序源代码中以明文存储的数据。你可以使用 Docker _secrets_ 集中管理这些数据，并仅将其安全地传输给需要访问它的容器。Secrets 在 Docker swarm 中的传输和存储都是加密的。给定的 secret 只能被那些被明确授予访问权限的服务访问，并且仅在这些服务任务运行时有效。

你可以使用 secrets 来管理容器在运行时需要但又不希望存储在镜像中或源代码控制中的任何敏感数据，例如：

- 用户名和密码
- TLS 证书和密钥
- SSH 密钥
- 其他重要数据，例如数据库或内部服务器的名称
- 通用字符串或二进制内容（最大 500 KB）

> [!NOTE]
>
> Docker secrets 仅对 swarm 服务可用，对独立容器不可用。要使用此功能，请考虑调整你的容器以作为服务运行。有状态容器通常可以以 1 的规模运行，而无需更改容器代码。

使用 secrets 的另一个用例是在容器和一组凭据之间提供一层抽象。考虑一个场景，你的应用程序有独立的开发、测试和生产环境。每个环境都可以在开发、测试和生产 swarm 中使用相同的 secret 名称存储不同的凭据。你的容器只需要知道 secret 的名称就能在所有三个环境中工作。

你也可以使用 secrets 来管理非敏感数据，例如配置文件。但是，Docker 支持使用 [configs](configs.md) 来存储非敏感数据。Configs 直接挂载到容器的文件系统中，无需使用 RAM 磁盘。

### Windows 支持

Docker 包含对 Windows 容器中 secrets 的支持。在实现上存在差异的地方，下面的示例中会特别指出。请记住以下显著差异：

- Microsoft Windows 没有内置的 RAM 磁盘管理驱动程序，因此在运行的 Windows 容器中，secrets 以明文形式持久化到容器的根磁盘上。但是，当容器停止时，secrets 会被明确删除。此外，Windows 不支持使用 `docker commit` 或类似命令将运行的容器持久化为镜像。

- 在 Windows 上，我们建议在主机机器上包含 Docker 根目录的卷上启用
  [BitLocker](https://technet.microsoft.com/en-us/library/cc732774(v=ws.11).aspx)，以确保运行容器的 secrets 在静态时得到加密。

- 具有自定义目标的 secret 文件不会直接绑定挂载到 Windows 容器中，因为 Windows 不支持非目录文件绑定挂载。相反，容器的所有 secrets 都挂载在容器内的 `C:\ProgramData\Docker\internal\secrets` 中（这是一个实现细节，应用程序不应依赖于此）。符号链接用于从那里指向容器内 secret 的期望目标。默认目标是 `C:\ProgramData\Docker\secrets`。

- 创建使用 Windows 容器的服务时，不支持为 secrets 指定 UID、GID 和 mode 选项。Secrets 目前只能由容器内的管理员和具有 `system` 访问权限的用户访问。

## Docker 如何管理 secrets

当你向 swarm 添加 secret 时，Docker 通过相互 TLS 连接将 secret 发送到 swarm 管理器。Secret 存储在加密的 Raft 日志中。整个 Raft 日志在其他管理器之间复制，确保 secrets 与其他 swarm 管理数据具有相同的高可用性保证。

当你授予新创建或正在运行的服务访问 secret 的权限时，解密的 secret 会挂载到容器的内存文件系统中。容器内挂载点的位置默认为 Linux 容器中的 `/run/secrets/<secret_name>`，或 Windows 容器中的 `C:\ProgramData\Docker\secrets`。你也可以指定自定义位置。

你可以随时更新服务以授予其访问额外 secrets 的权限或撤销其对给定 secret 的访问权限。

节点只有在是 swarm 管理器或正在运行被授予访问 secret 权限的服务任务时，才能访问（加密的）secrets。当容器任务停止运行时，与其共享的解密 secrets 会从该容器的内存文件系统中卸载并从节点的内存中清除。

如果节点在运行具有访问 secret 权限的任务容器时失去与 swarm 的连接，任务容器仍然可以访问其 secrets，但在节点重新连接到 swarm 之前无法接收更新。

你可以随时添加或检查单个 secret，或列出所有 secrets。你不能删除正在运行的服务使用的 secret。请参阅 [轮换 secret](secrets.md#example-rotate-a-secret) 以了解在不中断运行服务的情况下删除 secret 的方法。

为了更容易更新或回滚 secrets，请考虑在 secret 名称中添加版本号或日期。由于可以控制 secret 在给定容器内的挂载点，这变得更容易。

## 了解 `docker secret` 命令的更多信息

使用这些链接了解特定命令的详细信息，或继续阅读
[关于在服务中使用 secrets 的示例](secrets.md#simple-example-get-started-with-secrets)。

- [`docker secret create`](/reference/cli/docker/secret/create.md)
- [`docker secret inspect`](/reference/cli/docker/secret/inspect.md)
- [`docker secret ls`](/reference/cli/docker/secret/ls.md)
- [`docker secret rm`](/reference/cli/docker/secret/rm.md)
- [`--secret`](/reference/cli/docker/service/create.md#secret) 标志用于 `docker service create`
- [`--secret-add` 和 `--secret-rm`](/reference/cli/docker/service/update.md#secret-add) 标志用于 `docker service update`

## 示例

本节包含三个渐进的示例，说明如何使用 Docker secrets。这些示例中使用的镜像已更新以更容易使用 Docker secrets。要了解如何以类似方式修改你自己的镜像，请参阅
[在你的镜像中构建 Docker Secrets 支持](#build-support-for-docker-secrets-into-your-images)。

> [!NOTE]
>
> 这些示例使用单引擎 swarm 和未扩展的服务以简化说明。示例使用 Linux 容器，但 Windows 容器也支持 secrets。请参阅 [Windows 支持](#windows-support)。

### 在 compose 文件中定义和使用 secrets

`docker-compose` 和 `docker stack` 命令都支持在 compose 文件中定义 secrets。详细信息请参阅
[Compose 文件参考](/reference/compose-file/legacy-versions.md)。

### 简单示例：开始使用 secrets

这个简单示例展示了 secrets 在几个命令中是如何工作的。要了解真实世界的示例，请继续阅读
[中级示例：在 Nginx 服务中使用 secrets](#intermediate-example-use-secrets-with-a-nginx-service)。

1.  向 Docker 添加一个 secret。`docker secret create` 命令读取标准输入，因为最后一个参数（表示要从其读取 secret 的文件）设置为 `-`。

    ```console
    $ printf "This is a secret" | docker secret create my_secret_data -
    ```

2.  创建一个 `redis` 服务并授予其访问 secret 的权限。默认情况下，容器可以在 `/run/secrets/<secret_name>` 访问 secret，但你可以使用 `target` 选项自定义容器中的文件名。

    ```console
    $ docker service  create --name redis --secret my_secret_data redis:alpine
    ```

3.  使用 `docker service ps` 验证任务是否正常运行。如果一切正常，输出看起来类似于：

    ```console
    $ docker service ps redis

    ID            NAME     IMAGE         NODE              DESIRED STATE  CURRENT STATE          ERROR  PORTS
    bkna6bpn8r1a  redis.1  redis:alpine  ip-172-31-46-109  Running        Running 8 seconds ago  
    ```

    如果有错误，任务会失败并反复重启，你会看到类似这样的内容：

    ```console
    $ docker service ps redis

    NAME                      IMAGE         NODE  DESIRED STATE  CURRENT STATE          ERROR                      PORTS
    redis.1.siftice35gla      redis:alpine  moby  Running        Running 4 seconds ago                             
     \_ redis.1.whum5b7gu13e  redis:alpine  moby  Shutdown       Failed 20 seconds ago      "task: non-zero exit (1)"  
     \_ redis.1.2s6yorvd9zow  redis:alpine  moby  Shutdown       Failed 56 seconds ago      "task: non-zero exit (1)"  
     \_ redis.1.ulfzrcyaf6pg  redis:alpine  moby  Shutdown       Failed about a minute ago  "task: non-zero exit (1)"  
     \_ redis.1.wrny5v4xyps6  redis:alpine  moby  Shutdown       Failed 2 minutes ago       "task: non-zero exit (1)"
    ```

4.  使用 `docker ps` 获取 `redis` 服务任务容器的 ID，以便你可以使用 `docker container exec` 连接到容器并读取 secret 数据文件的内容，secret 默认对所有用户可读，名称与 secret 名称相同。下面的第一个命令说明了如何找到容器 ID，第二和第三个命令使用 shell 补全自动执行此操作。

    ```console
    $ docker ps --filter name=redis -q

    5cb1c2348a59

    $ docker container exec $(docker ps --filter name=redis -q) ls -l /run/secrets

    total 4
    -r--r--r--    1 root     root            17 Dec 13 22:48 my_secret_data

    $ docker container exec $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data

    This is a secret
    ```

5.  验证如果提交容器，secret 不可用。

    ```console
    $ docker commit $(docker ps --filter name=redis -q) committed_redis

    $ docker run --rm -it committed_redis cat /run/secrets/my_secret_data

    cat: can't open '/run/secrets/my_secret_data': No such file or directory
    ```

6.  尝试删除 secret。由于 `redis` 服务正在运行并具有访问 secret 的权限，删除失败。

    ```console
    $ docker secret ls

    ID                          NAME                CREATED             UPDATED
    wwwrxza8sxy025bas86593fqs   my_secret_data      4 hours ago         4 hours ago


    $ docker secret rm my_secret_data

    Error response from daemon: rpc error: code = 3 desc = secret
    'my_secret_data' is in use by the following service: redis
    ```

7.  通过更新服务从正在运行的 `redis` 服务中删除对 secret 的访问权限。

    ```console
    $ docker service update --secret-rm my_secret_data redis
    ```

8.  重复步骤 3 和 4，验证服务不再有访问 secret 的权限。容器 ID 不同，因为 `service update` 命令重新部署了服务。

    ```console
    $ docker container exec -it $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data

    cat: can't open '/run/secrets/my_secret_data': No such file or directory
    ```

9.  停止并删除服务，并从 Docker 中删除 secret。

    ```console
    $ docker service rm redis

    $ docker secret rm my_secret_data
    ```

### 简单示例：在 Windows 服务中使用 secrets

这是一个非常简单的示例，展示如何在 Docker for Windows 上运行的 Microsoft IIS 服务中使用 secrets，该服务在 Microsoft Windows 10 上运行 Windows 容器。这是一个天真的示例，将网页存储在 secret 中。

本示例假设你已安装 PowerShell。

1.  将以下内容保存到新文件 `index.html` 中。

    ```html
    <html lang="en">
      <head><title>Hello Docker</title></head>
      <body>
        <p>Hello Docker! You have deployed a HTML page.</p>
      </body>
    </html>
    ```

2.  如果尚未初始化或加入 swarm，请执行此操作。

    ```console
    > docker swarm init
    ```

3.  将 `index.html` 文件作为名为 `homepage` 的 swarm secret 保存。

    ```console
    > docker secret create homepage index.html
    ```

4.  创建一个 IIS 服务并授予其访问 `homepage` secret 的权限。

    ```console
    > docker service create `
        --name my-iis `
        --publish published=8000,target=8000 `
        --secret src=homepage,target="\inetpub\wwwroot\index.html" `
        microsoft/iis:nanoserver
    ```

    > [!NOTE]
    >
    > 从技术上讲，此示例没有使用 secrets 的原因；[configs](configs.md) 更适合。此示例仅用于说明。

5.  访问 `http://localhost:8000/` 上的 IIS 服务。它应该提供来自第一步的 HTML 内容。

6.  删除服务和 secret。

    ```console
    > docker service rm my-iis
    > docker secret rm homepage
    > docker image remove secret-test
    ```

### 中级示例：在 Nginx 服务中使用 secrets

此示例分为两部分。
[第一部分](#generate-the-site-certificate) 完全关于生成站点证书，不直接涉及 Docker secrets，但它为 [第二部分](#configure-the-nginx-container) 做准备，在第二部分中你将存储和使用站点证书和 Nginx 配置作为 secrets。

#### 生成站点证书

为你的站点生成根 CA 和 TLS 证书及密钥。对于生产站点，你可能希望使用 `Let’s Encrypt` 等服务生成 TLS 证书和密钥，但此示例使用命令行工具。这一步有点复杂，但只是一个设置步骤，以便你有东西可以作为 Docker secret 存储。如果你不想执行这些子步骤，可以 [使用 Let's Encrypt](https://letsencrypt.org/getting-started/) 生成站点密钥和证书，将文件命名为 `site.key` 和 `site.crt`，然后跳到
[配置 Nginx 容器](#configure-the-nginx-container)。

1.  生成根密钥。

    ```console
    $ openssl genrsa -out "root-ca.key" 4096
    ```

2.  使用根密钥生成 CSR。

    ```console
    $ openssl req \
              -new -key "root-ca.key" \
              -out "root-ca.csr" -sha256 \
              -subj '/C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA'
    ```

3.  配置根 CA。编辑一个名为 `root-ca.cnf` 的新文件并将其以下内容粘贴到其中。这限制了根 CA 只能签署叶证书而不能签署中间 CA。

    ```ini
    [root_ca]
    basicConstraints = critical,CA:TRUE,pathlen:1
    keyUsage = critical, nonRepudiation, cRLSign, keyCertSign
    subjectKeyIdentifier=hash
    ```

4.  签署证书。

    ```console
    $ openssl x509 -req  -days 3650  -in "root-ca.csr" \
                   -signkey "root-ca.key" -sha256 -out "root-ca.crt" \
                   -extfile "root-ca.cnf" -extensions \
                   root_ca
    ```

5.  生成站点密钥。

    ```console
    $ openssl genrsa -out "site.key" 4096
    ```

6.  生成站点证书并使用站点密钥签署它。

    ```console
    $ openssl req -new -key "site.key" -out "site.csr" -sha256 \
              -subj '/C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost'
    ```

7.  配置站点证书。编辑一个名为 `site.cnf` 的新文件并将其以下内容粘贴到其中。这限制了站点证书只能用于身份验证服务器，不能用于签署证书。

    ```ini
    [server]
    authorityKeyIdentifier=keyid,issuer
    basicConstraints = critical,CA:FALSE
    extendedKeyUsage=serverAuth
    keyUsage = critical, digitalSignature, keyEncipherment
    subjectAltName = DNS:localhost, IP:127.0.0.1
    subjectKeyIdentifier=hash
    ```

8.  签署站点证书。

    ```console
    $ openssl x509 -req -days 750 -in "site.csr" -sha256 \
        -CA "root-ca.crt" -CAkey "root-ca.key"  -CAcreateserial \
        -out "site.crt" -extfile "site.cnf" -extensions server
    ```

9.  `site.csr` 和 `site.cnf` 文件不需要由 Nginx 服务使用，但如果你要生成新的站点证书，你需要它们。保护 `root-ca.key` 文件。

#### 配置 Nginx 容器

1.  生成一个非常基本的 Nginx 配置，通过 HTTPS 提供静态文件。TLS 证书和密钥存储为 Docker secrets，以便可以轻松轮换它们。

    在当前目录中，创建一个名为 `site.conf` 的新文件，内容如下：

    ```nginx
    server {
        listen                443 ssl;
        server_name           localhost;
        ssl_certificate       /run/secrets/site.crt;
        ssl_certificate_key   /run/secrets/site.key;

        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
    }
    ```

2.  创建三个 secrets，代表密钥、证书和 `site.conf`。你可以将任何文件存储为 secret，只要它小于 500 KB。这允许你将密钥、证书和配置与使用它们的服务解耦。在这些命令中的每一个中，最后一个参数表示要从主机机器文件系统中读取 secret 的文件路径。在这些示例中，secret 名称和文件名称相同。

    ```console
    $ docker secret create site.key site.key

    $ docker secret create site.crt site.crt

    $ docker secret create site.conf site.conf
    ```

    ```console
    $ docker secret ls

    ID                          NAME                  CREATED             UPDATED
    2hvoi9mnnaof7olr3z5g3g7fp   site.key       58 seconds ago      58 seconds ago
    aya1dh363719pkiuoldpter4b   site.crt       24 seconds ago      24 seconds ago
    zoa5df26f7vpcoz42qf2csth8   site.conf      11 seconds ago      11 seconds ago
    ```

3.  创建一个运行 Nginx 并可以访问三个 secrets 的服务。`docker service create` 命令的最后一部分在 `site.conf` secret 的位置和 `/etc/nginx.conf.d/`（Nginx 查找额外配置文件的位置）之间创建一个符号链接。此步骤在 Nginx 实际启动之前发生，因此如果你更改 Nginx 配置，不需要重建镜像。

    > [!NOTE]
    >
    > 通常你会创建一个 Dockerfile 来复制 `site.conf` 到适当位置，构建镜像，并运行使用自定义镜像的容器。此示例不需要自定义镜像。它将 `site.conf` 放到位并在一步中运行容器。

    默认情况下，Secrets 位于容器内的 `/run/secrets/` 目录中，这可能需要在容器内采取额外步骤使 secret 在不同路径中可用。下面的示例说明了如何使 `site.conf` secret 在容器内的 `/etc/nginx/conf.d/site.conf` 处可用，而无需使用符号链接：

    ```console
    $ docker service create \
         --name nginx \
         --secret site.key \
         --secret site.crt \
         --secret source=site.conf,target=/etc/nginx/conf.d/site.conf \
         --publish published=3000,target=443 \
         nginx:latest \
         sh -c "exec nginx -g 'daemon off;'"
    ```

    相反，Secrets 允许你使用 `target` 选项指定自定义位置。下面的示例说明了如何使 `site.conf` secret 在容器内的 `/etc/nginx/conf.d/site.conf` 处可用，而无需使用符号链接：

    ```console
    $ docker service create \
         --name nginx \
         --secret source=site.conf,target=/etc/nginx/conf.d/site.conf \
         --publish published=3000,target=443 \
         nginx:latest \
         sh -c "exec nginx -g 'daemon off;'"
    ```

    `site.key` 和 `site.crt` secrets 使用简写语法，没有设置自定义 `target` 位置。简写语法将 secrets 挂载在 `/run/secrets/` 中，名称与 secret 相同。在正在运行的容器内，现在存在以下三个文件：

    - `/run/secrets/site.key`
    - `/run/secrets/site.crt`
    - `/etc/nginx/conf.d/site.conf`

4.  验证 Nginx 服务正在运行。

    ```console
    $ docker service ls

    ID            NAME   MODE        REPLICAS  IMAGE
    zeskcec62q24  nginx  replicated  1/1       nginx:latest

    $ docker service ps nginx

    NAME                  IMAGE         NODE  DESIRED STATE  CURRENT STATE          ERROR  PORTS
    nginx.1.9ls3yo9ugcls  nginx:latest  moby  Running        Running 3 minutes ago
    ```

5.  验证服务正在运行：你可以访问 Nginx 服务器，并且正在使用正确的 TLS 证书。

    ```console
    $ curl --cacert root-ca.crt https://localhost:3000

    <!DOCTYPE html>
    <html>
    <head>
    <title>Welcome to nginx!</title>
    <style>
        body {
            width: 35em;
            margin: 0 auto;
            font-family: Tahoma, Verdana, Arial, sans-serif;
        }
    </style>
    </head>
    <body>
    <h1>Welcome to nginx!</h1>
    <p>If you see this page, the nginx web server is successfully installed and
    working. Further configuration is required.</p>

    <p>For online documentation and support. refer to
    <a href="https://nginx.org">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="https://www.nginx.com">nginx.com</a>.</p>

    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>
    ```

    ```console
    $ openssl s_client -connect localhost:3000 -CAfile root-ca.crt

    CONNECTED(00000003)
    depth=1 /C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA
    verify return:1
    depth=0 /C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost
    verify return:1
    ---
    Certificate chain
     0 s:/C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost
       i:/C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA
    ---
    Server certificate
    -----BEGIN CERTIFICATE-----
    …
    -----END CERTIFICATE-----
    subject=/C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost
    issuer=/C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA
    ---
    No client certificate CA names sent
    ---
    SSL handshake has read 1663 bytes and written 712 bytes
    ---
    New, TLSv1/SSLv3, Cipher is AES256-SHA
    Server public key is 4096 bit
    Secure Renegotiation IS supported
    Compression: NONE
    Expansion: NONE
    SSL-Session:
        Protocol  : TLSv1
        Cipher    : AES256-SHA
        Session-ID: A1A8BF35549C5715648A12FD7B7E3D861539316B03440187D9DA6C2E48822853
        Session-ID-ctx:
        Master-Key: F39D1B12274BA16D3A906F390A61438221E381952E9E1E05D3DD784F0135FB81353DA38C6D5C021CB926E844DFC49FC4
        Key-Arg   : None
        Start Time: 1481685096
        Timeout   : 300 (sec)
        Verify return code: 0 (ok)
    ```

6.  在运行此示例后清理，删除 `nginx` 服务和存储的 secrets。

    ```console
    $ docker service rm nginx

    $ docker secret rm site.crt site.key site.conf
    ```

### 高级示例：在 WordPress 服务中使用 secrets

在此示例中，你创建一个自定义根密码的单节点 MySQL 服务，将凭据添加为 secrets，并创建一个单节点 WordPress 服务，使用这些凭据连接到 MySQL。[下一个示例](#example-rotate-a-secret) 基于此示例，向你展示如何轮换 MySQL 密码并更新服务，以便 WordPress 服务仍能连接到 MySQL。

此示例说明了一些技术，以避免将敏感凭据保存在镜像中或通过命令行直接传递。

> [!NOTE]
>
> 此示例使用单引擎 swarm 以简化说明，并使用单节点 MySQL 服务，因为单个 MySQL 服务器实例无法通过简单地使用复制服务来扩展，设置 MySQL 集群超出了此示例的范围。
>
> 此外，更改 MySQL 根密码不像更改磁盘上的单个文件那么简单。你必须使用查询或 `mysqladmin` 命令来更改 MySQL 中的密码。

1.  为 MySQL 生成随机字母数字密码并将其存储为名为 `mysql_password` 的 Docker secret，使用 `docker secret create` 命令。要使密码更短或更长，请调整 `openssl` 命令的最后一个参数。这只是创建相对随机密码的一种方法。如果你愿意，可以使用另一个命令生成密码。

    > [!NOTE]
    >
    > 创建 secret 后，你无法更新它。你只能删除并重新创建它，并且不能删除服务正在使用的 secret。但是，你可以使用 `docker service update` 授予或撤销运行服务对 secrets 的访问权限。如果你需要更新 secret 的能力，请考虑在 secret 名称中添加版本组件，以便你以后可以添加新版本，更新服务使用它，然后删除旧版本。

    最后一个参数设置为 `-`，表示从标准输入读取输入。

    ```console
    $ openssl rand -base64 20 | docker secret create mysql_password -

    l1vinzevzhj4goakjap5ya409
    ```

    返回的值不是密码，而是 secret 的 ID。在本教程的其余部分，省略了 ID 输出。

    为 MySQL `root` 用户生成第二个 secret。此 secret 不与稍后创建的 WordPress 服务共享。它仅在引导 `mysql` 服务时需要。

    ```console
    $ openssl rand -base64 20 | docker secret create mysql_root_password -
    ```

    使用 `docker secret ls` 列出 Docker 管理的 secrets：

    ```console
    $ docker secret ls

    ID                          NAME                  CREATED             UPDATED
    l1vinzevzhj4goakjap5ya409   mysql_password        41 seconds ago      41 seconds ago
    yvsczlx9votfw3l0nz5rlidig   mysql_root_password   12 seconds ago      12 seconds ago
    ```

    Secrets 存储在 swarm 的加密 Raft 日志中。

2.  创建一个用户定义的覆盖网络，用于 MySQL 和 WordPress 服务之间的通信。没有必要将 MySQL 服务暴露给任何外部主机或容器。

    ```console
    $ docker network create -d overlay mysql_private
    ```

3.  创建 MySQL 服务。MySQL 服务具有以下特征：

    - 因为规模设置为 `1`，所以只运行一个 MySQL 任务。负载均衡 MySQL 留给读者作为练习，涉及的不仅仅是扩展服务。
    - 只能被 `mysql_private` 网络上的其他容器访问。
    - 使用卷 `mydata` 存储 MySQL 数据，以便在 `mysql` 服务重启时持久化。
    - Secrets 分别挂载在容器的 `tmpfs` 文件系统中的 `/run/secrets/mysql_password` 和 `/run/secrets/mysql_root_password`。它们永远不会作为环境变量暴露，也不能在运行 `docker commit` 命令时提交到镜像中。`mysql_password` secret 是非特权 WordPress 容器用于连接 MySQL 的那个。
    - 设置环境变量 `MYSQL_PASSWORD_FILE` 和 `MYSQL_ROOT_PASSWORD_FILE` 指向文件 `/run/secrets/mysql_password` 和 `/run/secrets/mysql_root_password`。`mysql` 镜像在首次初始化系统数据库时从这些文件读取密码字符串。之后，密码存储在 MySQL 系统数据库本身中。
    - 设置环境变量 `MYSQL_USER` 和 `MYSQL_DATABASE`。创建一个名为 `wordpress` 的新数据库，当容器启动时，`wordpress` 用户对此数据库具有完全权限。此用户无法创建或删除数据库或更改 MySQL 配置。

      ```console
      $ docker service create \
           --name mysql \
           --replicas 1 \
           --network mysql_private \
           --mount type=volume,source=mydata,destination=/var/lib/mysql \
           --secret source=mysql_root_password,target=mysql_root_password \
           --secret source=mysql_password,target=mysql_password \
           -e MYSQL_ROOT_PASSWORD_FILE="/run/secrets/mysql_root_password" \
           -e MYSQL_PASSWORD_FILE="/run/secrets/mysql_password" \
           -e MYSQL_USER="wordpress" \
           -e MYSQL_DATABASE="wordpress" \
           mysql:latest
      ```

4.  使用 `docker service ls` 命令验证 `mysql` 容器正在运行。

    ```console
    $ docker service ls

    ID            NAME   MODE        REPLICAS  IMAGE
    wvnh0siktqr3  mysql  replicated  1/1       mysql:latest
    ```

5.  现在 MySQL 已设置，创建一个连接到 MySQL 服务的 WordPress 服务。WordPress 服务具有以下特征：

    - 因为规模设置为 `1`，所以只运行一个 WordPress 任务。负载均衡 WordPress 留给读者作为练习，因为将 WordPress 会话数据存储在容器文件系统上的限制。
    - 在主机机器的端口 30000 上暴露 WordPress，因此你可以从外部主机访问它。如果你在主机机器的端口 80 上没有 web 服务器，可以暴露端口 80。
    - 连接到 `mysql_private` 网络，因此它可以与 `mysql` 容器通信，并且还将端口 80 发布到所有 swarm 节点的端口 30000。
    - 可以访问 `mysql_password` secret，但指定容器内不同的目标文件名。WordPress 容器使用挂载点 `/run/secrets/wp_db_password`。
    - 设置环境变量 `WORDPRESS_DB_PASSWORD_FILE` 为 secret 挂载的文件路径。WordPress 服务从该文件读取 MySQL 密码字符串并将其添加到 `wp-config.php` 配置文件中。
    - 使用用户名 `wordpress` 和 `/run/secrets/wp_db_password` 中的密码连接到 MySQL 容器，并在不存在时创建 `wordpress` 数据库。
    - 将其数据（如主题和插件）存储在名为 `wpdata` 的卷中，以便在服务重启时这些文件持久化。

    ```console
    $ docker service create \
         --name wordpress \
         --replicas 1 \
         --network mysql_private \
         --publish published=30000,target=80 \
         --mount type=volume,source=wpdata,destination=/var/www/html \
         --secret source=mysql_password,target=wp_db_password \
         -e WORDPRESS_DB_USER="wordpress" \
         -e WORDPRESS_DB_PASSWORD_FILE="/run/secrets/wp_db_password" \
         -e WORDPRESS_DB_HOST="mysql:3306" \
         -e WORDPRESS_DB_NAME="wordpress" \
         wordpress:latest
    ```

6.  使用 `docker service ls` 和 `docker service ps` 命令验证服务正在运行。

    ```console
    $ docker service ls

    ID            NAME       MODE        REPLICAS  IMAGE
    wvnh0siktqr3  mysql      replicated  1/1       mysql:latest
    nzt5xzae4n62  wordpress  replicated  1/1       wordpress:latest
    ```

    ```console
    $ docker service ps wordpress

    ID            NAME         IMAGE             NODE  DESIRED STATE  CURRENT STATE           ERROR  PORTS
    aukx6hgs9gwc  wordpress.1  wordpress:latest  moby  Running        Running 52 seconds ago   
    ```

    此时，你可以实际上撤销 WordPress 服务对 `mysql_password` secret 的访问权限，因为 WordPress 已将 secret 复制到其配置文件 `wp-config.php` 中。现在不要这样做，因为我们稍后使用它来促进轮换 MySQL 密码。

7.  从任何 swarm 节点访问 `http://localhost:30000/`，并使用基于 Web 的向导设置 WordPress。所有这些设置都存储在 MySQL `wordpress` 数据库中。WordPress 自动为你的 WordPress 用户生成密码，这与 WordPress 用于访问 MySQL 的密码完全不同。将此密码安全存储，例如在密码管理器中。你需要它在
    [轮换 secret](#example-rotate-a-secret) 后登录 WordPress。

    继续写几篇博客文章并安装 WordPress 插件或主题，以验证 WordPress 完全可操作并且其状态在服务重启时保存。

8.  如果你打算继续下一个示例，请不要清理任何服务或 secrets，下一个示例演示如何轮换 MySQL 密码。

### 示例：轮换 secret

此示例基于前面的示例。在此场景中，你创建一个具有新 MySQL 密码的新 secret，更新 `mysql` 和 `wordpress` 服务使用它，然后删除旧 secret。

> [!NOTE]
>
> 更改 MySQL 数据库的密码涉及运行额外的查询或命令，而不是仅仅更改单个环境变量或文件，因为镜像仅在数据库不存在时设置 MySQL 密码，而 MySQL 默认在 MySQL 数据库中存储密码。轮换密码或其他 secrets 可能涉及 Docker 之外的额外步骤。

1.  创建新密码并将其存储为名为 `mysql_password_v2` 的 secret。

    ```console
    $ openssl rand -base64 20 | docker secret create mysql_password_v2 -
    ```

2.  更新 MySQL 服务，使其同时访问旧 secret 和新 secret。请记住，你不能更新或重命名 secret，但可以撤销 secret 并使用新目标文件名授予访问权限。

    ```console
    $ docker service update \
         --secret-rm mysql_password mysql

    $ docker service update \
         --secret-add source=mysql_password,target=old_mysql_password \
         --secret-add source=mysql_password_v2,target=mysql_password \
         mysql
    ```

    更新服务会导致其重启，当 MySQL 服务第二次重启时，它可以在 `/run/secrets/old_mysql