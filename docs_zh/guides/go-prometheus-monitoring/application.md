---
title: 构建应用程序
linkTitle: 了解应用程序
weight: 10 #
keywords: go, golang, prometheus, grafana, containerize, monitor
description: 学习如何创建一个 Golang 服务器，使用 Prometheus 注册指标。
---

## 前置条件

* 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但你可以使用任何客户端。

你将创建一个 Golang 服务器，并添加一些端点来模拟真实世界的应用程序。然后，你将使用 Prometheus 从服务器暴露指标。

## 获取示例应用程序

克隆示例应用程序以配合本指南使用。打开终端，将目录切换到你想要工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/dockersamples/go-prometheus-monitoring.git 
```

克隆完成后，你会在 `go-prometheus-monitoring` 目录中看到以下内容结构：

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
- **compose.yaml** - 启动所有服务的 Compose 文件（Golang 应用、Prometheus 和 Grafana）。
- **dashboard.json** - Grafana 仪表板配置文件。
- **Dockerfile** - 用于构建 Golang 应用的 Dockerfile。
- **compose.yaml** - 用于启动所有服务的 Docker Compose 文件（Golang 应用、Prometheus 和 Grafana）。
- 其他文件用于授权和文档。

## 了解应用程序

以下是应用程序的完整逻辑，你可以在 `main.go` 中找到：

```go
package main

import (
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

// 定义指标
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

// 自定义注册表（不包含默认的 Go 指标）
var customRegistry = prometheus.NewRegistry()

// 使用自定义注册表注册指标
func init() {
	customRegistry.MustRegister(HttpRequestTotal, HttpRequestErrorTotal)
}

func main() {
	router := gin.Default()

	// 在中间件之前注册 /metrics
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

// 使用自定义注册表的自定义指标处理器
func PrometheusHandler() gin.HandlerFunc {
	h := promhttp.HandlerFor(customRegistry, promhttp.HandlerOpts{})
	return func(c *gin.Context) {
		h.ServeHTTP(c.Writer, c.Request)
	}
}

// 记录传入请求指标的中间件
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

在这段代码中，你导入了所需的包 `gin`、`prometheus` 和 `promhttp`。然后定义了几个变量，`HttpRequestTotal` 和 `HttpRequestErrorTotal` 是 Prometheus 计数器指标，`customRegistry` 是一个自定义注册表，将用于注册这些指标。指标的名称是一个字符串，你可以用它来标识指标。帮助字符串是在你查询 `/metrics` 端点以了解指标时会显示的字符串。你使用自定义注册表的原因是为了避免 Prometheus 客户端默认注册的 Go 默认指标。然后使用 `init` 函数将指标注册到自定义注册表中。

```go
import (
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

// 定义指标
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

// 自定义注册表（不包含默认的 Go 指标）
var customRegistry = prometheus.NewRegistry()

// 使用自定义注册表注册指标
func init() {
	customRegistry.MustRegister(HttpRequestTotal, HttpRequestErrorTotal)
}
```

在 `main` 函数中，你创建了一个 `gin` 框架的新实例，并创建了三个路由。你可以看到健康检查端点位于路径 `/health`，它会返回一个包含 `{"message": "Up and running!"}` 的 JSON，以及 `/v1/users` 端点，它会返回一个包含 `{"message": "Hello from /v1/users"}` 的 JSON。第三个路由是 `/metrics` 端点，它会以 Prometheus 格式返回指标。然后你有了 `RequestMetricsMiddleware` 中间件，它会在每次对 API 的请求时被调用。它会记录传入请求的指标，如状态码和路径。最后，你在端口 8000 上运行 gin 应用。

```golang
func main() {
	router := gin.Default()

	// 在中间件之前注册 /metrics
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

现在来看中间件函数 `RequestMetricsMiddleware`。这个函数会在每次对 API 的请求时被调用。如果状态码小于 400，它会增加 `HttpRequestTotal` 计数器（不同路径和状态码对应不同的计数器）。如果状态码大于等于 400，它会增加 `HttpRequestErrorTotal` 计数器（不同路径和状态码对应不同的计数器）。`PrometheusHandler` 函数是自定义处理器，会在 `/metrics` 端点被调用时执行。它会以 Prometheus 格式返回指标。

```golang
// 使用自定义注册表的自定义指标处理器
func PrometheusHandler() gin.HandlerFunc {
	h := promhttp.HandlerFor(customRegistry, promhttp.HandlerOpts{})
	return func(c *gin.Context) {
		h.ServeHTTP(c.Writer, c.Request)
	}
}

// 记录传入请求指标的中间件
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

就是这样，这就是应用程序的完整要点。现在是时候运行并测试应用程序是否正确注册了指标。

## 运行应用程序

确保你仍在终端中的 `go-prometheus-monitoring` 目录中，然后运行以下命令。通过运行 `go mod tidy` 安装依赖项，然后通过运行 `go run main.go` 构建并运行应用程序。然后访问 `http://localhost:8000/health` 或 `http://localhost:8000/v1/users`。你应该看到输出 `{"message": "Up and running!"}` 或 `{"message": "Hello from /v1/users"}`。如果你能看到这个，那么你的应用程序已成功启动并运行。

现在，通过访问 `/metrics` 端点来检查应用程序的指标。在浏览器中打开 `http://localhost:8000/metrics`。你应该看到类似以下的输出。

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
> 如果你不想在本地运行应用程序，而想在 Docker 容器中运行，请跳到下一页，在那里你将创建一个 Dockerfile 并容器化应用程序。

## 总结

在本节中，你学习了如何创建一个 Golang 应用程序，使用 Prometheus 注册指标。通过实现中间件函数，你能够根据请求路径和状态码增加计数器。

## 下一步

在下一节中，你将学习如何容器化你的应用程序。