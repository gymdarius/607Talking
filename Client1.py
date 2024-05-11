from LoginPanel import LoginPanel
from MainPanel import MainPanel
from RegisterPanel import RegisterPanel
import tkinter as tk
from tkinter import messagebox, Toplevel, Button, Label, Entry
from threading import Thread
import time
import re
import math
import socket
import configparser
import pyaudio
import os
import random

phone_flag = 1
phone_set = 0


class Client:
    def __init__(self):
        global phone_flag
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while 1:
            try:
                self.target_ip = '8.139.254.59'
                self.target_port = 9808

                self.s.connect((self.target_ip, self.target_port))

                break
            except:
                print("Couldn't connect to server")

        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        print("Connected to Server")

        # start threads
        receive_thread = Thread(target=self.receive_server_data).start()
        self.send_data_to_server()

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass

    def send_data_to_server(self):
        global phone_flag
        while True:
            try:
                if phone_flag == 1:
                    data = self.recording_stream.read(1024)
                    print(phone_flag)
                    self.s.sendall(data)
            # elif phone_flag == 0:
            # 发送白噪声数据
            # print("noise")
            # noise_data = bytes([random.randint(0, 255) for _ in range(1024)])
            # self.s.sendall(noise_data)
            except:
                pass


class ChatClient:

    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read("userdata\\config.ini")
        secs = cf.sections()
        opts = cf.options("sec_a")
        items = cf.items("sec_a")
        val = cf.get("sec_a", "server_ip")

        self.sk = socket.socket()
        self.file_sk = socket.socket()
        self.sk.connect((val, 8080))
        self.file_sk.connect((val, 8081))
        # self.sk.connect(('10.132.3.123', 8080))

    # 验证登录
    def check_user(self, user, key):
        # 请求类型
        self.sk.sendall(bytes("1", "utf-8"))
        # 依次发送用户名密码
        self.send_string_with_length(user)
        self.send_string_with_length(key)
        # 获取服务器的返回值，"1"代表通过，“0”代表不通过
        check_result = self.recv_string_by_length(1)
        return check_result

    # 注册
    def register_user(self, user, key):
        # 请求类型
        self.sk.sendall(bytes("2", "utf-8"))
        # 依次发送用户名密码
        self.send_string_with_length(user)
        self.send_string_with_length(key)
        # 获取服务器的返回值，"0"代表通过，“1”代表已有用户名, "2"代表其他错误
        return self.recv_string_by_length(1)

    # 发送消息
    def send_message(self, message):
        self.sk.sendall(bytes("3", "utf-8"))
        self.send_string_with_length(message)

    # 发送私聊
    def send_private(self, message):
        self.sk.sendall(bytes("5", "utf-8"))
        self.send_string_with_length(message)

    # 发送带长度的字符串
    def send_string_with_length(self, content):
        # 发送内容的长度
        self.sk.sendall(bytes(content, encoding='utf-8').__len__().to_bytes(4, byteorder='big'))
        # 发送内容
        self.sk.sendall(bytes(content, encoding='utf-8'))

    # 获取服务器传来的定长字符串
    def recv_string_by_length(self, len):
        return str(self.sk.recv(len), "utf-8")

    # 获取服务端传来的变长字符串，这种情况下服务器会先传一个长度值
    def recv_all_string(self):
        # 获取消息长度
        length = int.from_bytes(self.sk.recv(4), byteorder='big')
        b_size = 3 * 1024  # utf8编码中汉字占3字节，英文占1字节
        times = math.ceil(length / b_size)
        content = ''
        for i in range(times):
            if i == times - 1:
                seg_b = self.sk.recv(length % b_size)
            else:
                seg_b = self.sk.recv(b_size)
            content += str(seg_b, encoding='utf-8')
        return content

    def send_number(self, number):
        self.sk.sendall(int(number).to_bytes(4, byteorder='big'))

    def recv_number(self):
        return int.from_bytes(self.sk.recv(4), byteorder='big')

    def send_file_to_server(self, file_path):
        self.file_sk.sendall(bytes("6", "utf-8"))
        # 获取文件名
        file_name = os.path.basename(file_path)
        # 发送文件名
        self.file_sk.sendall(file_name.encode('utf-8'))

        time.sleep(0.5)
        # 获取文件大小
        file_size = os.path.getsize(file_path)
        self.file_sk.sendall(str(file_size).encode('utf-8'))

        time.sleep(0.5)
        # 询问服务器已经接收了多少数据
        self.file_sk.sendall(b"received_size?")
        received_size = int(self.file_sk.recv(1024).decode())
        print(received_size)
        # 打开文件以读取
        with open(file_path, "rb") as file:
            file.seek(received_size)
            # 发送文件内容
            while True:
                data = file.read(1024)  # 以1024大小不断读取
                if len(data) != 0:
                    print(data)
                else:
                    print("send null")
                    break
                self.file_sk.sendall(data)

        # 接收服务器确认消息
        response = self.file_sk.recv(1024)
        print(f"Server response: {response.decode('utf-8')}")

    # 客户端函数，用于从服务器下载文件
    def download_file_from_server(self, file_name):
        self.file_sk.sendall(bytes("7", "utf-8"))
        # 发送文件名
        self.file_sk.sendall(file_name.encode('utf-8'))
        # 读走报文头
        # head = self.file_sk.recv(1024).decode('utf-8')
        # 接收文件内容长度
        file_size_str = self.file_sk.recv(1024).decode('utf-8')
        file_size = int(file_size_str)
        print(file_size)
        # 文件路径
        file_path = f"client_file\\{file_name}"
        print(file_path)

        # 检查文件是否已存在，如果存在则告诉服务端已接收的数据大小
        if os.path.exists(file_path):
            received_size = os.path.getsize(file_path)
            self.file_sk.sendall(str(received_size).encode('utf-8'))
            print(received_size)
        else:
            received_size = 0
            self.file_sk.sendall(str(received_size).encode('utf-8'))
            print(received_size)

        # 检查文件是否存在
        if os.path.exists(file_path):
            print("File already exist")

        # 保存文件
        with open(file_path, "ab") as file:
            while received_size < file_size:
                data = self.file_sk.recv(1024)
                print(data)
                file.write(data)
                received_size += len(data)
                print(received_size)
            print("get out")
            # self.file_sk.settimeout(5.0)
            # data = self.file_sk.recv(1024*1024*100)
            # file.write(data)

        # 接收服务器确认消息
        '''
        confirmation_msg = self.file_sk.recv(1024).decode('utf-8')
        if confirmation_msg == "File sent":
            print(f"File {file_name} downloaded")
        else:
            print("Error in file transfer")
        print(f"File {file_name} downloaded")
        '''


