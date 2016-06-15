Title: PHP 中依赖注入的实现
Date: 2016-05-08 11:04
Category: PHP
Tags: PHP, 依赖注入
Slug: how-dependency-injection-work-in-php
Author: zqhong

### 依赖注入的例子
#### 没依赖注入的情况下
```php
<?php
class Foo
{
    public function foo($a)
    {
        echo $a;
    }
}

class Bar
{
    public function test($a)
    {
        // 这里我们需要手动实例化对象
        $foo = new Foo();
        $foo->foo($a);
    }
}
```

#### 有依赖注入的情况下
```php
<?php
class Foo
{
    public function foo($a)
    {
        echo $a;
    }
}

class Bar
    {
    public function test(Foo $foo, $a)
    {
        // 依赖注入自动帮我们实例化 Foo 对象，然后作为参数传入
        $foo->foo($a);
    }
}
```

<!--more-->

---

### 依赖注入的实现
使用 `ReflectionMethod` 反射类方法，获取里面的参数。遍历获取到的参数集合，如果该参数类型为 class 时，实例化该对象，并替代原来的参数列表。

---

### 依赖注入示例代码
```php
<?php

class Database
{
    public function test(MysqlAdapter $adapter, $a, $b)
    {
        echo $a + $b;
        $adapter->test();
    }
}

class MysqlAdapter
{
    public function test()
    {
        echo "I am MysqlAdapter test";
    }
}

class app
{
    public static function run($instance, $method, $parameters = null)
    {
        if (!method_exists($instance, $method)) {
            return null;
        }

        if (empty($parameters)) {
            $parameters = [];
        }

        $reflector = new ReflectionMethod($instance, $method);
        foreach ($reflector->getParameters() as $key => $parameter) {
            $class = $parameter->getClass();

            if ($class) {
                array_splice($parameters, $key, 0, [
                    new $class->name()
                ]);
            }
        }

        call_user_func_array([
            $instance,
            $method
        ], $parameters);
    }
}

app::run(new Database(), 'test', [1,2]);
```

---

### 参考资料
[Laravel 依赖注入原理](https://phphub.org/topics/843)
[依赖注入 - Java 实现](https://github.com/android-cn/blog/tree/master/java/dependency-injection)
