# -*- coding: utf-8 -*-

"""
生成新文章模板
"""

import argparse
import os
import time


class TemplateGenerator:
    def __init__(self):
        """
        初始化
        """
        self.args = ''
        self.dir = 'content'
        self.template = """Title: Your_Title
Date: {date}
Category: category1
Tags: tag1
Slug: {slug}
Author: {author}
"""

    def parse_args(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('-f', '--filename', help='New file you want to write', type=str)
        arg_parser.add_argument('-a', '--author', help='the article author', default='zqhong', type=str)
        self.args = arg_parser.parse_args()

        if self.args.filename is None:
            arg_parser.print_help()
            exit()

    def make_file(self):
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
        file_path = self.dir + '/' + self.args.filename + '.md'
        return file_path

    def run(self):
        self.parse_args()
        file_path = self.make_file()
        today = time.strftime("%Y-%m-%d %H:%M")
        content = self.template.format(date=today, slug=self.args.filename, author=self.args.author)
        with open(file_path, 'w') as fw:
            fw.write(content)


if __name__ == '__main__':
    tg = TemplateGenerator()
    tg.run()
