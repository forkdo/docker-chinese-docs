# Azure Blob Storage cache





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    
      
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Availability:</span>
        <span>
          Experimental
          
            
          
            
          
            
              <span class="icon-svg"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M172-120q-41.78 0-59.39-39T124-230l248-280v-270h-52q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h320q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-52v270l248 280q29 32 11.39 71T788-120H172Z"/></svg></span>
            
          
            
          
            
          
        </span>
      </div>
    

    

    
  </div>



The `azblob` cache store uploads your resulting build cache to
[Azure's blob storage service](https://azure.microsoft.com/en-us/services/storage/blobs/).

This cache storage backend is not supported with the default `docker` driver.
To use this feature, create a new builder using a different driver. See
[Build drivers](/manuals/build/builders/drivers/_index.md) for more information.

## Synopsis

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=azblob,name=<cache-image>[,parameters...] \
  --cache-from type=azblob,name=<cache-image>[,parameters...] .
```

The following table describes the available CSV parameters that you can pass to
`--cache-to` and `--cache-from`.

| Name                | Option                  | Type        | Default | Description                                        |
| ------------------- | ----------------------- | ----------- | ------- | -------------------------------------------------- |
| `name`              | `cache-to`,`cache-from` | String      |         | Required. The name of the cache image.             |
| `account_url`       | `cache-to`,`cache-from` | String      |         | Base URL of the storage account.                   |
| `secret_access_key` | `cache-to`,`cache-from` | String      |         | Blob storage account key, see [authentication][1]. |
| `mode`              | `cache-to`              | `min`,`max` | `min`   | Cache layers to export, see [cache mode][2].       |
| `ignore-error`      | `cache-to`              | Boolean     | `false` | Ignore errors caused by failed cache exports.      |

[1]: #authentication
[2]: _index.md#cache-mode

## Authentication

The `secret_access_key`, if left unspecified, is read from environment variables
on the BuildKit server following the scheme for the
[Azure Go SDK](https://docs.microsoft.com/en-us/azure/developer/go/azure-sdk-authentication).
The environment variables are read from the server, not the Buildx client.

## Further reading

For an introduction to caching see [Docker build cache](../_index.md).

For more information on the `azblob` cache backend, see the
[BuildKit README](https://github.com/moby/buildkit#azure-blob-storage-cache-experimental).

