:: 删除编译文件
rmdir /S /Q build dist canoe_filter.egg-info

:: 编译源文件
python setup.py sdist bdist_wheel

:: 上传编译的文件(cmd下运行)
:: python -m twine upload dist/*