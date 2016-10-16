Title: Running Selenium Headless Using xvfb
Date: 2016-10-16 15:35
Category: 随想
Tags: 随想,selenium
Slug: running-selenim-headless-using-xvfb
Author: zqhong

# Running Selenium Headless

First, install Xvfb:
```
$ sudo apt-get install xvfb xfonts-100dpi xfonts-75dpi xfonts-cyrillic xorg dbus-x11
```

Run Xvfb on this display, with access control off1:
```
# Xvfb :99 -ac
```

Now you need to ensure that your display is set to 99 before running the Selenium server (which itself launches the browser).
```
$ export DISPLAY=:99
$ firefox
```

# 参考
[Running Selenium Headless](http://www.alittlemadness.com/2008/03/05/running-selenium-headless/)