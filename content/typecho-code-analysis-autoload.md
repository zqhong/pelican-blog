Title: typecho 源码分析：1、Autoload
Date: 2016-02-26 14:50
Category: PHP
Tags: typecho, php, autoload
Slug: typecho-code-analysis-autoload
Author: zqhong

### 前言
这里有几点需要注意的：
1. 分析的 [Typecho](https://github.com/typecho/typecho/releases/tag/v1.0-14.10.10-release) 版本为 **1.0 (14.10.10)**。
2. 之前没接触过自动加载类的，请参考 PHP 官方手册的这篇文章：[PHP：自动加载类](http://php.net/manual/zh/language.oop5.autoload.php)。如果想深入理解这个呢，请看这个：[细说“PHP类库自动加载”](https://github.com/qinjx/adv_php_book/blob/master/class_autoload.md)。
3. 为了减少篇幅和便于理解，列出的代码仅是源码的部分。
4. 文件路径中，**typecho/** 表示 typecho 的根目录。

---

### typecho 自动加载机制
#### 一、入口文件
目前许多 web 程序都使用单入口模式。即使用 *index.php* 作为入口文件，加载配置文件进行初始化，利用路由分析URI，调用合适的类方法解决问题并输出结果。typecho 也是使用单入口模式。因此，我们照例看 *index.php* 这个文件。

*typecho/index.php*
```php
if (!defined('__TYPECHO_ROOT_DIR__') && !@include_once 'config.inc.php') {
    file_exists('./install.php') ? header('Location: install.php') : print('Missing Config File');
    exit;
}
```

代码分析：
1. 如果还没完成安装（不存在文件 *config.inc.php* ），这个时候会将浏览器重定向到 *install.php*，完成初始化安装。
2. 加载配置文件 *config.inc.php*（如果已经完成初始化）

<!--more-->

#### 二、初始化配置文件

*config.inc.php*
```php
define('__TYPECHO_ROOT_DIR__', dirname(__FILE__));

define('__TYPECHO_PLUGIN_DIR__', '/usr/plugins');

define('__TYPECHO_THEME_DIR__', '/usr/themes');

define('__TYPECHO_ADMIN_DIR__', '/admin/');

@set_include_path(get_include_path() . PATH_SEPARATOR .
__TYPECHO_ROOT_DIR__ . '/var' . PATH_SEPARATOR .
__TYPECHO_ROOT_DIR__ . __TYPECHO_PLUGIN_DIR__);

require_once 'Typecho/Common.php';

Typecho_Common::init();
```

代码分析：
1. 定义目录常量，比如：\_\_TYPECHO_ROOT_DIR\_\_、\_\_TYPECHO_PLUGIN_DIR\_\_、\_\_TYPECHO_THEME_DIR\_\_等，便于以后使用。
2. 设置包含路径。这个东西类似于 Windows 的环境变量。假设你在 Windows 的命令提示符下输入命令 `php`，首先，系统会在当前路径下着有没有名字叫 *php* 的执行文件。如果没有，系统会再去环境变量 *PATH* 中设置的路径中再查找有没有叫 *php* 的可执行文件。这里的作用是一样的，让系统在原先的*include_path* 和用户自己设置的 *include_path* 中寻找用户需要的 php 文件。
3. 初始化程序（`Typecho_Common::init()`）

> 备注：如果需要看系统默认设置了哪些 *include_path*，请看 *php.ini* 这个文件，里面搜索 *include_path* 即可。

#### 三、初始化程序
这里是实现自动加载类的重点，而且也就几行代码。请认真看看

> 备注：当然，现在一般都使用 Composer，自动加载类不需要自己实现。

*typecho/var/Typecho/Common.php*
```php
class Typecho_Common
{
    public static function __autoLoad($className)
    {
        @include_once str_replace(array('\\', '_'), '/', $className) . '.php';
    }

    public static function init()
    {
        if (function_exists('spl_autoload_register')) {
            spl_autoload_register(array('Typecho_Common', '__autoLoad'));
        } else {
            function __autoLoad($className) {
                Typecho_Common::__autoLoad($className);
            }
        }
    }
}

```

代码分析：
1. 注册 *Typecho_Common::\_\_autoLoad* 方法，当程序尝试加载未定义的类时，会启动该方法。
2. 再看看 *Typecho_Common::\_\_autoLoad* 这个方法，该方法将类名中的"\"和"_"替换为"/"，接着调用 require_once 包含这个类。比如，"Typecho_Db"，最终会被替换为："Typecho/Db.php"。接着调用 require_once "Typecho/Db.php"。最后在 include_path 中的 *typecho/var/Typecho/Db.php* 中找到我们所需要的类文件。

---

### 相关资料
[PHP：自动加载类](http://php.net/manual/zh/language.oop5.autoload.php)
[细说“PHP类库自动加载”](https://github.com/qinjx/adv_php_book/blob/master/class_autoload.md)
[Composer](https://getcomposer.org/)
