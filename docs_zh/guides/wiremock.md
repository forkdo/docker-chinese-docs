---
title: 使用 WireMock 在开发和测试中模拟 API 服务
description: *desc 使用 WireMock 在开发和测试中模拟 API 服务
keywords: WireMock, 基于容器的开发
linktitle: 使用 WireMock 模拟 API 服务
summary: *desc
tags: [app-dev, distributed-systems]
languages: [js]
params:
  time: 20 分钟
---

在本地开发和测试过程中，经常会遇到应用依赖远程 API 的情况。网络问题、速率限制，甚至 API 提供者的停机都可能阻碍你的进度。这会显著影响你的效率，使测试变得更加困难。这时 WireMock 就派上用场了。

WireMock 是一个开源工具，帮助开发者创建模拟真实 API 行为的模拟服务器，为开发和测试提供可控的环境。

想象一下，你有一个 API 和一个前端应用，想要测试前端如何与 API 交互。使用 WireMock，你可以设置一个模拟服务器来模拟 API 的响应，让你无需依赖实际 API 即可测试前端行为。当 API 仍在开发中，或你想测试不同场景而不影响实际 API 时，这特别有用。WireMock 支持 HTTP 和 HTTPS 协议，可以模拟各种响应场景，包括延迟、错误和不同的 HTTP 状态码。

在本指南中，你将学习如何：

- 使用 Docker 启动 WireMock 容器。
- 在本地开发中使用模拟数据，不依赖外部 API。
- 在生产环境中使用实时 API 从 AccuWeather 获取实时天气数据。

## 使用 Docker 运行 WireMock

