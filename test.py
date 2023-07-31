d = {
    'test':1,
    'test':2,
}

def fun(**kwargs):
    for key, val in kwargs.items():
        # print(f"{key}={val}")
        # 打印key的名字
        print(key)


if __name__ == "__main__":
    fun(a=2,b=3)