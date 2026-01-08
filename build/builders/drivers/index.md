# Build drivers

Build drivers are configurations for how and where the BuildKit backend runs.
Driver settings are customizable and allow fine-grained control of the builder.
Buildx supports the following drivers:

- `docker`: uses the BuildKit library bundled into the Docker daemon.
- `docker-container`: creates a dedicated BuildKit container using Docker.
- `kubernetes`: creates BuildKit pods in a Kubernetes cluster.
- `remote`: connects directly to a manually managed BuildKit daemon.

Different drivers support different use cases. The default `docker` driver
prioritizes simplicity and ease of use. It has limited support for advanced
features like caching and output formats, and isn't configurable. Other drivers
provide more flexibility and are better at handling advanced scenarios.

The following table outlines some differences between drivers.

| Feature                      |  `docker`   | `docker-container` | `kubernetes` |      `remote`      |
| :--------------------------- | :---------: | :----------------: | :----------: | :----------------: |
| **Automatically load image** |     ✅      |                    |              |                    |
| **Cache export**             |     ✅\*     |         ✅         |      ✅      |         ✅         |
| **Tarball output**           |             |         ✅         |      ✅      |         ✅         |
| **Multi-arch images**        |             |         ✅         |      ✅      |         ✅         |
| **BuildKit configuration**   |             |         ✅         |      ✅      | Managed externally |

\* _The `docker` driver doesn't support all cache export options.
See [Cache storage backends](/manuals/build/cache/backends/_index.md) for more information._

## Loading to local image store

Unlike when using the default `docker` driver, images built using other drivers
aren't automatically loaded into the local image store. If you don't specify an
output, the build result is exported to the build cache only.

To build an image using a non-default driver and load it to the image store,
   use the `--load` flag with the build command:

   ```console
   $ docker buildx build --load -t <image> --builder=container .
   ...
   => exporting to oci image format                                                                                                      7.7s
   => => exporting layers                                                                                                                4.9s
   => => exporting manifest sha256:4e4ca161fa338be2c303445411900ebbc5fc086153a0b846ac12996960b479d3                                      0.0s
   => => exporting config sha256:adf3eec768a14b6e183a1010cb96d91155a82fd722a1091440c88f3747f1f53f                                        0.0s
   => => sending tarball                                                                                                                 2.8s
   => importing to docker
   ```

   With this option, the image is available in the image store after the build finishes:

   ```console
   $ docker image ls
   REPOSITORY                       TAG               IMAGE ID       CREATED             SIZE
   <image>                          latest            adf3eec768a1   2 minutes ago       197MB
   ```

### Load by default





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Buildx <a class="link" href="https://github.com/docker/buildx/releases/tag/v0.14.0" rel="noopener">0.14.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



You can configure the custom build drivers to behave in a similar way to the
default `docker` driver, and load images to the local image store by default.
To do so, set the `default-load` driver option when creating the builder:

```console
$ docker buildx create --driver-opt default-load=true
```

Note that, just like with the `docker` driver, if you specify a different
output format with `--output`, the result will not be loaded to the image store
unless you also explicitly specify `--output type=docker` or use the `--load`
flag.

## What's next

Read about each driver:

  - [Docker driver](./docker.md)
  - [Docker container driver](./docker-container.md)
  - [Kubernetes driver](./kubernetes.md)
- [Remote driver](./remote.md)


- [Docker container driver](/build/builders/drivers/docker-container/)

- [Docker driver](/build/builders/drivers/docker/)

- [Kubernetes driver](/build/builders/drivers/kubernetes/)

- [Remote driver](/build/builders/drivers/remote/)

