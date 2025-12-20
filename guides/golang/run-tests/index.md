# 使用 Go test 运行测试

## 前提条件

完成本指南的 [构建 Go 镜像](build-images.md) 部分。

## 概述

测试是现代软件开发中不可或缺的一部分。对于不同的开发团队，测试可能意味着很多不同的内容，包括单元测试、集成测试和端到端测试。在本指南中，您将了解如何在构建时在 Docker 中运行单元测试。

在本节中，请使用您在 [构建 Go 镜像](build-images.md) 中克隆的 `docker-gs-ping` 项目。

## 在构建时运行测试

要在构建时运行测试，您需要向 `Dockerfile.multistage` 添加一个测试阶段。示例应用程序仓库中的 `Dockerfile.multistage` 已包含以下内容：

```dockerfile {hl_lines="15-17"}
# syntax=docker/dockerfile:1

# 从源代码构建应用程序
FROM golang:1.19 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY *.go ./

RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# 在容器中运行测试
FROM build-stage AS run-test-stage
RUN go test -v ./...

# 将应用程序二进制文件部署到精简镜像中
FROM gcr.io/distroless/base-debian11 AS build-release-stage

WORKDIR /

COPY --from=build-stage /docker-gs-ping /docker-gs-ping

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/docker-gs-ping"]
```

运行以下命令，使用 `run-test-stage` 阶段作为目标来构建镜像，并查看测试结果。包含 `--progress plain` 以查看构建输出，`--no-cache` 以确保始终运行测试，以及 `--target run-test-stage` 以针对测试阶段。

```console
$ docker build -f Dockerfile.multistage -t docker-gs-ping-test --progress plain --no-cache --target run-test-stage .
```

您应该会看到包含以下内容的输出：

```text
#13 [run-test-stage 1/1] RUN go test -v ./...
#13 4.915 === RUN   TestIntMinBasic
#13 4.915 --- PASS: TestIntMinBasic (0.00s)
#13 4.915 === RUN   TestIntMinTableDriven
#13 4.915 === RUN   TestIntMinTableDriven/0,1
#13 4.915 === RUN   TestIntMinTableDriven/1,0
#13 4.915 === RUN   TestIntMinTableDriven/2,-2
#13 4.915 === RUN   TestIntMinTableDriven/0,-1
#13 4.915 === RUN   TestIntMinTableDriven/-1,0
#13 4.915 --- PASS: TestIntMinTableDriven (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/0,1 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/1,0 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/2,-2 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/0,-1 (0.00s)
#13 4.915     --- PASS: TestIntMinTableDriven/-1,0 (0.00s)
#13 4.915 PASS
```

## 下一步

在本节中，您学习了如何在构建镜像时运行测试。接下来，您将学习如何使用 GitHub Actions 设置 CI/CD 流水线。
