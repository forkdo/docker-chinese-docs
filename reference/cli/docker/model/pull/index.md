# docker model pull

**Description:** Pull a model from Docker Hub or HuggingFace to your local environment

**Usage:** `docker model pull MODEL`



<!--
本页面由 Docker 源代码自动生成。如果您希望修改此处显示的文本内容，请在 GitHub 上的源代码仓库中提交问题或拉取请求：

https://github.com/docker/model-cli
-->








## Description

Pull a model to your local environment. Downloaded models also appear in the Docker Desktop Dashboard.



## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--ignore-runtime-memory-check` |  |  Do not block pull if estimated runtime memory for model exceeds system resources.<br> |



## Examples

### Pulling a model from Docker Hub

```console
docker model pull ai/smollm2
```

### Pulling from HuggingFace

You can pull GGUF models directly from [Hugging Face](https://huggingface.co/models?library=gguf).

**Note about quantization:** If no tag is specified, the command tries to pull the `Q4_K_M` version of the model.
If `Q4_K_M` doesn't exist, the command pulls the first GGUF found in the **Files** view of the model on HuggingFace.
To specify the quantization, provide it as a tag, for example:
`docker model pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF:Q4_K_S`

```console
docker model pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```



