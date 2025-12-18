---
datafolder: sandbox-cli
datafile: docker_sandbox_inspect
title: docker sandbox inspect
layout: cli
---

# docker sandbox inspect

显示沙箱的详细信息

## 用法

```
docker sandbox inspect [OPTIONS] SANDBOX
```

## 描述

返回 Docker 沙箱的详细信息。

## 选项

| 名称, 简写 | 默认值 | 描述 |
| --- | --- | --- |
| `--format , -f` |  | 使用 Go 模板格式化输出 |
| `--pretty` |  | 以人类可读的格式打印工件，并转储所有 YAML |

## 父命令

| 命令 | 描述 |
| --- | --- |
| [docker sandbox](docker_sandbox.md) | 管理沙箱 |

## 相关命令

| 命令 | 描述 |
| --- | --- |
| [docker sandbox inspect](docker_sandbox_inspect.md) | 显示沙箱的详细信息 |
| [docker sandbox ls](docker_sandbox_ls.md) | 列出沙箱 |
| [docker sandbox rm](docker_sandbox_rm.md) | 移除一个或多个沙箱 |
| [docker sandbox stop](docker_sandbox_stop.md) | 停止一个或多个沙箱 |

## 示例

### 按名称或 ID 过滤

`docker sandbox inspect` 接受沙箱名称或 ID。例如，给定以下沙箱：

```console
$ docker sandbox ls

Sandbox ID          Name                Labels              Created             Updated             Status              IPv4 Address        IPv6 Address        Node ID             Task ID
a23456789b0cd       web-server-1        <none>              10 minutes ago      10 minutes ago      RUNNING             10.0.0.3/24         -                   a1234567890bc       a3456789b0cde
```

```console
$ docker sandbox inspect a23456789b0cd

[
    {
        "ID": "a23456789b0cd",
        "Version": {
            "Index": 123
        },
        "CreatedAt": "2025-08-22T21:36:56.789012Z",
        "UpdatedAt": "2025-08-22T21:36:56.789012Z",
        "Spec": {
            "Labels": {},
            "Ingress": false,
            "LoadBalancer": {
                "Mode": "vip"
            },
            "Task": {
                "ID": "a3456789b0cde",
                "Version": {
                    "Index": 124
                },
                "Spec": {
                    "ContainerSpec": {
                        "Image": "nginx:latest",
                        "Labels": {
                            "com.docker.stack.namespace": "web"
                        },
                        "Privileges": {
                            "CredentialSpec": null,
                            "SELinuxContext": null
                        },
                        "Hostname": "web-server-1",
                        "StopGracePeriod": 10000000000,
                        "DNSConfig": {},
                        "Isolation": "default"
                    },
                    "Resources": {
                        "Limits": {},
                        "Reservations": {}
                    },
                    "RestartPolicy": {
                        "Condition": "any",
                        "Delay": 5000000000,
                        "MaxAttempts": 0,
                        "Window": 0
                    },
                    "Placement": {
                        "Platforms": [
                            {
                                "Architecture": "amd64",
                                "OS": "linux"
                            }
                        ]
                    },
                    "Networks": [
                        {
                            "Target": "web-network"
                        }
                    ],
                    "ForceUpdate": 0,
                    "Runtime": "container",
                    "Infra": {
                        "Image": "docker.io/library/alpine:latest"
                    }
                },
                "ServiceID": "s1234567890abc",
                "Slot": 1,
                "NodeID": "a1234567890bc",
                "Status": {
                    "Timestamp": "2025-08-22T21:36:56.789012Z",
                    "State": "running",
                    "Message": "started",
                    "ContainerStatus": {
                        "ContainerID": "c987654321fedba98",
                        "PID": 1234,
                        "ExitCode": 0
                    },
                    "PortStatus": {}
                },
                "DesiredState": "running",
                "NetworksAttachments": [
                    {
                        "Network": {
                            "ID": "n1234567890abc",
                            "Version": {
                                "Index": 125
                            },
                            "CreatedAt": "2025-08-22T21:36:56.789012Z",
                            "UpdatedAt": "2025-08-22T21:36:56.789012Z",
                            "Spec": {
                                "Name": "web-network",
                                "Labels": {},
                                "DriverConfiguration": {},
                                "IPAMOptions": {
                                    "Driver": {
                                        "Name": "default"
                                    },
                                    "Configs": [
                                        {
                                            "Subnet": "10.0.0.0/24",
                                            "Gateway": "10.0.0.1"
                                        }
                                    ]
                                }
                            },
                            "Driver": "overlay",
                            "IPAMOptions": {
                                "Driver": {
                                    "Name": "default"
                                },
                                "Configs": [
                                    {
                                        "Subnet": "10.0.0.0/24",
                                        "Gateway": "10.0.0.1"
                                    }
                                ]
                            }
                        },
                        "Addresses": [
                            "10.0.0.3/24"
                        ]
                    }
                ]
            },
            "Endpoint": {
                "Spec": {},
                "VirtualIPs": [
                    {
                        "NetworkID": "n1234567890abc",
                        "Addr": "10.0.0.4/24"
                    }
                ]
            }
        },
        "Endpoint": {
            "Spec": {},
            "VirtualIPs": [
                {
                    "NetworkID": "n1234567890abc",
                    "Addr": "10.0.0.4/24"
                }
            ]
        }
    }
]
```

