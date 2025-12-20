# Create an advanced frontend extension

To start creating your extension, you first need a directory with files which range from the extension’s source code to the required extension-specific files. This page provides information on how to set up an extension with a more advanced frontend.

Before you start, make sure you have installed the latest version of [Docker Desktop](/manuals/desktop/release-notes.md).

## Extension folder structure

The quickest way to create a new extension is to run `docker extension init my-extension` as in the
[Quickstart](../quickstart.md). This creates a new directory `my-extension` that contains a fully functional extension.

> [!TIP]
>
> The `docker extension init` generates a React based extension. But you can still use it as a starting point for
> your own extension and use any other frontend framework, like Vue, Angular, Svelte, etc. or even stay with
> vanilla Javascript.

Although you can start from an empty directory or from the `react-extension` [sample folder](https://github.com/docker/extensions-sdk/tree/main/samples),
it's highly recommended that you start from the `docker extension init` command and change it to suit your needs.

```bash
.
├── Dockerfile # (1)
├── ui # (2)
│   ├── public # (3)
│   │   └── index.html
│   ├── src # (4)
│   │   ├── App.tsx
│   │   ├── index.tsx
│   ├── package.json
│   └── package-lock.lock
│   ├── tsconfig.json
├── docker.svg # (5)
└── metadata.json # (6)
```

1. Contains everything required to build the extension and run it in Docker Desktop.
2. High-level folder containing your front-end app source code.
3. Assets that aren’t compiled or dynamically generated are stored here. These can be static assets like logos or the robots.txt file.
4. The src, or source folder contains all the React components, external CSS files, and dynamic assets that are brought into the component files.
5. The icon that is displayed in the left-menu of the Docker Desktop Dashboard.
6. A file that provides information about the extension such as the name, description, and version.

## Adapting the Dockerfile

> [!NOTE]
>
> When using the `docker extension init`, it creates a `Dockerfile` that already contains what is needed for a React
> extension.

Once the extension is created, you need to configure the `Dockerfile` to build the extension and configure the labels
that are used to populate the extension's card in the Marketplace. Here is an example of a `Dockerfile` for a React
extension:








<div
  class="tabs"
  
    
      x-data="{ selected: 'React' }"
    
    @tab-select.window="$event.detail.group === 'framework' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'React' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'framework', name:
          'React'})"
        
      >
        React
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Vue' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'framework', name:
          'Vue'})"
        
      >
        Vue
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Angular' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'framework', name:
          'Angular'})"
        
      >
        Angular
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Svelte' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'framework', name:
          'Svelte'})"
        
      >
        Svelte
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'React' && 'hidden'"
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
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQpGUk9NIC0tcGxhdGZvcm09JEJVSUxEUExBVEZPUk0gbm9kZToxOC45LWFscGluZTMuMTUgQVMgY2xpZW50LWJ1aWxkZXIKV09SS0RJUiAvdWkKIyBjYWNoZSBwYWNrYWdlcyBpbiBsYXllcgpDT1BZIHVpL3BhY2thZ2UuanNvbiAvdWkvcGFja2FnZS5qc29uCkNPUFkgdWkvcGFja2FnZS1sb2NrLmpzb24gL3VpL3BhY2thZ2UtbG9jay5qc29uClJVTiAtLW1vdW50PXR5cGU9Y2FjaGUsdGFyZ2V0PS91c3Ivc3JjL2FwcC8ubnBtIFwKICAgIG5wbSBzZXQgY2FjaGUgL3Vzci9zcmMvYXBwLy5ucG0gJiYgXAogICAgbnBtIGNpCiMgaW5zdGFsbApDT1BZIHVpIC91aQpSVU4gbnBtIHJ1biBidWlsZAoKRlJPTSBhbHBpbmUKTEFCRUwgb3JnLm9wZW5jb250YWluZXJzLmltYWdlLnRpdGxlPSJNeSBleHRlbnNpb24iIFwKICAgIG9yZy5vcGVuY29udGFpbmVycy5pbWFnZS5kZXNjcmlwdGlvbj0iWW91ciBEZXNrdG9wIEV4dGVuc2lvbiBEZXNjcmlwdGlvbiIgXAogICAgb3JnLm9wZW5jb250YWluZXJzLmltYWdlLnZlbmRvcj0iQXdlc29tZSBJbmMuIiBcCiAgICBjb20uZG9ja2VyLmRlc2t0b3AuZXh0ZW5zaW9uLmFwaS52ZXJzaW9uPSIwLjMuMyIgXAogICAgY29tLmRvY2tlci5kZXNrdG9wLmV4dGVuc2lvbi5pY29uPSJodHRwczovL3d3dy5kb2NrZXIuY29tL3dwLWNvbnRlbnQvdXBsb2Fkcy8yMDIyLzAzL01vYnktbG9nby5wbmciIFwKICAgIGNvbS5kb2NrZXIuZXh0ZW5zaW9uLnNjcmVlbnNob3RzPSIiIFwKICAgIGNvbS5kb2NrZXIuZXh0ZW5zaW9uLmRldGFpbGVkLWRlc2NyaXB0aW9uPSIiIFwKICAgIGNvbS5kb2NrZXIuZXh0ZW5zaW9uLnB1Ymxpc2hlci11cmw9IiIgXAogICAgY29tLmRvY2tlci5leHRlbnNpb24uYWRkaXRpb25hbC11cmxzPSIiIFwKICAgIGNvbS5kb2NrZXIuZXh0ZW5zaW9uLmNoYW5nZWxvZz0iIgoKQ09QWSBtZXRhZGF0YS5qc29uIC4KQ09QWSBkb2NrZXIuc3ZnIC4KQ09QWSAtLWZyb209Y2xpZW50LWJ1aWxkZXIgL3VpL2J1aWxkIHVp', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-Dockerfile" data-lang="Dockerfile"><span class="line"><span class="cl"><span class="c"># syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> --platform=$BUILDPLATFORM node:18.9-alpine3.15 AS client-builder</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">WORKDIR</span><span class="s"> /ui</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># cache packages in layer</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> ui/package.json /ui/package.json<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> ui/package-lock.json /ui/package-lock.json<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/usr/src/app/.npm <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    npm <span class="nb">set</span> cache /usr/src/app/.npm <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    npm ci<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># install</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> ui /ui<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> npm run build<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> alpine</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">LABEL</span> org.opencontainers.image.title<span class="o">=</span><span class="s2">&#34;My extension&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    org.opencontainers.image.description<span class="o">=</span><span class="s2">&#34;Your Desktop Extension Description&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    org.opencontainers.image.vendor<span class="o">=</span><span class="s2">&#34;Awesome Inc.&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    com.docker.desktop.extension.api.version<span class="o">=</span><span class="s2">&#34;0.3.3&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    com.docker.desktop.extension.icon<span class="o">=</span><span class="s2">&#34;https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    com.docker.extension.screenshots<span class="o">=</span><span class="s2">&#34;&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    com.docker.extension.detailed-description<span class="o">=</span><span class="s2">&#34;&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    com.docker.extension.publisher-url<span class="o">=</span><span class="s2">&#34;&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    com.docker.extension.additional-urls<span class="o">=</span><span class="s2">&#34;&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    com.docker.extension.changelog<span class="o">=</span><span class="s2">&#34;&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> metadata.json .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> docker.svg .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>client-builder /ui/build ui</span></span></code></pre></div>
      
    </div>
  </div>
