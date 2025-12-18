---
title: 使用 Docker secrets 管理敏感数据
description: 如何安全地存储、检索和使用 Docker 服务的敏感数据
keywords: swarm, secrets, credentials, sensitive strings, sensitive data, security, encryption, encryption at rest
tags: [Secrets]
---

## 关于 secrets

从 Docker Swarm 服务的角度来看，_secret_ 是一段数据块，例如密码、SSH 私钥、SSL 证书，或其他不应通过网络传输或以明文形式存储在 Dockerfile 或应用源代码中的数据。你可以使用 Docker _secrets_ 来集中管理这些数据，并仅将它们安全地传输给需要访问的服务容器。Secrets 在 Docker swarm 中传输和存储时都是加密的。特定的 secret 只能被明确授权访问它的服务访问，并且仅在这些服务任务运行时生效。

你可以使用 secrets 来管理容器在运行时需要但又不希望存储在镜像或源代码控制中的任何敏感数据，例如：

- 用户名和密码
- TLS 证书和密钥
- SSH 密钥
- 其他重要数据，如数据库或内部服务器的名称
- 通用字符串或二进制内容（最大 500 KB）

> [!NOTE]
>
> Docker secrets 仅对 swarm 服务可用，不适用于独立容器。
> 要使用此功能，请考虑将你的容器调整为作为服务运行。有状态容器通常可以以 1 的规模运行，而无需更改容器代码。

使用 secrets 的另一个用例是，在容器和一组凭据之间提供一层抽象。考虑一个场景，你的应用有独立的开发、测试和生产环境。每个环境可以有不同的凭据，存储在开发、测试和生产 swarm 中，使用相同的 secret 名称。你的容器只需要知道 secret 的名称，就能在所有三个环境中运行。

你也可以使用 secrets 来管理非敏感数据，如配置文件。但是，Docker 支持使用 [configs](configs.md) 来存储非敏感数据。Configs 直接挂载到容器的文件系统中，不使用 RAM 磁盘。

### Windows 支持

Docker 在 Windows 容器中支持 secrets。在实现上有差异的地方，下面的例子中会特别说明。请记住以下显著差异：

- Microsoft Windows 没有内置的 RAM 磁盘管理驱动，因此在运行的 Windows 容器中，secrets 以明文形式持久化到容器的根磁盘上。但是，当容器停止时，secrets 会被显式删除。此外，Windows 不支持使用 `docker commit` 或类似命令将运行的容器持久化为镜像。

