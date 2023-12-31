#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2023/12/28 0:06
@File  : setup.py
'''

from setuptools import setup, find_packages
from canoe_filter.__version__ import __version__

f = open('README.md', 'r', encoding='utf-8')

setup(
    # 指定项目名称，我们在后期打包时，这就是打包的包名称，当然打包时的名称可能还会包含下面的版本号哟~
    name='canoe_filter',
    # 指定版本号
    version=__version__,
    # 这是对当前项目的一个描述
    description="基于py_canoe实现的CANoe信号的过滤用于快速知道所需要的数据；参考的内存修改工具CE（Cheat Engine）的部分查找数据的功能"
    + "Python(>=3.9)"
    + "Vector CANoe software(>=v11)",
    long_description=f.read(),
    long_description_content_type="text/markdown",
    # 作者是谁，
    author='xiaobaiTser',
    # 作者的邮箱
    author_email='807447312@qq.com',
    # 写上项目的地址。
    url='https://github.com/Tser/canoe_filter',
    # 指定包名，即你需要打包的包名称，要实际在你本地存在哟，它会将指定包名下的所有"*.py"文件进行打包哟，但不会递归去拷贝所有的子包内容。
    # 综上所述，我们如果想要把一个包的所有"*.py"文件进行打包，应该在packages列表写下所有包的层级关系哟~这样就开源将指定包路径的所有".py"文件进行打包!
    keywords="canoe py_canoe",
    packages=find_packages(),
    include_package_data=True,
    # 指定Python的版本
    python_requires='>=3.9',
    install_requires=[
        'py_canoe',
    ],
    entry_points={
        'console_scripts': [
            'canoe_filter = canoe_filter.canoe_filter_ui:main'
        ]
    },
    data_files=[
        ('favicon', ['canoe_filter/favicon.ico']),
    ]
)

'''
#python setup.py sdist bdist_wheel
#python -m twine upload dist/*
'''