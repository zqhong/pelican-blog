Title: MySQL 常用中间件介绍
Date: 2016-10-16 15:46
Category: 随笔
Tags: 随笔
Slug: mysql-proxy
Author: zqhong

# mysql-proxy
官方提供的 mysql 中间件产品可以实现负载平衡，读写分离， failover 等，但其不支持大数据量的分库分表且性能较差。

# Atlas
由 Qihoo 360, Web 平台部基础架构团队开发维护的一个基于 MySQL 协议的数据中间层项目。它是在 mysql-proxy 0.8.2 版本的基础上，对其进行了优化，增加了一些新的功能特性。360 内部使用 Atlas 运行的 mysql 业务，每天承载的读写请求数达几十亿条。

# Cobar
阿里巴巴（ B2B）部门开发的一种关系型数据的分布式处理系统，它可以在分布式的环境下看上去像传统数据库一样为您提供海量数据服务。

# heisenberg
强大好用的 mysql 分库分表中间件,来自百度。

# 参考
[mycat分布式mysql中间件（mysql中间件研究)](http://songwie.com/articlelist/44)
