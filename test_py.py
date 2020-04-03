#!/usr/bin/python3

dist = [[float('inf')] * 4 for i in range(4)]

dist[0][0] = 0
dist[1][1] = 0
dist[2][2] = 0
dist[3][3] = 0

dist[0][1] = 2
dist[1][0] = 2

dist[0][3] = 7
dist[3][0] = 7

dist[1][3] = 8
dist[3][1] = 8

dist[1][2] = 3
dist[2][1] = 3

dist[2][3] = 6
dist[3][2] = 6

# for k in range(4):
#     for i in range(4):
#         for j in range(4):
#             if dist[i][j] > dist[i][k] + dist[k][j]:
#                 dist[i][j] = dist[i][k] + dist[k][j]
#
# print(dist)

a = float('inf')
b = float('inf') + 5

