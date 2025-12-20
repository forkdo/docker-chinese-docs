# FIPS <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>





  
  
  
  


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



## 什么是 FIPS 140？

[FIPS 140](https://csrc.nist.gov/publications/detail/fips/140/3/final) 是一项美国政府标准，用于定义保护敏感信息的加密模块的安全要求。它广泛应用于政府、医疗保健和金融服务等受监管的环境。

FIPS 认证由 [NIST 加密模块验证计划 (CMVP)](https://csrc.nist.gov/projects/cryptographic-module-validation-program) 管理，该计划确保加密模块符合严格的安全标准。

## 为什么 FIPS 合规性很重要

在许多受监管的环境中，例如政府、医疗保健、金融和国防领域，FIPS 140 合规性是必需或强烈推荐的，这些环境中的敏感数据必须得到保护。这些标准确保加密操作使用经过审查、可信赖的算法，并在安全的模块中实现。

使用依赖经验证的加密模块的软件组件可以帮助组织：

- 满足联邦和行业法规要求，例如 FedRAMP，它要求或强烈推荐使用 FIPS 140 验证的加密技术。
- 通过可验证的、基于标准的安全加密实践证据，证明已做好审计准备。
- 通过阻止未经批准或不安全的算法（例如 MD5）并确保跨环境行为的一致性，来降低安全风险。

## Docker Hardened Images 如何支持 FIPS 合规性

虽然 Docker Hardened Images 对所有用户开放，但 FIPS 变体需要 Docker Hardened Images Enterprise 订阅。

Docker Hardened Images (DHI) 包含使用经 FIPS 140 验证的加密模块的变体。这些镜像旨在通过整合符合该标准的组件，帮助组织满足合规要求。

- FIPS 镜像变体使用已通过 FIPS 140 验证的加密模块。
- 这些变体由 Docker 构建和维护，以支持具有监管或合规需求的环境。
- Docker 提供签名的测试证明，记录了经验证的加密模块的使用情况。这些证明可以支持内部审计和合规报告。

> [!NOTE]
>
> 使用 FIPS 镜像变体有助于满足合规要求，但并不能使应用程序或系统完全合规。合规性取决于镜像在更广泛的系统中如何被集成和使用。

## 识别支持 FIPS 的镜像

支持 FIPS 的 Docker Hardened Images 在 Docker Hardened Images 目录中被标记为 **FIPS** 合规。

要查找具有 FIPS 镜像变体的 DHI 仓库，请[探索镜像](../how-to/explore.md)并：

- 在目录页面上使用 **FIPS** 筛选器
- 在单个镜像列表中查找 **FIPS** 合规标识

这些指示器可帮助您快速定位支持基于 FIPS 合规需求的仓库。包含 FIPS 支持的镜像变体将有一个以 `-fips` 结尾的标签，例如 `3.13-fips`。

## 使用 FIPS 变体

要使用 FIPS 变体，您必须[镜像](../how-to/mirror.md)该仓库，然后从您的镜像仓库中拉取 FIPS 镜像。

## 查看 FIPS 证明

Docker Hardened Images 的 FIPS 变体包含一个 FIPS 证明，其中列出了镜像中包含的实际加密模块。

您可以使用 Docker Scout CLI 检索和检查 FIPS 证明：

```console
$ docker scout attest get \
  --predicate-type https://docker.com/dhi/fips/v0.1 \
  --predicate \
  dhi.io/<image>:<tag>
```

例如：

```console
$ docker scout attest get \
  --predicate-type https://docker.com/dhi/fips/v0.1 \
  --predicate \
  dhi.io/python:3.13-fips
```

证明输出是一个 JSON 数组，描述了镜像中包含的加密模块及其合规状态。例如：

```json
[
  {
    "certification": "CMVP #4985",
    "certificationUrl": "https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4985",
    "name": "OpenSSL FIPS Provider",
    "package": "pkg:dhi/openssl-provider-fips@3.1.2",
    "standard": "FIPS 140-3",
    "status": "active",
    "sunsetDate": "2030-03-10",
    "version": "3.1.2"
  }
]
```
