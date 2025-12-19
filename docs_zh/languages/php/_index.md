---
title: PHP
params:
  icon: https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/php/php-original.svg
---
# PHP

## 什么是 PHP？

PHP 是一种广泛使用的开源脚本语言，特别适用于 Web 开发，并且可以嵌入到 HTML 中。

## 为什么使用 PHP？

- 学习简单，但功能强大
- 跨平台兼容
- 大量开源框架和库
- 与数据库良好集成
- 广泛的社区支持

## 基础语法

### Hello World

```php
<?php
echo "Hello, World!";
?>
```

### 变量

```php
<?php
$name = "John";
$age = 25;
$isStudent = true;
?>
```

### 函数

```php
<?php
function greet($name) {
    return "Hello, " . $name . "!";
}

echo greet("Alice");
?>
```

### 条件语句

```php
<?php
$score = 85;

if ($score >= 90) {
    echo "A";
} elseif ($score >= 80) {
    echo "B";
} else {
    echo "C";
}
?>
```

### 循环

```php
<?php
// For 循环
for ($i = 1; $i <= 5; $i++) {
    echo $i . " ";
}

// Foreach 循环
$colors = ["red", "green", "blue"];
foreach ($colors as $color) {
    echo $color . " ";
}
?>
```

### 数组

```php
<?php
// 索引数组
$fruits = ["apple", "banana", "orange"];

// 关联数组
$person = [
    "name" => "John",
    "age" => 30,
    "city" => "New York"
];

// 访问数组元素
echo $fruits[0]; // apple
echo $person["name"]; // John
?>
```

### 类和对象

```php
<?php
class Car {
    public $brand;
    public $color;
    
    public function __construct($brand, $color) {
        $this->brand = $brand;
        $this->color = $color;
    }
    
    public function start() {
        return "The " . $this->color . " " . $this->brand . " is starting.";
    }
}

$myCar = new Car("Toyota", "red");
echo $myCar->start();
?>
```

## 常用函数

### 字符串函数

```php
<?php
$text = "Hello World";

echo strlen($text);        // 11
echo strtoupper($text);   // HELLO WORLD
echo strtolower($text);   // hello world
echo substr($text, 0, 5); // Hello
?>
```

### 数组函数

```php
<?php
$numbers = [3, 1, 4, 1, 5];

echo count($numbers);           // 5
sort($numbers);                 // 排序
print_r($numbers);              // 显示数组
$unique = array_unique($numbers); // 去重
?>
```

### 日期函数

```php
<?php
echo date("Y-m-d");         // 2024-01-15
echo date("H:i:s");         // 14:30:25
echo time();                // Unix 时间戳
?>
```

## 表单处理

### HTML 表单

```html
<form method="post" action="process.php">
    <input type="text" name="username" placeholder="用户名">
    <input type="email" name="email" placeholder="邮箱">
    <input type="submit" value="提交">
</form>
```

### PHP 处理

```php
<?php
if ($_POST) {
    $username = $_POST['username'];
    $email = $_POST['email'];
    
    echo "用户名: " . $username;
    echo "邮箱: " . $email;
}
?>
```

## 数据库连接

### MySQLi 连接

```php
<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "myDB";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

echo "连接成功";
?>
```

### 执行查询

```php
<?php
$sql = "SELECT id, name, email FROM users";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        echo "ID: " . $row["id"]. " - 名称: " . $row["name"]. " - 邮箱: " . $row["email"]. "<br>";
    }
} else {
    echo "0 个结果";
}
?>
```

## 会话管理

```php
<?php
session_start();

// 设置会话变量
$_SESSION["username"] = "john_doe";
$_SESSION["login_time"] = time();

// 检查会话
if (isset($_SESSION["username"])) {
    echo "欢迎, " . $_SESSION["username"];
}

// 销毁会话
// session_destroy();
?>
```

## 文件操作

```php
<?php
// 写入文件
$content = "这是要写入的内容";
file_put_contents("test.txt", $content);

// 读取文件
$content = file_get_contents("test.txt");
echo $content;

// 检查文件是否存在
if (file_exists("test.txt")) {
    echo "文件存在";
}
?>
```

