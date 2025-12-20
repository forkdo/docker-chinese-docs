# 高级配置





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    
      
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Availability:</span>
        <span>
          Experimental
          
            
          
            
          
            
              <span class="icon-svg"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M172-120q-41.78 0-59.39-39T124-230l248-280v-270h-52q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h320q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-52v270l248 280q29 32 11.39 71T788-120H172Z"/></svg></span>
            
          
            
          
            
          
        </span>
      </div>
    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 
    
  
  <a class="link" href="https://docs.docker.com/desktop/release-notes/#4500">4.50</a> or later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



本指南介绍在本地运行的沙箱代理的高级配置。

## 管理沙箱

### 重新创建沙箱

由于Docker强制每个工作空间只能有一个沙箱，因此每次在给定目录中运行`docker sandbox run <agent>`时，都会重用同一个沙箱。要创建新的沙箱，您需要先删除现有的沙箱：

```console
$ docker sandbox ls  # 查找沙箱ID
$ docker sandbox rm <sandbox-id>
$ docker sandbox run <agent>  # 创建新沙箱
```

### 何时重新创建沙箱

沙箱会记住其初始配置，不会从后续的`docker sandbox run`命令中获取更改。您必须重新创建沙箱才能修改：

- 环境变量（`-e`标志）
- 卷挂载（`-v`标志）
- Docker套接字访问（`--mount-docker-socket`标志）
- 凭据模式（`--credentials`标志）

### 列出和检查沙箱

查看所有沙箱：

```console
$ docker sandbox ls
```

获取特定沙箱的详细配置信息：

```console
$ docker sandbox inspect <sandbox-id>
```

这将显示沙箱的配置，包括环境变量、卷和创建时间。

### 删除沙箱

删除特定沙箱：

```console
$ docker sandbox rm <sandbox-id>
```

一次性删除所有沙箱：

```console
$ docker sandbox rm $(docker sandbox ls -q)
```

这在完成项目或想要重新开始进行清理时非常有用。

## 授予代理Docker访问权限

挂载Docker套接字以授予代理在容器内访问Docker命令的权限。代理可以构建镜像、运行容器并使用Docker Compose设置。

> [!CAUTION]
> 挂载Docker套接字授予代理对Docker守护进程的完全访问权限，该守护进程在您的系统上具有root级权限。代理可以启动或停止任何容器、访问卷，并可能逃离沙箱。仅当您完全信任代理正在处理的代码时才使用此选项。

### 启用Docker套接字访问

使用`--mount-docker-socket`标志：

```console
$ docker sandbox run --mount-docker-socket claude
```

这将把主机的Docker套接字（`/var/run/docker.sock`）挂载到容器中，授予代理访问Docker命令的权限。

> [!IMPORTANT]
> 代理可以看到并与主机上的所有容器交互，而不仅仅是沙箱内创建的容器。

### 示例：测试容器化应用程序

如果您的项目有Dockerfile，代理可以构建并测试它：

```console
$ cd ~/my-docker-app
$ docker sandbox run --mount-docker-socket claude
```

示例对话：

```plaintext
您："构建Docker镜像并运行测试"

Claude: *运行*
  docker build -t myapp:test .
  docker run myapp:test npm test
```

### 代理使用Docker套接字访问可以做什么

启用Docker访问后，代理可以：

- 使用Docker Compose启动多容器应用程序
- 为多种架构构建镜像
- 管理主机上的现有容器
- 验证Dockerfile并测试构建过程

## 环境变量

使用`-e`标志传递环境变量以配置沙箱环境：

```console
$ docker sandbox run \
  -e NODE_ENV=development \
  -e DATABASE_URL=postgresql://localhost/myapp_dev \
  -e DEBUG=true \
  claude
```

这些变量可用于容器中的所有进程，包括代理及其运行的任何命令。使用多个`-e`标志设置多个变量。

### 示例：开发环境设置

设置完整的开发环境：

