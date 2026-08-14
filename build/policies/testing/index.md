# 测试构建策略


[`docker buildx policy test`](/reference/cli/docker/buildx/policy/test/) 命令使用 OPA 的 [标准测试框架](https://www.openpolicyagent.org/docs/policy-testing) 为构建策略运行单元测试。

```console
$ docker buildx policy test <path>
```

这使用模拟输入来验证策略逻辑。

要针对真实源（实际的镜像元数据、Git 仓库）进行测试，请改用 [`docker buildx policy eval`](/reference/cli/docker/buildx/policy/eval/)。你可以使用 `eval --print` 选项为特定源解析输入，以便编写测试用例。

## 基本示例

从一个只允 `alpine` 镜像的简单策略开始：

```rego {title="Dockerfile.rego"}
package docker

default allow = false

allow if {
    input.image.repo == "alpine"
}

decision := {"allow": allow}
```

创建一个带有 `*_test.rego` 后缀的测试文件。测试函数必须以 `test_` 开头：

```rego {title="Dockerfile_test.rego"}
package docker

test_alpine_allowed if {
    decision.allow with input as {"image": {"repo": "alpine"}}
}

test_ubuntu_denied if {
    not decision.allow with input as {"image": {"repo": "ubuntu"}}
}
```

运行测试：

```console
$ docker buildx policy test .
test_alpine_allowed: PASS (allow=true)
test_ubuntu_denied: PASS (allow=false)
```

`PASS` 表示 `Dockerfile_test.rego` 中定义的测试已成功执行，并且所有断言都得到满足。

## 命令选项

使用 `--run` 按名称过滤测试：

```console
$ docker buildx policy test --run alpine .
test_alpine_allowed: PASS (allow=true)
```

使用 `--filename` 测试具有非默认文件名的策略：

```console
$ docker buildx policy test --filename app.Dockerfile .
```

这会加载 `app.Dockerfile.rego` 并针对它运行 `*_test.rego` 文件。

## 测试输出

通过的测试显示允许状态和任何拒绝消息：

```console
test_alpine_allowed: PASS (allow=true)
test_ubuntu_denied: PASS (allow=false, deny_msg=only alpine images are allowed)
```

失败的测试显示输入、决策输出和缺失字段：

```console
test_invalid: FAIL (allow=false)
input:
  {
    "image": {}
  }
decision:
  {
    "allow": false,
    "deny_msg": [
      "only alpine images are allowed"
    ]
  }
missing_input: input.image.repo
```

## 测试拒绝消息

要测试自定义错误消息，请捕获完整的决策结果并对 `deny_msg` 字段进行断言。

对于一个带有拒绝消息的策略：

```rego {title="Dockerfile.rego"}
package docker

default allow = false

allow if {
    input.image.repo == "alpine"
}

deny_msg contains msg if {
    not allow
    msg := "only alpine images are allowed"
}

decision := {"allow": allow, "deny_msg": deny_msg}
```

测试拒绝消息：

```rego {title="Dockerfile_test.rego"}
test_deny_message if {
    result := decision with input as {"image": {"repo": "ubuntu"}}
    not result.allow
    "only alpine images are allowed" in result.deny_msg
}
```

## 测试模式

**测试特定环境的规则：**

```rego
test_production_requires_digest if {
    decision.allow with input as {
        "env": {"target": "production"},
        "image": {"isCanonical": true}
    }
}

test_development_allows_tags if {
    decision.allow with input as {
        "env": {"target": "development"},
        "image": {"isCanonical": false}
    }
}
```

**测试多个镜像仓库：**

```rego
test_dockerhub_allowed if {
    decision.allow with input as {
        "image": {
            "ref": "docker.io/library/alpine",
            "host": "docker.io",
            "repo": "alpine"
        }
    }
}

test_ghcr_allowed if {
    decision.allow with input as {
        "image": {
            "ref": "ghcr.io/myorg/myapp",
            "host": "ghcr.io",
            "repo": "myorg/myapp"
        }
    }
}
```

有关可用的输入字段，请参阅 [输入参考](./inputs.md)。

## 组织测试文件

测试运行器会递归发现所有 `*_test.rego` 文件：

```plaintext
build-policies/
├── Dockerfile.rego
├── Dockerfile_test.rego
└── tests/
    ├── registries_test.rego
    ├── signatures_test.rego
    └── environments_test.rego
```

运行所有测试：

```console
$ docker buildx policy test .
```

或测试特定文件：

```console
$ docker buildx policy test tests/registries_test.rego
```

