---
title: 使用 Docker Configs 存储配置数据
description: 如何将配置数据与运行时分离
keywords: swarm, 配置, configs
---

## 关于 configs

Docker swarm 服务的 configs 允许你将非敏感信息（如配置文件）存储在服务镜像或运行中容器之外。这让你的镜像保持尽可能通用，无需将配置文件绑定挂载到容器中或使用环境变量。

Configs 的工作方式与 [secrets](secrets.md) 类似，但它们在磁盘上未加密，并直接挂载到容器的文件系统中，不使用 RAM 磁盘。Configs 可以随时添加或从服务中移除，服务之间可以共享一个 config。你甚至可以将 configs 与环境变量或标签结合使用，以获得最大的灵活性。Config 值可以是通用字符串或二进制内容（最大 500 KB）。

> [!NOTE]
>
> Docker configs 仅对 swarm 服务可用，不适用于独立容器。要使用此功能，请考虑将你的容器调整为以 1 的规模运行服务。

Configs 在 Linux 和 Windows 服务上均受支持。

### Windows 支持

Docker 包含对 Windows 容器上 configs 的支持，但实现上存在差异，以下示例中会指出这些差异。请记住以下显著差异：

- 带有自定义目标的配置文件不会直接绑定挂载到 Windows 容器中，因为 Windows 不支持非目录文件绑定挂载。相反，容器的所有 configs 都挂载在容器内的 `C:\ProgramData\Docker\internal\configs`（一个不应被应用程序依赖的实现细节）中。符号链接用于从那里指向容器内配置的目标位置，默认目标是 `C:\ProgramData\Docker\configs`。

- 创建使用 Windows 容器的服务时，不支持为 configs 指定 UID、GID 和 mode 选项。Configs 当前只能由容器内的管理员和具有 `system` 访问权限的用户访问。

