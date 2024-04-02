import datetime


now = datetime.datetime.now()
greet=" "
print("print:")
print(greet)
if 5 <= now.hour < 12:
    greet= "早上好 "
elif 12 <= now.hour < 18:
    greet= "中午好 "
elif 18 <= now.hour < 21:
    greet= "下午好 "
else:
    greet= "晚上好 "
print(greet)

greet=greet + "hello"+greet
print(greet)
