---
title: 构建应用程序
linkTitle: 了解应用程序
weight: 10
keywords: go, golang, prometheus, grafana, containerize, monitor
description: 学习如何创建一个 Golang 服务器来向 Prometheus 注册指标。
---

## 先决条件

* 您拥有一个 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 Git 客户端，但您可以使用任何客户端。

您将创建一个带有一些端点的 Golang 服务器来模拟真实的应用程序。然后，您将使用 Prometheus 从服务器暴露指标。

## 获取示例应用程序

克隆示例应用程序以配合本指南使用。打开终端，切换到您想要工作的目录，然后运行以下命令来克隆仓库：

```console
$ git clone https://github.com/dockersamples/go-prometheus-monitoring.git 
```

克隆完成后，您将在 `go-prometheus-monitoring` 目录中看到以下内容结构：

```text
go-prometheus-monitoring
├── CONTRIBUTING.md
├── Docker
│   ├── grafana.yml
│   └── prometheus.yml
├── dashboard.json
├── Dockerfile
├── LICENSE
├── README.md
├── compose.yaml
├── go.mod
├── go.sum
└── main.go
```

- **main.go** - 应用程序的入口点。
- **go.mod 和 go.sum** - Go 模块文件。
- **Dockerfile** - 用于构建应用程序的 Dockerfile。
- **Docker/** - 包含 Grafana 和 Prometheus 的 Docker Compose 配置文件。
- **compose.yaml** - 用于启动所有内容（Golang 应用程序、Prometheus 和 Grafana）的 Compose 文件。
- **dashboard.json** - Grafana 仪表板配置文件。
- **Dockerfile** - 用于构建 Golang 应用程序的 Dockerfile。
- **compose.yaml** - 用于启动所有内容（Golang 应用程序、Prometheus 和 Grafana）的 Docker Compose 文件。
- 其他文件用于许可和文档目的。

## 了解应用程序

以下是您将在 `main.go` 中找到的应用程序的完整逻辑。

```go
package main

import (
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

// Define metrics
var (
	HttpRequestTotal = prometheus.NewCounterVec(prometheus.CounterOpts{
		Name: "api_http_request_total",
		Help: "Total number of requests processed by the API",
	}, []string{"path", "status"})

	HttpRequestErrorTotal = prometheus.NewCounterVec(prometheus.CounterOpts{
		Name: "api_http_request_error_total",
		Help: "Total number of errors returned by the API",
	}, []string{"path", "status"})
)

// Custom registry (without default Go metrics)
var customRegistry = prometheus.NewRegistry()

// Register metrics with custom registry
func init() {
	customRegistry.MustRegister(HttpRequestTotal, HttpRequestErrorTotal)
}

func main() {
	router := gin.Default()

	// Register /metrics before middleware
	router.GET("/metrics", PrometheusHandler())
	
	router.Use(RequestMetricsMiddleware())
	router.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "Up and running!",
		})
	})
	router.GET("/v1/users", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "Hello from /v1/users",
		})
	})

	router.Run(":8000")
}

// Custom metrics handler with custom registry
func PrometheusHandler() gin.HandlerFunc {
	h := promhttp.HandlerFor(customRegistry, promhttp.HandlerOpts{})
	return func(c *gin.Context) {
		h.ServeHTTP(c.Writer, c.Request)
	}
}

// Middleware to record incoming requests metrics
func RequestMetricsMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		path := c.Request.URL.Path
		c.Next()
		status := c.Writer.Status()
		if status < 400 {
			HttpRequestTotal.WithLabelValues(path, strconv.Itoa(status)).Inc()
		} else {
			HttpRequestErrorTotal.WithLabelValues(path, strconv.Itoa(status)).Inc()
		}
	}
}
```

在这部分代码中，您导入了所需的包 `gin`、`prometheus` 和 `promhttp`。然后您定义了几个变量，`HttpRequestTotal` 和 `HttpRequestErrorTotal` 是 Prometheus 计数器指标，`customRegistry` 是一个自定义注册表，将用于注册这些指标。指标名称是一个字符串，可用于标识该指标。帮助字符串是在您查询 `/metrics` 端点以了解该指标时将显示的字符串。您使用自定义注册表的原因是为了避免 Prometheus 客户端默认注册的 Go 默认指标。然后使用 `init` 函数将指标注册到自定义注册表中。

```go
import (
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

// Define metrics
var (
	HttpRequestTotal = prometheus.NewCounterVec(prometheus.CounterOpts{
		Name: "api_http_request_total",
		Help: "Total number of requests processed by the API",
	}, []string{"path", "status"})

	HttpRequestErrorTotal = prometheus.NewCounterVec(prometheus.CounterOpts{
		Name: "api_http_request_error_total",
		Help: "Total number of errors returned by the API",
	}, []string{"path", "status"})
)

// Custom registry (without default Go metrics)
var customRegistry = prometheus.NewRegistry()

// Register metrics with custom registry
func init() {
	customRegistry.MustRegister(HttpRequestTotal, HttpRequestErrorTotal)
}
```

在 `main` 函数中，您创建了一个 `gin` 框架的新实例，并创建了三个路由。您可以看到健康检查端点位于路径 `/health`，它将返回一个包含 `{"message": "Up and running!"}` 的 JSON，以及 `/v1/users` 端点，它将返回一个包含 `{"message": "Hello from /v1/users"}` 的 JSON。第三个路由是用于 `/metrics` 端点的，它将以 Prometheus 格式返回指标。然后您有 `RequestMetricsMiddleware` 中间件，它将被对 API 的每个请求调用。它将记录传入请求的指标，如状态码和路径。最后，您将在端口 8000 上运行 gin 应用程序。

```golang
func main() {
	router := gin.Default()

	// Register /metrics before middleware
	router.GET("/metrics", PrometheusHandler())
	
	router.Use(RequestMetricsMiddleware())
	router.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "Up and running!",
		})
	})
	router.GET("/v1/users", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "Hello from /v1/users",
		})
	})

	router.Run(":8000")
}
```

现在来看中间件函数 `RequestMetricsMiddleware`。这个函数会被对 API 的每个请求调用。如果状态码小于 400，它会增加 `HttpRequestTotal` 计数器（不同路径和状态码使用不同的计数器）。如果状态码大于 400，它会增加 `HttpRequestErrorTotal` 计数器（不同路径和状态码使用不同的计数器）。`PrometheusHandler` 函数是将为 `/metrics` 端点调用的自定义处理程序。它将以 Prometheus 格式返回指标。

```golang
// Custom metrics handler with custom registry
func PrometheusHandler() gin.HandlerFunc {
	h := promhttp.HandlerFor(customRegistry, promhttp.HandlerOpts{})
	return func(c *gin.Context) {
		h.ServeHTTP(c.Writer, c.Request)
	}
}

// Middleware to record incoming requests metrics
func RequestMetricsMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		path := c.Request.URL.Path
		c.Next()
		status := c.Writer.Status()
		if status < 400 {
			HttpRequestTotal.WithLabelValues(path, strconv.Itoa(status)).Inc()
		} else {
			HttpRequestErrorTotal.WithLabelValues(path, strconv.Itoa(status)).Inc()
		}
	}
}
```

就是这样，这就是应用程序的完整要点。现在是时候运行并测试应用程序是否正确注册指标了。

## 运行应用程序

确保您仍在终端的 `go-prometheus-monitoring` 目录中，然后运行以下命令。通过运行 `go mod tidy` 安装依赖项，然后通过运行 `go run main.go` 构建并运行应用程序。然后访问 `http://localhost:8000/health` 或 `http://localhost:8000/v1/users`。您应该会看到输出 `{"message": "Up and running!"}` 或 `{"message": "Hello from /v1/users"}`。如果您能看到这些，说明您的应用程序已成功启动并运行。

现在，通过访问 `/metrics` 端点检查您的应用程序指标。
在浏览器中打开 `http://localhost:8000/metrics`。您应该会看到类似于以下内容的输出。

```sh
# HELP api_http_request_error_total Total number of errors returned by the API
# TYPE api_http_request_error_total counter
api_http_request_error_total{path="/",status="404"} 1
api_http_request_error_total{path="//v1/users",status="404"} 1
api_http_request_error_total{path="/favicon.ico",status="404"} 1
# HELP api_http_request_total Total number of requests processed by the API
# TYPE api_http_request_total counter
api_http_request_total{path="/health",status="200"} 2
api_http_request_total{path="/v1/users",status="200"} 1
```

在终端中，按 `ctrl` + `c` 停止应用程序。

> [!Note]
> 如果您不想在本地运行应用程序，而是想在 Docker 容器中运行，请跳到下一页，您将在那里创建 Dockerfile 并容器化应用程序。

## 总结

在本节中，您学习了如何创建一个 Golang 应用程序来向 Prometheus 注册指标。通过实现中间件函数，您能够根据请求路径和状态码增加计数器。

## 下一步

在下一节中，您将学习如何容器化您的应用程序。