- 在 Windows 上，使用 `--credential-spec` 以 `config://<config-name>` 格式创建或更新服务。这在容器启动前将 gMSA 凭据文件直接传递给节点。工作节点上不会写入任何 gMSA 凭据到磁盘。更多信息，请参考
  [将服务部署到 swarm](services.md#gmsa-for-swarm)。

## Docker 如何管理 configs

当你向 swarm 添加 config 时，Docker 通过相互 TLS 连接将 config 发送到 swarm 管理器。Config 存储在加密的 Raft 日志中。整个 Raft 日志在其他管理器之间复制，确保 configs 与其他 swarm 管理数据具有相同的高可用性保证。

当你授予新创建或正在运行的服务访问 config 的权限时，config 会作为文件挂载到容器中。挂载点在容器内的默认位置是 Linux 容器中的 `/<config-name>`。在 Windows 容器中，configs 都挂载到 `C:\ProgramData\Docker\configs` 中，并创建符号链接到容器内所需的位置，默认为 `C:\<config-name>`。

你可以使用数值 ID 或用户或组的名称设置配置的所有权（`uid` 和 `gid`）。你还可以指定文件权限（`mode`）。这些设置对 Windows 容器被忽略。

- 如果未设置，config 由运行容器命令的用户（通常是 `root`）及其默认组（也通常是 `root`）拥有。
- 如果未设置，config 具有全局可读权限（mode `0444`），除非容器内设置了 `umask`，在这种情况下，mode 受该 `umask` 值影响。

你可以随时更新服务以授予其对其他 configs 的访问权限或撤销其对给定 config 的访问权限。

节点只有在作为 swarm 管理器或运行被授予访问 config 权限的任务容器时，才能访问 configs。当容器任务停止运行时，共享给它的 configs 会从该容器的内存文件系统中卸载并从节点内存中清除。

如果节点在运行具有访问 config 权限的任务容器时失去与 swarm 的连接，任务容器仍然可以访问其 configs，但无法在节点重新连接到 swarm 之前接收更新。

你可以随时添加或检查单个 config，或列出所有 configs。你不能删除正在运行的服务使用的 config。有关在不中断运行服务的情况下删除 config 的方法，请参阅 [轮换 config](configs.md#example-rotate-a-config)。

为了更容易更新或回滚 configs，请考虑在 config 名称中添加版本号或日期。这得益于能够在给定容器内控制 config 的挂载点。

要更新堆栈，请修改 Compose 文件，然后重新运行 `docker stack deploy -c <new-compose-file> <stack-name>`。如果你在该文件中使用新 config，你的服务将开始使用它们。请记住，配置是不可变的，因此你不能更改现有服务的文件。

你可以运行 `docker stack rm` 来停止应用并拆除堆栈。这会删除由 `docker stack deploy` 使用相同堆栈名称创建的任何 config。这会删除 _所有_ configs，包括那些未被服务引用的和 `docker service update --config-rm` 后剩余的。

## 了解更多关于 `docker config` 命令的信息

使用这些链接阅读有关特定命令的详细信息，或继续阅读 [关于在服务中使用 configs 的示例](#advanced-example-use-configs-with-a-nginx-service)。

- [`docker config create`](/reference/cli/docker/config/create.md)
- [`docker config inspect`](/reference/cli/docker/config/inspect.md)
- [`docker config ls`](/reference/cli/docker/config/ls.md)
- [`docker config rm`](/reference/cli/docker/config/rm.md)

## 示例

本节包含渐进式示例，展示如何使用 Docker configs。

> [!NOTE]
>
> 这些示例使用单引擎 swarm 和未扩展的服务以简化说明。示例使用 Linux 容器，但 Windows 容器也支持 configs。

### 在 Compose 文件中定义和使用 configs

`docker stack` 命令支持在 Compose 文件中定义 configs。
但是，`docker compose` 不支持 `configs` 键。详情请见
[Compose 文件参考](/reference/compose-file/legacy-versions.md)。

### 简单示例：开始使用 configs

这个简单示例展示了 configs 如何在几个命令中工作。对于真实世界的示例，请继续阅读
[高级示例：将 configs 与 Nginx 服务一起使用](#advanced-example-use-configs-with-a-nginx-service)。

1.  向 Docker 添加一个 config。`docker config create` 命令读取标准输入，因为最后一个参数（表示要从中读取 config 的文件）设置为 `-`。

    ```console
    $ echo "这是一个配置" | docker config create my-config -
    ```

2.  创建一个 `redis` 服务并授予其访问 config 的权限。默认情况下，容器可以在 `/my-config` 访问 config，但你可以使用 `target` 选项自定义容器上的文件名。

    ```console
    $ docker service create --name redis --config my-config redis:alpine
    ```

3.  使用 `docker service ps` 验证任务是否正常运行而无问题。如果一切正常，输出看起来类似于：

    ```console
    $ docker service ps redis

    ID            NAME     IMAGE         NODE              DESIRED STATE  CURRENT STATE          ERROR  PORTS
    bkna6bpn8r1a  redis.1  redis:alpine  ip-172-31-46-109  Running        Running 8 seconds ago
    ```

4.  使用 `docker ps` 获取 `redis` 服务任务容器的 ID，以便你可以使用 `docker container exec` 连接到容器并读取配置数据文件的内容，该文件默认可被所有人读取，且名称与 config 名称相同。以下第一个命令说明了如何查找容器 ID，第二和第三个命令使用 shell 补全自动执行此操作。

    ```console
    $ docker ps --filter name=redis -q

    5cb1c2348a59

    $ docker container exec $(docker ps --filter name=redis -q) ls -l /my-config

    -r--r--r--    1 root     root            12 Jun  5 20:49 my-config

    $ docker container exec $(docker ps --filter name=redis -q) cat /my-config

    这是一个配置
    ```

5.  尝试删除 config。删除失败，因为 `redis` 服务正在运行且有权访问 config。

    ```console

    $ docker config ls

    ID                          NAME                CREATED             UPDATED
    fzwcfuqjkvo5foqu7ts7ls578   hello               31 minutes ago      31 minutes ago


    $ docker config rm my-config

    错误响应来自守护进程：rpc error: code = 3 desc = config 'my-config' is
    is
    in use by the following service: redis
    ```

6.  通过更新服务从正在运行的 `redis` 服务中移除对 config 的访问。

    ```console
    $ docker service update --config-rm my-config redis
    ```

7.  再次重复步骤 3 和 4，验证服务不再有权访问 config。容器 ID 不同，因为 `service update` 命令重新部署了服务。

    ```console
    $ docker container exec -it $(docker ps --filter name=redis -q) cat /my-config

    cat: can't open '/my-config': No such file or directory
    ```

8.  停止并移除服务，并从 Docker 中移除 config。

    ```console
    $ docker service rm redis

    $ docker config rm my-config
    ```

### 简单示例：在 Windows 服务中使用 configs

这是一个非常简单的示例，展示如何在 Docker for Windows 上运行 Windows 容器的 Microsoft IIS 服务中使用 configs。这是一个天真的示例，将网页存储在 config 中。

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

2.  如果尚未执行，请初始化或加入 swarm。

    ```powershell
    docker swarm init
    ```

3.  将 `index.html` 文件保存为名为 `homepage` 的 swarm config。

    ```powershell
    docker config create homepage index.html
    ```

4.  创建一个 IIS 服务并授予其访问 `homepage` config 的权限。

    ```powershell
    docker service create
        --name my-iis
        --publish published=8000,target=8000
        --config src=homepage,target="\inetpub\wwwroot\index.html"
        microsoft/iis:nanoserver
    ```

5.  访问 `http://localhost:8000/` 上的 IIS 服务。它应该提供第一步中的 HTML 内容。

6.  移除服务和 config。

    ```powershell
    docker service rm my-iis

    docker config rm homepage
    ```

### 示例：使用模板化 config

要创建内容将使用模板引擎生成的配置，请使用 `--template-driver` 参数并指定引擎名称作为其参数。容器创建时将渲染模板。

1.  将以下内容保存到新文件 `index.html.tmpl` 中。

    ```html
    <html lang="en">
      <head><title>Hello Docker</title></head>
      <body>
        <p>Hello {{ env "HELLO" }}! I'm service {{ .Service.Name }}.</p>
      </body>
    </html>
    ```

2.  将 `index.html.tmpl` 文件保存为名为 `homepage` 的 swarm config。提供参数 `--template-driver` 并指定 `golang` 作为模板引擎。

    ```console
    $ docker config create --template-driver golang homepage index.html.tmpl
    ```

3.  创建一个运行 Nginx 的服务，该服务有权访问环境变量 HELLO 和 config。

    ```console
    $ docker service create \
         --name hello-template \
         --env HELLO="Docker" \
         --config source=homepage,target=/usr/share/nginx/html/index.html \
         --publish published=3000,target=80 \
         nginx:alpine
    ```

4.  验证服务是否正常运行：你可以访问 Nginx 服务器，并且正在提供正确的内容。

    ```console
    $ curl http://0.0.0.0:3000

    <html lang="en">
      <head><title>Hello Docker</title></head>
      <body>
        <p>Hello Docker! I'm service hello-template.</p>
      </body>
    </html>
    ```

### 高级示例：将 configs 与 Nginx 服务一起使用

此示例分为两部分。
[第一部分](#generate-the-site-certificate) 全部关于生成站点证书，不直接涉及 Docker configs，但它设置了 [第二部分](#configure-the-nginx-container)，在第二部分中，你将站点证书作为一系列 secrets 存储，将 Nginx 配置作为 config 存储。示例展示了如何设置 config 的选项，如容器内的目标位置和文件权限（`mode`）。

#### 生成站点证书

为你的站点生成根 CA 和 TLS 证书及密钥。对于生产站点，你可能希望使用 `Let's Encrypt` 等服务生成 TLS 证书和密钥，但此示例使用命令行工具。此步骤有点复杂，但只是设置步骤，以便你有东西可以存储为 Docker secret。如果你想跳过这些子步骤，可以 [使用 Let's Encrypt](https://letsencrypt.org/getting-started/) 生成站点密钥和证书，将文件命名为 `site.key` 和 `site.crt`，然后跳到
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

3.  配置根 CA。编辑名为 `root-ca.cnf` 的新文件并粘贴以下内容。这限制根 CA 只能签署终端证书而不能签署中间 CA。

    ```ini
    [root_ca]
    basicConstraints = critical,CA:TRUE,pathlen:1
    keyUsage = critical, nonRepudiation, cRLSign, keyCertSign
    subjectKeyIdentifier=hash
    ```

4.  签署证书。

    ```console
    $ openssl x509 -req -days 3650 -in "root-ca.csr" \
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

7.  配置站点证书。编辑名为 `site.cnf` 的新文件并粘贴以下内容。这限制站点证书只能用于服务器身份验证，不能用于签署证书。

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
        -CA "root-ca.crt" -CAkey "root-ca.key" -CAcreateserial \
        -out "site.crt" -extfile "site.cnf" -extensions server
    ```

9.  `site.csr` 和 `site.cnf` 文件不需要 Nginx 服务，但如果你想生成新的站点证书，需要它们。保护 `root-ca.key` 文件。

#### 配置 Nginx 容器

1.  生成一个非常基本的 Nginx 配置，通过 HTTPS 提供静态文件。TLS 证书和密钥存储为 Docker secrets，以便可以轻松轮换。

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

2.  创建两个 secrets，代表密钥和证书。你可以将任何小于 500 KB 的文件存储为 secret。这允许你将密钥和证书与其使用的服务解耦。在这些示例中，secret 名称和文件名相同。

    ```console
    $ docker secret create site.key site.key

    $ docker secret create site.crt site.crt
    ```

3.  将 `site.conf` 文件保存在 Docker config 中。第一个参数是 config 的名称，第二个参数是要从中读取的文件。

    ```console
    $ docker config create site.conf site.conf
    ```

    列出 configs：

    ```console
    $ docker config ls

    ID                          NAME                CREATED             UPDATED
    4ory233120ccg7biwvy11gl5z   site.conf           4 seconds ago       4 seconds ago
    ```


4.  创建一个运行 Nginx 的服务，该服务有权访问两个 secrets 和 config。将 mode 设置为 `0440`，以便文件只能由其所有者及其组读取，不能被全局读取。

    ```console
    $ docker service create \
         --name nginx \
         --secret site.key \
         --secret site.crt \
         --config source=site.conf,target=/etc/nginx/conf.d/site.conf,mode=0440 \
         --publish published=3000,target=443 \
         nginx:latest \
         sh -c "exec nginx -g 'daemon off;'"
    ```

    在运行的容器内，现在存在以下三个文件：

    - `/run/secrets/site.key`
    - `/run/secrets/site.crt`
    - `/etc/nginx/conf.d/site.conf`

5.  验证 Nginx 服务是否正在运行。

    ```console
    $ docker service ls

    ID            NAME   MODE        REPLICAS  IMAGE
    zeskcec62q24  nginx  replicated  1/1       nginx:latest

    $ docker service ps nginx

    NAME                  IMAGE         NODE  DESIRED STATE  CURRENT STATE          ERROR  PORTS
    nginx.1.9ls3yo9ugcls  nginx:latest  moby  Running        Running 3 minutes ago
    ```

6.  验证服务是否正常运行：你可以访问 Nginx 服务器，并且正在使用正确的 TLS 证书。

    ```console
    $ curl --cacert root-ca.crt https://0.0.0.0:3000

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

    <p>For online documentation and support, refer to
    <a href="https://nginx.org">nginx.org</a>.<br/>
    Commercial support is available at
    <a href="https://www.nginx.com">www.nginx.com</a>.</p>

    <p><em>Thank you for using nginx.</em></p>
    </body>
    </html>
    ```

    ```console
    $ openssl s_client -connect 0.0.0.0:3000 -CAfile root-ca.crt

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

7.  除非你要继续下一个示例，否则通过移除 `nginx` 服务以及存储的 secrets 和 config 来清理示例。

    ```console
    $ docker service rm nginx

    $ docker secret rm site.crt site.key

    $ docker config rm site.conf
    ```

现在你已经配置了一个 Nginx 服务，其配置与其镜像分离。你可以运行多个具有完全相同镜像但不同配置的站点，而无需构建自定义镜像。

### 示例：轮换 config

要轮换 config，你首先保存一个与当前使用的名称不同的新 config。然后重新部署服务，在容器内同一挂载点移除旧 config 并添加新 config。此示例基于前面的示例，通过轮换 `site.conf` 配置文件。

1.  本地编辑 `site.conf` 文件。在 `index` 行添加 `index.php`，并保存文件。

    ```nginx
    server {
        listen                443 ssl;
        server_name           localhost;
        ssl_certificate       /run/secrets/site.crt;
        ssl_certificate_key   /run/secrets/site.key;

        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm index.php;
        }
    }
    ```

2.  使用新的 `site.conf` 创建名为 `site-v2.conf` 的新 Docker config。

    ```bah
    $ docker config create site-v2.conf site.conf
    ```

3.  更新 `nginx` 服务以使用新 config 而不是旧 config。

    ```console
    $ docker service update \
      --config-rm site.conf \
      --config-add source=site-v2.conf,target=/etc/nginx/conf.d/site.conf,mode=0440 \
      nginx
    ```

4.  使用 `docker service ps nginx` 验证 `nginx` 服务是否完全重新部署。当它完成时，你可以移除旧的 `site.conf` config。

    ```console
    $ docker config rm site.conf
    ```

5.  清理时，你可以移除 `nginx` 服务以及 secrets 和 configs。

    ```console
    $ docker service rm nginx

    $ docker secret rm site.crt site.key

    $ docker config rm site-v2.conf
    ```

现在你已经更新了 `nginx` 服务的配置，而无需重建其镜像。