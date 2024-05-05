from tkinter import *
import time
import datetime


# 主界面类
class MainPanel:

    def on_return_key(self, event):
        # 调用发送消息的函数
        self.send_func()
        # 阻止默认的换行行为
        return 'break'

    def on_escape_key(self, event):
        # 调用清空输入框的函数
        self.clear_send_text()
        # 阻止默认的ESC键行为
        return 'break'

    def __init__(self, username, send_func, close_callback,start_phone, upload_file, download_file):
        self.username = username
        self.friend_list = None
        self.message_text = None
        self.send_text = None
        self.send_func = send_func
        self.close_callback = close_callback
        self.main_frame = None
        self.start_phone = start_phone
        self.upload_file = upload_file
        self.download_file = download_file

    def show(self):
        global main_frame
        main_frame = Tk()
        main_frame.title("607Talking")
        main_frame.configure(background="#f2f2f2")
        # 设置窗口关闭按钮回调，用于退出时关闭socket连接
        main_frame.protocol("WM_DELETE_WINDOW", self.close_callback)
        #设置窗口大小
        width = 900
        height = 600
        #获取屏幕尺寸
        screen_width = main_frame.winfo_screenwidth()
        screen_height = main_frame.winfo_screenheight()
        #设置窗口位置
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height -  height) / 2)
        main_frame.geometry(gm_str)
        # 设置最小尺寸,窗口不会被缩小
        main_frame.minsize(width, height)
        now = datetime.datetime.now()
        if 5 <= now.hour < 12:
            greet= "早上好 "
        elif 12 <= now.hour < 18:
            greet= "中午好 "
        elif 18 <= now.hour < 21:
            greet= "下午好 "
        else:
            greet= "晚上好 "

        Label(main_frame, text=greet + self.username+"          输入 #!你想要私聊的人!# 加上消息内容就可以私聊哦 注意半角符号", font=("宋体", 13), bg="#f2f2f2",
              fg="#7A7AFF").grid(row=0, column=0, ipady=10, padx=10, columnspan=2, sticky=W)

        #展示好友列表，同时好友列表和消息列表均具有滚动条，以在消息或用户过多时全部显示
        friend_list_var = StringVar()
        self.friend_list = Listbox(main_frame, selectmode=NO, listvariable=friend_list_var,
                                   bg="white", fg="#003366", font=("黑体", 14), highlightcolor="#9933ff")
        self.friend_list.grid(row=1, column=0, rowspan=3, sticky=N + S, padx=10, pady=(0, 5))
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(1, weight=1)
        #用户滚动条
        sc_bar = Scrollbar(main_frame)
        sc_bar.grid(row=1, column=0, sticky=N + S + E, rowspan=3, pady=(0, 5))
        sc_bar['command'] = self.friend_list.yview
        self.friend_list['yscrollcommand'] = sc_bar.set
        #消息滚动条
        msg_sc_bar = Scrollbar(main_frame)
        msg_sc_bar.grid(row=1, column=1, sticky=E + N + S, padx=(0, 10))
        self.message_text = Text(main_frame, bg="white", height=1,
                                 highlightcolor="white", highlightthickness=1)
        
        # 显示消息的文本框不可编辑，当需要修改内容时再修改版为可以编辑模式 NORMAL
        self.message_text.config(state=DISABLED)
        #配置了两个标签，用于显示不同的消息
        self.message_text.tag_configure('greencolor', foreground='green')
        self.message_text.tag_configure('bluecolor', foreground='blue')
        #设置显示消息的文本框的位置
        self.message_text.grid(row=1, column=1, sticky=W + E + N + S, padx=(10, 30))
        #将消息滚动条与消息文本框绑定
        msg_sc_bar["command"] = self.message_text.yview
        self.message_text["yscrollcommand"] = msg_sc_bar.set
        #发送消息滚动条
        send_sc_bar = Scrollbar(main_frame)
        send_sc_bar.grid(row=2, column=1, sticky=E + N + S, padx=(0, 10), pady=10)
        #发送消息文本框
        self.send_text = Text(main_frame, bg="white", height=6, highlightcolor="white",
                              highlightbackground="#cc99ff", highlightthickness=3)
        # 绑定回车键
        self.send_text.bind('<Control-Return>', self.on_return_key)
        # 绑定ESC键
        self.send_text.bind('<Escape>', self.on_escape_key)
        #确保send_text文本框的内容始终显示最底部的文本
        self.send_text.see(END)
        #设置send_text文本框的位置
        self.send_text.grid(row=2, column=1, sticky=W + E + N + S, padx=(10, 30), pady=10)
        #将发送消息滚动条与发送消息文本框绑定
        send_sc_bar["command"] = self.send_text.yview
        self.send_text["yscrollcommand"] = send_sc_bar.set
        main_frame.columnconfigure(1, weight=1)
        Button(main_frame, text="发送(Ctrl+Enter)", bg="#4d88ff", font=("黑体", 14), fg="white", command=self.send_func,width=20) \
            .grid(row=4, column=1, pady=5, padx=10, sticky=W, ipady=3, ipadx=10)
        Button(main_frame, text="清空(Esc)", bg="#4d88ff", font=("黑体", 14), fg="white", command=self.clear_send_text,width=20) \
            .grid(row=4, column=1, pady=5, sticky=W, padx=(220, 0), ipady=3, ipadx=10)
        Button(main_frame, text="语音通话", bg="#4d88ff", font=("黑体", 14), fg="white", command=self.start_phone,width=20) \
            .grid(row=4, column=1, pady=5, sticky=W, padx=(420, 0), ipady=3, ipadx=10)
        Button(main_frame, text="上传文件", bg="#4d88ff", font=("黑体", 14), fg="white", command=self.upload_file) \
            .grid(row=3, column=1, pady=5, padx=(320, 0), sticky=W, ipady=3, ipadx=10)
        Button(main_frame, text="下载文件", bg="#4d88ff", font=("黑体", 14), fg="white", command=self.download_file) \
            .grid(row=3, column=1, pady=5, padx=(120, 0), sticky=W, ipady=3, ipadx=10)
        self.main_frame = main_frame
        main_frame.mainloop()

    # 刷新在线列表
    def refresh_friends(self, names):
        self.friend_list.delete(0, END)
        for name in names:
            self.friend_list.insert(0, name)

    # 接受到消息，在文本框中显示，自己的消息用绿色，别人的消息用蓝色
    def recv_message(self, user, content):
        self.message_text.config(state=NORMAL)
        title = user + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
        if user == self.username:
            self.message_text.insert(END, title, 'greencolor')
        else:
            self.message_text.insert(END, title, 'bluecolor')
        self.message_text.insert(END, content + "\n")
        self.message_text.config(state=DISABLED)
        # 滚动到最底部
        self.message_text.see(END)

    # 清空消息输入框
    def clear_send_text(self):
        self.send_text.delete('0.0', END)

    # 获取消息输入框内容
    def get_send_text(self):
        return self.send_text.get('0.0', END)