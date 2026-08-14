# 使用 Docker 加固镜像


你可以像使用 Docker Hub 上的任何其他镜像一样使用 Docker 加固镜像（DHI）。DHI 遵循相同的熟悉使用模式：使用 `docker pull` 拉取镜像，在 Dockerfile 中引用它们，并使用 `docker run` 运行容器。

关键区别在于，DHI 专注于安全性，并且有意保持最小化以减少攻击面。这意味着某些变体默认不包含 shell 或包管理器，并且可能以非 root 用户身份运行。

> [!IMPORTANT]
>
> 你必须向 Docker 加固镜像注册表 (`dhi.io`) 进行身份验证才能拉取 DHI Community 镜像。你可以使用以下任一方式进行身份验证：
>
> - **Docker ID 和密码：** 使用你的 Docker Hub 用户名和密码。如果你没有 Docker 账户，请[免费创建一个](../../accounts/create-account.md)。
> - **访问令牌：** 对个人账户使用[个人访问令牌 (PAT)](../../security/access-tokens.md)，或对组织使用以你的组织名称为用户名的[组织访问令牌 (OAT)](../../enterprise/security/access-tokens.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

## 采用 DHI 时的注意事项

Docker 加固镜像有意保持最小化以提高安全性。如果你正在更新现有的 Dockerfile 或框架以使用 DHI，请记住运行时镜像不包含 shell 或包管理器，默认以非 root 用户身份运行，并且可能具有与你熟悉的镜像不同的配置。

有关迁移注意事项的完整清单和详细指南，请参阅[迁移到 Docker 安全加固镜像](../migration/_index.md)。

## 拉取、运行和引用 DHI

Docker 安全加固镜像根据你的订阅使用不同的镜像引用：

| 订阅 | 镜像引用 | 身份验证 |
|---------------------|----------------------------|-----------------------|
| Community | `dhi.io/<image>:<tag>` | `docker login dhi.io` |
| Select 和 Enterprise | `<your-org>/<image>:<tag>` | `docker login` |

Select 和 Enterprise 用户应该将仓库[镜像](./mirror.md)到其 Docker Hub 组织，以访问合规变体和自定义功能。

身份验证后，在标准 Docker 命令和 Dockerfile 中使用镜像引用。例如：

```console
$ docker pull dhi.io/python:3.13
$ docker run --rm dhi.io/python:3.13 python -c "print('Hello from DHI')"
```

```dockerfile
FROM dhi.io/python:3.13
COPY . /app
CMD ["python", "/app/main.py"]
```

对于多阶段构建：
- 对于需要 shell 或包管理器的构建阶段，使用 `-dev` 标签。请参阅[为基于框架的应用程序使用 dev 变体](#use-dev-variants-for-framework-based-applications)。
- 对于具有最小化运行时依赖的已编译可执行文件，使用 `static` 镜像。请参阅[为编译后的可执行文件使用静态镜像](#use-a-static-image-for-compiled-executables)。

要了解如何搜索可用的变体，请参阅[搜索和评估镜像](./search-evaluate.md)。

## 在 CI/CD 流水线中使用 DHI

Docker 安全加固镜像在你的 CI/CD 流水线中的使用方式与其他任何镜像相同。你可以在 Dockerfile 中引用它们，在流水线步骤中拉取它们，或在构建和测试期间基于它们运行容器。

与典型的容器镜像不同，DHI 还包含已签名的[证明](../explore/security-concepts/attestations.md)，例如 SBOM 和来源元数据。如果你的工具支持，你可以将这些证明集成到流水线中，以支持供应链安全、策略检查或审计要求。

为了加强你的软件供应链，请考虑在使用 DHI 构建镜像时添加你自己的证明。这使你能够记录镜像的构建方式、验证其完整性，并使用 Docker Scout 等工具实现下游验证和策略执行。

要了解如何在构建过程中附加证明，请参阅 [Docker Build 证明](/manuals/build/metadata/attestations.md)。

### 使用 ORAS 发现证明

你可以使用 [ORAS](https://oras.land/) 来发现和检查附加到 Docker 安全加固镜像的证明。这在 CI/CD 流水线中对于供应链安全验证和合规性检查特别有用。

对于自动化工作流，请使用[组织访问令牌 (OAT)](../../enterprise/security/access-tokens.md) 进行身份验证。OAT 归组织所有，而非个人用户，因此更适合 CI/CD 流水线。

要使用 ORAS 发现证明：

1. 生成一个具有**读取公共仓库**范围的[组织访问令牌](../../enterprise/security/access-tokens.md)。

   以下示例展示了如何在 `dhi.io` 上的 DHI 社区镜像上发现证明。如果你要在镜像到你组织的镜像上发现证明，请生成一个用于从镜像仓库读取的 OAT，而不是**读取公共仓库**。

2. 使用你的组织名称作为用户名、OAT 作为密码登录 `dhi.io`。

   > [!WARNING]
   >
   > 以下示例为了演示目的在命令行上直接导出凭据。这会在你的 shell 历史记录和进程列表中暴露敏感令牌。在生产环境中，请使用安全的方法，例如从受限权限的文件中读取、在运行时加载的环境文件，或密钥管理工具。

    ```console
    $ oras login dhi.io -u <YOUR_ORGANIZATION_NAME>
    ```

   或者在 CI/CD 流水线中以非交互方式设置你的组织名称和令牌：

   ```console
   $ export DOCKER_ORG="YOUR_ORGANIZATION_NAME"
   $ export OAT="YOUR_ORGANIZATION_ACCESS_TOKEN"
   $ echo $OAT | oras login dhi.io -u "$DOCKER_ORG" --password-stdin
   ```

3. 在 DHI 镜像上发现证明：

   ```console
   $ oras discover dhi.io/node:24-dev --platform linux/amd64
   ```

   > [!NOTE]
   >
   > `--platform` 标志是必需的。如果没有它，`oras discover` 会解析到多架构镜像索引，该索引仅返回索引级别的签名，而不是完整的每个平台证明集。

   成功的响应会列出附加到镜像的证明，包括 SBOM、来源、漏洞报告和变更日志元数据。

## 为编译后的可执行文件使用静态镜像

Docker 安全加固镜像包含一个专门设计用于在极其最小化和安全的运行时中运行编译后可执行文件的 `static` 镜像仓库。与未加固的 `FROM scratch` 镜像不同，DHI `static` 镜像包含证明以及 `ca-certificates` 等基本包。

使用 `-dev` 或其他构建器镜像来编译你的二进制文件，然后将输出复制到 `static` 镜像中：

```dockerfile
FROM dhi.io/golang:1.22-dev AS build
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o myapp

FROM dhi.io/static:20230311
COPY --from=build /app/myapp /myapp
ENTRYPOINT ["/myapp"]
```

有关更多多阶段构建模式，请参阅 [Go 迁移示例](../migration/examples/go.md)。

## 为基于框架的应用程序使用 dev 变体

如果你正在使用需要包管理器或构建工具（如 Python、Node.js 或 Go）的框架构建应用程序，请在开发或构建阶段使用 `-dev` 变体。这些变体包含 shell、编译器和包管理器等必要工具，以支持本地迭代和 CI 工作流。

在内部开发循环或隔离的 CI 阶段使用 `-dev` 镜像，以最大限度地提高生产力。当您准备好为生产环境生成制品时，请切换到更小的运行时变体，以减少攻击面和镜像大小。

有关使用 dev 变体的详细多阶段 Dockerfile 示例，请参阅迁移示例：
- [Go](../migration/examples/go.md)
- [Python](../migration/examples/python.md)
- [Node.js](../migration/examples/node.md)

## 使用 Socket Firewall 变体监控包安装

如果你希望在依赖项安装期间获得供应链保护，请在构建阶段使用 Socket Firewall 变体替代标准的 `-dev` 变体。这些变体预装了 [Socket](https://socket.dev/)，用于监控包管理器活动并在恶意包进入镜像之前将其阻止。

提供两个级别。对 Socket Firewall Free 使用 `-sfw-dev`，或对 Socket Firewall Enterprise 使用 `-sfw-ent-dev`（需要来自 Socket 的 API 密钥）。无论你使用哪个构建阶段变体，运行时阶段保持不变。

```dockerfile
FROM dhi.io/python:3.13-alpine3.23-sfw-dev AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM dhi.io/python:3.13-alpine3.23
COPY --from=build /app /app
CMD ["python", "app.py"]
```

有关 Socket Firewall 变体的更多信息，请参阅[可用镜像类型](../explore/available.md)。

## 使用合规和 ELS 变体



拥有 DHI Select 或 DHI Enterprise 订阅后，你可以访问额外的镜像变体：

- 合规变体：用于监管要求的启用 FIPS 和符合 STIG 准备的镜像
- ELS（扩展生命周期支持）变体（需要附加组件）：针对已停止维护的镜像版本的安全补丁

要访问这些变体，请将仓库[镜像](./mirror.md)到你的 Docker Hub 组织。对于 ELS，请在设置镜像时启用 **Mirror end-of-life images**。镜像完成后，像使用任何其他镜像标签一样使用合规或 EOL 标签。

## 与 Kubernetes 配合使用

将 Docker 安全加固镜像部署到 Kubernetes 时，过程与使用任何其他容器镜像类似，但有一个关键区别：你必须配置镜像拉取密钥以向 DHI 注册表进行身份验证。无论你是直接从 `dhi.io` 拉取、从 Docker Hub 上的镜像拉取，还是从你自己的第三方注册表拉取，都是如此。

### 创建镜像拉取密钥

你可以使用访问令牌或 Docker Desktop 凭据创建镜像拉取密钥。

对于 `--docker-server` 值：
- 对于直接从 Docker 安全加固镜像拉取的社区镜像，使用 `dhi.io`
- 对于 Docker Hub 上的镜像仓库，使用 `docker.io`
- 对于第三方注册表，使用你的注册表主机名

#### 使用访问令牌

使用[个人访问令牌 (PAT)](../../security/access-tokens.md) 或[组织访问令牌 (OAT)](../../enterprise/security/access-tokens.md) 创建密钥。确保令牌至少对仓库具有只读访问权限。

```console
$ kubectl create -n <kubernetes namespace> secret docker-registry <secret name> --docker-server=<registry server> \
        --docker-username=<registry user> --docker-password=<access token> \
        --docker-email=<registry email>
```

#### 使用 Docker Desktop 凭据

如果你已经使用 Docker Desktop 进行了身份验证，则可以使用存储的凭据创建密钥。此方法适用于你已通过 Docker Desktop（使用 `docker login <registry>`）进行身份验证的注册表。

```console
$ NS=<namespace>
$ kubectl create -n ${NS} secret docker-registry dhi-pull-secret \
    --docker-server=<registry server> \
    --docker-username=<registry user> \
    --docker-password="$(echo https://<registry server> | docker-credential-desktop get | jq -r .Secret)" \
    --docker-email=<registry email>
```

此方法从 Docker Desktop 的凭据存储中提取凭据，无需为本地开发创建单独的访问令牌。

### 测试镜像拉取密钥

创建密钥后，通过部署一个在其 `imagePullSecrets` 配置中引用该密钥的测试 Pod 来验证它是否有效。

创建测试 Pod：

```console
kubectl apply --wait -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: dhi-test
  namespace: <kubernetes namespace>
spec:
  containers:
  - name: test
    image: bash:5
    command: [ "sh", "-c", "echo 'Hello from DHI in Kubernetes!'" ]
  imagePullSecrets:
  - name: <secret name>
EOF
```

检查 Pod 状态以确保其成功完成：

```console
$ kubectl get -n <kubernetes namespace> pods/dhi-test
```

成功的测试显示 `Completed` 状态：

```console
NAME       READY   STATUS      RESTARTS     AGE
dhi-test   0/1     Completed   ...          ...
```

如果你看到的是 `ErrImagePull` 状态，则你的密钥配置有问题：

```console
NAME       READY   STATUS         RESTARTS   AGE
dhi-test   0/1     ErrImagePull   0          ...
```

验证 Pod 输出是否与预期消息匹配：

```console
$ kubectl logs -n <kubernetes namespace> pods/dhi-test
Hello from DHI in Kubernetes!
```

清理测试 Pod：

```console
$ kubectl delete -n <kubernetes namespace> pods/dhi-test
```

