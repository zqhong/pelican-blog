Title: 在 Python 中使用 Protocol Buffer
Date: 2016-06-13 11:08
Category: Python, WEB
Tags: Python, Protocol Buffer
Slug: Protocol-Buffer-Basics-Python
Author: zqhong

# Protocol Buffer 简介
Protocol Buffer 是谷歌开发的一种数据描述语言，能够将结构化数据序列化，可用于数据存储、通讯协议等方面。可以把它理解为更快、更简单、更小的 JSON 或者 XML，区别在于Protocol Buffers是二进制格式，而JSON和XML是文本格式。

---

# 如何使用 Protocol Buffer
Protoco Buffer 目前有三种实现：C++、C#、Go、Java 和 Python。这里以 Python 为例，但大致的步骤是一样的。
* 在 `.proto` 文件中定义消息（message）
* 使用 protocol buffer compiler 将 `.proto` 文件生成其他语言能使用的代码
* 使用 API 去读写消息（message）


<!--more-->

## 一：定义消息（message）
```
# filename: addressbook.proto
# 声明包，避免冲突
package tutorial;

# 定义一个 Person 消息
message Person {
  # required 是字段约束，string 是字段类型，name 是字段名，1 是字段编号
  # required：必须赋值
  required string name = 1;
  required int32 id = 2;
  # optional：可选赋值，可为空。如果没有指定默认值，则会使用该类型的默认值。
  # 或者使用 [default = xxx] 指定默认值
  optional string email = 3;

  enum PhoneType {
    MOBILE = 0;
    HOME = 1;
    WORK = 2;
  }

  # 可以在 message 中嵌入另一个 message
  message PhoneNumber {
    required string number = 1;
    optional PhoneType type = 2 [default = HOME];
  }

  # repeated：集合字段，可以填充多个对象。
  repeated PhoneNumber phone = 4;
}

message AddressBook {
  repeated Person person = 1;
}
```

### 关于字段编号
每个消息中的字段都有一个字段编号。这些编号用于在二进制格式的 message 中识别出你的字段。因此，请别修改这些值。

> 备注：1-15 占用一个字节；16-2047 占用两个字节；为了减少二进制格式的 message 的大小，建议多使用 1-15 范围内的字段编号。
> 最小的字段编号为 1，最大的为 536,870,911。不能使用 19000-19999 这个范围内保留的字段编号。


## 二：生成代码
### 安装 `protobuf compiler`
在 debian/ubuntu/mint 系统中，直接使用 `sudo apt-get install protobuf-compiler` 安装。其他系统请参考：[Download Protocol Buffers](https://developers.google.com/protocol-buffers/docs/downloads)

### 开始生成代码
```
# 在当前目录下生成 Python 可用的代码
# 如果是其他语言，使用：--cpp_out（C++）、--java_out（Java）
protobuf --python_out=. addressbook.proto
```

## 使用 API 读写消息
两个重要的 API：SerializeToString 和 ParseFromString
* SerializeToString()：序列化 message，返回 string。
* ParseFromString(data)：从所给的 string 数据中解析 message

其他请参考 [API 文档 - google.protobuf.message.Message-class](https://developers.google.com/protocol-buffers/docs/reference/python/google.protobuf.message.Message-class)

### Writing a Message
```
# filename: add_person.py
#! /usr/bin/env python

# See README.txt for information and build instructions.

import addressbook_pb2
import sys

# This function fills in a Person message based on user input.
def PromptForAddress(person):
  person.id = int(raw_input("Enter person ID number: "))
  person.name = raw_input("Enter name: ")

  email = raw_input("Enter email address (blank for none): ")
  if email != "":
    person.email = email

  while True:
    number = raw_input("Enter a phone number (or leave blank to finish): ")
    if number == "":
      break

    phone_number = person.phones.add()
    phone_number.number = number

    type = raw_input("Is this a mobile, home, or work phone? ")
    if type == "mobile":
      phone_number.type = addressbook_pb2.Person.MOBILE
    elif type == "home":
      phone_number.type = addressbook_pb2.Person.HOME
    elif type == "work":
      phone_number.type = addressbook_pb2.Person.WORK
    else:
      print "Unknown phone type; leaving as default value."

# Main procedure:  Reads the entire address book from a file,
#   adds one person based on user input, then writes it back out to the same
#   file.
if len(sys.argv) != 2:
  print "Usage:", sys.argv[0], "ADDRESS_BOOK_FILE"
  sys.exit(-1)

address_book = addressbook_pb2.AddressBook()

# Read the existing address book.
try:
  with open(sys.argv[1], "rb") as f:
    address_book.ParseFromString(f.read())
except IOError:
  print sys.argv[1] + ": File not found.  Creating a new file."

# Add an address.
PromptForAddress(address_book.people.add())

# Write the new address book back to disk.
with open(sys.argv[1], "wb") as f:
  f.write(address_book.SerializeToString())

```

### Reading a Message
```
# filename: list_people.py
#! /usr/bin/env python

# See README.txt for information and build instructions.

import addressbook_pb2
import sys

# Iterates though all people in the AddressBook and prints info about them.
def ListPeople(address_book):
  for person in address_book.people:
    print "Person ID:", person.id
    print "  Name:", person.name
    if person.email != "":
      print "  E-mail address:", person.email

    for phone_number in person.phones:
      if phone_number.type == addressbook_pb2.Person.MOBILE:
        print "  Mobile phone #:",
      elif phone_number.type == addressbook_pb2.Person.HOME:
        print "  Home phone #:",
      elif phone_number.type == addressbook_pb2.Person.WORK:
        print "  Work phone #:",
      print phone_number.number

# Main procedure:  Reads the entire address book from a file and prints all
#   the information inside.
if len(sys.argv) != 2:
  print "Usage:", sys.argv[0], "ADDRESS_BOOK_FILE"
  sys.exit(-1)

address_book = addressbook_pb2.AddressBook()

# Read the existing address book.
with open(sys.argv[1], "rb") as f:
  address_book.ParseFromString(f.read())

ListPeople(address_book)

```

---

# 相关资料
[Protocol Buffer Basics: Python](https://developers.google.com/protocol-buffers/docs/pythontutorial)
[在Python中使用protocol buffers参考指南(译)](http://blog.csdn.net/losophy/article/details/17006573)
[Protocol Buffer - Language Guide](https://developers.google.com/protocol-buffers/docs/proto)
[Protocol Buffers序列化协议及应用](https://worktile.com/tech/share/prototol-buffers)
