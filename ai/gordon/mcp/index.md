# Model Context Protocol (MCP)


[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) 是一种开放协议，用于标准化应用程序向大型语言模型提供上下文和附加功能的方式。MCP 采用客户端-服务器协议，其中客户端（例如 Gordon 这样的应用程序）发送请求，服务器处理这些请求，从而向 AI 提供必要的上下文。MCP 服务器可以通过执行代码以执行操作并检索结果、调用外部 API 或其他类似操作来收集此上下文。

Gordon 以及 Claude Desktop 或 Cursor 等其他 MCP 客户端，可以与作为容器运行的 MCP 服务器进行交互。


