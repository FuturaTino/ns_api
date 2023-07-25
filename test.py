from threading import Thread
from queue import Queue

q = Queue(5)
i = 1

def producer():
    global i
    q.put(f"包子{i}")
    i += 1

def consumer():
    global i
    q.get()
    i -= 1

if __name__ == "__main__":
    while True:
        a = input("输入1生产，输入2消费")
        if a == "1":
            producer()
        elif a == "2":
            consumer()
        else:
            break
