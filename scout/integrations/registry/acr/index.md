# 将 Docker Scout 与 Azure Container Registry 集成

将 Docker Scout 与 Azure Container Registry (ACR) 集成后，您可以查看托管在 ACR 仓库中的镜像的洞察信息。在将 Docker Scout 与 ACR 集成并为仓库激活 Docker Scout 后，向仓库推送镜像将自动触发镜像分析。您可以使用 Docker Scout Dashboard 或 `docker scout` CLI 命令查看镜像洞察信息。

## 工作原理

为帮助您实现 Azure Container Registry 与 Docker Scout 的集成，您可以使用一个自定义的 Azure Resource Manager (ARM) 模板，该模板会自动为您在 Azure 中创建必要的基础设施：

- 用于镜像推送和删除事件的 EventGrid 主题和订阅。
- 用于注册表的只读授权令牌，用于列出仓库并提取镜像。

当资源已在 Azure 中创建后，您可以在集成的 ACR 实例中为镜像仓库启用集成。一旦您启用了一个仓库，推送新镜像将自动触发镜像分析。分析结果将显示在 Docker Scout Dashboard 中。

如果您在已包含镜像的仓库上启用集成，Docker Scout 会自动拉取并分析最新的镜像版本。

### ARM 模板

下表描述了配置资源。

> [!NOTE]
>
> 创建这些资源会在 Azure 账户上产生少量持续费用。
> 表中的 **费用** 列表示当集成每天推送 100 个镜像的 ACR 注册表时，这些资源的估计月费用。
>
> 出口费用根据使用情况而变化，但大约为每 GB 0.1 美元，前 100 GB 免费。

| Azure                   | 资源                                                                                   | 费用                                              |
| ----------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| Event Grid 系统主题 | 订阅 Azure Container Registry 事件（镜像推送和镜像删除）                 | 免费                                              |
| 事件订阅      | 通过 Webhook 订阅将 Event Grid 事件发送到 Scout                                 | 每 100 万条消息 0.60 美元。前 10 万条免费。 |
| 注册表令牌          | 用于 Scout 列出仓库并从注册表拉取镜像的只读令牌 | 免费                                              |

以下 JSON 文档显示了 Docker Scout 用于创建 Azure 资源的 ARM 模板。






<div
  id="json-模板"
  x-data="{ open: false }"
  class="my-6 rounded-sm border border-gray-200 bg-white py-2 dark:border-gray-700 dark:bg-gray-900"
