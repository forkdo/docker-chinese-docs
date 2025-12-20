# Amazon S3 cache





  
  
  
  


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



The `s3` cache storage uploads your resulting build cache to
[Amazon S3 file storage service](https://aws.amazon.com/s3/)
or other S3-compatible services, such as [MinIO](https://min.io/).

This cache storage backend is not supported with the default `docker` driver.
To use this feature, create a new builder using a different driver. See
[Build drivers](/manuals/build/builders/drivers/_index.md) for more information.

## Synopsis

```console
$ docker buildx build --push -t <user>/<image> \
  --cache-to type=s3,region=<region>,bucket=<bucket>,name=<cache-image>[,parameters...] \
  --cache-from type=s3,region=<region>,bucket=<bucket>,name=<cache-image> .
```

The following table describes the available CSV parameters that you can pass to
`--cache-to` and `--cache-from`.

| Name                 | Option                  | Type        | Default      | Description                                                    |
|----------------------| ----------------------- | ----------- |--------------|----------------------------------------------------------------|
| `region`             | `cache-to`,`cache-from` | String      |              | Required. Geographic location.                                 |
| `bucket`             | `cache-to`,`cache-from` | String      |              | Required. Name of the S3 bucket.                               |
| `name`               | `cache-to`,`cache-from` | String      | `buildkit`   | Name of the cache image.                                       |
| `endpoint_url`       | `cache-to`,`cache-from` | String      |              | Endpoint of the S3 bucket.                                     |
| `prefix`             | `cache-to`,`cache-from` | String      |              | Prefix to prepend to all filenames.                            |
| `blobs_prefix`       | `cache-to`,`cache-from` | String      | `blobs/`     | Prefix to prepend to blob filenames.                           |
| `upload_parallelism` | `cache-to`              | Integer     | `4`          | Number of parallel layer uploads.                              |
| `touch_refresh`      | `cache-to`              | Time        | `24h`        | Interval for updating the timestamp of unchanged cache layers. |
| `manifests_prefix`   | `cache-to`,`cache-from` | String      | `manifests/` | Prefix to prepend to manifest filenames.                       |
| `use_path_style`     | `cache-to`,`cache-from` | Boolean     | `false`      | When `true`, uses `bucket` in the URL instead of hostname.     |
| `access_key_id`      | `cache-to`,`cache-from` | String      |              | See [authentication][1].                                       |
| `secret_access_key`  | `cache-to`,`cache-from` | String      |              | See [authentication][1].                                       |
| `session_token`      | `cache-to`,`cache-from` | String      |              | See [authentication][1].                                       |
| `mode`               | `cache-to`              | `min`,`max` | `min`        | Cache layers to export, see [cache mode][2].                   |
| `ignore-error`       | `cache-to`              | Boolean     | `false`      | Ignore errors caused by failed cache exports.                  |

[1]: #authentication
[2]: _index.md#cache-mode

## Authentication

Buildx can reuse existing AWS credentials, configured either using a
credentials file or environment variables, for pushing and pulling cache to S3.
Alternatively, you can use the `access_key_id`, `secret_access_key`, and
`session_token` attributes to specify credentials directly on the CLI.

Refer to [AWS Go SDK, Specifying Credentials][3] for details about
authentication using environment variables and credentials file.

[3]: https://docs.aws.amazon.com/sdk-for-go/v2/developer-guide/configure-gosdk.html#specifying-credentials

## Further reading

For an introduction to caching see [Docker build cache](../_index.md).

For more information on the `s3` cache backend, see the
[BuildKit README](https://github.com/moby/buildkit#s3-cache-experimental).

