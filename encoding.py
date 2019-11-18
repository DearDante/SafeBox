import cv2
import numpy as np
import os

class Passport(object):
    '''TODO:1. 目前只支持一种模式，在文件夹下仅能存在一个passport
    '''
    def __init__(self):
        pass

    def select_pic(self, pic_name):
        self.passport = cv2.imread(pic_name)
        if len(self.passport.shape) > 2:  #RGB图需要转成灰度图
            self.passport = cv2.cvtColor(self.passport, cv2.COLOR_RGB2GRAY)
        self.rows, self.cols = self.passport.shape
        self.length = min(self.rows, self.cols)
        if self.cols < 500:
            print('请选择宽大于500像素的图片')

    def create_pass(self, passwd_list):
        if len(passwd_list) > self.rows:
            print('需要更大的图片来保存更多的密码')
        info = ''
        for row in range(len(passwd_list)):
            net = passwd_list[row][0]
            account = passwd_list[row][1]
            passwd = passwd_list[row][2]
            ascii = np.fromstring(passwd, dtype = np.uint8)
            inser_index = self.pass_index(len(passwd))
            self.passport[row][0] = len(passwd)
            for count in range(len(passwd)):
                self.passport[row][inser_index[count]] = ascii[count]
            info += net + ',' + account + ','
        #依次保存站点，账号
        with open('accounts', 'w') as f1:
            f1.write(info)
        #bmp不会压缩图片，灰度值不会变化
        #如果存在bmp文件，则先删除原有的bmp文件
        for roots, dirs, files in os.walk(os.curdir):
            for file in files:
                if file[-3:] == 'bmp':
                    os.remove(file)
        cv2.imwrite('passport_{0}.bmp'.format(len(passwd_list)), self.passport)

    def decode_pass(self):
        #搜索是否存在passport开头的图片
        pass_file = ''
        for roots, dirs, files in os.walk(os.curdir):
            for file in files:
                if file[-3:] == 'bmp': pass_file = file
        if pass_file == '': print('未生成passport')
        else:
            with open('accounts', 'r') as f1:
                info = f1.read()
            info_list = info.split(',')
            info_list.pop(-1)
            net = []
            account = []
            for i in range(0, len(info_list), 2):
                net.append(info_list[i])
                account.append(info_list[i+1])
            passport = cv2.imread(pass_file, 0)
            passwords = []
            rows = int(pass_file.split('_')[-1].split('.')[0])
            for row in range(rows):
                pass_len = int(passport[row][0])
                pass_index_list = self.pass_index(pass_len)
                password_ascii = []
                for col in pass_index_list:
                    password_ascii.append(passport[row][col])
                password = ''.join(map(chr, password_ascii))
                passwords.append((net[row], account[row], password))
        return passwords

    def Fibonacci(self, n):
        if n == 1: return 0
        elif n == 2: return 1
        else: return self.Fibonacci(n-2) + self.Fibonacci(n-1)

    def pass_index(self, pass_num):
        pass_index_list = []
        for i in range(pass_num):
            if i < 10:
                pass_index = self.Fibonacci(i+4)
            else:
                int_part = i // 9
                dot_part = i % 9
                f_n = dot_part + 3
                pass_index = int_part * 144 +self.Fibonacci(f_n)
            pass_index_list.append(pass_index)
        return pass_index_list

if '__name__' == '__main__':
    p = Passport()
    p.select_pic(r'pass.jpg')
    pass_list = [('net', 'asdasd', '831143'),
                 ('web', 'qweqwe', '831143hSt0823'),
                 ('qq', 'zxczxc', '831143qkgmcVtf2'),
                 ('oh', 'fghfgh', '123123')]
    p.create_pass(pass_list)
    print(p.decode_pass())