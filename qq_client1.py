from socket import *
import json
import re
import time
from multiprocessing import Process, Queue, Lock


def online(udp_sk, username, q, receive_port):
    while True:
        msg = "上线" + ":" + username + ":" + str(receive_port[1])
        print("上线中1")
        udp_sk.sendto(msg.encode("utf-8"), ("10.3.88.88", 9000))
        print("上线中2")
        json_dict1, server_addr = udp_sk.recvfrom(1024)
        print("上线中3")
        dict1 = json.loads(json_dict1.decode("utf-8"))
        print("上线中4")
        print(dict1)
        q.put(dict1)
        print("上线成功")


def recive_msg(udp_sk):
    while True:
        try:
            qq_msg, addr = udp_sk.recvfrom(1024)  # 阻塞状态，等待接收消息
            re_list = re.findall("88", qq_msg.decode("utf-8"))

            if "88" in re_list: continue
            print('来自[%s:%s]的一条消息:\033[1;34;43m%s\033[0m' % (addr[0], addr[1], qq_msg.decode('utf-8')))
        except Exception:
            continue

def send_msg(udp_sk, dict1):
    # 聊天
    p1 = input("请输入聊天对象：")
    p1_addr = tuple(dict1[p1])
    p1_addr = (p1_addr[0], int(p1_addr[1]))
    print(p1_addr)

    # 聊天过程
    while True:
        msg = input('请输入消息,回车发送,\n输入88告诉对方结束，输入q结束和他的聊天： ').strip()
        if msg == 'q': break
        if not msg: continue
        msg = username + '发给' + p1 + ': ' + msg
        udp_sk.sendto(msg.encode('utf-8'), p1_addr)

def offline(udp_sk):

    msg = "下线" + ":" + username
    udp_sk.sendto(msg.encode("utf-8"), ("10.3.88.88", 9000))

if __name__ == '__main__':
    udp_sk = socket(type=SOCK_DGRAM)
    udp_sk.bind(("10.3.88.88", 8081))

    receive_port = ("10.3.88.88", 8091)
    udp_sk_receive = socket(type=SOCK_DGRAM)
    udp_sk_receive.bind(receive_port)

    username = input("请输入用户名：")
    q = Queue(1)


    online_p = Process(target=online, args=(udp_sk, username, q, receive_port))
    online_p.start()
    recive_msg_p = Process(target=recive_msg, args=(udp_sk_receive, ))
    recive_msg_p.start()


    while True:

        menu = '''欢迎来到QQ聊天室
                1. 发送会话
                2. 下线'''
        print(menu)
        user_select = int(input("请输入您的选择"))
        # try:
        if user_select == 1:
            print("查询字典")
            dict1 = q.get()
            print("字典查询结束")
            send_msg(udp_sk, dict1)
        elif user_select == 2:
            offline(udp_sk)

            online_p.terminate()
            recive_msg_p.terminate()

            break
        else:
            print("请输入正确的选择")
        # except Exception:
        #     continue