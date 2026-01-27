# 配置选项


Docker Model Runner 提供了多种配置选项来调整模型行为、内存使用和推理性能。本指南涵盖了关键设置及其应用方法。

## 上下文大小（上下文长度）

上下文大小决定了模型在单个请求中可以处理的最大令牌数，包括输入提示和生成的输出。这是影响内存使用和模型能力的最重要设置之一。

### 默认上下文大小

默认情况下，Docker Model Runner 使用的上下文大小在能力和资源效率之间取得了平衡：

| 引擎 | 默认行为 |
|--------|------------------|
| llama.cpp | 4096 个令牌 |
| vLLM | 使用模型训练的最大上下文大小 |

> [!NOTE]
> 实际默认值因模型而异。大多数模型默认支持 2,048 到 8,192 个令牌。一些较新的模型支持 32K、128K 甚至更大的上下文。

### 配置上下文大小

您可以使用 `docker model configure` 命令为每个模型调整上下文大小：

```console
$ docker model configure --context-size 8192 ai/qwen2.5-coder
```

或者在 Compose 文件中：

```yaml
models:
  llm:
    model: ai/qwen2.5-coder
    context_size: 8192
```

### 上下文大小指南

| 上下文大小 | 典型用例 | 内存影响 |
|--------------|------------------|---------------|
| 2,048 | 简单查询、短代码片段 | 低 |
| 4,096 | 标准对话、中等代码文件 | 中等 |
| 8,192 | 长对话、较大代码文件 | 较高 |
| 16,384+ | 扩展文档、多文件上下文 | 高 |

> [!IMPORTANT]
> 更大的上下文大小需要更多内存（RAM/VRAM）。如果遇到内存不足错误，请减小上下文大小。粗略指南是，每增加 1,000 个令牌大约需要 100-500 MB 的额外内存，具体取决于模型大小。

### 检查模型的最大上下文

要查看模型的配置，包括上下文大小：

```console
$ docker model inspect ai/qwen2.5-coder
```

> [!NOTE]
> `docker model inspect` 命令显示模型支持的最大上下文长度（例如 `gemma3.context_length`），而不是配置的上下文大小。配置的上下文大小是您使用 `docker model configure --context-size` 设置的值，表示推理期间使用的实际限制，该限制应小于或等于模型支持的最大上下文长度。

## 运行时标志

运行时标志允许您直接将参数传递给底层推理引擎。这提供了对模型行为的细粒度控制。

### 使用运行时标志

运行时标志可以通过多种机制提供：

#### 使用 Docker Compose

在 Compose 文件中：

```yaml
models:
  llm:
    model: ai/qwen2.5-coder
    context_size: 4096
    runtime_flags:
      - "--temp"
      - "0.7"
      - "--top-p"
      - "0.9"
```

#### 使用命令行

使用 `docker model configure` 命令：

```console
$ docker model configure --runtime-flag "--temp" --runtime-flag "0.7" --runtime-flag "--top-p" --runtime-flag "0.9" ai/qwen2.5-coder
```

### 常用 llama.cpp 参数

这些是最常用的 llama.cpp 参数。对于典型用例，您无需查阅 llama.cpp 文档。

#### 采样参数

| 标志 | 描述 | 默认值 | 范围 |
|------|-------------|---------|-------|
| `--temp` | 采样温度。越低 = 越确定，越高 = 越有创意 | 0.8 | 0.0-2.0 |
| `--top-k` | 限制采样到前 K 个令牌。越低 = 越集中 | 40 | 1-100 |
| `--top-p` | 核心采样阈值。越低 = 越集中 | 0.9 | 0.0-1.0 |
| `--min-p` | 最小概率阈值 | 0.05 | 0.0-1.0 |
| `--repeat-penalty` | 重复令牌的惩罚 | 1.1 | 1.0-2.0 |

**示例：确定性输出（用于代码生成）**

```yaml
runtime_flags:
  - "--temp"
  - "0"
  - "--top-k"
  - "1"
```

**示例：创意输出（用于故事创作）**

```yaml
runtime_flags:
  - "--temp"
  - "1.2"
  - "--top-p"
  - "0.95"
```

#### 性能参数