</div>


  

<blockquote
  
  class="admonition not-prose">
  <p>Note</p>
<p>In the example Dockerfile, you can see that the image label <code>com.docker.desktop.extension.icon</code> is set to an icon URL. The Extensions Marketplace displays this icon without installing the extension. The Dockerfile also includes <code>COPY docker.svg .</code> to copy an icon file inside the image. This second icon file is used to display the extension UI in the Dashboard, once the extension is installed.</p>

  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Vue' && 'hidden'"
      >
        

  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 8V12M12 16H12.01M7.8 21H16.2C17.8802 21 18.7202 21 19.362 20.673C19.9265 20.3854 20.3854 19.9265 20.673 19.362C21 18.7202 21 17.8802 21 16.2V7.8C21 6.11984 21 5.27976 20.673 4.63803C20.3854 4.07354 19.9265 3.6146 19.362 3.32698C18.7202 3 17.8802 3 16.2 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Important
      </span>
    </div>
    <div class="admonition-content">
      <p>We don't have a working Dockerfile for Vue yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.1333218187=Vue" rel="noopener">Fill out the form</a>
and let us know if you'd like a Dockerfile for Vue.</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Angular' && 'hidden'"
      >
        

  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 8V12M12 16H12.01M7.8 21H16.2C17.8802 21 18.7202 21 19.362 20.673C19.9265 20.3854 20.3854 19.9265 20.673 19.362C21 18.7202 21 17.8802 21 16.2V7.8C21 6.11984 21 5.27976 20.673 4.63803C20.3854 4.07354 19.9265 3.6146 19.362 3.32698C18.7202 3 17.8802 3 16.2 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Important
      </span>
    </div>
    <div class="admonition-content">
      <p>We don't have a working Dockerfile for Angular yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.1333218187=Angular" rel="noopener">Fill out the form</a>
