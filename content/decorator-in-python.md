Title: Python 中的装饰器
Date: 2016-04-08 17:05
Category: Python
Tags: python, decorator
Slug: decorator-in-python
Author: zqhong

### 一个简单的例子
```python
# coding: utf8

from __future__ import print_function


def decorator(func):
    def wrap():
        print("I am doing some boring work before executing func()")
        return func()
        print("I am doing some boring work after executing func()")
    return wrap

def func():
    print("I am the function which needs some decoration to remove my foul smell")

func = decorator(func)
func()

# Output:
# I am doing some boring work before executing func()
# I am the function which needs some decoration to remove my foul smell
# I am doing some boring work after executing func()

```

解释：
`decorator`函数接收一个函数变量`func`，内置的`wrap`函数对接收到的函数变量`func`进行修饰。最后，返回修饰成功的`wrap`函数。


<!--more-->

---

### 使用 Python 的修饰器
```python
# coding: utf8

from __future__ import print_function


def decorator(func):
    def wrap():
        print("I am doing some boring work before executing func()")
        return func()
        print("I am doing some boring work after executing func()")
    return wrap

@decorator
def func():
    print("I am the function which needs some decoration to remove my foul smell")

func()
print(func.__name__)

# Output:
# I am doing some boring work before executing func()
# I am the function which needs some decoration to remove my foul smell
# I am doing some boring work after executing func()
# wrap

```

解释：
这个和第一个例子其实是一样的，只是更加方便。但这里存在一个问题，`func`函数的名字变成了 `wrap`。这并不是我们希望看到的。

---

### 解决方案
```python
# coding: utf8

from __future__ import print_function
from functools import wraps


def decorator(func):
    @wraps(func)
    def wrap():
        print("I am doing some boring work before executing func()")
        func()
        print("I am doing some boring work after executing func()")
    return wrap

@decorator
def func():
    print("I am the function which needs some decoration to remove my foul smell")

func()
print(func.__name__)

# Output:
# I am doing some boring work before executing func()
# I am the function which needs some decoration to remove my foul smell
# I am doing some boring work after executing func()
# func

```

---

### 使用场景1 - 授权
```python
from functools import wraps

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            authenticate()
        return f(*args, **kwargs)
    return decorated

```

---

### 使用场景2 - 日志
```python
from functools import wraps

def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging

@logit
def addition_func(x):
   """Do some math."""
   return x + x


result = addition_func(4)
# Output: addition_func was called
```

### 推荐阅读
[Python 进阶 - 修饰器](https://eastlakeside.gitbooks.io/interpy-zh/content/decorators/index.html)
[Python修饰器的函数式编程](http://coolshell.cn/articles/11265.html)
