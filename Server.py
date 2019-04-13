#!/usr/bin/python3

import requests
import socket
import time
import sim800l
# 建立一个服务端

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('0.0.0.0',9001)) #绑定要监听的端口
server.listen(5) #开始监听 表示可以使用五个链接排队
while True:# conn就是客户端链接过来而在服务端为期生成的一个链接实例
    print('等待连接中...')
    conn,addr = server.accept() #等待链接,多个链接的时候就会出现问题,其实返回了两个值
    print(conn,addr)
    while True:
        try:
            databin = conn.recv(1024)  #接收数据
            print('recive.bin:',databin) #打印接收到的数据
            print('recive:',databin.decode()) #打印接收到的数据
            datas = databin.decode()

            if len(datas) >= 50:
                if datas.find('08') >= 0:
                    d = sim800l.decode(datas)
                elif datas.find('91') >= 0:
                    d = sim800l.decode(datas)
                else:
                    break
                    
                r = requests.post("http://localhost/add",data={'content': d})
                # r = requests.post("http://localhost/add",data={'content':data[1],'status':data[0]})
                if 200 == r.status_code:
                    print('数据提交成功！')
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    print('--------------------')
                # 		break
                #         # conn.send(data.upper()) #然后再发送数据'
                    break
            else:
                break
        except ConnectionResetError as e:
            print('关闭了正在占线的链接！')
            break
    conn.close()
