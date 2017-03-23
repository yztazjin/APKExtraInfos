from tkinter.filedialog import *
from tkinter import messagebox
import tkinter.ttk
import os
import fast_apktool
import sys
import threading

sys.path.append(os.path.dirname(__file__))


class APKToolIndex(LabelFrame):
    def __init__(self):
        self.root = Tk()
        icon_path = os.path.dirname(__file__) + '/resources/droid.ico'
        self.root.iconbitmap(icon_path)
        self.parentWidth = 500
        self.parentHeight = 350
        self.parentCenterX = int(self.root.winfo_screenwidth() / 2 - self.parentWidth / 2)
        self.parentCenterY = int(self.root.winfo_screenheight() / 2 - self.parentHeight / 2)
        self.root.configure(bg='white')
        self.root.title('APKTool By Hjq')
        self.root.maxsize(self.parentWidth, self.parentHeight)
        self.root.minsize(self.parentWidth, self.parentHeight)
        self.root.geometry(
            "{width}x{height}+{x}+{y}".format(width=self.parentWidth, height=self.parentHeight, x=self.parentCenterX,
                                              y=self.parentCenterY))

        LabelFrame.__init__(self, self.root, width=self.parentWidth, height=self.parentHeight)
        self.page = self
        self.page.pack(expand=True, fill=BOTH)
        self.configure(borderwidth=0,
                       bg='#ffffff')

        APKToolIndex.__ui_add_components(self)

    def show(self):
        self.root.mainloop()

    def __ui_add_components(self):
        line_y = 5
        line_x = 15

        entry_style = tkinter.ttk.Style()
        entry_style.configure("TEntry", foreground="black", background="#eee")

        # 源APK目录
        self.label_source_apk = Label(self, text='源APK路径', bg='#ffffff')
        self.label_source_apk.place(x=line_x, y=5)
        line_y += self.label_source_apk.winfo_reqheight()

        self.entry_source_apk_strvar = StringVar()
        self.entry_source_apk_strvar.set('请选择要签名的APK')
        self.entry_source_apk = tkinter.ttk.Entry(self, textvariable=self.entry_source_apk_strvar, style='TEntry')
        self.entry_source_apk.place(x=line_x, y=line_y + 10, relwidth=0.7, height=30)

        self.entry_source_apk_btn = tkinter.ttk.Button(self, text='选择文件', command=self.__select_source_apk)
        self.entry_source_apk_btn.place(relx=0.77, y=line_y + 8, relwidth=0.18, height=30)

        line_y += 30

        # 生成文件目录
        self.label_result_apk = Label(self, text='生成APK目录', bg='#fff')
        self.label_result_apk.place(x=line_x, y=line_y + 20)
        line_y += 40

        self.entry_rst_apk_strvar = StringVar()
        self.entry_rst_apk_strvar.set('请选择要生成的APK的目录')
        self.entry_rst_apk = tkinter.ttk.Entry(self, textvariable=self.entry_rst_apk_strvar, style="TEntry")
        self.entry_rst_apk.place(x=line_x, y=line_y + 10, relwidth=0.7, height=30)

        self.entry_rst_apk_btn = tkinter.ttk.Button(self, text='选择目录', command=self.__select_result_apk)
        self.entry_rst_apk_btn.place(relx=0.77, y=line_y + 8, relwidth=0.18, height=30)

        line_y += 60
        # Key1
        self.label_key_1 = Label(self, text='ip', bg='#eee')
        self.label_key_1.place(x=line_x, y=line_y, width=80, height=30)

        self.entry_key_1_strvar = StringVar(value='192.168.2.159')
        self.entry_key_1 = tkinter.ttk.Entry(self, textvariable=self.entry_key_1_strvar, style='TEntry')
        self.entry_key_1.place(x=line_x + 100, y=line_y, width=360, height=30)
        # Key2
        line_y += 40
        self.label_key_2 = Label(self, text='port', bg='#eee')
        self.label_key_2.place(x=line_x, y=line_y, width=80, height=30)

        self.entry_key_2_strvar = StringVar(value='1851')
        self.entry_key_2 = tkinter.ttk.Entry(self, textvariable=self.entry_key_2_strvar, style='TEntry')
        self.entry_key_2.place(x=line_x + 100, y=line_y, width=360, height=30)
        # Key3
        line_y += 40
        self.label_key_3 = Label(self, text='channel', bg='#eee')
        self.label_key_3.place(x=line_x, y=line_y, width=80, height=30)

        self.entry_key_3_strvar = StringVar(value='official')
        self.entry_key_3 = tkinter.ttk.Entry(self, textvariable=self.entry_key_3_strvar, style='TEntry',
                                             state='readonly')
        self.entry_key_3.place(x=line_x + 100, y=line_y, width=360, height=30)

        # Button To Generate
        line_y += 60
        self.btn_generate = tkinter.ttk.Button(self, text='Generate', command=self.__to_generate)
        self.btn_generate.place(x=50, y=line_y, width=400, height=30)
        pass

    def __select_source_apk(self):
        source_apk_path = askopenfilename()

        if not source_apk_path:
            return

        if not str(source_apk_path).endswith('apk'):
            messagebox.showerror('提示', '请选择APK类型的文件', parent=self.root)
            return

        if fast_apktool.is_sourceapk_signed(source_apk_path):
            messagebox.showerror('提示', '请选择没有签名过的APK文件', parent=self.root)
            return

        self.source_apk_path = source_apk_path
        self.entry_source_apk_strvar.set(self.source_apk_path)

    def __select_result_apk(self):
        result_apk_dir = askdirectory()

        if not result_apk_dir:
            return

        self.result_apk_dir = result_apk_dir
        self.entry_rst_apk_strvar.set(self.result_apk_dir)

    def __to_generate(self):

        # 判断源APK文件
        if not hasattr(self, 'entry_source_apk_path') \
                or not self.source_apk_path \
                or self.source_apk_path == '请选择要签名的APK':
            self.source_apk_path = self.entry_source_apk_strvar.get()
            if not self.source_apk_path or self.source_apk_path == '请选择要签名的APK':
                messagebox.showerror('提示', '请选择APK类型的文件', parent=self.root)
                return

        # 判断生成APK目录
        if not hasattr(self, 'result_apk_dir') \
                or not self.result_apk_dir \
                or self.result_apk_dir == '请选择要生成的APK的目录':
            self.result_apk_dir = self.entry_rst_apk_strvar.get()
            if not self.result_apk_dir or self.entry_rst_apk == '请选择要生成的APK的目录':
                messagebox.showerror('提示', '请选择要生成的APK的目录', parent=self.root)
                return

        # 获取key ip, key port, key channel
        args = {
            '-ip': '192.168.1.10',
            '-port': 1851,
            '-channel': 'official'
        }
        ip = self.entry_key_1_strvar.get()
        port = self.entry_key_2_strvar.get()
        channel = self.entry_key_3_strvar.get()
        if ip:
            args['-ip'] = ip
        if port:
            try:
                args['-port'] = int(port)
            except ValueError as e:
                messagebox.showerror('提示', "Port必须为整型")
                return
        if channel:
            args['-channel'] = str(channel)
        # 获取keystore
        keystore_config = dict()
        # keystore 路径
        keystore_config['keystore_path'] = os.path.dirname(os.path.abspath(__file__)) + '/keystore/jdwb.jks'
        # keystore password
        keystore_config['keystore_pwd'] = '123456'
        # keystore alias
        keystore_config['alias'] = 'jdwb'
        # keysotre alias password
        keystore_config['alias_pwd'] = '123456'

        self.btn_generate.configure(text='Generating...')
        threading.Thread(target=self.__generate_core, args=(self.source_apk_path, self.result_apk_dir, args, keystore_config)).start()

    def __generate_core(self, source_apk_path, result_apk_dir, args, keystore_config):
        rst = fast_apktool.write_apk_extra_info(source_apk_path, result_apk_dir, args)
        fast_apktool.sign_handled_apk(keystore_config, rst)

        self.btn_generate.configure(text='Generate')
        messagebox.showinfo('提示', '生成成功\n{path}'.format(path=rst), parent=self.root)

if __name__ == '__main__':
    page = APKToolIndex()
    page.show()