>
  <button
    class="not-prose flex w-full justify-between px-4 py-2"
    x-on:click="open = ! open"
  >
    <div class=" flex items-center gap-2">
      JSON 模板
    </div>
    <span :class="{ 'hidden' : !open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
    >
    <span :class="{ 'hidden' : open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
    >
  </button>
  <div x-show="open" x-collapse class="px-4">
    <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ewogICAiJHNjaGVtYSI6ICJodHRwczovL3NjaGVtYS5tYW5hZ2VtZW50LmF6dXJlLmNvbS9zY2hlbWFzLzIwMTktMDQtMDEvZGVwbG95bWVudFRlbXBsYXRlLmpzb24jIiwKICAgImNvbnRlbnRWZXJzaW9uIjogIjEuMC4wLjAiLAogICAicGFyYW1ldGVycyI6IHsKICAgICAgIkRvY2tlclNjb3V0V2ViaG9vayI6IHsKICAgICAgICAgIm1ldGFkYXRhIjogewogICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiRXZlbnRHcmlkJ3Mgc3Vic2NyaXB0aW9uIFdlYmhvb2siCiAgICAgICAgIH0sCiAgICAgICAgICJ0eXBlIjogIlN0cmluZyIKICAgICAgfSwKICAgICAgIlJlZ2lzdHJ5TmFtZSI6IHsKICAgICAgICAgIm1ldGFkYXRhIjogewogICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiTmFtZSBvZiB0aGUgcmVnaXN0cnkgdG8gYWRkIERvY2tlciBTY291dCIKICAgICAgICAgfSwKICAgICAgICAgInR5cGUiOiAiU3RyaW5nIgogICAgICB9LAogICAgICAic3lzdGVtVG9waWNzX2RvY2tlclNjb3V0UmVwb3NpdG9yeSI6IHsKICAgICAgICAgImRlZmF1bHRWYWx1ZSI6ICJkb2NrZXItc2NvdXQtcmVwb3NpdG9yeSIsCiAgICAgICAgICJtZXRhZGF0YSI6IHsKICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIkV2ZW50R3JpZCdzIHRvcGljIG5hbWUiCiAgICAgICAgIH0sCiAgICAgICAgICJ0eXBlIjogIlN0cmluZyIKICAgICAgfQogICB9LAogICAicmVzb3VyY2VzIjogWwogICAgICB7CiAgICAgICAgICJhcGlWZXJzaW9uIjogIjIwMjMtMDYtMDEtcHJldmlldyIsCiAgICAgICAgICJpZGVudGl0eSI6IHsKICAgICAgICAgICAgInR5cGUiOiAiTm9uZSIKICAgICAgICAgfSwKICAgICAgICAgImxvY2F0aW9uIjogIltyZXNvdXJjZUdyb3VwKCkubG9jYXRpb25dIiwKICAgICAgICAgIm5hbWUiOiAiW3BhcmFtZXRlcnMoJ3N5c3RlbVRvcGljc19kb2NrZXJTY291dFJlcG9zaXRvcnknKV0iLAogICAgICAgICAicHJvcGVydGllcyI6IHsKICAgICAgICAgICAgInNvdXJjZSI6ICJbZXh0ZW5zaW9uUmVzb3VyY2VJZChyZXNvdXJjZUdyb3VwKCkuSWQgLCAnTWljcm9zb2Z0LkNvbnRhaW5lclJlZ2lzdHJ5L1JlZ2lzdHJpZXMnLCBwYXJhbWV0ZXJzKCdSZWdpc3RyeU5hbWUnKSldIiwKICAgICAgICAgICAgInRvcGljVHlwZSI6ICJNaWNyb3NvZnQuQ29udGFpbmVyUmVnaXN0cnkuUmVnaXN0cmllcyIKICAgICAgICAgfSwKICAgICAgICAgInR5cGUiOiAiTWljcm9zb2Z0LkV2ZW50R3JpZC9zeXN0ZW1Ub3BpY3MiCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAgImFwaVZlcnNpb24iOiAiMjAyMy0wNi0wMS1wcmV2aWV3IiwKICAgICAgICAgImRlcGVuZHNPbiI6IFsKICAgICAgICAgICAgIltyZXNvdXJjZUlkKCdNaWNyb3NvZnQuRXZlbnRHcmlkL3N5c3RlbVRvcGljcycsIHBhcmFtZXRlcnMoJ3N5c3RlbVRvcGljc19kb2NrZXJTY291dFJlcG9zaXRvcnknKSldIgogICAgICAgICBdLAogICAgICAgICAibmFtZSI6ICJbY29uY2F0KHBhcmFtZXRlcnMoJ3N5c3RlbVRvcGljc19kb2NrZXJTY291dFJlcG9zaXRvcnknKSwgJy9pbWFnZS1jaGFuZ2UnKV0iLAogICAgICAgICAicHJvcGVydGllcyI6IHsKICAgICAgICAgICAgImRlc3RpbmF0aW9uIjogewogICAgICAgICAgICAgICAiZW5kcG9pbnRUeXBlIjogIldlYkhvb2siLAogICAgICAgICAgICAgICAicHJvcGVydGllcyI6IHsKICAgICAgICAgICAgICAgICAgImVuZHBvaW50VXJsIjogIltwYXJhbWV0ZXJzKCdEb2NrZXJTY291dFdlYmhvb2snKV0iLAogICAgICAgICAgICAgICAgICAibWF4RXZlbnRzUGVyQmF0Y2giOiAxLAogICAgICAgICAgICAgICAgICAicHJlZmVycmVkQmF0Y2hTaXplSW5LaWxvYnl0ZXMiOiA2NAogICAgICAgICAgICAgICB9CiAgICAgICAgICAgIH0sCiAgICAgICAgICAgICJldmVudERlbGl2ZXJ5U2NoZW1hIjogIkV2ZW50R3JpZFNjaGVtYSIsCiAgICAgICAgICAgICJmaWx0ZXIiOiB7CiAgICAgICAgICAgICAgICJlbmFibGVBZHZhbmNlZEZpbHRlcmluZ09uQXJyYXlzIjogdHJ1ZSwKICAgICAgICAgICAgICAgImluY2x1ZGVkRXZlbnRUeXBlcyI6IFsKICAgICAgICAgICAgICAgICAgIk1pY3Jvc29mdC5Db250YWluZXJSZWdpc3RyeS5JbWFnZVB1c2hlZCIsCiAgICAgICAgICAgICAgICAgICJNaWNyb3NvZnQuQ29udGFpbmVyUmVnaXN0cnkuSW1hZ2VEZWxldGVkIgogICAgICAgICAgICAgICBdCiAgICAgICAgICAgIH0sCiAgICAgICAgICAgICJsYWJlbHMiOiBbXSwKICAgICAgICAgICAgInJldHJ5UG9saWN5IjogewogICAgICAgICAgICAgICAiZXZlbnRUaW1lVG9MaXZlSW5NaW51dGVzIjogMTQ0MCwKICAgICAgICAgICAgICAgIm1heERlbGl2ZXJ5QXR0ZW1wdHMiOiAzMAogICAgICAgICAgICB9CiAgICAgICAgIH0sCiAgICAgICAgICJ0eXBlIjogIk1pY3Jvc29mdC5FdmVudEdyaWQvc3lzdGVtVG9waWNzL2V2ZW50U3Vic2NyaXB0aW9ucyIKICAgICAgfSwKICAgICAgewogICAgICAgICAiYXBpVmVyc2lvbiI6ICIyMDIzLTAxLTAxLXByZXZpZXciLAogICAgICAgICAibmFtZSI6ICJbY29uY2F0KHBhcmFtZXRlcnMoJ1JlZ2lzdHJ5TmFtZScpLCAnL2RvY2tlci1zY291dC1yZWFkb25seS10b2tlbicpXSIsCiAgICAgICAgICJwcm9wZXJ0aWVzIjogewogICAgICAgICAgICAiY3JlZGVudGlhbHMiOiB7fSwKICAgICAgICAgICAgInNjb3BlTWFwSWQiOiAiW3Jlc291cmNlSWQoJ01pY3Jvc29mdC5Db250YWluZXJSZWdpc3RyeS9yZWdpc3RyaWVzL3Njb3BlTWFwcycsIHBhcmFtZXRlcnMoJ1JlZ2lzdHJ5TmFtZScpLCAnX3JlcG9zaXRvcmllc19wdWxsX21ldGFkYXRhX3JlYWQnKV0iCiAgICAgICAgIH0sCiAgICAgICAgICJ0eXBlIjogIk1pY3Jvc29mdC5Db250YWluZXJSZWdpc3RyeS9yZWdpc3RyaWVzL3Rva2VucyIKICAgICAgfQogICBdLAogICAidmFyaWFibGVzIjoge30KfQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-json" data-lang="json"><span class="line"><span class="cl"><span class="p">{</span>
