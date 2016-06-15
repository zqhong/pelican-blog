Title: PhpStorm 使用 Composer 安装配置 PHPUnit
Date: 2016-03-02 14:09
Category: PHP
Tags: typecho, php, widget
Slug: PhpStorm-Enabling-PHPUnit-Support-Use-Composer
Author: zqhong

### 配置 Composer
#### Command Line Tool Support 添加 Composer
**File - Settings - Tools - Command Line Tool Support**，配置 Composer。
![PhpStorm-Composer-Settings](https://www.sinaimg.cn/large/ce744de6gw1f1ihqi13ypj20tr0jatcf.jpg)

> 备注：如果在 Tools 中没有看到 Command Line Tool Support，请在 Plugins 启用或安装 Command Line Tool Support。

#### 使用 Composer 添加 PHPUnit
**Tools - Composer - Add Dependency**，搜索 **phpunit/phpunit**，这里安装的是 **PHPUnit 4.8.23**。
![Search-PHPUnit](https://www.sinaimg.cn/large/ce744de6gw1f1ihzdiu7fj20n20f0dia.jpg)

> 备注：PhpStorm 9.0 对 PHPUnit 5.x 的支持不好。如果需要使用 PHPUnit 5.x，请尝试升级使用 PhpStorm 10。另外，Composer 在国内不怎么稳定，如果一直无法获取 packages，请尝试使用国外代理 或 使用 Composer 镜像。

<!--more-->

---

### 配置 PHPUnit 和 运行测试
#### 配置 PHPUnit
**File - Settings - Languages & Frameworks - PHP - PHPUnit**，因为我们使用的是 Composer 安装，所以选择第二选项 "*Use custom autoloader*"。然后，可以根据需要配置 *Default configuration file*（默认配置文件） 和 *Default bootstrap file*（默认启动文件，运行测试文件前会先加载这个文件）。
![PHPUnit-Configuration](https://www.sinaimg.cn/large/ce744de6gw1f1iic57zsvj20tr0lugol.jpg)

#### 创建测试
打开需要测试的文件，**Navigate - Test (Ctrl+Shift+T) - Create New Test**，根据自己的需要，输入文件名、文件路径等信息。
![Create-New-Test](https://www.sinaimg.cn/large/ce744de6gw1f1iih4l8drj20aj0b8dhd.jpg)

#### 执行测试
勾选 **View - Toolbar**，显示工具栏。然后，打开你的测试文件。接着，打开工具栏中的 "*Edit Configurations*"。根据自己的需要配置。最后点击工具栏中的 **Run** 图标。
![Click-Edit-Configrations](https://www.sinaimg.cn/large/ce744de6gw1f1iik0nil6j20ss068ace.jpg)
![Run/Debug Configurations](https://www.sinaimg.cn/large/ce744de6gw1f1iiloi47ej20uc0jkdja.jpg)
![Start-Run](https://www.sinaimg.cn/large/ce744de6gw1f1iip191ksj20i502jt9a.jpg)

---

### 坑
PhpStorm 9.0 不支持 PHPUnit 5.2，换成 PHPUnit 4.8 就行了。PhpStorm 配置 PHPUnit 不难，但是因为这个坑。。浪费了不少时间。

---

### 相关资料
[PHPUnit support in PhpStorm](https://confluence.jetbrains.com/display/PhpStorm/PHPUnit+support+in+PhpStorm)
[Enabling PHPUnit Support](https://www.jetbrains.com/phpstorm/help/enabling-phpunit-support.html)
[PHPUnit安装配置及样例](http://blog.coinidea.com/web%E5%BC%80%E5%8F%91/php-1088.html)
