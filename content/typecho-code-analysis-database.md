Title: typecho 源码分析：4、Database
Date: 2016-03-04 11:46
Category: PHP
Tags: typecho, php, database
Slug: typecho-code-analysis-database
Author: zqhong

### Typecho_Db
Typecho 没有 Model 层，采用自建的 DB 类帮助开发者快速获取自己需要的数据。

#### 一、初始化数据库
*config.inc.php*
```php
# 这里的配置文件只作为参考，可能和你自己的配置文件有出入。
$db = new Typecho_Db('Pdo_Mysql', 'typecho_');
$db->addServer(array (
  'host' => 'localhost',
  'user' => 'username',
  'charset' => 'utf8',
  'port' => 'password',
  'database' => 'typecho',
), Typecho_Db::READ | Typecho_Db::WRITE);
Typecho_Db::set($db);
```

*typecho/var/Typecho/Db.php*
```php
class Typecho_Db
{
    private static $_instance;

    public function __construct($adapterName, $prefix = 'typecho_')
    {
        /** 获取适配器名称 */
        $this->_adapterName = $adapterName;

        /** 数据库适配器 */
        $adapterName = 'Typecho_Db_Adapter_' . $adapterName;

        if (!call_user_func(array($adapterName, 'isAvailable'))) {
            throw new Typecho_Db_Exception("Adapter {$adapterName} is not available");
        }

        $this->_prefix = $prefix;

        /** 初始化内部变量 */
        $this->_pool = array();
        $this->_connectedPool = array();
        $this->_config = array();

        //实例化适配器对象
        $this->_adapter = new $adapterName();
    }

    public function addServer($config, $op)
    {
        $this->_config[] = Typecho_Config::factory($config);
        $key = count($this->_config) - 1;

        /** 将连接放入池中 */
        switch ($op) {
            case self::READ:
            case self::WRITE:
                $this->_pool[$op][] = $key;
                break;
            default:
                $this->_pool[self::READ][] = $key;
                $this->_pool[self::WRITE][] = $key;
                break;
        }
    }

    public static function get()
    {
        if (empty(self::$_instance)) {
            /** Typecho_Db_Exception */
            throw new Typecho_Db_Exception('Missing Database Object');
        }

        return self::$_instance;
    }

    public static function set(Typecho_Db $db)
    {
        self::$_instance = $db;
    }
}
```

代码分析：
1. 初始化内部变量（`$this->_pool, $this->_connectedPool、$this->_config`）和实例化适配器对象,这里的适配器对象为：*Typecho_Db_Adapter_Pdo_Mysql*（`$this->_adapter`）。
2. 添加配置信息到 `$this->_config` 中。然后，将配置信息在 `$this->_config` 中的 key 保存到对应的连接池中。（这里假设数据库操作为读，`$this->_pool[self::READ][] = $key`）
3. 最后，将实例化后的 Typecho_Db 对象保存在 `Typecho_Db::$_instance` 中。

> 备注：上面的 *$this* 指的是 Typecho_Db 实例对象

---

<!--more-->

#### 二、Typecho如何实现数据库查询
```php
$db = Typecho_Db::get();
$select = $db->select()->from("table.options")->where("user = 0");
$result = $db->fetchAll($select);
```

