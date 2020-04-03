#!/usr/bin/python3
# import zmq
# import base64
#
# context = zmq.Context()
# print("Connecting to hello world server...")
# socket = context.socket(zmq.REQ)
# socket.connect("tcp://172.16.1.231:9999")
# for request in range(10):
#     print("Sending request %s ..." % request)
#
#     # socket.send(
#     #     b'{"data":{"interval":30,"sn":"00-A0-C9-16-01-66","secret":"A"},"cmd":"heartBeat","timestamp":1581644636051}')
#     socket.send(a)
#
#     message = socket.recv()
#     print("Received reply %s [ %s ]" % (request, message))

# import socket
# import time
#
# a = '123'
# a = a.encode('utf-8')
# s = socket.socket()
# s.connect(('172.16.1.231', 9999))
# s.send(a)
#
# time.sleep(10)
# import time
# print(round(time.time()*1000))

n =10
path = [[0] * n for i in range(n)]
print(path)