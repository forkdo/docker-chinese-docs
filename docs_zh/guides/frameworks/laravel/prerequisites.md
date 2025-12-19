---
title: 使用 Docker Compose 搭建 Laravel 的先决条件
description: 在使用 Docker Compose 搭建 Laravel 之前，请确保您已具备所需的工具和知识。
weight: 10
---

在开始使用 Docker Compose 搭建 Laravel 之前，请确保您满足以下先决条件：

## Docker 和 Docker Compose

您需要在系统中安装 Docker 和 Docker Compose。Docker 允许您将应用程序容器化，而 Docker Compose 可帮助您管理多容器应用程序。

- Docker：请确保您的机器上已安装并正在运行 Docker。请参考 [Docker 安装指南](/get-docker/) 安装 Docker。
- Docker Compose：Docker Compose 已包含在 Docker Desktop 中，但您也可以根据需要参考 [Docker Compose 安装指南](/compose/install/)。

## 对 Docker 和容器的基本了解

对 Docker 以及容器工作原理的基本了解将有所帮助。如果您是 Docker 新手，请考虑查看 [Docker 概述](/get-started/overview/) 以熟悉容器化概念。

## 对 Laravel 的基本知识

本指南假定您对 Laravel 和 PHP 有基本的了解。熟悉 Laravel 的命令行工具（如 [Artisan](https://laravel.com/docs/12.x/artisan)）及其项目结构对于遵循本指南的说明非常重要。

- Laravel CLI：您应该能够熟练使用 Laravel 的命令行工具 (`artisan`)。
- Laravel 项目结构：请熟悉 Laravel 的文件夹结构（`app`、`config`、`routes`、`tests` 等）。