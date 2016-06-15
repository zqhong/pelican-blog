Title: 使用iodine搭建DNS隧道
Date: 2016-02-16 13:36
Category: WEB
Tags: iodine, dns, proxy, tunnel
Slug: build-dns-tunnel
Author: zqhong

### 一、dns配置
以我的域名 **zqhong.com** 为例：
```
ns.zqhong.com NS t.zqhong.com. # 注意：最后需要一个 "."
t.zqhong.com  A  1.2.3.4       # 1.2.3.4 是你的服务器地址
```

---

### 二、服务端配置
1. 开启 Linux 的 ipv4 转发功能
```
$ sudo echo 1 > /proc/sys/net/ipv4/ip_forward
# 接着编辑 /etc/sysctl.conf，设置：net.ipv4.ip_forward=1
```
2. 允许DNS通过防火墙
```
# iptables -A INPUT -p udp --dport 53 -j ACCEPT
# iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
# iptables -t filter -A FORWARD -i eth0 -o dns0 -m state --state RELATED,ESTABLISHED -j ACCEPT
# iptables -t filter -A FORWARD -i dns0 -o eth0 -j ACCEPT
# iptables-save > /etc/iptables.rules
```
3. 启动 iodined
```
$ iodined -f -c -P password -p 53 172.16.0.0 ns.zqhong.com

参数说明：
-f 前段显示，用于调试
-c 显示客户端请求
-P 设置密码（最多32个字符）
-p 监听的端口号，默认为 53
172.16.0.0    tunnel_ip
ns.zqhong.com topdomain
```
4. 新增用户：
```
$ useradd -p password akira
```
5. 允许 ssh 密码登录
```
# 编辑文件：/etc/ssh/sshd_config，设置：PasswordAuthentication yes
# 重启 sshd
$ service sshd restart
```

<!--more-->

---

### 三、客户端配置
1. 安装客户端（Windows下，Linux用户请使用包管理器安装或直接源码编译）
请安装 **NDIS5** 版本的 [TAP Driver](https://openvpn.net/index.php/open-source/downloads.html)。接着下载 [iodine windows客户端](http://code.kryo.se/iodine/iodine-0.7.0-windows.zip)
> 备注：NDIS6 版本的 TAP Driver 有兼容性问题。
2. 启用客户端
```
# 如果这里使用，比 114.114.114.114 修改成其他 DNS服务器试试看。
# 比如：223.5.5.5（阿里）、8.8.8.8（谷歌）、199.91.73.222（V2EX）、114.114.115.115（114DNS）、180.76.76.76（百度DNS）
$ iodine.exe -f -P password 114.114.114.114 ns.zqhong.com

参数说明：
-f 前段显示，用于调试
-P 密码
114.114.114.114 nameserver，使用哪个DNS服务器，默认为系统指定的DNS服务器
ns.zqhong.com   topdomain
```
3. ping（保持连接，如果客户端超过60秒没有连接，会自动断开）
```
# 备注：到这一步，我们的客户机已经可以和服务器通讯了。这里的 172.16.0.0 相当于我们的服务器地址 1.2.3.4
$ ping 172.16.0.0 -t
```
4. ssh 端口转发
```
# 下面这条命令的意思是：所有连接到 127.0.0.1:9999 的请求都会被转发到 172.16.0.0:822
$ ssh -D 9999 -p 822 akira@172.16.0.0      # 接着输入密码：password
```
> 备注：这里我们的 ssh 端口是 822，如果不是 822，请修改

---


### 四、代理配置（windows 下）
1. 下载 Proxifier，下载地址：[https://www.proxifier.com/distr/ProxifierSetup.exe](https://www.proxifier.com/distr/ProxifierSetup.exe)
2. 注册码：（只适用于 Proxifier v3.x Setup版）
```
akira
MBZKT-ZWTSL-M8X24-3AN7T-NRWU6
```
3. 添加代理服务器
```
Profile - Proxy Servers - Add

Address  127.0.0.1
Port     9999
Type     SOCKS5
```
4. 将刚添加的代理服务器设置为默认代理
```
Profile - Proxification Runles，将上面那个 Rule（127.0.0.1:9999） 设置为 Default。
```

----


### 其他
#### windows 下安装 dig（dig用于调试，这步可忽略）
1. 在 [https://www.isc.org/downloads/](https://www.isc.org/downloads/) 下载适合你系统的 dig（x86 或 x64）
2. 解压缩下载好的压缩文件，安装 vcredist_xxx.exe
3. 复制 l*.dll 和 dig.exe 文件到 c:/windows/system32


#### DNS 测试
iodined服务端会响应所支持的请求中以“z”开头的请求，例如：
```
dig -t TXT z456.t1.mydomain.com
dig -t SRV z456.t1.mydomain.com
dig -t CNAME z456.t1.mydomain.com
```

例子：
```
$ dig -t TXT z456.ns.zqhong.com

; <<>> DiG 9.9.8-P3 <<>> -t TXT z456.ns.zqhong.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 37349
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4000
;; QUESTION SECTION:
;z456.ns.zqhong.com.            IN      TXT

;; ANSWER SECTION:
z456.ns.zqhong.com.     0       IN      TXT     "tpi0dknro"（被混淆的信息，如果能看到这个，说明 iodined 支持该DNS请求类型，这里是 TXT）

;; Query time: 15 msec
;; SERVER: 192.168.18.1#53(192.168.18.1)
;; WHEN: Mon Feb 15 16:51:57 ?D1ú±ê×?ê±?? 2016
;; MSG SIZE  rcvd: 69
```

---

### 相关资料
[iodine - wiki](http://dev.kryo.se/iodine/wiki)
[iodine - Linux man page](http://linux.die.net/man/8/iodine)
[iodine - IP over DNS](http://jeremy5189.logdown.com/posts/263029-iodine-ip-over-dns)
[iodine - README](http://code.kryo.se/iodine/README.html)
[Bypassing Captive Portals/Airport Pay Restrictions with Iodine on a Debian VPS Guide](http://www.putdispenserhere.com/bypassing-captive-portalsairport-pay-restrictions-with-iodine-on-a-debian-vps-guide/)
[SSH端口转发（隧道）](http://linux-wiki.cn/wiki/zh-hans/SSH%E7%AB%AF%E5%8F%A3%E8%BD%AC%E5%8F%91%EF%BC%88%E9%9A%A7%E9%81%93%EF%BC%89)
[Installing Dig on Windows](https://samsclass.info/40/proj/digwin.htm)

---

### 相关资源
[Installer(NDIS5) tap-windows-9.9.2_3.exe](https://swupdate.openvpn.org/community/releases/tap-windows-9.9.2_3.exe)
[iodine-0.7.0-windows.zip](http://code.kryo.se/iodine/iodine-0.7.0-windows.zip)
[ProxifierSetup.exe](https://www.proxifier.com/distr/ProxifierSetup.exe)