### 格式化输出

使用 `--format` 选项，可以使用 Go 模板格式化 `docker sandbox inspect` 的输出。

使用 `--format` 选项时，`docker sandbox inspect` 会将指定的 Go 模板应用于每个查询结果。

Go 模板提示：

- `%+v` 会以其所有字段和值的完整语法打印值
- `{{ .Field }}` 会打印特定字段的值
- 如果字段是结构体，`{{ .Field.SubField }}` 会打印该字段的子字段

#### 示例 1：获取沙箱的创建时间

```console
$ docker sandbox inspect --format='{{.CreatedAt}}' a23456789b0cd

2025-08-22T21:36:56.789012Z
```

#### 示例 2：获取沙箱的 IPv4 地址

```console
$ docker sandbox inspect --format='{{.Task.NetworksAttachments.0.Addresses.0}}' a23456789b0cd

10.0.0.3/24
```

#### 示例 3：获取沙箱的节点 ID

```console
$ docker sandbox inspect --format='{{.Task.NodeID}}' a23456789b0cd

a1234567890bc
```

#### 示例 4：获取沙箱的任务状态

```console
$ docker sandbox inspect --format='{{.Task.Status.State}}' a23456789b0cd

running
```

#### 示例 5：获取沙箱的容器 ID

```console
$ docker sandbox inspect --format='{{.Task.Status.ContainerStatus.ContainerID}}' a23456789b0cd

c987654321fedba98
```

#### 示例 6：获取沙箱的镜像

```console
$ docker sandbox inspect --format='{{.Task.Spec.ContainerSpec.Image}}' a23456789b0cd

nginx:latest
```

#### 示例 7：获取沙箱的网络 ID

```console
$ docker sandbox inspect --format='{{.Task.NetworksAttachments.0.Network.ID}}' a23456789b0cd

n1234567890abc
```

#### 示例 8：获取沙箱的标签

```console
$ docker sandbox inspect --format='{{json .Spec.Labels}}' a23456789b0cd

{}
```

#### 示例 9：获取沙箱的重启策略条件

```console
$ docker sandbox inspect --format='{{.Task.Spec.RestartPolicy.Condition}}' a23456789b0cd

any
```

#### 示例 10：获取沙箱的资源限制

```console
$ docker sandbox inspect --format='{{json .Task.Spec.Resources.Limits}}' a23456789b0cd

{}
```

#### 示例 11：获取沙箱的资源预留

```console
$ docker sandbox inspect --format='{{json .Task.Spec.Resources.Reservations}}' a23456789b0cd

{}
```

#### 示例 12：获取沙箱的放置平台

```console
$ docker sandbox inspect --format='{{json .Task.Spec.Placement.Platforms}}' a23456789b0cd

[{"Architecture":"amd64","OS":"linux"}]
```

#### 示例 13：获取沙箱的网络目标

```console
$ docker sandbox inspect --format='{{.Task.Spec.Networks.0.Target}}' a23456789b0cd

web-network
```

#### 示例 14：获取沙箱的虚拟 IP

```console
$ docker sandbox inspect --format='{{.Endpoint.VirtualIPs.0.Addr}}' a23456789b0cd

10.0.0.4/24
```

#### 示例 15：获取沙箱的更新时间

```console
$ docker sandbox inspect --format='{{.UpdatedAt}}' a23456789b0cd

2025-08-22T21:36:56.789012Z
```

#### 示例 16：获取沙箱的任务版本索引

```console
$ docker sandbox inspect --format='{{.Task.Version.Index}}' a23456789b0cd

124
```

#### 示例 17：获取沙箱的沙箱版本索引

```console
$ docker sandbox inspect --format='{{.Version.Index}}' a23456789b0cd

123
```

#### 示例 18：获取沙箱的主机名

```console
$ docker sandbox inspect --format='{{.Task.Spec.ContainerSpec.Hostname}}' a23456789b0cd

web-server-1
```

#### 示例 19：获取沙箱的停止宽限期

```console
$ docker sandbox inspect --format='{{.Task.Spec.ContainerSpec.StopGracePeriod}}' a23456789b0cd

10000000000
```

#### 示例 20：获取沙箱的重启策略延迟

```console
$ docker sandbox inspect --format='{{.Task.Spec.RestartPolicy.Delay}}' a23456789b0cd

5000000000
```

#### 示例 21：获取沙箱的重启策略最大尝试次数

```console
$ docker sandbox inspect --format='{{.Task.Spec.RestartPolicy.MaxAttempts}}' a23456789b0cd

0
```

