# 在基于 Arch 的发行版上安装 Docker Desktop





  
  
  
  


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
    

    

    
  </div>



> **Docker Desktop 使用条款**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要 [付费订阅](https://www.docker.com/pricing/)。

本页面包含如何在基于 Arch 的发行版上安装、启动和升级 Docker Desktop 的信息。

## 前置条件

要成功安装 Docker Desktop，您必须满足 [通用系统要求](_index.md#general-system-requirements)。

## 安装 Docker Desktop

1. [在 Linux 上安装 Docker 客户端二进制文件](/manuals/engine/install/binaries.md#install-daemon-and-client-binaries-on-linux)。Linux 的 Docker 客户端静态二进制文件可作为 `docker` 获得。您可以使用：

   ```console
   $ wget https://download.docker.com/linux/static/stable/x86_64/docker-29.1.3.tgz -qO- | tar xvfz - docker/docker --strip-components=1
   $ sudo cp -rp ./docker /usr/local/bin/ && rm -r ./docker
   ```

2. 从 [发布说明](/manuals/desktop/release-notes.md) 下载最新的 Arch 包。

3. 安装该包：

   ```console
   $ sudo pacman -U ./docker-desktop-x86_64.pkg.tar.zst
   ```

   默认情况下，Docker Desktop 安装在 `/opt/docker-desktop`。

## 启动 Docker Desktop



要启动 Docker Desktop for Linux：

1.  在您的 Gnome/KDE 桌面中找到 Docker Desktop 应用程序。
2.  选择 **Docker Desktop** 以启动 Docker。

    此时将显示 Docker 订阅服务协议。

3.  选择 **接受** 继续。接受条款后，Docker Desktop 将会启动。

    请注意，如果您不同意该条款，Docker Desktop 将无法运行。您可以通过稍后打开 Docker Desktop 来选择接受条款。

    更多信息，请参阅 [Docker Desktop 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)。建议您同时阅读 [常见问题解答](https://www/docker.com/pricing/faq)。

或者，打开终端并运行：

```console
$ systemctl --user start docker-desktop
```

当 Docker Desktop 启动时，它会创建一个专用的 [上下文](/engine/context/working-with-contexts)，供 Docker CLI 作为目标使用，并将其设置为当前正在使用的上下文。这样做是为了避免与可能在 Linux 主机上运行并使用默认上下文的本地 Docker Engine 发生冲突。关闭时，Docker Desktop 会将当前上下文重置为之前的上下文。

Docker Desktop 安装程序会更新主机上的 Docker Compose 和 Docker CLI 二进制文件。它会安装 Docker Compose V2，并允许用户通过设置面板选择将其链接为 docker-compose。Docker Desktop 会在 `/usr/local/bin/com.docker.cli` 安装包含云集成功能的新版 Docker CLI 二进制文件，并在 `/usr/local/bin` 创建指向经典 Docker CLI 的符号链接。

成功安装 Docker Desktop 后，您可以通过运行以下命令来检查这些二进制文件的版本：

```console
$ docker compose version
Docker Compose version v2.39.4

$ docker --version
Docker version 28.4.0, build d8eb465

$ docker version
Client:
 Version:           28.4.0
 API version:       1.51
 Go version:        go1.24.7
<...>
```

要让 Docker Desktop 在登录时自动启动，请从 Docker 菜单中选择 **设置** > **常规** > **登录计算机时启动 Docker Desktop**。

或者，打开终端并运行：

```console
$ systemctl --user enable docker-desktop
```

要停止 Docker Desktop，请选择 Docker 菜单图标以打开 Docker 菜单，然后选择 **退出 Docker Desktop**。

或者，打开终端并运行：

```console
$ systemctl --user stop docker-desktop
```

## 后续步骤

- 探索 [Docker 的订阅计划](https://www.docker.com/pricing/)，了解 Docker 能为您提供什么。
- 查看 [Docker 工作坊](/get-started/workshop/_index.md)，学习如何构建镜像并将其作为容器化应用程序运行。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 描述了常见问题、解决方法、如何运行和提交诊断信息以及提交问题的方法。
- [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供了对常见问题的解答。
- [发布说明](/manuals/desktop/release-notes.md) 列出了与 Docker Desktop 发布相关的组件更新、新功能和改进。
- [备份和还原数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了与 Docker 相关的数据备份和还原的说明。
