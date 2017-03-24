import sys
import os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'D:\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'D:\Python\Python36-32\tcl\tk8.6'

base = None
# 判断Windows系统
if sys.platform == 'win32':
    base = 'Win32GUI'
elif sys.platform == 'win64':
    base = 'Win64GUI'

packages = []

for dbmodule in ['cx_Freeze', 'tkinter']:

    try:

        __import__(dbmodule)

    except ImportError:

        pass

    else:
        packages.append(dbmodule)

include_files = ['./resources/tcl86t.dll', './resources/tk86t.dll', './keystore', './resources', './fast_apktool.py']
options = {
    'build_exe':
        {
            # 依赖的包
            "packages": packages
            # 额外添加的文件
            , 'include_files': include_files
        }

}

executables = [
    Executable(
        # 工程的 入口
        'index.py'
        , base=base
        # 生成 的文件 名字
        , targetName='APKTool.exe'
        # 生成的EXE的图标
        , icon="./resources/droid.ico" #图标, 32*32px
    )
]

setup(
    # 产品名称
    name='APKTool',
    # 版本号
    version='1.0',
    # 产品说明
    description='APKTool',
    options=options,
    executables=executables
)
