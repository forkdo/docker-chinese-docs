# 将 Docker Compose 应用程序打包为 OCI 工件进行部署





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="/compose/releases/release-notes/#2340">2.34.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



Docker Compose 支持使用 [OCI 工件](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md)，允许你通过容器注册表打包和分发你的 Compose 应用程序。这意味着你可以将 Compose 文件与容器镜像存储在一起，从而更轻松地对多容器应用程序进行版本控制、共享和部署。

## 将你的 Compose 应用程序发布为 OCI 工件

要将你的 Compose 应用程序作为 OCI 工件分发，你可以使用 `docker compose publish` 命令将其发布到 OCI 兼容的注册表。
这样其他人就可以直接从注册表部署你的应用程序。

发布功能支持 Compose 的大部分组合功能，如覆盖（overrides）、扩展（extends）或包含（include），[但存在一些限制](#limitations)。

### 一般步骤

1. 导航到你的 Compose 应用程序目录。  
   确保你位于包含 `compose.yml` 文件的目录中，或者使用 `-f` 标志指定你的 Compose 文件。

2. 在终端中，登录到你的 Docker 账户，以便通过 Docker Hub 进行身份验证。

   ```console
   $ docker login
   ```

3. 使用 `docker compose publish` 命令将你的应用程序推送到 OCI 工件：

   ```console
   $ docker compose publish username/my-compose-app:latest
   ```
   如果你有多个 Compose 文件，请运行：

   ```console
   $ docker compose -f compose-base.yml -f compose-production.yml publish username/my-compose-app:latest
   ```

### 高级发布选项

发布时，你可以传递其他选项：
- `--oci-version`：指定 OCI 版本（默认自动确定）。
- `--resolve-image-digests`：将镜像标签固定到摘要。
- `--with-env`：在发布的 OCI 工件中包含环境变量。

Compose 会检查配置中是否包含任何敏感数据，并显示你的环境变量以确认你是否要发布它们。

```text
...
you are about to publish sensitive data within your OCI artifact.
please double check that you are not leaking sensitive data
AWS Client ID
"services.serviceA.environment.AWS_ACCESS_KEY_ID": xxxxxxxxxx
AWS Secret Key
"services.serviceA.environment.AWS_SECRET_ACCESS_KEY": aws"xxxx/xxxx+xxxx+"
Github authentication
"GITHUB_TOKEN": ghp_xxxxxxxxxx
JSON Web Token
"": xxxxxxx.xxxxxxxx.xxxxxxxx
Private Key
"": -----BEGIN DSA PRIVATE KEY-----
xxxxx
-----END DSA PRIVATE KEY-----
Are you ok to publish these sensitive data? [y/N]:y

you are about to publish environment variables within your OCI artifact.
please double check that you are not leaking sensitive data
Service/Config  serviceA
FOO=bar
Service/Config  serviceB
FOO=bar
QUIX=
BAR=baz
Are you ok to publish these environment variables? [y/N]: 
```

如果你拒绝，发布过程将停止，不会向注册表发送任何内容。

## 限制

将 Compose 应用程序发布为 OCI 工件存在一些限制。你无法发布包含以下内容的 Compose 配置：
- 包含绑定挂载（bind mounts）的服务
- 仅包含 `build` 部分的服务
- 使用 `include` 属性包含本地文件。要成功发布，请确保任何包含的本地文件也已发布。然后你可以使用 `include` 来引用这些文件，因为支持远程 `include`。

## 启动 OCI 工件应用程序

要启动使用 OCI 工件的 Docker Compose 应用程序，你可以使用 `-f`（或 `--file`）标志，后跟 OCI 工件引用。这允许你指定存储在注册表中作为 OCI 工件的 Compose 文件。

`oci://` 前缀表示 Compose 文件应从 OCI 兼容的注册表中拉取，而不是从本地文件系统加载。

```console
$ docker compose -f oci://docker











.

.

.






.






.

.

.

.

.

.

.

.


.

.

.

.

.

.

.

.

.

.

.

.

.

。

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

。

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

   compose。    compose。 / compose   compose compose  compose compose compose compose compose。 compose compose � publish工应用程序```  compose compose 。 compose compose这些 Compose   compose
``    ` `  **
`



```console
$ docker compose -f oci://docker.io/username/my-compose-app:latest:latest up
```

要运行 Compose 应用程序，请使用 `docker compose up` 命指向你的 OCI 工件的 `-f` 标：

```console
$ docker compose -f oci://docker.io/username/my-compose-app:latest up
```

### 故障排除

当你从 OCI 工件运行应用程序时，Compose 可能会显示警告消息，要求你确认以下内容，以限制运行恶意应用程序的风险：

- 使用的插值变量及其值的列表
- 应用程序使用的所有环境变量的列表
- 如果你的 OCI 工件应用程序正在使用其他远程资源，例如通过 [`include`](/reference/compose-file/include/)。

```text 
$ REGISTRY=myregistry.com docker compose -f oci://docker.io/username/my-compose-app:latest up

Found the following variables in configuration:
VARIABLE     VALUE                SOURCE        REQUIRED    DEFAULT
REGISTRY     myregistry.com      command-line   yes         
TAG          v1.0                environment    no          latest
DOCKERFILE   Dockerfile          default        no          Dockerfile
API_KEY      <unset>             none           no          

Do you want to proceed with these variables? [Y/n]:y

Warning: This Compose project includes files from remote sources:
- oci://registry.example.com/stack:latest
Remote includes could potentially be malicious. Make sure you trust the source.
Do you want to continue? [y/N]: 
```

如果你同意启动应用程序，Compose 会显示所有资源从 OCI 工件下载到的目录：

```text
...
Do you want to continue? [y/N]: y

Your compose stack "oci://registry.example.com/stack:latest" is stored in "~/Library/Caches/docker-compose/964e715660d6f6c3b384e05e7338613795f7dcd3613890cfa57e3540353b9d6d"
```

`docker compose publish` 命令支持非交互式执行，你可以通过包含 `-y`（或 `--yes`）标志来跳过确认提示：

```console
$ docker compose publish -y username/my-compose-app:latest
```

## 下一步

- [了解 Docker Hub 中的 OCI 工件](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md)
- [Compose publish 命令](/reference/cli/docker/compose/publish.md)
- [了解 `include`](/reference/compose-file/include.md)
