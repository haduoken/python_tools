import serial, time

# def convert_hex(string):
#     result = []
#     for s in string:
#         number = int(s, 16)
#         result.append(number)
#     return result
#
#
# class Sonar:
#     def __init__(self, port):
#         self.sonar = serial.Serial(port=port, stopbits=1)
#
#     def read(self):
#         while True:
#             self.sonar.write(['b1', '10', '01'])
#             print(self.sonar.read(7))
#             time.sleep(0.1)
# a = ['1','2','3','4']

# a = '12A4'

# b = int(a,16)
# print(b)

# a = bytes('123')
a = b'xff'
b = bytes([])


print(a)
print(b)
# print(c)

# 写的16进制字符串 ['0x12','0x22'] 能够转换成bytes
a = '0x12'
# 1将str的list 转换成int list
a = int(a, 16)
# 2
a = bytes([a])
print(a)

# a = bytes.fromhex('0x11 0xAB 0xCC 0xde')
# print(a)


# print(a[0],a[1])
# b = a.hex()

# for data in b:

# print(a.decode())
# print(a.index(1))
# print(b[0])

a = bytes.fromhex('23 99 88 23 41 32')

for i in range(0,len(a),3):
    c = a[i:i+3]
    print(c)
    
    c = c.hex()
    print(c)
    # print(int(c))

# a = bin(b[0])
# a.join(b)
# print(a)
# print(str(b))
# print(hex(b[0]))
# c = ''.join(b)
# for data in b:
#     c.join()
# c = bin(b[0])
# a = b'11'
# print(a.hex())
# print(c)

# print(c[-3:])
# for i in range(3,)
# num = int((len(c) - 2) / 4)
# for i in range(num):
#     s_index = 2 + num * 4
#     e_index = s_index + 4
#     print(c[s_index:e_index + 1])

# print(a)
# print(a[0],a[1])
# b = a[:]
# print(type(b))
# print(a[1])
# print(int(a[0],10)[1])
# b = bin(a[0])
# print(b)


# 将读取到的bytes 转换成int list
# a = int(a,16)
# print(a)
