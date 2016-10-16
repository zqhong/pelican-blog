Title: Persistent rehash
Date: 2016-10-16 16:59
Category: 随笔
Tags: 随笔
Slug: rehash
Author: zqhong

# Persistent rehash
Typically, compinit will not automatically find new executables in the $PATH.Thus, to have these new exectuables included, one would run:
```
$ rehash
```

This 'rehash' can be set to happen automatically. Simply include the following in your zshrc:
```
~/.zshrc
```

zstyle ':completion:*' rehash true
Note: This hack has been found in a PR for Oh My Zsh

https://wiki.archlinux.org/index.php/zsh#Persistent_rehash