```console
$ docker sandbox run \
  -e NODE_ENV=development \
  -e DATABASE_URL=postgresql://localhost/myapp_dev \
  -e REDIS_URL=redis://localhost:6379 \
  -e LOG_LEVEL=debug \
  claude
```

示例对话：

```plaintext
您："运行数据库迁移并启动开发服务器"

Claude: *使用DATABASE_URL和其他环境变量*
  npm run migrate
  npm run dev
```

### 常见用例

测试API密钥：

```console
$ docker sandbox run \
  -e STRIPE_TEST_KEY=sk_test_xxx \
  -e SENDGRID_API_KEY=SG.xxx \
  claude
```

> [!CAUTION]
> 在沙箱中仅使用测试/开发API密钥，切勿使用生产密钥。

从.env文件加载：

沙箱不会自动从工作区加载`.env`文件，但您可以要求Claude使用它们：

```plaintext
您："从.env.development加载环境变量并启动服务器"
```

Claude可以使用`dotenv`工具或直接获取文件。

## 卷挂载

挂载其他目录或文件以共享主工作区之外的数据。使用`-v`标志和语法`host-path:container-path`：

```console
$ docker sandbox run -v ~/datasets:/data claude
```

这会使`~/datasets`在容器内的`/data`位置可用。代理可以读写此位置的文件。

只读挂载：

添加`:ro`以防止修改：

```console
$ docker sandbox run -v ~/configs/app.yml:/config/app.yml:ro claude
```

多个挂载：

使用多个`-v`标志挂载多个位置：

```console
$ docker sandbox run \
  -v ~/datasets:/data:ro \
  -v ~/models:/models \
  -v ~/.cache/pip:/root/.cache/pip \
  claude
```

### 示例：机器学习工作流

设置具有共享数据集、模型存储和持久缓存的ML环境：

```console
$ docker sandbox run \
  -v ~/datasets:/data:ro \
  -v ~/models:/models \
  -v ~/.cache/pip:/root/.cache/pip \
  claude
```

这提供了对数据集的只读访问（防止意外修改）、对保存训练模型的读写访问，以及持久pip缓存，以便在会话之间更快地安装包。

示例对话：

```plaintext
您："在MNIST数据集上训练模型并将其保存到/models"

Claude: *运行*
  python train.py --data /data/mnist --output /models/mnist_model.h5
```

### 常见用例

共享配置文件：

```console
$ docker sandbox run -v ~/.aws:/root/.aws:ro claude
```

构建缓存：

```console
$ docker sandbox run \
  -v ~/.cache/go-build:/root/.cache/go-build \
  -v ~/go/pkg/mod:/go/pkg/mod \
  claude
```

自定义工具：

```console
$ docker sandbox run -v ~/bin:/shared-bin:ro claude
```

## 自定义模板

创建自定义沙箱模板以重用配置环境。与其每次启动代理时都安装工具，不如构建一个包含所有预安装内容的Docker镜像：

```dockerfile
# syntax=docker/dockerfile:1
FROM docker/sandbox-templates:claude-code
RUN <<EOF
curl -LsSf https://astral.sh/uv/install.sh | sh
. ~/.local/bin/env
uv tool install ruff@latest
EOF
ENV PATH="$PATH:~/.local/bin"
```

构建镜像，并使用[`docker sandbox run --template`](/reference/cli/docker/sandbox/run#template)标志启动基于该镜像的新沙箱。

```console
$ docker build -t my-dev-env .
$ docker sandbox run --template my-dev-env claude
```

### 使用标准镜像

您可以使用标准Docker镜像作为沙箱模板，但它们不包含Docker沙箱模板提供的代理二进制文件、shell配置或运行时依赖项。直接使用标准Python镜像会失败：

```console
$ docker sandbox run --template python:3-slim claude
The claude binary was not found in the sandbox; please check this is the correct sandbox for this agent.
```

要使用标准镜像，请创建一个Dockerfile，在基础镜像之上安装代理二进制文件、依赖项和shell配置。当您需要的特定基础镜像（例如，确切的OS版本或具有特定构建工具的专业镜像）时，这种方法很有意义。