- 在 Windows 上，建议在主机机器的 Docker 根目录所在卷上启用
  [BitLocker](https://technet.microsoft.com/en-us/library/cc732774(v=ws.11).aspx)，以确保运行容器的 secrets 在静态时是加密的。

- 带有自定义目标的 secret 文件不会直接绑定挂载到 Windows 容器中，因为 Windows 不支持非目录文件的绑定挂载。相反，容器的所有 secrets 都挂载在容器内的
  `C:\ProgramData\Docker\internal\secrets`（一个实现细节，应用不应依赖于此）中。然后使用符号链接从那里指向容器内 secret 的期望目标。默认目标是 `C:\ProgramData\Docker\secrets`。

- 创建使用 Windows 容器的服务时，secrets 不支持指定 UID、GID 和 mode 选项。Secrets 目前只能被容器内的管理员和具有 `system` 访问权限的用户访问。

## Docker 如何管理 secrets

当你向 swarm 添加 secret 时，Docker 通过相互 TLS 连接将 secret 发送到 swarm 管理器。Secret 存储在加密的 Raft 日志中。整个 Raft 日志在其他管理器之间复制，确保 secrets 与其他 swarm 管理数据具有相同的高可用性保证。

当你授予新创建或正在运行的服务访问 secret 的权限时，解密的 secret 会挂载到容器的内存文件系统中。容器内挂载点的位置默认为 Linux 容器中的 `/run/secrets/<secret_name>`，或 Windows 容器中的 `C:\ProgramData\Docker\secrets`。你也可以指定自定义位置。

你可以随时更新服务，授予其访问额外 secrets 的权限，或撤销其对特定 secret 的访问权限。

节点只有在是 swarm 管理器或运行已授予访问 secret 权限的服务任务时，才能访问（加密的）secrets。当容器任务停止运行时，共享给它的解密 secrets 会从该容器的内存文件系统中卸载并从节点内存中清除。

如果节点在运行有访问 secret 权限的任务容器时失去与 swarm 的连接，任务容器仍然可以访问其 secrets，但无法接收更新，直到节点重新连接到 swarm。

你可以随时添加或检查单个 secret，或列出所有 secrets。你不能删除正在被运行服务使用的 secret。有关在不中断运行服务的情况下删除 secret 的方法，请参阅 [轮换 secret](secrets.md#example-rotate-a-secret)。

为了更容易更新或回滚 secrets，请考虑在 secret 名称中添加版本号或日期。这通过能够在给定容器内控制 secret 的挂载点而变得更容易。

## 了解更多关于 `docker secret` 命令

使用这些链接了解特定命令，或继续阅读
[使用服务的 secrets 简单示例](secrets.md#simple-example-get-started-with-secrets)。

- [`docker secret create`](/reference/cli/docker/secret/create.md)
- [`docker secret inspect`](/reference/cli/docker/secret/inspect.md)
- [`docker secret ls`](/reference/cli/docker/secret/ls.md)
- [`docker secret rm`](/reference/cli/docker/secret/rm.md)
- [`--secret`](/reference/cli/docker/service/create.md#secret) 标志用于 `docker service create`
- [`--secret-add` 和 `--secret-rm`](/reference/cli/docker/service/update.md#secret-add) 标志用于 `docker service update`

## 示例

本节包含三个渐进的示例，说明如何使用 Docker secrets。这些示例中使用的镜像已更新，以便更容易使用 Docker secrets。要了解如何以类似方式修改你自己的镜像，请参阅
[在你的镜像中构建 Docker Secrets 支持](#build-support-for-docker-secrets-into-your-images)。

> [!NOTE]
>
> 这些示例使用单引擎 swarm 和未扩展的服务以简化说明。
> 示例使用 Linux 容器，但 Windows 容器也支持 secrets。请参阅 [Windows 支持](#windows-support)。

### 在 compose 文件中定义和使用 secrets

`docker-compose` 和 `docker stack` 命令都支持在 compose 文件中定义 secrets。详细信息请参阅
[Compose 文件参考](/reference/compose-file/legacy-versions.md)。

### 简单示例：开始使用 secrets

这个简单示例展示了 secrets 在几个命令中如何工作。要了解真实世界的示例，请继续阅读
[中级示例：将 secrets 与 Nginx 服务一起使用](#intermediate-example-use-secrets-with-a-nginx-service)。

1.  向 Docker 添加一个 secret。`docker secret create` 命令读取标准输入，因为最后一个参数（表示要从哪个文件读取 secret）被设置为 `-`。

    ```console
    $ printf "This is a secret" | docker secret create my_secret_data -
    ```

2.  创建一个 `redis` 服务并授予它访问 secret 的权限。默认情况下，容器可以在 `/run/secrets/<secret_name>` 访问 secret，但你可以使用 `target` 选项自定义容器中的文件名。

    ```console
    $ docker service  create --name redis --secret my_secret_data redis:alpine
    ```

3.  使用 `docker service ps` 验证任务是否正常运行。如果一切正常，输出看起来像这样：

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

4.  使用 `docker ps` 获取 `redis` 服务任务容器的 ID，以便你可以使用 `docker container exec` 连接到容器并读取 secret 数据文件的内容，该文件默认可被所有人读取，且名称与 secret 名称相同。下面的第一个命令说明了如何找到容器 ID，第二个和第三个命令使用 shell 补全自动执行此操作。

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

6.  尝试删除 secret。删除失败，因为 `redis` 服务正在运行并且有访问该 secret 的权限。

    ```console
    $ docker secret ls

    ID                          NAME                CREATED             UPDATED
    wwwrxza8sxy025bas86593fqs   my_secret_data      4 hours ago         4 hours ago


    $ docker secret rm my_secret_data

    Error response from daemon: rpc error: code = 3 desc = secret
    'my_secret_data' is in use by the following service: redis
    ```

7.  通过更新服务，从正在运行的 `redis` 服务中移除对 secret 的访问。

    ```console
    $ docker service update --secret-rm my_secret_data redis
    ```

8.  重复步骤 3 和 4，验证服务不再有访问 secret 的权限。容器 ID 不同，因为 `service update` 命令重新部署了服务。

    ```console
    $ docker container exec -it $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data

    cat: can't open '/run/secrets/my_secret_data': No such file or directory
    ```

9.  停止并移除服务，并从 Docker 中移除 secret。

    ```console
    $ docker service rm redis

    $ docker secret rm my_secret_data
    ```

### 简单示例：在 Windows 服务中使用 secrets

这是一个非常简单的示例，展示如何在 Docker for Windows 上运行的 Microsoft Windows 10 的 Windows 容器中使用 Microsoft IIS 服务的 secrets。这是一个天真的示例，将网页存储在 secret 中。

此示例假设你已安装 PowerShell。

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

3.  将 `index.html` 文件保存为名为 `homepage` 的 swarm secret。

    ```console
    > docker secret create homepage index.html
    ```

4.  创建一个 IIS 服务并授予它访问 `homepage` secret 的权限。

    ```console
    > docker service create `
        --name my-iis `
        --publish published=8000,target=8000 `
        --secret src=homepage,target="\inetpub\wwwroot\index.html" `
        microsoft/iis:nanoserver
    ```

    > [!NOTE]
    >
    > 从技术上讲，没有理由对这个示例使用 secrets；
    > [configs](configs.md) 更适合。这个示例仅用于说明。

5.  访问 `http://localhost:8000/` 上的 IIS 服务。它应该提供来自第一步的 HTML 内容。

6.  移除服务和 secret。

    ```console
    > docker service rm my-iis
    > docker secret rm homepage
    > docker image remove secret-test
    ```

### 中级示例：将 secrets 与 Nginx 服务一起使用

此示例分为两部分。
[第一部分](#generate-the-site-certificate) 全部关于生成站点证书，不直接涉及 Docker secrets，但它为 [第二部分](#configure-the-nginx-container) 做准备，在第二部分中，你将站点证书和 Nginx 配置作为 secrets 存储和使用。

#### 生成站点证书

为你的站点生成根 CA 和 TLS 证书及密钥。对于生产站点，你可能希望使用 `Let’s Encrypt` 等服务来生成 TLS 证书和密钥，但此示例使用命令行工具。这一步有点复杂，但只是一个设置步骤，以便你有一些可以存储为 Docker secret 的内容。如果你不想执行这些子步骤，可以 [使用 Let's Encrypt](https://letsencrypt.org/getting-started/) 生成站点密钥和证书，将文件命名为 `site.key` 和 `site.crt`，然后跳到
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

3.  配置根 CA。编辑一个名为 `root-ca.cnf` 的新文件并粘贴以下内容到其中。这限制了根 CA 只能签署叶证书，不能签署中间 CA。

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

7.  配置站点证书。编辑一个名为 `site.cnf` 的新文件并粘贴以下内容到其中。这限制了站点证书只能用于服务器身份验证，不能用于签署证书。

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

9.  `site.csr` 和 `site.cnf` 文件不需要 Nginx 服务，但如果你要生成新站点证书，就需要它们。保护 `root-ca.key` 文件。

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

2.  创建三个 secrets，代表密