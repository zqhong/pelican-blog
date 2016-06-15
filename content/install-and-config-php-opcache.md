Title: 安装和配置 Opcache
Date: 2016-03-19 19:23
Category: PHP
Tags: php, opcache
Slug: install-and-config-php-opcache
Author: zqhong

### Opcache 简介
PHP 解释器执行 PHP 脚本会先将脚本内容转换成 [opcode](http://www.laruence.com/2008/06/18/221.html)，然后再执行字节码。但这样有一个问题，每次都这样，浪费很多资源。解决办法很简单，就是把字节码缓存起来。目前，对于 PHP 5.5 以上的版本，推荐使用 [Opcache](http://ua2.php.net/manual/zh/book.opcache.php)。旧版本可以考虑：[APC](http://php.net/manual/zh/book.apc.php)、[XCache](http://xcache.lighttpd.net/)


Opcache 官网介绍：
OPcache 通过将 PHP 脚本预编译的字节码存储到共享内存中来提升 PHP 的性能， 存储预编译字节码的好处就是 省去了每次加载和解析 PHP 脚本的开销。

---

### 安装 Opcache
如何安装请看这里：[PHP - Opcache Installing](http://ua2.php.net/manual/en/opcache.installation.php)

简单的说，对于 PHP 5.5.0+ 的版本，在编译的时候加上 **--enable-opcache** 这个参数，并在 php.ini 中添加`zend_extension=/full/path/to/opcache.so `启用 Opcache 即可。

---

### 配置 Opcache
1. 在网站根目录新建一个 *phpinfo.php* 的文件，内容为：
```php
<?php
echo phpinfo();

```
2. 使用浏览器访问该文件，比如：`http://hostname.com/phpinfo.php`
3. 找到这一行：**Loaded Configuration File    /path/to/php.ini**
4. 编辑上面那个 *php.ini* 文件，修改内容为：
```
[opcache]
; OPcache 的共享内存大小，单位：MB
opcache.memory_consumption=64

; 用来存储临时字符串的内存大小，单位：MB
opcache.interned_strings_buffer=16

; OPcache 哈希表中可存储的脚本文件数量上限
opcache.max_accelerated_files=4000

opcache.fast_shutdown=1

; 注意，这里我将 validate_timestamps 设置为 0，Opcache 不会自动更新你的脚本
; 如果你需要了脚本文件，需要手动重启 Web 服务器 或者使用 opcache_reset() 函数
opcache.validate_timestamps=0

; 同样的，还是在上面的网页中找到 extension_dir 这个配置项，然后把你自己的 opcache.so 的路径写进去即可。
zend_extension=/path/to/opcache.so
```
5. 重启 php
```
# 如果服务器是 Nginx
$ /etc/init.d/php-fpm restart

# 如果服务器是 Apache，直接重启 Apache 即可
$ /etc/init.d/apache restart
```
6. 最后，重新打开上面的地址。如果能看到下面的内容，则说明成功。
![Opcache-Successful](https://www.sinaimg.cn/large/ce744de6gw1f22eu6hacrj20qm0dsdi9.jpg)

---

### reset Opcache
1. 如果使用的服务器是 Apache
```
$ service httpd reload
$ apachectl graceful
```
2. 如果是 PHP-FPM（一般 Nginx 会采用这种方式）
```
$ service php-fpm reload
```

> 注意：如果你的代码修改了，但是访问网站后发现无效。这个时候就要怀疑是不是缓存的问题了。

<!--more-->

### 相关资料
[PHP - Opcache Installing](http://ua2.php.net/manual/zh/opcache.installation.php)
[PHP - Opcache 运行时配置](http://ua2.php.net/manual/zh/opcache.configuration.php)
[使用 OpCache 提升 PHP 5.5+ 程序性能](https://phphub.org/topics/301)
[opcache.fast_shutdown=1导致cphalcon莫名其妙的的错误](http://www.ximici.com/2014/09/04/opcache-fast_shutdown1%E5%AF%BC%E8%87%B4cphalcon%E8%8E%AB%E5%90%8D%E5%85%B6%E5%A6%99%E7%9A%84%E7%9A%84%E9%94%99%E8%AF%AF/?ckattempt=1)
[深入理解PHP原理之Opcodes](http://www.laruence.com/2008/06/18/221.html)
[PHP 之道 - 缓存](http://wiki.jikexueyuan.com/project/php-right-way/cache.html)
