Title: gdb 笔记
Date: 2016-10-16 15:42
Category: DEBUG
Tags: gdb,debug,note,随想
Slug: gdb-manual
Author: zqhong

# 笔记
gdb program_name
启动 GDB 开始调试

break
break function，在函数 funtion 入口处设置 breakpoint。

step
step [count]:如果没有指定 count, 则继续执行程序，直到到达与当前源文件不同的源文件中时停止；如果指定了 count,则重复行上面的过程 count 次

next
next [count]:如果没有指定 count, 单步执行下一行程序；如果指定了 count，单步执行接下来的 count 行程序

finish
finish:继续执行程序，直到当前被调用的函数结束，如果该函数有返回值，把返回值也打印到控制台

run
运行调试的程序

info threads
显示当前可调试的所有线程，每个线程会有一个 GDB 为其分配的 ID，后面操作线程的时候会用到这个 ID。 前面有*的是当前调试的线程。

thread ID
切换当前调试的线程为指定 ID 的线程。


# gdb cheat sheet
http://darkdust.net/files/GDB%20Cheat%20Sheet.pdf