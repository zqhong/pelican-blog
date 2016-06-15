Title: typecho 源码分析：3、Router
Date: 2016-03-04 09:50
Category: PHP
Tags: typecho, php, router
Slug: typecho-code-analysis-router
Author: zqhong

### Router
在 web 程序中，Router 负责解析用户的 uri，匹配路由表。再根据路由表信息，选择相对应的函数（function）或方法（method）。

#### 一、入口函数
*index.php*
```php
Typecho_Widget::widget('Widget_Init');
Typecho_Router::dispatch();
```
代码分析：
1. 初始化路由器
2. 开始路由分发

---

#### 二、初始化路由表
*typecho/var/Widget/Init.php*
```php
class Widget_Init extends Typecho_Widget
{
    public function execute()
    {
        /** 对变量赋值 */
        $options = $this->widget('Widget_Options');

        if (defined('__TYPECHO_PATHINFO_ENCODING__')) {
            $pathInfo = $this->request->getPathInfo(__TYPECHO_PATHINFO_ENCODING__, $options->charset);
        } else {
            $pathInfo = $this->request->getPathInfo();
        }

        Typecho_Router::setPathInfo($pathInfo);

        /** 初始化路由器 */
        Typecho_Router::setRoutes($options->routingTable);
    }
}

class Widget_Options extends Typecho_Widget
{
    public function execute()
    {
        $this->db->fetchAll($this->db->select()->from('table.options')
        ->where('user = 0'), array($this, 'push'));

        /** 自动初始化路由表 */
        $this->routingTable = unserialize($this->routingTable);
        if (!isset($this->routingTable[0])) {
            /** 解析路由并缓存 */
            $parser = new Typecho_Router_Parser($this->routingTable);
            $parsedRoutingTable = $parser->parse();
            $this->routingTable = array_merge(array($parsedRoutingTable), $this->routingTable);
            $this->db->query($this->db->update('table.options')->rows(array('value' => serialize($this->routingTable)))
            ->where('name = ?', 'routingTable'));
        }
    }
}

class Typecho_Router
{
    public static $_routingTable = array();

    public static function setRoutes($routes)
    {
        if (isset($routes[0])) {
            self::$_routingTable = $routes[0];
        } else {
            /** 解析路由配置 */
            $parser = new Typecho_Router_Parser($routes);
            self::$_routingTable = $parser->parse();
        }
    }
}
```

代码分析：
1. 组件*Widget_Options*读取数据库表*typecho_options*中*name*的值为*routingTable*的记录，反序列化该记录中的*value*列，得到一个路由表数组。
2. 默认情况下，这个路由表数组的有效路由保存在索引值为0的元素里面，如果不存在该索引，则解析路由并将结果更新到数据库。
3. 最后，将 `$options->routingTable` 的值保存到 `Typecho_Router::$_routingTable` 中。

---

<!--more-->

#### 二、开始路由分发
typecho/var/Typecho/Router.php
```php
class Typecho_Router
{
    public static function dispatch()
    {
        /** 获取PATHINFO */
        $pathInfo = self::getPathInfo();

        foreach (self::$_routingTable as $key => $route) {
            if (preg_match($route['regx'], $pathInfo, $matches)) {
                self::$current = $key;

                try {
                    /** 载入参数 */
                    $params = NULL;

                    if (!empty($route['params'])) {
                        unset($matches[0]);
                        $params = array_combine($route['params'], $matches);
                    }

                    $widget = Typecho_Widget::widget($route['widget'], NULL, $params);

                    if (isset($route['action'])) {
                        $widget->{$route['action']}();
                    }

                    return;

                } catch (Exception $e) {
                    if (404 == $e->getCode()) {
                        Typecho_Widget::destory($route['widget']);
                        continue;
                    }

                    throw $e;
                }
            }
        }

        /** 载入路由异常支持 */
        throw new Typecho_Router_Exception("Path '{$pathInfo}' not found", 404);
    }
}

// 路由表长这个样子：
Array
(
    [index] => Array
        (
            [url] => /
            [widget] => Widget_Archive
            [action] => render
            [regx] => |^[/]?$|
            [format] => /
            [params] => Array()
        )

    [archive] => Array
        (
            [url] => /blog/
            [widget] => Widget_Archive
            [action] => render
            [regx] => |^/blog[/]?$|
            [format] => /blog/
            [params] => Array()
        )
)
```

代码分析：
1. 获取 *PATHINFO*，比如用户访问的URL为：*http://localhost/typecho/index.php/123/456?a=1*，则PATHINFO为：*/123/456*。
2. 根据 PATHINFO 的值，在路由表中遍历，寻找是否有匹配的路由规则。(主要代码：`preg_match($route['regx'], $pathInfo, $matches`)
3. 以 PATHINFO 为 */* 为例。遍历路由表，最终找到匹配项：*index*。接着，调用 `Typecho_Widget::widget("Widget_Archive", NULL, $params)`生成一个 *Widget_Archive* 实例。如果匹配值存在 *action* 索引，则获取该匹配值索引号为 *action* 的值，这里为 *render*。接着，调用 *Widget_Archive* 的 *render* 方法。（部分代码：`$widget->{$route['action']}();`）

---

### 相关资料
[typecho 设计文档 - Router](http://docs.typecho.org/develop/route)

> 备注：官方的设计文档很久没更新（最后编辑时间：2013/10/21 14:55），和现在最新的 *typecho* 代码有很大出入。
