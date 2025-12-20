# 将 Docker Scout 与 GitHub 集成





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    
      
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Availability:</span>
        <span>
          Beta
          
            
              <span class="icon-svg"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M360-360H217q-18 0-26.5-16t2.5-31l338-488q8-11 20-15t24 1q12 5 19 16t5 24l-39 309h176q19 0 27 17t-4 32L388-66q-8 10-20.5 13T344-55q-11-5-17.5-16T322-95l38-265Z"/></svg></span>
            
          
            
          
            
          
            
          
            
          
        </span>
      </div>
    

    

    
  </div>



Docker Scout 的 GitHub 应用集成授权 Docker Scout 访问您在 GitHub 上的源代码仓库。这种对镜像构建过程的深入可见性意味着 Docker Scout 可以为您提供自动化且具有上下文的修复建议。

## 工作原理

当您启用 GitHub 集成时，Docker Scout 可以在镜像分析结果与源代码之间建立直接链接。

在分析您的镜像时，Docker Scout 会检查 [provenance attestations](/manuals/build/metadata/attestations/slsa-provenance.md) 以检测镜像的源代码仓库位置。如果找到源代码位置，并且您已启用 GitHub 应用，Docker Scout 将解析用于创建镜像的 Dockerfile。

解析 Dockerfile 可以揭示用于构建镜像的基础镜像标签。通过了解使用的基础镜像标签，Docker Scout 可以检测标签是否已过时，即标签已指向不同的镜像摘要。例如，假设您使用 `alpine:3.18` 作为基础镜像，在后续某个时间点，镜像维护者发布了版本 `3.18` 的补丁版本，其中包含安全修复。您一直在使用的 `alpine:3.18` 标签就变成了过时版本；您使用的 `alpine:3.18` 不再是最新版本。

当发生这种情况时，Docker Scout 会检测到差异并通过 [Up-to-Date Base Images policy](/manuals/scout/policy/_index.md#up-to-date-base-images-policy) 将其呈现出来。当启用 GitHub 集成时，您还会获得关于如何更新基础镜像的自动化建议。有关 Docker Scout 如何帮助您自动改进供应链行为和安全态势的更多信息，请参阅 [Remediation](../../policy/remediation.md)。

## 设置

要将 Docker Scout 与您的 GitHub 组织集成：

1. 访问 Docker Scout 仪表板上的 [GitHub integration](https://scout.docker.com/settings/integrations/github/) 页面。
2. 选择 **Integrate GitHub app** 按钮以打开 GitHub。
3. 选择您要集成的组织。
4. 选择是要集成 GitHub 组织中的所有仓库，还是手动选择仓库。
5. 选择 **Install & Authorize** 以将 Docker Scout 应用添加到该组织。

   此操作会将您重定向回 Docker Scout 仪表板，其中列出了您活动的 GitHub 集成。

GitHub 集成现已激活。
