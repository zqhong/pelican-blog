Title: Set phantomjs user-agent string
Date: 2016-10-16 15:37
Category: Python
Tags: python,随想,phantomjs
Slug: Set-Phantomjs-User-Agent-String
Author: zqhong


# 示例代码
```
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
"(KHTML, like Gecko) Chrome/15.0.87"
)
driver = webdriver.PhantomJS(desired_capabilities=dcap)
```


# 参考
[Set phantomjs user-agent string](https://coderwall.com/p/9jgaeq/set-phantomjs-user-agent-string)
