# tmpfs 挂载

[Volumes](volumes.md) 和 [bind mounts](bind-mounts.md) 允许你在主机和容器之间共享文件，以便在容器停止后仍能保留数据。

如果你在 Linux 上运行 Docker，还有第三种选择：tmpfs 挂载。
当你使用 tmpfs 挂载创建容器时，容器可以在容器的可写层之外创建文件。

与 volumes 和 bind mounts 不同，tmpfs 挂载是临时的，仅保留在主机内存中。当容器停止时，tmpfs 挂载会被移除，写入其中的文件不会被保留。

tmpfs 挂载最适合用于你既不希望数据保留在主机上，也不希望保留在容器内的情况。这可能是出于安全原因，或当你的应用程序需要写入大量非持久状态数据时，为了保护容器性能。

> [!IMPORTANT]
> Docker 中的 tmpfs 挂载直接映射到 Linux 内核中的
> [tmpfs](https://en.wikipedia.org/wiki/Tmpfs)。因此，
> 临时数据可能会被写入交换文件，从而持久化到
> 文件系统中。

## 覆盖现有数据的挂载

如果你在容器中已存在文件或目录的目录中创建 tmpfs 挂载，则预先存在的文件会被挂载掩盖。这类似于在 Linux 主机上将文件保存到 `/mnt`，然后将 USB 驱动器挂载到 `/mnt`。在卸载 USB 驱动器之前，`/mnt` 的内容会被 USB 驱动器的内容掩盖。

对于容器，没有直接的方法可以移除挂载以再次显示被掩盖的文件。你最好的选择是重新创建容器而不使用挂载。

## tmpfs 挂载的限制

- 与 volumes 和 bind mounts 不同，你无法在容器之间共享 tmpfs 挂载。
- 此功能仅在你运行 Docker on Linux 时可用。
- 在 tmpfs 上设置权限可能会导致它们在[容器重启后重置](https://github.com/docker/for-linux/issues/138)。在某些情况下，[设置 uid/gid](https://github.com/docker/compose/issues/3425#issuecomment-423091370) 可以作为解决方法。

## 语法

要使用 `docker run` 命令挂载 tmpfs，你可以使用 `--mount` 或 `--tmpfs` 标志。

```console
$ docker run --mount type=tmpfs,dst=<mount-path>
$ docker run --tmpfs <mount-path>
```

通常，推荐使用 `--mount`。主要区别在于 `--mount` 标志更明确。另一方面，`--tmpfs` 更简洁，并提供了更多灵活性，因为它允许你设置更多挂载选项。

`--tmpfs` 标志不能与 swarm services 一起使用。你必须使用 `--mount`。

### `--tmpfs` 的选项

`--tmpfs` 标志由两个字段组成，用冒号字符（`:`）分隔。

```console
$ docker run --tmpfs <mount-path>[:opts]
```

第一个字段是要挂载到 tmpfs 的容器路径。第二个字段是可选的，允许你设置挂载选项。`--tmpfs` 的有效挂载选项包括：

| 选项         | 描述                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------- |
| `ro`         | 创建只读 tmpfs 挂载。                                                            |
| `rw`         | 创建读写 tmpfs 挂载（默认行为）。                                        |
| `nosuid`     | 防止在执行期间识别 `setuid` 和 `setgid` 位。                    |
| `suid`       | 允许在执行期间识别 `setuid` 和 `setgid` 位（默认行为）。        |
| `nodev`      | 可以创建设备文件，但这些设备文件不可用（访问会导致错误）。            |
| `dev`        | 可以创建设备文件，并且这些设备文件完全可用。                                       |
| `exec`       | 允许在挂载的文件系统中执行可执行二进制文件。                     |
| `noexec`     | 不允许在挂载的文件系统中执行可执行二进制文件。             |
| `sync`       | 对文件系统的所有 I/O 操作同步进行。                                           |
| `async`      | 对文件系统的所有 I/O 操作异步进行（默认行为）。                       |
| `dirsync`    | 对文件系统中的目录更新同步进行。                            |
| `atime`      | 每次访问文件时更新文件访问时间。                                    |
| `noatime`    | 访问文件时不更新文件访问时间。                                |
| `diratime`   | 每次访问目录时更新目录访问时间。                         |
| `nodiratime` | 访问目录时不更新目录访问时间。                      |
| `size`       | 指定 tmpfs 挂载的大小，例如 `size=64m`。                             |
| `mode`       | 指定 tmpfs 挂载的文件模式（权限），例如 `mode=1777`。       |
| `uid`        | 指定 tmpfs 挂载所有者的用户 ID，例如 `uid=1000`。           |
| `gid`        | 指定 tmpfs 挂载所有者的组 ID，例如 `gid=1000`。          |
| `nr_inodes`  | 指定 tmpfs 挂载的最大 inode 数，例如 `nr_inodes=400k`。 |
| `nr_blocks`  | 指定 tmpfs 挂载的最大块数，例如 `nr_blocks=1024`。 |

```console {title="示例"}
$ docker run --tmpfs /data:noexec,size=1024,mode=1777
```

并非 Linux mount 命令中所有可用的 tmpfs 挂载功能都支持 `--tmpfs` 标志。如果你需要高级 tmpfs 选项或功能，你可能需要使用特权容器或在 Docker 外部配置挂载。

> [!CAUTION]
> 使用 `--privileged` 运行容器会授予提升的权限，并可能
> 使主机系统面临安全风险。仅在绝对必要且可信的环境中使用此选项。

```console
$ docker run --privileged -it debian sh
/# mount -t tmpfs -o <options> tmpfs /data
```

### `--mount` 的选项

`--mount` 标志由多个键值对组成，用逗号分隔，每个键值对由 `<key>=<value>` 元组组成。键的顺序不重要。

```console
$ docker run --mount type=tmpfs,dst=<mount-path>[,<key>=<value>...]
```

`--mount type=tmpfs` 的有效选项包括：

| 选项                         | 描述                                                                                                            |
| :----------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `destination`, `dst`, `target` | 要挂载到 tmpfs 的容器路径。                                                                                  |
| `tmpfs-size`                   | tmpfs 挂载的大小（以字节为单位）。如果未设置，tmpfs 卷的默认最大大小为主机总 RAM 的 50%。 |
| `tmpfs-mode`                   | tmpfs 的文件模式（八进制）。例如 `700` 或 `0770`。默认为 `1777` 或全局可写。                  |

```console {title="示例"}
$ docker run --mount type=tmpfs,dst=/app,tmpfs-size=21474836480,tmpfs-mode=1770
```

## 在容器中使用 tmpfs 挂载

要在容器中使用 `tmpfs` 挂载，请使用 `--tmpfs` 标志，或使用带有 `type=tmpfs` 和 `destination` 选项的 `--mount` 标志。`tmpfs` 挂载没有 `source`。以下示例在 Nginx 容器中的 `/app` 处创建了一个 `tmpfs` 挂载。第一个示例使用 `--mount` 标志，第二个使用 `--tmpfs` 标志。








<div
  class="tabs"
  
    x-data="{ selected: '--mount' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '--mount' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '--mount'"
        
      >
        <code>--mount</code>
      </button>
    
      <button
        class="tab-item"
        :class="selected === '--tmpfs' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '--tmpfs'"
        
      >
        <code>--tmpfs</code>
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '--mount' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kIFwKICAtaXQgXAogIC0tbmFtZSB0bXB0ZXN0IFwKICAtLW1vdW50IHR5cGU9dG1wZnMsZGVzdGluYXRpb249L2FwcCBcCiAgbmdpbng6bGF0ZXN0', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -d <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span><span class="go">  -it \
</span></span></span><span class="line"><span class="cl"><span class="go">  --name tmptest \
</span></span></span><span class="line"><span class="cl"><span class="go">  --mount type=tmpfs,destination=/app \
</span></span></span><span class="line"><span class="cl"><span class="go">  nginx:latest
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>通过在 <code>docker inspect</code> 输出的 <code>Mounts</code> 部分中查找来验证挂载是否为 <code>tmpfs</code> 挂载：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgaW5zcGVjdCB0bXB0ZXN0IC0tZm9ybWF0ICd7eyBqc29uIC5Nb3VudHMgfX0nClt7IlR5cGUiOiJ0bXBmcyIsIlNvdXJjZSI6IiIsIkRlc3RpbmF0aW9uIjoiL2FwcCIsIk1vZGUiOiIiLCJSVyI6dHJ1ZSwiUHJvcGFnYXRpb24iOiIifV0=', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker inspect tmptest --format <span class="s1">&#39;{{ json .Mounts }}&#39;</span>
</span></span><span class="line"><span class="cl"><span class="go">[{&#34;Type&#34;:&#34;tmpfs&#34;,&#34;Source&#34;:&#34;&#34;,&#34;Destination&#34;:&#34;/app&#34;,&#34;Mode&#34;:&#34;&#34;,&#34;RW&#34;:true,&#34;Propagation&#34;:&#34;&#34;}]
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '--tmpfs' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kIFwKICAtaXQgXAogIC0tbmFtZSB0bXB0ZXN0IFwKICAtLXRtcGZzIC9hcHAgXAogIG5naW54OmxhdGVzdA==', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -d <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span><span class="go">  -it \
</span></span></span><span class="line"><span class="cl"><span class="go">  --name tmptest \
</span></span></span><span class="line"><span class="cl"><span class="go">  --tmpfs /app \
</span></span></span><span class="line"><span class="cl"><span class="go">  nginx:latest
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>通过在 <code>docker inspect</code> 输出的 <code>Mounts</code> 部分中查找来验证挂载是否为 <code>tmpfs</code> 挂载：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgaW5zcGVjdCB0bXB0ZXN0IC0tZm9ybWF0ICd7eyBqc29uIC5Nb3VudHMgfX0nCnsiL2FwcCI6IiJ9', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker inspect tmptest --format <span class="s1">&#39;{{ json .Mounts }}&#39;</span>
</span></span><span class="line"><span class="cl"><span class="go">{&#34;/app&#34;:&#34;&#34;}
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


停止并移除容器：

```console
$ docker stop tmptest
$ docker rm tmptest
```

## 下一步

- 了解 [volumes](volumes.md)
- 了解 [bind mounts](bind-mounts.md)
- 了解 [storage drivers](/engine/storage/drivers/)