| 标志 | 描述 | 默认值 | 备注 |
|------|-------------|---------|-------|
| `--threads` | 用于生成的 CPU 线程数 | 自动 | 设置为性能核心数 |
| `--threads-batch` | 用于批处理的 CPU 线程数 | 自动 | 通常与 `--threads` 相同 |
| `--batch-size` | 提示处理的批处理大小 | 512 | 越高 = 提示处理越快 |
| `--mlock` | 将模型锁定在内存中 | 关闭 | 防止交换，需要足够的 RAM |
| `--no-mmap` | 禁用内存映射 | 关闭 | 可能在某些系统上提高性能 |

**示例：针对多核 CPU 优化**

```yaml
runtime_flags:
  - "--threads"
  - "8"
  - "--batch-size"
  - "1024"
```

#### GPU 参数

| 标志 | 描述 | 默认值 | 备注 |
|------|-------------|---------|-------|
| `--n-gpu-layers` | 卸载到 GPU 的层数 | 全部（如果 GPU 可用） | 如果 VRAM 不足则减少 |
| `--main-gpu` | 用于计算的 GPU | 0 | 用于多 GPU 系统 |
| `--split-mode` | 如何跨 GPU 分割 | layer | 选项：`none`, `layer`, `row` |

**示例：部分 GPU 卸载（VRAM 有限）**

```yaml
runtime_flags:
  - "--n-gpu-layers"
  - "20"
```

#### 高级参数

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--rope-scaling` | RoPE 缩放方法 | 自动 |
| `--rope-freq-base` | RoPE 基础频率 | 模型默认值 |
| `--rope-freq-scale` | RoPE 频率缩放 | 模型默认值 |
| `--no-prefill-assistant` | 禁用助手预填充 | 关闭 |
| `--reasoning-budget` | 推理模型的令牌预算 | 0（禁用） |

### vLLM 参数

使用 vLLM 后端时，可使用不同的参数。

使用 `--hf_overrides` 以 JSON 格式传递 HuggingFace 模型配置覆盖：

```console
$ docker model configure --hf_overrides '{"rope_scaling": {"type": "dynamic", "factor": 2.0}}' ai/model-vllm
```

## 配置预设

以下是常见用例的完整配置示例。

### 代码补全（快速、确定性）

```yaml
models:
  coder:
    model: ai/qwen2.5-coder
    context_size: 4096
    runtime_flags:
      - "--temp"
      - "0.1"
      - "--top-k"
      - "1"
      - "--batch-size"
      - "1024"
```

### 聊天助手（平衡）

```yaml
models:
  assistant:
    model: ai/llama3.2
    context_size: 8192
    runtime_flags:
      - "--temp"
      - "0.7"
      - "--top-p"
      - "0.9"
      - "--repeat-penalty"
      - "1.1"
```

### 创意写作（高温度）

```yaml
models:
  writer:
    model: ai/llama3.2
    context_size: 8192
    runtime_flags:
      - "--temp"
      - "1.2"
      - "--top-p"
      - "0.95"
      - "--repeat-penalty"
      - "1.0"
```

### 长文档分析（大上下文）

```yaml
models:
  analyzer:
    model: ai/qwen2.5-coder:14B
    context_size: 32768
    runtime_flags:
      - "--mlock"
      - "--batch-size"
      - "2048"
```

### 低内存系统

```yaml
models:
  efficient:
    model: ai/smollm2:360M-Q4_K_M
    context_size: 2048
    runtime_flags:
      - "--threads"
      - "4"
```

## 基于环境的配置

您还可以通过容器中的环境变量配置模型：

| 变量 | 描述 |
|----------|-------------|
| `LLM_URL` | 自动注入的模型端点 URL |
| `LLM_MODEL` | 自动注入的模型标识符 |

有关如何填充这些值的详细信息，请参阅 [Models and Compose](/manuals/ai/compose/models-and-compose.md)。

## 重置配置

通过 `docker model configure` 设置的配置会一直保留，直到模型被移除。要重置配置：

```console
$ docker model configure --context-size -1 ai/qwen2.5-coder
```

使用 `-1` 可重置为默认值。

## 下一步

- [推理引擎](inference-engines.md) - 了解 llama.cpp 和 vLLM
- [API 参考](api-reference.md) - 用于每个请求配置的 API 参数
- [Models and Compose](/manuals/ai/compose/models-and-compose.md) - 在 Compose 应用程序中配置模型
