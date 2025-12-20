# Model Context Protocol (MCP)

[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) 是一种开放协议，用于标准化应用程序向大型语言模型提供上下文和附加功能的方式。MCP 采用客户端-服务器协议，其中客户端（例如 Gordon 这样的应用程序）发送请求，服务器处理这些请求，从而向 AI 提供必要的上下文。MCP 服务器可以通过执行代码以执行操作并检索结果、调用外部 API 或其他类似操作来收集此上下文。

Gordon 以及 Claude Desktop 或 Cursor 等其他 MCP 客户端，可以与作为容器运行的 MCP 服务器进行交互。


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/ai/gordon/mcp/built-in-tools" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M740-149 517-371l57-57 223 223q12 12 12 28t-12 28q-12 12-28.5 12T740-149Zm-581 0q-12-12-12-28.5t12-28.5l261-261-107-107-2 2q-9 9-21 9t-21-9l-23-23v97q0 10-9.5 13.5T220-488L102-606q-7-7-3.5-16.5T112-632h98l-27-27q-9-9-9-21t9-21l110-110q17-17 37-23t44-6q21 0 36 5.5t32 18.5q5 5 5.5 11t-4.5 11l-95 95 27 27q9 9 9 21t-9 21l-3 3 104 104 122-122q-8-13-12.5-30t-4.5-36q0-53 38.5-91.5T711-841q8 0 14.5.5T737-838q6 3 7.5 9.5T741-817l-61 61q-5 5-5 11t5 11l53 53q5 5 11 5t11-5l59-59q5-5 13-4t11 8q2 6 2.5 12.5t.5 14.5q0 53-38.5 91.5T711-579q-18 0-31-2.5t-24-7.5L215-148q-12 12-28 11.5T159-149Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">内置工具</h3>
    </div>
    <div class="card-content">
      <p class="card-description">使用内置工具。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/ai/gordon/mcp/yaml" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M223-545q-20-5-37.5-14.5T154-583l-22 9q-10 4-19.5 1T98-585l-6-10q-5-8-4-18t9-17l20-19q-5-20-5-39t5-39l-20-19q-8-7-9-17.5t4-18.5l5-8q5-9 15-12.5t20 .5l22 9q14-14 31.5-23.5T223-831l3-23q2-11 10-18.5t19-7.5h8q11 0 19 7.5t10 18.5l3 23q20 5 37.5 14.5T364-793l22-9q10-4 19.5-1t14.5 12l6 9q5 8 4 18.5t-9 17.5l-21 19q5 19 5 38.5t-5 39.5l21 19q8 7 9 17t-4 19l-5 8q-5 9-15 12.5t-20-.5l-22-9q-14 15-31.5 24T295-545l-3 23q-2 11-10 18.5t-19 7.5h-8q-11 0-19-7.5T226-522l-3-23Zm36-51q38 0 65-27t27-65q0-38-27-65t-65-27q-38 0-65 27t-27 65q0 38 27 65t65 27ZM630-97q-27-7-51.5-21T536-154l-26 8q-12 4-24-.5T467-162l-8-14q-7-11-5-24t12-22l20-18q-8-26-8-54t8-54l-20-17q-10-8-12-21.5t5-24.5l9-15q6-11 17.5-15t23.5-1l27 7q19-21 43-35.5t51-20.5l7-29q3-12 12.5-20t22.5-8h18q13 0 23 8t13 20l7 29q29 4 52.5 19t42.5 37l27-7q12-3 23.5 1.5T896-425l9 14q7 11 4.5 24T897-365l-19 17q8 26 8 54t-8 54l20 18q10 9 12 22t-5 24l-8 14q-7 11-19 16t-25 0l-25-8q-18 23-42.5 36.5T733-97l-7 29q-3 12-12.5 20T691-40h-18q-13 0-23-8t-13-20l-7-29Zm52-58q58 0 98.5-40.5T821-294q0-58-40.5-98.5T682-433q-58 0-98.5 40.5T543-294q0 58 40.5 98.5T682-155Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">MCP 配置</h3>
    </div>
    <div class="card-content">
      <p class="card-description">基于每个项目配置 MCP 工具。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [Gordon 中的内置工具](https://docs.docker.com/ai/gordon/mcp/built-in-tools/)

- [使用 YAML 配置 MCP 服务器](https://docs.docker.com/ai/gordon/mcp/yaml/)

