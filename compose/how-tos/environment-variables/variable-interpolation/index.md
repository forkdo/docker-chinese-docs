# 在 Compose 文件中使用插值设置、使用和管理变量

Compose 文件可以使用变量来提供更大的灵活性。如果你想在镜像标签之间快速切换以测试多个版本，或者想将卷源调整到你的本地环境，你不需要每次都编辑 Compose 文件，只需设置变量即可在运行时将值插入到你的 Compose 文件中。

插值也可以用来在运行时将值插入到你的 Compose 文件中，然后用于将变量传递到容器的环境中。

下面是一个简单的例子：

```console
$ cat .env
TAG=v1.5
$ cat compose.yaml
services:
  web:
    image: "webapp:${TAG}"
```

当你运行 `docker compose up` 时，Compose 文件中定义的 `web` 服务会将镜像[插值](variable-interpolation.md)为在 `.env` 文件中设置的 `webapp:v1.5`。你可以使用 [config 命令](/reference/cli/docker/compose/config.md) 来验证这一点，该命令会将你解析后的应用配置打印到终端：

```console
$ docker compose config
services:
  web:
    image: 'webapp:v1.5'
```

## 插值语法

插值应用于未引用和双引号引用的值。
支持带花括号 (`${VAR}`) 和不带花括号 (`$VAR`) 的表达式。

对于带花括号的表达式，支持以下格式：
- 直接替换
  - `${VAR}` -> `VAR` 的值
- 默认值
  - `${VAR:-default}` -> 如果 `VAR` 已设置且非空，则为 `VAR` 的值，否则为 `default`
  - `${VAR-default}` -> 如果 `VAR` 已设置，则为 `VAR` 的值，否则为 `default`
- 必需值
  - `${VAR:?error}` -> 如果 `VAR` 已设置且非空，则为 `VAR` 的值，否则以错误退出
  - `${VAR?error}` -> 如果 `VAR` 已设置，则为 `VAR` 的值，否则以错误退出
- 替代值
  - `${VAR:+replacement}` -> 如果 `VAR` 已设置且非空，则为 `replacement`，否则为空
  - `${VAR+replacement}` -> 如果 `VAR` 已设置，则为 `replacement`，否则为空

更多信息，请参阅 Compose 规范中的 [插值](/reference/compose-file/interpolation.md)。

## 使用插值设置变量的方法

Docker Compose 可以从多个来源将变量插值到你的 Compose 文件中。

请注意，当同一个变量被多个来源声明时，适用优先级规则：

1. 来自 Shell 环境的变量
2. 如果未设置 `--env-file`，则由本地工作目录 (`PWD`) 中的 `.env` 文件设置的变量
3. 由 `--env-file` 设置的文件或项目目录中的 `.env` 文件中的变量

你可以通过运行 `docker compose config --environment` 来检查 Compose 用于插值 Compose 模型的变量和值。

### `.env` 文件

Docker Compose 中的 `.env` 文件是一个文本文件，用于定义在运行 `docker compose up` 时应可用于插值的变量。此文件通常包含变量的键值对，它让你可以集中管理和配置。如果你有多个需要存储的变量，`.env` 文件非常有用。