and let us know if you'd like a Dockerfile for Angular.</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Svelte' && 'hidden'"
      >
        

  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 8V12M12 16H12.01M7.8 21H16.2C17.8802 21 18.7202 21 19.362 20.673C19.9265 20.3854 20.3854 19.9265 20.673 19.362C21 18.7202 21 17.8802 21 16.2V7.8C21 6.11984 21 5.27976 20.673 4.63803C20.3854 4.07354 19.9265 3.6146 19.362 3.32698C18.7202 3 17.8802 3 16.2 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Important
      </span>
    </div>
    <div class="admonition-content">
      <p>We don't have a working Dockerfile for Svelte yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.1333218187=Svelte" rel="noopener">Fill out the form</a>
and let us know if you'd like a Dockerfile for Svelte.</p>
    </div>
  </blockquote>


      </div>
    
  </div>
</div>


## Configure the metadata file

In order to add a tab in Docker Desktop for your extension, you have to configure it in the `metadata.json`
file the root of your extension directory.

```json
{
  "icon": "docker.svg",
  "ui": {
    "dashboard-tab": {
      "title": "UI Extension",
      "root": "/ui",
      "src": "index.html"
    }
  }
}
```

The `title` property is the name of the extension that is displayed in the left-menu of the Docker Desktop Dashboard.
The `root` property is the path to the frontend application in the extension's container filesystem used by the
system to deploy it on the host.
The `src` property is the path to the HTML entry point of the frontend application within the `root` folder.

