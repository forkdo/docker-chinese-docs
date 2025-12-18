> [!NOTE]
>
> Buildx v0.10 启用了对最小化 [SLSA Provenance](https://slsa.dev/provenance/) 证明的支持，
> 该功能需要支持 [OCI 合规](https://github.com/opencontainers/image-spec) 的多平台镜像。
> 这可能会导致注册中心和运行时支持出现问题
> （例如 [Google Cloud Run 和 AWS Lambda](https://github.com/docker/buildx/issues/1533)）。
> 您可以使用 `--provenance=false` 选择性地禁用默认的证明功能。