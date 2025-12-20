# 在 Kubernetes 中使用 Docker Hardened 镜像

## 认证

要在 Kubernetes 中使用 Docker Hardened Images，你需要创建一个 Kubernetes 密钥（secret），以便从你的镜像或内部注册表中拉取镜像。

> [!NOTE]
>
> 你需要在每个使用 DHI 的 Kubernetes 命名空间中创建此密钥。

使用个人访问令牌（PAT）创建密钥。确保该令牌至少对公共仓库具有只读访问权限。对于 Docker Hardened Images，将 `<registry server>` 替换为 `dhi.io`。如果你使用的是镜像仓库，请将其替换为你的镜像注册表服务器，例如 Docker Hub 使用 `docker.io`。

```console
$ kubectl create -n <kubernetes namespace> secret docker-registry <secret name> --docker-server=<registry server> \
        --docker-username=<registry user> --docker-password=<access token> \
        --docker-email=<registry email>
```

要测试密钥，请使用以下命令：

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

通过运行以下命令获取 Pod 的状态：

```console
$ kubectl get -n <kubernetes namespace> pods/dhi-test
```

该命令应返回以下结果：

```console
NAME       READY   STATUS      RESTARTS     AGE
dhi-test   0/1     Completed   ...          ...
```

如果结果如下所示，则密钥可能存在配置问题：

```console
NAME       READY   STATUS         RESTARTS   AGE
dhi-test   0/1     ErrImagePull   0          ...
```

运行以下命令查看 Pod 输出，应返回 `Hello from DHI in Kubernetes!`：

```console
kubectl logs -n <kubernetes namespace> pods/dhi-test
```

测试成功后，可以使用以下命令删除测试 Pod：

```console
$ kubectl delete -n <kubernetes namespace> pods/dhi-test
```