```php
class Typecho_Db
{
    private static $_instance;

    public static function get()
    {
        if (empty(self::$_instance)) {
            /** Typecho_Db_Exception */
            throw new Typecho_Db_Exception('Missing Database Object');
        }

        return self::$_instance;
    }

    public function sql()
    {
        return new Typecho_Db_Query($this->_adapter, $this->_prefix);
    }

    public function select()
    {
        $args = func_get_args();
        return call_user_func_array(array($this->sql(), 'select'), $args ? $args : array('*'));
    }

    public function query($query, $op = self::READ, $action = self::SELECT)
    {
        /** 在适配器中执行查询 */
        if ($query instanceof Typecho_Db_Query) {
            $action = $query->getAttribute('action');
            $op = (self::UPDATE == $action || self::DELETE == $action
            || self::INSERT == $action) ? self::WRITE : self::READ;
        } else if (!is_string($query)) {
            /** 如果query不是对象也不是字符串,那么将其判断为查询资源句柄,直接返回 */
            return $query;
        }

        /** 选择连接池 */
        $handle = $this->selectDb($op);

        /** 提交查询 */
        $resource = $this->_adapter->query($query, $handle, $op, $action);

        if ($action) {
            //根据查询动作返回相应资源
            switch ($action) {
                case self::UPDATE:
                case self::DELETE:
                    return $this->_adapter->affectedRows($resource, $handle);
                case self::INSERT:
                    return $this->_adapter->lastInsertId($resource, $handle);
                case self::SELECT:
                default:
                    return $resource;
            }
        } else {
            //如果直接执行查询语句则返回资源
            return $resource;
        }
    }

    public function selectDb($op)
    {
        if (!isset($this->_connectedPool[$op])) {
            if (empty($this->_pool[$op])) {
                /** Typecho_Db_Exception */
                throw new Typecho_Db_Exception('Missing Database Connection');
            }

            //获取相应读或写服务器连接池中的一个
            $selectConnection = rand(0, count($this->_pool[$op]) - 1);
            //获取随机获得的连接池配置
            $selectConnectionConfig = $this->_config[$this->_pool[$op][$selectConnection]];
            $selectConnectionHandle = $this->_adapter->connect($selectConnectionConfig);
            $this->_connectedPool[$op] = &$selectConnectionHandle;

        }

        return $this->_connectedPool[$op];
    }

    public function fetchAll($query, array $filter = NULL)
    {
        //执行查询
        $resource = $this->query($query, self::READ);
        $result = array();

        /** 取出过滤器 */
        if (!empty($filter)) {
            list($object, $method) = $filter;
        }

        //取出每一行
        while ($rows = $this->_adapter->fetch($resource)) {
            //判断是否有过滤器
            $result[] = $filter ? call_user_func(array(&$object, $method), $rows) : $rows;
        }

        return $result;
    }
}

class Typecho_Db_Query
{
    public function select($field = '*')
    {
        $this->_sqlPreBuild['action'] = Typecho_Db::SELECT;
        $args = func_get_args();

        $this->_sqlPreBuild['fields'] = $this->getColumnFromParameters($args);
        return $this;
    }

    public function from($table)
    {
        $this->_sqlPreBuild['table'] = $this->filterPrefix($table);
        return $this;
    }

    public function where()
    {
        $condition = func_get_arg(0);
        $condition = str_replace('?', "%s", $this->filterColumn($condition));
        $operator = empty($this->_sqlPreBuild['where']) ? ' WHERE ' : ' AND';

        if (func_num_args() <= 1) {
            $this->_sqlPreBuild['where'] .= $operator . ' (' . $condition . ')';
        } else {
            $args = func_get_args();
            array_shift($args);
            $this->_sqlPreBuild['where'] .= $operator . ' (' . vsprintf($condition, $this->quoteValues($args)) . ')';
        }

        return $this;
    }

    public function __toString()
    {
        switch ($this->_sqlPreBuild['action']) {
            case Typecho_Db::SELECT:
                return $this->_adapter->parseSelect($this->_sqlPreBuild);
            case Typecho_Db::INSERT:
                return 'INSERT INTO '
                . $this->_sqlPreBuild['table']
                . '(' . implode(' , ', array_keys($this->_sqlPreBuild['rows'])) . ')'
                . ' VALUES '
                . '(' . implode(' , ', array_values($this->_sqlPreBuild['rows'])) . ')'
                . $this->_sqlPreBuild['limit'];
            case Typecho_Db::DELETE:
                return 'DELETE FROM '
                . $this->_sqlPreBuild['table']
                . $this->_sqlPreBuild['where'];
            case Typecho_Db::UPDATE:
                $columns = array();
                if (isset($this->_sqlPreBuild['rows'])) {
                    foreach ($this->_sqlPreBuild['rows'] as $key => $val) {
                        $columns[] = "$key = $val";
                    }
                }

                return 'UPDATE '
                . $this->_sqlPreBuild['table']
                . ' SET ' . implode(' , ', $columns)
                . $this->_sqlPreBuild['where'];
            default:
                return NULL;
        }
    }
}
```

代码分析：
1. 获取数据库对象实例（`Typecho_Db::get()`）
2. 使用 *Typecho_Db_Query* 构造 SQL 语句。其中 `$db->select()` 返回 *Typecho_Db_Query* 实例化对象。
3. 执行查询操作

如果对这部分有兴趣，请深入代码了解。


### 相关资料
[typecho 设计文档 - database](http://docs.typecho.org/develop/db)
