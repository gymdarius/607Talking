import re

def is_valid_password(password):
    # 定义正则表达式，检查字符串是否满足要求
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*-+?.]).{8,}$'
    return bool(re.match(pattern, password))

# 测试字符串
password = input()
if is_valid_password(password):
    print("密码有效。")
else:
    print("密码无效。")
