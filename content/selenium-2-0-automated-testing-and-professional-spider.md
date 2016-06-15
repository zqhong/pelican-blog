Title: Selenium 2.0 自动化测试&高级爬虫
Date: 2016-05-08 11:04
Category: Python
Tags: Python, Selenium, 自动化, 测试
Slug: selenium-2-0-automated-testing-and-professional-spider
Author: zqhong

# Example1：登录网易邮箱
```
# coding: utf8

from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Netease(object):
    def __init__(self):
        # 使用到的 url
        self.login_url = "http://reg.163.com/"
        self.account_info_url = "http://reg.163.com/account/accountInfo.jsp"

        # 邮箱和密码，这里使用一个没用的账号用于测试
        self.email = "your_email"
        self.password = "your_password"

        # 获取 WebDriver 对象
        # 需要 ChromeDriver 的支持。
        # 根据系统下载：http://chromedriver.storage.googleapis.com/index.html?path=2.21/
        # 除了使用 Chrome，你也可以使用 Firefox、IE、Opera 等。用法差不多
        executable_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=executable_path)

        # 设置默认延迟
        self.delay = 60
        self.driver.set_page_load_timeout(60)
        self.driver.implicitly_wait(15)

    def login(self):
        # 打开登陆页面
        self.driver.get(self.login_url)

        # WebDriver 每次只能在一个页面上识别元素
        # 对于 frame 嵌套内的页面上的元素，直接定位是定位是定位不到的
        # 需要通过 switch_to_frame() 方法将当前定位的主体切换了 frame 里
        elem_login_by_account = self.driver.find_element(By.ID, "loginByAccount")
        elem_login_frame = elem_login_by_account.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(elem_login_frame)

        # 找到 email 输入框、password 输入框 和 登录按钮
        elem_email = self.driver.find_element(By.NAME, "email")
        elem_password = self.driver.find_element(By.NAME, "password")
        elem_dologin = self.driver.find_element(By.ID, "dologin")

        # 清除输入框内容（因为某些网站或浏览器可能会有记住用户名的功能）
        elem_email.clear()
        elem_password.clear()

        # 输入邮箱和密码
        elem_email.send_keys(self.email)
        elem_password .send_keys(self.password)

        # 点击登陆按钮
        elem_dologin.click()

        # 等待页面加载，直到页面出现 id 为 "accountManage" 的元素
        # 如果超过指定的时间（这里为 self.delay），则会抛出一个 TimeoutException 的异常
        WebDriverWait(self.driver, self.delay).until(
            EC.presence_of_element_located((By.ID, "accountManage"))
        )

    def run(self):
        self.login()

        # 打开用户信息页面
        self.driver.get(self.account_info_url)

        # 打印登录用户的昵称
        nickname = self.driver.find_element(By.CLASS_NAME, "clear")
        print(nickname.text)

        # 退出浏览器
        self.driver.quit()

if __name__ == '__main__':
    Netease().run()

```

> 请阅读以上代码，里面包含了 WebDriver 大部分的用法。

<!--more-->

---

# Example2：Selenium 2.0+PhantomJS
## PhantomJS 简介
PhantomJS is a headless WebKit scriptable with a JavaScript API. It has fast and native support for various web standards: DOM handling, CSS selector, JSON, Canvas, and SVG.

简单的说，PhantomJS 是个无头的（headless）浏览器。

