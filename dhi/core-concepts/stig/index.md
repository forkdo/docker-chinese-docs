# STIG <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>





  
  
  
  


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



## 什么是 STIG？

[安全技术实施指南
(STIGs)](https://public.cyber.mil/stigs/) 是由美国国防信息系统局 (DISA) 发布的配置标准。它们定义了美国国防部 (DoD) 环境中使用的操作系统、应用程序、数据库和其他技术的安全要求。

STIG 有助于确保系统以安全且一致的方式进行配置，以减少漏洞。它们通常基于更广泛的要求，例如 DoD 的通用操作系统安全要求指南 (GPOS SRG)。

## 为什么 STIG 指南很重要

遵循 STIG 指南对于与美国政府系统合作或支持这些系统的组织至关重要。它表明与 DoD 安全标准的一致性，并有助于：

- 加速 DoD 系统的运营授权 (ATO) 流程
- 降低配置错误和可利用弱点的风险
- 通过标准化基线简化审计和报告

即使在联邦环境之外，注重安全的组织也将 STIG 用作强化系统配置的基准。

STIG 源自更广泛的 NIST 指南，特别是 [NIST 特别出版物 800-53](https://csrc.nist.gov/publications/sp800)，该出版物定义了联邦系统的安全和隐私控制目录。追求符合 800-53 或相关框架（如 FedRAMP）的组织可以使用 STIG 作为实施指南，以帮助满足适用的控制要求。

## Docker Hardened Images 如何帮助应用 STIG 指南

Docker Hardened Images (DHIs) 包含 STIG 变体，这些变体针对基于自定义 STIG 的配置文件进行扫描，并包含签名的 STIG 扫描证明。这些证明可以支持审计和合规报告。

虽然 Docker Hardened Images 对所有用户开放，但 STIG 变体需要 Docker 订阅。

Docker 基于 GPOS SRG 和 DoD 容器强化流程指南为镜像创建自定义的基于 STIG 的配置文件。由于 DISA 尚未发布专门针对容器的 STIG，因此这些配置文件有助于以一致、可审查的方式将类似 STIG 的指南应用于容器环境，并旨在减少容器镜像中常见的误报。

## 识别包含 STIG 扫描结果的镜像

包含 STIG 扫描结果的 Docker Hardened Images 在 Docker Hardened Images 目录中被标记为 **STIG**。

要查找具有 STIG 镜像变体的 DHI 仓库，请[探索镜像](../how-to/explore.md)并：

- 在目录页面上使用 **STIG** 筛选器
- 在单个镜像列表中查找 **STIG** 标签

要在仓库中找到 STIG 镜像变体，请转到仓库的 **Tags** 选项卡，并在 **Compliance** 列中查找标记为 **STIG** 的镜像。

## 使用 STIG 变体

要使用 STIG 变体，您必须[镜像](../how-to/mirror.md)该仓库，然后从您的镜像仓库中拉取 STIG 镜像。

## 查看和验证 STIG 扫描结果

Docker 为每个支持 STIG 的镜像提供签名的 [STIG 扫描证明](../core-concepts/attestations.md)。这些证明包括：

- 扫描结果摘要，包括通过、失败和不适用的检查数量
- 使用的 STIG 配置文件的名称和版本
- HTML 和 XCCDF (XML) 格式的完整输出

### 查看 STIG 扫描证明

您可以使用 Docker Scout CLI 检索和检查 STIG 扫描证明：

```console
$ docker scout attest get \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  dhi.io/<image>:<tag>
```

### 提取 HTML 报告

提取和查看人类可读的 HTML 报告：

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  | jq -r '.[0].output[] | select(.format == "html").content | @base64d' > stig_report.html
```

### 提取 XCCDF 报告

提取 XML (XCCDF) 报告以用于与其他工具集成：

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  | jq -r '.[0].output[] | select(.format == "xccdf").content | @base64d' > stig_report.xml
```

### 查看 STIG 扫描摘要

仅查看扫描摘要，不查看完整报告：

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  | jq -r '.[0] | del(.output)'
```
