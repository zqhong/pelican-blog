Title: 全站使用HTTPS（StartSSL+Nginx）
Date: 2016-01-21 14:01
Category: WEB
Tags: SSL, Nginx
Slug: add-ssl-certificate-on-your-domain
Author: zqhong

### 1、开通企业邮箱
这里使用的是阿里云企业邮箱，大致步骤：**1、添加解析   2、设置密码   3、分配员工账号**。具体请参考：[阿里云企业邮箱开通指南](https://help.aliyun.com/knowledge_detail/6555183.html?spm=5176.200037.n2.7.mA5m6G)。

> 备注：申请SSL证书需要确认申请人是否拥有域名的管理权。一般会发验证链接到 postmaster@yourdomain.com 或 admin@yourdomain.com。

---

### 2、申请证书
*i.zqhong.com*现在使用的是[StartSSL](https://www.startssl.com/)的免费证书。关于SSL证书的选择，可以参考：[最便宜的SSL证书 - 乔大海](https://qiaodahai.com/cheapest-ssl-certificates.html)。申请过程很简单，这里不再说明。

<!--more-->

---

### 3、配置服务器
以*nginx*为例。
```
# /etc/nginx/conf.d/default.conf
server {
    server_name yourdomain.com;
    listen 443;
    ssl on;
    ssl_certificate /usr/local/nginx/conf/server.crt;
    ssl_certificate_key /usr/local/nginx/conf/server.key;
}
```

如果是*Apache*，请参考：[Apache SSL Installation Instructions](https://www.sslshopper.com/apache-server-ssl-installation-instructions.html)、[SSL/TLS Strong Encryption: How-To](https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html)、[openssl建立证书，非常详细配置ssl+apache](http://blog.51yip.com/apachenginx/958.html)。下面是简单的配置：
```
LoadModule ssl_module modules/mod_ssl.so

Listen 443
<VirtualHost *:443>
    ServerName www.example.com
    SSLEngine on
    SSLCertificateFile "/path/to/www.example.com.cert"
    SSLCertificateKeyFile "/path/to/www.example.com.key"
</VirtualHost>
```

### 4、测试
[ssllabs](https://www.ssllabs.com/ssltest/index.html)提供免费的SSL测试，提交你想测试的域名即可。或者直接使用现代浏览器访问你要测试的域名。

---

### 5、提交你的域名到 HSTS Preload Submission
将域名提交到 [HSTS Preload Submission](https://hstspreload.appspot.com/)的好处是：
1. 现代浏览器默认会使用 https 访问你的网站，无论你有没有加 https
2. 如果你的域名在浏览器内置的HSTS列表中，即使第一次访问你的网站，也会使用 https 连接。保证了初始连接的安全。

域名提交成功后，需要等几周的时间。如果你的域名出现在 [transport_security_state_static.json](https://code.google.com/p/chromium/codesearch#chromium/src/net/http/transport_security_state_static.json) 就说明已经成功啦。
关于HSTS的更多信息，可以查看：[HTTP严格传输安全](https://zh.wikipedia.org/wiki/HTTP%E4%B8%A5%E6%A0%BC%E4%BC%A0%E8%BE%93%E5%AE%89%E5%85%A8)

---

### 6、参考配置
下面是我使用的配置，环境是：Debian + Nginx + PHP-FPM。详细请参考：[分享一个 HTTPS A+ 的 nginx 配置](https://www.textarea.com/zhicheng/fenxiang-yige-https-a-di-nginx-peizhi-320/)

> 备注：使用`openssl dhparam -dsaparam -out dhparam.pem 4096` 生成 *dhparam.pem*。这里如果不加**-dsaparam**参数速度会相当的慢。

```
# /etc/nginx/conf.d/i.zqhong.com.conf
server {
    # 博客
    server_name  i.zqhong.com;
    listen 443;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
    index index.html index.htm index.php;
    root /usr/share/nginx/xxxx;
    include /etc/nginx/secure_params;

    location / {
            #rewrite rule for typecho staticize
             if (!-e $request_filename) {
                 rewrite ^/(.*)$ /index.php/$1 last;
             }
    }
    location ~ ^.+\.php {
            fastcgi_pass unix:/var/run/php5-fpm.sock;
            fastcgi_index index.php;
            fastcgi_split_path_info ^(.+\.php)(/.+)$;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include fastcgi_params;
    }
}

# /etc/nginx/secure_params
ssl on;
ssl_certificate /root/xxx.crt;
ssl_certificate_key /root/xxx.key;
ssl_dhparam /root/dhparam.pem;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
ssl_stapling on;
ssl_ciphers "ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA";
ssl_prefer_server_ciphers on;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
```

---

### 相关术语
#### [HTTPS（维基百科）](https://zh.wikipedia.org/wiki/%E8%B6%85%E6%96%87%E6%9C%AC%E4%BC%A0%E8%BE%93%E5%AE%89%E5%85%A8%E5%8D%8F%E8%AE%AE)
超文本传输安全协议（英语：Hypertext Transfer Protocol Secure，缩写：HTTPS）是一种网络安全传输协议。在计算机网络上，**HTTPS经由超文本传输协议进行通讯，但利用SSL/TLS来对数据包进行加密**。HTTPS开发的主要目的，是提供对网络服务器的身份认证，保护交换数据的隐私与完整性。

#### [HSTS（维基百科）](https://zh.wikipedia.org/wiki/HTTP%E4%B8%A5%E6%A0%BC%E4%BC%A0%E8%BE%93%E5%AE%89%E5%85%A8)
HTTP严格传输安全（英语：HTTP Strict Transport Security，缩写：HSTS）是一套由互联网工程任务组发布的互联网安全策略机制。网站可以选择使用HSTS策略，来**让浏览器强制使用HTTPS与网站进行通信，以减少会话劫持风险**。

---

### 相关链接
[阿里云企业邮箱开通指南](https://help.aliyun.com/knowledge_detail/6555183.html?spm=5176.200037.n2.7.mA5m6G)
[分享一个 HTTPS A+ 的 nginx 配置](https://www.textarea.com/zhicheng/fenxiang-yige-https-a-di-nginx-peizhi-320/)
[HSTS Preload Submission](https://hstspreload.appspot.com/)
[ssllabs](https://www.ssllabs.com/ssltest/index.html)
[Apache SSL Installation Instructions](https://www.sslshopper.com/apache-server-ssl-installation-instructions.html)
[SSL/TLS Strong Encryption: How-To](https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html)
[openssl建立证书，非常详细配置ssl+apache](http://blog.51yip.com/apachenginx/958.html)
