Title: lsof - list open files
Date: 2016-10-16 15:20
Category: Linux
Tags: Linux,随想,lsof,command,cli
Slug: list-open-files
Author: zqhong

# 简单用法
```
# 查看所有网络连接
sudo lsof -i
# 仅所有 IPV6 连接
sudo lsof -i 6
# 仅显示 TCP 连接
sudo lsof -iTCP
# 使用-i:port来显示与指定端口相关的网络信息
sudo lsof -i:22
#使用@host来显示指定到指定主机的连接
sudo lsof -i@172.16.12.5
```

> NOTE：某些信息需要有权限才能访问，必要时加上 sudo 或使用 root 用户执行 lsof 命令。


# 参考
[Linux 命令神器：lsof 入门](https://linux.cn/article-4099-1.html)
[每天一个linux命令（51）：lsof命令](http://www.cnblogs.com/peida/archive/2013/02/26/2932972.html)