## 错误处理

```php
<?php
try {
    // 可能出错的代码
    if ($someCondition) {
        throw new Exception("发生错误");
    }
} catch (Exception $e) {
    echo "错误: " . $e->getMessage();
}
?>
```

## Composer 包管理

### composer.json

```json
{
    "name": "myproject/myapp",
    "require": {
        "monolog/monolog": "^2.0"
    },
    "autoload": {
        "psr-4": {
            "MyApp\\": "src/"
        }
    }
}
```

### 使用 Composer 包

```php
<?php
require_once 'vendor/autoload.php';

use Monolog\Logger;
use Monolog\Handler\StreamHandler;

// 创建日志器
$log = new Logger('name');
$log->pushHandler(new StreamHandler('logs/app.log', Logger::WARNING));

// 添加日志记录
$log->warning('这是一条警告信息');
?>
```

## 安全最佳实践

### 防止 SQL 注入

```php
<?php
$stmt = $conn->prepare("SELECT * FROM users WHERE id = ?");
$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();
?>
```

### 防止 XSS

```php
<?php
// 输出前转义
$user_input = htmlspecialchars($_POST['input'], ENT_QUOTES, 'UTF-8');
echo $user_input;
?>
```

### 密码哈希

```php
<?php
// 密码加密
$hashed_password = password_hash($password, PASSWORD_DEFAULT);

// 验证密码
if (password_verify($input_password, $hashed_password)) {
    echo "密码正确";
}
?>
```

## 常用框架

### Laravel

```php
<?php
// routes/web.php
Route::get('/', function () {
    return view('welcome');
});

Route::get('/users', [UserController::class, 'index']);
?>
```

### Symfony

```php
<?php
// Controller
class DefaultController extends AbstractController
{
    #[Route('/hello/{name}', name: 'hello')]
    public function hello(string $name): Response
    {
        return $this->render('hello.html.twig', [
            'name' => $name,
        ]);
    }
}
?>
```

## 性能优化

### 使用 OPcache

```php
// php.ini 配置
opcache.enable=1
opcache.memory_consumption=256
opcache.max_accelerated_files=20000
opcache.validate_timestamps=0
```

### 缓存查询结果

```php
<?php
// 使用 Memcached
$memcached = new Memcached();
$memcached->addServer('localhost', 11211);

$key = 'user_data_' . $user_id;
$data = $memcached->get($key);

if ($data === false) {
    $data = $db->query("SELECT * FROM users WHERE id = $user_id");
    $memcached->set($key, $data, 3600); // 缓存 1 小时
}
?>
```

## 调试技巧

### 使用 var_dump()

```php
<?php
$variable = ['name' => 'John', 'age' => 30];
var_dump($variable);
?>
```

### 使用 print_r()

```php
<?php
$variable = ['name' => 'John', 'age' => 30];
echo '<pre>';
print_r($variable);
echo '</pre>';
?>
```

### 错误报告

```php
<?php
// 开启错误报告
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
?>
```

## 常见问题

### 1. PHP 语法错误

- 检查括号是否匹配
- 确保分号结尾
- 验证引号配对

### 2. 数据库连接失败

- 检查主机名、用户名、密码
- 确认数据库服务运行
- 验证权限设置

### 3. 会话不工作

- 确保 session_start() 在任何输出之前调用
- 检查 php.ini 中的 session 配置
- 验证浏览器是否启用 cookies

## 学习资源

- [PHP 官方文档](https://www.php.net/manual/zh/)
- [Laravel 框架](https://laravel.com/docs)
- [Symfony 框架](https://symfony.com/doc)
- [Composer 文档](https://getcomposer.org/doc/)

## 总结

PHP 是一个功能强大且灵活的编程语言，特别适合 Web 开发。通过掌握基础语法、安全实践和性能优化技巧，你可以构建出高效、安全的 Web 应用。

开始你的 PHP 学习之旅，探索更多可能性！