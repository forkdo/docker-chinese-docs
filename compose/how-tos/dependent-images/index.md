# 构建依赖镜像





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="https://docs.docker.com/compose/releases/release-notes/#2220">2.22.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



为了减少推送/拉取时间以及镜像体积，Compose 应用程序的一个常见实践是让服务尽可能共享基础层。通常，你会为所有服务选择相同的操作系统基础镜像。但更进一步，当镜像共享相同的系统包时，还可以共享镜像层。接下来需要解决的挑战是避免在所有服务中重复编写完全相同的 Dockerfile 指令。

为了便于说明，本页假设你希望所有服务都基于 `alpine` 基础镜像构建，并安装系统包 `openssl`。

## 多阶段 Dockerfile

推荐的方法是将共享声明分组到单个 Dockerfile 中，并使用多阶段特性，以便服务镜像基于此共享声明进行构建。

Dockerfile：

```dockerfile
FROM alpine as base
RUN /bin/sh -c apk add --update --no-cache openssl

FROM base as service_a
# 构建服务 a
...

FROM base as service_b
# 构建服务 b
...
```

Compose 文件：

```yaml
services:
  a:
     build:
       target: service_a
  b:
     build:
       target: service_b
```

## 使用另一个服务的镜像作为基础镜像

一种常见的模式是在一个服务中复用另一个服务的镜像作为基础镜像。由于 Compose 不会解析 Dockerfile，因此它无法自动检测服务之间的这种依赖关系，从而无法正确排序构建执行。

a.Dockerfile：

```dockerfile
FROM alpine
RUN /bin/sh -c apk add --update --no-cache openssl
```

b.Dockerfile：

```dockerfile
FROM service_a
# 构建服务 b
```

Compose 文件：

```yaml
services:
  a:
     image: service_a 
     build:
       dockerfile: a.Dockerfile
  b:
     image: service_b
     build:
       dockerfile: b.Dockerfile
```

传统的 Docker Compose v1 会顺序构建镜像，这使得该模式可以开箱即用。Compose v2 使用 BuildKit 优化构建，并并行构建镜像，因此需要显式声明。

推荐的方法是将依赖的基础镜像声明为额外的构建上下文：

Compose 文件：

```yaml
services:
  a:
     image: service_a
     build: 
       dockerfile: a.Dockerfile
  b:
     image: service_b
     build:
       dockerfile: b.Dockerfile
       additional_contexts:
         # `FROM service_a` 将被解析为对服务 "a" 的依赖，该服务必须首先构建
         service_a: "service:a"
```

使用 `additional_contexts` 属性，你可以引用另一个服务构建的镜像，而无需显式命名：

b.Dockerfile：

```dockerfile

FROM base_image  
# `base_image` 不会解析为实际的镜像。这用于指向一个命名的附加上下文

# 构建服务 b
```

Compose 文件：

```yaml
services:
  a:
     build: 
       dockerfile: a.Dockerfile
       # 构建的镜像将被标记为 <project_name>_a
  b:
     build:
       dockerfile: b.Dockerfile
       additional_contexts:
         # `FROM base_image` 将被解析为对服务 "a" 的依赖，该服务必须首先构建
         base_image: "service:a"
```

## 使用 Bake 构建

使用 [Bake](/manuals/build/bake/_index.md) 可以传递所有服务的完整构建定义，并以最高效的方式编排构建执行。

要启用此功能，请在环境中设置 `COMPOSE_BAKE=true` 变量来运行 Compose。

```console
$ COMPOSE_BAKE=true docker compose build
[+] Building 0.0s (0/1)                                                         
 => [internal] load local bake definitions                                 0.0s
...
[+] Building 2/2 manifest list sha256:4bd2e88a262a02ddef525c381a5bdb08c83  0.0s
 ✔ service_b  Built                                                        0.7s 
 ✔ service_a  Built    
```

也可以通过编辑 `$HOME/.docker/config.json` 配置文件将 Bake 选为默认构建器：
```json
{
  ...
  "plugins": {
    "compose": {
      "build": "bake"
    }
  }
  ...
}
```

## 其他资源

- [Docker Compose 构建参考](/reference/cli/docker/compose/build.md)
- [了解多阶段 Dockerfile](/manuals/build/building/multi-stage.md)