#### 示例 22：获取沙箱的重启策略窗口

```console
$ docker sandbox inspect --format='{{.Task.Spec.RestartPolicy.Window}}' a23456789b0cd

0
```

#### 示例 23：获取沙箱的容器 PID

```console
$ docker sandbox inspect --format='{{.Task.Status.ContainerStatus.PID}}' a23456789b0cd

1234
```

#### 示例 24：获取沙箱的容器退出码

```console
$ docker sandbox inspect --format='{{.Task.Status.ContainerStatus.ExitCode}}' a23456789b0cd

0
```

#### 示例 25：获取沙箱的端口状态

```console
$ docker sandbox inspect --format='{{json .Task.Status.PortStatus}}' a23456789b0cd

{}
```

#### 示例 26：获取沙箱的网络规范

```console
$ docker sandbox inspect --format='{{json .Task.NetworksAttachments.0.Network.Spec}}' a23456789b0cd

{"Name":"web-network","Labels":{},"DriverConfiguration":{},"IPAMOptions":{"Driver":{"Name":"default"},"Configs":[{"Subnet":"10.0.0.0/24","Gateway":"10.0.0.1"}]}}
```

#### 示例 27：获取沙箱的网络驱动

```console
$ docker sandbox inspect --format='{{.Task.NetworksAttachments.0.Network.Driver}}' a23456789b0cd

overlay
```

#### 示例 28：获取沙箱的 IPAM 配置

```console
$ docker sandbox inspect --format='{{json .Task.NetworksAttachments.0.Network.IPAMOptions}}' a23456789b0cd

{"Driver":{"Name":"default"},"Configs":[{"Subnet":"10.0.0.0/24","Gateway":"10.0.0.1"}]}
```

#### 示例 29：获取沙箱的网络创建时间

```console
$ docker sandbox inspect --format='{{.Task.NetworksAttachments.0.Network.CreatedAt}}' a23456789b0cd

2025-08-22T21:36:56.789012Z
```

#### 示例 30：获取沙箱的网络更新时间

```console
$ docker sandbox inspect --format='{{.Task.NetworksAttachments.0.Network.UpdatedAt}}' a23456789b0cd

2025-08-22T21:36:56.789012Z
```

#### 示例 31：获取沙箱的网络版本索引

```console
$ docker sandbox inspect --format='{{.Task.NetworksAttachments.0.Network.Version.Index}}' a23456789b0cd

125
```

#### 示例 32：获取沙箱的网络地址

```console
$ docker sandbox inspect --format='{{json .Task.NetworksAttachments.0.Addresses}}' a23456789b0cd

["10.0.0.3/24"]
```

#### 示例 33：获取沙箱的任务规范

```console
$ docker sandbox inspect --format='{{json .Task.Spec}}' a23456789b0cd

{"ContainerSpec":{"Image":"nginx:latest","Labels":{"com.docker.stack.namespace":"web"},"Privileges":{"CredentialSpec":null,"SELinuxContext":null},"Hostname":"web-server-1","StopGracePeriod":10000000000,"DNSConfig":{},"Isolation":"default"},"Resources":{"Limits":{},"Reservations":{}},"RestartPolicy":{"Condition":"any","Delay":5000000000,"MaxAttempts":0,"Window":0},"Placement":{"Platforms":[{"Architecture":"amd64","OS":"linux"}]},"Networks":[{"Target":"web-network"}],"ForceUpdate":0,"Runtime":"container","Infra":{"Image":"docker.io/library/alpine:latest"}}
```

#### 示例 34：获取沙箱的容器规范

```console
$ docker sandbox inspect --format='{{json .Task.Spec.ContainerSpec}}' a23456789b0cd

{"Image":"nginx:latest","Labels":{"com.docker.stack.namespace":"web"},"Privileges":{"CredentialSpec":null,"SELinuxContext":null},"Hostname":"web-server-1","StopGracePeriod":10000000000,"DNSConfig":{},"Isolation":"default"}
```

#### 示例 35：获取沙箱的资源规范

```console
$ docker sandbox inspect --format='{{json .Task.Spec.Resources}}' a23456789b0cd

{"Limits":{},"Reservations":{}}
```

#### 示例 36：获取沙箱的重启策略规范

```console
$ docker sandbox inspect --format='{{json .Task.Spec.RestartPolicy}}' a23456789b0cd

{"Condition":"any","Delay":5000000000,"MaxAttempts":0,"Window":0}
```

#### 示例 37：获取沙箱的放置规范

```console
$ docker sandbox inspect --format='{{json .Task.Spec.Placement}}' a23456789b0cd

{"Platforms":[{"Architecture":"amd64","OS":"linux"}]}
```

#### 示例 38：获取沙箱的网络规范列表

```console
$ docker sandbox inspect --format='{{json .Task.Spec.Networks}}' a23456789b0cd

[{"Target":"web-network"}]
```

#### 示例 39：获取沙箱的强制