def send_message():
    print("send message:")
    content = main_frame.get_send_text()
    if content == "" or content == "\n":
        print("empty message")
        return
    print(content)
    # 清空输入框
    main_frame.clear_send_text()
    flag = "#!"
    if (flag in content):
        client.send_private(content)
    else:
        client.send_message(content)


# def close_sk():
#     client.sk.close()

def close_main_window():
    client.sk.close()
    main_frame.main_frame.destroy()


def send_file_to_server():
    # 创建一个对话框
    input_window = Toplevel()
    input_window.title("输入文件名")
    input_window.geometry("300x100+500+200")

    # 创建一个标签
    label = Label(input_window, text="文件名:")
    label.pack()

    # 创建一个输入框
    entry = Entry(input_window)
    entry.pack()

    # 创建一个完成按钮，当点击时会关闭输入窗口并保存输入的文件路径
    def on_complete():
        global file_path  # 声明file_path为全局变量
        file_name = entry.get()  # 获取输入的文件路径
        file_path = f"client_file\\{file_name}"
        input_window.destroy()  # 关闭输入窗口
        # 调用发送文件的函数
        client.send_file_to_server(file_path)

    complete_button = Button(input_window, text="完成", command=on_complete)
    complete_button.pack()

    # 启动GUI的事件循环
    input_window.mainloop()


