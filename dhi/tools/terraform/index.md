# Use the DHI Terraform provider


[DHI Terraform 提供商](https://registry.terraform.io/providers/docker-hardened-images/dhi/latest/docs)
让您能够以基础设施即代码的方式管理 Docker Hardened Image 镜像和自定义配置。

## 安装并配置提供商

将提供商添加到您的 Terraform 配置中：

```hcl
terraform {
  required_providers {
    dhi = {
      source = "docker-hardened-images/dhi"
    }
  }
}

provider "dhi" {
  docker_hub_username = var.docker_username
  docker_hub_password = var.docker_password
  organization        = var.org_name
}
```

除了在 provider 块中指定凭据外，您也可以设置环境变量：

| 变量 | 描述 |
|----------|-------------|
| `DOCKER_USERNAME` | Docker Hub 用户名或组织命名空间 |
| `DOCKER_PASSWORD` | Docker Hub 密码或个人/组织访问令牌 |
| `DHI_ORG` | 目标组织命名空间 |

您可以使用个人访问令牌 (PAT) 或组织访问令牌 (OAT) 代替密码进行身份验证。使用 OAT 时，权限范围适用：

- 列出镜像需要读取（拉取）访问权限。
- 创建或删除镜像需要推送访问权限。

## 资源

### `dhi_mirror`

管理您组织中的已镜像 DHI 仓库。有关基于任务的示例，请参阅[镜像 Docker Hardened Image 仓库](/dhi/how-to/mirror/)。

有关资源属性的完整列表，请参阅 [Terraform Registry 文档](https://registry.terraform.io/providers/docker-hardened-images/dhi/latest/docs/resources/mirror)。

### `dhi_customization`

管理应用于已镜像仓库的镜像自定义配置。有关基于任务的示例，请参阅[自定义 Docker Hardened Image](/dhi/how-to/customize/)。

有关资源属性的完整列表，请参阅 [Terraform Registry 文档](https://registry.terraform.io/providers/docker-hardened-images/dhi/latest/docs/resources/customization)。

