# 合并 Compose 文件



Compose 允许您通过多个 Compose 文件来定义 Compose 应用程序模型。
在此过程中，Compose 遵循特定规则来合并 Compose 文件。

这些规则如下所述。

## 映射（Mapping）

YAML `mapping` 通过添加缺失的条目并合并冲突的条目来实现合并。

合并以下示例 YAML 树：

```yaml
services:
  foo:
    key1: value1
    key2: value2
```

```yaml
services:
  foo:
    key2: VALUE
    key3: value3
```

结果是一个等效于以下 YAML 树的 Compose 应用模型：

```yaml
services:
  foo:
    key1: value1
    key2: VALUE
    key3: value3
```

## 序列（Sequence）

YAML `sequence` 通过将覆盖的 Compose 文件中的值追加到前一个文件中来实现合并。

合并以下示例 YAML 树：

```yaml
services:
  foo:
    DNS:
      - 1.1.1.1
```

```yaml
services:
  foo:
    DNS: 
      - 8.8.8.8
```

结果是一个等效于以下 YAML 树的 Compose 应用模型：

```yaml
services:
  foo:
    DNS:
      - 1.1.1.1
      - 8.8.8.8
```

## 例外情况

### Shell 命令

当合并使用服务属性 [command](services.md#command)、[entrypoint](services.md#entrypoint) 和 [healthcheck: `test`](services.md#healthcheck) 的 Compose 文件时，值会被最新的 Compose 文件覆盖，而不是追加。

合并以下示例 YAML 树：

```yaml
services:
  foo:
    command: ["echo", "foo"]
```

```yaml
services:
  foo:
    command: ["echo", "bar"]
```

结果是一个等效于以下 YAML 树的 Compose 应用模型：

```yaml
services:
  foo:
    command: ["echo", "bar"]
```

### 唯一资源

适用于 [ports](services.md#ports)、[volumes](services.md#volumes)、[secrets](services.md#secrets) 和 [configs](services.md#configs) 服务属性。
虽然这些类型在 Compose 文件中建模为序列，但它们具有特殊的唯一性要求：

| 属性      | 唯一键                   |
|-----------|--------------------------|
| volumes   |  target                  |
| secrets   |  target                  |
| configs   |  target                  |
| ports     |  {ip, target, published, protocol}   |

合并 Compose 文件时，Compose 会追加不违反唯一性约束的新条目，并合并共享唯一键的条目。

合并以下示例 YAML 树：

```yaml
services:
  foo:
    volumes:
      - foo:/work
```

```yaml
services:
  foo:
    volumes:
      - bar:/work
```

结果是一个等效于以下 YAML 树的 Compose 应用模型：

```yaml
services:
  foo:
    volumes:
      - bar:/work
```

### 重置值

除了前面描述的机制外，覆盖 Compose 文件还可用于从应用模型中移除元素。
为此，可以设置自定义 [YAML 标签](https://yaml.org/spec/1.2.2/#24-tags) `!reset` 来覆盖被覆盖 Compose 文件设置的值。必须为属性提供有效值，但将被忽略，目标属性将设置为类型的默认值或 `null`。

为了提高可读性，建议将属性值显式设置为 null (`null`) 或空数组 `[]`（使用 `!reset null` 或 `!reset []`），以明确结果属性将被清除。

一个基础的 `compose.yaml` 文件：

```yaml
services:
  app:
    image: myapp
    ports:
      - "8080:80" 
    environment:
      FOO: BAR           
```

和一个 `compose.override.yaml` 文件：

```yaml
services:
  app:
    image: myapp
    ports: !reset []
    environment:
      FOO: !reset null
```

结果为：

```yaml
services:
  app:
    image: myapp
```

### 替换值





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose <a class="link" href="https://github.com/docker/compose/releases/tag/v2.24.4" rel="noopener">2.24.4</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



虽然 `!reset` 可用于通过覆盖文件从 Compose 文件中移除声明，但 `!override` 允许您完全替换属性，绕过标准合并规则。一个典型的例子是完全替换资源定义，以依赖不同的模型但使用相同的名称。

一个基础的 `compose.yaml` 文件：

```yaml
services:
  app:
    image: myapp
    ports:
      - "8080:80"
```

要移除原始端口但暴露一个新端口，使用以下覆盖文件：

```yaml
services:
  app:
    ports: !override
      - "8443:443" 
```

结果为：

```yaml
services:
  app:
    image: myapp
    ports:
      - "8443:443" 
```

如果未使用 `!override`，根据[上述合并规则](#sequence)，`8080:80` 和 `8443:443` 都将被暴露。

## 其他资源

有关如何使用合并创建复合 Compose 文件的更多信息，请参阅[使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)
