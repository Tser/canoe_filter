#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2023/12/28 0:16
@File  : flet_ui.py
'''

# print(hex(int('0x1234', 16)))
# import re
#
# source = '00 00 00aa 00 00 0 '.strip().upper().replace(' ', '')
#
# # 不够偶数补齐
# if len(source) % 2: source += '0'
#
# pattern = re.compile(r'[\dA-F]+')
#
# r = re.match(pattern, source).group()
#
# print(' '.join([r[i:i+2] for i in range(0, len(r), 2)]))

from tkinter import messagebox




r = messagebox.askokcancel('提示:', '数据格式不正确，是否重置')
print(r)