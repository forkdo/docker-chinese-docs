---
title: 在容器中运行 PHP 测试
linkTitle: 运行测试
weight: 30
keywords: php, test
description: 了解如何在容器中运行 PHP 测试。
aliases:
- /language/php/run-tests/
- /guides/language/php/run-tests/
---

## 前提条件

完成本指南的所有先前部分，从 [容器化 PHP 应用程序](containerize.md) 开始。

## 概述

测试是现代软件开发中不可或缺的一部分。对于不同的开发团队来说，测试可能意味着很多事情。有单元测试、集成测试和端到端测试。在本指南中，您将了解在开发和构建时如何在 Docker 中运行单元测试。

## 在本地开发时运行测试

示例应用程序在 `tests` 目录中已经有一个 PHPUnit 测试。在本地开发时，您可以使用 Compose 来运行测试。

在 `docker-php-sample` 目录中运行以下命令，以在容器内运行测试。

```console
$ docker compose run --build --rm server ./vendor/bin/phpunit tests/HelloWorldTest.php
```

您应该会看到包含以下内容的输出。

```console
Hello, Docker!PHPUnit 9.6.13 by Sebastian Bergmann and contributors.

.                                                                   1 / 1 (100%)

Time: 00:00.003, Memory: 4.00 MB

OK (1 test, 1 assertion)
```

要了解有关该命令的更多信息，请参阅 [docker compose run](/reference/cli/docker/compose/run/)。

## 在构建时运行测试

要在构建时运行测试，您需要更新您的 Dockerfile。创建一个新的测试阶段来运行测试。

以下是更新后的 Dockerfile。

```dockerfile {hl_lines="26-28"}
# syntax=docker/dockerfile:1

FROM composer:lts as prod-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM composer:lts as dev-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-interaction

FROM php:8.2-apache as base
RUN docker-php-ext-install pdo pdo_mysql
COPY ./src /var/www/html

FROM base as development
COPY ./tests /var/www/html/tests
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"
COPY --from=dev-deps app/vendor/ /var/www/html/vendor

FROM development as test
WORKDIR /var/www/html
RUN ./vendor/bin/phpunit tests/HelloWorldTest.php

FROM base as final
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=prod-deps app/vendor/ /var/www/html/vendor
USER www-data
```

运行以下命令，使用测试阶段作为目标来构建镜像，并查看测试结果。包含 `--progress plain` 以查看构建输出，`--no-cache` 以确保始终运行测试，以及 `--target test` 以定位测试阶段。

```console
$ docker build -t php-docker-image-test --progress plain --no-cache --target test .
```

您应该会看到包含以下内容的输出。

```console
#18 [test 2/2] RUN ./vendor/bin/phpunit tests/HelloWorldTest.php
#18 0.385 Hello, Docker!PHPUnit 9.6.13 by Sebastian Bergmann and contributors.
#18 0.392
#18 0.394 .                                                                   1 / 1 (100%)
#18 0.395
#18 0.395 Time: 00:00.003, Memory: 4.00 MB
#18 0.395
#18 0.395 OK (1 test, 1 assertion)
```

## 总结

在本节中，您学习了如何在本地开发时使用 Compose 运行测试，以及如何在构建镜像时运行测试。

相关信息：

- [docker compose run](/reference/cli/docker/compose/run/)

## 下一步

接下来，您将学习如何使用 GitHub Actions 设置 CI/CD 流水线。