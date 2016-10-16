Title: Is there a way to use PhantomJS in Python?
Date: 2016-10-16 16:54
Category: 随笔
Tags: 随笔
Slug: using-phantomjs-in-python
Author: zqhong


# Is there a way to use PhantomJS in Python?

```
from selenium import webdriver

driver = webdriver.PhantomJS() # or add to your PATH
driver.set_window_size(1024, 768) # optional
driver.get('https://google.com/')
driver.save_screenshot('screen.png') # save a screenshot to disk
sbtn = driver.find_element_by_css_selector('button.gbqfba')
sbtn.click()
```

http://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python