`.env` 文件是设置变量的默认方法。`.env` 文件应放置在项目目录的根目录下，与你的 `compose.yaml` 文件相邻。有关环境文件格式的更多信息，请参阅 [环境文件语法](#env-file-syntax)。

基本示例：

```console
$ cat .env
## define COMPOSE_DEBUG based on DEV_MODE, defaults to false
COMPOSE_DEBUG=${DEV_MODE:-false}

$ cat compose.yaml 
  services:
    webapp:
      image: my-webapp-image
      environment:
        - DEBUG=${COMPOSE_DEBUG}

$ DEV_MODE=true docker compose config
services:
  webapp:
    environment:
      DEBUG: "true"
```

#### 其他信息

- 如果你在 `.env` 文件中定义了一个变量，你可以在 `compose.yaml` 中直接使用 [`environment` 属性](/reference/compose-file/services.md#environment) 引用它。例如，如果你的 `.env` 文件包含环境变量 `DEBUG=1`，并且你的 `compose.yaml` 文件如下所示：
   ```yaml
    services:
      webapp:
        image: my-webapp-image
        environment:
          - DEBUG=${DEBUG}
   ```
   Docker Compose 会用 `.env` 文件中的值替换 `${DEBUG}`。

   > [!IMPORTANT]
   >
   > 在容器环境中将 `.env` 文件中的变量用作环境变量时，请注意[环境变量优先级](envvars-precedence.md)。

- 你可以将 `.env` 文件放在项目目录根目录以外的位置，然后使用 CLI 中的 [`--env-file` 选项](#substitute-with
---env-file)，以便 Compose 可以导航到它。

- 如果使用 [`--env-file`](#substitute-with
---env-file) 进行替换，你的 `.env` 文件可能会被另一个 `.env` 文件覆盖。

> [!IMPORTANT]
>
> 从 `.env` 文件进行替换是 Docker Compose CLI 的一项功能。
>
> 在运行 `docker stack deploy` 时，Swarm 不支持此功能。

#### `.env` 文件语法

以下语法规则适用于环境文件：

- 以 `#` 开头的行被视为注释并被忽略。
- 空行被忽略。
- 未引用和双引号 (`"`) 引用的值会应用插值。
- 每行代表一个键值对。值可以选择性地加引号。
- 分隔键和值的分隔符可以是 `=` 或 `:`。
- 值前后的空格会被忽略。
  - `VAR=VAL` -> `VAL`
  - `VAR="VAL"` -> `VAL`
  - `VAR='VAL'` -> `VAL`
  - `VAR: VAL` -> `VAL`
  - `VAR = VAL  ` -> `VAL` <!-- markdownlint-disable-line no-space-in-code -->
- 未引用值的行内注释前面必须有空格。
  - `VAR=VAL # comment` -> `VAL`
  - `VAR=VAL# not a comment` -> `VAL# not a comment`
- 引用值的行内注释必须跟在闭合引号后面。
  - `VAR="VAL # not a comment"` -> `VAL # not a comment`
  - `VAR="VAL" # comment` -> `VAL`
- 单引号 (`'`) 引用的值按字面意思使用。
  - `VAR='$OTHER'` -> `$OTHER`
  - `VAR='${OTHER}'` -> `${OTHER}`
- 引号可以用 `\` 转义。
  - `VAR='Let\'s go!'` -> `Let's go!`
  - `VAR="{\"hello\": \"json\"}"` -> `{"hello": "json"}`
- 双引号引用的值中支持常见的 Shell 转义序列，包括 `\n`, `\r`, `\t` 和 `\\`。
  - `VAR="some\tvalue"` -> `some  value`
  - `VAR='some\tvalue'` -> `some\tvalue`
  - `VAR=some\tvalue` -> `some\tvalue`
- 单引号引用的值可以跨越多行。例如：

   ```yaml
   KEY='SOME
   VALUE'
   ```

   如果你然后运行 `docker compose config`，你会看到：

   ```yaml
   environment:
     KEY: |-
       SOME
       VALUE
   ```

### 使用 `--env-file` 替换

你可以在 `.env` 文件中为多个环境变量设置默认值，然后在 CLI 中将该文件作为参数传递。

这种方法的优点是，你可以将文件存储在任何地方并适当地命名，例如，该文件路径相对于执行 Docker Compose 命令的当前工作目录。使用 `--env-file` 选项传递文件路径：

```console
$ docker compose --env-file ./config/.env.dev up
```

#### 其他信息

- 如果你想临时覆盖已在 `compose.yaml` 文件中引用的 `.env` 文件，此方法非常有用。例如，你可能有用于生产 (`.env.prod`) 和测试 (`.env.test`) 的不同 `.env` 文件。
  在以下示例中，有两个环境文件 `.env` 和 `.env.dev`。两者都为 `TAG` 设置了不同的值。
  ```console
  $ cat .env
  TAG=v1.5
  $ cat ./config/.env.dev
  TAG=v1.6
  $ cat compose.yaml
  services:
    web:
      image: "webapp:${TAG}"
  ```
  如果命令行中未使用 `--env-file`，则默认加载 `.env` 文件：
  ```console
  $ docker compose config
  services:
    web:
      image: 'webapp:v1.5'
  ```
  传递 `--env-file` 参数会覆盖默认文件路径：
  ```console
  $ docker compose --env-file ./config/.env.dev config
  services:
    web:
      image: 'webapp:v1.6'
  ```
  当传递的 `--env-file` 参数文件路径无效时，Compose 会返回错误：
  ```console
  $ docker compose --env-file ./doesnotexist/.env.dev  config
  ERROR: Couldn't find env file: /home/user/./doesnotexist/.env.dev
  ```
- 你可以使用多个 `--env-file` 选项来指定多个环境文件，Docker Compose 会按顺序读取它们。后面的文件可以覆盖前面文件中的变量。
  ```console
  $ docker compose --env-file .env --env-file .env.override up
  ```
- 启动容器时，你可以从命令行覆盖特定的环境变量。
  ```console
  $ docker compose --env-file .env.dev up -e DATABASE_URL=mysql://new_user:new_password@new_db:3306/new_database
  ```

### 本地 `.env` 文件与 <项目目录> `.env` 文件

`.env` 文件也可用于声明用于控制 Compose 行为和要加载的文件的[预定义环境变量](envvars.md)。

当在没有显式 `--env-file` 标志的情况下执行时，Compose 会在你的工作目录 ([PWD](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html#index-PWD)) 中搜索 `.env` 文件，并加载值用于自身配置和插值。如果此文件中的值定义了 `COMPOSE_FILE` 预定义变量，这会导致项目目录被设置为另一个文件夹，Compose 将加载第二个 `.env` 文件（如果存在）。这第二个 `.env` 文件具有较低的优先级。

这种机制使得可以使用一组自定义变量作为覆盖来调用现有的 Compose 项目，而无需通过命令行传递环境变量。

```console
$ cat .env
COMPOSE_FILE=../compose.yaml
POSTGRES_VERSION=9.3

$ cat ../compose.yaml 
services:
  db:
    image: "postgres:${POSTGRES_VERSION}"
$ cat ../.env
POSTGRES_VERSION=9.2

$ docker compose config
services:
  db:
    image: "postgres:9.3"
```

### 从 Shell 替换

你可以使用主机机器上或执行 `docker compose` 命令的 Shell 环境中的现有环境变量。这允许你在运行时将值动态注入到 Docker Compose 配置中。
例如，假设 Shell 包含 `POSTGRES_VERSION=9.3`，并且你提供以下配置：

```yaml
db:
  image: "postgres:${POSTGRES_VERSION}"
```

当你使用此配置运行 `docker compose up` 时，Compose 会在 Shell 中查找 `POSTGRES_VERSION` 环境变量并替换其值。在此示例中，Compose 在运行配置之前将镜像解析为 `postgres:9.3`。

如果环境变量未设置，Compose 会用空字符串替换。在前面的示例中，如果 `POSTGRES_VERSION` 未设置，镜像选项的值为 `postgres:`。

> [!NOTE]
>
> `postgres:` 不是有效的镜像引用。Docker 期望一个不带标签的引用，如 `postgres`（默认为最新镜像），或者带标签的引用，如 `postgres:15`。