下载地址：[http://phantomjs.org/download.html](http://phantomjs.org/download.html)

主要修改地方：
```
class Netease(object):
    def __init__(self):
        # 省略 ...
        # 这里写上 phantomjs 的路径
        executable_path = "C:\Python27\phantomjs.exe"
        self.driver = webdriver.PhantomJS(executable_path=executable_path)
        # 省略 ...

    def login(self):
        # 省略 ...
        # 请看这里：https://github.com/detro/ghostdriver/issues/159
        # 简单的说就是：如果 frame 元素没有 name 属性，GD 就会无法处理。
        # 使用 driver.switch_to_frame(1) 就能很好的解决当 iframes 没有 name 属性这个问题
        self.driver.switch_to.frame(1)
        # 省略 ...
```

---

# Example3：登录淘宝
```
# coding: utf8

from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time


class Alimama(object):
    def __init__(self):
        self.login_url = "https://www.alimama.com/member/login.htm?forward=http%3A%2F%2Fad.alimama.com%2Findex.htm"
        self.username = "your_username"
        self.password = "your_password"

        # executable_path = "C:\Program Files (x86)\Internet Explorer\IEDriverServer.exe"
        executable_path = "C:\Program Files (x86)\Internet Explorer\IEDriverServer_win32.exe"
        self.driver = webdriver.Ie(executable_path=executable_path)

        # set default delay time
        self.driver.set_page_load_timeout(60)
        self.driver.implicitly_wait(15)

    def random_wait(self):
        time.sleep(2.1 + random.randint(0, 3))

    def login(self):
        # open login page
        self.driver.get(self.login_url)

        # switch iframe
        iframe = self.driver.find_element(By.NAME, "taobaoLoginIfr")
        self.driver.switch_to.frame(iframe)

        # find elements
        elem_quick2static = self.driver.find_element(By.ID, "J_Quick2Static")       # 扫一扫登录 切换到 密码登录
        elem_username = self.driver.find_element(By.ID, "TPL_username_1")
        elem_password = self.driver.find_element(By.ID, "TPL_password_1")
        elem_login_btn = self.driver.find_element(By.ID, "J_SubmitStatic")

        # 出现 扫一扫登录 切换到 密码登录按钮，点击该按钮。切换到 密码登录 模式
        if elem_quick2static.is_displayed():
            elem_quick2static.click()

        # clear username and password
        elem_username.clear()
        elem_password.clear()

        # key your username and password
        elem_username.send_keys(self.username)
        elem_password.send_keys(self.password)

        # 等待数秒钟再登陆
        self.random_wait()
        elem_login_btn.click()

    def run(self):
        self.login()

if __name__ == '__main__':
    Alimama().run()
```

## 使用方法
使用 IE 浏览器，手动登陆一次。（第一次需要认证）接着使用程序自动登陆。

> 备注：[http://www.alimama.com/member/login.htm?forward=http%3A%2F%2Fad.alimama.com%2Findex.htm](http://www.alimama.com/member/login.htm?forward=http%3A%2F%2Fad.alimama.com%2Findex.htm) 这个登录页面不需要拖动滑块登录。

## 这里有几个我遇到的问题：
1. IE Driver 需要使用 32 位的，不然在 send_keys 的时候，速度异常的慢。
2. 需要设置一下 IE，Internet 选项 - 安全，每个区域都需要选中 "启用保护模式"。接着重启 IE。
3. 设置 IE 的字体大小为默认 （Ctrl + 0）
4. 在输入完用户名和密码的时候，不要马上点击登陆。不然无法登陆成功。（请看第 54 行代码）

---

# WebDriver API
## 定位
### 通过 find_element*
```
# 寻找单个元素
find_element_by_id()
find_element_by_name()
find_element_by_class_name()
find_element_by_tag_name()
find_element_by_link_text()
find_element_by_partial_link_text()
find_element_by_xpath()
find_element_by_css_selector()

# 寻找多个元素
find_elements_by_id()
find_elements_by_name()
find_elements_by_class_name()
find_elements_by_tag_name()
find_elements_by_link_text()
find_elements_by_partial_link_text()
find_elements_by_xpath()
find_elements_by_css_selector()
```

### 通过 By 定位
```
# find_element()方法需要两个参数：第一个参数是定位方式，这个由 By 提供；另
第二个参数是定位的值。
# 在使用 By 时需要将 By 类导入。from selenium.webdriver.common.by import By

# 寻找单个元素
find_element(By.ID,"kw")
find_element(By.NAME,"wd")
find_element(By.CLASS_NAME,"s_ipt")
find_element(By.TAG_NAME,"input")
find_element(By.LINK_TEXT,u"新闻")
find_element(By.PARTIAL_LINK_TEXT,u"新")
find_element(By.XPATH,"//*[@class='bg s_btn']")
find_element(By.CSS_SELECTOR,"span.bg s_btn_wr>input#su")

# 寻找多个元素，将 find_element 改为 find_elements
```

## 元素操作
```
# 方法
clear() 清除文本，如果是一个文件输入框
send_keys(*value) 在元素上模拟按键输入
click() 单击元素
submit()方法用于提交表单，这里特别用于没提交按钮的情况。

# 属性
size 返回元素的尺寸。
text 获取元素的文本。
get_attribute(name) 获得属性值。
is_displayed() 设置该元素是否用户可见。
```

## 控制浏览器
```
# 控制浏览器大小
driver.set_window_size(480, 800)

# 控制浏览器行为
# 后退
driver.back()
# 前进
driver.forward()
# 退出
driver.quit()
```

##　鼠标事件
```
perform() 执行所有 ActionChains 中存储的行为
context_click() 右击
double_click() 双击
drag_and_drop() 拖动
move_to_element() 鼠标悬停
```

### 一个简单的例子：右键操作
```
# 定位到要右击的元素
right_click =driver.find_element_by_id("xx")
# 对定位到的元素执行鼠标右键操作
ActionChains(driver).context_click(right_click).perform()
```

## 元素等待
###　显式等待
显式等待使 WebdDriver 等待某个条件成立时继续执行，否则在达到最大时长时抛弃超时异常
（TimeoutException）。
```
#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("http://www.baidu.com")
element = WebDriverWait(driver,5,0.5).until(
EC.presence_of_element_located((By.ID,"kw"))
)
element.send_keys('selenium')
driver.quit()
```

### 隐式等待
隐式等待是通过一定的时长等待页面所元素加载完成。哪果超出了设置的时长元素还没有被加载测抛
NoSuchElementException 异常。WebDriver 提供了 implicitly_wait()方法来实现隐式等待，默认设置为 0。它
的用法相对来说要简单的多。
```
#coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("http://www.baidu.com")
input_ = driver.find_element_by_id("kw22")
input_.send_keys('selenium')
driver.quit()
```

implicitly_wait()默认参数的单位为秒，本例中设置等待时长为 10 秒，首先这 10 秒并非一个固定的等
待时间，它并不影响脚本的执行速度。其次，它并不真对页面上的某一元素进行等待，当脚本执行到某个
元素定位时，如果元素可定位那么继续执行，如果元素定位不到，那么它将以轮询的方式不断的判断元素
是否被定位到，假设在第 6 秒钟定位到元素则继续执行。直接超出设置时长（10 秒）还没定位到元素则抛
出异常。
在上面的例子中，显然百度输入框的定位 id=kw22 是有误的，那么在超出 10 秒后将抛出异常。

## 多表单切换
在 web 应用中经常会遇到 frame 嵌套页面的应用，页 WebDriver 每次只能在一个页面上识别元素，对
于 frame 嵌套内的页面上的元素，直接定位是定位是定位不到的。这个时候就需要通过 switch_to_frame()
方法将当前定位的主体切换了 frame 里。
```
#coding=utf-8
from selenium import webdriver
import time
import os

driver = webdriver.Firefox()
file_path = 'file:///' + os.path.abspath('frame.html')
driver.get(file_path)
#切换到 iframe（id = "if"）
driver.switch_to_frame("if")
#下面就可以正常的操作元素了
driver.find_element_by_id("kw").send_keys("selenium")
driver.find_element_by_id("su").click()
time.sleep(3)
driver.quit()
```

---

# 相关资料
[Selenium Document - WebDriver](http://www.seleniumhq.org/docs/03_webdriver.jsp)
[Selenium Document - WebDriver Advanced Usage](http://www.seleniumhq.org/docs/04_webdriver_advanced.jsp)
[Selenium with Python](http://selenium-python.readthedocs.io/index.html)
[Selenium2自动化测试实战--基于Python语言](http://www.cnblogs.com/fnng/p/3542333.html)
[Can't switch between nested frames #159 - ghostdriver Issues](https://github.com/detro/ghostdriver/issues/159)

> 备注：WebDriver API 部分主要摘抄 《Selenium2自动化测试实战》 第四章内容。有兴趣的可以阅读这本书。或者看官方文档。