For more information on the `ui` section of the `metadata.json`, see [Metadata](../architecture/metadata.md#ui-section).

## Build the extension and install it

Now that you have configured the extension, you need to build the extension image that Docker Desktop will use to
install it.

```bash
docker build --tag=awesome-inc/my-extension:latest .
```

This built an image tagged `awesome-inc/my-extension:latest`, you can run `docker inspect
awesome-inc/my-extension:latest` to see more details about it.

Finally, you can install the extension and see it appearing in the Docker Desktop Dashboard.

```bash
docker extension install awesome-inc/my-extension:latest
```

## Use the Extension APIs client

To use the Extension APIs and perform actions with Docker Desktop, the extension must first import the
`@docker/extension-api-client` library. To install it, run the command below:

```bash
npm install @docker/extension-api-client
```

Then call the `createDockerDesktopClient` function to create a client object to call the extension APIs.

```js
import { createDockerDesktopClient } from '@docker/extension-api-client';

const ddClient = createDockerDesktopClient();
```

When using Typescript, you can also install `@docker/extension-api-client-types` as a dev dependency. This will
provide you with type definitions for the extension APIs and auto-completion in your IDE.

```bash
npm install @docker/extension-api-client-types --save-dev
```

![Auto completion in an IDE](images/types-autocomplete.png)

For example, you can use the `docker.cli.exec` function to get the list of all the containers via the `docker ps --all`
command and display the result in a table.








<div
  class="tabs"
  
    
      x-data="{ selected: 'React' }"
    
    @tab-select.window="$event.detail.group === 'framework' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'React' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'framework', name:
          'React'})"
        
      >
        React
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Vue' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'framework', name:
          'Vue'})"
        
      >
        Vue
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Angular' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'framework', name:
          'Angular'})"
        
      >
        Angular
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Svelte' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'framework', name:
          'Svelte'})"
        
      >
        Svelte
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'React' && 'hidden'"
      >
        <p>Replace the <code>ui/src/App.tsx</code> file with the following code:</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Ci8vIHVpL3NyYy9BcHAudHN4CmltcG9ydCBSZWFjdCwgeyB1c2VFZmZlY3QgfSBmcm9tICdyZWFjdCc7CmltcG9ydCB7CiAgUGFwZXIsCiAgU3RhY2ssCiAgVGFibGUsCiAgVGFibGVCb2R5LAogIFRhYmxlQ2VsbCwKICBUYWJsZUNvbnRhaW5lciwKICBUYWJsZUhlYWQsCiAgVGFibGVSb3csCiAgVHlwb2dyYXBoeQp9IGZyb20gIkBtdWkvbWF0ZXJpYWwiOwppbXBvcnQgeyBjcmVhdGVEb2NrZXJEZXNrdG9wQ2xpZW50IH0gZnJvbSAiQGRvY2tlci9leHRlbnNpb24tYXBpLWNsaWVudCI7CgovL29idGFpbiBkb2NrZXIgZGVza3RvcCBleHRlbnNpb24gY2xpZW50CmNvbnN0IGRkQ2xpZW50ID0gY3JlYXRlRG9ja2VyRGVza3RvcENsaWVudCgpOwoKZXhwb3J0IGZ1bmN0aW9uIEFwcCgpIHsKICBjb25zdCBbY29udGFpbmVycywgc2V0Q29udGFpbmVyc10gPSBSZWFjdC51c2VTdGF0ZTxhbnlbXT4oW10pOwoKICB1c2VFZmZlY3QoKCkgPT4gewogICAgLy8gTGlzdCBhbGwgY29udGFpbmVycwogICAgZGRDbGllbnQuZG9ja2VyLmNsaS5leGVjKCdwcycsIFsnLS1hbGwnLCAnLS1mb3JtYXQnLCAnInt7anNvbiAufX0iJ10pLnRoZW4oKHJlc3VsdCkgPT4gewogICAgICAvLyByZXN1bHQucGFyc2VKc29uTGluZXMoKSBwYXJzZXMgdGhlIG91dHB1dCBvZiB0aGUgY29tbWFuZCBpbnRvIGFuIGFycmF5IG9mIG9iamVjdHMKICAgICAgc2V0Q29udGFpbmVycyhyZXN1bHQucGFyc2VKc29uTGluZXMoKSk7CiAgICB9KTsKICB9LCBbXSk7CgogIHJldHVybiAoCiAgICA8U3RhY2s&#43;CiAgICAgIDxUeXBvZ3JhcGh5IGRhdGEtdGVzdGlkPSJoZWFkaW5nIiB2YXJpYW50PSJoMyIgcm9sZT0idGl0bGUiPgogICAgICAgIENvbnRhaW5lciBsaXN0CiAgICAgIDwvVHlwb2dyYXBoeT4KICAgICAgPFR5cG9ncmFwaHkKICAgICAgZGF0YS10ZXN0aWQ9InN1YmhlYWRpbmciCiAgICAgIHZhcmlhbnQ9ImJvZHkxIgogICAgICBjb2xvcj0idGV4dC5zZWNvbmRhcnkiCiAgICAgIHN4PXt7IG10OiAyIH19CiAgICA&#43;CiAgICAgIFNpbXBsZSBsaXN0IG9mIGNvbnRhaW5lcnMgdXNpbmcgRG9ja2VyIEV4dGVuc2lvbnMgU0RLLgogICAgICA8L1R5cG9ncmFwaHk&#43;CiAgICAgIDxUYWJsZUNvbnRhaW5lciBzeD17e210OjJ9fT4KICAgICAgICA8VGFibGU&#43;CiAgICAgICAgICA8VGFibGVIZWFkPgogICAgICAgICAgICA8VGFibGVSb3c&#43;CiAgICAgICAgICAgICAgPFRhYmxlQ2VsbD5Db250YWluZXIgaWQ8L1RhYmxlQ2VsbD4KICAgICAgICAgICAgICA8VGFibGVDZWxsPkltYWdlPC9UYWJsZUNlbGw&#43;CiAgICAgICAgICAgICAgPFRhYmxlQ2VsbD5Db21tYW5kPC9UYWJsZUNlbGw&#43;CiAgICAgICAgICAgICAgPFRhYmxlQ2VsbD5DcmVhdGVkPC9UYWJsZUNlbGw&#43;CiAgICAgICAgICAgICAgPFRhYmxlQ2VsbD5TdGF0dXM8L1RhYmxlQ2VsbD4KICAgICAgICAgICAgPC9UYWJsZVJvdz4KICAgICAgICAgIDwvVGFibGVIZWFkPgogICAgICAgICAgPFRhYmxlQm9keT4KICAgICAgICAgICAge2NvbnRhaW5lcnMubWFwKChjb250YWluZXIpID0&#43;ICgKICAgICAgICAgICAgICA8VGFibGVSb3cKICAgICAgICAgICAgICAgIGtleT17Y29udGFpbmVyLklEfQogICAgICAgICAgICAgICAgc3g9e3sgJyY6bGFzdC1jaGlsZCB0ZCwgJjpsYXN0LWNoaWxkIHRoJzogeyBib3JkZXI6IDAgfSB9fQogICAgICAgICAgICAgID4KICAgICAgICAgICAgICAgIDxUYWJsZUNlbGw&#43;e2NvbnRhaW5lci5JRH08L1RhYmxlQ2VsbD4KICAgICAgICAgICAgICAgIDxUYWJsZUNlbGw&#43;e2NvbnRhaW5lci5JbWFnZX08L1RhYmxlQ2VsbD4KICAgICAgICAgICAgICAgIDxUYWJsZUNlbGw&#43;e2NvbnRhaW5lci5Db21tYW5kfTwvVGFibGVDZWxsPgogICAgICAgICAgICAgICAgPFRhYmxlQ2VsbD57Y29udGFpbmVyLkNyZWF0ZWRBdH08L1RhYmxlQ2VsbD4KICAgICAgICAgICAgICAgIDxUYWJsZUNlbGw&#43;e2NvbnRhaW5lci5TdGF0dXN9PC9UYWJsZUNlbGw&#43;CiAgICAgICAgICAgICAgPC9UYWJsZVJvdz4KICAgICAgICAgICAgKSl9CiAgICAgICAgICA8L1RhYmxlQm9keT4KICAgICAgICA8L1RhYmxlPgogICAgICA8L1RhYmxlQ29udGFpbmVyPgogICAgPC9TdGFjaz4KICApOwp9', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-tsx" data-lang="tsx"><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1">// ui/src/App.tsx
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="kr">import</span> <span class="nx">React</span><span class="p">,</span> <span class="p">{</span> <span class="nx">useEffect</span> <span class="p">}</span> <span class="kr">from</span> <span class="s1">&#39;react&#39;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl"><span class="kr">import</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">  <span class="nx">Paper</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nx">Stack</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nx">Table</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nx">TableBody</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nx">TableCell</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nx">TableContainer</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nx">TableHead</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nx">TableRow</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nx">Typography</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span> <span class="kr">from</span> <span class="s2">&#34;@mui/material&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl"><span class="kr">import</span> <span class="p">{</span> <span class="nx">createDockerDesktopClient</span> <span class="p">}</span> <span class="kr">from</span> <span class="s2">&#34;@docker/extension-api-client&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1">//obtain docker desktop extension client
</span></span></span><span class="line"><span class="cl"><span class="c1"></span><span class="kr">const</span> <span class="nx">ddClient</span> <span class="o">=</span> <span class="nx">createDockerDesktopClient</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">export</span> <span class="kd">function</span> <span class="nx">App() {</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="p">[</span><span class="nx">containers</span><span class="p">,</span> <span class="nx">setContainers</span><span class="p">]</span> <span class="o">=</span> <span class="nx">React</span><span class="p">.</span><span class="nx">useState</span><span class="p">&lt;</span><span class="nt">any</span><span class="err">[]</span><span class="p">&gt;([]);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">useEffect</span><span class="p">(()</span> <span class="o">=&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="c1">// List all containers
</span></span></span><span class="line"><span class="cl"><span class="c1"></span>    <span class="nx">ddClient</span><span class="p">.</span><span class="nx">docker</span><span class="p">.</span><span class="nx">cli</span><span class="p">.</span><span class="nx">exec</span><span class="p">(</span><span class="s1">&#39;ps&#39;</span><span class="p">,</span> <span class="p">[</span><span class="s1">&#39;--all&#39;</span><span class="p">,</span> <span class="s1">&#39;--format&#39;</span><span class="p">,</span> <span class="s1">&#39;&#34;{{json .}}&#34;&#39;</span><span class="p">]).</span><span class="nx">then</span><span class="p">((</span><span class="nx">result</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="c1">// result.parseJsonLines() parses the output of the command into an array of objects
</span></span></span><span class="line"><span class="cl"><span class="c1"></span>      <span class="nx">setContainers</span><span class="p">(</span><span class="nx">result</span><span class="p">.</span><span class="nx">parseJsonLines</span><span class="p">());</span>
</span></span><span class="line"><span class="cl">    <span class="p">});</span>
</span></span><span class="line"><span class="cl">  <span class="p">},</span> <span class="p">[]);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">return</span> <span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="p">&lt;</span><span class="nt">Stack</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">      <span class="p">&lt;</span><span class="nt">Typography</span> <span class="na">data-testid</span><span class="o">=</span><span class="s">&#34;heading&#34;</span> <span class="na">variant</span><span class="o">=</span><span class="s">&#34;h3&#34;</span> <span class="na">role</span><span class="o">=</span><span class="s">&#34;title&#34;</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">        <span class="nx">Container</span> <span class="nx">list</span>
</span></span><span class="line"><span class="cl">      <span class="p">&lt;/</span><span class="nt">Typography</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">      <span class="p">&lt;</span><span class="nt">Typography</span>
</span></span><span class="line"><span class="cl">      <span class="na">data-testid</span><span class="o">=</span><span class="s">&#34;subheading&#34;</span>
</span></span><span class="line"><span class="cl">      <span class="na">variant</span><span class="o">=</span><span class="s">&#34;body1&#34;</span>
</span></span><span class="line"><span class="cl">      <span class="na">color</span><span class="o">=</span><span class="s">&#34;text.secondary&#34;</span>
</span></span><span class="line"><span class="cl">      <span class="na">sx</span><span class="o">=</span><span class="p">{{</span> <span class="nx">mt</span>: <span class="kt">2</span> <span class="p">}}</span>
</span></span><span class="line"><span class="cl">    <span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">      <span class="nx">Simple</span> <span class="nx">list</span> <span class="k">of</span> <span class="nx">containers</span> <span class="nx">using</span> <span class="nx">Docker</span> <span class="nx">Extensions</span> <span class="nx">SDK</span><span class="p">.</span>
</span></span><span class="line"><span class="cl">      <span class="p">&lt;/</span><span class="nt">Typography</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">      <span class="p">&lt;</span><span class="nt">TableContainer</span> <span class="na">sx</span><span class="o">=</span><span class="p">{{</span><span class="nx">mt</span>:<span class="kt">2</span><span class="p">}}&gt;</span>
</span></span><span class="line"><span class="cl">        <span class="p">&lt;</span><span class="nt">Table</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">          <span class="p">&lt;</span><span class="nt">TableHead</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">            <span class="p">&lt;</span><span class="nt">TableRow</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">              <span class="p">&lt;</span><span class="nt">TableCell</span><span class="p">&gt;</span><span class="nx">Container</span> <span class="nx">id</span><span class="p">&lt;/</span><span class="nt">TableCell</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">              <span class="p">&lt;</span><span class="nt">TableCell</span><span class="p">&gt;</span><span class="nx">Image</span><span class="p">&lt;/</span><span class="nt">TableCell</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">              <span class="p">&lt;</span><span class="nt">TableCell</span><span class="p">&gt;</span><span class="nx">Command</span><span class="p">&lt;/</span><span class="nt">TableCell</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">              <span class="p">&lt;</span><span class="nt">TableCell</span><span class="p">&gt;</span><span class="nx">Created</span><span class="p">&lt;/</span><span class="nt">TableCell</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">              <span class="p">&lt;</span><span class="nt">TableCell</span><span class="p">&gt;</span><span class="nx">Status</span><span class="p">&lt;/</span><span class="nt">TableCell</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">            <span class="p">&lt;/</span><span class="nt">TableRow</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">          <span class="p">&lt;/</span><span class="nt">TableHead</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">          <span class="p">&lt;</span><span class="nt">TableBody</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">            <span class="p">{</span><span class="nx">containers</span><span class="p">.</span><span class="nx">map</span><span class="p">((</span><span class="nx">container</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="p">(</span>
</span></span><span class="line"><span class="cl">              <span class="p">&lt;</span><span class="nt">TableRow</span>
</span></span><span class="line"><span class="cl">                <span class="na">key</span><span class="o">=</span><span class="p">{</span><span class="nx">container</span><span class="p">.</span><span class="nx">ID</span><span class="p">}</span>
</span></span><span class="line"><span class="cl">                <span class="na">sx</span><span class="o">=</span><span class="p">{{</span> <span class="s1">&#39;&amp;:last-child td, &amp;:last-child th&#39;</span><span class="o">:</span> <span class="p">{</span> <span class="nx">border</span>: <span class="kt">0</span> <span class="p">}</span> <span class="p">}}</span>
</span></span><span class="line"><span class="cl">              <span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">                <span class="p">&lt;</span><span class="nt">TableCell</span><span class="p">&gt;{</span><span class="nx">container</span><span class="p">.</span><span class="nx">ID</span><span class="p">}&lt;/</span><span class="nt">TableCell</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">                <span class="p">&lt;</span><span class="nt">TableCell</span><span class="p">&gt;{</span><span class="nx">container</span><span class="p">.</span><span class="nx">Image</span><span class="p">}&lt;/</span><span class="nt">TableCell</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">                <span class="p">&lt;</span><span class="nt">TableCell</span><span class="p">&gt;{</span><span class="nx">container</span><span class="p">.</span><span class="nx">Command</span><span class="p">}&lt;/</span><span class="nt">TableCell</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">                <span class="p">&lt;</span><span class="nt">TableCell</span><span class="p">&gt;{</span><span class="nx">container</span><span class="p">.</span><span class="nx">CreatedAt</span><span class="p">}&lt;/</span><span class="nt">TableCell</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">                <span class="p">&lt;</span><span class="nt">TableCell</span><span class="p">&gt;{</span><span class="nx">container</span><span class="p">.</span><span class="nx">Status</span><span class="p">}&lt;/</span><span class="nt">TableCell</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">              <span class="p">&lt;/</span><span class="nt">TableRow</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">            <span class="p">))}</span>
</span></span><span class="line"><span class="cl">          <span class="p">&lt;/</span><span class="nt">TableBody</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">        <span class="p">&lt;/</span><span class="nt">Table</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">      <span class="p">&lt;/</span><span class="nt">TableContainer</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">    <span class="p">&lt;/</span><span class="nt">Stack</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/extensions/extensions-sdk/build/images/react-extension.png"
    alt="Screenshot of the container list."
    
    
    class="mx-auto rounded-sm"
  />
  
  <template x-teleport="body">
    <div
      x-show="zoom"
      @click="zoom = false"
      x-transition.opacity.duration.250ms
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/100 p-6"
    >
      <button class="icon-svg fixed top-6 right-8 z-30 text-white">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-438 270-228q-9 9-21 9t-21-9q-9-9-9-21t9-21l210-210-210-210q-9-9-9-21t9-21q9-9 21-9t21 9l210 210 210-210q9-9 21-9t21 9q9 9 9 21t-9 21L522-480l210 210q9 9 9 21t-9 21q-9 9-21 9t-21-9L480-438Z"/></svg>
      </button>
      <img
        loading="lazy"
        class="max-h-full max-w-full rounded-sm"
        src="/extensions/extensions-sdk/build/images/react-extension.png"
        alt="Screenshot of the container list."
      />
    </div>
  </template>
</figure>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Vue' && 'hidden'"
      >
        

  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 8V12M12 16H12.01M7.8 21H16.2C17.8802 21 18.7202 21 19.362 20.673C19.9265 20.3854 20.3854 19.9265 20.673 19.362C21 18.7202 21 17.8802 21 16.2V7.8C21 6.11984 21 5.27976 20.673 4.63803C20.3854 4.07354 19.9265 3.6146 19.362 3.32698C18.7202 3 17.8802 3 16.2 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Important
      </span>
    </div>
    <div class="admonition-content">
      <p>We don't have an example for Vue yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.1333218187=Vue" rel="noopener">Fill out the form</a>
and let us know if you'd like a sample with Vue.</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Angular' && 'hidden'"
      >
        

  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 8V12M12 16H12.01M7.8 21H16.2C17.8802 21 18.7202 21 19.362 20.673C19.9265 20.3854 20.3854 19.9265 20.673 19.362C21 18.7202 21 17.8802 21 16.2V7.8C21 6.11984 21 5.27976 20.673 4.63803C20.3854 4.07354 19.9265 3.6146 19.362 3.32698C18.7202 3 17.8802 3 16.2 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Important
      </span>
    </div>
    <div class="admonition-content">
      <p>We don't have an example for Angular yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.1333218187=Angular" rel="noopener">Fill out the form</a>
and let us know if you'd like a sample with Angular.</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Svelte' && 'hidden'"
      >
        

  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 8V12M12 16H12.01M7.8 21H16.2C17.8802 21 18.7202 21 19.362 20.673C19.9265 20.3854 20.3854 19.9265 20.673 19.362C21 18.7202 21 17.8802 21 16.2V7.8C21 6.11984 21 5.27976 20.673 4.63803C20.3854 4.07354 19.9265 3.6146 19.362 3.32698C18.7202 3 17.8802 3 16.2 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Important
      </span>
    </div>
    <div class="admonition-content">
      <p>We don't have an example for Svelte yet. <a class="link" href="https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&amp;entry.1333218187=Svelte" rel="noopener">Fill out the form</a>
and let us know if you'd like a sample with Svelte.</p>
    </div>
  </blockquote>


      </div>
    
  </div>
</div>


## Policies enforced for the front-end code

Extension UI code is rendered in a separate electron session and doesn't have a node.js environment initialized, nor direct access to the electron APIs. 

This is to limit the possible unexpected side effects to the overall Docker Dashboard.

The extension UI code can't perform privileged tasks, such as making changes to the system, or spawning sub-processes, except by using the SDK APIs provided with the extension framework.
The Extension UI code can also perform interactions with Docker Desktop, such as navigating to various places in the Dashboard, only through the extension SDK APIs.

Extensions UI parts are isolated from each other and extension UI code is running in its own session for each extension. Extensions can't access other extensions’ session data.

`localStorage` is one of the mechanisms of a browser’s web storage. It allows users to save data as key-value pairs in the browser for later use. `localStorage` doesn't clear data when the browser (the extension pane) closes. This makes it ideal for persisting data when navigating out of the extension to other parts of Docker Desktop.

If your extension uses `localStorage` to store data, other extensions running in Docker Desktop can't access the local storage of your extension. The extension’s local storage is persisted even after Docker Desktop is stopped or restarted. When an extension is upgraded, its local storage is persisted, whereas when it is uninstalled, its local storage is completely removed.

## Re-build the extension and update it

Since you have modified the code of the extension, you must build again the extension.

```console
$ docker build --tag=awesome-inc/my-extension:latest .
```

Once built, you need to update it.

```console
$ docker extension update awesome-inc/my-extension:latest
```

Now you can see the backend service running in the containers tab of the Docker Desktop Dashboard and watch the logs
when you need to debug it.

> [!TIP]
>
> You can turn on [hot reloading](../dev/test-debug.md#hot-reloading-whilst-developing-the-ui) to avoid the need to
> rebuild the extension every time you make a change.

## What's next?

- Add a [backend](backend-extension-tutorial.md) to your extension.
- Learn how to [test and debug](../dev/test-debug.md) your extension.
- Learn how to [setup CI for your extension](../dev/continuous-integration.md).
- Learn more about extensions [architecture](../architecture/_index.md).
- For more information and guidelines on building the UI, see the [Design and UI styling section](../design/design-guidelines.md).
- If you want to set up user authentication for the extension, see [Authentication](../guides/oauth2-flow.md).

