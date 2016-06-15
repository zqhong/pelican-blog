Title: typecho 源码分析：2、Widget
Date: 2016-02-26 16:08
Category: PHP
Tags: typecho, php, widget
Slug: typecho-code-analysis-widget
Author: zqhong

### Widget 分析

#### 一、Widget 超类 Typecho_Widget
所有 Widget 都继承这个类，所以很有必要了解这个类。

*typecho/var/Typecho/Widget.php*
```php
abstract class Typecho_Widget
{
    private static $_widgetAlias = array();

    private static $_widgetPool = array();

    public $request;

    public $response;

    public $parameter;

    public function __construct($request, $response, $params = NULL)
    {
        //设置函数内部对象
        $this->request = $request;
        $this->response = $response;
        $this->parameter = new Typecho_Config();

        if (!empty($params)) {
            $this->parameter->setDefault($params);
        }
    }

    public static function widget($alias, $params = NULL, $request = NULL, $enableResponse = true)
    {
        $parts = explode('@', $alias);
        $className = $parts[0];
        $alias = empty($parts[1]) ? $className : $parts[1];

        if (isset(self::$_widgetAlias[$className])) {
            $className = self::$_widgetAlias[$className];
        }

        if (!isset(self::$_widgetPool[$alias])) {
            /** 如果类不存在 */
            if (!class_exists($className)) {
                throw new Typecho_Widget_Exception($className);
            }

            /** 初始化request */
            if (!empty($request)) {
                $requestObject = new Typecho_Request();
                $requestObject->setParams($request);
            } else {
                $requestObject = Typecho_Request::getInstance();
            }

            /** 初始化response */
            $responseObject = $enableResponse ? Typecho_Response::getInstance()
            : Typecho_Widget_Helper_Empty::getInstance();

            /** 初始化组件 */
            $widget = new $className($requestObject, $responseObject, $params);

            $widget->execute();
            self::$_widgetPool[$alias] = $widget;
        }

        return self::$_widgetPool[$alias];
    }
}
```

代码分析：
`Typecho_Widget::widget` 是负责生产 widget 的工厂方法。生产并初始化一个 widget 实例，然后执行这个实例对象的 *execute* 方法。最后将生产出来的 widget 放在 `Typecho_Widget::$_widgetPool` 中。

<!--more-->

#### 二、初始化组件
程序在 *index.php* 在调用 *Typecho_Widget::widget("Widget_Init")*，生成 Widget_Init 实例，并执行该实例的 *execute* 方法。*execute*才是真正实现组件初始化的地方。


*typecho/var/Widget/Init.php*
```php
class Widget_Init extends Typecho_Widget
{
    public function execute()
    {
        /** 对变量赋值 */
        $options = $this->widget('Widget_Options');

        /** 语言包初始化 */
        if ($options->lang && $options->lang != 'zh_CN') {
            $dir = defined('__TYPECHO_LANG_DIR__') ? __TYPECHO_LANG_DIR__ : __TYPECHO_ROOT_DIR__ . '/usr/langs';
            Typecho_I18n::setLang($dir . '/' . $options->lang . '.mo');
        }

        /** cookie初始化 */
        Typecho_Cookie::setPrefix($options->rootUrl);

        /** 初始化charset */
        Typecho_Common::$charset = $options->charset;

        /** 初始化exception */
        Typecho_Common::$exceptionHandle = 'Widget_ExceptionHandle';

        /** 设置路径 */
        if (defined('__TYPECHO_PATHINFO_ENCODING__')) {
            $pathInfo = $this->request->getPathInfo(__TYPECHO_PATHINFO_ENCODING__, $options->charset);
        } else {
            $pathInfo = $this->request->getPathInfo();
        }

        Typecho_Router::setPathInfo($pathInfo);

        /** 初始化路由器 */
        Typecho_Router::setRoutes($options->routingTable);

        /** 初始化插件 */
        Typecho_Plugin::init($options->plugins);

        /** 初始化回执 */
        $this->response->setCharset($options->charset);
        $this->response->setContentType($options->contentType);

        /** 默认时区 */
        if (function_exists("ini_get") && !ini_get("date.timezone") && function_exists("date_default_timezone_set")) {
            @date_default_timezone_set('UTC');
        }

        /** 初始化时区 */
        Typecho_Date::setTimezoneOffset($options->timezone);

        /** 开始会话, 减小负载只针对后台打开session支持 */
        if ($this->widget('Widget_User')->hasLogin()) {
            @session_start();
        }

        /** 监听缓冲区 */
        ob_start();
    }

    // 从父类继承过来的魔术方法，这里是没有的。写在这里是为了容易查看
    public function __get($name)
    {
        if (array_key_exists($name, $this->row)) {
            return $this->row[$name];
        } else {
            $method = '___' . $name;

            if (method_exists($this, $method)) {
                return $this->$method();
            } else {
                $return = $this->pluginHandle()->trigger($plugged)->{$method}($this);
                if ($plugged) {
                    return $return;
                }
            }
        }

        return NULL;
    }

    // 也是从父类继承过来的魔术方法。
    public function __set($name, $value)
    {
        $this->row[$name] = $value;
    }
}

```

代码分析：
1. 生产一个叫 *Widget_Options* 的实例，该实例的 *execute* 方法会去读取数据表 *typecho_options* 的数据。将获取到的数据，保存到自身的 *row* 属性中。接着，初始化站点信息、设置皮肤目录、初始化路由表等。
2. 说下初始化路由表这部分。路由表本身是一个数组，被序列化保存在数据库中。在初始化时，读取数据库的配置信息，并将路由表反序列化。路由表将需要解析的路由保存到自身值为 0 索引中。当不存在该索引时，系统将解析路由并缓存。


注意点：
> * 当访问不可访问属性的值时，从父类继承过来的 *\_\_get* 魔术方法会被调用。假如我们访问一个不可访问的属性叫 "url"，这个时候系统将调用 *\_\_get* 方法，*\_\_get* 方法首先看 *$this=>row["url"]* 是否存在，不存在的话，看本身是否有 *\_\_url* 方法。同样的，当用户给一个不可访问的属性赋值时，从父类继承过来的 *\_\_set* 魔术方法将被调用。该方法将用户的数据保存在 *$this->row* 数组中。
> * 上面提到的 *typecho_options* 数据表是默认的情况，如果你设置了别的数据表前缀，就不是这个值了。

---

### 相关资料
[typecho - Widget设计文档](http://docs.typecho.org/develop/widget)
