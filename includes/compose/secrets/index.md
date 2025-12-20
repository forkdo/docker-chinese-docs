# 
Docker Compose 提供了一种使用 secrets 的方式，无需通过环境变量来存储信息。如果将密码和 API 密钥作为环境变量注入，可能会导致信息意外泄露。服务只有在 `services` 顶层元素中通过 `secrets` 属性明确授权后，才能访问 secrets。
