---
title: 使用 Docker 进行 ROS 2 开发入门
linkTitle: ROS 2
description: 学习如何使用 Docker 容器化并开发 ROS 2 应用。
keywords: ros2, robotics, devcontainers, python, cpp, Dockerfile, rviz
summary: |
  本指南详述了如何使用 Docker 容器化 ROS 2 应用。
aliases:
  - /guides/ros2/develop/
  - /guides/ros2/run-ros2/
  - /guides/ros2/turtlesim-example/
params:
  tags: [deployment]
  time: 30 minutes
  image: /images/guides/ros2.jpg
  featured: false
---


> **致谢**
>
> 本指南由社区贡献。Docker 在此感谢
> [Shakirth Anisha](https://www.linkedin.com/in/shakirth-anisha/) 对本指南的贡献。

[ROS 2](https://www.ros.org/) 是一套用于构建机器人应用的软件库和工具。它使用数据分发服务（Data Distribution Service，DDS）在分布式节点之间进行实时、安全的通信，非常适合机器人技术和自主系统。

---

## 你将学到什么？

在本指南中，你将学习如何：

- 使用 Docker Hub 上的官方 ROS 2 基础镜像
- 在 Ubuntu 容器中运行 ROS 2
- 安装 ROS 2 软件包和依赖
- 搭建用于本地开发的开发容器
- 用 Turtlesim 运行一个完整的端到端示例

## 先决条件

在开始之前，请确保你已熟悉以下内容：

- [Docker Desktop](https://docs.docker.com/desktop/)：你必须已安装并运行 Docker Desktop。
- [Docker 概念](/get-started/docker-concepts/the-basics/what-is-a-container.md)：你必须理解镜像和容器等核心 Docker 概念。
- [ROS 2 概念](https://www.ros.org)：对节点（nodes）、软件包（packages）、话题（topics）和服务（services）等基本概念有所了解。

## 接下来做什么？

首先使用 Docker 和开发容器搭建你的 ROS 2 开发环境。

## 在容器中运行 ROS 2

### 概述

在本节中，你将使用官方 ROS 2 镜像在隔离的 Docker 容器中运行 ROS 2，验证 ROS 2 是否正常工作，并安装额外的 ROS 2 软件包用于开发和测试。

---

### 在容器中运行 ROS 2

开始使用 ROS 2 最快的方式是使用[官方 Docker 镜像](https://hub.docker.com/_/ros/)。要拉取镜像、启动容器并打开交互式 bash shell：

1. 拉取并运行官方 ROS 2 Docker 镜像：

   ```console
   $ docker run -it ros:humble
   ```

   本指南使用的是 Humble 发行版。你可以将 `humble` 替换为其他受支持的发行版，例如 `rolling`、`jazzy` 或 `iron`。

   > [!NOTE]
   >
   > 该环境是临时的，不保证持久化。
   > 你创建的任何文件或安装的软件包，在容器停止或移除后都会被删除。

2. 验证 ROS 2 是否正常工作：

   ```console
   $ echo $ROS_DISTRO
   ```

   你应该会看到类似如下的输出：

   ```text
   humble
   ```

### 安装 ROS 2 软件包

官方 ROS 2 镜像包含核心软件包。要安装额外的软件包，请使用 `apt` 包管理器：

1. 更新包管理器：

   ```console
   $ sudo apt update
   ```

2. 安装所需软件包：

   ```console
   $ sudo apt install $PACKAGE_NAME
   ```

将 `$PACKAGE_NAME` 替换为你想安装的任何软件包。

一些常用的软件包包括：

- `ros-humble-turtlesim` —— 可视化与仿真工具
- `ros-humble-rviz2` —— 3D 可视化工具
- `ros-humble-rqt` —— 基于 Qt 的 ROS 图形工具
- `ros-humble-demo-nodes-cpp` —— C++ 演示节点
- `ros-humble-demo-nodes-py` —— Python 演示节点
- `ros-humble-colcon-common-extensions` —— 构建系统扩展

### 小结

在本节中，你拉取了官方 ROS 2 Docker 镜像，启动了交互式会话，并通过使用 apt 安装额外的 ROS 2 软件包扩展了容器的能力。

### 下一步

在下一节中，你将配置一个持久化的工作区，以确保你的代码和修改在各会话之间都能保存。

## 构建并开发 ROS 2 工作区

### 概述

在本节中，你将使用 Docker 和开发容器搭建一个 ROS 2 工作区，查看工作区布局，在 Visual Studio Code 中打开工作区，并在容器内编辑和构建 ROS 2 项目。

---

### 获取示例 ROS 2 工作区

一致的工作区可以简化跨不同发行版的 ROS 2 项目和构建产物的管理。

1. 打开终端，克隆示例工作区仓库：

   ```console
   $ git clone https://github.com/shakirth-anisha/docker-ros2-workspace.git
   $ cd docker-ros2-workspace

   ```

   后续 Linux 用户可以使用 `ws_linux` 文件夹，macOS 用户可以使用 `ws_mac`。

2. 验证工作区结构：

   ```text
   ws_linux/
   ├── compose.yml
   ├── Dockerfile
   └── src/
       ├── package1/
       └── package2/

   ws_mac/
   ├── compose.yml
   ├── Dockerfile
   └── src/
       ├── package1/
       └── package2/

   ```

3. 探索工作区布局

- `compose.yml`：定义 Docker Compose 如何构建和运行 ROS 2 容器，包括挂载、环境变量和网络设置。
- `Dockerfile`：构建 ROS 2 开发镜像。它使用官方 ROS 2 基础镜像，创建非 root 的开发用户，并安装所需的系统和 ROS 2 依赖。
- `src`：包含所有 ROS 2 软件包。该目录作为活动工作区挂载到容器中。

### 打开并构建容器

1. 执行以下命令构建并启动容器：

   Linux：

   ```console
   $ cd ws_linux
   $ docker compose up -d
   $ docker compose exec ros2 /bin/bash
   ```

   macOS：

   ```console
   $ cd ws_mac
   $ docker compose up -d
   $ docker compose exec ros2 /bin/bash
   ```

   该命令会构建你 `Dockerfile` 中定义的 Docker 镜像，并在后台启动容器。

   > [!NOTE]
   >
   > 首次运行时构建镜像可能需要几分钟，
   > 因为 CLI 需要拉取 ROS 2 基础镜像并安装所需依赖。
   > 后续启动会明显更快。

2. 容器运行后，使用 `exec` 在容器内执行命令：

   ```console
   $ docker compose exec ros2 /bin/bash
   ```

3. 在容器终端内，验证环境：

```console
$ echo $ROS_VERSION
$ which colcon
```

所有命令都应在容器内成功执行。

### 切换 ROS 2 发行版

更新你 `Dockerfile` 中的基础镜像，从 `humble` 改为其他发行版，例如 `rolling`、`jazzy` 或 `iron`。

### 小结

在本节中，你学习了如何创建结构化的工作区、编写包含开发工具的 Dockerfile，并配置 Docker Compose 设置。你的 ROS 2 开发环境现已就绪，可在任意机器上获得一致、可复现的设置。

### 下一步

在下一节中，你将用 Turtlesim 运行一个完整的端到端示例。

## 用 Turtlesim 运行完整示例

### 概述

Turtlesim 是一个简单的仿真工具，用于演示节点、话题和服务等 ROS 2 基础概念。在本节中，你将用 Turtlesim 运行一个完整示例，控制乌龟、监视话题，并使用 rqt 可视化系统。

---

### 配置显示转发

#### Linux

允许 Docker 访问你的 X 服务器：

```console
$ xhost +local:docker
```

#### macOS

在 macOS 上，使用 XQuartz 提供 X11 支持。使用 Homebrew 安装 XQuartz：

1. 使用 Homebrew 安装 XQuartz：

   ```console
   $ brew install --cask xquartz
   ```

2. 从应用程序打开 XQuartz，然后进入 `Preferences > Security`（偏好设置 > 安全），并启用 `Allow connections from network clients`（允许来自网络客户端的连接）。重启你的电脑以确保更改生效。

3. 重启后，打开终端并允许本地连接：

   ```console
   $ defaults write org.xquartz.X11 nolisten_tcp -bool false
   $ xhost +localhost
   $ xhost + 127.0.0.1
   ```

### 启动容器

使用与工作区一节相同的 Docker Compose 设置启动容器。

Linux：

```console
$ cd ws_linux
$ docker compose up -d
$ docker compose exec ros2 /bin/bash
```

macOS：

```console
$ cd ws_mac
$ docker compose up -d
$ docker compose exec ros2 /bin/bash
```

### 安装并运行 Turtlesim

在容器内，安装 Turtlesim 软件包：

1. 更新包管理器：

   ```console
   $ sudo apt update
   ```

2. 安装 Turtlesim 软件包：

   ```console
   $ sudo apt install -y ros-humble-turtlesim
   ```

3. 运行 Turtlesim 节点：

   ```console
   $ ros2 run turtlesim turtlesim_node
   ```

   你的桌面上应出现一个窗口，显示网格中的一只乌龟。

### 控制乌龟

1. 打开一个新终端并连接到同一个容器，然后启动键盘 teleop 节点：

   ```console
   $ ros2 run turtlesim turtle_teleop_key
   ```

   该节点允许你用键盘控制乌龟。使用方向键让乌龟向前、向后、向左、向右移动。按 `Ctrl+C` 停止 teleop 节点。

2. 让乌龟在窗口中移动。你应该会看到它移动时画出一条路径。

### 监视话题

1. 打开另一个终端并连接到同一个容器，然后列出所有活动话题：

   ```console
   $ ros2 topic list
   ```

   你应该会看到类似如下的输出：

   ```text
   /parameter_events
   /rosout
   /turtle1/cmd_vel
   /turtle1/color_sensor
   /turtle1/pose
   ```

2. 获取某个特定话题的信息：

   ```console
   $ ros2 topic info /turtle1/pose
   ```

   你会看到话题类型，以及哪些节点发布和订阅它。

### 使用 rqt 可视化系统

1. 打开另一个终端并连接到同一个容器，然后更新包管理器：

   ```console
   $ sudo apt update
   ```

2. 安装 rqt：

   ```console
   $ sudo apt install -y 'ros-humble-rqt*'
   ```

3. 启动 rqt：

   ```console
   $ ros2 run rqt_gui rqt_gui
   ```

   应出现一个 rqt 窗口。rqt 提供了多个用于可视化和监视 ROS 2 系统的实用插件。

#### 节点图

你可以通过 **Plugins > Introspection > Node Graph** 浏览节点图。会打开一个新标签页，以线条显示节点和话题及其连接关系。该可视化展示了 teleop 节点如何将速度命令发送给 Turtlesim 节点，以及 Turtlesim 节点如何通过话题将位置数据发布回去。

#### 话题监视器

你可以通过 **Plugins > Topics > Topic Monitor** 监视活动话题。会打开一个新标签页，显示所有活动话题及其当前值。点击 `/turtle1/pose` 旁边的眼睛图标以监视它。当你移动乌龟时，观察位姿值实时更新，显示乌龟的位置和朝向随你的命令而变化。

#### 服务调用器

你可以使用 **Plugins > Services > Service Caller** 从 rqt 调用服务。选择一个服务（例如 `/turtle1/teleport_absolute`），在请求字段中输入值，然后选择 **Call** 发送请求。

#### 绘图

要随时间的推移绘制话题数据，请导航到 **Plugins > Visualization > Plot**。例如，在 Plot 窗口的 Topic 字段中输入 `/turtle1/pose/x` 并按回车。移动乌龟并观察 X 位置随时间以图形方式显示。

### 调用 ROS 2 服务

Turtlesim 提供了用于重定位乌龟、清除路径等动作的服务。

1. 列出可用服务：

   ```console
   $ ros2 service list
   ```

   你应该会看到诸如 `/turtle1/set_pen`（更改画笔颜色和宽度）、`/turtle1/teleport_absolute`（将乌龟移动到指定位置）和 `/turtle1/teleport_relative`（相对于乌龟当前位置移动它）之类的服务。

2. 将乌龟传送到新位置：

   ```console
   $ ros2 service call /turtle1/teleport_absolute turtlesim/srv/TeleportAbsolute "
   x: 1.0
   y: 3.0
   theta: 0.0
   "
   ```

   乌龟应立即移动到指定位置 (1.0, 3.0)。

### 创建一个简单的发布者

1. 创建一个 Python 脚本，发布速度命令以编程方式控制乌龟。在新终端中，创建一个名为 `move_turtle.py` 的文件：

   ```python
   import rclpy
   from geometry_msgs.msg import Twist
   import time

   def main():
       rclpy.init()
       node = rclpy.create_node('turtle_mover')
       publisher = node.create_publisher(Twist, 'turtle1/cmd_vel', 10)

       # Create a twist message
       msg = Twist()
       msg.linear.x = 2.0  # Move forward at 2 m/s
       msg.angular.z = 1.0  # Rotate at 1 rad/s

       # Publish the message
       for i in range(50):
           publisher.publish(msg)
           time.sleep(0.1)

       # Stop the turtle
       msg.linear.x = 0.0
       msg.angular.z = 0.0
       publisher.publish(msg)

       node.destroy_node()
       rclpy.shutdown()

   if __name__ == '__main__':
       main()
   ```

2. 运行脚本：

   ```console
   $ python3 move_turtle.py
   ```

   乌龟应做圆周运动 5 秒，然后停止。

### 小结

在本节中，你配置了显示转发，使用了 Turtlesim 节点，检查了节点和话题，并使用 rqt 可视化了系统。最后，你与 ROS 2 服务进行了交互，并创建了一个简单的发布者以编程方式移动乌龟。

这些基础概念直接适用于具有真实传感器和执行器的实际机器人应用。

### 相关资源

- [ROS 2 Turtlesim 教程](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
- [ROS 2 概念](https://docs.ros.org/en/humble/Concepts.html)
- [Geometry 消息](https://github.com/ros2/geometry2/tree/humble/geometry_msgs)
