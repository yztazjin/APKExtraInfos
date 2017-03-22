from tkinter.filedialog import *
from tkinter import messagebox
import os
import fast_apktool


class APKToolIndex(LabelFrame):

    def __init__(self):
        self.root = Tk()
        icon_path = os.path.dirname(__file__) + '/resources/droid.ico'
        self.root.iconbitmap(icon_path)
        self.parentWidth = 400
        self.parentHeight = 520
        self.parentCenterX = int(self.root.winfo_screenwidth()/2 - self.parentWidth/2)
        self.parentCenterY = int(self.root.winfo_screenheight()/2 - self.parentHeight/2)
        self.root.configure(bg='white')
        self.root.title('APKTool By Hjq')
        self.root.maxsize(self.parentWidth, self.parentHeight)
        self.root.minsize(self.parentWidth, self.parentHeight)
        self.root.geometry("{width}x{height}+{x}+{y}".format(width=self.parentWidth, height=self.parentHeight, x=self.parentCenterX, y=self.parentCenterY))

        LabelFrame.__init__(self, self.root, width=self.parentWidth, height=self.parentHeight)
        self.page = self
        self.page.pack(expand=True, fill=BOTH)
        self.configure(borderwidth=0,
                       bg='#ffffff')

        APKToolIndex.__ui_add_components(self)

    def show(self):
        self.root.mainloop()

    def __ui_add_components(self):
        line_y = 0
        line_x = 15

        self.label_source_apk = Label(self, text='源APK路径', bg='#ffffff')
        self.label_source_apk.place(x=line_x, y=5)
        line_y += self.label_source_apk.winfo_reqheight()

        self.entry_source_apk_strvar = StringVar()
        self.entry_source_apk_strvar.set('请选择要签名的APK')
        self.entry_source_apk = Entry(self, textvariable=self.entry_source_apk_strvar)
        self.entry_source_apk.place(x=line_x, y=line_y+10, relwidth=0.6, height=30)

        self.entry_source_apk_btn = Button(self, text='选择文件', command=self.__select_source_apk)
        self.entry_source_apk_btn.place(relx=0.67, y=line_y+10, relwidth=0.28, height=30)

        pass

    def __select_source_apk(self):
        source_apk_path = askopenfilename()

        if not str(source_apk_path).endswith('apk'):
            messagebox.showerror('提示', '请选择APK类型的文件', parent=self.root)

        if fast_apktool.is_sourceapk_signed(source_apk_path):
            messagebox.showerror('提示', '请选择没有签名过的APK文件', parent=self.root)

        self.entry_source_apk_path = source_apk_path
        self.entry_source_apk_strvar.set(self.source_apk_path)

if __name__ == '__main__':
    page = APKToolIndex()
    page.show()
