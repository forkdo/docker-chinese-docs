# Azure Blob Storage 缓存




`azblob` 缓存存储会将你生成的构建缓存上传到
[Azure 的 blob 存储服务](https://azure.microsoft.com/en-us/services/storage/blobs/)。

默认的 `docker` 驱动不支持这种缓存存储后端。要使用此功能，请使用不同的驱动创建一个新的 builder。更多信息请参阅 [Build drivers](/manuals/build/builders/drivers/_index.md)。

## 概要（Synopsis）

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=azblob,name=<cache-image>[,parameters...] \
  --cache-from type=azblob,name=<cache-image>[,parameters...] .
```

下表描述了你可以传递给 `--cache-to` 和 `--cache-from` 的可用 CSV 参数。

| Name                | Option                  | Type        | Default | Description                                        |
| ------------------- | ----------------------- | ----------- | ------- | -------------------------------------------------- |
| `name`              | `cache-to`,`cache-from` | String      |         | 必填。缓存镜像的名称。                             |
| `account_url`       | `cache-to`,`cache-from` | String      |         | 存储账户的基础 URL。                               |
| `secret_access_key` | `cache-to`,`cache-from` | String      |         | Blob 存储账户密钥，参见 [authentication][1]。      |
| `mode`              | `cache-to`              | `min`,`max` | `min`   | 要导出的缓存层，参见 [cache mode][2]。             |
| `ignore-error`      | `cache-to`              | Boolean     | `false` | 忽略由缓存导出失败引起的错误。                     |

[1]: #authentication
[2]: _index.md#cache-mode

## 身份验证（Authentication）

如果未指定 `secret_access_key`，则会按照
[Azure Go SDK](https://docs.microsoft.com/en-us/azure/developer/go/azure-sdk-authentication)
的方案，从 BuildKit 服务器上的环境变量读取。环境变量是从服务器读取的，而非从 Buildx 客户端读取。

## 延伸阅读（Further reading）

有关缓存的入门介绍，请参阅 [Docker 构建缓存](../_index.md)。

有关 `azblob` 缓存后端的更多信息，请参阅
[BuildKit README](https://github.com/moby/buildkit#azure-blob-storage-cache-experimental)。