def download_file_from_server():
    # 创建一个对话框
    input_window = Toplevel()
    input_window.title("输入文件名")
    input_window.geometry("300x100+500+200")

    # 创建一个标签
    label = Label(input_window, text="请输入要下载的文件名:")
    label.pack()

    # 创建一个输入框
    entry = Entry(input_window)
    entry.pack()

    # 创建一个完成按钮，当点击时会关闭输入窗口并保存输入的文件名
    def on_complete():
        global file_name  # 声明file_name为全局变量
        file_name = entry.get()  # 获取输入的文件名
        input_window.destroy()  # 关闭输入窗口
        # 调用下载文件的函数
        client.download_file_from_server(file_name)

    complete_button = Button(input_window, text="完成", command=on_complete)
    complete_button.pack()

    # 启动GUI的事件循环
    input_window.mainloop()


def close_login_window():
    client.sk.close()
    login_frame.login_frame.destroy()


# 关闭注册界面并打开登陆界面
def close_reg_window():
    reg_frame.close()
    login_frame.show()


# 关闭登陆界面前往主界面
def goto_main_frame(user):
    login_frame.close()
    global main_frame
    main_frame = MainPanel(user, send_message, close_main_window, start_phone, send_file_to_server,
                           download_file_from_server, end_phone)
    # 新开一个线程专门负责接收并处理数据
    Thread(target=recv_data).start()
    main_frame.show()


def my_function():
    Client()


my_thread = Thread(target=my_function)


def start_phone():
    my_thread.start()


def start_phone():
    global phone_flag
    global phone_set
    if phone_set == 0:
        phone_set = 1
        my_thread.start()
    elif phone_set == 1:
        phone_flag = 1


def end_phone():
    global phone_flag
    phone_flag = 0
    print("now phone_flag = ")
    print(phone_flag)


def login():
    user, key = login_frame.get_input()

    if user == "" or key == "":
        messagebox.showwarning(title="提示", message="用户名或者密码为空")
        return
    print("user: " + user + ", key: " + key)
    if client.check_user(user, key) == '1':
        # 验证成功
        goto_main_frame(user)
    elif client.check_user(user, key) == '0':
        # 验证失败
        messagebox.showerror(title="错误", message="用户名或者密码错误")
    elif client.check_user(user, key) == '2':
        messagebox.showerror(title="错误", message="该用户已经登录")


# 登陆界面前往注册界面
def register():
    login_frame.close()
    global reg_frame
    reg_frame = RegisterPanel(close_reg_window, register_submit, close_reg_window)
    reg_frame.show()


# 提交注册表单
def register_submit():
    user, key, confirm = reg_frame.get_input()
    if user == "" or key == "" or confirm == "":
        messagebox.showwarning("错误", "请完成注册表单")
        return
    if not key == confirm:
        messagebox.showwarning("错误", "两次密码输入不一致")
        return

    # 发送注册请求
    result = client.register_user(user, key)
    if result == "0":
        # 注册成功，跳往登陆界面
        messagebox.showinfo("成功", "注册成功")
        close_reg_window()
    elif result == "1":
        # 用户名重复
        messagebox.showerror("错误", "该用户名已被注册")
    elif result == "2":
        # 未知错误
        messagebox.showerror("错误", "发生未知错误")
    elif result == "3":
        # 密码不符合要求
        messagebox.showerror("错误", "密码必须包含大写字母、小写字母、数字并且长度>=8")


# 处理消息接收的线程方法
def recv_data():
    # 暂停几秒，等主界面渲染完毕
    time.sleep(1)
    while True:
        try:
            # 首先获取数据类型
            message_type = client.recv_all_string()
            print("recv type: " + message_type)
            if message_type == "#!onlinelist#!":
                # 获取在线列表数据
                online_list = list()
                for n in range(client.recv_number()):
                    online_list.append(client.recv_all_string())
                main_frame.refresh_friends(online_list)
                print(online_list)
            elif message_type == "#!message#!":
                # 获取新消息
                user = client.recv_all_string()
                print("user: " + user)
                content = client.recv_all_string()
                print("message: " + content)
                main_frame.recv_message(user, content)
        except Exception as e:
            print("server error occurred:" + str(e))
            break


def start():
    global client
    client = ChatClient()
    global login_frame
    login_frame = LoginPanel(login, register, close_login_window)
    global main_frame
    global reg_frame

    login_frame.show()


if __name__ == "__main__":
    start()