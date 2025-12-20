# 在 Docker Desktop 中使用 USB/IP





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 
    
  
  <a class="link" href="https://docs.docker.com/desktop/release-notes/#4350">4.35.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">For:</span>
        <span>Docker Desktop for Mac, Linux, and Windows with the Hyper-V backend</span>
        
      </div>
    
  </div>



USB/IP 可让您通过网络共享 USB 设备，然后即可从 Docker 容器内访问这些设备。本页面重点介绍如何共享连接到运行 Docker Desktop 的主机上的 USB 设备。您可以根据需要重复以下过程来挂载和使用其他 USB 设备。

> [!NOTE]
>
> Docker Desktop 包含许多常见 USB 设备的内置驱动程序，但 Docker 无法保证所有 USB 设备都能在此设置下正常工作。

## 设置与使用

### 第一步：运行 USB/IP 服务器

要使用 USB/IP，您需要运行一个 USB/IP 服务器。本指南将使用 [jiegec/usbip](https://github.com/jiegec/usbip) 提供的实现。

1. 克隆仓库。

    ```console
    $ git clone https://github.com/jiegec/usbip
    $ cd usbip
    ```

2. 运行模拟的人机接口设备 (HID) 示例。

    ```console
    $ env RUST_LOG=info cargo run --example hid_keyboard
    ```

### 第二步：启动特权 Docker 容器

要挂载 USB 设备，请启动一个特权 Docker 容器，并将其 PID 命名空间设置为 `host`：

```console
$ docker run --rm -it --privileged --pid=host alpine
```

`--privileged` 使容器拥有对主机的完全访问权限，`--pid=host` 允许其共享主机的进程命名空间。

### 第三步：进入 PID 1 的挂载命名空间

在容器内，进入 `init` 进程的挂载命名空间，以访问预安装的 USB/IP 工具：

```console
$ nsenter -t 1 -m
```

### 第四步：使用 USB/IP 工具

现在，您可以像在任何其他系统上一样使用 USB/IP 工具：

#### 列出 USB 设备

列出主机上可导出的 USB 设备：

```console
$ usbip list -r host.docker.internal
```

预期输出：

```console
Exportable USB devices
======================
 - host.docker.internal
      0-0-0: unknown vendor : unknown product (0000:0000)
           : /sys/bus/0/0/0
           : (Defined at Interface level) (00/00/00)
           :  0 - unknown class / unknown subclass / unknown protocol (03/00/00)
```

#### 挂载 USB 设备

要挂载特定的 USB 设备，本例中是模拟的键盘：

```console
$ usbip attach -r host.docker.internal -d 0-0-0
```

#### 验证设备挂载

挂载模拟键盘后，检查 `/dev/input` 目录中的设备节点：

```console
$ ls /dev/input/
```

示例输出：

```console
event0  mice
```

### 第五步：从另一个容器访问设备

当初始容器保持运行以维持 USB 设备操作时，您可以从另一个容器访问已挂载的设备。例如：

1. 启动一个包含已挂载设备的新容器。

    ```console
    $ docker run --rm -it --device "/dev/input/event0" alpine
    ```

2. 安装 `evtest` 等工具来测试模拟键盘。

    ```console
    $ apk add evtest
    $ evtest /dev/input/event0
    ```

3. 与设备交互，并观察输出。

    示例输出：

    ```console
    Input driver version is 1.0.1
    Input device ID: bus 0x3 vendor 0x0 product 0x0 version 0x111
    ...
    Properties:
    Testing ... (interrupt to exit)
    Event: time 1717575532.881540, type 4 (EV_MSC), code 4 (MSC_SCAN), value 7001e
    Event: time 1717575532.881540, type 1 (EV_KEY), code 2 (KEY_1), value 1
    Event: time 1717575532.881540, -------------- SYN_REPORT ------------
    ...
    ```

> [!IMPORTANT]
>
> 初始容器必须保持运行以维持与 USB 设备的连接。退出容器将导致设备停止工作。
