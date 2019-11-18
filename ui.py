from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as msg
import os

from encoding import Passport

class App:
    def __init__(self, master):
        self.master = master
        self.passport = Passport()
        self.initWidgets()
        self.passwd_list = []
        # TODO: 暂时使用一下方案来处理已存在bmp文件的情况
        for roots, dirs, files in os.walk(os.curdir):
            for file in files:
                if file[-3:] == 'bmp':
                    self.passport.select_pic(file)

    def initWidgets(self):
        self.btn_get_pic = Button(self.master, text='选择passport图像', command=self.open_file)
        self.btn_encode = Button(self.master, text='加密', command=self.encode)
        self.btn_decode = Button(self.master, text='解密', command=self.decode)
        self.btn_add = Button(self.master, text='添加账户', command=self.add)

        self.btn_get_pic.grid(row=0, column=0)
        self.btn_encode.grid(row=0, column=1)
        self.btn_decode.grid(row=0, column=2)
        self.btn_add.grid(row=0, column=3)

        Label(self.master, text="站点").grid(row=1, column=0)
        Label(self.master, text="账号").grid(row=1, column=1)
        Label(self.master, text="密码").grid(row=1, column=2)

        self.account_box = []
        self.rows = 2

    def open_file(self):
        self.file_path = filedialog.askopenfilename()
        self.passport.select_pic(self.file_path)

    def encode(self):
        for account_info in self.account_box:
            info_net = account_info[0].get()
            info_account = account_info[1].get()
            info_passwd = account_info[2].get()

            self.passwd_list.append((info_net, info_account, info_passwd))

        self.passport.create_pass(self.passwd_list)
        print('加密完成')

    def decode(self):
        #TODO: 如果在一次运行中，重复加密解密加密的操作，存在冗余。
        accounts = self.passport.decode_pass()
        rows = 2
        for account in accounts:
            e_1 = Entry(self.master)
            e_2 = Entry(self.master, width=50)
            e_3 = Entry(self.master, width=50)
            btn_4 = Button(self.master, text="删除项目", command=self.delete)

            e_1.grid(row=rows, column=0)
            e_2.grid(row=rows, column=1)
            e_3.grid(row=rows, column=2)
            btn_4.grid(row=rows, column=3)

            e_1.insert(0, account[0])
            e_2.insert(0, account[1])
            e_3.insert(0, account[2])

            self.account_box.append((e_1, e_2, e_3, btn_4))
            rows += 1

        self.rows = rows



    def add(self):
        e_1 = Entry(self.master)
        e_2 = Entry(self.master, width=50)
        e_3 = Entry(self.master, width=50)
        btn_4 = Button(self.master, text="删除项目", command=self.delete)

        e_1.grid(row=self.rows, column=0)
        e_2.grid(row=self.rows, column=1)
        e_3.grid(row=self.rows, column=2)
        btn_4.grid(row=self.rows, column=3)

        self.account_box.append((e_1, e_2, e_3, btn_4))
        self.rows += 1

    def delete(self):
        #TODO:tkinter如何获取是谁触发了事件？？
        msg.askyesnocancel('暂时不提供删除功能')

root = Tk()
root.title('SafeBox')
App(root)
root.mainloop()
