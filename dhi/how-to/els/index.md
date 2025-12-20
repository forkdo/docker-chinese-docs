# 使用 Docker Hardened Images 的扩展生命周期支持 <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Subscription:</span>
        
          <span>Docker Hardened Images Enterprise</span>
          <span class="icon-svg">
            
            
              <svg 
  class="w-5 h-5 text-gray-800 dark:text-white"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
  xmlns="http://www.w3.org/2000/svg"
  focusable="false"
  aria-hidden="true"
>
<path d="M18.1639 21.6147V18.6147M18.1639 18.6147V15.6147M18.1639 18.6147H15.1639M18.1639 18.6147H21.1639M19.8692 13.3281C19.9541 12.8974 20 12.4544 20 11.9999V7.21747C20 6.41796 20 6.0182 19.8692 5.67457C19.7537 5.37101 19.566 5.10015 19.3223 4.8854C19.0465 4.64231 18.6722 4.50195 17.9236 4.22122L12.5618 2.21054C12.3539 2.13258 12.25 2.0936 12.143 2.07815C12.0482 2.06444 11.9518 2.06444 11.857 2.07815C11.75 2.0936 11.6461 2.13258 11.4382 2.21054L6.0764 4.22122C5.3278 4.50195 4.9535 4.64231 4.67766 4.8854C4.43398 5.10015 4.24627 5.37101 4.13076 5.67457C4 6.0182 4 6.41796 4 7.21747V11.9999C4 16.9083 9.35396 20.4783 11.302 21.6147C11.5234 21.7439 11.6341 21.8085 11.7903 21.842C11.9116 21.868 12.0884 21.868 12.2097 21.842C12.3659 21.8085 12.4766 21.7439 12.698 21.6147C12.986 21.4467 13.3484 21.2255 13.757 20.9547M14.517 9.70865C14.517 10.4365 14.2081 11.0922 13.7143 11.5517C13.5354 11.7181 13.446 11.8013 13.4126 11.8658C13.3774 11.9337 13.3672 11.9737 13.3656 12.0501C13.364 12.1227 13.3936 12.2115 13.4528 12.3891L14.2225 14.6983C14.322 14.9966 14.3717 15.1458 14.3419 15.2645C14.3158 15.3684 14.2509 15.4584 14.1606 15.516C14.0574 15.5818 13.9002 15.5818 13.5858 15.5818H10.4142C10.0998 15.5818 9.94255 15.5818 9.83936 15.516C9.74903 15.4584 9.68416 15.3684 9.65807 15.2645C9.62826 15.1458 9.67797 14.9966 9.7774 14.6983L10.5472 12.3891C10.6063 12.2115 10.6359 12.1227 10.6344 12.0501C10.6328 11.9737 10.6226 11.9337 10.5874 11.8658C10.5539 11.8013 10.4645 11.7181 10.2857 11.5517C9.79182 11.0922 9.48291 10.4365 9.48291 9.70865C9.48291 8.31852 10.6098 7.19159 12 7.19159C13.3901 7.19159 14.517 8.31852 14.517 9.70865Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
            
          </span>
        
      </div>
    

    

    

    
  </div>



通过 Docker Hardened Images 订阅附加组件，您可以将扩展生命周期支持 (ELS) 用于 Docker Hardened Images。ELS 为生命周期结束 (EOL) 的镜像版本提供安全补丁，让您在按照自己的时间表规划升级的同时，保持安全、合规的运营。您可以像使用任何其他 Docker Hardened Image 一样使用 ELS 镜像，但您必须为要使用 ELS 的每个仓库启用 ELS。

## 发现支持 ELS 的仓库

要查找支持 ELS 的镜像：

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Hardened Images** > **Catalog**。
5. 在 **Filter by** 中，选择 **Extended Lifecycle Support**。

## 为仓库启用 ELS

要为仓库启用 ELS，组织所有者必须将仓库[镜像](./mirror.md)到您的组织。

要在镜像时启用 ELS：

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Hardened Images** > **Catalog**。
5. 选择一个 DHI 仓库以查看其详细信息。
6. 选择 **Use this image** > **Mirror repository**。
7. 选择 **Enable support for end-of-life versions**，然后按照屏幕上的说明操作。

## 为仓库禁用 ELS

要为仓库禁用 ELS，您必须在镜像仓库的 **Settings** 选项卡中取消选中 ELS 选项，或者停止镜像该仓库。要停止镜像，请参阅[停止镜像仓库](./mirror.md#stop-mirroring-a-repository)。

要更新设置：

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Repositories**，然后选择镜像的仓库。
5. 选择 **Settings** 选项卡。
6. 取消选中 **Mirror end-of-life images** 选项。

## 管理 ELS 仓库

您可以像管理任何其他镜像的 DHI 仓库一样，查看和管理带有 ELS 的镜像仓库。更多详情，请参阅[管理镜像](./manage.md)。