</span></span><span class="line"><span class="cl">   <span class="nt">&#34;$schema&#34;</span><span class="p">:</span> <span class="s2">&#34;https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">   <span class="nt">&#34;contentVersion&#34;</span><span class="p">:</span> <span class="s2">&#34;1.0.0.0&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">   <span class="nt">&#34;parameters&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nt">&#34;DockerScoutWebhook&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;metadata&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;description&#34;</span><span class="p">:</span> <span class="s2">&#34;EventGrid&#39;s subscription Webhook&#34;</span>
</span></span><span class="line"><span class="cl">         <span class="p">},</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;type&#34;</span><span class="p">:</span> <span class="s2">&#34;String&#34;</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">      <span class="nt">&#34;RegistryName&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;metadata&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;description&#34;</span><span class="p">:</span> <span class="s2">&#34;Name of the registry to add Docker Scout&#34;</span>
</span></span><span class="line"><span class="cl">         <span class="p">},</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;type&#34;</span><span class="p">:</span> <span class="s2">&#34;String&#34;</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">      <span class="nt">&#34;systemTopics_dockerScoutRepository&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;defaultValue&#34;</span><span class="p">:</span> <span class="s2">&#34;docker-scout-repository&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;metadata&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;description&#34;</span><span class="p">:</span> <span class="s2">&#34;EventGrid&#39;s topic name&#34;</span>
</span></span><span class="line"><span class="cl">         <span class="p">},</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;type&#34;</span><span class="p">:</span> <span class="s2">&#34;String&#34;</span>
</span></span><span class="line"><span class="cl">      <span class="p">}</span>
</span></span><span class="line"><span class="cl">   <span class="p">},</span>
</span></span><span class="line"><span class="cl">   <span class="nt">&#34;resources&#34;</span><span class="p">:</span> <span class="p">[</span>
</span></span><span class="line"><span class="cl">      <span class="p">{</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;apiVersion&#34;</span><span class="p">:</span> <span class="s2">&#34;2023-06-01-preview&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;identity&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;type&#34;</span><span class="p">:</span> <span class="s2">&#34;None&#34;</span>
</span></span><span class="line"><span class="cl">         <span class="p">},</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;location&#34;</span><span class="p">:</span> <span class="s2">&#34;[resourceGroup().location]&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;name&#34;</span><span class="p">:</span> <span class="s2">&#34;[parameters(&#39;systemTopics_dockerScoutRepository&#39;)]&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;properties&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;source&#34;</span><span class="p">:</span> <span class="s2">&#34;[extensionResourceId(resourceGroup().Id , &#39;Microsoft.ContainerRegistry/Registries&#39;, parameters(&#39;RegistryName&#39;))]&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;topicType&#34;</span><span class="p">:</span> <span class="s2">&#34;Microsoft.ContainerRegistry.Registries&#34;</span>
</span></span><span class="line"><span class="cl">         <span class="p">},</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;type&#34;</span><span class="p">:</span> <span class="s2">&#34;Microsoft.EventGrid/systemTopics&#34;</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">      <span class="p">{</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;apiVersion&#34;</span><span class="p">:</span> <span class="s2">&#34;2023-06-01-preview&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;dependsOn&#34;</span><span class="p">:</span> <span class="p">[</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;[resourceId(&#39;Microsoft.EventGrid/systemTopics&#39;, parameters(&#39;systemTopics_dockerScoutRepository&#39;))]&#34;</span>
</span></span><span class="line"><span class="cl">         <span class="p">],</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;name&#34;</span><span class="p">:</span> <span class="s2">&#34;[concat(parameters(&#39;systemTopics_dockerScoutRepository&#39;), &#39;/image-change&#39;)]&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;properties&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;destination&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">               <span class="nt">&#34;endpointType&#34;</span><span class="p">:</span> <span class="s2">&#34;WebHook&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">               <span class="nt">&#34;properties&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                  <span class="nt">&#34;endpointUrl&#34;</span><span class="p">:</span> <span class="s2">&#34;[parameters(&#39;DockerScoutWebhook&#39;)]&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">                  <span class="nt">&#34;maxEventsPerBatch&#34;</span><span class="p">:</span> <span class="mi">1</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">                  <span class="nt">&#34;preferredBatchSizeInKilobytes&#34;</span><span class="p">:</span> <span class="mi">64</span>
</span></span><span class="line"><span class="cl">               <span class="p">}</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;eventDeliverySchema&#34;</span><span class="p">:</span> <span class="s2">&#34;EventGridSchema&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;filter&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">               <span class="nt">&#34;enableAdvancedFilteringOnArrays&#34;</span><span class="p">:</span> <span class="kc">true</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">               <span class="nt">&#34;includedEventTypes&#34;</span><span class="p">:</span> <span class="p">[</span>
</span></span><span class="line"><span class="cl">                  <span class="s2">&#34;Microsoft.ContainerRegistry.ImagePushed&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">                  <span class="s2">&#34;Microsoft.ContainerRegistry.ImageDeleted&#34;</span>
</span></span><span class="line"><span class="cl">               <span class="p">]</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;labels&#34;</span><span class="p">:</span> <span class="p">[],</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;retryPolicy&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">               <span class="nt">&#34;eventTimeToLiveInMinutes&#34;</span><span class="p">:</span> <span class="mi">1440</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">               <span class="nt">&#34;maxDeliveryAttempts&#34;</span><span class="p">:</span> <span class="mi">30</span>
</span></span><span class="line"><span class="cl">            <span class="p">}</span>
</span></span><span class="line"><span class="cl">         <span class="p">},</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;type&#34;</span><span class="p">:</span> <span class="s2">&#34;Microsoft.EventGrid/systemTopics/eventSubscriptions&#34;</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">      <span class="p">{</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;apiVersion&#34;</span><span class="p">:</span> <span class="s2">&#34;2023-01-01-preview&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;name&#34;</span><span class="p">:</span> <span class="s2">&#34;[concat(parameters(&#39;RegistryName&#39;), &#39;/docker-scout-readonly-token&#39;)]&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;properties&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;credentials&#34;</span><span class="p">:</span> <span class="p">{},</span>
</span></span><span class="line"><span class="cl">            <span class="nt">&#34;scopeMapId&#34;</span><span class="p">:</span> <span class="s2">&#34;[resourceId(&#39;Microsoft.ContainerRegistry/registries/scopeMaps&#39;, parameters(&#39;RegistryName&#39;), &#39;_repositories_pull_metadata_read&#39;)]&#34;</span>
</span></span><span class="line"><span class="cl">         <span class="p">},</span>
</span></span><span class="line"><span class="cl">         <span class="nt">&#34;type&#34;</span><span class="p">:</span> <span class="s2">&#34;Microsoft.ContainerRegistry/registries/tokens&#34;</span>
</span></span><span class="line"><span class="cl">      <span class="p">}</span>
</span></span><span class="line"><span class="cl">   <span class="p">],</span>
</span></span><span class="line"><span class="cl">   <span class="nt">&#34;variables&#34;</span><span class="p">:</span> <span class="p">{}</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

  </div>
