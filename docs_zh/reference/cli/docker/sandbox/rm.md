---
datafolder: sandbox-cli
datafile: docker_sandbox_rm
title: docker sandbox rm
layout: cli
---

# docker sandbox rm

从 Docker 沙箱中移除一个或多个资源

## 概要

从 Docker 沙箱中移除一个或多个资源

```
docker sandbox rm [OPTIONS] SANDBOX
```

## 描述

`docker sandbox rm` 命令允许您从 Docker 沙箱中移除资源。这包括容器、网络、卷和镜像。

## 选项

| 选项 | 描述 |
|------|------|
| `--all, -a` | 移除所有资源 |
| `--containers` | 移除所有容器 |
| `--networks` | 移除所有网络 |
| `--volumes` | 移除所有卷 |
| `--images` | 移除所有镜像 |
| `--force, -f` | 强制移除，不提示确认 |
| `--help, -h` | 打印使用信息 |

## 示例

### 移除特定沙箱中的所有容器

```
$ docker sandbox rm --containers my-sandbox
```

### 移除特定沙箱中的所有资源

```
$ docker sandbox rm --all my-sandbox
```

### 强制移除特定沙箱中的所有网络

```
$ docker sandbox rm --networks --force my-sandbox
```

## 相关命令

* [docker sandbox create](docker_sandbox_create.md) - 创建一个新的 Docker 沙箱
* [docker sandbox ls](docker_sandbox_ls.md) - 列出 Docker 沙箱
* [docker sandbox run](docker_sandbox_run.md) - 在 Docker 沙箱中运行命令
* [docker sandbox exec](docker_sandbox_exec.md) - 在 Docker 沙箱中执行命令
* [docker sandbox logs](docker_sandbox_logs.md) - 获取 Docker 沙箱的日志
* [docker sandbox inspect](docker_sandbox_inspect.md) - 显示 Docker 沙箱的详细信息
* [docker sandbox export](docker_sandbox_export.md) - 导出 Docker 沙箱
* [docker sandbox import](docker_sandbox_import.md) - 导入 Docker 沙箱
* [docker sandbox prune](docker_sandbox_prune.md) - 清理未使用的 Docker 沙箱资源
* [docker sandbox update](docker_sandbox_update.md) - 更新 Docker 沙箱配置
* [docker sandbox attach](docker_sandbox_attach.md) - 附加到 Docker 沙箱
* [docker sandbox detach](docker_sandbox_detach.md) - 从 Docker 沙箱分离
* [docker sandbox pause](docker_sandbox_pause.md) - 暂停 Docker 沙箱
* [docker sandbox resume](docker_sandbox_resume.md) - 恢复 Docker 沙箱
* [docker sandbox stop](docker_sandbox_stop.md) - 停止 Docker 沙箱
* [docker sandbox start](docker_sandbox_start.md) - 启动 Docker 沙箱
* [docker sandbox restart](docker_sandbox_restart.md) - 重启 Docker 沙箱
* [docker sandbox kill](docker_sandbox_kill.md) - 杀死 Docker 沙箱中的进程
* [docker sandbox wait](docker_sandbox_wait.md) - 等待 Docker 沙箱状态改变
* [docker sandbox port](docker_sandbox_port.md) - 显示 Docker 沙箱的端口映射
* [docker sandbox top](docker_sandbox_top.md) - 显示 Docker 沙箱中运行的进程
* [docker sandbox stats](docker_sandbox_stats.md) - 显示 Docker 沙箱的资源使用统计
* [docker sandbox history](docker_sandbox_history.md) - 显示 Docker 沙箱的历史记录
* [docker sandbox diff](docker_sandbox_diff.md) - 显示 Docker 沙箱文件系统的差异
* [docker sandbox commit](docker_sandbox_commit.md) - 从 Docker 沙箱创建新镜像
* [docker sandbox cp](docker_sandbox_cp.md) - 在 Docker 沙箱和本地文件系统之间复制文件
* [docker sandbox build](docker_sandbox_build.md) - 使用 Dockerfile 构建 Docker 沙箱
* [docker sandbox push](docker_sandbox_push.md) - 推送 Docker 沙箱到注册表
* [docker sandbox pull](docker_sandbox_pull.md) - 从注册表拉取 Docker 沙箱
* [docker sandbox tag](docker_sandbox_tag.md) - 为 Docker 沙箱添加标签
* [docker sandbox save](docker_sandbox_save.md) - 将 Docker 沙箱保存到 tar 文件
* [docker sandbox load](docker_sandbox_load.md) - 从 tar 文件加载 Docker 沙箱
* [docker sandbox login](docker_sandbox_login.md) - 登录到 Docker 注册表
* [docker sandbox logout](docker_sandbox_logout.md) - 从 Docker 注册表登出
* [docker sandbox search](docker_sandbox_search.md) - 在 Docker 注册表中搜索 Docker 沙箱
* [docker sandbox events](docker_sandbox_events.md) - 获取 Docker 沙箱的实时事件流
* [docker sandbox info](docker_sandbox_info.md) - 显示 Docker 沙箱的系统范围信息
* [docker sandbox version](docker_sandbox_version.md) - 显示 Docker 沙箱版本信息
* [docker sandbox system df](docker_sandbox_system_df.md) - 显示 Docker 沙箱磁盘使用情况
* [docker sandbox config create](docker_sandbox_config_create.md) - 创建配置
* [docker sandbox config inspect](docker_sandbox_config_inspect.md) - 显示配置的详细信息
* [docker sandbox config ls](docker_sandbox_config_ls.md) - 列出配置
* [docker sandbox config rm](docker_sandbox_config_rm.md) - 移除一个或多个配置
* [docker sandbox secret create](docker_sandbox_secret_create.md) - 创建机密
* [docker sandbox secret inspect](docker_sandbox_secret_inspect.md) - 显示机密的详细信息
* [docker sandbox secret ls](docker_sandbox_secret_ls.md) - 列出机密
* [docker sandbox secret rm](docker_sandbox_secret_rm.md) - 移除一个或多个机密
* [docker sandbox service create](docker_sandbox_service_create.md) - 创建服务
* [docker sandbox service inspect](docker_sandbox_service_inspect.md) - 显示服务的详细信息
* [docker sandbox service logs](docker_sandbox_service_logs.md) - 获取服务的日志
* [docker sandbox service ls](docker_sandbox_service_ls.md) - 列出服务
* [docker sandbox service ps](docker_sandbox_service_ps.md) - 列出服务的任务
* [docker sandbox service rm](docker_sandbox_service_rm.md) - 移除一个或多个服务
* [docker sandbox service rollback](docker_sandbox_service_rollback.md) - 回滚服务到上一个版本
* [docker sandbox service scale](docker_sandbox_service_scale.md) - 扩展或缩减一个或多个复制服务
* [docker sandbox service update](docker_sandbox_service_update.md) - 更新服务
* [docker sandbox stack deploy](docker_sandbox_stack_deploy.md) - 部署新堆栈或更新现有堆栈
* [docker sandbox stack ls](docker_sandbox_stack_ls.md) - 列出堆栈
* [docker sandbox stack ps](docker_sandbox_stack_ps.md) - 列出堆栈中的任务
* [docker sandbox stack rm](docker_sandbox_stack_rm.md) - 移除堆栈
* [docker sandbox stack services](docker_sandbox_stack_services.md) - 列出堆栈中的服务
* [docker sandbox swarm ca](docker_sandbox_swarm_ca.md) - 显示根 CA 证书和密钥的详细信息
* [docker sandbox swarm init](docker_sandbox_swarm_init.md) - 在当前节点上初始化 Swarm
* [docker sandbox swarm join](docker_sandbox_swarm_join.md) - 将节点加入 Swarm
* [docker sandbox swarm join-token](docker_sandbox_swarm_join-token.md) - 管理加入令牌
* [docker sandbox swarm leave](docker_sandbox_swarm_leave.md) - 离开 Swarm
* [docker sandbox swarm unlock](docker_sandbox_swarm_unlock.md) - 解锁 Swarm
* [docker sandbox swarm unlock-key](docker_sandbox_swarm_unlock-key.md) - 管理解锁密钥
* [docker sandbox swarm update](docker_sandbox_swarm_update.md) - 更新 Swarm
* [docker sandbox node demote](docker_sandbox_node_demote.md) - 将一个或多个节点降级
* [docker sandbox node inspect](docker_sandbox_node_inspect.md) - 显示一个或多个节点的详细信息
* [docker sandbox node ls](docker_sandbox_node_ls.md) - 列出节点
* [docker sandbox node promote](docker_sandbox_node_promote.md) - 将一个或多个节点提升
* [docker sandbox node ps](docker_sandbox_node_ps.md) - 列出一个或多个节点上的任务
* [docker sandbox node rm](docker_sandbox_node_rm.md) - 移除一个或多个节点
* [docker sandbox node update](docker_sandbox_node_update.md) - 更新节点
* [docker sandbox plugin create](docker_sandbox_plugin_create.md) - 从根文件夹中的文件和模板创建插件
* [docker sandbox plugin disable](docker_sandbox_plugin_disable.md) - 禁用插件
* [docker sandbox plugin enable](docker_sandbox_plugin_enable.md) - 启用插件
* [docker sandbox plugin inspect](docker_sandbox_plugin_inspect.md) - 显示一个或多个插件的详细信息
* [docker sandbox plugin install](docker_sandbox_plugin_install.md) - 安装插件
* [docker sandbox plugin ls](docker_sandbox_plugin_ls.md) - 列出插件
* [docker sandbox plugin push](docker_sandbox_plugin_push.md) - 将插件推送到注册表
* [docker sandbox plugin rm](docker_sandbox_plugin_rm.md) - 移除一个或多个插件
* [docker sandbox plugin set](docker_sandbox_plugin_set.md) - 更改插件的设置
* [docker sandbox plugin disable](docker_sandbox_plugin_disable.md) - 禁用插件
* [docker sandbox plugin enable](docker_sandbox_plugin_enable.md) - 启用插件
* [docker sandbox plugin upgrade](docker_sandbox_plugin_upgrade.md) - 升级插件
* [docker sandbox volume create](docker_sandbox_volume_create.md) - 创建卷
* [docker sandbox volume inspect](docker_sandbox_volume_inspect.md) - 显示一个或多个卷的详细信息
* [docker sandbox volume ls](docker_sandbox_volume_ls.md) - 列出卷
* [docker sandbox volume prune](docker_sandbox_volume_prune.md) - 移除所有未使用的卷
* [docker sandbox volume rm](docker_sandbox_volume_rm.md) - 移除一个或多个卷
* [docker sandbox network connect](docker_sandbox_network_connect.md) - 将沙箱连接到网络
* [docker sandbox network create](docker_sandbox_network_create.md) - 创建网络
* [docker sandbox network disconnect](docker_sandbox_network_disconnect.md) - 将沙箱与网络断开连接
* [docker sandbox network inspect](docker_sandbox_network_inspect.md) - 显示一个或多个网络的详细信息
* [docker sandbox network ls](docker_sandbox_network_ls.md) - 列出网络
* [docker sandbox network prune](docker_sandbox_network_prune.md) - 移除所有未使用的网络
* [docker sandbox network rm](docker_sandbox_network_rm.md) - 移除一个或多个网络
* [docker sandbox container attach](docker_sandbox_container_attach.md) - 附加到正在运行的沙箱
* [docker sandbox container commit](docker_sandbox_container_commit.md) - 创建沙箱的新镜像
* [docker sandbox container cp](docker_sandbox_container_cp.md) - 在沙箱和本地文件系统之间复制文件
* [docker sandbox container create](docker_sandbox_container_create.md) - 创建新沙箱
* [docker sandbox container diff](docker_sandbox_container_diff.md) - 检查沙箱文件系统的更改
* [docker sandbox container exec](docker_sandbox_container_exec.md) - 在正在运行的沙箱中执行命令
* [docker sandbox container export](docker_sandbox_container_export.md) - 将沙箱的文件系统导出为 tar 存档
* [docker sandbox container inspect](docker_sandbox_container_inspect.md) - 显示一个或多个沙箱的详细信息
* [docker sandbox container kill](docker_sandbox_container_kill.md) - 杀死一个或多个正在运行的沙箱
* [docker sandbox container logs](docker_sandbox_container_logs.md) - 获取沙箱的日志
* [docker sandbox container ls](docker_sandbox_container_ls.md) - 列出沙箱
* [docker sandbox container pause](docker_sandbox_container_pause.md) - 暂停一个或多个沙箱中的所有进程
* [docker sandbox container port](docker_sandbox_container_port.md) - 列出沙箱的端口映射或绑定
* [docker sandbox container prune](docker_sandbox_container_prune.md) - 移除所有停止的沙箱
* [docker sandbox container rename](docker_sandbox_container_rename.md) - 重命名沙箱
* [docker sandbox container restart](docker_sandbox_container_restart.md) - 重启一个或多个沙箱
* [docker sandbox container rm](docker_sandbox_container_rm.md) - 移除一个或多个沙箱
* [docker sandbox container run](docker_sandbox_container_run.md) - 在新沙箱中运行命令
* [docker sandbox container start](docker_sandbox_container_start.md) - 启动一个或多个停止的沙箱
* [docker sandbox container stats](docker_sandbox_container_stats.md) - 显示沙箱的实时资源使用统计
* [docker sandbox container stop](docker_sandbox_container_stop.md) - 停止一个或多个正在运行的沙箱
* [docker sandbox container top](docker_sandbox_container_top.md) - 显示沙箱中运行的进程
* [docker sandbox container unpause](docker_sandbox_container_unpause.md) - 恢复一个或多个沙箱中的所有进程
* [docker sandbox container update](docker_sandbox_container_update.md) - 更新一个或多个沙箱的配置
* [docker sandbox container wait](docker_sandbox_container_wait.md) - 阻塞直到一个或多个沙箱停止
* [docker sandbox container attach](docker_sandbox_container_attach.md) - 附加到正在运行的沙箱
* [docker sandbox container commit](docker_sandbox_container_commit.md) - 创建沙箱的新镜像
* [docker sandbox container cp](docker_sandbox_container_cp.md) - 在沙箱和本地文件系统之间复制文件
* [docker sandbox container create](docker_sandbox_container_create.md) - 创建新沙箱
* [docker sandbox container diff](docker_sandbox_container_diff.md) - 检查沙箱文件系统的更改
* [docker sandbox container exec](docker_sandbox_container_exec.md) - 在正在运行的沙箱中执行命令
* [docker sandbox container export](docker_sandbox_container_export.md) - 将沙箱的文件系统导出为 tar 存档
* [docker sandbox container inspect](docker_sandbox_container_inspect.md) - 显示一个或多个沙箱的详细信息
* [docker sandbox container kill](docker_sandbox_container_kill.md) - 杀死一个或多个正在运行的沙箱
* [docker sandbox container logs](docker_sandbox_container_logs.md) - 获取沙箱的日志
* [docker sandbox container ls](docker_sandbox_container_ls.md) - 列出沙箱
* [docker sandbox container pause](docker_sandbox_container_pause.md) - 暂停一个或多个沙箱中的所有进程
* [docker sandbox container port](docker_sandbox_container_port.md) - 列出沙箱的端口映射或绑定
* [docker sandbox container prune](docker_sandbox_container_prune.md) - 移除所有停止的沙箱
* [docker sandbox container rename](docker_sandbox_container_rename.md) - 重命名沙箱
* [docker sandbox container restart](docker_sandbox_container_restart.md) - 重启一个或多个沙箱
* [docker sandbox container rm](docker_sandbox_container_rm.md) - 移除一个或多个沙箱
* [docker sandbox container run](docker_sandbox_container_run.md) - 在新沙箱中运行命令
* [docker sandbox container start](docker_sandbox_container_start.md) - 启动一个或多个停止的沙箱
* [docker sandbox container stats](docker_sandbox_container_stats.md) - 显示沙箱的实时资源使用统计
* [docker sandbox container stop](docker_sandbox_container_stop.md) - 停止一个或多个正在运行的沙箱
* [docker sandbox container top](docker_sandbox_container_top.md) - 显示沙箱中运行的进程
* [docker sandbox container unpause](docker_sandbox_container_unpause.md) - 恢复一个或多个沙箱中的所有进程
* [docker sandbox container update](docker_sandbox_container_update.md) - 更新一个或多个沙箱的配置
* [docker sandbox container wait](docker_sandbox_container_wait.md) - 阻塞直到一个或多个沙箱停止
* [docker sandbox image build](docker_sandbox_image_build.md) - 从 Dockerfile 构建镜像
* [docker sandbox image history](docker_sandbox_image_history.md) - 显示镜像的历史记录
* [docker sandbox image import](docker_sandbox_image_import.md) - 从 tar 或 stdin 导入内容创建镜像
* [docker sandbox image inspect](docker_sandbox_image_inspect.md) - 显示一个或多个镜像的详细信息
* [docker sandbox image load](docker_sandbox_image_load.md) - 从 tar 存档或 stdin 加载镜像
* [docker sandbox image ls](docker_sandbox_image_ls.md) - 列出镜像
* [docker sandbox image prune](docker_sandbox_image_prune.md) - 移除未使用的镜像
* [docker sandbox image pull](docker_sandbox_image_pull.md) - 从注册表拉取镜像或仓库
* [docker sandbox image push](docker_sandbox_image_push.md) - 将镜像或仓库推送到注册表
* [docker sandbox image rm](docker_sandbox_image_rm.md) - 移除一个或多个镜像
* [docker sandbox image save](docker_sandbox_image_save.md) - 将一个或多个镜像保存到 tar 存档（可能压缩）
* [docker sandbox image tag](docker_sandbox_image_tag.md) - 为源镜像创建目标镜像的标签
* [docker sandbox manifest annotate](docker_sandbox_manifest_annotate.md) - 向本地清单或清单列表添加注释
* [docker sandbox manifest create](docker_sandbox_manifest_create.md) - 创建本地清单或清单列表
* [docker sandbox manifest inspect](docker_sandbox_manifest_inspect.md) - 显示清单或清单列表的详细信息
* [docker sandbox manifest push](docker_sandbox_manifest_push.md) - 将清单或清单列表推送到注册表
* [docker sandbox manifest rm](docker_sandbox_manifest_rm.md) - 删除一个或多个清单列表
* [docker sandbox trust inspect](docker_sandbox_trust_inspect.md) - 显示镜像的元数据
* [docker sandbox trust key generate](docker_sandbox_trust_key_generate.md) - 生成并加载密钥对
* [docker sandbox trust key load](docker_sandbox_trust_key_load.md) - 加载私钥
* [docker sandbox trust key remove](docker_sandbox_trust_key_remove.md) - 删除私钥
* [docker sandbox trust signer add](docker_sandbox_trust_signer_add.md) - 向给定的镜像添加签名者
* [docker sandbox trust signer remove](docker_sandbox_trust_signer_remove.md) - 从给定的镜像中删除签名者
* [docker sandbox trust sign](docker_sandbox_trust_sign.md) - 向镜像添加数字签名
* [docker sandbox trust revoke](docker_sandbox_trust_revoke.md) - 撤销对镜像的签名
* [docker sandbox trust rotate](docker_sandbox_trust_rotate.md) - 轮换给定角色的密钥
* [docker sandbox trust init](docker_sandbox_trust_init.md) - 初始化对镜像的签名验证
* [docker sandbox build buildkit](docker_sandbox_build_buildkit.md) - 使用 BuildKit 构建镜像
* [docker sandbox build prune](docker_sandbox_build_prune.md) - 清理构建缓存
* [docker sandbox context create](docker_sandbox_context_create.md) - 从 Dockerfile 创建镜像
* [docker sandbox context export](docker_sandbox_context_export.md) - 导出一个或多个上下文到 tar 文件或 stdin
* [docker sandbox context import](docker_sandbox_context_import.md) - 从 tar 文件或 stdin 导入上下文
* [docker sandbox context inspect](docker_sandbox_context_inspect.md) - 显示一个或多个上下文的详细信息
* [docker sandbox context ls](docker_sandbox_context_ls.md) - 列出上下文
* [docker sandbox context rm](docker_sandbox_context_rm.md) - 移除一个或多个上下文
* [docker sandbox context update](docker_sandbox_context_update.md) - 更新上下文
* [docker sandbox context use](docker_sandbox_context_use.md) - 设置当前 docker 上下文