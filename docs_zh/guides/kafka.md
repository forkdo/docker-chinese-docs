---
description: 使用 Kafka 和 Docker 开发事件驱动应用程序
keywords: kafka, container-supported development
title: 使用 Kafka 和 Docker 开发事件驱动应用程序
linktitle: 使用 Kafka 的事件驱动应用程序
summary: |
  本指南解释了如何在 Docker 容器中运行 Apache Kafka。
tags: [distributed-systems]
languages: [js]
aliases:
  - /guides/use-case/kafka/
params:
  time: 20 minutes
---

随着微服务的兴起，事件驱动架构变得越来越流行。[Apache Kafka](https://kafka.apache.org/) 是一个分布式事件流平台，通常是这些架构的核心。不幸的是，为开发设置和部署自己的 Kafka 实例往往很棘手。幸运的是，Docker 和容器使这变得容易得多。

在本指南中，您将学习如何：

1. 使用 Docker 启动 Kafka 集群
2. 将非容器化应用连接到集群
3. 将容器化应用连接到集群
4. 部署 Kafka-UI 以帮助故障排除和调试

## 先决条件

遵循本指南需要满足以下先决条件：

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js](https://nodejs.org/en/download/package-manager) 和 [yarn](https://yarnpkg.com/)
- Kafka 和 Docker 的基础知识

## 启动 Kafka

从 [Kafka 3.3](https://www.confluent.io/blog/apache-kafka-3-3-0-new-features-and-updates/) 开始，由于 KRaft（Kafka Raft）的引入，Kafka 的部署得到了极大简化，不再需要 Zookeeper。借助 KRaft，为本地开发设置 Kafka 实例变得更加容易。从 [Kafka 3.8](https://www.confluent.io/blog/introducing-apache-kafka-3-8/) 发布开始，现在提供了一个新的 [kafka-native](https://hub.docker.com/r/apache/kafka-native) Docker 镜像，提供了更快的启动速度和更低的内存占用。

> [!TIP]
>
> 本指南将使用 apache/kafka 镜像，因为它包含了许多有助于管理和使用 Kafka 的脚本。但是，您可能希望使用 apache/kafka-native 镜像，因为它启动更快且需要更少的资源。

### 启动 Kafka

按照以下步骤启动基本的 Kafka 集群。此示例将启动一个集群，将端口 9092 暴露到主机，以便本地运行的应用程序连接到它。

1. 通过运行以下命令启动 Kafka 容器：

   ```console
   $ docker run -d --name=kafka -p 9092:9092 apache/kafka
   ```

2. 镜像拉取完成后，您将在一两秒内拥有一个启动并运行的 Kafka 实例。

3. apache/kafka 镜像在 `/opt/kafka/bin` 目录中附带了几个有用的脚本。运行以下命令以验证集群已启动并运行并获取其集群 ID：

   ```console
   $ docker exec -ti kafka /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server :9092
   ```

   执行后将产生类似以下的输出：

   ```plaintext
   Cluster ID: 5L6g3nShT-eMCtK--X86sw
   ```

4. 创建一个示例主题并生成（或发布）几条消息，运行以下命令：

   ```console
   $ docker exec -ti kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server :9092 --topic demo
   ```

   运行后，您可以逐行输入消息。例如，输入几条消息，每行一条。一些示例可能是：

   ```plaintext
   First message
   ```

   以及

   ```plaintext
   Second message
   ```

   按 `enter` 发送最后一条消息，完成后按 ctrl+c。消息将发布到 Kafka。

5. 通过消费消息来确认消息已发布到集群：

   ```console
   $ docker exec -ti kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server :9092 --topic demo --from-beginning
   ```

   您应该在输出中看到您的消息：

   ```plaintext
   First message
   Second message
   ```

   如果需要，您可以打开另一个终端并发布更多消息，查看它们出现在消费者中。

   完成后，按 ctrl+c 停止消费消息。

您现在拥有一个本地运行的 Kafka 集群，并已验证可以连接到它。

## 从非容器化应用连接到 Kafka

现在您已经展示了可以从命令行连接到 Kafka 实例，是时候从应用程序连接到集群了。在本示例中，您将使用一个简单的 Node 项目，它使用 [KafkaJS](https://github.com/tulios/kafkajs) 库。

由于集群在本地运行并在端口 9092 上暴露，应用可以在 localhost:9092 连接到集群（因为它现在是本地运行而不是在容器中）。连接后，此示例应用将记录从 `demo` 主题消费的消息。此外，当它在开发模式下运行时，如果主题不存在，它还会创建该主题。

1. 如果您没有从上一步运行 Kafka 集群，运行以下命令启动 Kafka 实例：

   ```console
   $ docker run -d --name=kafka -p 9092:9092 apache/kafka
   ```

2. 在本地克隆 [GitHub 仓库](https://github.com/dockersamples/kafka-development-node)。

   ```console
   $ git clone https://github.com/dockersamples/kafka-development-node.git
   ```

3. 导航到项目。

   ```console
   cd kafka-development-node/app
   ```

4. 使用 yarn 安装依赖项。

   ```console
   $ yarn install
   ```

5. 使用 `yarn dev` 启动应用。这将设置 `NODE_ENV` 环境变量为 `development` 并使用 `nodemon` 监视文件更改。

   ```console
   $ yarn dev
   ```

6. 应用现在运行，它将把接收到的消息记录到控制台。在新终端中，使用以下命令发布几条消息：

   ```console
   $ docker exec -ti kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server :9092 --topic demo
   ```

   然后向集群发送一条消息：

   ```plaintext
   Test message
   ```

   记住完成后按 `ctrl+c` 停止生成消息。

## 从容器和本地应用连接到 Kafka

现在您已经有一个应用通过暴露的端口连接到 Kafka，是时候探索从另一个容器连接到 Kafka 需要哪些更改。为此，您现在将从容器而不是本地运行应用。

但在这样做之前，了解 Kafka 监听器的工作原理以及这些监听器如何帮助客户端连接是很重要的。

### 理解 Kafka 监听器

当客户端连接到 Kafka 集群时，它实际上连接到一个“代理”。虽然代理有很多角色，但其中之一是支持客户端的负载均衡。当客户端连接时，代理返回一组客户端应使用的连接 URL，以便客户端连接以生成或消费消息。这些连接 URL 是如何配置的？

每个 Kafka 实例都有一组监听器和广告监听器。“监听器”是 Kafka 绑定的内容，而“广告监听器”配置客户端应如何连接到集群。客户端接收到的连接 URL 基于客户端连接到的监听器。

### 定义监听器

为了更好地理解这一点，让我们看看 Kafka 需要如何配置以支持两种连接机会：

1. 主机连接（通过主机映射端口传入的连接）- 这些需要使用 localhost 连接
2. Docker 连接（来自 Docker 网络内部的连接）- 这些不能使用 localhost 连接，但可以使用 Kafka 服务的网络别名（或 DNS 地址）

由于客户端有两种不同的连接方法，需要两个不同的监听器 - `HOST` 和 `DOCKER`。`HOST` 监听器将告诉客户端使用 localhost:9092 连接，而 `DOCKER` 监听器将通知客户端使用 `kafka:9093` 连接。注意这意味着 Kafka 在端口 9092 和 9093 上监听。但是，只有主机监听器需要暴露给主机。

![显示 DOCKER 和 HOST 监听器的图表，以及它们如何暴露给主机和 Docker 网络](./images/kafka-1.webp)

为了设置这个，Kafka 的 `compose.yaml` 需要一些额外的配置。一旦您开始覆盖一些默认值，您还需要指定一些其他选项以使 KRaft 模式工作。

```yaml
services:
  kafka:
    image: apache/kafka-native
    ports:
      - "9092:9092"
    environment:
      # Configure listeners for both docker and host communication
      KAFKA_LISTENERS: CONTROLLER://localhost:9091,HOST://0.0.0.0:9092,DOCKER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: HOST://localhost:9092,DOCKER://kafka:9093
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,DOCKER:PLAINTEXT,HOST:PLAINTEXT

      # Settings required for KRaft mode
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9091

      # Listener to use for broker-to-broker communication
      KAFKA_INTER_BROKER_LISTENER_NAME: DOCKER

      # Required for a single node cluster
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

按照以下步骤尝试一下。

1. 如果您从上一步运行了 Node 应用，继续按 `ctrl+c` 在终端中停止它。

2. 如果您从上一节运行了 Kafka 集群，继续使用以下命令停止该容器：

   ```console
   $ docker rm -f kafka
   ```

3. 通过在克隆项目的根目录运行以下命令启动 Compose 栈：

   ```console
   $ docker compose up
   ```

   一会儿后，应用将启动并运行。

4. 栈中有另一个可以用来发布消息的服务。通过转到 [http://localhost:3000](http://localhost:3000) 打开它。当您输入消息并提交表单时，您应该看到应用接收到消息的日志消息。

   这有助于演示容器化方法如何使添加额外服务变得容易，以帮助测试和调试您的应用。

## 添加集群可视化

一旦您开始在开发环境中使用容器，您就会意识到添加额外服务的便利性，这些服务专门专注于帮助开发，比如可视化器和其他支持服务。由于您已经运行了 Kafka，可视化 Kafka 集群中发生的事情可能会有所帮助。为此，您可以运行 [Kafbat UI web application](https://github.com/kafbat/kafka-ui)。

要将其添加到您自己的项目中（它已经在演示应用中），您只需要在 Compose 文件中添加以下配置：

```yaml
services:
  kafka-ui:
    image: kafbat/kafka-ui:main
    ports:
      - 8080:8080
    environment:
      DYNAMIC_CONFIG_ENABLED: "true"
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9093
    depends_on:
      - kafka
```

然后，一旦 Compose 栈启动，您就可以在浏览器中打开 [http://localhost:8080](http://localhost:8080) 并浏览以查看有关集群的更多详细信息，检查消费者，发布测试消息等。

## 使用 Kafka 进行测试

如果您有兴趣了解如何轻松地将 Kafka 集成到集成测试中，请查看 [使用 Testcontainers 测试 Spring Boot Kafka 监听器指南](https://testcontainers.com/guides/testing-spring-boot-kafka-listener-using-testcontainers/)。本指南将教您如何使用 Testcontainers 管理测试中 Kafka 容器的生命周期。

## 结论

通过使用 Docker，您可以简化使用 Kafka 开发和测试事件驱动应用程序的过程。容器简化了设置和部署各种服务以进行开发的过程。一旦它们在 Compose 中定义，团队中的每个人都可以受益于易用性。

如果您之前错过了，所有示例应用代码都可以在 dockersamples/kafka-development-node 找到。