</div>



## 集成注册表

1. 转到 Docker Scout Dashboard 上的 [ACR 集成页面](https://scout.docker.com/settings/integrations/azure/)。
2. 在 **如何集成** 部分，输入您要集成的注册表的 **注册表主机名**。
3. 选择 **下一步**。
4. 选择 **部署到 Azure** 以在 Azure 中打开模板部署向导。

   如果您尚未登录 Azure 账户，可能会提示您登录。

5. 在模板向导中，配置您的部署：

   - **资源组**：输入与容器注册表使用的相同资源组。Docker Scout 资源必须部署到与注册表相同的资源组中。

   - **注册表名称**：该字段已预填充注册表主机名的子域名。

6. 选择 **查看 + 创建**，然后选择 **创建** 以部署模板。

7. 等待部署完成。
8. 在 **部署详细信息** 部分，点击新创建的 **容器注册表令牌** 类型的资源。为此令牌生成一个新密码。
    
    或者，使用 Azure 中的搜索功能导航到您希望集成的 **容器注册表** 资源，并为创建的访问令牌生成新密码。

9. 复制生成的密码，然后返回 Docker Scout Dashboard 以完成集成。
10. 将生成的密码粘贴到 **注册表令牌** 字段中。
11. 选择 **启用集成**。

选择 **启用集成** 后，Docker Scout 将执行连接测试以验证集成。如果验证成功，您将被重定向到 Azure 注册表摘要页面，该页面显示当前组织的所有 Azure 集成。

接下来，在 [仓库设置](https://scout.docker.com/settings/repos/) 中为您希望分析的仓库激活 Docker Scout。

激活仓库后，您推送的镜像将由 Docker Scout 分析。分析结果将显示在 Docker Scout Dashboard 中。如果您的仓库已包含镜像，Docker Scout 会自动拉取并分析最新的镜像版本。

## 移除集成

> [!IMPORTANT]
>
> 在 Docker Scout Dashboard 中移除集成不会自动移除在 Azure 中创建的资源。

要移除 ACR 集成：

1. 转到 Docker Scout Dashboard 上的 [ACR 集成页面](https://scout.docker.com/settings/integrations/azure/)。
2. 找到您要移除的 ACR 集成，然后选择 **移除** 按钮。
3. 在打开的对话框中，通过选择 **移除** 进行确认。
4. 在 Docker Scout Dashboard 中移除集成后，还需移除与集成相关的 Azure 资源：

   - 容器注册表的 `docker-scout-readonly-token` 令牌。
   - `docker-scout-repository` Event Grid 系统主题。
