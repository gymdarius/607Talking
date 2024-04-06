# 导入tkinter模块，这是Python的标准GUI库
from tkinter import *


# 定义注册界面类
class RegisterPanel:
    def __init__(self, quit_func, reg_func, close_callback):
        self.reg_frame = None
        self.btn_reg = None
        self.btn_quit = None
        self.user = None
        self.key = None
        self.confirm = None
        self.quit_func = quit_func
        self.reg_func = reg_func
        self.close_callback = close_callback

    # 初始化方法，创建注册窗口的框架和组件
    def show(self):
        # 创建注册窗口的框架，并设置相关配置
        self.reg_frame = Tk()
        self.reg_frame.configure(background="#f2f2f2")  # 设置背景颜色
        # 设置窗口关闭时的回调函数，用于关闭socket连接
        self.reg_frame.protocol("WM_DELETE_WINDOW", self.close_callback)

        # 获取屏幕尺寸，以计算窗口的位置
        screen_width = self.reg_frame.winfo_screenwidth()
        screen_height = self.reg_frame.winfo_screenheight()

        # 设置窗口的大小和位置
        width = 400  # 窗口宽度
        height = 320  # 窗口高度
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)  # 窗口的位置和大小设置
        self.reg_frame.geometry(gm_str)  # 应用位置和大小设置
        self.reg_frame.title("注册")  # 设置窗口标题
        self.reg_frame.resizable(width=False, height=False)  # 禁止调整窗口大小

        # 创建标题标签
        title_lable = Label(self.reg_frame, text="SCU聊天室 - 注册", font=("黑体", 16),
                            fg="white", bg="#80aaff")
        title_lable.pack(ipady=10, fill=X)  # 放置标题标签，设置垂直填充和水平填充

        # 创建注册表单的frame
        form_frame = Frame(self.reg_frame, bg="#f2f2f2")
        # 创建用户名输入标签和文本框
        Label(form_frame, text="用户名：", font=("黑体", 12), bg="#f2f2f2", fg="#003366") \
            .grid(row=0, column=1, pady=20)  # 放置用户名输入标签
        self.user = StringVar()  # 创建用户名的文本变量
        Entry(form_frame, textvariable=self.user, bg="#e3e3e3", width=30) \
            .grid(row=0, column=2, ipady=1)  # 放置用户名输入框

        # 创建密码输入标签和文本框，文本框内容以星号(*)显示以隐藏内容
        Label(form_frame, text="密码(必须包含英文)：", font=("黑体", 12), bg="#f2f2f2", fg="#003366") \
            .grid(row=1, column=1, pady=20)
        self.key = StringVar()  # 创建密码的文本变量
        Entry(form_frame, textvariable=self.key, show="*", bg="#e3e3e3", width=30) \
            .grid(row=1, column=2, ipady=1)

        # 创建确认密码输入标签和文本框
        Label(form_frame, text="确认密码：", font=("黑体", 12), bg="#f2f2f2", fg="#003366") \
            .grid(row=2, column=1, pady=20)
        self.confirm = StringVar()  # 创建确认密码的文本变量
        Entry(form_frame, textvariable=self.confirm, show="*", bg="#e3e3e3", width=30) \
            .grid(row=2, column=2, ipady=1)
        form_frame.pack(fill=X, padx=20, pady=10)  # 放置注册表单frame，设置水平填充和垂直填充

        # 创建按钮的frame
        btn_frame = Frame(self.reg_frame, bg="#f2f2f2")

        # 创建取消按钮，点击时调用quit_func函数
        self.btn_quit = Button(btn_frame, text="取消", bg="#4d88ff", fg="white", width=15,
                               font=('黑体', 11), command=self.quit_func)
        self.btn_quit.pack(side=LEFT, ipady=3)

        # 创建注册按钮，点击时调用reg_func函数
        self.btn_reg = Button(btn_frame, text="注册", bg="#4d88ff", fg="white", width=15,
                              font=('黑体', 11), command=self.reg_func)
        self.btn_reg.pack(side=RIGHT, ipady=3)

        btn_frame.pack(fill=X, padx=20, pady=20)  # 放置按钮frame，设置水平填充和垂直填充
        self.reg_frame.mainloop()  # 启动Tkinter事件循环

    # 关闭注册窗口的方法
    def close(self):
        if self.reg_frame == None:
            print("no interface error")
        else:
            self.reg_frame.destroy()  # 摧毁窗口

    # 获取输入的用户名、密码、确认密码的方法
    def get_input(self):
        return self.user.get(), self.key.get(), self.confirm.get()  # 返回输入的用户名、密码、确认密码
