#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2023/12/28 0:16
@File  : flet_ui.py
'''

# import glob, os

# 设计UI界面全盘搜索文件或者文件夹，使用glob
# class GUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title('查找小工具')
#         # 窗口设置为自适应
#         self.root.columnconfigure(0, weight=1)
#         self.root.rowconfigure(0, weight=1)
#
# drivers = [i.replace(' ', '').replace('\n', '') for i in os.popen('wmic logicaldisk get deviceid |findstr :').readlines() if i.replace(' ', '').replace('\n', '') != '']
# print(drivers)
# for d in drivers:
#     print(glob.glob(d+'**\\xiaobai.dbc**', recursive=True))