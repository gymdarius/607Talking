from tkinter import *


# 定义一个名为LoginPanel的类，用于创建登录界面
class LoginPanel:

    # 初始化方法，接收登录函数、注册函数和窗口关闭回调函数
    def __init__(self, login_func, reg_func, close_callback):
        self.login_frame = None  # 登录窗口框架
        self.btn_reg = None  # 注册按钮
        self.btn_login = None  # 登录按钮
        self.user = None  # 用户名变量
        self.key = None  # 密码变量
        self.login_func = login_func  # 登录函数
        self.reg_func = reg_func  # 注册函数
        self.close_callback = close_callback  # 窗口关闭回调函数

    # 显示登录界面的方法
    def show(self):
        self.login_frame = Tk()  # 创建Tkinter窗口对象
        self.login_frame.configure(background="#f2f2f2")  # 设置窗口背景颜色
        # 设置窗口关闭按钮回调，用于退出时关闭socket连接
        self.login_frame.protocol("WM_DELETE_WINDOW", self.close_callback)
        screen_width = self.login_frame.winfo_screenwidth()  # 获取屏幕宽度
        screen_height = self.login_frame.winfo_screenheight()  # 获取屏幕高度
        width = 360  # 设置窗口宽度
        height = 260  # 设置窗口高度
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2, (screen_height - 1.2 * height) / 2)  # 设置窗口位置
        self.login_frame.geometry(gm_str)  # 设置窗口大小和位置
        self.login_frame.title("登录")  # 设置窗口标题
        self.login_frame.resizable(width=False, height=False)  # 设置窗口不可调整大小

        # 创建标题标签
        title_lable = Label(self.login_frame, text="SCU聊天室 - 登录", font=("黑体", 16),
                            fg="white", bg="#80aaff")
        title_lable.pack(ipady=10, fill=X)  # 布局标题标签

        # 创建登录表单frame
        form_frame = Frame(self.login_frame, bg="#f2f2f2")
        Label(form_frame, text="用户名：", font=("黑体", 12), bg="#f2f2f2", fg="#003366") \
            .grid(row=0, column=1, pady=20)  # 创建用户名标签
        Label(form_frame, text="密  码：", font=("黑体", 12), bg="#f2f2f2", fg="#003366") \
            .grid(row=1, column=1, pady=20)  # 创建密码标签
        # 获取输入的用户名和密码
        self.user = StringVar()  # 创建用户名变量
        self.key = StringVar()  # 创建密码变量
        # 创建用户名和密码的输入框
        Entry(form_frame, textvariable=self.user, bg="#e3e3e3", width=30) \
            .grid(row=0, column=2, ipady=1)  # 创建用户名输入框
        Entry(form_frame, textvariable=self.key, show="*", bg="#e3e3e3", width=30) \
            .grid(row=1, column=2, ipady=1)  # 创建密码输入框
        # 绑定回车登录
        self.login_frame.bind("<Return>", self.login_on_enter)
        form_frame.pack(fill=X, padx=20, pady=10)  # 布局登录表单frame

        # 创建按钮frame
        btn_frame = Frame(self.login_frame, bg="#f2f2f2")
        self.btn_reg = Button(btn_frame, text="注册", bg="#4d88ff", fg="white", width=15,
                              font=('黑体', 11), command=self.reg_func).pack(side=LEFT, ipady=3)  # 创建注册按钮
        self.btn_login = Button(btn_frame, text="登录(Enter)", bg="#4d88ff", fg="white", width=15,
                                font=('黑体', 11), command=self.login_func).pack(side=RIGHT, ipady=3)  # 创建登录按钮
        btn_frame.pack(fill=X, padx=20, pady=20)  # 布局按钮frame

        self.login_frame.mainloop()  # 进入Tkinter事件循环
        # Thread(target=self.login_frame.mainloop).start()  # 启动一个新线程来运行事件循环，但这通常不是必要的

    # 关闭登录界面的方法
    def close(self):
        if self.login_frame == None:
            print("no interface error")  # 如果登录窗口未创建，则打印错误信息
        else:
            self.login_frame.destroy()  # 否则，销毁登录窗口

    # 获取输入的用户名密码的方法
    def get_input(self):
        return self.user.get(), self.key.get()  # 返回用户输入的用户名和密码

    # 绑定回车登录的事件处理方法
    def login_on_enter(self, event):
        if event.keysym == "Return":  # 如果用户按下回车键
            self.login_func()  # 调用登录函数
