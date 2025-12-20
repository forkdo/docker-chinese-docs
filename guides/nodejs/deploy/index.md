# 部署你的 Node.js 应用

## 前置条件

- 完成本指南的所有前面章节，从 [容器化 Node.js 应用](containerize.md) 开始。
- 在 Docker Desktop 中[启用 Kubernetes](/manuals/desktop/use-desktop/kubernetes.md#enable-kubernetes)。

## 概述

在本节中，你将学习如何使用 Docker Desktop 将容器化的 Node.js 应用部署到 Kubernetes。此部署使用生产就绪的配置，包括安全加固、自动扩展、持久化存储和高可用性功能。

你将部署一个完整的栈，包括：

- Node.js Todo 应用，3 个副本。
- PostgreSQL 数据库，带有持久化存储。
- 基于 CPU 和内存使用率的自动扩展。
- 入口配置以供外部访问。
- 安全设置。

## 创建 Kubernetes 部署文件

在项目根目录创建一个新文件 `nodejs-sample-kubernetes.yaml`：

```yaml
# ========================================
# Node.js Todo App - Kubernetes Deployment
# ========================================

apiVersion: v1
kind: Namespace
metadata:
  name: todoapp
  labels:
    app: todoapp

---
# ========================================
# ConfigMap for Application Configuration
# ========================================
apiVersion: v1
kind: ConfigMap
metadata:
  name: todoapp-config
  namespace: todoapp
data:
  NODE_ENV: 'production'
  ALLOWED_ORIGINS: 'https://yourdomain.com'
  POSTGRES_HOST: 'todoapp-postgres'
  POSTGRES_PORT: '5432'
  POSTGRES_DB: 'todoapp'
  POSTGRES_USER: 'todoapp'

---
# ========================================
# Secret for Database Credentials
# ========================================
apiVersion: v1
kind: Secret
metadata:
  name: todoapp-secrets
  namespace: todoapp
type: Opaque
data:
  postgres-password: dG9kb2FwcF9wYXNzd29yZA== # base64 encoded "todoapp_password"

---
# ========================================
# PostgreSQL PersistentVolumeClaim
# ========================================
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: todoapp
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard

---
# ========================================
# PostgreSQL Deployment
# ========================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todoapp-postgres
  namespace: todoapp
  labels:
    app: todoapp-postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todoapp-postgres
  template:
    metadata:
      labels:
        app: todoapp-postgres
    spec:
      containers:
        - name: postgres
          image: postgres:18-alpine
          ports:
            - containerPort: 5432
              name: postgres
          env:
            - name: POSTGRES_DB
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: POSTGRES_DB
            - name: POSTGRES_USER
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: POSTGRES_USER
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: todoapp-secrets
                  key: postgres-password
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql
          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - todoapp
                - -d
                - todoapp
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - todoapp
                - -d
                - todoapp
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc

---
# ========================================
# PostgreSQL Service
# ========================================
apiVersion: v1
kind: Service
metadata:
  name: todoapp-postgres
  namespace: todoapp
  labels:
    app: todoapp-postgres
spec:
  type: ClusterIP
  ports:
    - port: 5432
      targetPort: 5432
      protocol: TCP
      name: postgres
  selector:
    app: todoapp-postgres

---
# ========================================
# Application Deployment
# ========================================
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todoapp-deployment
  namespace: todoapp
  labels:
    app: todoapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: todoapp
  template:
    metadata:
      labels:
        app: todoapp
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 1001
      containers:
        - name: todoapp
          image: ghcr.io/your-username/docker-nodejs-sample:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 3000
              name: http
              protocol: TCP
          env:
            - name: NODE_ENV
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: NODE_ENV
            - name: ALLOWED_ORIGINS
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: ALLOWED_ORIGINS
            - name: POSTGRES_HOST
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: POSTGRES_HOST
            - name: POSTGRES_PORT
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: POSTGRES_PORT
            - name: POSTGRES_DB
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: POSTGRES_DB
            - name: POSTGRES_USER
              valueFrom:
                configMapKeyRef:
                  name: todoapp-config
                  key: POSTGRES_USER
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: todoapp-secrets
                  key: postgres-password
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            requests:
              memory: '256Mi'
              cpu: '250m'
            limits:
              memory: '512Mi'
              cpu: '500m'
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL

---
# ========================================
# Application Service
# ========================================
apiVersion: v1
kind: Service
metadata:
  name: todoapp-service
  namespace: todoapp
  labels:
    app: todoapp
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 80
      targetPort: 3000
      protocol: TCP
  selector:
    app: todoapp

---
# ========================================
# Ingress for External Access
# ========================================
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todoapp-ingress
  namespace: todoapp
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: 'letsencrypt-prod'
spec:
  tls:
    - hosts:
        - yourdomain.com
      secretName: todoapp-tls
  rules:
    - host: yourdomain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: todoapp-service
                port:
                  number: 80

---
# ========================================
# HorizontalPodAutoscaler
# ========================================
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todoapp-hpa
  namespace: todoapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todoapp-deployment
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80

---
# ========================================
# PodDisruptionBudget
# ========================================
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: todoapp-pdb
  namespace: todoapp
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: todoapp
```

## 配置部署

在部署之前，你需要根据你的环境自定义部署文件：

1. **镜像引用**：将 `your-username` 替换为你的 GitHub 用户名或 Docker Hub 用户名：

   ```yaml
   image: ghcr.io/your-username/docker-nodejs-sample:latest
   ```

2. **域名**：在两个地方将 `yourdomain.com` 替换为你的实际域名：

   ```yaml
   # In ConfigMap
   ALLOWED_ORIGINS: "https://yourdomain.com"

   # In Ingress
   - host: yourdomain.com
   ```

3. **数据库密码**（可选）：默认密码已经 base64 编码。如需更改：

   ```console
   $ echo -n "your-new-password" | base64
   ```

   然后更新 Secret：

   ```yaml
   data:
     postgres-password: <your-base64-encoded-password>
   ```

4. **存储类**：根据你的集群调整（当前：`standard`）

## 理解部署

部署文件创建了一个完整的应用栈，多个组件协同工作。

### 架构

部署包括：

- **Node.js 应用**：运行 3 个副本的容器化 Todo 应用
- **PostgreSQL 数据库**：单实例，带有 10Gi 的持久化存储
- **服务**：Kubernetes 服务处理应用副本间的负载均衡
- **入口**：通过入口控制器和 SSL/TLS 支持进行外部访问

### 安全

部署使用了多项安全功能：

- 容器以非 root 用户（UID 1001）运行
- 只读根文件系统防止未授权写入
- Linux 权限被丢弃以最小化攻击面
- 敏感数据如数据库密码存储在 Kubernetes secrets 中

### 高可用

为保持应用可靠运行：

- 三个应用副本确保一个 pod 失败时服务继续
- Pod 破坏预算在更新期间保持至少一个可用 pod
- 滚动更新允许零停机时间部署
- `/health` 端点的健康检查确保只有健康的 pod 接收流量

### 自动扩展

水平 Pod 自动扩展器根据资源使用情况扩展应用：

- 在 1 到 5 个副本间自动扩展
- CPU 使用率超过 70% 时触发扩展
- 内存使用率超过 80% 时触发扩展
- 资源限制：每个 pod 256Mi-512Mi 内存，250m-500m CPU

### 数据持久化

PostgreSQL 数据持久化存储：

- 10Gi 持久化卷存储数据库文件
- 数据库在首次启动时自动初始化
- 数据在 pod 重启和更新期间保持

## 部署你的应用

### 步骤 1：部署到 Kubernetes

将应用部署到本地 Kubernetes 集群：

```console
$ kubectl apply -f nodejs-sample-kubernetes.yaml
```

你应该看到确认所有资源已创建的输出：

```shell
namespace/todoapp created
secret/todoapp-secrets created
configmap/todoapp-config created
persistentvolumeclaim/postgres-pvc created
deployment.apps/todoapp-postgres created
service/todoapp-postgres created
deployment.apps/todoapp-deployment created
service/todoapp-service created
ingress.networking.k8s.io/todoapp-ingress created
poddisruptionbudget.policy/todoapp-pdb created
horizontalpodautoscaler.autoscaling/todoapp-hpa created
```

### 步骤 2：验证部署

检查部署是否正在运行：

```console
$ kubectl get deployments -n todoapp
```

预期输出：

```shell
NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
todoapp-deployment   3/3     3            3           30s
todoapp-postgres     1/1     1            1           30s
```

验证服务已创建：

```console
$ kubectl get services -n todoapp
```

预期输出：

```shell
NAME               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
todoapp-service    ClusterIP   10.111.101.229   <none>        80/TCP     45s
todoapp-postgres   ClusterIP   10.111.102.130   <none>        5432/TCP   45s
```

检查持久化存储是否正常工作：

```console
$ kubectl get pvc -n todoapp
```

预期输出：

```shell
NAME           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
postgres-pvc   Bound    pvc-12345678-1234-1234-1234-123456789012   10Gi       RWO            standard       1m
```

### 步骤 3：访问你的应用

对于本地测试，使用端口转发访问应用：

```console
$ kubectl port-forward -n todoapp service/todoapp-service 8080:80
```

在浏览器中访问 [http://localhost:8080](http://localhost:8080) 查看在 Kubernetes 中运行的 Todo 应用。

### 步骤 4：测试部署

测试应用是否正确工作：

1. **通过 Web 界面添加一些待办事项**
2. **检查应用 pod**：

   ```console
   $ kubectl get pods -n todoapp -l app=todoapp
   ```

3. **查看应用日志**：

   ```console
   $ kubectl logs -f deployment/todoapp-deployment -n todoapp
   ```

4. **检查数据库连接性**：

   ```console
   $ kubectl get pods -n todoapp -l app=todoapp-postgres
   ```

5. **监控自动扩展**：
   ```console
   $ kubectl describe hpa todoapp-hpa -n todoapp
   ```

### 步骤 5：清理

测试完成后，删除部署：

```console
$ kubectl delete -f nodejs-sample-kubernetes.yaml
```

## 总结

你已将容器化的 Node.js 应用部署到 Kubernetes。你学会了如何：

- 创建带有安全加固的全面 Kubernetes 部署文件
- 部署多层应用（Node.js + PostgreSQL）并配置持久化存储
- 配置自动扩展、健康检查和高可用性功能
- 使用 Docker Desktop 的 Kubernetes 在本地测试和监控部署

你的应用现在运行在具有企业级功能的生产就绪环境中，包括安全上下文、资源管理和自动扩展。

---

## 相关资源

探索官方参考和最佳实践，以提升你的 Kubernetes 部署工作流：

- [Kubernetes 文档](https://kubernetes.io/docs/home/) – 了解核心概念、工作负载、服务等。
- [使用 Docker Desktop 部署到 Kubernetes](/manuals/desktop/use-desktop/kubernetes.md) – 使用 Docker Desktop 的内置 Kubernetes 支持进行本地测试和开发。
- [`kubectl` CLI 参考](https://kubernetes.io/docs/reference/kubectl/) – 从命令行管理 Kubernetes 集群。
- [Kubernetes Deployment 资源](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) – 了解如何使用部署管理扩展应用。
- [Kubernetes Service 资源](https://kubernetes.io/docs/concepts/services-networking/service/) – 了解如何将应用暴露给内部和外部流量。
