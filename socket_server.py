#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # 标准的回环地址 (localhost)
PORT = 65432  # 监听的端口 (非系统级的端口: 大于 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print('开始监听', HOST, PORT)
    # 拒绝之前, 最多挂起的数量
    s.listen(5)
    conn, addr = s.accept()
    with conn:
        print('与', addr, '建立连接')
        while True:
            # buffersize 是接收的最大数量
            data = conn.recv(1024)
            print('接收数据', data)
            if not data:
                break
            # 开始发送
            print('发送数据', data)
            conn.sendall(data)
    
    print('连接断开')