WireMock 的官方 [Docker 镜像](https://hub.docker.com/r/wiremock/wiremock) 提供了一种方便的方式来部署和管理 WireMock 实例。WireMock 支持多种 CPU 架构，包括 amd64、armv7 和 armv8，确保与不同设备和平台的兼容性。你可以在 [WireMock 文档网站](https://wiremock.org/docs/standalone/docker/) 了解更多关于 WireMock 独立运行的信息。

### 前置要求

要遵循本指南，需要满足以下前置条件：

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 启动 WireMock

按照以下步骤启动 WireMock 的快速演示：

 1. 在本地克隆 [GitHub 仓库](https://github.com/dockersamples/wiremock-node-docker)。

    ```console
    $ git clone https://github.com/dockersamples/wiremock-node-docker
    ```

 2. 导航到 `wiremock-endpoint` 目录

    ```console
    $ cd wiremock-node-docker/
    ```

    WireMock 作为你的后端将与之通信以检索数据的模拟 API。模拟 API 响应已预先创建在 mappings 目录中。

 3. 在克隆项目的根目录运行以下命令启动 Compose 栈：

    ```console
    $ docker compose up -d
    ```

    过一会儿，应用将启动并运行。

    ![显示在 Docker Desktop 上运行的 WireMock 容器的图表](./images/wiremock-using-docker.webp)

    你可以通过选择 `wiremock-node-docker` 容器查看日志：

    ![显示在 Docker Desktop 上运行的 WireMock 容器日志的图表](./images/wiremock-logs-docker-desktop.webp)

 4. 测试模拟 API。

    ```console
    $ curl http://localhost:8080/api/v1/getWeather\?city\=Bengaluru
    ```

    它将返回以下包含模拟数据的预设响应：

    ```plaintext
    {"city":"Bengaluru","temperature":27.1,"conditions":"Mostly cloudy","forecasts":[{"date":"2024-09-02T07:00:00+05:30","temperature":83,"conditions":"Partly sunny w/ t-storms"},{"date":"2024-09-03T07:00:00+05:30","temperature":83,"conditions":"Thunderstorms"},{"date":"2024-09-04T07:00:00+05:30","temperature":83,"conditions":"Intermittent clouds"},{"date":"2024-09-05T07:00:00+05:30","temperature":82,"conditions":"Dreary"},{"date":"2024-09-06T07:00:00+05:30","temperature":82,"conditions":"Dreary"}]}
    ```

    使用 WireMock，你可以使用映射文件定义预设响应。
    对于此请求，模拟数据在 JSON 文件中定义，位于
    `wiremock-endpoint/mappings/getWeather/getWeatherBengaluru.json`。
    
    有关模拟预设响应的更多信息，请参考
    [WireMock 文档](https://wiremock.org/docs/stubbing/)。

## 在开发中使用 WireMock

现在你已经尝试了 WireMock，让我们在开发和测试中使用它。在本例中，你将使用一个具有 Node.js 后端的示例应用。此应用栈的配置如下：

  - 本地开发环境：Node.js 后端和 WireMock 运行的上下文。
  - Node.js 后端：表示处理 HTTP 请求的后端应用。
  - 外部 AccuWeather API：从中获取实时天气数据的真实 API。
  - WireMock：在测试期间模拟 API 响应的模拟服务器。它作为 Docker 容器运行。

  ![显示开发中 WireMock 架构的图表](./images/wiremock-arch.webp)

  - 在开发中，Node.js 后端向 WireMock 发送请求，而不是实际的 AccuWeather API。
  - 在生产中，它直接连接到实时 AccuWeather API 获取真实数据。

## 在本地开发中使用模拟数据

让我们设置一个 Node 应用，向 WireMock 容器发送请求，而不是实际的 AccuWeather API。

### 前置要求

- 安装 [Node.js 和 npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- 确保 WireMock 容器已启动并运行（参见 [启动 WireMock](#launching-wiremock)

按照以下步骤设置非容器化的 Node 应用：

1. 导航到 `accuweather-api` 目录

   确保你在 `package.json` 文件所在的目录中。

2. 设置环境变量。

   打开 `accuweather-api/` 目录下的 `.env` 文件。删除旧条目，确保它只包含以下单行。

   ```plaintext
   API_ENDPOINT_BASE=http://localhost:8080
   ```

   这将告诉你的 Node.js 应用使用 WireMock 服务器进行 API 调用。

3. 检查应用入口点

   - 应用的主文件是 `index.js`，位于 `accuweather-api/src/api` 目录。
   - 此文件启动 `getWeather.js` 模块，这对你的 Node.js 应用至关重要。它使用 `dotenv` 包从 `.env` 文件加载环境变量。
   - 根据 `API_ENDPOINT_BASE` 的值，应用将请求路由到 WireMock 服务器（`http://localhost:8080`）或 AccuWeather API。在此设置中，它使用 WireMock 服务器。
   - 代码确保仅在应用不使用 WireMock 时才需要 `ACCUWEATHER_API_KEY`，提高效率并避免错误。

    ```javascript
    require("dotenv").config();

    const express = require("express");
    const axios = require("axios");

    const router = express.Router();
    const API_ENDPOINT_BASE = process.env.API_ENDPOINT_BASE;
    const API_KEY = process.env.ACCUWEATHER_API_KEY;

    console.log('API_ENDPOINT_BASE:', API_ENDPOINT_BASE);  // Log after it's defined
    console.log('ACCUWEATHER_API_KEY is set:', !!API_KEY); // Log boolean instead of actual key

    if (!API_ENDPOINT_BASE) {
      throw new Error("API_ENDPOINT_BASE is not defined in environment variables");
    }

    // Only check for API key if not using WireMock
    if (API_ENDPOINT_BASE !== 'http://localhost:8080' && !API_KEY) {
      throw new Error("ACCUWEATHER_API_KEY is not defined in environment variables");
    }
    // Function to fetch the location key for the city
    async function fetchLocationKey(townName) {
      const { data: locationData } = await
    axios.get(`${API_ENDPOINT_BASE}/locations/v1/cities/search`, {
        params: { q: townName, details: false, apikey: API_KEY },
      });
      return locationData[0]?.Key;
    }
    ```

4. 启动 Node 服务器

   在启动 Node 服务器之前，确保你已通过运行 `npm install` 安装了 `package.json` 文件中列出的节点包。

   ```console
   npm install 
   npm run start
   ```

   你应该看到以下输出：

    ```plaintext
    > express-api-starter@1.2.0 start
    > node src/index.js

    API_ENDPOINT_BASE: http://localhost:8080
    ..
    Listening: http://localhost:5001
    ```

   输出表明你的 Node 应用已成功启动。
   保持此终端窗口打开。

5. 测试模拟 API

   打开新的终端窗口，运行以下命令测试模拟 API：

   ```console
   $ curl "http://localhost:5001/api/v1/getWeather?city=Bengaluru"
   ```

   你应该看到以下输出：

   ```plaintext
   {"city":"Bengaluru","temperature":27.1,"conditions":"Mostly cloudy","forecasts":[{"date":"2024-09-02T07:00:00+05:30","temperature":83,"conditions":"Partly sunny w/ t-storms"},{"date":"2024-09-03T07:00:00+05:30","temperature":83,"conditions":"Thunderstorms"},{"date":"2024-09-04T07:00:00+05:30","temperature":83,"conditions":"Intermittent clouds"},{"date":"2024-09-05T07:00:00+05:30","temperature":82,"conditions":"Dreary"},{"date":"2024-09-06T07:00:00+05:30","temperature":82,"conditions":"Dreary"}]}%
   ```

   这表明你的 Node.js 应用现在已成功将请求路由到 WireMock 容器并接收模拟响应。

   你可能注意到你尝试使用 `http://localhost:5001` 而不是端口 `8080` 作为 URL。这是因为你的 Node.js 应用在端口 `5001` 上运行，它将请求路由到监听端口 `8080` 的 WireMock 容器。

   > [!TIP]
   > 在进入下一步之前，请确保停止 Node 应用服务。

## 在生产中使用实时 API 从 AccuWeather 获取实时天气数据

   为了增强你的 Node.js 应用的实时天气数据功能，你可以无缝集成 AccuWeather API。本指南的这一部分将引导你完成设置非容器化 Node.js 应用并直接从 AccuWeather API 获取天气信息的步骤。

1. 创建 AccuWeather API 密钥

   在 [https://developer.accuweather.com/](https://developer.accuweather.com/) 注册免费的 AccuWeather 开发者账户。在你的账户中，通过在顶部导航菜单选择 `MY APPS` 创建一个新应用以获取唯一的 API 密钥。

   ![显示 AccuWeather 仪表板的图表](images/wiremock-accuweatherapi.webp)

    [AccuWeather API](https://developer.accuweather.com/) 是一个提供实时天气数据和预报的 Web API。开发者可以在他们的应用、网站或其他项目中集成此 API 以获取天气信息。

2. 更改目录到 `accuweather-api`

   ```console
   $ cd accuweather-api
   ```

3. 使用 `.env` 文件设置你的 AccuWeather API 密钥：

   > [!TIP]
   > 为防止冲突，在修改 `.env` 文件之前，请确保删除任何名为 `API_ENDPOINT_BASE` 或 `ACCUWEATHER_API_KEY` 的现有环境变量。

   在终端运行以下命令：

   ```console
   unset API_ENDPOINT_BASE
   unset ACCUWEATHER_API_KEY
   ```

   现在是时候在 `.env` 文件中设置环境变量了：

   ```plaintext
   ACCUWEATHER_API_KEY=XXXXXX
   API_ENDPOINT_BASE=http://dataservice.accuweather.com
   ```

   确保用正确的值填充 `ACCUWEATHER_API_KEY`。

4. 安装依赖项

   运行以下命令安装所需包：

   ```console
   $ npm install
   ```

   这将安装 `package.json` 文件中列出的所有包。这些包对项目正确运行至关重要。

   如果你遇到与已弃用包相关的任何警告，目前可以忽略它们以进行此演示。

5. 假设你的系统上没有预先存在的 Node 服务器在运行，继续通过运行以下命令启动 Node 服务器：

   ```console
   $ npm run start
   ```

   你应该看到以下输出：

   ```plaintext
   > express-api-starter@1.2.0 start
   > node src/index.js

   API_ENDPOINT_BASE: http://dataservice.accuweather.com
   ACCUWEATHER_API_KEY is set: true 
   Listening: http://localhost:5001
   ```

   保持此终端窗口打开。

6. 运行 curl 命令向服务器 URL 发送 GET 请求。

   在新终端窗口中，输入以下命令：

   ```console
   $ curl "http://localhost:5000/api/v1/getWeather?city=Bengaluru"
   ```

   通过运行此命令，你本质上是在告诉你的本地服务器为你提供名为 `Bengaluru` 的城市的天气数据。请求专门针对 `/api/v1/getWeather` 端点，你提供查询参数 `city=Bengaluru`。执行命令后，服务器处理此请求，获取数据并将其作为响应返回，`curl` 将在你的终端中显示。

   当从外部 AccuWeather API 获取数据时，你正在与反映最新天气状况的实时数据交互。

## 回顾

本指南已引导你使用 Docker 设置 WireMock。你学会了如何创建模拟以模拟 API 端点，让你无需依赖外部服务即可开发和测试应用。通过使用 WireMock，你可以创建可靠且一致的测试环境，重现边缘情况，并加速开发工作流。