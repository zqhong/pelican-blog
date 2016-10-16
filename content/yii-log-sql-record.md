Title: Yii 记录 SQL 执行记录
Date: 2016-10-16 15:34
Category: PHP
Tags: php,yii,随想
Slug: yii-log-sql-record
Author: zqhong


# Yii 记录 SQL 执行记录
需开启 DEBUG 模式。（ define("DEBUG", true);）

```
// 日志记录组件
'log' => array(
    'class' => '\CLogRouter',
    'routes' => array(
        array(
            'class'=>'\CWebLogRoute',   // CWebLogRoute 在网页中显示记录；CFileLogRoute 记录在文件中；添加 logFile 键值指定输出路径
            'categories'=>'system.db.*',
            'except'=>'system.db.ar.*', // shows all db level logs but nothing in the ar category,
            //'logFile' => 'sql.log',
        ),
    ),
),
```

http://www.yiiframework.com/doc/guide/1.1/en/topics.logging